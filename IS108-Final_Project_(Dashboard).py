import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

ORANGE      = "#E8834A"  
ORANGE_LIGHT= "#F5C49A"  
ORANGE_PALE = "#FDF0E6"   
ORANGE_DARK = "#C05E28"   

BG          = "#FBF7F3"   
SURFACE     = "#FFFFFF"   
HEADER_BG   = "#3D2610"   
BORDER      = "#EDD9C8"  

FARM_COLORS = {
    "Farm 1": "#E8834A",   
    "Farm 2": "#6B8E6B",   
    "Farm 3": "#8B6B9E",  
    "Farm 4": "#C4956A", 
    "Farm 5": "#6B8FAB",  
    "Farm 6": "#B87B6B",   
}

TEXT_DARK   = "#2C1A0E"   
TEXT_MID    = "#6B4E35"   
TEXT_LIGHT  = "#A07850"   


CHART_SEQ = [
    ORANGE, "#6B8E6B", "#8B6B9E", "#C4956A", "#6B8FAB", "#B87B6B"
]

# DATA 

FARMS = ["Farm 1", "Farm 2", "Farm 3", "Farm 4", "Farm 5", "Farm 6"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov"]
MONTH_KEYS = ["2024-01","2024-02","2024-03","2024-04","2024-05","2024-06",
              "2024-07","2024-08","2024-09","2024-10","2024-11"]

FARM_STATS = {
    "Farm 1": {"hds":354319,"kg":405455,"alw":1.386,"carcass":78.30,"invoice":78.38,"byp":13.79,"std_c":2.99,"std_i":3.15,"batches":25,"pct":17.1},
    "Farm 2": {"hds":431756,"kg":470692,"alw":1.413,"carcass":76.06,"invoice":76.51,"byp":14.48,"std_c":2.82,"std_i":2.04,"batches":30,"pct":20.8},
    "Farm 3": {"hds":355510,"kg":395757,"alw":1.894,"carcass":76.91,"invoice":77.35,"byp":14.05,"std_c":3.91,"std_i":3.32,"batches":27,"pct":17.1},
    "Farm 4": {"hds":340037,"kg":380053,"alw":1.423,"carcass":77.15,"invoice":77.60,"byp":13.77,"std_c":3.10,"std_i":2.68,"batches":26,"pct":16.4},
    "Farm 5": {"hds":353561,"kg":403933,"alw":1.498,"carcass":76.65,"invoice":76.93,"byp":13.39,"std_c":2.28,"std_i":2.43,"batches":24,"pct":17.0},
    "Farm 6": {"hds":241286,"kg":268569,"alw":1.456,"carcass":76.31,"invoice":76.86,"byp":13.78,"std_c":3.37,"std_i":2.53,"batches":16,"pct":11.6},
}

MONTHLY_TOTAL = [306536,220751,123431,187143,185412,173441,194098,230555,243472,182313,29317]

MONTHLY_PER_FARM = {
    "Farm 1": [47346,63064,0,0,63321,0,93253,0,87335,0,0],
    "Farm 2": [87415,32142,65669,0,79677,0,79323,0,0,87530,0],
    "Farm 3": [123355,0,57762,0,42414,0,0,72616,0,59363,0],
    "Farm 4": [48420,50472,0,46974,0,84370,0,74381,0,35420,0],
    "Farm 5": [0,75073,0,66920,0,69877,0,83558,28816,0,29317],
    "Farm 6": [0,0,0,73249,0,19194,21522,0,127321,0,0],
}

MONTHLY_CARCASS = {
    "Farm 1": [79.88,76.31,None,None,83.29,None,76.35,None,77.73,None,None],
    "Farm 2": [78.36,76.60,73.71,None,76.36,None,77.06,None,None,74.62,None],
    "Farm 3": [77.75,None,78.03,None,78.38,None,None,75.06,None,75.83,None],
    "Farm 4": [80.34,76.28,None,75.91,None,76.28,None,77.99,None,77.41,None],
    "Farm 5": [None,76.77,None,77.34,None,76.56,None,74.96,77.55,None,76.61],
    "Farm 6": [None,None,None,72.81,None,79.82,80.17,None,76.22,None,None],
}

DOW_LABELS = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
DOW_VALUES = [460339,377560,273567,317090,212127,334597,101189]
DOW_BATCHES = [30,27,20,25,14,25,7]

OUTLIERS = [
    {"date":"Jan 17","farm":"Farm 3","metric":"Carcass Yield","value":"65.01%","type":"Below lower bound"},
    {"date":"Jan 23","farm":"Farm 3","metric":"Carcass Yield","value":"84.65%","type":"Above upper bound"},
    {"date":"Mar 6", "farm":"Farm 2","metric":"Carcass Yield","value":"65.48%","type":"Below lower bound"},
    {"date":"Apr 26","farm":"Farm 6","metric":"Carcass Yield","value":"69.05%","type":"Below lower bound"},
    {"date":"May 4", "farm":"Farm 1","metric":"Carcass Yield","value":"84.11%","type":"Above upper bound"},
    {"date":"Jun 7", "farm":"Farm 4","metric":"Carcass Yield","value":"69.64%","type":"Below lower bound"},
    {"date":"Jan 23","farm":"Farm 3","metric":"Invoice Yield","value":"84.67%","type":"Above upper bound"},
    {"date":"May 4", "farm":"Farm 1","metric":"Invoice Yield","value":"84.17%","type":"Above upper bound"},
    {"date":"May 7", "farm":"Farm 1","metric":"Invoice Yield","value":"83.91%","type":"Above upper bound"},
    {"date":"Sep 11","farm":"Farm 6","metric":"Invoice Yield","value":"70.56%","type":"Below lower bound"},
]

CORR_LABELS = ["Carcass Y.","Invoice Y.","By-Product","ALW","Vol (HDS)"]
CORR_MATRIX = [
    [1.000, 0.909,-0.587,-0.002, 0.043],
    [0.909, 1.000,-0.551,-0.029, 0.046],
    [-0.587,-0.551, 1.000,-0.011,-0.013],
    [-0.002,-0.029,-0.011, 1.000,-0.003],
    [0.043, 0.046,-0.013,-0.003, 1.000],
]


CHART_LAYOUT = dict(
    paper_bgcolor=SURFACE,
    plot_bgcolor=SURFACE,
    font=dict(family="Arial, sans-serif", color=TEXT_DARK, size=11),
    margin=dict(l=40, r=20, t=30, b=40),
    hoverlabel=dict(bgcolor=SURFACE, font_size=11, bordercolor=BORDER),
)

def axis_style(title=""):
    return dict(
        title=dict(text=title, font=dict(size=11, color=TEXT_MID)),
        showgrid=True,
        gridcolor=BORDER,
        gridwidth=0.5,
        zeroline=False,
        linecolor=BORDER,
        tickfont=dict(size=10, color=TEXT_MID),
    )

def make_monthly_trend(active_farms):
    totals = [sum(MONTHLY_PER_FARM[f][i] for f in active_farms) for i in range(11)]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=MONTHS, y=totals,
        mode="lines+markers",
        line=dict(color=ORANGE, width=2.5),
        marker=dict(size=7, color=ORANGE, line=dict(color=SURFACE, width=1.5)),
        fill="tozeroy",
        fillcolor=ORANGE_PALE,
        hovertemplate="<b>%{x}</b><br>%{y:,.0f} heads<extra></extra>",
        name="Production"
    ))
    fig.update_layout(
        **CHART_LAYOUT,
        xaxis=axis_style("Month"),
        yaxis=axis_style("Heads Processed"),
        showlegend=False,
        yaxis_tickformat=",",
    )
    return fig


