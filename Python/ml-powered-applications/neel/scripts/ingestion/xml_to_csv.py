# script to parse xml data to csv

import pandas as pd
import sys
import xml.etree.ElementTree as ET

# add path to runtime
sys.path.append('../')

from classes.general import YAMLHandler, LogToFile
# from functions.language_modeling import optimize_kmeans_cluster

# initialization
YMLparams = YAMLHandler()
LogHandler = LogToFile()

# get parameter objects
PARAMS = '../params_main.yaml'
params = YMLparams.read(read_loc=PARAMS)

# data paths
PATH_DATA = params["data_path"]
DATA_SOURCES = params["data_sources"]
PATH_LOG_MAIN = '{}\{}.csv'.format(PATH_DATA, params['data_logs']['xml_parser']["loc"])

# if there doesn't exist a log file, create one
if params['data_logs']['xml_parser']["exists"] is False:
    LogHandler.create_csv(PATH_LOG_MAIN, ['TimeStamp', 'Log'])
    params['data_logs']["xml_parser"]["exists"] = True # this isn't working for some reason
    YMLparams.write(PARAMS, params)

LogHandler.log_csv(PATH_LOG_MAIN, 'XML conversion started')

#
# XML pipline
#
# <posts>
#   <row>....

# Assuming that all data structures follow convention above

# For each xml data source and each file specified
for xml_source in DATA_SOURCES["raw_xml"]:
    for xml_file in DATA_SOURCES["raw_xml"][xml_source]["files"]:
        
        # define path and parse xml
        _path = '{}\{}\{}.xml'.format(PATH_DATA, DATA_SOURCES["raw_xml"][xml_source]["path"], xml_file)
        _path_export = '{}\{}\{}.csv'.format(PATH_DATA, DATA_SOURCES["raw_csv"][xml_source], xml_file)
        _columns = []
        _data = {}
        ElementTree = ET.parse(_path)
        root = ElementTree.getroot()

        # construct master column list
        for row in root.iter('row'):
            row_data = dict(row.attrib)
            row_keys = row.keys()
            for col in row_keys:
                if col not in _columns:
                    _columns.append(col)

        # initialize keys to master columns with lists of None
        _data = dict(zip(_columns, [[] for col in _columns]))

        # iterate between each column and append to data
        for row in root.iter('row'):
            row_data = dict(row.attrib)
            row_keys = row.keys()
            
            for col in _columns:

                # if the column in row attrib, append to dictionary otherwise append None
                if col in row_keys:
                    _data[col].append(row_data[col])
                else:
                    _data[col].append(None)
    
    # export to csv
    pd.DataFrame.from_dict(_data).to_csv(_path_export, index=False)
    LogHandler.log_csv(PATH_LOG_MAIN, 'XML conversion complete and exported to {}'.format(_path_export))