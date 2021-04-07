# script to govern the ingestion of data source for analysis

import pandas as pd
import sys
from bs4 import BeautifulSoup

# add path to runtime
sys.path.append('../')

from classes.general import YAMLHandler, LogToFile
# from functions.language_modeling import optimize_kmeans_cluster


## Functions
def remove_p_tags(row_string):
    if row_string is not None:
        soup = BeautifulSoup(row_string, 'html.parser')
        return soup.p.text

# initialization
YMLparams = YAMLHandler()
LogHandler = LogToFile()

# get parameter objects
PARAMS = '../params_main.yaml'
params = YMLparams.read(read_loc=PARAMS)

# data paths
PATH_DATA = params["data_path"]
DATA_SOURCES = params["data_sources"]
PATH_LOG_MAIN = '{}\{}.csv'.format(PATH_DATA, params['data_logs']['prepare_posts']["loc"])

# if there doesn't exist a log file, create one
if params['data_logs']['prepare_posts']["exists"] is False:
    LogHandler.create_csv(PATH_LOG_MAIN, ['TimeStamp', 'Log'])
    params['data_logs']["prepare_posts"]["exists"] = True # this isn't working for some reason
    YMLparams.write(PARAMS, params)

LogHandler.log_csv(PATH_LOG_MAIN, 'Ingestion of Stack Exchange Writers Posts started')

#
# Ingestion
#

# upload data sources into DataFrame
df_orig = pd.read_csv(
    '{}\{}\Posts.csv'.format(PATH_DATA, DATA_SOURCES["raw_csv"]["stackexchange_writers"]), 
    index_col='Id'
)

# extract dataframe based on required columns
columns = [
    "PostTypeId", "AcceptedAnswerId", "ParentId", "AnswerCount", 
    "CommentCount", "FavoriteCount", "LastActivityDate", "CreationDate",
    "ClosedDate", "LastEditDate", "Score", "Title", "Body" 
          ]

df1 = df_orig.copy()
df1 = df1.loc[:, columns]

#
# DATA CLEANSING
# - remove html tags in Body

df1.loc[:, "Body"] = df1.loc[:, "Body"].apply(lambda row: remove_p_tags(row))
print(df1.Body.head())

# export