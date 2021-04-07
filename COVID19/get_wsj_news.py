# library dependencies
import pandas as pd
import numpy as np
import requests
import os
import re

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from ManageJson import ManageJsonFile
from google.cloud import bigquery, storage
from time import sleep

################################################################################################################################
# COVID News Feed Data To BigQuery ETL
# Initial ingestion: 27 March 2020

# This script gathers headlines from wsj archives over a predefined period

# Process
# - User can choose to update history or not
# - If chosen to update history, will backtrack specified days and gather sources
# - If chosen to not update, data will update for the current day
#     - BigQuery ETL will trigger when complete

# BigQuery Output Schema
# - wsj_table
#     - source
#     - date
#     - headline


# Bugs
# - Reduced get request frequency to 10s
# - Removed empty rows that read_csv was somehow reading

# Feature updates
#     - None so far..

################################################################################################################################
# Functions
################################################################################################################################

def make_request(url, user_agent):

    # make get request to url

    client = requests.Session()
    response = client.get(
        url,
        headers={'User-Agent': user_agent}
    )
    if (response.status_code) == 200:
        # get html
        html = response.content
        soup = BeautifulSoup(html, "html.parser")

        return response, html, soup
    else:
        return False

# source: https://stackoverflow.com/questions/3424899/whats-the-simplest-way-to-subtract-a-month-from-a-date-in-python


def monthdelta(date, delta):
    return date + delta


def get_wsj_headlines(days_to_go_back, day_to_end, day, process_meta):

    # Data structures
    date = []
    headline = []
    headline_link = []
    source = []

    # iterate over days till today
    for days_before in np.arange(days_to_go_back, day_to_end, 1):

        end_day = monthdelta(datetime.now(), days_before*day)

        # get url
        url = WSJ_URL(end_day.strftime("%Y%m%d"))

        sleep(10)

        # get request data
        response, html, soup = make_request(url, user_agent)

        # If response is not false
        if response.status_code == 200:

            # get the code
            code = re.findall(
                r'typography--serif-display--([\w\W]{1,8})', str(html))[0]
            # print(code)
            headlines = soup.find_all(
                'h3', {"class": "typography--serif-display--{}".format(code)})

            if headlines:

                print("{} \t- Headlines found for: {}".format(datetime.now(), url))

                # update process meta data
                process_meta["wsj_extraction"]["got_headlines"] = 1
                process_meta = MJ.update_json(
                    process_meta, ignore_keys=["wsj_meta"])

                # get headlines and associated links
                for h in headlines:
                    h_link = h.find_all("a")
                    for link in h_link:
                        headline.append(h.text)
                        date.append(end_day.strftime("%Y-%m-%d"))
                        source.append("wsj")
                        headline_link.append(link["href"])

            else:
                # start trying to headlines by attempting a get every 10s

                # update process meta data
                process_meta["wsj_extraction"]["got_headlines"] = 0
                process_meta = MJ.update_json(
                    process_meta, ignore_keys=["wsj_meta"])

                while process_meta["wsj_extraction"]["got_headlines"] == 0:

                    print(
                        "**{} \t- Retrying headlines for: {}".format(datetime.now(), url))

                    # get request data
                    response, html, soup = make_request(url, user_agent)

                    # If response is not false
                    if response.status_code == 200:

                        # get the code
                        code = re.findall(
                            r'typography--serif-display--([\w\W]{1,8})', str(html))[0]
                        # print(code)
                        headlines = soup.find_all(
                            'h3', {"class": "typography--serif-display--{}".format(code)})

                        # if there is atleast one headline then append to data structure
                        if headlines:
                            print(
                                "{} \t- Headlines found for: {}".format(datetime.now(), url))

                            # update process meta data
                            process_meta["wsj_extraction"]["got_headlines"] = 1
                            process_meta = MJ.update_json(
                                process_meta, ignore_keys=["wsj_meta"])

                            # get headlines and associated links
                            for h in headlines:
                                h_link = h.find_all("a")
                                for link in h_link:
                                    headline.append(h.text)
                                    date.append(end_day.strftime("%Y-%m-%d"))
                                    source.append("wsj")
                                    headline_link.append(link["href"])

                            break

                        else:
                            print(
                                "**{} - Failed to get headlines for: {}".format(datetime.now(), url))
                    else:
                        print(
                            "**{} - Failed to connect to server. Trying again.".format(datetime.now()))
                        sleep(10)

        else:
            print("**{} - Failed to find data at: {}".format(datetime.now(), url))
            return False, False, False

    return headline, date, source, headline_link

