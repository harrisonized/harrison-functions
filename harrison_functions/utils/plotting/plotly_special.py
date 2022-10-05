import plotly.graph_objs as go
import plotly.figure_factory as ff
from .plotly import plot_heatmap
from ...etc.colors import warm

# Functions
# # plot_dendrogram
# # plot_clustergram


def plot_dendrogram(df, top_color_threshold=None, side_color_threshold=None):
    """Given a table, returns the upper and side dendrograms
    """

    # Create Upper Dendrogram
    dendro_top = ff.create_dendrogram(df.T,
                                      orientation='bottom',
                                      labels=df.columns,
                                      color_threshold=top_color_threshold)
    for scatter in dendro_top['data']:
        scatter['yaxis'] = 'y2'

    # Create Side Dendrogram
    dendro_side = ff.create_dendrogram(df,
                                       orientation='right',
                                       labels=df.index,
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


def plot_clustergram(df, xlabel='x', ylabel='y', zlabel='z', title=None,
                     show_xticklabels=True, show_yticklabels=True,
                     show_xtitle=True, show_ytitle=False,
                     show_dendrolabels=False,
                     top_color_threshold=None, side_color_threshold=None,
                     showscale=True,
                     annotations=False  # buggy
                     ):
    """Generates a heatmap with dendrograms to the top and left
    """

    dendro_top, dendro_side = plot_dendrogram(df,
                                              top_color_threshold=top_color_threshold,
                                              side_color_threshold=side_color_threshold,)  # this reindexes the table
    data = df[dendro_top['layout']['xaxis']['ticktext']].reindex(
        dendro_side['layout']['yaxis']['ticktext'][::-1]
    )

    fig = plot_heatmap(data, xlabel=xlabel, ylabel=ylabel, zlabel=zlabel,
                       showscale=showscale,
                       show_xtitle=show_xtitle, show_ytitle=show_ytitle,
                       annotations=annotations
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
                             'side':'right',
                             })

    # Dendrogram layout
    fig.layout.update(plot_bgcolor='rgba(0,0,0,0)',
                      yaxis2={'domain': [0.85, 1],  # upper dendrogram
                              'showticklabels': show_dendrolabels, },
                      xaxis2={'domain': [0, 0.15],  # side dendrogram
                              'showticklabels': show_dendrolabels, },
                      )
    return fig