def make_farm_volume(active_farms):
    farms = [f for f in FARMS if f in active_farms]
    vals  = [FARM_STATS[f]["hds"] for f in farms]
    colors= [FARM_COLORS[f] for f in farms]
    fig = go.Figure(go.Bar(
        x=farms, y=vals,
        marker_color=colors,
        marker_line_width=0,
        text=[f"{v/1000:.0f}k" for v in vals],
        textposition="outside",
        textfont=dict(size=10, color=TEXT_DARK),
        hovertemplate="<b>%{x}</b><br>%{y:,.0f} heads<extra></extra>",
    ))
    fig.update_layout(
        **CHART_LAYOUT,
        xaxis=axis_style("Farm"),
        yaxis=axis_style("Total Heads"),
        showlegend=False,
        yaxis_tickformat=",",
    )
    return fig

def make_product_pie():
    labels = ["FCA Prime","FCA Other","FCB","FCC"]
    values = [1351379, 1950609, 110458, 15402]
    colors = [ORANGE, ORANGE_LIGHT, "#6B8E6B", "#B87B6B"]
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.45,
        marker=dict(colors=colors, line=dict(color=SURFACE, width=2)),
        textinfo="percent",
        textfont=dict(size=11),
        hovertemplate="<b>%{label}</b><br>%{value:,.0f} heads<br>%{percent}<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        font=dict(family="Arial, sans-serif", color=TEXT_DARK, size=11),
        margin=dict(l=10, r=120, t=10, b=10),
        showlegend=True,
        legend=dict(orientation="v", x=1.02, y=0.5,
                    font=dict(size=10, color=TEXT_MID)),
        hoverlabel=dict(bgcolor=SURFACE, font_size=11, bordercolor=BORDER),
    )
    return fig


def make_carcass_yield(active_farms):
    farms = [f for f in FARMS if f in active_farms]
    vals  = [FARM_STATS[f]["carcass"] for f in farms]
    avg   = sum(vals)/len(vals) if vals else 76.91
    colors= [FARM_COLORS[f] for f in farms]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=farms, y=vals,
        marker_color=colors,
        marker_line_width=0,
        text=[f"{v:.2f}%" for v in vals],
        textposition="outside",
        textfont=dict(size=10, color=TEXT_DARK),
        hovertemplate="<b>%{x}</b><br>Carcass Yield: %{y:.2f}%<extra></extra>",
        name="Carcass Yield"
    ))
    fig.add_hline(y=avg, line_dash="dash", line_color=TEXT_MID,
                  line_width=1.5,
                  annotation_text=f"Avg {avg:.2f}%",
                  annotation_font_size=10,
                  annotation_font_color=TEXT_MID)
    fig.update_layout(
        **CHART_LAYOUT,
        xaxis=axis_style("Farm"),
        yaxis=dict(**axis_style("Carcass Yield (%)"), range=[73,81]),
        showlegend=False,
    )
    return fig


def make_yield_comparison(active_farms):
    farms = [f for f in FARMS if f in active_farms]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Carcass Yield",
        x=farms,
        y=[FARM_STATS[f]["carcass"] for f in farms],
        marker_color=ORANGE,
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Carcass: %{y:.2f}%<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Invoice Yield",
        x=farms,
        y=[FARM_STATS[f]["invoice"] for f in farms],
        marker_color="#6B8E6B",
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Invoice: %{y:.2f}%<extra></extra>",
    ))
    fig.update_layout(
        **CHART_LAYOUT,
        barmode="group",
        xaxis=axis_style("Farm"),
        yaxis=dict(**axis_style("Yield (%)"), range=[74,81]),
        legend=dict(orientation="h", y=1.12, x=0,
                    font=dict(size=10, color=TEXT_MID)),
    )
    return fig


