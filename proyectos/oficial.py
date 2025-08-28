import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

dash.register_page(__name__)

# Cargar datos
df_raw = pd.read_csv("Arritmias.csv")
cols = df_raw.columns[1:-4]
df = df_raw.copy()

# Preprocesamiento de datos
for i in range(len(cols)):
    df[cols[i]] = df[cols[i]].str.replace(",", ".").astype(float)

# Preprocesamiento para t-SNE
df_numeric = df.select_dtypes(include=["number"]).dropna()
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_numeric)
tsne = TSNE(n_components=2, random_state=42)
df["TSNE-1"], df["TSNE-2"] = tsne.fit_transform(df_scaled).T
df["AV"] = df["AV"].map({0: "Normal", 1: "Arritmia"})

# Crear gráfico t-SNE
fig_tsne = px.scatter(
    df, x="TSNE-1", y="TSNE-2", color="AV",
    title="Visualización t-SNE de los Datos de Arritmias",
    labels={"TSNE-1": "Componente t-SNE 1", "TSNE-2": "Componente t-SNE 2"},
    color_discrete_map={"Arritmia": "red", "Normal": "green"},
    hover_data=["PACIENTES", "EDAD", "SEXO", "LVEF", "LV MASS (g)"]
)

# Layout de la página
layout = html.Div([
    html.H2("Análisis t-SNE de Arritmias"),
    html.P("En esta sección se puede explorar la distribución de los pacientes con arritmias en un espacio de menor dimensión luego de aplicar t-SNE. Se presentan información grafica para cuatro variables a modo de ejemplo y se eligen solo las de gramos"),
    
    dcc.Graph(
        id="tsne-graph",
        figure=fig_tsne,
        clear_on_unhover=False  # Permitir mantener el hover activo
    ),
    
    dcc.Store(id="selected-patient", storage_type="memory", data=df["PACIENTES"].iloc[0]),  # Almacena el paciente seleccionado por defecto
    
    html.Button("Mantener selección", id="keep-selection", n_clicks=0),
    
    html.Div(id="patient-info"),
    
    dcc.Graph(id="histogram-lv-mass"),
    dcc.Graph(id="histogram-bz-core"),
    dcc.Graph(id="histogram-bz"),
    dcc.Graph(id="histogram-core"),
])

# Callback para almacenar el paciente seleccionado al hacer clic
@dash.callback(
    Output("selected-patient", "data"),
    Input("tsne-graph", "hoverData"),
    prevent_initial_call=True
)
def store_hover_patient(hoverData):
    if hoverData is None:
        return df["PACIENTES"].iloc[0]  # Por defecto, selecciona el primer paciente
    return hoverData["points"][0]["customdata"][0]  # Usa el identificador único del paciente

# Callback para mostrar información del paciente seleccionado
@dash.callback(
    [Output("patient-info", "children"), Output("histogram-lv-mass", "figure"),
     Output("histogram-bz-core", "figure"), Output("histogram-bz", "figure"), Output("histogram-core", "figure")],
    [Input("selected-patient", "data"), Input("keep-selection", "n_clicks")]
)
def display_patient_info(patient_id, _):
    if patient_id not in df["PACIENTES"].values:
        patient_id = df["PACIENTES"].iloc[0]  # Asegurar que siempre haya un paciente seleccionado
    
    patient_data = df[df["PACIENTES"] == patient_id].iloc[0]
    lv_mass = patient_data.get('LV MASS (g)', None)
    bz_core = patient_data.get('BZ + CORE (g)', None)
    bz = patient_data.get('BZ (g)', None)
    core = patient_data.get('CORE (g)', None)
    
    # Crear histogramas con líneas verticales si el valor no es NaN
    fig2 = px.histogram(df, x='LV MASS (g)', color='AV', nbins=30, 
                        title="Distribución de la Masa del Ventrículo Izquierdo",
                        labels={"LV MASS (g)": "Masa del Ventrículo Izquierdo (g)"},
                        color_discrete_map={"Arritmia": "red", "Normal": "green"})
    if pd.notna(lv_mass):
        fig2.add_vline(x=lv_mass, line_dash="dash", line_color="black")
    
    fig3 = px.histogram(df, x='BZ + CORE (g)', color='AV', nbins=30, 
                        title="Distribución de BZ + CORE (g)",
                        labels={"BZ + CORE (g)": "BZ + CORE (g)"},
                        color_discrete_map={"Arritmia": "red", "Normal": "green"})
    if pd.notna(bz_core):
        fig3.add_vline(x=bz_core, line_dash="dash", line_color="black")
    
    fig4 = px.histogram(df, x='BZ (g)', color='AV', nbins=30, 
                        title="Distribución de BZ (g)",
                        labels={"BZ (g)": "BZ (g)"},
                        color_discrete_map={"Arritmia": "red", "Normal": "green"})
    if pd.notna(bz):
        fig4.add_vline(x=bz, line_dash="dash", line_color="black")
    
    fig5 = px.histogram(df, x='CORE (g)', color='AV', nbins=30, 
                        title="Distribución de CORE (g)",
                        labels={"CORE (g)": "CORE (g)"},
                        color_discrete_map={"Arritmia": "red", "Normal": "green"})
    if pd.notna(core):
        fig5.add_vline(x=core, line_dash="dash", line_color="black")
    
    return html.Div([
        html.H4("Información del Paciente"),
        html.P(f"Paciente: {patient_data['PACIENTES']}", style={'font-weight': 'bold'}),
    ]), fig2, fig3, fig4, fig5