# test BigQuery Authentication


def implicit():

    # pip3 install --upgrade google-cloud-bigquery
    # pip3 install --upgrade google-cloud-storage

    # VM setting up python 3 environment
        # - https://cloud.google.com/python/setup
        # - install pip then upgrade to new version of pip

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.

    # set global environment
    credential_path = "/home/nroshania/Personal-Coding-Projects/COVID19/private/covid19-2020-0fb8513fcbd8.json"
    # credential_path = "C:\\Users\\nrosh\\Desktop\\Personal Coding Projects\\COVID19\\private\\covid19-2020-0fb8513fcbd8.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    if len(buckets) < 1:
        print("\n**Pre-authentication setup...\n")


def push_to_BigQuery(filename, process_meta, write_instruction):

    ################################################################################################################################
    # upload data to bigquery table
    ################################################################################################################################

    # source:
    # - https://cloud.google.com/bigquery/docs/loading-data-local
    # - authentication: https://cloud.google.com/docs/authentication/getting-started

    if process_meta["bq_info"]["wsj_project"]["start_big_query"] == 1:

        try:
            print("{} - BigQuery ETL started".format(datetime.now()))

            # set global environment and connect to BQ
            credential_path = "/home/nroshania/Personal-Coding-Projects/COVID19/private/covid19-2020-0fb8513fcbd8.json"
            # credential_path = "C:\\Users\\nrosh\\Desktop\\Personal Coding Projects\\COVID19\\private\\covid19-2020-0fb8513fcbd8.json"
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
            client = bigquery.Client(
                project=process_meta["bq_info"]["wsj_project"]["project_id"])

            # Define meta for ETL
            dataset_id = process_meta["bq_info"]["wsj_project"]["dataset_id"]
            table_id = process_meta["bq_info"]["wsj_project"]["table_cases"]
            print(
                "{} - BQ dataset and table info recieved from process_meta".format(datetime.now()))

            # setup dataset, table and job config refernces
            dataset_ref = client.dataset(dataset_id)
            table_ref = dataset_ref.table(table_id)
            job_config = bigquery.LoadJobConfig()
            job_config.source_format = bigquery.SourceFormat.CSV
            job_config.skip_leading_rows = 1
            job_config.autodetect = True
            # overwrite table WRITE_TRUNCATE and append with WRITE_APPEND
            job_config.write_disposition = write_instruction

            print("{} \t- BQ dataset ref, table ref and job config complete. Starting transfer...".format(datetime.now()))

            with open(filename, "rb") as source_file:
                job = client.load_table_from_file(
                    source_file, table_ref, job_config=job_config)
                # job = client.load_table_from_dataframe(df_updated, table_ref, job_config=job_config)

            job.result()  # Waits for table load to complete.

            print("{} \t- BigQuery ETL complete. {} rows loaded into {} of {}:{}".format(
                datetime.now(),
                job.output_rows,
                table_id,
                process_meta["bq_info"]["wsj_project"]["project_id"],
                dataset_id
            ))

        except:
            print("\n**{} - Failed to exectute BigQuery ETL...".format(datetime.now()))
    else:
        print("\n**{} - BigQuery ETL disabled.".format(datetime.now()))

