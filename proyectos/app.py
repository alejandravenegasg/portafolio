import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd


# Cargar los datos
df_raw = pd.read_csv("proyectos/Arritmias.csv")

cols = df_raw.columns[1:-4]
df = df_raw.copy()

# Preprocesamiento de datos
for i in range(len(cols)):
    df[cols[i]] = df[cols[i]].str.replace(",", ".").astype(float)

# Inicializar la app con soporte multipágina
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Agregar el DataFrame a la aplicación como un atributo global
app.df = df

# Layout de la aplicación
app.layout = dbc.Container([
    html.H1("Marcadores Cardiovasculares entre Pacientes con y sin Arritmia", style={"text-align": "center"}),
    html.Hr(),
    dbc.Nav([
        dbc.NavLink("Inicio", href="/", active="exact"),
        dbc.NavLink("Tablas", href="/tabla", active="exact"),
        dbc.NavLink("Figuras Interactivas", href="/oficial", active="exact")
    ], pills=True),
    html.Div(dash.page_container)  # Aquí se renderizan las páginas
], fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True)
