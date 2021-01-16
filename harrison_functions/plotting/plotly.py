import os
from collections import defaultdict
import itertools
import re
import json
import math
import numpy as np
import pandas as pd
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.io as pio
import plotly.offline as pyo
from .colors import (default_colors, warm,
                     generate_label_colors, hex_to_rgba, update_rgba_opacity)
from harrison_functions.formatting.text_tools import title_case_to_initials
# from _plotly_future_ import v4_subplots


# Functions included in this file:
# # save_png_json_html
# # export_fig_to_json
# # plot_heatmap
# # plot_single_bar
# # plot_single_scatter
# # split_df
# # plot_multiple_scatter
# # plot_violin
# # plot_box
# # average_bin
# # plot_surface_histogram
# # plot_panel_histogram
# # make_sankey_df
# # make_link_and_node_df
# # plot_sankey
# # digraph_dot_from_transition_matrix


def save_png_json_html(fig, dir_name, filename):
    pio.write_image(fig, f'{dir_name}/png/{filename}.png', width=800, height=600)
    with open(f'{dir_name}/json/{filename}.json', 'w') as outfile:
        json.dump(fig, outfile, cls=plotly.utils.PlotlyJSONEncoder)
    div = pyo.plot(fig, output_type='div')
    with open(f'{dir_name}/html/{filename}.html', 'w') as f:
        f.write(div)


def export_fig_to_json(fig, fig_dir='figures', filename='fig'):
    os.makedirs(f'{fig_dir}', exist_ok=True)
    with open(f'{fig_dir}/{filename}.json', 'w') as outfile:
        json.dump(fig, outfile, cls=plotly.utils.PlotlyJSONEncoder)


def plot_heatmap(df, xlabel=None, ylabel=None, title=None, vlabel='Value',
                 column_order=None, row_order=None,
                 annotations=False, xside=None, dec=0, trunc_lim=0, error_df=None,
                 hide_xylabel=False):
    """Returns a heatmap with the same dimensions as the input table
    """

    # Custom order to input dataframe
    if column_order is None:
        pass
    else:
        df = df[column_order]
        if error_df:
            error_df = error_df[column_order]

    if row_order is None:
        pass
    else:
        df = df.reindex(row_order)
        if error_df:
            error_df = error_df.reindex(row_order)

    df.columns = list(map(str, df.columns))
    df = df.reindex(list(df.index[::-1]))

    if error_df:
        error_df.columns = list(map(str, error_df.columns))
        error_df = error_df.reindex(list(error_df.index[::-1]))

    if trunc_lim == 0:
        trunc_lim = -0.5
    else:
        trunc_lim = len(df.index) - int(trunc_lim) - 0.85

    # Define data: hover text, heatmap, and annotation
    rows_array = []
    for i in range(len(df.columns)):
        rows_array.append(list(df.index))

    hover_rows = pd.DataFrame(rows_array).transpose()
    hover_rows.columns = list(map(str, df.columns))
    hover_rows.index = df.index

    # This returns a dataframe with matching rows and columns as the main data
    if error_df:
        hover_text = str(vlabel) + ': ' + df.round(4).applymap(str) \
                     + ' ± ' + error_df.round(4).applymap(str) + '<br>' \
                     + str(ylabel) + ': ' + hover_rows + '<br>' \
                     + str(xlabel) + ': ' + str(df.columns) + '<br>'
    else:
        hover_text = str(vlabel) + ': ' + df.round(4).applymap(str) + '<br>' \
                     + str(ylabel) + ': ' + hover_rows + '<br>' \
                     + str(xlabel) + ': ' + str(df.columns) + '<br>'

    data = go.Heatmap(z=df,
                      x=list(range(len(df.columns))),
                      y=df.index,
                      hoverinfo='text',
                      text=hover_text,
                      colorscale=warm)

    if annotations is True:
        annotations = []
        for i, j in itertools.product(range(len(df.columns)), range(len(df.index))):
            if error_df:
                annotation_text = str(df.round(dec).iloc[j][i]) + ' ± ' + str(error_df.round(dec).iloc[j][i])
            else:
                annotation_text = str(df.round(dec).iloc[j][i])
            annotations.append(dict(x=i,
                                    y=j,
                                    text=annotation_text,
                                    showarrow=False,
                                    align='center',
                                    font={'size': 11}))
    else:
        annotations = None

    if hide_xylabel is True:
        xlabel = None
        ylabel = None

    # Plot
    fig = go.Figure(data=data)
    fig.layout.update(plot_bgcolor='rgba(0,0,0,0)',
                      title_text=title,
                      xaxis={'title': xlabel,
                             'showgrid': False,
                             'tickvals': list(range(len(df.columns))),
                             'ticktext': df.columns,
                             'side': xside},
                      yaxis={'title': ylabel,
                             'showgrid': False,
                             'tickvals': list(range(len(df.index))),
                             'ticktext': df.index,
                             'range': [trunc_lim, len(df.index)]},
                      annotations=annotations)
    fig.update_yaxes(gridcolor='#E4EAF2', zeroline=False)

    return fig


