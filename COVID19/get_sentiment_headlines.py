from google.cloud import bigquery, storage
from get_big_query_table import get_table_data
from test_gcp_analyze_sentiment import sample_analyze_sentiment
from datetime import datetime
from ManageJson import ManageJsonFile

import os
import pandas as pd
import pytz
from time import sleep
import traceback

################################################################################################################################
# COVID News Feed Data To BigQuery ETL
# Initial ingestion: 27 March 2020

# This script calculate sentiment from text data and pushes to BigQuery

# Process
# - Retrieves headlines from articles
# - Uses the LanguageServiceClient API of Google's Natural Language API to,
#     - Calculate magnitude and score

# Bugs
# - None so far..

# Feature updates
#     - Update by range


################################################################################################################################
# Functions
################################################################################################################################


################################################################################################################################
# Initialize
################################################################################################################################

# process handlers
MJ = ManageJsonFile()
file_process_meta = 'meta/get_sentiment_headlines.json'

# Setting credentials
credential_path = "/home/nroshania/Personal-Coding-Projects/COVID19/private/covid19-2020-0fb8513fcbd8.json"
# credential_path = "C:\\Users\\nrosh\\Desktop\\Personal Coding Projects\\COVID19\\private\\covid19-2020-0fb8513fcbd8.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# load etl meta information
process_meta = MJ.load_json(file_process_meta)

################################################################################################################################
# Get Sentiment Score and Magnitude
################################################################################################################################

# re-initialize state variables
unique_id = []
source = []
date = []
headline = []
link = []
score = []
magnitude = []

row_count = 0
gotSentiment = True

# loop etl with external control

