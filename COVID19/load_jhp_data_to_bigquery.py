import pandas as pd
from time import sleep
from datetime import datetime
import json
import os
from google.cloud import bigquery, storage
from ManageJson import ManageJsonFile
import platform

################################################################################################################################
# COVID CSSEGISandData To BigQuery ETL
# Initial ingestion: 27 March 2020

# This script facilitates the ingestions of COVID CSSEGISandData to GoogleBigQuery by
#     - Streaming CSSEGISandData into pandas dataframe via url 
#     - Transforming data via melt in preperation for `covid19-2020-272000.covid19.cases` 
#     - Authenticates and loads to BigQuery

# Features
#     - previous_batch_meta.json file used to control
#         - BigQuery project and table information
#         - Process statuses
#         - CSSEGISandData url sources

# Bugs
#     - Script resets process_batch_meta.json to initial

# Feature updates 
#     - None so far..

################################################################################################################################


################################################################################################################################
# Initialization and Function Definitions
################################################################################################################################

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
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    if len(buckets) < 1:
        print("\n**Pre-authentication setup...\n")

################################################################################################################################
# Connect to BigQuery and confirm CSSEGISandData success
################################################################################################################################

implicit()

# initialize
MJ = ManageJsonFile()
file_process_meta = 'meta/previous_batch_meta.json'

# load etl meta information
process_meta = MJ.load_json(file_process_meta)

