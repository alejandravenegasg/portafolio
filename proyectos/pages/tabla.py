from dash import dcc, html, dash_table  # Correct import for dash_table
import pandas as pd
import dash
from dash.dash_table.Format import Group  # Correct import for Group formatting

# Registrar la página
dash.register_page(__name__, path='/tabla')  # Nueva pestaña

# Cargar datos
df_raw = pd.read_csv("Arritmias.csv")

# Preprocesamiento de datos
cols = df_raw.columns[1:-4]
df = df_raw.copy()

# Reemplazar comas por puntos en las columnas numéricas
for i in range(len(cols)):
    df[cols[i]] = df[cols[i]].str.replace(",", ".").astype(float)

# Layout de la nueva página
layout = html.Div([
    # Título de la página
    html.H1("Datos Completos de Pacientes con Arritmias", style={'textAlign': 'center', 'color': '#007ACC'}),
    
    # Descripción de la página
    html.Div([
        html.H3(""),
        html.P("En esta tabla se pueden aplicar filtros, buscar, y ordenar para explorar mejor la información. Recomiendo utilizar el signo '=' para las búsquedas")
    ], style={'textAlign': 'center', 'marginBottom': '30px'}),
    
    # Tabla con filtros interactivos
    html.Div([
        dash_table.DataTable(
            id='tabla-completa',
            columns=[
                {'name': col, 'id': col} for col in df.columns  # Creación dinámica de columnas
            ],
            data=df.to_dict('records'),  # Convertir el DataFrame a formato diccionario para Dash
            style_table={'height': '500px', 'overflowY': 'auto'},  # Estilo de la tabla con scroll
            style_cell={'textAlign': 'center', 'padding': '15px', 'border': '1px solid #ddd', 'fontSize': '14px'},
            style_header={'backgroundColor': '#00B0FF', 'fontWeight': 'bold', 'color': 'white'},
            style_data={'backgroundColor': 'rgb(248, 248, 248)', 'color': 'black'},
            
            # Estilo de filas alternadas
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)',  # Color de fondo para filas impares
                },
                {
                    'if': {'row_index': 'even'},
                    'backgroundColor': 'rgb(240, 240, 240)',  # Color de fondo para filas pares
                },
                {
                    'if': {
                        'state': 'active'  # Cambiar color al pasar el ratón sobre las filas
                    },
                    'backgroundColor': '#FFEB3B',  # Color cuando pasas el ratón
                    'color': 'black',
                }
            ],
            
            # Opciones de la tabla para la interacción
            filter_action='native',  # Habilitar el filtrado por las columnas
            sort_action='native',    # Permitir ordenar por las columnas
            page_size=10,            # Número de filas por página
            editable=True,           # Habilitar edición en la tabla
            row_deletable=True,      # Permitir eliminar filas (esto es opcional)
        )
    ], style={'marginBottom': '30px'}),
    
    # Descripción final
    html.Div([
        html.P("")
    ], style={'textAlign': 'center'})
])