while (process_meta["headline_sentiment_analysis_meta"]["keep_updating"] == 1):

    # decide what type of update is required
    try:

        # update all the history or a range over days
        if process_meta["headline_sentiment_analysis_meta"]["update_history"] == 1:
            
            # if all history otherwise consider the non-inclusive range
            if  process_meta["headline_sentiment_analysis_meta"]["update_all"] == 1:

                print("{} - Updating all data.".format(pytz.timezone("US/Pacific").localize(datetime.now())))

                # update all
                query = """
                        select *
                        from `covid19-2020-272000.covid19.articles`
                        where CAST(date AS DATE) != CAST(current_date('America/Los_Angeles') AS DATE)
                    """
                write_disposition_bq = "WRITE_TRUNCATE"
            
            else:
                
                # update by range
                update_start = process_meta["headline_sentiment_analysis_meta"]["update_start"]
                update_end   = process_meta["headline_sentiment_analysis_meta"]["update_end"]
                print("{} - Updating by range: {} to {}".format(
                    pytz.timezone("US/Pacific").localize(datetime.now()),
                    update_start,
                    update_end)
                    )

                # there must be a better way to do this
                query = 'select *\nfrom `covid19.articles`\nwhere date BETWEEN CAST(\"{}\" as date) AND CAST(\"{}\" as date)\norder by date asc\n'.format(update_start, update_end)
                write_disposition_bq = "WRITE_APPEND"
        else:

            # get sentiment for today only

            print("{} - Updating today only.".format(pytz.timezone("US/Pacific").localize(datetime.now())))

            query = """
                    select *
                    from `covid19-2020-272000.covid19.articles`
                    where CAST(date AS DATE) = CAST(current_date('America/Los_Angeles') AS DATE)
                """
            write_disposition_bq = "WRITE_APPEND"

        # get updated data from BigQuery
        GCP_QueryJob = get_table_data(query)

        print("{} - Starting sentiment and magnitude calculations...".format(
            pytz.timezone("US/Pacific").localize(datetime.now())))

        # get results
        for row in GCP_QueryJob:

            row_count += 1

            # AnalyzeSentimentResponse object
            try:

                response = sample_analyze_sentiment(row["headline"])

                # append dictionaries
                # unique_id.append(row_count) # not neccesary, create another table with unique id
                date.append(datetime.strftime(row["date"], format='%Y-%m-%d'))
                source.append(row["source"])
                link.append(row["link"])
                headline.append(row["headline"])
                score.append(round(response.document_sentiment.score, 3))
                magnitude.append(
                    round(response.document_sentiment.magnitude, 3))

                # curb api limit
                if (row_count % 600) == 0:
                    print("{} - 600 results reached. Goodnight...".format(
                        pytz.timezone("US/Pacific").localize(datetime.now())))
                    sleep(60)

            except Exception as e:
                print("**{} - Failed to get acquire setiment".format(
                    pytz.timezone("US/Pacific").localize(datetime.now())))
                print(e)
                break
                gotSentiment = False

        if gotSentiment:

            try:
                # define dataframe and ensure types
                df_scores = pd.DataFrame({
                    # "id": unique_id,
                    "date": date,
                    "source": source,
                    "link": link,
                    "headline": headline,
                    "score": score,
                    "magnitude": magnitude
                })

                # ensure type conversion
                # df_scores.id = df_scores.id.astype('int')
                df_scores.date = pd.to_datetime(df_scores.date)
                df_scores.source = df_scores.source.astype('str')
                df_scores.link = df_scores.link.astype('str')
                df_scores.headline = df_scores.headline.astype('str')
                df_scores.score = df_scores.score.astype('float')
                df_scores.magnitude = df_scores.magnitude.astype('float')

                df_scores.to_csv(
                    "data/headline_sentiment.csv", encoding='utf-8')
                print(
                    "{} - Data exported".format(pytz.timezone("US/Pacific").localize(datetime.now())))

                try:

                    # control big query transfer externally
                    if process_meta["bq_info"]["headline_sentiment_analysis"]["start_big_query"] == 1:
                        # load to BigQuery
                        print("{} - Starting BigQuery transfer".format(
                            pytz.timezone("US/Pacific").localize(datetime.now())))
                        client = bigquery.Client(
                            project=process_meta["bq_info"]["headline_sentiment_analysis"]["project_id"])
                        dataset_id = process_meta["bq_info"]["headline_sentiment_analysis"]["dataset_id"]
                        table_id = process_meta["bq_info"]["headline_sentiment_analysis"]["table"]
                        dataset_ref = client.dataset(dataset_id)
                        table_ref = dataset_ref.table(table_id)

                        # overwrite data
                        job_config = bigquery.LoadJobConfig(
                            write_disposition=write_disposition_bq,
                        )

                        # Make an API request
                        job = client.load_table_from_dataframe(
                            df_scores,
                            table_ref,
                            job_config=job_config
                        )

                        job.result()  # Wait for the job to complete.

                        print("{} - BigQuery transfer complete".format(
                            pytz.timezone("US/Pacific").localize(datetime.now())))
                    else:
                        print("{} - BigQuery transfer terminated by user".format(
                            pytz.timezone("US/Pacific").localize(datetime.now())))
                except Exception as e:
                    print("**{} - Failed to send to BigQuery".format(
                        pytz.timezone("US/Pacific").localize(datetime.now())))
                    print(e)
            except Exception as e:
                print("**{} - Failed to write dataframe to csv".format(
                    pytz.timezone("US/Pacific").localize(datetime.now())))
                print(e)
    except Exception as e:
        print("**{} - Failed to get BigQuery data".format(
            pytz.timezone("US/Pacific").localize(datetime.now())))
        print(e)

    # read process_batch_meta file to check update on termination
    process_meta = MJ.load_json(file_process_meta)

    # halt ETL for specified time
    print("**{} - ETL paused {}s".format(pytz.timezone("US/Pacific").localize(datetime.now()),
                                         process_meta["headline_sentiment_analysis_meta"]["pull_cycle_hr"]*60*60))
    sleep(process_meta["headline_sentiment_analysis_meta"]
          ["pull_cycle_hr"]*60*60)

    # END WHILE