def plot_single_bar(df, title=None, xlabel=None, ylabel=None, vlabel='Value',
                    error_bars=False, row_order=None, color=None, horizontal=True,
                    trunc_lim=0):
    """Plots a bar chart. Default is horizontal
    index = data label
    first col = main data
    second col = stdev
    """

    # Custom order to input dataframe

    if row_order is None:
        pass
    else:
        df = df.reindex(row_order)

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
                 hovertemplate='User: %{y}<br>' + vlabel + ': %{x}<extra></extra>'
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


def plot_single_scatter(df, x, y, title=None, xlabel=None, ylabel=None, mode='markers'):
    """Downsample if size too big
    """

    fig = go.Figure()

    hover_text = f'{xlabel}: ' + df[x].apply(lambda x: str(x)) + '<br>' \
                 + f'{ylabel}: ' + df[y].apply(lambda x: str(x)) + '<br>'

    scatter = go.Scatter(x=df[x],
                         y=df[y],
                         mode=mode,
                         # marker={'color':df[color]},
                         text=hover_text,
                         hovertemplate="%{text}<br>" +
                                       "<extra></extra>")

    fig.add_trace(scatter)

    if df[x].dtype == int or float or np.float64:
        xrange = [df[x].min() - df[x].min() * 0.2, df[x].max() * 1.2]
    else:
        xrange = None

    fig.layout.update(
        title=go.layout.Title(text=title),
        xaxis={'title_text': xlabel,
               'showgrid': True,
               'range': xrange},
        yaxis={'title_text': ylabel,
               'showgrid': True, 'gridcolor': '#E4EAF2', 'zeroline': False,
               'range': [df[y].min() - df[y].min() * 0.1, df[y].max() * 1.1]},
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        hovermode='closest'
    )

    return fig


def split_df(df, x, c=None):
    """Helper function for plot_multiple_scatter and plot_violin

    Takes a dataframe in the following format:
    cat   | val
    ------+---------
    cat_1 | val_1.1
    cat_1 | val_1.2
    ...
    cat_2 | val_2.1
    cat_2 | val_2.2
    ...

    If you instead have:
    cat1    | cat2    | ... 
    --------+---------+-----
    val_1.1 | val_2.1 | ... 
    val_1.2 | val_2.2 | ... 

    Reshape it into the appropriate format using pd.melt
    pd.melt(df, value_vars = [cat1, cat2, ...], var_name='category')
    The order of the value_vars determines the order they appear on the plot.

    """
    df_list = []

    if c is None:
        for cat in df[x].apply(str).unique():
            df_list.append(df[df[x].apply(str) == cat])
        return df_list

    else:
        count_df = df.groupby([x, c]).size().reset_index()
        combo_list = list(zip(count_df[x], count_df[c]))

        for combo in combo_list:
            df_list.append(df[(df[x].apply(str) == combo[0])
                              & (df[c].apply(str) == combo[1])])
        return df_list