# if allowed to update
if process_meta["meta"]["kill_process"] == 0:

    # Halt ETL over user defined period

    while (process_meta["meta"]["keep_updating"] == 1):

        # try to authenticate gcloud credentials
        try:
            # set global environment and connect to BQ
            credential_path = "/home/nroshania/Personal-Coding-Projects/COVID19/private/covid19-2020-0fb8513fcbd8.json"
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
            client = bigquery.Client(project=process_meta["bq_info"]["covid_project"]["project_id"])

            # update process_meta json to continue
            process_meta["bq_info"]["covid_project"]["BQ_Authentication"] = 1
            process_meta = MJ.update_json(process_meta, ignore_keys=["meta"])

        except:

            # update process_meta json to end
            process_meta["bq_info"]["covid_project"]["BQ_Authentication"] = 0
            process_meta = MJ.update_json(process_meta, ignore_keys=["meta"])
            print("\n**{} - BigQuery Authentication Error: Failed to connect to Big Query".format(datetime.now()))

        # if authentication is complete
        if process_meta["bq_info"]["covid_project"]["BQ_Authentication"] == 1:
            
            # John Hopkins raw csv paths
            url_confirmed = process_meta["sources"]["confirmed"]
            url_deaths    = process_meta["sources"]["deaths"]
            url_recovered = process_meta["sources"]["recovered"]

            try:
                # mark originals
                df_original_confirmed = pd.read_csv(url_confirmed)
                df_original_deaths = pd.read_csv(url_deaths)
                df_original_recovered = pd.read_csv(url_recovered)

                # update CSSEGISandData_found feedback
                process_meta["bq_info"]["covid_project"]["CSSEGISandData_found"] = 1
                process_meta = MJ.update_json(process_meta, ignore_keys=["meta"])
            except:
                # update process_meta json to end
                process_meta["bq_info"]["covid_project"]["CSSEGISandData_found"] = 0
                process_meta = MJ.update_json(process_meta, ignore_keys=["meta"])
                print("**{} \t- Failed to get CSSEGISandData...".format(datetime.now()))

            # If CSSEGISandData_found
            if process_meta["bq_info"]["covid_project"]["CSSEGISandData_found"] == 1:
                
                try:
                    # label by type
                    df_original_confirmed["case_type"] = "confirmed"
                    df_original_deaths["case_type"]    = "deaths"
                    df_original_recovered["case_type"] = "recovered"

                    # melt dataframe by all except data
                    df_original_confirmed = df_original_confirmed.melt(id_vars=['Country/Region', 'Province/State', 'Lat', 'Long', 'case_type'])
                    df_original_deaths = df_original_deaths.melt(      id_vars=['Country/Region', 'Province/State', 'Lat', 'Long', 'case_type'])
                    df_original_recovered = df_original_recovered.melt(id_vars=['Country/Region', 'Province/State', 'Lat', 'Long', 'case_type'])

                    # concat dataframes
                    df_all = pd.concat([
                        df_original_confirmed,
                        df_original_deaths,
                        df_original_recovered
                    ], axis=0)

                    # rename columns
                    df_all.rename(columns={
                        'Country/Region': 'country_region',
                        'Province/State': 'province_state',
                        'Lat'           : 'lat',
                        'Long'          : 'long',
                        'variable'      : 'date',
                        'value'         : 'cases'
                    }, inplace=True)

                    # replace null_values with blank
                    df_all.province_state.fillna("Entire", inplace=True)

                    # replace types
                    df_all.case_type.replace({
                        "confirmed": "Confirmed",
                        "deaths"   : "Deaths",
                        "recovered": "Recovered"
                    }, inplace=True)

                    # ensure type conversions
                    df_all.country_region = df_all.country_region.astype('str')
                    df_all.province_state = df_all.province_state.astype('str')
                    df_all.case_type      = df_all.case_type.astype('str')
                    df_all.date           = pd.to_datetime(df_all.date)

                    df_all.to_csv("df_all.csv", index=False)
                    process_meta["bq_info"]["covid_project"]["start_big_query"] = 1
                except:
                    # update process_meta json to end
                    process_meta["bq_info"]["covid_project"]["start_big_query"] = 0
                    process_meta = MJ.update_json(process_meta, ignore_keys=["meta"])
                    print("**{} \t- Failed to transform CSSEGISandData...".format(datetime.now()))
                    
                if process_meta["bq_info"]["covid_project"]["start_big_query"] == 1:
                    ################################################################################################################################
                    # upload data to bigquery table
                    ################################################################################################################################

                    # source: 
                    # - https://cloud.google.com/bigquery/docs/loading-data-local
                    # - authentication: https://cloud.google.com/docs/authentication/getting-started
                    try:
                        print("{} - BigQuery ETL started".format(datetime.now()))

                        # # implicit()

                        # Define meta for ETL
                        filename   = 'df_all.csv'
                        dataset_id = process_meta["bq_info"]["covid_project"]["dataset_id"]
                        table_id   = process_meta["bq_info"]["covid_project"]["table_cases"]
                        print("{} - BQ dataset and table info recieved from process_meta".format(datetime.now()))

                        # setup dataset, table and job config refernces
                        dataset_ref                  = client.dataset(dataset_id)
                        table_ref                    = dataset_ref.table(table_id)
                        job_config                   = bigquery.LoadJobConfig()
                        job_config.source_format     = bigquery.SourceFormat.CSV
                        job_config.skip_leading_rows = 1
                        job_config.autodetect        = True
                        job_config.write_disposition = "WRITE_TRUNCATE" # overwrite table

                        print("{} \t- BQ dataset ref, table ref and job config complete. Starting transfer...".format(datetime.now()))

                        with open(filename, "rb") as source_file:
                            job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
                            # job = client.load_table_from_dataframe(df_all, table_ref, job_config=job_config)

                        job.result()  # Waits for table load to complete.

                        print("{} \t- BigQuery ETL complete. {} rows loaded into {} of {}:{}".format(
                            datetime.now(), 
                            job.output_rows,
                            table_id,
                            process_meta["bq_info"]["covid_project"]["project_id"],
                            dataset_id
                            ))

                    except:
                        print("\n**{} - Failed to exectute BigQuery ETL...".format(datetime.now()))
                    
                    # read process_batch_meta file to check update on termination
                    process_meta = MJ.load_json(file_process_meta)
                    print("**{} - ETL paused {}s".format(datetime.now(), process_meta["meta"]["pull_cycle_hr"]*60*60))
                    sleep(process_meta["meta"]["pull_cycle_hr"]*60*60)

                else:
                    break
            else:
                break

        else:
            break

    print("\n{} - BigQuery ETL terminated...".format(datetime.now()))
else:
    print("\n{} - BigQuery ETL terminated...".format(datetime.now()))
