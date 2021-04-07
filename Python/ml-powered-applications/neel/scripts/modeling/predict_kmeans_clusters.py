# PURPOSE - To predict cluster index of a given umap coordinate and export for bokeh visualizations

# FUNCTIONALITY




# library dependencies
import sys
import spacy #python -m spacy download en_core_web_lg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import umap

# add path to runtime
sys.path.append('../')

from classes.general import YAMLHandler, LogToFile
from functions.general import export_df
from functions.language_modeling import nlp_red, umap_red, get_kmeans_clusters
import io

# intialization
YMLparams = YAMLHandler()
LogHandler = LogToFile()
features_to_export = []

# get parameter objects
PARAMS = '../params_main.yaml'
params = YMLparams.read(read_loc=PARAMS)
kmeans_params = YMLparams.read(read_loc=params['pretrained_models']['kmeans']['yaml_location'])

# data paths
PATH_DATA = params["data_path"]
DATA_SOURCES = params["data_sources"]
PATH_BOKEH = PATH_DATA + '\{}'.format(DATA_SOURCES["bokeh_data"])
PATH_LOG_MAIN = '{}\{}.csv'.format(PATH_DATA, params['data_logs']['predict_kmeansClusters']["loc"])

# if there doesn't exist a log file, create one
if params['data_logs']['predict_kmeansClusters']["exists"] is False:
    LogHandler.create_csv(PATH_LOG_MAIN, ['TimeStamp', 'Log'])
    params['data_logs']["predict_kmeansClusters"]["exists"] = True
    YMLparams.write(PARAMS, params)

LogHandler.log_csv(PATH_LOG_MAIN, 'predict_kmeans_clusters.py start')

contains_umap = lambda i: True if "umap" in i else False

#
# Ingestion
#

df_orig = pd.read_csv('{}\{}.csv'.format(PATH_DATA, DATA_SOURCES['clean_questions']), index_col=False)
df = df_orig.iloc[:, 1::].copy()
df_question = df.loc[df["PostTypeId"] == 1, :]

#
# LANGUAGE MODELLING & CLUSTERAL ALLOCATION
#

# load language model
nlp = spacy.load('en_core_web_lg', disable=["parser", "tagger", "ner", "textcat"])
LogHandler.log_csv(PATH_LOG_MAIN, 'language model loaded')

#
# Dimensionality reduction
#

# produce vector embeddings and clusteral predictions for a range of features
features_to_vectorize = ['Title']

for feature in features_to_vectorize:
    
    # produce embeddings
    vector_embeddings = nlp_red(
        nlp, 
        df_question.loc[:, feature].to_list(), 
        feature
        )
    
    feature_embeddings = vector_embeddings[feature].to_list()
    umap_vectors = umap_red(feature_embeddings)['_umap_vectors']

    print('- {} clusters'.format(int(kmeans_params['opt_clusters'])))

    # append vector emdbedings and cluster predictions to supplied dataframe
    df_question.loc[:, 'umap_x_{}'.format(feature)] = umap_vectors[:, 0]
    df_question.loc[:, 'umap_y_{}'.format(feature)] = umap_vectors[:, 1]
    df_question.loc[:, 'kmeans_cluster_{}'.format(feature)] = get_kmeans_clusters(
        vec_emb_list=feature_embeddings, 
        n_clusters=int(kmeans_params['opt_clusters']),
        _params=params
        )['_cluster_predictions']

# export dataframe for bokeh and current vector embeddings
LogHandler.log_csv(PATH_LOG_MAIN, 'clusters({}) mapped to fields'.format(int(kmeans_params['opt_clusters'])))

export_df(df_question, df_question.columns, export_loc=PATH_BOKEH, export_name=params["data_sources"]["bokeh_cluster_data"], return_df=False)
export_df(
    df_question.loc[:, df_question.columns.str.contains('umap')], 
    df_question.loc[:, df_question.columns.str.contains('umap')].columns, 
    export_loc=PATH_DATA, 
    export_name=params["data_sources"]["umap_vector_embeddings"], 
    return_df=False
)


# df_emb = pd.DataFrame(
#     {
#         "PrimaryID"          : df.loc[df["PostTypeId"] == 1, "Title"].index,
#         "post_title"         : post_titles.to_list(),
#         "vector_embedding"   : post_title_vectors,
#         "question_answered"  : df.loc[df["PostTypeId"]==1, "fe_question_answered"]\
#                                 .apply(lambda row: True if row==1 else False)
#     }
# )

# # df_emb.head()

# print(umap)