def plot_multiple_scatter(df, x, y, c,
                          xlabel=None, ylabel=None, clabel=None,
                          title=None,
                          mode='markers',
                          colors=default_colors,
                          label_colors=None
                          ):
    """Depends on split_df
    category is required, otherwise just use plot_single_scatter

    Takes a dataframe in the following format:
    cat   | val
    ------+---------
    cat_1 | val_1.1
    cat_1 | val_1.2
    ...
    cat_2 | val_2.1
    cat_2 | val_2.2
    ...

    If you instead have:
    cat1    | cat2    | ... 
    --------+---------+-----
    val_1.1 | val_2.1 | ... 
    val_1.2 | val_2.2 | ... 

    Reshape it into the appropriate format using pd.melt
    pd.melt(df, value_vars = [cat1, cat2, ...], var_name='category')
    The order of the value_vars determines the order they appear on the plot.

    """

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
               'range': [xmin, xmax]},
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
    """Depends on split_df and generate_label_colors
    If c==None, cannot input label_colors.

    Takes a dataframe in the following format:
    cat   | val
    ------+---------
    cat_1 | val_1.1
    cat_1 | val_1.2
    ...
    cat_2 | val_2.1
    cat_2 | val_2.2
    ...

    If you instead have:
    cat1    | cat2    | ... 
    --------+---------+-----
    val_1.1 | val_2.1 | ... 
    val_1.2 | val_2.2 | ... 

    Reshape it into the appropriate format using pd.melt
    pd.melt(df, value_vars = [cat1, cat2, ...], var_name='category')
    The order of the value_vars determines the order they appear on the plot.

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
    """Depends on split_df
    Takes df with columns: [x, y, category_label]
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


def average_bin(categorical, mode='mean'):
    """Helper function for plot_multiple_scatter and plot_violin
    Takes a str object like '[0, 25)' and returns the average
    """

    lower = float(re.match(r"([\[\(])(?P<lower>[0-9.]+), (?P<upper>[0-9.]+)([\)\]])", categorical).group('lower'))
    upper = float(re.match(r"([\[\(])(?P<lower>[0-9.]+), (?P<upper>[0-9.]+)([\)\]])", categorical).group('upper'))

    if mode == 'mean':
        return (lower + upper) / 2

    if mode == 'lower':
        return lower

    if mode == 'upper':
        return upper


