import os
import sys
import pandas as pd
from dash import Dash, dcc, html, Input, Output

# Add the script directory to sys.path to ensure charts module is found
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from charts.comparison_charts import (
    make_column_chart, make_bar_chart,
    make_stacked_column, make_stacked_bar,
    make_clustered_column, make_clustered_bar,
)
from charts.relationship_charts import (
    make_scatter_discount_profit, make_scatter_sales_profit,
    make_scatter_shipping_profit, make_bubble_chart,
)
from charts.distribution_timeseries_charts import (
    make_histogram, make_box, make_violin, make_line, make_area,
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "cleaned_data.csv")
df_raw = pd.read_csv(DATA_PATH)
df_raw["Order Date"] = pd.to_datetime(df_raw["Order Date"])
df_raw["Ship Date"]  = pd.to_datetime(df_raw["Ship Date"])

def _add_segment_label(df):
    if "Segment_Label" not in df.columns:
        def get_seg(row):
            if row.get("Segment_Corporate", False):   return "Corporate"
            if row.get("Segment_Home Office", False): return "Home Office"
            return "Consumer"
        df = df.copy()
        df["Segment_Label"] = df.apply(get_seg, axis=1)
    return df

df_raw = _add_segment_label(df_raw)
df_raw["Category_Label"] = df_raw["Category"].str.title()

ALL_REGIONS    = sorted(df_raw["Region"].dropna().unique().tolist())
ALL_CATEGORIES = sorted(df_raw["Category_Label"].dropna().unique().tolist())
ALL_YEARS      = sorted(df_raw["Year"].dropna().unique().astype(int).tolist())

C_BG        = "#FAF7F2"      
C_SIDEBAR   = "#10462F"     
C_CARD      = "#FFFFFF"
C_ACCENT1   = "#D4612A"      
C_ACCENT2   = "#DDF0E4"     
C_ACCENT3   = "#E8C547"      
C_TEXT      = "#2A2A2A"
C_TEXT_SOFT = "#6B6B6B"
C_BORDER    = "#E8E0D5"
C_HEADER_BG = "#10462F"     

CHART_COLORS = [C_ACCENT1, C_ACCENT2, C_ACCENT3, "#A8786A", "#5C8A7A", "#C4952A"]
app = Dash(__name__, title="Superstore Dashboard", suppress_callback_exceptions=True)
server = app.server

# helper: filter
def filter_df(region, category, year_range):
    dff = df_raw.copy()
    if region != "ALL":    dff = dff[dff["Region"] == region]
    if category != "ALL":  dff = dff[dff["Category_Label"] == category]
    dff = dff[(dff["Year"] >= year_range[0]) & (dff["Year"] <= year_range[1])]
    return dff

label_s = {
    "color": "rgba(255,255,255,0.6)", "fontSize": "10px",
    "fontWeight": "600", "letterSpacing": "1px",
    "textTransform": "uppercase", "marginBottom": "6px",
    "marginTop": "18px", "display": "block",
}
card_s = {
    "background": C_CARD, "borderRadius": "8px",
    "padding": "18px", "border": f"1px solid {C_BORDER}",
    "boxShadow": "0 1px 6px rgba(0,0,0,0.05)",
}

def week_badge(txt):
    return html.Span(txt, style={
        "background": C_ACCENT1, "color": "white",
        "fontSize": "9px", "fontWeight": "700",
        "letterSpacing": "0.7px", "padding": "2px 9px",
        "borderRadius": "4px", "marginBottom": "10px",
        "display": "inline-block", "textTransform": "uppercase",
    })

def chart_card(fig_id, badge=None, wide=False):
    kids = []
    if badge: kids.append(week_badge(badge))
    kids.append(dcc.Graph(id=fig_id, style={"height": "400px"}, config={"displayModeBar": False}))
    extra = {"gridColumn": "1 / -1"} if wide else {}
    return html.Div(kids, style={**card_s, **extra})

def two_col(*kids):
    return html.Div(kids, style={
        "display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "20px",
    })

def sec_title(title, sub, badge):
    return html.Div([
        html.Span(badge, style={
            "background": C_SIDEBAR, "color": "rgba(255,255,255,0.85)",
            "fontSize": "9px", "fontWeight": "700", "letterSpacing": "1px",
            "padding": "2px 10px", "borderRadius": "4px",
            "display": "inline-block", "marginBottom": "10px",
            "textTransform": "uppercase",
        }),
        html.H2(title, style={
            "color": C_TEXT, "fontSize": "18px", "fontWeight": "700",
            "margin": "0 0 5px", "fontFamily": "'Georgia', 'Times New Roman', serif",
        }),
        html.P(sub, style={
            "color": C_TEXT_SOFT, "fontSize": "13px",
            "margin": "0 0 20px", "lineHeight": "1.55",
        }),
    ])

