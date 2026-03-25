import pandas as pd
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import os

# 1. Caminho dinâmico para o arquivo
base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, '../data/ecommerce_estatistica.csv')
df = pd.read_csv(file_path)

# 2. Inicializar o App com um tema moderno
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# --- PROCESSAMENTO DE DADOS (TOP 5 MARCAS) ---
top_marcas = df['Marca'].value_counts().nlargest(5).reset_index()
top_marcas.columns = ['Marca', 'Contagem']

# --- CONFIGURAÇÃO VISUAL DOS GRÁFICOS ---
# Altura 250 para garantir que tudo apareça 
GRAPH_CONFIG = {'height': 250, 'margin': {'t': 40, 'b': 30, 'l': 30, 'r': 30}}

fig_hist = px.histogram(df, x='Preço', nbins=20, title='Distribuição de Preços', 
                        color_discrete_sequence=['#636EFA'])
fig_hist.update_layout(GRAPH_CONFIG, template='plotly_white')

fig_scatter = px.scatter(df, x='Preço', y='N_Avaliações', title='Preço vs Popularidade', 
                         opacity=0.6, color_discrete_sequence=['#EF553B'])
fig_scatter.update_layout(GRAPH_CONFIG, template='plotly_white')

df_temp = df.groupby('Temporada')['Preço'].mean().reset_index()
fig_bar = px.bar(df_temp, x='Temporada', y='Preço', color='Temporada', 
                 title='Média por Temporada', color_discrete_sequence=px.colors.qualitative.Safe)
fig_bar.update_layout(GRAPH_CONFIG, template='plotly_white', showlegend=False)

fig_pie = px.pie(top_marcas, values='Contagem', names='Marca', 
                 title='Top 5 Marcas', hole=.4,
                 color_discrete_sequence=px.colors.qualitative.Pastel)
fig_pie.update_layout(GRAPH_CONFIG, template='plotly_white')
fig_pie.update_traces(textinfo='percent+label')

# --- LAYOUT FINAL ---
app.layout = dbc.Container(fluid=True, style={'backgroundColor': '#f4f7f6', 'minHeight': '100vh'}, children=[
    
    dbc.Row([
        dbc.Col(html.H2("Dashboard E-commerce Insights", className="text-center my-3", 
                        style={'color': '#2c3e50', 'fontWeight': 'bold'}), width=12)
    ]),

    # Primeira Linha 
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(figure=fig_hist, config={'displayModeBar': False})]), className="shadow-sm"), width=6),
        dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(figure=fig_scatter, config={'displayModeBar': False})]), className="shadow-sm"), width=6),
    ], className="mb-4 g-3"),

    # Segunda Linha
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(figure=fig_bar, config={'displayModeBar': False})]), className="shadow-sm"), width=6),
        dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(figure=fig_pie, config={'displayModeBar': False})]), className="shadow-sm"), width=6),
    ], className="g-3"),

    html.Footer("Análise de Dados | Nicolly Gabriele", className="text-center mt-4 pb-3", style={'color': '#95a5a6'})
])

if __name__ == '__main__':
    app.run(debug=True)