################################################################################################################################
# Initialize
################################################################################################################################


implicit()

# agency urls


def WSJ_URL(x): return "https://www.wsj.com/news/archive/{}".format(x)


data_export_destination = "data/wsj_headlines.csv"

# request headers
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"

# process handlers
MJ = ManageJsonFile()
file_process_meta = 'meta/previous_batch_meta.json'

# load etl meta information
process_meta = MJ.load_json(file_process_meta)

################################################################################################################################
# Start extraction process
################################################################################################################################

# get date
day = timedelta(days=1)

# start_date = end_day - days_before*day

if process_meta["wsj_meta"]["kill_process"] == 0:

    print("**{} - Starting extraction process...".format(datetime.now()))

    while (process_meta["wsj_meta"]["keep_updating"] == 1):

        # if update history required
        if process_meta["wsj_meta"]["update_history"] == 1:

            # Initialize data structures
            head_line = []
            date_published = []
            source = []
            head_line_link = []

            # get data
            head_line, date_published, source, head_line_link = get_wsj_headlines(
                process_meta["wsj_meta"]["timeline_of_update_days"], 0, day, process_meta)

            # if data was found, then export to csv
            if head_line:
                print("{} - Headline extractions complete.".format(datetime.now()))

                pd.DataFrame(
                    {
                        "source": source,
                        "date": date_published,
                        "headline": head_line,
                        "link": head_line_link
                    }
                ).to_csv(data_export_destination, encoding='utf-8-sig', index=False)

                # start BigQuery ETL
                push_to_BigQuery(data_export_destination,
                                 process_meta, "WRITE_TRUNCATE")
                break

            else:
                print(
                    "\n**{} - Critical wsj extraction failure: Failed to find data".format(datetime.now()))

        else:
            # update for today only
                # - Read data from wsj_headlines.csv
                # - make a request for today
                # - append to dataframe and export

            # read existing data
            # df = pd.read_csv(data_export_destination, header=0)
            # df.dropna(how="all", inplace=True)

            # print(len(df.iloc[:, 1]))
            # print(df.columns)

            # initialize data structures
            update_head_line = []
            update_date_published = []
            update_source = []
            update_head_line_link = []

            # get current data
            update_head_line, update_date_published, update_source, update_head_line_link = get_wsj_headlines(
                -1, 0, day, process_meta)

            print(len(update_head_line))

            # if data was found, then export to csv
            if update_head_line:
                print("{} - Update complete.".format(datetime.now()))

                # initialize update dataframe
                df_today = pd.DataFrame(
                    {
                        "source": update_source,
                        "date": update_date_published,
                        "headline": update_head_line,
                        "link": update_head_line_link
                    }
                )

                # append data sets
                # df_updated = df.append(df_today)
                df_updated = df_today

                # ensure type conversion
                df_updated.source = df_updated.source.astype('str')
                df_updated.link = df_updated.link.astype('str')
                df_updated.headline = df_updated.headline.astype('str')
                df_updated.date = pd.to_datetime(df_updated.date)

                # export to csv
                df_updated.to_csv(data_export_destination,
                                  encoding='utf-8-sig', index=False)

                # start BigQuery ETL
                push_to_BigQuery(data_export_destination,
                                 process_meta, "WRITE_APPEND")

            else:
                print(
                    "\n**{} - Critical wsj extraction failure: Failed to find data".format(datetime.now()))

        # read process_batch_meta file to check update on termination
        process_meta = MJ.load_json(file_process_meta)

        print("**{} - ETL paused {}s".format(datetime.now(),
                                             process_meta["wsj_meta"]["pull_cycle_hr"]*60*60))
        sleep(process_meta["wsj_meta"]["pull_cycle_hr"]*60*60)

    print("**{} - Extraction ended by user.".format(datetime.now()))
else:
    print("\n**{} - WSJ news archive data search terminated...".format(datetime.now()))
