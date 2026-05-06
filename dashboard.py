import base64
import os
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import textwrap

app = Dash(__name__, external_stylesheets=[
    "https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;500;600;700&family=Barlow+Condensed:wght@400;600;700;800&display=swap"
])
app.title = "Mapeamento Salta Z – FUNASA"
server = app.server

LOGO_PATH = "FUNASA - LOGO.jpg"
logo_b64 = ""
if os.path.exists(LOGO_PATH):
    with open(LOGO_PATH, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode("utf-8")

def load_data():
    df = pd.read_excel("Salta_Z_planilha_tratada.xlsx")
    df.rename(columns={"LAT": "lat", "LON": "lon"}, inplace=True)
    df = df.dropna(subset=["lat", "lon"])
    for col in ["FUNCIONANDO", "SITUAÇÃO", "ESTADO", "COMUNIDADE", "MUNICIPIO", "Geolocalizador"]:
        if col in df.columns:
            df[col] = df[col].fillna("SEM INFORMAÇÃO").astype(str).str.upper().str.strip()
    return df

def quebrar_texto(df):
    df['SITUAÇÃO_FORMATADA'] = df['SITUAÇÃO'].apply(
        lambda x: "<br>".join(textwrap.wrap(str(x), width=40))
    )
    return df

df = quebrar_texto(load_data())

COLOR_MAP = {
    "SIM": "#1A5276",
    "NÃO": "#922B21",
    "SEM INFORMAÇÃO": "#626567",
}

CARD_BG = {
    "SIM": "linear-gradient(135deg, #1A5276 0%, #2E86C1 100%)",
    "NÃO": "linear-gradient(135deg, #922B21 0%, #C0392B 100%)",
    "SEM INFORMAÇÃO": "linear-gradient(135deg, #4D5656 0%, #717D7E 100%)",
}

FONT_MAIN = "Barlow, sans-serif"
FONT_DISPLAY = "Barlow Condensed, sans-serif"

def _label_style():
    return {"fontFamily": FONT_DISPLAY, "fontSize": "0.7rem"}

def _dropdown_style():
    return {"fontFamily": FONT_MAIN, "fontSize": "0.9rem"}

app.layout = html.Div([
    html.Div(style={"padding": "28px"}, children=[

        # 🔹 FILTROS
        html.Div(style={
            "display": "flex",
            "gap": "20px",
            "flexWrap": "wrap",
            "background": "#FFFFFF",
            "padding": "20px",
            "borderRadius": "12px",
        }, children=[

            html.Div([
                html.Label("ESTADO", style=_label_style()),
                dcc.Dropdown(
                    id="filter-estado",
                    options=[{"label": "Todos", "value": "TODOS"}] +
                            [{"label": e, "value": e} for e in sorted(df["ESTADO"].unique())],
                    value="TODOS",
                    clearable=False
                )
            ], style={"flex": "1"}),

            html.Div([
                html.Label("MUNICÍPIO", style=_label_style()),
                dcc.Dropdown(
                    id="filter-municipio",
                    options=[{"label": "Todos", "value": "TODOS"}],
                    value="TODOS",
                    clearable=False
                )
            ], style={"flex": "1"}),

            html.Div([
                html.Label("COMUNIDADE", style=_label_style()),
                dcc.Dropdown(
                    id="filter-comunidade",
                    options=[{"label": "Todos", "value": "TODOS"}],
                    value="TODOS",
                    clearable=False
                )
            ], style={"flex": "2"}),
        ]),

        html.Div(id="stat-cards"),
        dcc.Graph(id="mapa")
    ])
])


# 🔹 MUNICÍPIOS
@app.callback(
    Output("filter-municipio", "options"),
    Output("filter-municipio", "value"),
    Input("filter-estado", "value"),
)
def update_municipios(estado):
    df_t = df if estado == "TODOS" else df[df["ESTADO"] == estado]
    opts = [{"label": "Todos", "value": "TODOS"}] + \
           [{"label": m, "value": m} for m in sorted(df_t["MUNICIPIO"].unique())]
    return opts, "TODOS"


# 🔹 COMUNIDADES
@app.callback(
    Output("filter-comunidade", "options"),
    Output("filter-comunidade", "value"),
    Input("filter-estado", "value"),
    Input("filter-municipio", "value"),
)
def update_comunidades(estado, municipio):
    df_t = df.copy()

    if estado != "TODOS":
        df_t = df_t[df_t["ESTADO"] == estado]

    if municipio != "TODOS":
        df_t = df_t[df_t["MUNICIPIO"] == municipio]

    opts = [{"label": "Todos", "value": "TODOS"}] + \
           [{"label": c, "value": c} for c in sorted(df_t["COMUNIDADE"].unique())]

    return opts, "TODOS"


# 🔹 DASHBOARD
@app.callback(
    Output("mapa", "figure"),
    Output("stat-cards", "children"),
    Input("filter-estado", "value"),
    Input("filter-municipio", "value"),
    Input("filter-comunidade", "value"),
)
def update_dashboard(estado, municipio, comunidade):

    df_f = df.copy()

    if estado != "TODOS":
        df_f = df_f[df_f["ESTADO"] == estado]

    if municipio != "TODOS":
        df_f = df_f[df_f["MUNICIPIO"] == municipio]

    if comunidade != "TODOS":
        df_f = df_f[df_f["COMUNIDADE"] == comunidade]

    traces = []

    for func_val, group in df_f.groupby("FUNCIONANDO"):
        traces.append(go.Scattermapbox(
            lat=group["lat"],
            lon=group["lon"],
            mode="markers",
            name=func_val,
            marker=dict(size=9, color=COLOR_MAP.get(func_val))
        ))

    fig = go.Figure(traces)

    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            zoom=4,
            center=dict(lat=-14, lon=-52)
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig, []


if __name__ == "__main__":
    app.run(debug=True)
