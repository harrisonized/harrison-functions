import os
from collections import defaultdict
import itertools
import json
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from plotly.colors import find_intermediate_color
from ..std.text import title_case_to_initials, compute_average_bin
from ..std.dataframe import split_df
from ...etc.colors import (default_colors,
                           warm,
                           generate_label_colors,
                           hex_to_rgba,
                           update_rgba_opacity)
# from _plotly_future_ import v4_subplots


# Functions
# # save_fig_as_png
# # save_fig_as_json
# # save_fig_as_html
# # interpolate_colorscale
# # plot_heatmap
# # plot_single_bar
# # plot_single_scatter
# # plot_multiple_scatter
# # plot_violin
# # plot_box
# # plot_surface_histogram
# # plot_panel_histogram
# # plot_sankey
# # digraph_dot_from_transition_matrix

# Deprecated
# # save_png_json_html
# # plot_single_scatter_v1


def save_fig_as_png(fig, filepath, width=1200, height=800, scale=1, engine="kaleido"):
    """Make sure file extension is ".png"
    """
    if os.path.sep in filepath:
        os.makedirs(os.path.sep.join(str(filepath).split(os.path.sep )[:-1]), exist_ok=True)
    fig.write_image(filepath, width=width, height=height, scale=scale, engine=engine)


