#!/usr/bin/env python3
"""
Dash приложение для мониторинга WB, МойСклад и оптовой продажи
"""

import dash
from dash import dcc, html, callback, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
from datetime import datetime, timedelta
import os

# Инициализируем Dash приложение
app = dash.Dash(__name__)
app.title = "Aidar Business Dashboard"

# Путь к данным
DATA_DIR = "/root/frost-ai/users/583297536/dashboard/data"
os.makedirs(DATA_DIR, exist_ok=True)

def load_data(filename):
    """Загружает JSON данные"""
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def load_dataframe(filename):
    """Загружает CSV данные"""
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    return pd.DataFrame()

def get_wb_data():
    """Получает актуальные данные WB из JSON файла"""
    wb_data = load_data('wb_report.json')
    if wb_data and 'metrics' in wb_data:
        return wb_data['metrics']
    # Если файла нет, возвращаем тестовые данные
    return {
        'total_revenue': 13137621,
        'total_quantity': 4183,
        'average_check': 3140,
        'unique_products': 34,
    }

# CSS стили
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }
            .container {
                max-width: 1400px;
                margin: 0 auto;
            }
            .header {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .header h1 {
                margin: 0;
                color: #333;
                font-size: 32px;
            }
            .header p {
                margin: 5px 0 0 0;
                color: #666;
                font-size: 14px;
            }
            .card {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .metric-box {
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 8px;
                margin: 10px;
                min-width: 200px;
                text-align: center;
            }
            .metric-label {
                font-size: 12px;
                opacity: 0.9;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            .metric-value {
                font-size: 28px;
                font-weight: bold;
                margin: 10px 0;
            }
            .metric-unit {
                font-size: 12px;
                opacity: 0.8;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer></footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </body>
</html>
'''

# Макет приложения
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1("📊 Aidar Business Dashboard", style={'margin': 0}),
            html.P(f"Последнее обновление: {datetime.now().strftime('%d.%m.%Y %H:%M')}", 
                   style={'color': '#666', 'margin': '5px 0 0 0'}),
        ], className="header"),
        
        # ВКЛАДКИ
        dcc.Tabs(id="tabs", value="tab-wb", children=[
            
            # ТАБ 1: WB ФИНАНСЫ
            dcc.Tab(label="📈 WB Финансы", value="tab-wb", children=[
                html.Div([
                    # Метрики
                    html.Div([
                        html.Div(className="metric-box", children=[
                            html.Div("Выручка 60 дней", className="metric-label"),
                            html.Div("13.14M", className="metric-value"),
                            html.Div("₽", className="metric-unit"),
                        ]),
                        html.Div(className="metric-box", children=[
                            html.Div("Средний месяц", className="metric-label"),
                            html.Div("2.19M", className="metric-value"),
                            html.Div("₽", className="metric-unit"),
                        ]),
                        html.Div(className="metric-box", children=[
                            html.Div("Маржа", className="metric-label"),
                            html.Div("49%", className="metric-value"),
                            html.Div("от выручки", className="metric-unit"),
                        ]),
                        html.Div(className="metric-box", children=[
                            html.Div("Заказов", className="metric-label"),
                            html.Div("4,183", className="metric-value"),
                            html.Div("шт", className="metric-unit"),
                        ]),
                    ], style={'text-align': 'center', 'margin': '20px 0'}),
                    
                    # Графики
                    html.Div(className="card", children=[
                        html.H3("📊 Выручка по дням (последние 30 дней)"),
                        dcc.Graph(id="wb-daily-revenue-graph"),
                    ]),
                    
                    html.Div([
                        html.Div(className="card", style={'width': '48%', 'display': 'inline-block', 'margin-right': '2%'}, children=[
                            html.H3("🏆 Топ-5 товаров по выручке"),
                            dcc.Graph(id="wb-top-products-graph"),
                        ]),
                        html.Div(className="card", style={'width': '48%', 'display': 'inline-block'}, children=[
                            html.H3("💹 Маржинальность топ товаров"),
                            dcc.Graph(id="wb-margin-graph"),
                        ]),
                    ]),
                    
                    html.Div(className="card", children=[
                        html.H3("📋 Финансовая сводка"),
                        html.Table([
                            html.Tr([
                                html.Td("Выручка:", style={'fontWeight': 'bold'}),
                                html.Td("13,137,621₽", style={'textAlign': 'right', 'color': '#667eea'}),
                            ]),
                            html.Tr([
                                html.Td("Себестоимость:"),
                                html.Td("2,407,406₽", style={'textAlign': 'right'}),
                            ]),
                            html.Tr([
                                html.Td("Комиссия WB:"),
                                html.Td("4,293,538₽", style={'textAlign': 'right'}),
                            ]),
                            html.Tr([
                                html.Td("Прибыль:", style={'fontWeight': 'bold', 'borderTop': '2px solid #ddd', 'paddingTop': '10px'}),
                                html.Td("6,436,677₽", style={'textAlign': 'right', 'fontWeight': 'bold', 'color': '#28a745', 'borderTop': '2px solid #ddd', 'paddingTop': '10px'}),
                            ]),
                        ], style={'width': '100%', 'borderCollapse': 'collapse'}),
                    ]),
                ], className="container"),
            ]),
            
            # ТАБ 2: ОСТАТКИ МОЫСКЛАД
            dcc.Tab(label="📦 Остатки (МойСклад)", value="tab-stock", children=[
                html.Div([
                    html.Div(className="card", children=[
                        html.H3("🏢 Остатки по складам"),
                        html.Div(id="warehouse-summary"),
                    ]),
                    
                    html.Div(className="card", children=[
                        html.H3("📊 Распределение остатков"),
                        dcc.Graph(id="stock-distribution-graph"),
                    ]),
                    
                    html.Div(className="card", children=[
                        html.H3("📋 Топ товаров по остаткам"),
                        dcc.Graph(id="top-stock-graph"),
                    ]),
                ], className="container"),
            ]),
            
            # ТАБ 3: ОПТОВАЯ ПРОДАЖА
            dcc.Tab(label="💼 Оптовая продажа", value="tab-wholesale", children=[
                html.Div([
                    html.Div(className="card", children=[
                        html.H3("🎯 Целевая модель оптовой продажи"),
                        html.Table([
                            html.Tr([
                                html.Td("Период", style={'fontWeight': 'bold', 'borderBottom': '2px solid #ddd', 'padding': '10px'}),
                                html.Td("WB", style={'fontWeight': 'bold', 'borderBottom': '2px solid #ddd', 'padding': '10px'}),
                                html.Td("Оптовая", style={'fontWeight': 'bold', 'borderBottom': '2px solid #ddd', 'padding': '10px'}),
                                html.Td("ВСЕГО", style={'fontWeight': 'bold', 'borderBottom': '2px solid #ddd', 'padding': '10px', 'color': '#667eea'}),
                            ]),
                            html.Tr([
                                html.Td("Фев-Апр (сезон опт)"),
                                html.Td("3.5M₽"),
                                html.Td("—"),
                                html.Td("3.5M₽"),
                            ]),
                            html.Tr([
                                html.Td("Май-Июл (низкий сезон)"),
                                html.Td("3.5M₽"),
                                html.Td("1.5M₽"),
                                html.Td("5.0M₽"),
                            ]),
                            html.Tr([
                                html.Td("Авг-Фев (сезон LED)"),
                                html.Td("3.5M₽"),
                                html.Td("2-3M₽"),
                                html.Td("5.5-6.5M₽", style={'color': '#28a745', 'fontWeight': 'bold'}),
                            ]),
                        ], style={'width': '100%', 'borderCollapse': 'collapse'}),
                    ]),
                    
                    html.Div(className="card", children=[
                        html.H3("📊 Оптовые цены (ТОП-10 товаров)"),
                        dcc.Graph(id="wholesale-prices-graph"),
                    ]),
                    
                    html.Div(className="card", children=[
                        html.H3("💰 Бюджет май (1,000,000₽)"),
                        html.Div([
                            html.Div(className="metric-box", children=[
                                html.Div("LED-лампы (70%)", className="metric-label"),
                                html.Div("1,743", className="metric-value"),
                                html.Div("шт", className="metric-unit"),
                            ]),
                            html.Div(className="metric-box", children=[
                                html.Div("Бустеры (30%)", className="metric-label"),
                                html.Div("143", className="metric-value"),
                                html.Div("шт", className="metric-unit"),
                            ]),
                            html.Div(className="metric-box", children=[
                                html.Div("Ожидаемая прибыль", className="metric-label"),
                                html.Div("~900K", className="metric-value"),
                                html.Div("₽", className="metric-unit"),
                            ]),
                            html.Div(className="metric-box", children=[
                                html.Div("ROI", className="metric-label"),
                                html.Div("90%", className="metric-value"),
                                html.Div("за цикл", className="metric-unit"),
                            ]),
                        ], style={'text-align': 'center', 'margin': '20px 0'}),
                    ]),
                ], className="container"),
            ]),
            
            # ТАБ 4: АНАЛИТИКА
            dcc.Tab(label="📊 Аналитика", value="tab-analytics", children=[
                html.Div([
                    html.Div(className="card", children=[
                        html.H3("📈 Тренды"),
                        dcc.Graph(id="trends-graph"),
                    ]),
                    
                    html.Div(className="card", children=[
                        html.H3("🎯 Прогноз (следующие 30 дней)"),
                        dcc.Graph(id="forecast-graph"),
                    ]),
                    
                    html.Div(className="card", children=[
                        html.H3("⚠️ Ключевые метрики"),
                        html.Div([
                            html.Div(className="metric-box", children=[
                                html.Div("Концентрация ТОП-3", className="metric-label"),
                                html.Div("67%", className="metric-value"),
                                html.Div("от выручки", className="metric-unit"),
                            ]),
                            html.Div(className="metric-box", children=[
                                html.Div("Среднее время оборота", className="metric-label"),
                                html.Div("14", className="metric-value"),
                                html.Div("дней", className="metric-unit"),
                            ]),
                        ], style={'text-align': 'center', 'margin': '20px 0'}),
                    ]),
                ], className="container"),
            ]),
        ]),
    ], style={'marginTop': '20px'}),
], style={'backgroundColor': 'transparent'})

# Коллбеки для графиков (заглушки)
@callback(
    Output("wb-daily-revenue-graph", "figure"),
    Input("tabs", "value")
)
def update_daily_revenue(tab):
    wb_data = load_data('wb_report.json')
    
    if wb_data and 'daily_data' in wb_data and wb_data['daily_data']:
        # Используем реальные данные
        daily = pd.DataFrame(wb_data['daily_data'])
        daily['date'] = pd.to_datetime(daily['date'])
        daily = daily.sort_values('date')
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=daily['date'], y=daily['revenue'],
            mode='lines+markers',
            name='Выручка',
            line=dict(color='#667eea', width=3),
            fill='tozeroy',
            hovertemplate='<b>%{x|%d.%m}</b><br>Выручка: %{y:,.0f}₽<extra></extra>',
        ))
    else:
        # Тестовые данные если нет реальных
        dates = pd.date_range(start='2026-02-20', periods=30, freq='D')
        revenues = [55000 + i*2000 + (i%7)*5000 for i in range(30)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, y=revenues,
            mode='lines+markers',
            name='Выручка',
            line=dict(color='#667eea', width=3),
            fill='tozeroy',
        ))
    
    fig.update_layout(
        hovermode='x unified',
        height=400,
        template='plotly_white',
        xaxis_title='Дата',
        yaxis_title='Выручка (₽)',
    )
    return fig

@callback(
    Output("wb-top-products-graph", "figure"),
    Input("tabs", "value")
)
def update_top_products(tab):
    products = ['BYSTER', 'F15_H1', 'Полка прозрачная', 'F15_H4', 'F15_H7']
    revenues = [4949670, 1977140, 1823598, 743717, 712863]
    
    fig = px.bar(
        x=revenues, y=products,
        orientation='h',
        labels={'x': 'Выручка (₽)', 'y': 'Товар'},
        color=revenues,
        color_continuous_scale='Blues',
    )
    fig.update_layout(height=400, template='plotly_white', showlegend=False)
    return fig

@callback(
    Output("wb-margin-graph", "figure"),
    Input("tabs", "value")
)
def update_margin(tab):
    products = ['Полка прозрачная', 'BYSTER', 'F15_H7', 'F15_H1', 'F15_H4']
    margins = [60.5, 43.3, 52.3, 50.4, 43.6]
    
    fig = px.bar(
        x=margins, y=products,
        orientation='h',
        labels={'x': 'Маржа (%)', 'y': 'Товар'},
        color=margins,
        color_continuous_scale='Greens',
    )
    fig.update_layout(height=400, template='plotly_white', showlegend=False)
    return fig

@callback(
    Output("stock-distribution-graph", "figure"),
    Input("tabs", "value")
)
def update_stock(tab):
    warehouses = ['Основной', 'ВБ (Запас)', 'ОЗОН', 'КЕ (Запас)', 'Прочие']
    counts = [450, 280, 120, 90, 60]
    
    fig = px.pie(values=counts, names=warehouses, hole=0.3)
    fig.update_layout(height=400)
    return fig

@callback(
    Output("top-stock-graph", "figure"),
    Input("tabs", "value")
)
def update_top_stock(tab):
    products = ['F15_H1', 'BYSTER', 'F15_H4', 'S6_H7', 'Полка прозрачная']
    stocks = [280, 220, 145, 120, 95]
    
    fig = px.bar(x=products, y=stocks, labels={'y': 'Количество (шт)'})
    fig.update_layout(height=400, template='plotly_white')
    return fig

@callback(
    Output("wholesale-prices-graph", "figure"),
    Input("tabs", "value")
)
def update_wholesale(tab):
    products = ['BYSTER', 'F15_H4', 'F15_H1', 'F15_H7', 'S6_H11']
    wholesale = [3780, 1260, 603, 900, 425]
    retail = [8490, 2871, 2299, 2307, 1896]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=products, y=retail, name='Розница WB', marker_color='#764ba2'))
    fig.add_trace(go.Bar(x=products, y=wholesale, name='Оптовая цена', marker_color='#667eea'))
    fig.update_layout(barmode='group', height=400, template='plotly_white')
    return fig

@callback(
    Output("trends-graph", "figure"),
    Input("tabs", "value")
)
def update_trends(tab):
    dates = pd.date_range(start='2026-01-22', periods=60, freq='D')
    revenue = [50000 + i*1500 + (i%14)*10000 for i in range(60)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=revenue,
        mode='lines',
        name='Выручка (тренд)',
        line=dict(color='#667eea', width=3),
    ))
    fig.update_layout(height=400, template='plotly_white', hovermode='x unified')
    return fig

@callback(
    Output("forecast-graph", "figure"),
    Input("tabs", "value")
)
def update_forecast(tab):
    dates = pd.date_range(start='2026-03-24', periods=30, freq='D')
    forecast = [70000 + i*2000 for i in range(30)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=forecast,
        mode='lines',
        name='Прогноз',
        line=dict(color='#28a745', width=3, dash='dash'),
        fill='tozeroy',
    ))
    fig.update_layout(height=400, template='plotly_white')
    return fig

@app.callback(
    Output("warehouse-summary", "children"),
    Input("tabs", "value")
)
def update_warehouse_summary(tab):
    return html.Table([
        html.Tr([
            html.Td("Основной склад:", style={'fontWeight': 'bold'}),
            html.Td("450 шт", style={'textAlign': 'right'}),
        ]),
        html.Tr([
            html.Td("ВБ (Запас):"),
            html.Td("280 шт", style={'textAlign': 'right'}),
        ]),
        html.Tr([
            html.Td("ОЗОН (Запас):"),
            html.Td("120 шт", style={'textAlign': 'right'}),
        ]),
        html.Tr([
            html.Td("КЕ (Запас):"),
            html.Td("90 шт", style={'textAlign': 'right'}),
        ]),
        html.Tr([
            html.Td("Бракованные товары:", style={'borderTop': '2px solid #ddd', 'paddingTop': '10px'}),
            html.Td("12 шт", style={'textAlign': 'right', 'borderTop': '2px solid #ddd', 'paddingTop': '10px'}),
        ]),
        html.Tr([
            html.Td("ВСЕГО:", style={'fontWeight': 'bold'}),
            html.Td("952 шт", style={'textAlign': 'right', 'fontWeight': 'bold', 'color': '#667eea'}),
        ]),
    ], style={'width': '100%', 'borderCollapse': 'collapse'})

# Экспортируем server для Gunicorn/облачных платформ
server = app.server

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8050)
