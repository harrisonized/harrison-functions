import os
from collections import defaultdict
import json
import math
import plotly
import plotly.graph_objs as go
import plotly.io as pio
import plotly.offline as pyo
import plotly.figure_factory as ff
from ...etc.colors import warm


# Functions included in this file:
# # plot_heatmap
# # plot_dendrogram
# # plot_clustergram


def plot_heatmap(table_df, xlabel='x', ylabel='y', zlabel='z', title=None,
                 height=1200, width=800, showscale=True, show_xtitle=True, show_ytitle=True,
                 ):
    """Returns a heatmap with the same dimensions as the table_df
    """
    
    hovertemplate=xlabel+": %{x}<br>"+ylabel+": %{y}<br>"+zlabel+": %{z}<extra></extra>"

    data = go.Heatmap(x=table_df.columns,
                      y=table_df.index,
                      z=table_df,
                      hovertemplate=hovertemplate,
                      colorscale=warm)
    fig = go.Figure(data=data)

    # General Layout
    fig.layout.update(height=height,
                      width=width,
                      showlegend=False,
                      hovermode='closest', )

    # Heatmap Layout
    fig.layout.update(plot_bgcolor='rgba(0,0,0,0)',
                      title_text=title,
                      xaxis={'title': xlabel,
                             'mirror': False,
                             'showgrid': False,
                             'showline': False,
                             'zeroline': False,
                             'showticklabels': True,
                             'tickmode': 'auto',
                             'ticktext': table_df.index,
                             'ticks': ""},
                      yaxis={'title': ylabel,
                             'mirror': False,
                             'showgrid': False,
                             'showline': False,
                             'zeroline': False,
                             'showticklabels': True,
                             'ticktext': table_df.columns,
                             'ticks': "",
                             'autorange': 'reversed'
                             })

    fig.update_traces(showscale=showscale)

    if show_xtitle is False:
        fig.layout.update(xaxis={'title': None})

    if show_ytitle is False:
        fig.layout.update(yaxis={'title': None})

    return fig


def plot_dendrogram(table_df, top_color_threshold=None, side_color_threshold=None):
    """Given a table, returns the upper and side dendrograms
    """

    # Create Upper Dendrogram
    dendro_top = ff.create_dendrogram(table_df.T,
                                      orientation='bottom',
                                      labels=table_df.columns,
                                      color_threshold=top_color_threshold)
    for scatter in dendro_top['data']:
        scatter['yaxis'] = 'y2'

    # Create Side Dendrogram
    dendro_side = ff.create_dendrogram(table_df,
                                       orientation='right',
                                       labels=table_df.index,
                                       color_threshold=side_color_threshold)
    for scatter in dendro_side['data']:
        scatter['xaxis'] = 'x2'

    # Dendrogram layout
    dendro_top.layout.update(plot_bgcolor='rgba(0,0,0,0)',
                             xaxis={'showticklabels': False,
                                    'showgrid': False,},
                             yaxis2={'domain': [0.8, .95],  # upper dendrogram
                                     'mirror': False,
                                     'showgrid': False,
                                     'showline': False,
                                     'zeroline': False,
                                     'showticklabels': True,}, )
    dendro_side.layout.update(plot_bgcolor='rgba(0,0,0,0)',
                              xaxis2={'domain': [0, 0.15],  # lower
                                      'mirror': False,
                                      'showgrid': False,
                                      'showline': False,
                                      'zeroline': False,
                                      'showticklabels': True,},
                             yaxis={'showticklabels': False,
                                    'showgrid': False,}, )

    return dendro_top, dendro_side


def plot_clustergram(table_df, xlabel='x', ylabel='y', zlabel='z', title=None,
                     height=1200, width=800, show_xticklabels=True, show_yticklabels=False,
                     show_dendrolabels=False,
                     show_xtitle=True, show_ytitle=False,
                     top_color_threshold=None, side_color_threshold=None,
                     showscale=True):
    """Generates a heatmap with dendrograms to the top and left
    """

    dendro_top, dendro_side = plot_dendrogram(table_df,
                                              top_color_threshold=top_color_threshold,
                                              side_color_threshold=side_color_threshold,)  # this reindexes the table
    data = table_df[dendro_top['layout']['xaxis']['ticktext']].reindex(
        dendro_side['layout']['yaxis']['ticktext'])

    fig = plot_heatmap(data, xlabel=xlabel, ylabel=ylabel, zlabel=zlabel,
                       height=height, width=width, showscale=showscale,
                       show_xtitle=show_xtitle, show_ytitle=show_ytitle
                      )
    fig.data[0]['x'] = dendro_top['layout']['xaxis']['tickvals']
    fig.data[0]['y'] = dendro_side['layout']['yaxis']['tickvals']
    fig.add_traces(dendro_top['data'])
    fig.add_traces(dendro_side['data'])

    fig.layout.update(title=title)

    # Heatmap Layout
    fig.layout.update(xaxis={'domain': [0.15, 1],
                             'tickmode': 'array',
                             'tickvals': dendro_top['layout']['xaxis']['tickvals'],
                             'ticktext': dendro_top['layout']['xaxis']['ticktext'],
                             'showticklabels': show_xticklabels, },
                      yaxis={'domain': [0, .85],
                             'tickvals': dendro_side['layout']['yaxis']['tickvals'],
                             'ticktext': dendro_side['layout']['yaxis']['ticktext'],
                             'showticklabels': show_yticklabels,
                             'side':'right' })

    # Dendrogram layout
    fig.layout.update(plot_bgcolor='rgba(0,0,0,0)',
                      yaxis2={'domain': [0.8, .95],  # upper dendrogram
                              'showticklabels': show_dendrolabels, },
                      xaxis2={'domain': [0, 0.15],  # side dendrogram
                              'showticklabels': show_dendrolabels, },
                      )
    return fig