def save_fig_as_json(fig, filepath):
    """Make sure file extension is ".json"
    """
    if os.path.sep in filepath:
        os.makedirs(os.path.sep.join(str(filepath).split(os.path.sep )[:-1]), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(fig, f, cls=plotly.utils.PlotlyJSONEncoder)


def save_fig_as_html(fig, filepath):
    """Make sure file extension is ".html"
    """
    div = plotly.offline.plot(fig, output_type='div')
    if os.path.sep in filepath:
        os.makedirs(os.path.sep.join(str(filepath).split(os.path.sep )[:-1]), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(div)


def interpolate_colorscale(
        val,
        colorscale=[
            # warm
            [0.0, 'rgb(254.9, 245.6, 237.6)'],  # modified to be darker
            [0.2, 'rgb(254,224,144)'],
            [0.4, 'rgb(253,174,97)'],
            [0.6, 'rgb(244,109,67)'],
            [0.8, 'rgb(215,48,39)'],
            [1.0, 'rgb(165,0,38)']
        ]  
    ):
    """
    | Uses plotly.colors.find_intermediate_color to find the intermediate color
    | See: https://plotly.com/python-api-reference/generated/plotly.colors.html#plotly.colors.find_intermediate_color
    | Used in plot_paw
    """
    if val <= colorscale[0][0]:
        return colorscale[0][1]
    
    if val >= colorscale[-1][0]:
        return colorscale[-1][1]
    
    else:
        # just in case it's not in order
        colorscale = sorted(colorscale, key=lambda x: x[0])
        bins = [x[0] for x in colorscale]

        # get relevant bins
        left = np.digitize(val, bins, right=False)-1
        right = left+1
        
        # interpolate
        return find_intermediate_color(colorscale[left][1], colorscale[right][1], val, colortype='rgb')


def plot_heatmap(df, xlabel='x', ylabel='y', zlabel='z', title=None,
                 cols=[], rows=[],
                 error_df=None,
                 annotations=False, xside=None, dec=0,
                 showscale=True, show_xlabel=True, show_ylabel=True,
                 ):
    """Returns a heatmap with the same dimensions as the df
    """

    # Custom order to input dataframe
    if not cols:
        pass
    else:
        df = df[cols]
        if error_df:
            error_df = error_df[cols]

    if not rows:
        pass
    else:
        df = df.reindex(rows)
        if error_df:
            error_df = error_df.reindex(rows)

    df.columns = list(map(str, df.columns))
    df = df.reindex(list(df.index[::-1]))

    if error_df:
        error_df.columns = list(map(str, error_df.columns))
        error_df = error_df.reindex(list(error_df.index[::-1]))

    # Define data: hover text, heatmap, and annotation
    rows_array = []
    for i in range(len(df.columns)):
        rows_array.append(list(df.index))

    hover_rows = pd.DataFrame(rows_array).transpose()
    hover_rows.columns = df.columns.astype(str)
    hover_rows.index = df.index

    # This returns a dataframe with matching rows and columns as the main data
    if error_df:
        hover_text = str(zlabel) + ': ' + df.round(4).applymap(str) \
                     + ' ± ' + error_df.round(4).applymap(str) + '<br>' \
                     + str(ylabel) + ': ' + hover_rows + '<br>' \
                     + str(xlabel) + ': ' + df.columns.astype(str) + '<br>'
    else:
        hover_text = str(zlabel) + ': ' + df.round(4).applymap(str) + '<br>' \
                     + str(ylabel) + ': ' + hover_rows + '<br>' \
                     + str(xlabel) + ': ' + df.columns.astype(str) + '<br>'

    data = go.Heatmap(x=df.columns,
                      y=df.index,
                      z=df,
                      hoverinfo='text',
                      text=hover_text,
                      colorscale=warm)
    fig = go.Figure(data=data)

    if annotations is True:
        annotations = []
        for i, j in itertools.product(list(df.columns), list(df.index)):
            if error_df:
                annotation_text = str(df.round(dec).loc[j][i]) + ' ± ' + str(error_df.round(dec).loc[j][i])
            else:
                annotation_text = str(df.round(dec).loc[j][i])
            annotations.append(dict(x=i,
                                    y=j,
                                    text=annotation_text,
                                    showarrow=False,
                                    align='center',
                                    font={'size': 11}))
    else:
        annotations = None

    # General Layout
    fig.layout.update(showlegend=False,
                      hovermode='closest')

    # Heatmap Layout
    fig.layout.update(plot_bgcolor='rgba(0,0,0,0)',
                      title_text=title,
                      xaxis={'title': xlabel,
                             'mirror': False,
                             'showgrid': False,
                             'showline': False,
                             'zeroline': False,
                             'showticklabels': True,
                             'tickvals': [str(x) for x in df.columns],
                             'ticktext': [str(x) for x in df.columns],
                             'ticks': '',
                             'side': xside
                             },
                      yaxis={'title': ylabel,
                             'mirror': False,
                             'showgrid': False,
                             'showline': False,
                             'zeroline': False,
                             'showticklabels': True,
                             'tickvals': list(df.index),
                             'ticktext': list(df.index),
                             'ticks': '',
                             },
                      annotations=annotations)
    fig.update_yaxes(gridcolor='#E4EAF2', zeroline=False)
    fig.update_traces(showscale=showscale)

    if show_xlabel is False:
        fig.layout.update(xaxis={'title': None})

    if show_ylabel is False:
        fig.layout.update(yaxis={'title': None})

    return fig


def plot_single_bar(df, title=None, xlabel='x', ylabel='y', zlabel='z',
                    error_bars=False, rows=None, color=None, horizontal=True,
                    trunc_lim=0):
    """
    | Plots a bar chart. Default is horizontal
    | index = data label
    | first col = main data
    | second col = stdev
    """

    # Custom order to input dataframe

    if rows is None:
        pass
    else:
        df = df.reindex(rows)

    df.columns = list(map(str, df.columns))

    if trunc_lim == 0:
        trunc_lim = -0.5
    else:
        trunc_lim = len(df.index) - int(trunc_lim) - 0.85

    if horizontal is True:
        df = df.reindex(list(df.index[::-1]))
        y = df.index
        x = df[df.columns[0]]
        orientation = 'h'
        xaxis = {'title': xlabel,
                 'showgrid': False,
                 'range': [0, df[df.columns[0]].max() * 1.2 + 0.5]}
        yaxis = {'title': ylabel,
                 'showgrid': False,
                 'tickvals': list(range(len(df.index))),
                 'ticktext': df.index,
                 'range': [trunc_lim, len(df.index)]}
    else:
        x = df.index
        y = df[df.columns[0]]
        orientation = None
        xaxis = {'title': ylabel,
                 'showgrid': False,
                 'tickvals': list(range(len(df.index))),
                 'ticktext': df.index,
                 'range': [-0.5, len(df.index) - trunc_lim - 1]}
        yaxis = {'title': xlabel,
                 'showgrid': False,
                 'range': [0, df[df.columns[0]].max() * 1.2 + 0.5]}

    if error_bars is True:
        error_bars = df[df.columns[1]]
    else:
        error_bars = []

    bar = go.Bar(y=y,
                 x=x,
                 error_x={'type': 'data', 'array': error_bars},
                 error_y={'type': 'data', 'array': error_bars},
                 marker_color=color,
                 orientation=orientation,
                 hovertemplate='User: %{y}<br>' + zlabel + ': %{x}<extra></extra>'
                 )

    fig = go.Figure()
    fig.add_trace(bar)

    fig.layout.update(plot_bgcolor='rgba(0,0,0,0)',
                      title_text=title,
                      xaxis=xaxis,
                      yaxis=yaxis,
                      showlegend=False,
                      hovermode='closest')

    return fig


def plot_single_scatter(
    df, x, y, title=None,
    error_y=None, error_y_minus=None,
    xlabel=None, ylabel=None,
    xmin=None, xmax=None,
    ymin=None, ymax=None,
    log_x=False,
    mode='markers',
    color_discrete_sequence=px.colors.qualitative.G10,
):
    """Plots a single scatter function
    """
    
    # ----------------------------------------------------------------------
    # X Range
    
    if not log_x:
        xaxis_type = 'linear'
        # x_range
        if not xmin:
            xmin = df[x].min()
        if not xmax:
            xmax = df[x].max()
        xrange = [xmin - (xmax-xmin) * 0.05, xmax + (xmax-xmin) * 0.05]
    else:
        xaxis_type = 'log'
        xrange = [None, None]
    
    
    # ----------------------------------------------------------------------
    # Y Range
    
    if error_y:
        max_error_y_plus = df[error_y].max()
    else:
        max_error_y_plus = 0          
    if error_y_minus:
        max_error_y_minus = df[error_y_minus].max()
    else:
        max_error_y_minus = 0      
    if not ymin:
        ymin = df[y].min()-max_error_y_minus
    if not ymax:
        ymax = df[y].max()+max_error_y_plus   
    yrange = [ymin - (ymax-ymin) * 0.1, ymax + (ymax-ymin) * 0.1]
    
    
    # ----------------------------------------------------------------------
    # Figure
    
    fig = go.Figure()
    scatter = px.scatter(
        df, x=x, y=y, error_y=error_y, error_y_minus=error_y_minus,
        color_discrete_sequence=px.colors.qualitative.G10,
    )
    fig.add_trace(scatter.data[0])

    
    # ----------------------------------------------------------------------
    # Layout
    
    fig.layout.update(
        title=go.layout.Title(text=title),
        xaxis={'title_text': xlabel,
               'showgrid': True,
               'gridcolor': '#E4EAF2', 
               'range': xrange,
               'type': xaxis_type
              },
        yaxis={'title_text': ylabel,
               'showgrid': True, 'gridcolor': '#E4EAF2', 'zeroline': False,
               'range': yrange},
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='closest',
        showlegend=False,
    )
    
    fig.data[0].update(mode=mode)
    fig.update_traces(marker=dict(size=8))

    return fig


def plot_multiple_scatter(df, x, y, c,
                          xlabel=None, ylabel=None, clabel=None,
                          title=None,
                          mode='markers',
                          autocolor=True,
                          colors=default_colors,
                          label_colors=None,
                          log_x=False,
                          ):
    """
    | Depends on split_df
    | category is required, otherwise just use plot_single_scatter

    | Takes a dataframe in the following format:

    +-------+---------+
    | cat   | val     |
    +=======+=========+
    | cat_1 | val_1.1 |
    +-------+---------+
    | cat_1 | val_1.2 |
    +-------+---------+
    | ...   |         |
    +-------+---------+
    | cat_2 | val_2.1 |
    +-------+---------+
    | cat_2 | val_2.2 |
    +-------+---------+
    | ...   |         |
    +-------+---------+

    | If you instead have:

    +---------+---------+-----+
    | cat1    | cat2    | ... |
    +=========+=========+=====+
    | val_1.1 | val_2.1 | ... |
    +---------+---------+-----+
    | val_1.2 | val_2.2 | ... |
    +---------+---------+-----+

    | Reshape it into the appropriate format using pd.melt
    | pd.melt(df, value_vars = [cat1, cat2, ...], var_name='category')
    | The order of the value_vars determines the order they appear on the plot.
    """
    if autocolor:
        if label_colors:
            df['color'] = df[c].apply(lambda cat: label_colors[cat])
        else:
            label_colors = generate_label_colors(df[c].unique(), colors)
            df['color'] = df[c].apply(lambda cat: label_colors[cat])

    df_list = split_df(df, c)
    fig = go.Figure()

    range_params = defaultdict(list)
    range_params['xmin'] = []
    range_params['xmax'] = []
    range_params['ymin'] = []
    range_params['ymax'] = []

    legend_list = []

    for df in df_list:
        hover_text = f'{xlabel}: ' + df[x].apply(lambda x: str(x)) + '<br>' \
                     + f'{ylabel}: ' + df[y].apply(lambda x: str(x)) + '<br>' \
                     + f'{clabel}: ' + df[c].apply(lambda x: str(x)) + '<br>'

        if df[c].unique()[0] not in legend_list:
            legend_list.append(df[c].unique()[0])
            show_legend = True
        else:
            show_legend = False

        scatter = go.Scatter(x=df[x],
                             y=df[y],
                             name=df[c].unique()[0],
                             marker={'color': df['color'].unique()[0]},
                             showlegend=show_legend,
                             mode=mode,
                             text=hover_text,
                             hovertemplate="%{text}<br>" +
                                           "<extra></extra>")

        fig.add_trace(scatter)

        range_params['xmin'].append(df[x].min())
        range_params['xmax'].append(df[x].max())
        range_params['ymin'].append(df[y].min())
        range_params['ymax'].append(df[y].max())


    if log_x:
        xaxis_type = 'log'
        xrange = [None, None]
        xmin = None
        xmax = None
    else:
        xaxis_type = 'linear'
        x_range = (max(range_params['xmax']) - min(range_params['xmin']))
        xmin = min(range_params['xmin']) - x_range * 0.2
        xmax = max(range_params['xmax']) + x_range * 0.2
    
    y_range = (max(range_params['ymax']) - min(range_params['ymin']))
    ymin = min(range_params['ymin']) - y_range * 0.1
    ymax = max(range_params['ymax']) + y_range * 0.1

    fig.layout.update(
        title=go.layout.Title(text=title),
        xaxis={'title_text': xlabel,
               'showgrid': True,
               'range': [xmin, xmax],
               'type': xaxis_type
               },
        yaxis={'title_text': ylabel,
               'showgrid': True, 'gridcolor': '#E4EAF2', 'zeroline': False,
               'range': [ymin, ymax]},
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        hovermode='closest'
    )

    return fig


def plot_violin(df, x, y, c=None,
                xlabel=None, ylabel=None, clabel=None,
                title=None,
                colors=default_colors,
                label_colors=None
                ):
    """
    | Depends on split_df and generate_label_colors
    | If c==None, cannot input label_colors.

    | Takes a dataframe in the following format:

    +-------+---------+
    | cat   | val     |
    +=======+=========+
    | cat_1 | val_1.1 |
    +-------+---------+
    | cat_1 | val_1.2 |
    +-------+---------+
    | ...   |         |
    +-------+---------+
    | cat_2 | val_2.1 |
    +-------+---------+
    | cat_2 | val_2.2 |
    +-------+---------+
    | ...   |         |
    +-------+---------+

    | If you instead have:

    +---------+---------+-----+
    | cat1    | cat2    | ... |
    +=========+=========+=====+
    | val_1.1 | val_2.1 | ... |
    +---------+---------+-----+
    | val_1.2 | val_2.2 | ... |
    +---------+---------+-----+

    | Reshape it into the appropriate format using pd.melt
    | pd.melt(df, value_vars = [cat1, cat2, ...], var_name='category')
    | The order of the value_vars determines the order they appear on the plot.

    """

    if c and label_colors:
        df['color'] = df[c].apply(lambda cat: label_colors[cat])
    elif c and label_colors is None:
        label_colors = generate_label_colors(df[c].unique(), colors)
        df['color'] = df[c].apply(lambda cat: label_colors[cat])
    elif c is None:
        label_colors = generate_label_colors(df[x].unique(), colors)
        df['color'] = df[x].apply(lambda cat: label_colors[cat])

    df_list = split_df(df, x, c)
    fig = go.Figure()

    range_params = defaultdict(list)
    range_params['ymin'] = []
    range_params['ymax'] = []
    legend_list = []

    if c is None:
        c = x

    for df in df_list:

        hover_text = f'{xlabel}: ' + df[x].apply(lambda x: str(x)) + '<br>' \
                     + f'{ylabel}: ' + df[y].apply(lambda x: str(x)) + '<br>' \
                     + f'{clabel}: ' + df[c].apply(lambda x: str(x)) + '<br>'

        if df[c].unique()[0] not in legend_list:
            legend_list.append(df[c].unique()[0])
            show_legend = True
        else:
            show_legend = False

        violin = go.Violin(x=df[x].apply(str),
                           y=df[y],
                           name=df[c].unique()[0],
                           legendgroup=df[c].unique()[0],
                           scalegroup=df[c].unique()[0],
                           line_color=df['color'].unique()[0],
                           box_visible=True,
                           meanline_visible=True,
                           showlegend=show_legend,
                           text=hover_text,
                           hovertemplate="%{text}<br>" +
                                         "<extra></extra>")

        fig.add_trace(violin)
        range_params['ymin'].append(df[y].min())
        range_params['ymax'].append(df[y].max())

    fig.layout.update(
        title=go.layout.Title(text=title),
        xaxis={'title_text': xlabel,
               'showgrid': True, },
        yaxis={'title_text': ylabel,
               'showgrid': True, 'gridcolor': '#E4EAF2', 'zeroline': False,
               'range': [min(range_params['ymin']) - min(range_params['ymin']) * 0.1, max(range_params['ymax']) * 1.1]},
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        hovermode='closest')

    return fig


def plot_box(df, c, y,
             xlabel=None, ylabel=None,
             title=None):
    """
    | Depends on split_df
    | Takes df with columns: [x, y, category_label]
    """

    df_list = split_df(df, c)
    fig = go.Figure()

    range_params = defaultdict(list)
    range_params['ymin'] = []
    range_params['ymax'] = []
    for df in df_list:
        hover_text = f'{xlabel}: ' + df[c].apply(lambda x: str(x)) + '<br>' \
                     + f'{ylabel}: ' + df[y].apply(lambda x: str(x)) + '<br>'

        box = go.Box(x=df[c].apply(str),
                     y=df[y],
                     name=df[c].unique()[0],
                     text=hover_text,
                     hovertemplate="%{text}<br>" +
                                   "<extra></extra>")

        fig.add_trace(box)
        range_params['ymin'].append(df[y].min())
        range_params['ymax'].append(df[y].max())

    fig.layout.update(
        title=go.layout.Title(text=title),
        xaxis={'title_text': xlabel,
               'showgrid': True, },
        yaxis={'title_text': ylabel,
               'showgrid': True, 'gridcolor': '#E4EAF2', 'zeroline': False,
               'range': [min(range_params['ymin']) - min(range_params['ymin']) * 0.1, max(range_params['ymax']) * 1.1]},
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        hovermode='closest')

    return fig


def plot_surface_histogram(df,
                           xlabel=None, ylabel=None, zlabel=None, title=None,
                           colors=None, mode='mean'):
    """
    | Takes a table prepared for plot_heatmap (with categorical columns and indices)
    | Returns a surface plot
    
    | Depends on compute_average_bin
    """

    # Label formatting
    df.index, df.columns = df.index.astype(str), df.columns.astype(str)  # Convert categorical index to str
    idx_labels, col_labels = list(df.index), list(df.columns)  # Save labels
    df.index, df.columns = list(map(lambda x: compute_average_bin(x, mode), df.index)), list(
        map(lambda x: compute_average_bin(x, mode), df.columns))  # Get average bins

    # Plot
    surface = go.Surface(x=df.index, y=df.columns, z=df.T.values,
                         colorscale=colors)

    fig = go.Figure(data=surface)
    fig.layout.update(plot_bgcolor='rgba(0,0,0,0)',
                      title=title,
                      autosize=True,
                      margin=dict(l=0, b=100, t=100, r=0, ),
                      scene={"xaxis": {'title': xlabel,
                                       'showgrid': False,
                                       'tickvals': df.index,
                                       'ticktext': idx_labels},
                             "yaxis": {'title': ylabel,
                                       'showgrid': False,
                                       'tickvals': df.columns,
                                       'ticktext': col_labels},
                             "zaxis": {'title': zlabel},
                             'camera': {"eye": {"x": 1.5, "y": 1.5, "z": 1}},
                             "aspectratio": {"x": 1, "y": 1, "z": 0.5}
                             })
    return fig


def plot_panel_histogram(histogram_table: 'pd.DataFrame', title, xlabel=None, ylabel=None, y_nticks=5):
    """
    | Depends on plot_bar
    
    | Takes a histogram_table dataframe in the following format
    | (ie. shaped with generate_histogram_table):
    
    +------------+-------+-------+-----+
    | value_bins | cat_1 | cat_2 | ... |
    +============+=======+=======+=====+
    | [0, 10)    |   1   |   0   | ... |
    +------------+-------+-------+-----+
    | [10, 20)   |   0   |   1   | ... |
    +------------+-------+-------+-----+
    | ...        |  ...  |  ...  | ... |
    +------------+-------+-------+-----+
    
    | Returns a histogram in which each category gets its own panel.
    """
    num_rows = len(histogram_table.columns)
    fig = make_subplots(rows=num_rows, cols=1,
                        specs=[[{"type": "bar"}]] * num_rows,
                        shared_xaxes=True,
                        vertical_spacing=0.02,
                        subplot_titles=histogram_table.columns.to_list())

    for idx, category in enumerate(histogram_table.columns):
        trace = plot_bar(pd.DataFrame(histogram_table[category]),
                         horizontal=False)

        trace.data[0].name = category  # add legend name
        fig.add_trace(trace.data[0], row=idx + 1, col=1)
        fig.update_xaxes(showgrid=True,
                         tickson="boundaries",
                         gridcolor='#E4EAF2', zeroline=False,
                         showline=True, linewidth=1, linecolor='#E4EAF2',
                         row=idx + 1, col=1)

        trace.layout.yaxis.title = ylabel
        trace.layout.yaxis.showgrid = True
        fig.update_yaxes(trace.layout.yaxis,
                         tickmode='linear',
                         tick0=trace.layout.yaxis.range[0],
                         dtick=int(trace.layout.yaxis.range[1] / 1.2 / y_nticks),
                         gridcolor='#E4EAF2',
                         showline=True, linewidth=1, linecolor='#E4EAF2',
                         scaleratio=1,
                         row=idx + 1, col=1)

    fig.update_xaxes(title=xlabel, row=idx + 1, col=1)
    fig.layout.update(height=160 * num_rows, width=800,
                      title_text=title,
                      plot_bgcolor='rgba(0,0,0,0)')

    return fig


def plot_sankey(link_df, node_df,
                colors=default_colors,
                label_colors=None,
                title="Basic Sankey Diagram"):
    """
    | Takes link_df and node_df as inputs:
    
    | link_df:

    +---+--------+--------+-----+
    |   | source | target | num |
    +===+========+========+=====+
    | 0 |   0    |   8    | 114 |
    +---+--------+--------+-----+
    | 1 |   0    |   9    |  57 |
    +---+--------+--------+-----+

    | node_df:

    +---+-----+-------+
    |   | idx | label |
    +===+=====+=======+
    | 0 |  0  | cat_1 |
    +---+-----+-------+
    | 1 |  1  | cat_2 |
    +---+-----+-------+
    
    | label_colors should be hex
    """
    num_steps = node_df['step'].nunique() - 1
    node_df.loc[:, 'x_pos'] = node_df['step'].astype('category').cat.codes / num_steps
    node_df.loc[:, 'y_pos'] = 0.001

    sankey = go.Sankey(arrangement="snap",
                       node={'pad': 15, 'thickness': 20,
                             'line': {'color': 'black', 'width': 0.5},
                             'x': node_df['x_pos'].to_list(),
                             'y': node_df['y_pos'].to_list(),
                             'label': node_df['label'].to_list()
                             },
                       link={'source': link_df['source'].to_list(),
                             'target': link_df['target'].to_list(),
                             'value': link_df['num'].to_list(),
                             }
                       )

    if label_colors:
        node_df['color'] = node_df['label'].apply(lambda cat: hex_to_rgba(label_colors[cat], opacity=0.9))
        sankey.node.color = node_df['color'].to_list()
        sankey.link.color = sankey.node.color
        sankey.link.color = [update_rgba_opacity(sankey.node.color[idx], 0.3) for idx in sankey.link.source]
    else:
        label_colors = generate_label_colors(node_df['label'].unique(), colors)
        node_df['color'] = node_df['label'].apply(lambda cat: label_colors[cat])
        sankey.node.color = node_df['color'].to_list()

    fig = go.Figure(data=sankey)
    fig.update_layout(title_text=title, font_size=10)
    return fig


def digraph_dot_from_transition_matrix(transition_matrix, choices,
                                       colors=None, shape='circle'):
    """
    | Automatically generates a digraph dot string.
    | This only generates the string and is not responsible for plotting.

    | Example Input:
    
    .. code-block:: python

        choices = ['Space Mountain', 'Indiana Jones Adventure', 'Haunted Mansion']
        transition_matrix = np.array([[0.8, 0.15, 0.05],
                                      [0.3, 0.65, 0.05],
                                      [0.15, 0.05, 0.8]],)
    
    | Output:

    .. code-block:: python

        digraph {{
            rankdir=LR;
            node [shape=circle,style=filled,color=".7 .3 1.0"];
            SM
            IJA
            HM
            SM -> SM[label="0.8"];
            SM -> IJA[label="0.15"];
            SM -> HM[label="0.05"];
            IJA -> SM[label="0.3"];
            IJA -> IJA[label="0.65"];
            IJA -> HM[label="0.05"];
            HM -> SM[label="0.15"];
            HM -> IJA[label="0.05"];
            HM -> HM[label="0.8"];
        }}
    
    """
    choices_initials = [title_case_to_initials(x) for x in choices]
    
    header_text = []
    if colors:     
        for choice, color in zip(choices_initials, colors):
            header_text.append(f"""\n    {choice}[shape={shape},style=filled,color={color}]""")
    else:
        for choice in choices_initials:
            header_text.append(f"""\n    {choice}[shape={shape}]""")
    header = "".join(header_text)
    
    body_text = []
    for i, choice in enumerate(choices_initials):
        for j, value in enumerate(transition_matrix[i]):
            body_text.append(f"""\n    {choices_initials[i]} -> {choices_initials[j]}[label="{value}"];""")
    body = "".join(body_text)

    digraph = f"""digraph {{
    rankdir=LR;""" + header + body + "\n}}"

    return digraph


# ----------------------------------------------------------------------
# Deprecated

# def save_png_json_html(fig, dir_name, filename):
#     """legacy function"""
#     pio.write_image(fig, f'{dir_name}/png/{filename}.png', width=800, height=600)
#     with open(f'{dir_name}/json/{filename}.json', 'w') as outfile:
#         json.dump(fig, outfile, cls=plotly.utils.PlotlyJSONEncoder)
#     div = pyo.plot(fig, output_type='div')
#     with open(f'{dir_name}/html/{filename}.html', 'w') as f:
#         f.write(div)


# def plot_single_scatter_v1(df, x, y, title=None, xlabel=None, ylabel=None, mode='markers'):
#     """Downsample if size too big
#     """

#     fig = go.Figure()

#     hover_text = f'{xlabel}: ' + df[x].apply(lambda x: str(x)) + '<br>' \
#                  + f'{ylabel}: ' + df[y].apply(lambda x: str(x)) + '<br>'

#     scatter = go.Scatter(x=df[x],
#                          y=df[y],
#                          mode=mode,
#                          # marker={'color':df[color]},
#                          text=hover_text,
#                          hovertemplate="%{text}<br>" +
#                                        "<extra></extra>")

#     fig.add_trace(scatter)

#     if df[x].dtype == int or float or np.float64:
#         xrange = [df[x].min() - df[x].min() * 0.2, df[x].max() * 1.2]
#     else:
#         xrange = None

#     fig.layout.update(
#         title=go.layout.Title(text=title),
#         xaxis={'title_text': xlabel,
#                'showgrid': True,
#                'range': xrange},
#         yaxis={'title_text': ylabel,
#                'showgrid': True, 'gridcolor': '#E4EAF2', 'zeroline': False,
#                'range': [df[y].min() - df[y].min() * 0.1, df[y].max() * 1.1]},
#         plot_bgcolor='rgba(0,0,0,0)',
#         showlegend=False,
#         hovermode='closest'
#     )

#     return fig
