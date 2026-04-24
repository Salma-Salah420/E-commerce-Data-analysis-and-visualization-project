# ============================================================
# comparison_charts.py
# Charts   : Column Chart, Bar Chart,
#            Stacked Column, Stacked Bar,
#            Clustered Column, Clustered Bar
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
# 1. COLUMN CHART — Total Sales by Category  (Week 1)
# ============================================================
def make_column_chart(df: pd.DataFrame) -> go.Figure:
    """
    Column Chart: Total Sales by Category.
    Categorical vs Numerical Bivariate Analysis.
    Answers: Which category reaches the maximum sales volume?
    Guideline: Vertical bars, sorted descending, y-axis starts at 0.
    """
    df_plot = df.copy()
    df_plot['Category'] = df_plot['Category'].str.title()

    sales_by_cat = (
        df_plot.groupby('Category')['Sales']
               .sum()
               .reset_index()
               .sort_values('Sales', ascending=False)
    )

    fig = px.bar(
        sales_by_cat,
        x='Category',
        y='Sales',
        title='Total Sales by Category',
        labels={'Sales': 'Total Sales (USD)', 'Category': 'Product Category'},
        color='Category',
        color_discrete_sequence=['#2196F3', '#FF5722', '#4CAF50'],
        text='Sales',
    )

    fig.update_traces(
        texttemplate='$%{text:,.0f}',
        textposition='outside',
    )

    fig.update_layout(
        xaxis_title='Product Category',
        yaxis_title='Total Sales (USD)',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=13),
        title_font_size=16,
        title_x=0.5,
        showlegend=False,
        yaxis=dict(rangemode='tozero'),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='#eeeeee', tickprefix='$', tickformat=',')

    return fig


# ============================================================
# 2. BAR CHART — Profit by Sub-Category  (Week 1)
# ============================================================
def make_bar_chart(df: pd.DataFrame) -> go.Figure:
    """
    Bar Chart: Profit by Sub-Category — Leaderboard style.
    Categorical vs Numerical Bivariate Analysis.
    Answers: Which sub-category is at the bottom of profit standings?
    Guideline: Horizontal bars, sorted ascending (worst at top),
               negative values shown in red.
    """
    df_plot = df.copy()
    df_plot['Sub-Category'] = df_plot['Sub-Category'].str.title()

    profit_by_sub = (
        df_plot.groupby('Sub-Category')['Profit']
               .sum()
               .reset_index()
               .sort_values('Profit', ascending=True)
    )

    colors = ['#FF5252' if v < 0 else '#2196F3' for v in profit_by_sub['Profit']]

    fig = go.Figure(go.Bar(
        x=profit_by_sub['Profit'],
        y=profit_by_sub['Sub-Category'],
        orientation='h',
        marker_color=colors,
        text=profit_by_sub['Profit'].apply(lambda v: f'${v:,.0f}'),
        textposition='outside',
    ))

    fig.add_vline(
        x=0,
        line_dash='dash',
        line_color='red',
        line_width=1.5,
        annotation_text='Break-even',
        annotation_position='top',
        annotation_font_color='red',
    )

    fig.update_layout(
        title='Profit by Sub-Category (Ranked)',
        xaxis_title='Total Profit (USD)',
        yaxis_title='Sub-Category',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        title_font_size=16,
        title_x=0.5,
        height=600,
    )
    fig.update_xaxes(showgrid=True, gridcolor='#eeeeee', tickprefix='$', tickformat=',')
    fig.update_yaxes(showgrid=False)

    return fig


# ============================================================
# 3. STACKED COLUMN CHART — Sales by Category & Region  (Week 2)
# ============================================================
def make_stacked_column(df: pd.DataFrame) -> go.Figure:
    """
    Stacked Column Chart: Sales by Category and Region.
    Shows composition — how each region contributes to category totals.
    Guideline: Stacked bars, y-axis starts at 0, legend for sub-groups.
    """
    df_plot = df.copy()
    df_plot['Category'] = df_plot['Category'].str.title()

    sales_pivot = (
        df_plot.groupby(['Category', 'Region'])['Sales']
               .sum()
               .reset_index()
    )

    fig = px.bar(
        sales_pivot,
        x='Category',
        y='Sales',
        color='Region',
        barmode='stack',
        title='Sales by Category and Region (Stacked)',
        labels={'Sales': 'Total Sales (USD)', 'Category': 'Product Category'},
        color_discrete_sequence=['#2196F3', '#FF5722', '#4CAF50', '#9C27B0'],
    )

    fig.update_layout(
        xaxis_title='Product Category',
        yaxis_title='Total Sales (USD)',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=13),
        title_font_size=16,
        title_x=0.5,
        yaxis=dict(rangemode='tozero'),
        legend=dict(title='Region'),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='#eeeeee', tickprefix='$', tickformat=',')

    return fig