def make_monthly_yield_trend(active_farms):
    fig = go.Figure()
    for farm in [f for f in FARMS if f in active_farms]:
        y = MONTHLY_CARCASS[farm]
        fig.add_trace(go.Scatter(
            x=MONTHS, y=y,
            name=farm,
            mode="lines+markers",
            line=dict(color=FARM_COLORS[farm], width=2),
            marker=dict(size=5, color=FARM_COLORS[farm]),
            connectgaps=True,
            hovertemplate=f"<b>{farm}</b><br>%{{x}}: %{{y:.2f}}%<extra></extra>",
        ))
    fig.update_layout(
        **CHART_LAYOUT,
        xaxis=axis_style("Month"),
        yaxis=dict(**axis_style("Carcass Yield (%)"), range=[70,86]),
        legend=dict(orientation="h", y=1.12, x=0,
                    font=dict(size=10, color=TEXT_MID),
                    bgcolor="rgba(0,0,0,0)"),
    )
    return fig


def make_dow_chart():
    colors = [ORANGE if d not in ["Sat","Sun"] else "#C4956A" for d in DOW_LABELS]
    fig = go.Figure(go.Bar(
        x=DOW_LABELS, y=DOW_VALUES,
        marker_color=colors,
        marker_line_width=0,
        text=[f"{v/1000:.0f}k" for v in DOW_VALUES],
        textposition="outside",
        textfont=dict(size=10),
        hovertemplate="<b>%{x}</b><br>%{y:,.0f} heads<extra></extra>",
        name="Total Heads"
    ))
    fig.update_layout(
        **CHART_LAYOUT,
        xaxis=axis_style("Day of Week"),
        yaxis=axis_style("Total Heads"),
        showlegend=False,
        yaxis_tickformat=",",
    )
    return fig


def make_alw_chart(active_farms):
    farms = [f for f in FARMS if f in active_farms]
    vals  = [FARM_STATS[f]["alw"] for f in farms]
    colors= [FARM_COLORS[f] for f in farms]
    fig = go.Figure(go.Bar(
        y=farms, x=vals,
        orientation="h",
        marker_color=colors,
        marker_line_width=0,
        text=[f"{v:.2f} kg" for v in vals],
        textposition="outside",
        textfont=dict(size=10, color=TEXT_DARK),
        hovertemplate="<b>%{y}</b><br>Avg ALW: %{x:.3f} kg<extra></extra>",
    ))
    fig.update_layout(
        **CHART_LAYOUT,
        xaxis=dict(**axis_style("Average Live Weight (kg)"), range=[0, 2.5]),
        yaxis=dict(showgrid=False, tickfont=dict(size=10)),
        showlegend=False,
    )
    return fig


def make_heatmap():
    text_vals = [[f"{v:.2f}" for v in row] for row in CORR_MATRIX]
    fig = go.Figure(go.Heatmap(
        z=CORR_MATRIX,
        x=CORR_LABELS,
        y=CORR_LABELS,
        text=text_vals,
        texttemplate="%{text}",
        textfont=dict(size=11),
        colorscale=[
            [0.0, "#B87B6B"],
            [0.5, SURFACE],
            [1.0, ORANGE],
        ],
        zmid=0,
        zmin=-1, zmax=1,
        showscale=True,
        colorbar=dict(
            thickness=12,
            tickfont=dict(size=10, color=TEXT_MID),
            outlinewidth=0,
        ),
        hovertemplate="<b>%{y} vs %{x}</b><br>r = %{z:.3f}<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        font=dict(family="Arial, sans-serif", color=TEXT_DARK, size=11),
        margin=dict(l=90, r=60, t=10, b=80),
        hoverlabel=dict(bgcolor=SURFACE, font_size=11, bordercolor=BORDER),
        xaxis=dict(tickfont=dict(size=10, color=TEXT_MID), side="bottom"),
        yaxis=dict(tickfont=dict(size=10, color=TEXT_MID), autorange="reversed"),
    )
    return fig


def make_byproduct_chart(active_farms):
    farms = [f for f in FARMS if f in active_farms]
    vals  = [FARM_STATS[f]["byp"] for f in farms]
    colors= [FARM_COLORS[f] for f in farms]
    fig = go.Figure(go.Bar(
        x=farms, y=vals,
        marker_color=colors,
        marker_line_width=0,
        text=[f"{v:.2f}%" for v in vals],
        textposition="outside",
        textfont=dict(size=10, color=TEXT_DARK),
        hovertemplate="<b>%{x}</b><br>By-Product Recovery: %{y:.2f}%<extra></extra>",
    ))
    avg = sum(vals)/len(vals) if vals else 13.91
    fig.add_hline(y=avg, line_dash="dash", line_color=TEXT_MID, line_width=1.5,
                  annotation_text=f"Avg {avg:.2f}%",
                  annotation_font_size=10,
                  annotation_font_color=TEXT_MID)
    fig.update_layout(
        **CHART_LAYOUT,
        xaxis=axis_style("Farm"),
        yaxis=dict(**axis_style("By-Product Recovery (%)"), range=[11, 17]),
        showlegend=False,
    )
    return fig


def make_consistency_chart(active_farms):
    farms = [f for f in FARMS if f in active_farms]
    means = [FARM_STATS[f]["invoice"] for f in farms]
    stds  = [FARM_STATS[f]["std_i"] for f in farms]
    colors= [FARM_COLORS[f] for f in farms]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=farms, y=means,
        marker_color=colors,
        marker_line_width=0,
        error_y=dict(type="data", array=stds, visible=True,
                     color=TEXT_MID, thickness=1.5, width=6),
        text=[f"{m:.2f}%\n±{s:.2f}" for m,s in zip(means,stds)],
        textposition="outside",
        textfont=dict(size=9, color=TEXT_DARK),
        hovertemplate="<b>%{x}</b><br>Mean: %{y:.2f}%<extra></extra>",
    ))
    fig.update_layout(
        **CHART_LAYOUT,
        xaxis=axis_style("Farm"),
        yaxis=dict(**axis_style("Invoice Yield (%)"), range=[72, 86]),
        showlegend=False,
    )
    return fig