def plot_surface_histogram(df,
                           xlabel=None, ylabel=None, zlabel=None, title=None,
                           colors=None, mode='mean'):
    """Takes a table prepared for plot_heatmap (with categorical columns and indices)
    Returns a surface plot
    
    Depends on average_bin
    """

    # Label formatting
    df.index, df.columns = df.index.astype(str), df.columns.astype(str)  # Convert categorical index to str
    idx_labels, col_labels = list(df.index), list(df.columns)  # Save labels
    df.index, df.columns = list(map(lambda x: average_bin(x, mode), df.index)), list(
        map(lambda x: average_bin(x, mode), df.columns))  # Get average bins

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
    """Depends on plot_bar
    
    Takes a histogram_table dataframe in the following format
    (ie. shaped with generate_histogram_table):
    value_bins | cat_1 | cat_2 | ...
    -----------+-------+-------+-----
    [0, 10)    |   1   |   0   | ...
    [10, 20)   |   0   |   1   | ...
    ...        |  ...  |  ...  | ...
    
    Returns a histogram in which each category gets its own panel.
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


def make_sankey_df(history_df, dropna=False, fillna='None'):
    """Counts the number of occurences of each line of the history_df
    
    Takes a history_df in this format:
     idx  |   0   |   1   | ...
    ------+-------+-------+-----
     id_1 | cat_1 | cat_2 | ...
     id_2 | cat_2 | None  | ...
    
    Returns:
        |   0   |   1   | ... | num | idx_0 | idx_1 | ...
    ----+-------+-------+-----+-----+-------+-------+-----
     1  | cat_1 | cat_2 | ... |  2  |   1   |   8   | ...
     2  | cat_2 | None  | ... | 10  |   2   |   9   | ...
    ...
    
    Eg. id_1 = RQ1, cat_1 = Saliva, cat_2 = Blood, etc.
    ...
    
    use history_df.pivot to get the history_df after indexing
    Eg:
    history_df = history_df.pivot(index='rq', columns='ib_num', values='specimen_type')
    """
    steps = history_df.columns.to_list()
    index = history_df.index.name
    history_df = history_df.fillna(fillna)

    sankey_df = history_df.reset_index().groupby(steps)[index].nunique().reset_index().rename(columns={index: 'num'})

    # generate source-target indices
    idx_start = 0
    if dropna is True:
        sankey_df = sankey_df.replace({fillna: None})
        for step in steps:
            sankey_df[f'step_{step}'] = sankey_df[step].astype('category').cat.codes.replace({-1: None}) + idx_start
            idx_start = sankey_df[f'step_{step}'].max() + 1
    else:
        for step in steps:
            sankey_df[f'step_{step}'] = sankey_df[step].astype('category').cat.codes + idx_start
            idx_start = sankey_df[f'step_{step}'].max() + 1

    return sankey_df


def make_link_and_node_df(sankey_df, num_steps: int, dropna=False):
    """Takes a df in the following format (output of make_sankey_df):
        |   0   |   1   | ... | num | step_0 | step_1 | ...
    ----+-------+-------+-----+-----+--------+--------+-----
     1  | cat_1 | cat_2 | ... |  2  |   0    |   8    | ...
     2  | cat_2 | None  | ... | 10  |   1    |   9    | ...
    ...
    
    Returns link_df:
       | source | target | num
    ---+--------+--------+-----
     0 |   0    |   8    | 114
     1 |   1    |   9    |  57
    ...
    
    Returns node_df:
       | source | label | step
    ---+--------+-------+--------
     0 |   0    | cat_1 | step_0
     1 |   1    | cat_2 | step_0
    ...
    """
    # reshape into source-target
    steps = range(num_steps)
    link_df = pd.lreshape(sankey_df,
                          groups={'source': [f'step_{step}' for step in steps[:-1]],
                                  'target': [f'step_{step}' for step in steps[1:]]})[['source', 'target', 'num']]
    link_df = link_df.groupby(['source', 'target']).sum().reset_index()

    # get index labels
    node_df = pd.lreshape(sankey_df,
                          groups={'source': [f'step_{step}' for step in steps],
                                  'label': steps})[['source', 'label']].drop_duplicates().sort_values(
        'source').reset_index(drop=True)

    # link source indices to step
    step_source = sankey_df[[f'step_{step}' for step in steps]].to_dict(orient='list')
    step_source = {k: list(set(v)) for k, v in step_source.items()}
    source_step_dict = {}
    for k, v in step_source.items():
        for source in v:
            source_step_dict[source] = k
    node_df['step'] = node_df['source'].apply(lambda x: source_step_dict[x])

    if dropna is True:
        # generate new indices for link_df
        step_stack_df = pd.lreshape(link_df, {'step_stack': ['source', 'target']})[['step_stack']]
        step_stack_df['new_idx'] = step_stack_df['step_stack'].astype('category').cat.codes
        step_stack_df = step_stack_df.drop_duplicates()
        replace_dict = dict(zip(step_stack_df['step_stack'], step_stack_df['new_idx']))
        link_df.loc[:, ['source', 'target']] = link_df.loc[:, ['source', 'target']].replace(
            replace_dict)  # reassign missing keys

        # filter out missing keys from node_df
        node_df = node_df[(node_df['source'].isin(replace_dict.keys()))]
        node_df.loc[:, 'source'] = node_df.loc[:, 'source'].replace(replace_dict)  # reassign missing keys

    return link_df, node_df


def plot_sankey(link_df, node_df,
                colors=default_colors,
                label_colors=None,
                title="Basic Sankey Diagram"):
    """Takes link_df and node_df as inputs:
    
    link_df:
       | source | target | num
    ---+--------+--------+-----
     0 |   0    |   8    | 114
     1 |   0    |   9    |  57
    ...
    
    node_df:
       | idx | label
    ---+-----+-------
     0 |  0  | cat_1
     1 |  1  | cat_2
    
    label_colors should be hex
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
    """Automatically generates a digraph dot string.
    This only generates the string and is not responsible for plotting.

    Example Input:
    choices = ['Space Mountain', 'Indiana Jones Adventure', 'Haunted Mansion']
    transition_matrix = np.array([[0.8, 0.15, 0.05],
                                  [0.3, 0.65, 0.05],
                                  [0.15, 0.05, 0.8]],)
    Output:
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
