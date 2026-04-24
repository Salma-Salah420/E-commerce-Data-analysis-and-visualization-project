# ============================================================
# distribution_timeseries_charts.py
# ============================================================

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ── helper: reconstruct Segment label from dummy columns ────
def _add_segment_label(df: pd.DataFrame) -> pd.DataFrame:
    """Adds a 'Segment_Label' column if not already present."""
    if 'Segment_Label' not in df.columns:
        def get_seg(row):
            if row.get('Segment_Corporate', False):
                return 'Corporate'
            if row.get('Segment_Home Office', False):
                return 'Home Office'
            return 'Consumer'
        df = df.copy()
        df['Segment_Label'] = df.apply(get_seg, axis=1)
    return df


# ============================================================
# 1. HISTOGRAM — Distribution of Sales per Order  (Week 5)
# ============================================================
def make_histogram(df: pd.DataFrame) -> go.Figure:
    """
    Histogram: Distribution of Sales per Order.
    Shows right-skewed sales with mean & median reference lines.
    """
    mean_val   = df['Sales'].mean()
    median_val = df['Sales'].median()

    fig = px.histogram(
        df,
        x='Sales',
        nbins=50,
        title='Distribution of Sales per Order',
        labels={'Sales': 'Sales Amount (USD)', 'count': 'Number of Orders'},
        color_discrete_sequence=['#2196F3'],
        opacity=0.8,
    )

    # Mean line
    fig.add_vline(
        x=mean_val,
        line_dash='dash',
        line_color='#9C27B0',
        line_width=2,
        annotation_text=f'Mean  ${mean_val:,.0f}',
        annotation_position='top right',
        annotation_font_color='#9C27B0',
    )

    # Median line
    fig.add_vline(
        x=median_val,
        line_dash='dash',
        line_color='#4CAF50',
        line_width=2,
        annotation_text=f'Median  ${median_val:,.0f}',
        annotation_position='top left',
        annotation_font_color='#4CAF50',
    )

    fig.update_layout(
        xaxis_title='Sales Amount (USD)',
        yaxis_title='Number of Orders',
        bargap=0.05,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=13),
        title_font_size=16,
        title_x=0.5,
        showlegend=False,
    )
    fig.update_xaxes(range=[0, df['Sales'].quantile(0.99)], showgrid=True, gridcolor='#eeeeee')
    fig.update_yaxes(showgrid=True, gridcolor='#eeeeee')

    return fig


# ============================================================
# 2. BOX PLOT — Profit Distribution by Category  (Week 6)
# ============================================================
def make_box(df: pd.DataFrame) -> go.Figure:
    """
    Box Plot: Profit Distribution by Product Category.
    Highlights median, IQR, outliers, and break-even line.
    """
    df_plot = df.copy()
    df_plot['Category'] = df_plot['Category'].str.title()

    fig = px.box(
        df_plot,
        x='Category',
        y='Profit',
        color='Category',
        title='Profit Distribution by Product Category',
        labels={'Profit': 'Profit (USD)', 'Category': 'Product Category'},
        color_discrete_sequence=['#2196F3', '#FF5722', '#4CAF50'],
        points='outliers',
    )

    # Break-even reference line
    fig.add_hline(
        y=0,
        line_dash='dash',
        line_color='red',
        line_width=1.8,
        annotation_text='Break-even (Profit = 0)',
        annotation_position='top left',
        annotation_font_color='red',
    )

    fig.update_layout(
        xaxis_title='Product Category',
        yaxis_title='Profit (USD)',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=13),
        title_font_size=16,
        title_x=0.5,
        showlegend=False,
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='#eeeeee')

    return fig


# ============================================================
# 3. VIOLIN CHART — Profit by Customer Segment  (Week 7)
# ============================================================
def make_violin(df: pd.DataFrame) -> go.Figure:
    """
    Violin Chart: Profit Distribution by Customer Segment.
    Shows full distribution shape per segment with box inside.
    """
    df_plot = _add_segment_label(df)

    fig = px.violin(
        df_plot,
        y='Segment_Label',
        x='Profit',
        color='Segment_Label',
        orientation='h',
        box=True,
        points=False,
        title='Profit Distribution by Customer Segment',
        labels={'Profit': 'Profit (USD)', 'Segment_Label': 'Customer Segment'},
        color_discrete_sequence=['#2196F3', '#FF5722', '#4CAF50'],
        category_orders={'Segment_Label': ['Consumer', 'Corporate', 'Home Office']},
    )

    # Break-even line
    fig.add_vline(
        x=0,
        line_dash='dash',
        line_color='red',
        line_width=2,
        annotation_text='Break-even',
        annotation_position='top',
        annotation_font_color='red',
    )

    fig.update_layout(
        xaxis_title='Profit (USD)',
        yaxis_title='Customer Segment',
        xaxis_range=[-1500, 3000],
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=13),
        title_font_size=16,
        title_x=0.5,
        showlegend=False,
    )
    fig.update_xaxes(showgrid=True, gridcolor='#eeeeee')
    fig.update_yaxes(showgrid=False)

    return fig


