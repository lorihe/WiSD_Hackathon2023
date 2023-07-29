import pandas as pd
import plotly.graph_objects as go
import numpy as np
import dash
from dash import html
import plotly.express as px
from scipy import stats

def get_layout():
    # Create the basketball court shape
    court_shape = go.layout.Shape(
        type="rect",
        x0=-47,
        y0=-25,
        x1=47,
        y1=25,
        line=dict(color='black', width=1, dash='solid'),
        fillcolor='rgba(0, 0, 0, 0)'
    )

    # Create the center shape
    center_shape = go.layout.Shape(
        type="circle",
        x0=-6,
        y0=-6,
        x1=6,
        y1=6,
        line=dict(color='black', width=1),
        fillcolor='rgba(0, 0, 0, 0)'
    )

    # Create the free-throw lane shape
    lane_shape = go.layout.Shape(
        type="rect",
        x0=-47,
        y0=-6,
        x1=-28,
        y1=6,
        line=dict(color='black', width=1),
        fillcolor='rgba(0, 0, 0, 0)'
    )
    lane_circle_shape = go.layout.Shape(
        type="circle",
        x0=-22,
        y0=-6,
        x1=-34,
        y1=6,
        line=dict(color='black', width=1),
        fillcolor='rgba(0, 0, 0, 0)'
    )

    # Create the three-point line arc
    theta = np.linspace(-np.pi / 2, np.pi / 2, 100)
    x_arc = -43 + (24 * np.cos(theta))  # Adjusted x-axis coordinate
    y_arc = -24 * np.sin(theta) + 0  # Adjusted y-axis coordinate

    y_arc_ind = np.where((y_arc < 22) & (y_arc > -22))

    x_arc = x_arc[y_arc_ind]
    y_arc = y_arc[y_arc_ind]

    x_arc = pd.Series(x_arc).reset_index(drop=True)
    y_arc = pd.Series(y_arc).reset_index(drop=True)

    arc_shape = go.layout.Shape(
        type="path",
        path=f"M {x_arc[0]}, {y_arc[0]} L {'L '.join([str(x) + ', ' + str(y) for x, y in zip(x_arc, y_arc)])} ",
        line=dict(color='black', width=1))

    arc_top = go.layout.Shape(type="line", x0=-47, y0=22, x1=-33.3, y1=22, line=dict(color='black', width=1))
    arc_bottom = go.layout.Shape(type="line", x0=-47, y0=-22, x1=-33.3, y1=-22, line=dict(color='black', width=1))

    # Create the half-court line
    half_court_line = go.layout.Shape(
        type="line",
        x0=0,
        y0=-25,
        x1=0,
        y1=25,
        line=dict(color='black', width=1, dash='dash')
    )

    lane_shape_mirror = go.layout.Shape(
        type="rect",
        x0=28,
        y0=-6,
        x1=47,
        y1=6,
        line=dict(color='black', width=1),
        fillcolor='rgba(0, 0, 0, 0)'
    )

    lane_circle_shape_mirror = go.layout.Shape(
        type="circle",
        x0=22,
        y0=-6,
        x1=34,
        y1=6,
        line=dict(color='black', width=1),
        fillcolor='rgba(0, 0, 0, 0)'
    )

    arc_shape_mirror = go.layout.Shape(
        type="path",
        path=f"M {-x_arc[0]}, {y_arc[0]} L {'L '.join([str(-x) + ', ' + str(y) for x, y in zip(x_arc, y_arc)])} ",
        line=dict(color='black', width=1)
    )

    arc_top_mirror = go.layout.Shape(type="line", x0=47, y0=22, x1=33.3, y1=22, line=dict(color='black', width=1))
    arc_bottom_mirror = go.layout.Shape(type="line", x0=47, y0=-22, x1=33.3, y1=-22, line=dict(color='black', width=1))

    half_court_line_mirror = go.layout.Shape(
        type="line",
        x0=0,
        y0=-25,
        x1=0,
        y1=25,
        line=dict(color='black', width=1, dash='dash')
    )

    # Create the layout with the basketball court and additional lines
    layout = go.Layout(
        xaxis=dict(range=[-47, 47], dtick=5, constrain='domain'),
        yaxis=dict(range=[-25, 25], dtick=5, scaleanchor = "x", scaleratio = 1),
        plot_bgcolor='white',
        shapes=[court_shape, center_shape, lane_shape, arc_shape, arc_top, arc_bottom, half_court_line,
                lane_shape_mirror, arc_shape_mirror, arc_top_mirror, arc_bottom_mirror, half_court_line_mirror,
                lane_circle_shape, lane_circle_shape_mirror]
    )

    return layout