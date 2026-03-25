import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# 1. Ler o arquivo de estatísticas
import os
base_path = os.path.dirname(__file__) # Pega o caminho da pasta 'src'
file_path = os.path.join(base_path, '../data/ecommerce_estatistica.csv')
df = pd.read_csv(file_path)

# Inicializar o App Dash
app = dash.Dash(__name__)

# --- CRIAÇÃO DOS GRÁFICOS COM PLOTLY ---

# Histograma de Preços
fig_hist = px.histogram(df, x='Preço', nbins=30, title='Distribuição de Preços')

# Dispersão: Preço vs N_Avaliações
fig_scatter = px.scatter(df, x='Preço', y='N_Avaliações', title='Preço vs Número de Avaliações',
                         hover_data=['Título'])

# Mapa de Calor (Correlação)
df_corr = df[['Preço', 'N_Avaliações', 'Nota', 'Desconto']].corr()
fig_heat = px.imshow(df_corr, text_auto=True, title='Mapa de Calor de Correlação',
                     color_continuous_scale='RdBu_r')

# Barras: Média de Preço por Temporada
df_temp = df.groupby('Temporada')['Preço'].mean().reset_index()
fig_bar = px.bar(df_temp, x='Temporada', y='Preço', title='Preço Médio por Temporada')

# Pizza: Top 5 Marcas
fig_pie = px.pie(df, names='Marca', title='Participação das Marcas no Mercado')

# --- LAYOUT DA APLICAÇÃO ---

app.layout = html.Div(children=[
    html.H1(children='Dashboard de E-commerce - Análise de Dados'),
    html.P(children='Visualize os principais KPIs e tendências do marketplace.'),

    html.Div([
        dcc.Graph(figure=fig_hist),
        dcc.Graph(figure=fig_scatter)
    ], style={'display': 'flex'}),

    html.Div([
        dcc.Graph(figure=fig_bar),
        dcc.Graph(figure=fig_pie)
    ], style={'display': 'flex'}),

    html.Div([
        dcc.Graph(figure=fig_heat)
    ])
])

# Rodar a aplicação
if __name__ == '__main__':
    app.run(debug=True)