# ============================================================
# 4. LINE CHART — Monthly Sales & Profit Trends  (Week 8)
# ============================================================
def make_line(df: pd.DataFrame) -> go.Figure:
    """
    Line Chart: Monthly Sales & Profit Trends.
    Shows raw monthly values + 5-month moving average for both metrics.
    """
    df_plot = df.copy()
    df_plot['Order Date'] = pd.to_datetime(df_plot['Order Date'])

    monthly = (
        df_plot.groupby(df_plot['Order Date'].dt.to_period('M'))
               .agg(Sales=('Sales', 'sum'), Profit=('Profit', 'sum'))
               .reset_index()
    )
    monthly['Order Date']  = monthly['Order Date'].dt.to_timestamp()
    monthly['Sales_MA5']   = monthly['Sales'].rolling(5, center=True, min_periods=1).mean()
    monthly['Profit_MA5']  = monthly['Profit'].rolling(5, center=True, min_periods=1).mean()

    fig = go.Figure()

    # Raw faint lines
    fig.add_trace(go.Scatter(
        x=monthly['Order Date'], y=monthly['Sales'],
        mode='lines', name='Sales (raw)',
        line=dict(color='#2196F3', width=1),
        opacity=0.25, showlegend=False,
    ))
    fig.add_trace(go.Scatter(
        x=monthly['Order Date'], y=monthly['Profit'],
        mode='lines', name='Profit (raw)',
        line=dict(color='#FF5722', width=1),
        opacity=0.25, showlegend=False,
    ))

    # Bold moving average lines
    fig.add_trace(go.Scatter(
        x=monthly['Order Date'], y=monthly['Sales_MA5'],
        mode='lines', name='Sales (5-Month MA)',
        line=dict(color='#2196F3', width=2.5),
    ))
    fig.add_trace(go.Scatter(
        x=monthly['Order Date'], y=monthly['Profit_MA5'],
        mode='lines', name='Profit (5-Month MA)',
        line=dict(color='#FF5722', width=2.5),
    ))

    # Break-even line
    fig.add_hline(
        y=0,
        line_dash='dash',
        line_color='red',
        line_width=1.5,
        annotation_text='Break-even',
        annotation_position='top left',
        annotation_font_color='red',
    )

    fig.update_layout(
        title='Monthly Sales & Profit Trends (5-Month Moving Average)',
        xaxis_title='Order Date',
        yaxis_title='Amount (USD)',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=13),
        title_font_size=16,
        title_x=0.5,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0),
        hovermode='x unified',
    )
    fig.update_xaxes(showgrid=True, gridcolor='#eeeeee')
    fig.update_yaxes(showgrid=True, gridcolor='#eeeeee')

    return fig


# ============================================================
# 5. AREA CHART — Quarterly Sales by Category  (Week 9)
# ============================================================
def make_area(df: pd.DataFrame) -> go.Figure:
    """
    Stacked Area Chart: Quarterly Sales by Product Category.
    Shows each category's share of total quarterly revenue over time.
    """
    df_plot = df.copy()
    df_plot['Order Date'] = pd.to_datetime(df_plot['Order Date'])
    df_plot['Quarter']    = df_plot['Order Date'].dt.to_period('Q').dt.to_timestamp()
    df_plot['Category']   = df_plot['Category'].str.title()

    quarterly = (
        df_plot.groupby(['Quarter', 'Category'])['Sales']
               .sum()
               .reset_index()
    )

    fig = px.area(
        quarterly,
        x='Quarter',
        y='Sales',
        color='Category',
        title='Quarterly Sales by Product Category (Stacked Area)',
        labels={'Sales': 'Total Sales (USD)', 'Quarter': 'Quarter', 'Category': 'Category'},
        color_discrete_map={
            'Furniture':       '#FF5722',
            'Office Supplies': '#4CAF50',
            'Technology':      '#2196F3',
        },
    )

    fig.update_layout(
        xaxis_title='Quarter',
        yaxis_title='Total Sales (USD)',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=13),
        title_font_size=16,
        title_x=0.5,
        yaxis=dict(rangemode='tozero'),
        legend=dict(title='Category'),
        hovermode='x unified',
    )
    fig.update_xaxes(showgrid=True, gridcolor='#eeeeee')
    fig.update_yaxes(showgrid=True, gridcolor='#eeeeee', tickprefix='$', tickformat=',')

    return fig


# ============================================================
# Quick test — run this file directly to preview all charts
# ============================================================
if __name__ == '__main__':
    import os

    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'cleaned_data.csv')
    df = pd.read_csv(data_path)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date']  = pd.to_datetime(df['Ship Date'])

    print('Data loaded:', df.shape)

    make_histogram(df).write_html("test_histogram.html")
    make_box(df).write_html("test_box.html")
    make_violin(df).write_html("test_violin.html")
    make_line(df).write_html("test_line.html")
    make_area(df).write_html("test_area.html")

    print("Done! Open the .html files in your browser.")