# Goal: generate bokeh visualization from a specified script

# bokeh serve --show bokeh_visualize_clusters.py

# dependencies
import sys
import pandas as pd
import numpy as np
import bokeh.models as bmo
import bokeh.plotting as bpl
import matplotlib.pyplot as plt

from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.palettes import d3, all_palettes
from bokeh.layouts import row, layout
from bokeh.models import CheckboxGroup, Panel
from bokeh.models.tools import HoverTool
from bokeh.models.widgets import Tabs
# from bokeh.io import show, output_notebook

# add path to runtime
sys.path.append('../')

from functions.general import export_df, test
from functions.bokeh_callbacks import checkbox_categorical_filter
from classes.general import YAMLHandler, LogToFile

# intialization
YMLparams = YAMLHandler()
LogHandler = LogToFile()

# get parameter objects
PARAMS = '../params_main.yaml'
params = YMLparams.read(read_loc=PARAMS)

# data paths
PATH_DATA = params["data_path"]
DATA_SOURCES = params["data_sources"]
PATH_CLUSTER_DATA = '{}\{}\{}.csv'.format(PATH_DATA, DATA_SOURCES["bokeh_data"], DATA_SOURCES["bokeh_cluster_data"])

# ingest optimized clusters
df_orig = pd.read_csv(PATH_CLUSTER_DATA)
df = df_orig.iloc[:, 1::].copy()


# Bokeh setup and sources

# Last mile conversions
df_bokeh                      = df.copy()
df_bokeh["question_answered"] = df_bokeh.fe_question_answered.apply(lambda row: "answered" if row==True else "unanswered")
df_bokeh["kmeans_cluster"]           = df_bokeh.kmeans_cluster_Title.apply(lambda row: str(row))
df_bokeh.rename(columns={
    'umap_x_Title': 'x',
    'umap_y_Title': 'y',
}, inplace=True)

print(df_bokeh.info())

# define UI Tools
TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"
LABELS_kmeans = ["Cluster {}".format(cluster) for cluster in np.sort(df_bokeh.kmeans_cluster_Title.unique())]

print(LABELS_kmeans)

# sources
df_ans   = df_bokeh.loc[df_bokeh.question_answered == 'answered', :]
df_nans  = df_bokeh.loc[df_bokeh.question_answered == 'unanswered', :]

src_ans_orig = bpl.ColumnDataSource(
    df_ans.to_dict('list')
)

src_ans  = bpl.ColumnDataSource(
    df_ans.to_dict('list')
)

src_nans_orig = bpl.ColumnDataSource(
    df_nans.to_dict('list')
)

src_nans = bpl.ColumnDataSource(
    df_nans.to_dict('list')
)

## Bokeh worflow

# output_notebook()

#
# Figures and colormaps
#

p_answered = figure(tools=TOOLS)
p_nanswered = figure(tools=TOOLS)

# palettes assume 3 if number of clusters less than it
color_palettes = lambda x: all_palettes['Set1'][3] if (len(x) < 3) else all_palettes['Set1'][len(x)]

ans_cmap = bmo.CategoricalColorMapper(
    factors=df_ans.kmeans_cluster.unique(),
    palette=color_palettes(df_ans.kmeans_cluster.unique())
)

nans_cmap = bmo.CategoricalColorMapper(
    factors=df_nans.kmeans_cluster.unique(),
    palette=color_palettes(df_nans.kmeans_cluster.unique())
) # this changes the order with which the colors are applied

#
# Visualizations
#

p_answered.scatter(
    x='x', 
    y='y',
    source=src_ans,
    color={'field': 'kmeans_cluster', 'transform': ans_cmap},
    fill_alpha=0.9,
    line_color=None,
    legend_group='kmeans_cluster'
)

# using the color mapped define by answered questions - potential bug
p_nanswered.scatter(
    x='x', 
    y='y',
    source=src_nans,
    color={'field': 'kmeans_cluster', 'transform': ans_cmap},
    fill_alpha=0.9,
    line_color=None,
    legend_group='kmeans_cluster'
)

# Decorations
p_answered.title.text = 'Answered questions'
p_answered.legend.title = 'Cluster'
p_answered.xaxis.axis_label = 'Dimensional x'
p_answered.yaxis.axis_label = 'Dimensional y'


p_nanswered.title.text = 'Unanswered questions'
p_nanswered.legend.title = 'Cluster'
p_nanswered.xaxis.axis_label = 'Dimensional x'
p_nanswered.yaxis.axis_label = 'Dimensional y'

fig_dim = 550
p_answered.width = p_nanswered.width = fig_dim
p_answered.height = p_nanswered.height = fig_dim

# hover parameters
hover_answered = HoverTool()
hover_answered.tooltips=[
    ('Post Question Title', '@Title'),
    ('kmeans_cluster', '@kmeans_cluster'),
]

hover_nanswered = HoverTool()
hover_nanswered.tooltips=[
    ('Post Question Title', '@Title'),
    ('kmeans_cluster', '@kmeans_cluster')
]

p_answered.add_tools(hover_answered)
p_nanswered.add_tools(hover_answered)

#
# Widgets
#

# data filters
filter_answered = checkbox_categorical_filter(src_ans, src_ans_orig)
filter_nanswered = checkbox_categorical_filter(src_nans, src_nans_orig)

# checkbox object
checkbox_group = CheckboxGroup(labels=LABELS_kmeans, active=[i for i in range(len(LABELS_kmeans))])

# event handlers
checkbox_group.js_on_change('active', filter_answered)
checkbox_group.js_on_change('active', filter_nanswered)

# output_file("color_scatter.html", title="color_scatter.py example")

# layout specificationns 
lay = layout(
        children = [
            [p_answered, p_nanswered],
            [checkbox_group],
        ]
)

tab = Panel(child=lay, title = 'Clusters')
tabs = Tabs(tabs=[tab])

curdoc().add_root(tabs)

# show(tabs)  # open a browser or notebook depending on configuration