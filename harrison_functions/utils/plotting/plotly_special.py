import itertools
from collections import defaultdict
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from .plotly import interpolate_colorscale, plot_heatmap
from ...etc.colors import warm

# Functions
# # plot_paw
# # plot_dendrogram
# # plot_clustergram


def plot_paw(
    paw_scores:dict,
    title='Paw Plot',
    opacity=0.9,
    default_color='blue',
    showticklabels=False,
    autorange_color=True,
    rescale_color=1,
    format_code='{:2.2f}',
    num_decimals=2,
    max_color=1,
    min_color=0
):
    
    """
    | Like a heatmap, but for mouse paws
    | Enter a paw_score between 0 to 1 as a dictionary
    | Example:
    
    .. code-block:: python
    
        paw_scores = {
            "fr_palm": 0.1,
            "fr_thumb": 0.2,
            "fr_index": 0.7,
            "fr_middle": 0.8,
            "fr_ring": 0.9,
            "fr_pinky": 1,
            "fl_palm": 0.1,
            "fl_thumb": 0.2,
            "fl_index": 0.7,
            "fl_middle": 0.8,
            "fl_ring": 0.9,
            "fl_pinky": 1,
            "hr_palm": 0.1,
            "hr_thumb": 0.2,
            "hr_index": 0.7,
            "hr_middle": 0.8,
            "hr_ring": 0.9,
            "hr_pinky": 1,
            "hl_palm": 0.1,
            "hl_thumb": 0.3,
            "hl_index": 0.7,
            "hl_middle": 0.8,
            "hl_ring": 0.9,
            "hl_pinky": 1,
        }
        
        fig = plot_paw(paw_scores, opacity=0.9, showticklabels=False)
        fig.show()
        
    | Values are manually chosen to be centered in a 3x3 grid
    | Do not change the dimensions of this plot
    """

    if autorange_color:
        min_color = min([x[1] for x in paw_scores.items()])
        max_color = max([x[1] for x in paw_scores.items()])
        if max_color == min_color:
            min_color, max_color = 0, 1

    paw_colors = {k: interpolate_colorscale((v-min_color)/(max_color-min_color)*rescale_color) for k, v in paw_scores.items()}
    
    # ----------------------------------------------------------------------
    # Settings
    
    limbs = ['fr', 'fl', 'hr', 'hl']
    digits = ['thumb', 'index', 'middle', 'palm', 'ring', 'pinky']

    coordinates_for_digit = defaultdict(dict, {

        # FL                     
        "fl_thumb": {
            "shape_x": (0.8375, 1.05),  # (x0, x1)
            "shape_y": (1.325, 1.675),  # (y0, y1)
            "annotation": (0.8375, 1.575),  # (x, y)
            "annotation_position": "top left",
        },
        "fl_index": {
            "shape_x": (1.05, 1.2625),  # (x0, x1)
            "shape_y": (1.625, 2.25),  # (y0, y1)
            "annotation": (1.05, 2.15),  # (x, y)
            "annotation_position": "top left",
        },
        "fl_middle": {
            "shape_x": (1.3125, 1.525),  # (x0, x1)
            "shape_y": (1.75, 2.4),  # (y0, y1)
            "annotation": (1.525, 2.4),  # (x, y)
            "annotation_position": "top left",
        },
        "fl_ring": {
            "shape_x": (1.575, 1.7825),  # (x0, x1)
            "shape_y": (1.725, 2.325),  # (y0, y1)
            "annotation": (1.7825, 2.325),  # (x, y)
            "annotation_position": "top center", 
        },
        "fl_pinky": {
            "shape_x": (1.8375, 2.05),  # (x0, x1)
            "shape_y": (1.5, 2.15),  # (y0, y1)
            "annotation": (2.05, 2.15),  # (x, y)
            "annotation_position": "top right",
        },
        "fl_palm": {
            "shape_x": (1, 2),  # (x0, x1)
            "shape_y": (0.5, 1.75),  # (y0, y1)
            "annotation": (1.5, 1.025),  # (x, y)
            "annotation_position": "top center", 
        },

        # HL
        "hl_thumb": { 
            "shape_x": (0.9, 1.1),  # (x0, x1)
            "shape_y": (1.4, 1.9),  # (y0, y1)
            "annotation": (1, 1.9),  # (x, y)
            "annotation_position": "top left",
        },
        "hl_index": {
            "shape_x": (1.1, 1.3),  # (x0, x1)
            "shape_y": (1.825, 2.6),  # (y0, y1)
            "annotation": (1.2, 2.6),  # (x, y)
            "annotation_position": "top left",
        },
        "hl_middle": {
            "shape_x": (1.35, 1.55),  # (x0, x1)
            "shape_y": (2, 2.8),  # (y0, y1)
            "annotation": (1.45, 2.8),  # (x, y)
            "annotation_position": "top center",
        },
        "hl_ring": {
            "shape_x": (1.6, 1.8),  # (x0, x1)
            "shape_y": (1.925, 2.675),  # (y0, y1)
            "annotation": (1.8, 2.575),  # (x, y)
            "annotation_position": "top right", 
        },
        "hl_pinky": {
            "shape_x": (1.825, 2.025),  # (x0, x1)
            "shape_y": (1.6, 2.325),  # (y0, y1)
            "annotation": (2.025, 2.225),  # (x, y)
            "annotation_position": "top right",
        },
        "hl_palm": {
            "shape_x": (1.05, 1.95),  # (x0, x1)
            "shape_y": (0.25, 2),  # (y0, y1)
            "annotation": (1.5, 1.025),  # (x, y)
            "annotation_position": "top center", 
        },
    })
    
    # mirror image of the "left" limbs (right on the image)
    for l_limb, digit in itertools.product(['fl', 'hl'], digits):
        
        r_limb = l_limb.replace('l', 'r')
        
        coordinates_for_digit[f'{r_limb}_{digit}']["shape_x"] = (
            3-coordinates_for_digit[f'{l_limb}_{digit}']["shape_x"][1],
            3-coordinates_for_digit[f'{l_limb}_{digit}']["shape_x"][0]
        )
        coordinates_for_digit[f'{r_limb}_{digit}']["shape_y"] = coordinates_for_digit[f'{l_limb}_{digit}']["shape_y"]
        coordinates_for_digit[f'{r_limb}_{digit}']["annotation"] = (
            3-coordinates_for_digit[f'{l_limb}_{digit}']["annotation"][0],
            coordinates_for_digit[f'{l_limb}_{digit}']["annotation"][1],
        )
        coordinates_for_digit[f'{r_limb}_{digit}']["annotation_position"] = (
            {'top right': 'top left',
             'top center': 'top center',
             'top left': 'top right'
            }[coordinates_for_digit[f'{l_limb}_{digit}']["annotation_position"]]
        )
        
    rowcol_for_limb = {
        'fr': (1, 1),
        'fl': (1, 2),
        'hr': (2, 1),
        'hl': (2, 2),
    }

    xyref_for_limb = {
        'fr': ('x', 'y'),
        'fl': ('x2', 'y2'),
        'hr': ('x3', 'y4'),
        'hl': ('x4', 'y4'),
    }
    
    # ----------------------------------------------------------------------
    # Instantiate Figure
    
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{}, {}],
               [{}, {}]],
        subplot_titles=("Right", "Left", "", "")
    )
    
    # ----------------------------------------------------------------------
    # Add Shapes and Annotations
    
    trace_args = defaultdict(dict)
    shapes = []
    for limb, digit in itertools.product(limbs, digits):

        coordinate = coordinates_for_digit[f'{limb}_{digit}']
        
        # ----------------------------------------------------------------------
        # Shapes
        
        shapes.append(
            {'x0': coordinate['shape_x'][0], 'x1': coordinate['shape_x'][1],
             'y0': coordinate['shape_y'][0], 'y1': coordinate['shape_y'][1],
             'type': 'circle',
             'opacity': opacity,
             'fillcolor': paw_colors.get(f'{limb}_{digit}', interpolate_colorscale(0)),  # color
             'line_color': paw_colors.get(f'{limb}_{digit}', interpolate_colorscale(0)),  # color
             'xref': xyref_for_limb.get(limb)[0],
             'yref': xyref_for_limb.get(limb)[1],
             "layer": "below"
            },
        )
        
        # ----------------------------------------------------------------------
        # Annotations

        # get position
        annotation_position = coordinate['annotation_position']

        # instantiate if not exist
        if trace_args[limb].get(annotation_position) is None:
            trace_args[limb][annotation_position] = {
                'x': [],
                'y': [], 
                'text': []
            }

        # append
        trace_args[limb][annotation_position]['x'].append(coordinate['annotation'][0])
        trace_args[limb][annotation_position]['y'].append(coordinate['annotation'][1])
        trace_args[limb][annotation_position]['text'].append(paw_scores.get(f'{limb}_{digit}'))  # text
    
    # annotations
    for limb in limbs:
        for textposition in trace_args[limb].keys():
            fig.append_trace(
                go.Scatter(
                    mode="text",
                    x=trace_args[limb][textposition]['x'],
                    y=trace_args[limb][textposition]['y'],
                    text=[round(float(format_code.format(text)), num_decimals) for text in trace_args[limb][textposition]['text']],
                    textposition=textposition
                ), rowcol_for_limb[limb][0], rowcol_for_limb[limb][1]
            )
    
    # ----------------------------------------------------------------------
    # Layout
    
    fig['layout'].update(shapes=shapes)

    # domain and range
    fig['layout'].update(
        xaxis={'domain': [0, 0.45], 'range': [0, 3], 'showgrid': False, 'showticklabels': showticklabels},  # FR
        yaxis={'domain': [0.55, 1], 'range': [0, 3], 'showgrid': False, 'showticklabels': showticklabels,  # FR
               'title': {'text': 'Front', 'font': {'size': 16}}},
        xaxis2={'domain': [0.55, 1], 'range': [0, 3], 'showgrid': False, 'showticklabels': showticklabels},  # FL
        yaxis2={'domain': [0.55, 1], 'range': [0, 3], 'showgrid': False, 'showticklabels': showticklabels},  # FL
        xaxis3={'domain': [0, 0.45], 'range': [0, 3], 'showgrid': False, 'showticklabels': showticklabels},  # HR
        yaxis3={'domain': [0, 0.45], 'range': [0, 3], 'showgrid': False, 'showticklabels': showticklabels,  # HR
                'title': {'text': 'Hind', 'font': {'size': 16}}},
        xaxis4={'domain': [0.55, 1], 'range': [0, 3], 'showgrid': False, 'showticklabels': showticklabels},  # HL
        yaxis4={'domain': [0, 0.45], 'range': [0, 3], 'showgrid': False, 'showticklabels': showticklabels},  # HL
    )
    
    fig['layout'].update(
        plot_bgcolor='rgba(0,0,0,0)',
        height=600, width=600,
        title_text=title,
        showlegend=False
    )
    
    return fig


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