def kpi_card(label, value, sub="", color=ORANGE, border_color=ORANGE):
    return html.Div([
        html.P(label, style={
            "fontSize":"10px","fontWeight":"600","textTransform":"uppercase",
            "letterSpacing":"0.8px","color":TEXT_LIGHT,"margin":"0 0 6px 0"
        }),
        html.P(value, style={
            "fontSize":"22px","fontWeight":"700","color":color,
            "margin":"0 0 2px 0","lineHeight":"1"
        }),
        html.P(sub, style={
            "fontSize":"10px","color":TEXT_MID,"margin":"0"
        }),
    ], style={
        "background":SURFACE,
        "borderRadius":"8px",
        "padding":"14px 16px",
        "border":f"0.5px solid {BORDER}",
        "borderTop":f"3px solid {border_color}",
        "flex":"1",
        "minWidth":"130px",
    })


def insight_box(text):
    return html.Div(text, style={
        "marginTop":"10px",
        "padding":"8px 12px",
        "background":ORANGE_PALE,
        "borderLeft":f"3px solid {ORANGE}",
        "borderRadius":"0 6px 6px 0",
        "fontSize":"11px",
        "color":TEXT_MID,
        "lineHeight":"1.6",
    })


def section_title(text, subtitle=""):
    return html.Div([
        html.P(text, style={
            "fontSize":"13px","fontWeight":"700",
            "color":TEXT_DARK,"margin":"0 0 2px 0"
        }),
        html.P(subtitle, style={
            "fontSize":"11px","color":TEXT_MID,"margin":"0 0 12px 0"
        }) if subtitle else None
    ])


def panel(*children, style=None):
    base = {
        "background":SURFACE,
        "borderRadius":"10px",
        "border":f"0.5px solid {BORDER}",
        "padding":"16px",
        "overflow":"hidden",
    }
    if style:
        base.update(style)
    return html.Div(list(children), style=base)


#OUTLIER TABLE 

def outlier_table():
    header = html.Tr([
        html.Th(h, style={
            "background":HEADER_BG,"color":"#FFF",
            "padding":"8px 10px","fontSize":"10px",
            "textTransform":"uppercase","letterSpacing":"0.5px",
            "fontWeight":"600","textAlign":"left"
        }) for h in ["Date","Farm","Metric","Value","Type"]
    ])
    rows = []
    for o in OUTLIERS:
        badge_color = "#C4956A" if "Below" in o["type"] else ORANGE
        rows.append(html.Tr([
            html.Td(o["date"], style={"padding":"7px 10px","fontSize":"11px","borderBottom":f"0.5px solid {BORDER}"}),
            html.Td(o["farm"], style={"padding":"7px 10px","fontSize":"11px","color":FARM_COLORS[o["farm"]],"fontWeight":"600","borderBottom":f"0.5px solid {BORDER}"}),
            html.Td(o["metric"], style={"padding":"7px 10px","fontSize":"11px","borderBottom":f"0.5px solid {BORDER}"}),
            html.Td(o["value"], style={"padding":"7px 10px","fontSize":"11px","fontWeight":"600","borderBottom":f"0.5px solid {BORDER}"}),
            html.Td(
                html.Span(o["type"], style={
                    "background": "#FDF0E6" if "Above" in o["type"] else "#F5EBE0",
                    "color": badge_color,
                    "padding":"2px 8px","borderRadius":"10px",
                    "fontSize":"10px","fontWeight":"600"
                }),
                style={"padding":"7px 10px","borderBottom":f"0.5px solid {BORDER}"}
            ),
        ]))
    return html.Table([html.Thead(header), html.Tbody(rows)],
                      style={"width":"100%","borderCollapse":"collapse"})

def scorecard_table(active_farms):
    farms = [f for f in FARMS if f in active_farms]
    max_hds = max(FARM_STATS[f]["hds"] for f in farms)
    top = max(farms, key=lambda f: FARM_STATS[f]["hds"])
    low = min(farms, key=lambda f: FARM_STATS[f]["hds"])

    header = html.Tr([
        html.Th(h, style={
            "background":HEADER_BG,"color":"#FFF",
            "padding":"8px 10px","fontSize":"10px",
            "textTransform":"uppercase","letterSpacing":"0.5px",
            "fontWeight":"600","textAlign":"left"
        }) for h in ["Farm","Total HDS","% Share","Avg ALW","Carcass Yield","Invoice Yield","By-Product","Batches","Status"]
    ])

    rows = []
    for i, f in enumerate(farms):
        d = FARM_STATS[f]
        bg = SURFACE if i % 2 == 0 else ORANGE_PALE

        if f == top:
            badge = html.Span("Top Farm", style={"background":"#E8F5E8","color":"#2D6A2D","padding":"2px 8px","borderRadius":"10px","fontSize":"10px","fontWeight":"600"})
        elif f == low:
            badge = html.Span("Needs Review", style={"background":"#FDF0E6","color":ORANGE_DARK,"padding":"2px 8px","borderRadius":"10px","fontSize":"10px","fontWeight":"600"})
        else:
            badge = html.Span("Active", style={"background":"#EEF3FA","color":"#4A6FA5","padding":"2px 8px","borderRadius":"10px","fontSize":"10px","fontWeight":"600"})

        rows.append(html.Tr([
            html.Td([
                html.Span(style={"display":"inline-block","width":"8px","height":"8px","borderRadius":"50%","background":FARM_COLORS[f],"marginRight":"6px"}),
                html.Strong(f)
            ], style={"padding":"8px 10px","fontSize":"11px","background":bg,"borderBottom":f"0.5px solid {BORDER}"}),
            html.Td(f"{d['hds']:,}", style={"padding":"8px 10px","fontSize":"11px","background":bg,"borderBottom":f"0.5px solid {BORDER}"}),
            html.Td(f"{d['pct']}%", style={"padding":"8px 10px","fontSize":"11px","background":bg,"borderBottom":f"0.5px solid {BORDER}"}),
            html.Td(f"{d['alw']:.2f} kg", style={"padding":"8px 10px","fontSize":"11px","background":bg,"borderBottom":f"0.5px solid {BORDER}"}),
            html.Td(f"{d['carcass']:.2f}%", style={"padding":"8px 10px","fontSize":"11px","background":bg,"borderBottom":f"0.5px solid {BORDER}","fontWeight":"600","color":ORANGE_DARK if d['carcass']>77 else TEXT_DARK}),
            html.Td(f"{d['invoice']:.2f}%", style={"padding":"8px 10px","fontSize":"11px","background":bg,"borderBottom":f"0.5px solid {BORDER}"}),
            html.Td(f"{d['byp']:.2f}%", style={"padding":"8px 10px","fontSize":"11px","background":bg,"borderBottom":f"0.5px solid {BORDER}"}),
            html.Td(str(d["batches"]), style={"padding":"8px 10px","fontSize":"11px","background":bg,"borderBottom":f"0.5px solid {BORDER}"}),
            html.Td(badge, style={"padding":"8px 10px","background":bg,"borderBottom":f"0.5px solid {BORDER}"}),
        ]))

    return html.Table([html.Thead(header), html.Tbody(rows)],
                      style={"width":"100%","borderCollapse":"collapse","fontSize":"11px"})


