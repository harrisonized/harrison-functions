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
    showticklabels=False
):
    
    """
    | Like a heatmap, but for mouse paws
    | Enter a paw_score between 0 to 1 as a dictionary
    | Example:
    
    .. code-block:: python
    
        paw_scores = {
            'fr_palm': 0.1,
            'fr_thumb': 0.2,
            'fr_index': 0.7,
            'fr_middle': 0.8,
            'fr_ring': 0.9,
            'fr_pinky': 1,

            'fl_palm': 0.1,
            'fl_thumb': 0.2,
            'fl_index': 0.7,
            'fl_middle': 0.8,
            'fl_ring': 0.9,
            'fl_pinky': 1,

            'hr_palm': 0.1,
            'hr_thumb': 0.2,
            'hr_index': 0.7,
            'hr_middle': 0.8,
            'hr_ring': 0.9,
            'hr_pinky': 1,

            'hl_palm': 0.1,
            'hl_thumb': 0.3,
            'hl_index': 0.7,
            'hl_middle': 0.8,
            'hl_ring': 0.9,
            'hl_pinky': 1,
        }
        
    | Values are hard-coded, do not change the dimensions
    """
    
    paw_colors = {k: interpolate_colorscale(v) for k, v in paw_scores.items()}
    
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{}, {}],
               [{}, {}]],
        subplot_titles=("Right", "Left", "", "")
    )
    
    # ----------------------------------------------------------------------
    # Annotations

    # FR
    fig.append_trace(go.Scatter(
        x=[1.95625, 1.84375, 1.48125],
        y=[1.5, 1.9375, 2.4],
        mode="text",
        text=[
              paw_scores.get("fr_thumb"),  # thumb
              paw_scores.get("fr_index"),  # index
              paw_scores.get("fr_middle"),  # middle
             ],
        textposition="top right"
    ), 1, 1)
    
    fig.append_trace(go.Scatter(
        x=[1.5, 1.22125, 1.05625],
        y=[1.025, 2.325, 1.725],
        mode="text",
        text=[paw_scores.get('fr_palm'),  # palm
              paw_scores.get("fr_ring"),  # ring
              paw_scores.get("fr_pinky")  # pinky
             ],
        textposition="top center"
    ), 1, 1)
    
    # FL
    fig.append_trace(go.Scatter(
        x=[0.94375, 1.15625, 1.41875],
        y=[1.5, 1.9375, 2.4],
        mode="text",
        text=[paw_scores.get("fl_thumb"),  # thumb
              paw_scores.get("fl_index"),  # index
              paw_scores.get("fl_middle"),  # middle
             ],
        textposition="top left"
    ), 1, 2)
    
    fig.append_trace(go.Scatter(
        x=[1.5, 1.67875, 1.94375],
        y=[1.025, 2.325, 1.725],
        mode="text",
        text=[paw_scores.get("fl_palm"),  # palm
              paw_scores.get("fl_ring"),  # ring
              paw_scores.get("fl_pinky")  # pinky
             ],
        textposition="top center"
    ), 1, 2)
    
    # HR
    fig.append_trace(go.Scatter(
        x=[2, 1.8, 1.5],
        y=[1.65, 2.2125, 2.8],
        mode="text",
        text=[paw_scores.get("hr_thumb"),  # thumb
              paw_scores.get("hr_index"),  # index
              paw_scores.get("hr_middle"),  # middle
             ],
        textposition="top right"
    ), 2, 1)
    fig.append_trace(go.Scatter(
        x=[1.5, 1.3, 1.075],
        y=[1.025, 2.7, 1.8625],
        mode="text",
        text=[paw_scores.get("hr_palm"),  # palm
              paw_scores.get("hr_ring"),  # ring
              paw_scores.get("hr_pinky")  # pinky
             ],
        textposition="top center"
    ), 2, 1)

    
    # HL
    fig.append_trace(go.Scatter(
        x=[1, 1.2, 1.45],
        y=[1.65, 2.2125, 2.8],
        mode="text",
        text=[paw_scores.get("hl_thumb"),  # thumb
              paw_scores.get("hl_index"),  # index
              paw_scores.get("hl_middle"),  # middle
             ],
        textposition="top left"
    ), 2, 2)
    fig.append_trace(go.Scatter(
        x=[1.5, 1.7, 1.925],
        y=[1.025, 2.7, 1.8625],
        mode="text",
        text=[paw_scores.get("hl_palm"),  # palm
              paw_scores.get("hl_ring"),  # ring
              paw_scores.get("hl_pinky")  # pinky
             ],
        textposition="top center"
    ), 2, 2)
    
    
    # ----------------------------------------------------------------------
    # Shapes
    
    shapes = [
        
        # FR
        {'type': 'circle', 'x0': 1, 'x1': 2, 'y0': 0.5, 'y1': 1.75, 'opacity': opacity, 'fillcolor': paw_colors.get('fr_palm'), 'line_color': paw_colors.get('fr_palm'), 'xref': 'x', 'yref': 'y', "layer": "below"},  # palm
        {'type': 'circle', 'x0': 1.95, 'x1': 2.1625, 'y0': 1.325, 'y1': 1.675, 'opacity': opacity, 'fillcolor': paw_colors.get('fr_thumb'), 'line_color': paw_colors.get('fr_thumb'), 'xref': 'x', 'yref': 'y', "layer": "below"},  # thumb
        {'type': 'circle', 'x0': 1.7375, 'x1': 1.95, 'y0': 1.625, 'y1': 2.25, 'opacity': opacity, 'fillcolor': paw_colors.get('fr_index'), 'line_color': paw_colors.get('fr_index'), 'xref': 'x', 'yref': 'y', "layer": "below"},  # index 
        {'type': 'circle', 'x0': 1.475, 'x1': 1.6875, 'y0': 1.75, 'y1': 2.4, 'opacity': opacity, 'fillcolor': paw_colors.get('fr_middle'), 'line_color': paw_colors.get('fr_middle'), 'xref': 'x', 'yref': 'y', "layer": "below"},  # middle
        {'type': 'circle', 'x0': 1.2175, 'x1': 1.425, 'y0': 1.725, 'y1': 2.325, 'opacity': opacity, 'fillcolor': paw_colors.get('fr_ring'), 'line_color': paw_colors.get('fr_ring'), 'xref': 'x', 'yref': 'y', "layer": "below"},  # ring
        {'type': 'circle', 'x0': 0.95, 'x1': 1.1625, 'y0': 1.5, 'y1': 2.15, 'opacity': opacity, 'fillcolor': paw_colors.get('fr_pinky'), 'line_color': paw_colors.get('fr_pinky'), 'xref': 'x', 'yref': 'y', "layer": "below"},  # pinky

        # FL
        {'type': 'circle', 'x0': 1, 'x1': 2, 'y0': 0.5, 'y1': 1.75, 'opacity': opacity, 'fillcolor': paw_colors.get('fl_palm'), 'line_color': paw_colors.get('fl_palm'), 'xref': 'x2', 'yref': 'y2', "layer": "below"},  # palm
        {'type': 'circle', 'x0': 0.8375, 'x1': 1.05, 'y0': 1.325, 'y1': 1.675, 'opacity': opacity, 'fillcolor': paw_colors.get('fl_thumb'), 'line_color': paw_colors.get('fl_thumb'), 'xref': 'x2', 'yref': 'y2', "layer": "below"},  # thumb
        {'type': 'circle', 'x0': 1.05, 'x1': 1.2625, 'y0': 1.625, 'y1': 2.25, 'opacity': opacity, 'fillcolor': paw_colors.get('fl_index'), 'line_color': paw_colors.get('fl_index'), 'xref': 'x2', 'yref': 'y2', "layer": "below"},  # index 
        {'type': 'circle', 'x0': 1.3125, 'x1': 1.525, 'y0': 1.75, 'y1': 2.4, 'opacity': opacity, 'fillcolor': paw_colors.get('fl_middle'), 'line_color': paw_colors.get('fl_middle'), 'xref': 'x2', 'yref': 'y2', "layer": "below"},  # middle
        {'type': 'circle', 'x0': 1.575, 'x1': 1.7825, 'y0': 1.725, 'y1': 2.325, 'opacity': opacity, 'fillcolor': paw_colors.get('fl_ring'), 'line_color': paw_colors.get('fl_ring'), 'xref': 'x2', 'yref': 'y2', "layer": "below"},  # ring
        {'type': 'circle', 'x0': 1.8375, 'x1': 2.05, 'y0': 1.5, 'y1': 2.15, 'opacity': opacity, 'fillcolor': paw_colors.get('fl_pinky'), 'line_color': paw_colors.get('fl_pinky'), 'xref': 'x2', 'yref': 'y2', "layer": "below"},  # pinky

        # HR
        {'type': 'circle', 'x0': 1.05, 'x1': 1.95, 'y0': 0.25, 'y1': 2, 'opacity': opacity, 'fillcolor': paw_colors.get('hr_palm'), 'line_color': paw_colors.get('hr_palm'), 'xref': 'x3', 'yref': 'y3', "layer": "below"},  # palm
        {'type': 'circle', 'x0': 1.9, 'x1': 2.1, 'y0': 1.4, 'y1': 1.9, 'opacity': opacity, 'fillcolor': paw_colors.get('hr_thumb'), 'line_color': paw_colors.get('hr_thumb'), 'xref': 'x3', 'yref': 'y3', "layer": "below"},  # thumb
        {'type': 'circle', 'x0': 1.7, 'x1': 1.9, 'y0': 1.825, 'y1': 2.6, 'opacity': opacity, 'fillcolor': paw_colors.get('hr_index'), 'line_color': paw_colors.get('hr_index'), 'xref': 'x3', 'yref': 'y3', "layer": "below"},  # index
        {'type': 'circle', 'x0': 1.45, 'x1': 1.65, 'y0': 2, 'y1': 2.8, 'opacity': opacity, 'fillcolor': paw_colors.get('hr_middle'), 'line_color': paw_colors.get('hr_middle'), 'xref': 'x3', 'yref': 'y3', "layer": "below"},  # middle
        {'type': 'circle', 'x0': 1.2, 'x1': 1.4, 'y0': 1.925, 'y1': 2.675, 'opacity': opacity, 'fillcolor': paw_colors.get('hr_ring'), 'line_color': paw_colors.get('hr_ring'), 'xref': 'x3', 'yref': 'y3', "layer": "below"},  # ring
        {'type': 'circle', 'x0': 0.975, 'x1': 1.175, 'y0': 1.6, 'y1': 2.325, 'opacity': opacity, 'fillcolor': paw_colors.get('hr_pinky'), 'line_color': paw_colors.get('hr_pinky'), 'xref': 'x3', 'yref': 'y3', "layer": "below"},  # pinky
        
        # HL
        {'type': 'circle', 'x0': 1.05, 'x1': 1.95, 'y0': 0.25, 'y1': 2, 'opacity': opacity, 'fillcolor': paw_colors.get('hl_palm'), 'line_color': paw_colors.get('hl_palm'), 'xref': 'x4', 'yref': 'y4', "layer": "below"},  # palm
        {'type': 'circle', 'x0': 0.9, 'x1': 1.1, 'y0': 1.4, 'y1': 1.9, 'opacity': opacity, 'fillcolor': paw_colors.get('hl_thumb'), 'line_color': paw_colors.get('hl_thumb'), 'xref': 'x4', 'yref': 'y4', "layer": "below"},  # thumb
        {'type': 'circle', 'x0': 1.1, 'x1': 1.3, 'y0': 1.825, 'y1': 2.6, 'opacity': opacity, 'fillcolor': paw_colors.get('hl_index'), 'line_color': paw_colors.get('hl_index'), 'xref': 'x4', 'yref': 'y4', "layer": "below"},  # index
        {'type': 'circle', 'x0': 1.35, 'x1': 1.55, 'y0': 2, 'y1': 2.8, 'opacity': opacity, 'fillcolor': paw_colors.get('hl_middle'), 'line_color': paw_colors.get('hl_middle'), 'xref': 'x4', 'yref': 'y4', "layer": "below"},  # middle
        {'type': 'circle', 'x0': 1.6, 'x1': 1.8, 'y0': 1.925, 'y1': 2.675, 'opacity': opacity, 'fillcolor': paw_colors.get('hl_ring'), 'line_color': paw_colors.get('hl_ring'), 'xref': 'x4', 'yref': 'y4', "layer": "below"},  # ring
        {'type': 'circle', 'x0': 1.825, 'x1': 2.025, 'y0': 1.6, 'y1': 2.325, 'opacity': opacity, 'fillcolor': paw_colors.get('hl_pinky'), 'line_color': paw_colors.get('hl_pinky'), 'xref': 'x4', 'yref': 'y4', "layer": "below"},  # pinky

    ]
    
    fig['layout'].update(shapes=shapes)
    
    
    # ----------------------------------------------------------------------
    # Layout

    # set range
    fig['layout'].update(
        
        # FR
        xaxis={'domain': [0, 0.45], 'range': [0, 3], 'showgrid': False, 'showticklabels': showticklabels},
        yaxis={'domain': [0.55, 1], 'range': [0, 3], 'showgrid': False, 'showticklabels': showticklabels, 'title': {'text': 'Front', 'font': {'size': 16}}},
        
        # FL
        xaxis2={'domain': [0.55, 1], 'range': [0, 3], 'showgrid': False, 'showticklabels': showticklabels},
        yaxis2={'domain': [0.55, 1], 'range': [0, 3], 'showgrid': False, 'showticklabels': showticklabels},
        
        # HR
        xaxis3={'domain': [0, 0.45], 'range': [0, 3], 'showgrid': False, 'showticklabels': showticklabels},
        yaxis3={'domain': [0, 0.45], 'range': [0, 3], 'showgrid': False, 'showticklabels': showticklabels, 'title': {'text': 'Hind', 'font': {'size': 16}}},
        
        # HL
        xaxis4={'domain': [0.55, 1], 'range': [0, 3], 'showgrid': False, 'showticklabels': showticklabels},
        yaxis4={'domain': [0, 0.45], 'range': [0, 3], 'showgrid': False, 'showticklabels': showticklabels},
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
