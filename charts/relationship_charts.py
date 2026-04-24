# ============================================================
# relationship_charts.py
# Charts   : Scatter Chart, Bubble Chart
# ============================================================

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# 1. SCATTER CHART — Discount vs Profit  (Week 3)
# ============================================================
def make_scatter_discount_profit(df: pd.DataFrame) -> go.Figure:
    """
    Scatter Chart: Discount vs Profit.
    Numerical vs Numerical Bivariate Analysis.
    Answers: Is there a correlation between discount and profit?
    Guideline: Each dot = one transaction, color by category,
               reference line at profit=0, opacity to handle overplotting.
    """
    df_plot = df.copy()
    df_plot['Category'] = df_plot['Category'].str.title()

    fig = px.scatter(
        df_plot,
        x='Discount',
        y='Profit',
        color='Category',
        title='Discount vs Profit',
        labels={
            'Discount': 'Discount Rate',
            'Profit': 'Profit (USD)',
            'Category': 'Category',
        },
        color_discrete_map={
            'Furniture':       '#FF5722',
            'Office Supplies': '#4CAF50',
            'Technology':      '#2196F3',
        },
        opacity=0.5,
        hover_data=['Sales', 'Quantity'],
    )

    # Break-even reference line
    fig.add_hline(
        y=0,
        line_dash='dash',
        line_color='red',
        line_width=1.5,
        annotation_text='Break-even (Profit = 0)',
        annotation_position='top left',
        annotation_font_color='red',
    )

    fig.update_layout(
        xaxis_title='Discount Rate',
        yaxis_title='Profit (USD)',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=13),
        title_font_size=16,
        title_x=0.5,
        legend=dict(title='Category'),
    )
    fig.update_xaxes(
        showgrid=True, gridcolor='#eeeeee',
        tickformat='.0%',
    )
    fig.update_yaxes(showgrid=True, gridcolor='#eeeeee', tickprefix='$', tickformat=',')

    return fig


# ============================================================
# 2. SCATTER CHART — Sales vs Profit  (Week 3)
# ============================================================
def make_scatter_sales_profit(df: pd.DataFrame) -> go.Figure:
    """
    Scatter Chart: Sales vs Profit.
    Numerical vs Numerical Bivariate Analysis.
    Answers: Does higher sales always lead to higher profit?
    Guideline: Each dot = one transaction, color by category,
               zoomed to 99th percentile to reduce outlier distortion.
    """
    df_plot = df.copy()
    df_plot['Category'] = df_plot['Category'].str.title()

    x_max = df_plot['Sales'].quantile(0.99)

    fig = px.scatter(
        df_plot,
        x='Sales',
        y='Profit',
        color='Category',
        title='Sales vs Profit',
        labels={
            'Sales': 'Sales Amount (USD)',
            'Profit': 'Profit (USD)',
            'Category': 'Category',
        },
        color_discrete_map={
            'Furniture':       '#FF5722',
            'Office Supplies': '#4CAF50',
            'Technology':      '#2196F3',
        },
        opacity=0.5,
        hover_data=['Discount', 'Quantity'],
    )

    fig.add_hline(
        y=0,
        line_dash='dash',
        line_color='red',
        line_width=1.5,
        annotation_text='Break-even (Profit = 0)',
        annotation_position='top left',
        annotation_font_color='red',
    )

    fig.update_layout(
        xaxis_title='Sales Amount (USD)',
        yaxis_title='Profit (USD)',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=13),
        title_font_size=16,
        title_x=0.5,
        legend=dict(title='Category'),
        xaxis=dict(range=[0, x_max]),
    )
    fig.update_xaxes(showgrid=True, gridcolor='#eeeeee', tickprefix='$', tickformat=',')
    fig.update_yaxes(showgrid=True, gridcolor='#eeeeee', tickprefix='$', tickformat=',')

    return fig