# ─── APP LAYOUT ──────────────────────────────────────────────────────────────

app = dash.Dash(__name__, title="Poultry BI Dashboard")
app.config.suppress_callback_exceptions = True

app.layout = html.Div([

    # ── Z ROW 1: HEADER (top-left anchor) ─────────────────────────────────
    html.Div([
        html.Div([
            html.P("IS108 – IJK1  ·  Business Intelligence  ·  Caraga State University", style={
                "fontSize":"10px","letterSpacing":"1.5px","textTransform":"uppercase",
                "color":ORANGE_LIGHT,"marginBottom":"4px"
            }),
            html.H1("Poultry Production & Dressing", style={
                "fontSize":"20px","fontWeight":"700","color":"#FFFFFF",
                "margin":"0","letterSpacing":"-0.3px"
            }),
            html.P("Business Intelligence Dashboard", style={
                "fontSize":"13px","color":ORANGE_LIGHT,"margin":"2px 0 0 0"
            }),
        ]),
        html.Div([
            html.P("Dataset Period", style={"fontSize":"10px","color":ORANGE_LIGHT,"margin":"0"}),
            html.P("Jan 2, 2024 – Nov 3, 2024", style={"fontSize":"13px","fontWeight":"600","color":"#FFF","margin":"1px 0"}),
            html.P("148 batches  ·  6 farms  ·  11 months", style={"fontSize":"10px","color":ORANGE_LIGHT,"margin":"0"}),
        ], style={"textAlign":"right"}),
    ], style={
        "background":HEADER_BG,
        "padding":"18px 32px",
        "display":"flex",
        "alignItems":"center",
        "justifyContent":"space-between",
        "borderBottom":f"3px solid {ORANGE}",
    }),

    # ── FARM FILTER ────────────────────────────────────────────────────────
    html.Div([
        html.Span("Filter by farm:", style={
            "fontSize":"10px","fontWeight":"600","textTransform":"uppercase",
            "letterSpacing":"1px","color":TEXT_MID,"marginRight":"8px"
        }),
        dcc.Checklist(
            id="farm-filter",
            options=[{"label": f"  {f}", "value": f} for f in FARMS],
            value=FARMS,
            inline=True,
            style={"display":"inline-flex","gap":"6px","flexWrap":"wrap"},
            labelStyle={
                "padding":"4px 12px","borderRadius":"20px",
                "border":f"1px solid {BORDER}",
                "fontSize":"11px","cursor":"pointer","color":TEXT_MID,
                "background":SURFACE,"marginRight":"4px",
            },
            inputStyle={"marginRight":"5px"},
        ),
    ], style={
        "background":SURFACE,
        "padding":"10px 32px",
        "borderBottom":f"0.5px solid {BORDER}",
        "display":"flex","alignItems":"center","flexWrap":"wrap",
    }),

    # ── TABS ───────────────────────────────────────────────────────────────
    html.Div([
        dcc.Tabs(id="tabs", value="overview", children=[
            dcc.Tab(label="Overview",          value="overview"),
            dcc.Tab(label="Production Trend",  value="production"),
            dcc.Tab(label="Yield Analysis",    value="yield"),
            dcc.Tab(label="Farm Comparison",   value="farms"),
            dcc.Tab(label="Product Categories",value="product"),
            dcc.Tab(label="Outliers & KPIs",   value="outliers"),
        ], style={"fontFamily":"Arial, sans-serif"},
        colors={"border":BORDER,"primary":ORANGE,"background":SURFACE}),
    ], style={"background":SURFACE,"borderBottom":f"0.5px solid {BORDER}","padding":"0 32px"}),

    # ── TAB CONTENT ────────────────────────────────────────────────────────
    html.Div(id="tab-content", style={
        "padding":"20px 32px",
        "background":BG,
        "minHeight":"calc(100vh - 180px)",
    }),

    # ── FOOTER ─────────────────────────────────────────────────────────────
    html.Div(
        "CSC 126 – IJK1 Business Intelligence Final Project  ·  Caraga State University  ·  Dataset: Jan 2, 2024 – Nov 3, 2024  ·  148 records  ·  6 farms",
        style={
            "textAlign":"center","padding":"14px 32px",
            "fontSize":"10px","color":TEXT_MID,
            "borderTop":f"0.5px solid {BORDER}",
            "background":SURFACE,
        }
    ),

], style={
    "fontFamily":"Arial, sans-serif",
    "background":BG,
    "minHeight":"100vh",
    "width":"100%",
})


