from dash import dcc, html, dash_table  # Correct import for dash_table
import pandas as pd
import plotly.express as px
from dash.dash_table.Format import Group  # Correct import for Group formatting
import dash

# Registrar la página
dash.register_page(__name__, path='/')

# Cargar datos
df_raw = pd.read_csv("Arritmias.csv")

# Preprocesamiento de datos
cols = df_raw.columns[1:-4]
df = df_raw.copy()

# Reemplazar comas por puntos en las columnas numéricas
for i in range(len(cols)):
    df[cols[i]] = df[cols[i]].str.replace(",", ".").astype(float)

# Crear tabla de distribución de Sexo vs Arritmia
sexo_arritmia = df.groupby(['SEXO', 'AV']).size().reset_index(name='Cantidad')

# Reemplazar valores de AV para mostrar "Arritmia" o "Normal"
sexo_arritmia['AV'] = sexo_arritmia['AV'].map({0: 'Normal', 1: 'Arritmia'})

# Layout de la página
layout = html.Div([
    # Título principal
    html.H1("Estadistica descriptivos de Datos de Pacientes con Arritmias", style={'textAlign': 'center'}),
    
    # Descripción de la página
  
    html.Div([
        html.P("Los datos reflejan un grupo relativamente homogéneo en términos de edad, con una ligera tendencia a que los pacientes con arritmia sean mayores que aquellos sin ella. Ademas, se debe considerar que la cantidad de pacientes con arritmia es relativamente baja en comparacion con el grupo sin arritmia, lo que puede influir en la interpretacion de los resultados."),
        html.P("En la tabla presentada, se observa que no existen registros de pacientes con arritmia cuyo sexo sea igual a 2. Esto debe tenerse en cuenta al interpretar las figuras y tablas en las siguientes pestanas.")
    ], style={'textAlign': 'center', 'marginBottom': '30px'}),

   html.Div([
    html.Div([
        html.H4("Estadísticas Generales"),
        html.P(f"Cantidad Total de Pacientes: {len(df)}", style={'fontSize': '18px'}),
        html.P(f"Porcentaje de Pacientes con Arritmia: {df['AV'].value_counts(normalize=True)[1] * 100:.2f}%", style={'fontSize': '18px'}),
        html.P(f"Porcentaje de Pacientes sin Arritmia: {df['AV'].value_counts(normalize=True)[0] * 100:.2f}%", style={'fontSize': '18px'}),
        html.P(f"Edad Promedio de los Pacientes: {df['EDAD'].mean():.2f} años", style={'fontSize': '18px'}),
        html.P(f"Edad Promedio de Pacientes con Arritmia: {df[df['AV'] == 1]['EDAD'].mean():.2f} años", style={'fontSize': '18px'}),
        html.P(f"Edad Promedio de Pacientes sin Arritmia: {df[df['AV'] == 0]['EDAD'].mean():.2f} años", style={'fontSize': '18px'})
    ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '5%'}),
    
    html.Div([
        html.H4("Distribución de Sexo"),
        dcc.Graph(figure=px.pie(df, names='SEXO', title="Distribución de Sexo", 
                                color_discrete_map={"M": "blue", "F": "pink"}), style={'marginTop': '20px'})
    ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '30px'}),

    # Tabla simple de Sexo vs Arritmia
    html.Div([
        html.H4("Distribución de Sexo y Arritmia"),
       dash_table.DataTable(
            id='sexo-arritmia-table',
            columns=[
                {'name': 'Sexo', 'id': 'SEXO'},
                {'name': 'Arritmia', 'id': 'AV'},
                {'name': 'Cantidad', 'id': 'Cantidad'}
            ],
            data=sexo_arritmia.to_dict('records'),
            style_table={'height': '350px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'center', 'padding': '10px', 'border': '1px solid #ddd'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
            style_data={'backgroundColor': 'rgb(248, 248, 248)'}
        )
    ], style={'marginBottom': '30px'}),
    
    html.Div([
        html.P(" ")
    ], style={'textAlign': 'center'})
])