# ============================================================
# 3. SCATTER CHART — Shipping Time vs Profit  (Week 3)
# ============================================================
def make_scatter_shipping_profit(df: pd.DataFrame) -> go.Figure:
    """
    Scatter Chart: Shipping Time vs Profit.
    Numerical vs Numerical Bivariate Analysis.
    Answers: Does shipping time impact profit?
    Guideline: Each dot = one transaction, color by ship mode,
               opacity to handle overplotting.
    """
    df_plot = df.copy()
    df_plot['Category'] = df_plot['Category'].str.title()

    fig = px.scatter(
        df_plot,
        x='Shipping Time',
        y='Profit',
        color='Category',
        title='Shipping Time vs Profit',
        labels={
            'Shipping Time': 'Shipping Time (Days)',
            'Profit': 'Profit (USD)',
            'Category': 'Category',
        },
        color_discrete_map={
            'Furniture':       '#FF5722',
            'Office Supplies': '#4CAF50',
            'Technology':      '#2196F3',
        },
        opacity=0.5,
        hover_data=['Sales', 'Discount'],
    )

    fig.add_hline(
        y=0,
        line_dash='dash',
        line_color='red',
        line_width=1.5,
        annotation_text='Break-even (Profit = 0)',
        annotation_position='top left',
        annotation_font_color='red',
    )

    fig.update_layout(
        xaxis_title='Shipping Time (Days)',
        yaxis_title='Profit (USD)',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=13),
        title_font_size=16,
        title_x=0.5,
        legend=dict(title='Category'),
    )
    fig.update_xaxes(showgrid=True, gridcolor='#eeeeee')
    fig.update_yaxes(showgrid=True, gridcolor='#eeeeee', tickprefix='$', tickformat=',')

    return fig


# ============================================================
# 4. BUBBLE CHART — Sales vs Profit (Bubble = Quantity)  (Week 4)
# ============================================================
def make_bubble_chart(df: pd.DataFrame) -> go.Figure:
    """
    Bubble Chart: Sales vs Profit, bubble size = Quantity.
    Numerical vs Numerical Multivariate Analysis.
    Answers: Do larger quantity orders amplify profit or loss?
    Guideline: x=Sales, y=Profit, size=Quantity, color=Category,
               opacity for overplotting, size_max to cap bubble size.
    """
    df_plot = df.copy()
    df_plot['Category'] = df_plot['Category'].str.title()

    x_max = df_plot['Sales'].quantile(0.99)

    fig = px.scatter(
        df_plot,
        x='Sales',
        y='Profit',
        size='Quantity',
        color='Category',
        title='Sales vs Profit (Bubble Size = Quantity)',
        labels={
            'Sales': 'Sales Amount (USD)',
            'Profit': 'Profit (USD)',
            'Quantity': 'Quantity',
            'Category': 'Category',
        },
        color_discrete_map={
            'Furniture':       '#FF5722',
            'Office Supplies': '#4CAF50',
            'Technology':      '#2196F3',
        },
        opacity=0.6,
        size_max=30,
        hover_data=['Discount', 'Quantity'],
    )

    fig.add_hline(
        y=0,
        line_dash='dash',
        line_color='red',
        line_width=1.5,
        annotation_text='Break-even (Profit = 0)',
        annotation_position='top left',
        annotation_font_color='red',
    )

    fig.update_layout(
        xaxis_title='Sales Amount (USD)',
        yaxis_title='Profit (USD)',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=13),
        title_font_size=16,
        title_x=0.5,
        legend=dict(title='Category'),
        xaxis=dict(range=[0, x_max]),
    )
    fig.update_xaxes(showgrid=True, gridcolor='#eeeeee', tickprefix='$', tickformat=',')
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

    make_scatter_discount_profit(df).write_html('test_scatter_discount.html')
    make_scatter_sales_profit(df).write_html('test_scatter_sales.html')
    make_scatter_shipping_profit(df).write_html('test_scatter_shipping.html')
    make_bubble_chart(df).write_html('test_bubble.html')

    print("Done! Open the .html files in your browser.")