app.layout = html.Div(
    style={"fontFamily": "'Trebuchet MS', Verdana, sans-serif", "background": C_BG, "color": C_TEXT},
    children=[

        html.Div(style={
            "position": "fixed", "top": 0, "left": 0, "bottom": 0,
            "width": "255px", "background": C_SIDEBAR,
            "padding": "22px 18px", "overflowY": "auto", "zIndex": 999,
        }, children=[

            html.Div([
                html.Div("", style={"fontSize": "28px"}),
                html.H1("Superstore\nDashboard", style={
                    "color": "white", "fontSize": "15px", "fontWeight": "700",
                    "margin": "6px 0 3px", "lineHeight": "1.3",
                }),
                html.P("Sales & Profit Analysis", style={
                    "color": "rgba(255,255,255,0.45)", "fontSize": "11px", "margin": 0,
                }),
            ], style={"borderBottom": "1px solid rgba(255,255,255,0.12)", "paddingBottom": "18px"}),

            html.Label("Region", style=label_s),
            dcc.Dropdown(
                id="filter-region",
                options=[{"label": "All Regions", "value": "ALL"}] +
                        [{"label": r, "value": r} for r in ALL_REGIONS],
                value="ALL", clearable=False,
                style={"fontSize": "12px", "borderRadius": "6px"},
            ),

            html.Label("Category", style=label_s),
            dcc.Dropdown(
                id="filter-category",
                options=[{"label": "All Categories", "value": "ALL"}] +
                        [{"label": c, "value": c} for c in ALL_CATEGORIES],
                value="ALL", clearable=False,
                style={"fontSize": "12px", "borderRadius": "6px"},
            ),

            html.Label("Year Range", style=label_s),
            dcc.RangeSlider(
                id="filter-year",
                min=ALL_YEARS[0], max=ALL_YEARS[-1], step=1,
                value=[ALL_YEARS[0], ALL_YEARS[-1]],
                marks={y: {"label": str(y), "style": {"color": "rgba(255,255,255,0.55)", "fontSize": "10px"}}
                       for y in ALL_YEARS},
                tooltip={"placement": "bottom", "always_visible": False},
            ),

            html.Label("Scatter Chart View", style=label_s),
            dcc.RadioItems(
                id="filter-scatter",
                options=[
                    {"label": "Discount vs Profit",      "value": "discount_profit"},
                    {"label": "Sales vs Profit",         "value": "sales_profit"},
                    {"label": "Shipping Time vs Profit", "value": "shipping_profit"},
                ],
                value="discount_profit",
                labelStyle={"display": "block", "color": "rgba(255,255,255,0.75)",
                            "fontSize": "12px", "marginBottom": "5px"},
                inputStyle={"marginRight": "7px"},
            ),

            html.Hr(style={"borderColor": "rgba(255,255,255,0.1)", "marginTop": "22px"}),
            html.Div(id="sidebar-stats"),
        ]),

        html.Div(style={"marginLeft": "255px"}, children=[

            html.Div(style={
                "background": C_HEADER_BG, "padding": "32px 36px 28px", "color": "white",
            }, children=[

                html.H1("E-Commerce Sales Performance",
                        style={"fontSize": "26px", "fontWeight": "800", "margin": "0 0 8px",
                               "letterSpacing": "-0.3px", "fontFamily": "'Georgia', serif"}),

                html.Div(id="kpi-row", style={"marginTop": "26px"}),
            ]),

            html.Div(style={"padding": "28px 32px", "borderBottom": f"1px solid {C_BORDER}"}, children=[
                sec_title("Comparison Charts", "Comparison between categories and regions", "Section 1"),
                two_col(
                    chart_card("fig-column",        "Week 1 · Column Chart"),
                    chart_card("fig-bar",           "Week 1 · Bar Chart"),
                    chart_card("fig-stacked-col",   "Week 2 · Stacked Column"),
                    chart_card("fig-stacked-bar",   "Week 2 · Stacked Bar"),
                    chart_card("fig-clustered-col", "Week 2 · Clustered Column"),
                    chart_card("fig-clustered-bar", "Week 2 · Clustered Bar"),
                ),
            ]),  

            html.Div(style={"padding": "28px 32px", "borderBottom": f"1px solid {C_BORDER}"}, children=[
                sec_title("Relationship Charts", "Weeks 3 & 4", "Section 2"),
                two_col(
                    chart_card("fig-scatter", "Week 3 · Scatter Chart"),
                    chart_card("fig-bubble",  "Week 4 · Bubble Chart"),
                ),
            ]),

            html.Div(style={"padding": "28px 32px", "borderBottom": f"1px solid {C_BORDER}"}, children=[
                sec_title("Distribution Charts", "Weeks 5, 6 & 7", "Section 3"),
                two_col(
                    chart_card("fig-histogram", "Week 5 · Histogram"),
                    chart_card("fig-box",       "Week 6 · Box Chart"),
                    chart_card("fig-violin", "Week 7 · Violin Chart", wide=True),
                ),
            ]),

            html.Div(style={"padding": "28px 32px"}, children=[
                sec_title("Time-Series Charts", "Weeks 8 & 9", "Section 4"),
                html.Div([
                    chart_card("fig-line", "Week 8 · Line Chart",  wide=True),
                    html.Div(style={"height": "20px"}),
                    chart_card("fig-area", "Week 9 · Area Chart", wide=True),
                ]),
            ]),

            html.Div(
                "Sample Superstore Dataset  ·  Data Visualization Final Project  ·  Plotly Dash",
                style={"textAlign": "center", "color": C_TEXT_SOFT, "fontSize": "11px",
                       "padding": "16px", "borderTop": f"1px solid {C_BORDER}",
                       "background": "#F0EBE3"},
            ),
        ]),
    ],
)