# ============================================================
# 4. STACKED BAR CHART — Sales by Segment & Category  (Week 2)
# ============================================================
def make_stacked_bar(df: pd.DataFrame) -> go.Figure:
    """
    Stacked Bar Chart: Sales by Segment and Category.
    Shows composition — how each category contributes within each segment.
    Guideline: Horizontal stacked bars, sorted by total, legend for sub-groups.
    """
    df_plot = _add_segment_label(df)
    df_plot['Category'] = df_plot['Category'].str.title()

    sales_pivot = (
        df_plot.groupby(['Segment_Label', 'Category'])['Sales']
               .sum()
               .reset_index()
    )

    seg_order = (
        sales_pivot.groupby('Segment_Label')['Sales']
                   .sum()
                   .sort_values(ascending=True)
                   .index.tolist()
    )

    fig = px.bar(
        sales_pivot,
        x='Sales',
        y='Segment_Label',
        color='Category',
        barmode='stack',
        orientation='h',
        title='Sales by Customer Segment and Category (Stacked)',
        labels={'Sales': 'Total Sales (USD)', 'Segment_Label': 'Customer Segment'},
        color_discrete_map={
            'Furniture':       '#FF5722',
            'Office Supplies': '#4CAF50',
            'Technology':      '#2196F3',
        },
        category_orders={'Segment_Label': seg_order},
    )

    fig.update_layout(
        xaxis_title='Total Sales (USD)',
        yaxis_title='Customer Segment',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=13),
        title_font_size=16,
        title_x=0.5,
        xaxis=dict(rangemode='tozero'),
        legend=dict(title='Category'),
    )
    fig.update_xaxes(showgrid=True, gridcolor='#eeeeee', tickprefix='$', tickformat=',')
    fig.update_yaxes(showgrid=False)

    return fig


# ============================================================
# 5. CLUSTERED COLUMN CHART — Sales by Category & Year  (Week 2)
# ============================================================
def make_clustered_column(df: pd.DataFrame) -> go.Figure:
    """
    Clustered Column Chart: Sales by Category per Year.
    Side-by-side comparison — identify performance gap across years.
    Guideline: Grouped bars side-by-side, same baseline, legend for groups.
    """
    df_plot = df.copy()
    df_plot['Category'] = df_plot['Category'].str.title()
    df_plot['Order Date'] = pd.to_datetime(df_plot['Order Date'])
    df_plot['Year'] = df_plot['Order Date'].dt.year

    sales_pivot = (
        df_plot.groupby(['Year', 'Category'])['Sales']
               .sum()
               .reset_index()
    )
    sales_pivot['Year'] = sales_pivot['Year'].astype(str)

    fig = px.bar(
        sales_pivot,
        x='Year',
        y='Sales',
        color='Category',
        barmode='group',
        title='Sales by Category per Year (Clustered)',
        labels={'Sales': 'Total Sales (USD)', 'Year': 'Year'},
        color_discrete_map={
            'Furniture':       '#FF5722',
            'Office Supplies': '#4CAF50',
            'Technology':      '#2196F3',
        },
    )

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Total Sales (USD)',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=13),
        title_font_size=16,
        title_x=0.5,
        yaxis=dict(rangemode='tozero'),
        legend=dict(title='Category'),
        bargap=0.2,
        bargroupgap=0.05,
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='#eeeeee', tickprefix='$', tickformat=',')

    return fig


# ============================================================
# 6. CLUSTERED BAR CHART — Profit by Region & Category  (Week 2)
# ============================================================
def make_clustered_bar(df: pd.DataFrame) -> go.Figure:
    """
    Clustered Bar Chart: Profit by Region and Category.
    Side-by-side comparison — which region/category leads in profit?
    Guideline: Horizontal grouped bars, same baseline, legend for groups.
    """
    df_plot = df.copy()
    df_plot['Category'] = df_plot['Category'].str.title()

    profit_pivot = (
        df_plot.groupby(['Region', 'Category'])['Profit']
               .sum()
               .reset_index()
    )

    fig = px.bar(
        profit_pivot,
        x='Profit',
        y='Region',
        color='Category',
        barmode='group',
        orientation='h',
        title='Profit by Region and Category (Clustered)',
        labels={'Profit': 'Total Profit (USD)', 'Region': 'Region'},
        color_discrete_map={
            'Furniture':       '#FF5722',
            'Office Supplies': '#4CAF50',
            'Technology':      '#2196F3',
        },
    )

    fig.add_vline(
        x=0,
        line_dash='dash',
        line_color='red',
        line_width=1.5,
        annotation_text='Break-even',
        annotation_position='top',
        annotation_font_color='red',
    )

    fig.update_layout(
        xaxis_title='Total Profit (USD)',
        yaxis_title='Region',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=13),
        title_font_size=16,
        title_x=0.5,
        legend=dict(title='Category'),
        bargap=0.2,
        bargroupgap=0.05,
    )
    fig.update_xaxes(showgrid=True, gridcolor='#eeeeee', tickprefix='$', tickformat=',')
    fig.update_yaxes(showgrid=False)

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

    make_column_chart(df).write_html('test_column.html')
    make_bar_chart(df).write_html('test_bar.html')
    make_stacked_column(df).write_html('test_stacked_column.html')
    make_stacked_bar(df).write_html('test_stacked_bar.html')
    make_clustered_column(df).write_html('test_clustered_column.html')
    make_clustered_bar(df).write_html('test_clustered_bar.html')

    print("Done! Open the .html files in your browser.")