# ─── CALLBACKS ────────────────────────────────────────────────────────────────

@app.callback(
    Output("tab-content","children"),
    Input("tabs","value"),
    Input("farm-filter","value"),
)
def render_tab(tab, active_farms):
    if not active_farms:
        active_farms = FARMS

    af = active_farms

    # Computed KPIs
    total_hds   = sum(FARM_STATS[f]["hds"] for f in af)
    total_kg    = sum(FARM_STATS[f]["kg"]  for f in af)
    avg_alw     = sum(FARM_STATS[f]["alw"] for f in af) / len(af)
    avg_carcass = sum(FARM_STATS[f]["carcass"] for f in af) / len(af)
    avg_invoice = sum(FARM_STATS[f]["invoice"] for f in af) / len(af)
    avg_byp     = sum(FARM_STATS[f]["byp"] for f in af) / len(af)
    top_farm    = max(af, key=lambda f: FARM_STATS[f]["hds"])
    low_farm    = min(af, key=lambda f: FARM_STATS[f]["hds"])
    best_yield  = max(af, key=lambda f: FARM_STATS[f]["carcass"])

    # ── Z ROW 2: KPI CARDS (left to right) ───────────────────────────────
    kpi_row = html.Div([
        kpi_card("Total Dressing Volume", f"{total_hds:,}", "heads processed", ORANGE, ORANGE),
        kpi_card("Total Weight (KG)", f"{total_kg:,}", "kg processed", "#6B8E6B", "#6B8E6B"),
        kpi_card("Average ALW", f"{avg_alw:.2f} kg", "avg live weight", "#8B6B9E", "#8B6B9E"),
        kpi_card("Avg Carcass Yield", f"{avg_carcass:.2f}%", "dressing efficiency", ORANGE_DARK, ORANGE_DARK),
        kpi_card("Avg Invoice Yield", f"{avg_invoice:.2f}%", "saleable output", "#6B8FAB", "#6B8FAB"),
        kpi_card("By-Product Recovery", f"{avg_byp:.2f}%", "avg recovery rate", "#B87B6B", "#B87B6B"),
        kpi_card("Top Farm", top_farm, f"{FARM_STATS[top_farm]['hds']:,} heads", ORANGE, ORANGE),
        kpi_card("Lowest Farm", low_farm, f"{FARM_STATS[low_farm]['hds']:,} heads", "#C4956A", "#C4956A"),
    ], style={"display":"flex","gap":"10px","flexWrap":"wrap","marginBottom":"16px"})

    # ── OVERVIEW TAB ──────────────────────────────────────────────────────
    if tab == "overview":
        return html.Div([
            kpi_row,
            # Z Row 3: Big chart left, supporting right
            html.Div([
                panel(
                    section_title("Monthly Production Trend",
                                  "Total heads processed per month — Jan to Nov 2024"),
                    dcc.Graph(figure=make_monthly_trend(af), config={"displayModeBar":False},
                              style={"height":"220px"}),
                    insight_box("January peaked at 306,536 heads. March dropped 60% to 123,431 — the sharpest dip in the dataset. Recovery was gradual through Q3, reaching 243,472 in September before tapering toward year-end."),
                    style={"flex":"2","minWidth":"300px"}
                ),
                panel(
                    section_title("Product Category Distribution",
                                  "Share of total heads by product grade"),
                    dcc.Graph(figure=make_product_pie(), config={"displayModeBar":False},
                              style={"height":"220px"}),
                    insight_box("FCA categories total 96.3% of output. FCB and FCC together are only 3.6%, confirming consistently high product grading across all farms."),
                    style={"flex":"1","minWidth":"220px"}
                ),
            ], style={"display":"flex","gap":"14px","marginBottom":"14px"}),

            # Z Row 4: Full-width volume bar
            panel(
                section_title("Total Dressing Volume by Farm",
                              "Cumulative heads processed per farm — Jan to Nov 2024"),
                dcc.Graph(figure=make_farm_volume(af), config={"displayModeBar":False},
                          style={"height":"180px"}),
                insight_box("Farm 2 leads at 431,756 heads (20.8% of total). Farm 6 trails at 241,286 heads — 44% less than Farm 2 and the lowest among all farms."),
                style={"marginBottom":"14px"}
            ),

            # Z Row 5: Two charts side by side — completes the Z diagonal
            html.Div([
                panel(
                    section_title("Average ALW by Farm","Average live weight per chicken (kg)"),
                    dcc.Graph(figure=make_alw_chart(af), config={"displayModeBar":False},
                              style={"height":"180px"}),
                    insight_box("Farm 3 has the heaviest chicken at 1.89 kg avg ALW, yet its carcass yield is only average — heavier chicken do not guarantee better dressing results."),
                    style={"flex":"1"}
                ),
                panel(
                    section_title("Production by Day of Week","Total heads per day — weekly scheduling pattern"),
                    dcc.Graph(figure=make_dow_chart(), config={"displayModeBar":False},
                              style={"height":"180px"}),
                    insight_box("Monday is the busiest day at 460,339 heads (30 batches). Wednesday and Friday are underutilized. Redistributing mid-week batches would balance plant load."),
                    style={"flex":"1"}
                ),
            ], style={"display":"flex","gap":"14px"}),
        ])

    # PRODUCTION TAB 
    elif tab == "production":
        return html.Div([
            kpi_row,
            html.Div([
                panel(
                    section_title("Monthly Production Trend — Full View",
                                  "Total heads per month across all selected farms"),
                    dcc.Graph(figure=make_monthly_trend(af), config={"displayModeBar":False},
                              style={"height":"250px"}),
                    insight_box("The March 2024 dip is operation-wide — not linked to one farm. Production recovered steadily from July, strongest in August–September. November is partial (data ends Nov 3) and should not be compared to full months."),
                    style={"flex":"2","minWidth":"300px"}
                ),
                panel(
                    section_title("Average ALW by Farm","kg live weight per chicken"),
                    dcc.Graph(figure=make_alw_chart(af), config={"displayModeBar":False},
                              style={"height":"250px"}),
                    insight_box("Farm 3 processes the heaviest chicken (1.89 kg). Despite the highest ALW, its carcass yield is only at the dataset average — suggesting ALW alone does not drive yield."),
                    style={"flex":"1","minWidth":"220px"}
                ),
            ], style={"display":"flex","gap":"14px","marginBottom":"14px"}),
            panel(
                section_title("Production by Day of Week",
                              "Total heads and batch count per day — reveals weekly scheduling pattern"),
                dcc.Graph(figure=make_dow_chart(), config={"displayModeBar":False},
                          style={"height":"200px"}),
                insight_box("Monday is the peak day at 460,339 heads across 30 batches. Saturday remains active (334,597 heads). Wednesday (273,567) and Friday (212,127) are the lowest weekdays. A more even schedule could reduce Monday bottlenecks and improve plant utilization.")
            ),
        ])

    # YIELD TAB 
    elif tab == "yield":
        return html.Div([
            kpi_row,
            html.Div([
                panel(
                    section_title("Average Carcass Yield by Farm",
                                  "% of live weight becoming usable carcass — dashed line shows dataset average"),
                    dcc.Graph(figure=make_carcass_yield(af), config={"displayModeBar":False},
                              style={"height":"220px"}),
                    insight_box("Farm 1 leads at 78.30% — 1.39 points above the dataset average of 76.91%. Farm 2 has the lowest at 76.06% despite being the top volume producer. The dashed line marks the dataset average."),
                    style={"flex":"1"}
                ),
                panel(
                    section_title("Carcass Yield vs Invoice Yield",
                                  "Dressing efficiency vs actual saleable product — per farm"),
                    dcc.Graph(figure=make_yield_comparison(af), config={"displayModeBar":False},
                              style={"height":"220px"}),
                    insight_box("Invoice yield closely tracks carcass yield across all farms, meaning most of what is dressed gets sold. Farm 1 leads both metrics. The smallest gap between the two is at Farm 4."),
                    style={"flex":"1"}
                ),
            ], style={"display":"flex","gap":"14px","marginBottom":"14px"}),
            html.Div([
                panel(
                    section_title("By-Product Recovery by Farm",
                                  "% of recoverable by-products (feet, organs, etc.) — dashed line shows dataset average"),
                    dcc.Graph(figure=make_byproduct_chart(af), config={"displayModeBar":False},
                              style={"height":"200px"}),
                    insight_box("Farm 2 has the highest by-product recovery at 14.48% — but also the lowest carcass yield. This confirms the trade-off: r = -0.587. Farm 5 has the lowest recovery (13.39%) and above-average carcass yield."),
                    style={"flex":"1"}
                ),
                panel(
                    section_title("Invoice Yield Consistency",
                                  "Average invoice yield with variability (±std dev) — shorter error bar = more consistent"),
                    dcc.Graph(figure=make_consistency_chart(af), config={"displayModeBar":False},
                              style={"height":"200px"}),
                    insight_box("Farm 1 has the best average (78.38%) but highest variability (±3.15). Farm 2 is the most consistent farm (±2.04) — the most reliable for production planning and forecasting."),
                    style={"flex":"1"}
                ),
            ], style={"display":"flex","gap":"14px"}),
        ])

    # ── FARM COMPARISON TAB ───────────────────────────────────────────────
    elif tab == "farms":
        return html.Div([
            kpi_row,
            panel(
                section_title("KPI Scorecard — All Farms",
                              "Key performance indicators per farm with volume bar and status ranking"),
                html.Div(scorecard_table(af), style={"overflowX":"auto"}),
                insight_box("Farm 1 is the yield leader. Farm 2 is the volume leader. Farm 6 is the only farm with no standout metric — lowest volume (241,286 heads), fewest batches (16), and below-average yields across the board."),
                style={"marginBottom":"14px"}
            ),
            html.Div([
                panel(
                    section_title("Monthly Carcass Yield per Farm",
                                  "Month-by-month yield movement — reveals swings hidden by averages"),
                    dcc.Graph(figure=make_monthly_yield_trend(af), config={"displayModeBar":False},
                              style={"height":"230px"}),
                    insight_box("Farm 1 spiked to 83.29% in May — its highest recorded yield. Farm 2 dropped to 73.71% in March — its worst month. These swings confirm dressing conditions are not stable across batches and months."),
                    style={"flex":"1"}
                ),
                panel(
                    section_title("Correlation Heatmap",
                                  "Relationship strength between key production variables (r values)"),
                    dcc.Graph(figure=make_heatmap(), config={"displayModeBar":False},
                              style={"height":"230px"}),
                    insight_box("Carcass yield and invoice yield are very strongly correlated (r = 0.91). Carcass yield vs by-product recovery is r = -0.59 — a real operational trade-off. ALW shows almost no correlation with yield (r = -0.002)."),
                    style={"flex":"1"}
                ),
            ], style={"display":"flex","gap":"14px"}),
        ])

    # ── PRODUCT CATEGORIES TAB ────────────────────────────────────────────
    elif tab == "product":
        return html.Div([
            kpi_row,
            html.Div([
                panel(
                    section_title("Product Category Breakdown",
                                  "Total heads by product classification — FCA, FCB, FCC"),
                    dcc.Graph(figure=go.Figure(go.Bar(
                        x=["FCA Prime","FCA Other","FCB","FCC"],
                        y=[1351379,1950609,110458,15402],
                        marker_color=[ORANGE,ORANGE_LIGHT,"#6B8E6B","#B87B6B"],
                        marker_line_width=0,
                        text=["1,351,379\n(39.4%)","1,950,609\n(56.9%)","110,458\n(3.2%)","15,402\n(0.4%)"],
                        textposition="outside",
                        textfont=dict(size=10),
                        hovertemplate="<b>%{x}</b><br>%{y:,.0f} heads<extra></extra>",
                    )).update_layout(**CHART_LAYOUT,
                        xaxis=axis_style("Product Category"),
                        yaxis=dict(**axis_style("Total Heads"), tickformat=","),
                        showlegend=False),
                    config={"displayModeBar":False}, style={"height":"240px"}),
                    insight_box("FCA categories total 96.3% of all output. FCA Prime alone is 39.4% — the single highest-value classification. FCB (3.2%) and FCC (0.4%) combined are only 3.6%, indicating consistently high product grading."),
                    style={"flex":"2","minWidth":"300px"}
                ),
                panel(
                    section_title("Distribution Donut","Proportional share of total heads"),
                    dcc.Graph(figure=make_product_pie(), config={"displayModeBar":False},
                              style={"height":"200px"}),
                    html.Div([
                        html.Table([
                            html.Thead(html.Tr([html.Th(h,style={"padding":"4px 8px","fontSize":"10px","color":TEXT_MID,"fontWeight":"600","textAlign":"left","borderBottom":f"0.5px solid {BORDER}"}) for h in ["Category","HDS","Share"]])),
                            html.Tbody([
                                html.Tr([html.Td(c,style={"padding":"5px 8px","fontSize":"11px","borderBottom":f"0.5px solid {BORDER}"}),
                                         html.Td(v,style={"padding":"5px 8px","fontSize":"11px","borderBottom":f"0.5px solid {BORDER}"}),
                                         html.Td(p,style={"padding":"5px 8px","fontSize":"11px","borderBottom":f"0.5px solid {BORDER}","color":ORANGE_DARK,"fontWeight":"600"})])
                                for c,v,p in [
                                    ("FCA Prime","1,351,379","39.4%"),
                                    ("FCA Other","1,950,609","56.9%"),
                                    ("FCB","110,458","3.2%"),
                                    ("FCC","15,402","0.4%"),
                                    ("Total","3,427,848","100%"),
                                ]
                            ])
                        ], style={"width":"100%","borderCollapse":"collapse","marginTop":"8px","fontSize":"11px"})
                    ]),
                    style={"flex":"1","minWidth":"200px"}
                ),
            ], style={"display":"flex","gap":"14px"}),
        ])

    # ── OUTLIERS & KPIs TAB ───────────────────────────────────────────────
    elif tab == "outliers":
        return html.Div([
            kpi_row,
            html.Div([
                panel(
                    section_title("Outlier Detection — IQR Method",
                                  "Records falling outside Q1−1.5×IQR or Q3+1.5×IQR bounds"),
                    outlier_table(),
                    insight_box("6 outliers in carcass yield, 4 in invoice yield. Farm 3 had the lowest recorded carcass yield at 65.01% (Jan 17) — well below the normal range. Farm 1 had the highest at 84.11% (May 4). These likely reflect unusual batch conditions and should be verified by operations staff."),
                    style={"flex":"3","minWidth":"400px"}
                ),
                panel(
                    section_title("KPI Reference Card","Dataset-level performance benchmarks"),
                    html.Div([
                        html.Table([
                            html.Thead(html.Tr([
                                html.Th(h, style={"background":HEADER_BG,"color":"#FFF","padding":"8px 10px","fontSize":"10px","textTransform":"uppercase","letterSpacing":"0.5px","fontWeight":"600","textAlign":"left"})
                                for h in ["KPI","Value","Description"]
                            ])),
                            html.Tbody([
                                html.Tr([
                                    html.Td(k,style={"padding":"7px 10px","fontSize":"11px","fontWeight":"600","borderBottom":f"0.5px solid {BORDER}","background":ORANGE_PALE if i%2==0 else SURFACE}),
                                    html.Td(v,style={"padding":"7px 10px","fontSize":"11px","color":ORANGE_DARK,"fontWeight":"700","borderBottom":f"0.5px solid {BORDER}","background":ORANGE_PALE if i%2==0 else SURFACE}),
                                    html.Td(d,style={"padding":"7px 10px","fontSize":"10px","color":TEXT_MID,"borderBottom":f"0.5px solid {BORDER}","background":ORANGE_PALE if i%2==0 else SURFACE}),
                                ]) for i,(k,v,d) in enumerate([
                                    ("Total Volume","2,076,469 hds","All farms combined"),
                                    ("Total Weight","2,324,459 kg","All farms combined"),
                                    ("Avg ALW","1.52 kg","All batches avg"),
                                    ("Avg Carcass","76.91%","Dataset average"),
                                    ("Avg Invoice","77.28%","Dataset average"),
                                    ("Avg By-Product","13.91%","Dataset average"),
                                    ("Top Farm (vol)","Farm 2","431,756 heads"),
                                    ("Best Yield","Farm 1","78.30% carcass"),
                                    ("Lowest Farm","Farm 6","241,286 heads"),
                                    ("Top Category","FCA Prime","39.4% of output"),
                                ])
                            ])
                        ], style={"width":"100%","borderCollapse":"collapse"})
                    ]),
                    style={"flex":"2","minWidth":"280px"}
                ),
            ], style={"display":"flex","gap":"14px"}),
        ])

    return html.Div("Select a tab above.")


#RUN

server = app.server

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)