@app.callback(
    Output("kpi-row",       "children"),
    Output("sidebar-stats", "children"),
    Input("filter-region",   "value"),
    Input("filter-category", "value"),
    Input("filter-year",     "value"),
)
def update_summary(region, category, year_range):
    dff = filter_df(region, category, year_range)
    total_sales  = dff["Sales"].sum()
    total_profit = dff["Profit"].sum()
    total_orders = dff["Order ID"].nunique()
    margin       = (total_profit / total_sales * 100) if total_sales > 0 else 0

    def kpi(lbl, val, color=C_ACCENT3):
        return html.Div([
            html.P(lbl, style={"margin": "0 0 3px", "fontSize": "10px",
                                "color": "rgba(255,255,255,0.55)", "letterSpacing": "0.8px",
                                "textTransform": "uppercase", "fontWeight": "600"}),
            html.H3(val, style={"margin": 0, "fontSize": "20px", "fontWeight": "800", "color": "white"}),
        ], style={
            "background": "rgba(255,255,255,0.09)", "borderRadius": "8px",
            "padding": "14px 18px", "borderLeft": f"3px solid {color}",
        })

    kpi_row = html.Div([
        kpi("Total Sales",   f"${total_sales:,.0f}",  C_ACCENT3),
        kpi("Total Profit",  f"${total_profit:,.0f}", C_ACCENT2),
        kpi("Orders",        f"{total_orders:,}",     C_ACCENT1),
        kpi("Profit Margin", f"{margin:.1f}%",        "#A8786A"),
    ], style={"display": "grid", "gridTemplateColumns": "repeat(4, 1fr)", "gap": "14px"})

    sidebar = html.Div([
        html.P("showing", style={"color": "rgba(255,255,255,0.45)", "fontSize": "10px",
                                  "margin": "0", "textTransform": "uppercase", "letterSpacing": "0.8px"}),
        html.H2(f"{len(dff):,}", style={"color": C_ACCENT3, "margin": "2px 0 0", "fontSize": "26px", "fontWeight": "800"}),
        html.P("records", style={"color": "rgba(255,255,255,0.4)", "fontSize": "10px", "margin": 0}),
    ], style={"marginTop": "12px"})

    return kpi_row, sidebar


@app.callback(
    Output("fig-column",        "figure"),
    Output("fig-bar",           "figure"),
    Output("fig-stacked-col",   "figure"),
    Output("fig-stacked-bar",   "figure"),
    Output("fig-clustered-col", "figure"),
    Output("fig-clustered-bar", "figure"),
    Input("filter-region",   "value"),
    Input("filter-category", "value"),
    Input("filter-year",     "value"),
)
def update_comparison(region, category, yr):
    dff = filter_df(region, category, yr)
    return (make_column_chart(dff), make_bar_chart(dff),
            make_stacked_column(dff), make_stacked_bar(dff),
            make_clustered_column(dff), make_clustered_bar(dff))


@app.callback(
    Output("fig-scatter", "figure"),
    Output("fig-bubble",  "figure"),
    Input("filter-region",   "value"),
    Input("filter-category", "value"),
    Input("filter-year",     "value"),
    Input("filter-scatter",  "value"),
)
def update_relationship(region, category, yr, scatter_type):
    dff = filter_df(region, category, yr)
    fn  = {"discount_profit": make_scatter_discount_profit,
           "sales_profit":    make_scatter_sales_profit,
           "shipping_profit": make_scatter_shipping_profit}.get(scatter_type, make_scatter_discount_profit)
    return fn(dff), make_bubble_chart(dff)


@app.callback(
    Output("fig-histogram", "figure"),
    Output("fig-box",       "figure"),
    Output("fig-violin",    "figure"),
    Input("filter-region",   "value"),
    Input("filter-category", "value"),
    Input("filter-year",     "value"),
)
def update_distribution(region, category, yr):
    dff = filter_df(region, category, yr)
    return make_histogram(dff), make_box(dff), make_violin(dff)


@app.callback(
    Output("fig-line", "figure"),
    Output("fig-area", "figure"),
    Input("filter-region",   "value"),
    Input("filter-category", "value"),
    Input("filter-year",     "value"),
)
def update_timeseries(region, category, yr):
    dff = filter_df(region, category, yr)
    return make_line(dff), make_area(dff)


if __name__ == "__main__":
    app.run(debug=True, port=8050)