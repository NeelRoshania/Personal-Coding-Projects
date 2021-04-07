from google.cloud import bigquery, storage
import os


def get_table_data(query):
    # sources
    #     - https://cloud.google.com/bigquery/docs/running-queries

    # set credentials before using this

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # Make an API request
    return client.query(query)

# # extract row information
# for row in get_table_data(query):

#         # Row values can be accessed by field name or index.
#         print("{}, {}".format(row["date"], row["headline"]))
