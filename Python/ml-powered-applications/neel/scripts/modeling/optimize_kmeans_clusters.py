# Script orchesrtate kmeans clusteral optimization 

import pandas as pd
import sys

# add path to runtime
sys.path.append('../')

from classes.general import YAMLHandler, LogToFile
from functions.language_modeling import optimize_kmeans_cluster

# initialization
YMLparams = YAMLHandler()
LogHandler = LogToFile()

# get parameter objects
PARAMS = '../params_main.yaml'
params = YMLparams.read(read_loc=PARAMS)

# data paths
PATH_DATA = params["data_path"]
PATH_KMEANS = params['pretrained_models']['kmeans']['yaml_location']
DATA_SOURCES = params["data_sources"] 
PATH_LOG_MAIN = '{}\{}.csv'.format(PATH_DATA, params['data_logs']['optimize_kmeansClusters']["loc"])

params_kmeans = YMLparams.read(read_loc=PATH_KMEANS)

# if there doesn't exist a log file, create one
if params['data_logs']['optimize_kmeansClusters']["exists"] is False:
    LogHandler.create_csv(PATH_LOG_MAIN, ['TimeStamp', 'Log'])
    params['data_logs']["optimize_kmeansClusters"]["exists"] = True # this isn't working for some reason
    YMLparams.write(PARAMS, params)

LogHandler.log_csv(PATH_LOG_MAIN, 'kmeans optimization started')

#
# Optimization
#

# read current vector space
vector_emd = pd.read_csv(
    '{}\{}.csv'.format(
        PATH_DATA, 
        DATA_SOURCES['umap_vector_embeddings']
        ), index_col=False)\
            .iloc[:, 1::]

# optimize clusters and update yaml
LogHandler.log_csv(PATH_LOG_MAIN, 'optimal clusters found: {}'.format((optimize_kmeans_cluster(vector_emd))))

# write to yaml
params_kmeans["opt_clusters"] = optimize_kmeans_cluster(vector_emd)
YMLparams.write(PATH_KMEANS, params_kmeans)
