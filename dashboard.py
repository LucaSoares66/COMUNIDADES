import base64
import os
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# =========================
# 🔹 APP
# =========================
app = Dash(__name__, external_stylesheets=[
    "https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;500;600;700&family=Barlow+Condensed:wght@400;600;700;800&display=swap"
])
app.title = "Mapeamento Salta Z – FUNASA"
server = app.server

# =========================
# 🔹 LOGO (base64)
# =========================
LOGO_PATH = "FUNASA - LOGO.jpg"
logo_b64 = ""
if os.path.exists(LOGO_PATH):
    with open(LOGO_PATH, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode("utf-8")

# =========================
# 🔹 LOAD & CLEAN
# =========================
def load_data():
    df = pd.read_excel("Salta_Z_planilha_tratada.xlsx")
    df.rename(columns={"LAT": "lat", "LON": "lon"}, inplace=True)
    df = df.dropna(subset=["lat", "lon"])
    for col in ["FUNCIONANDO", "SITUAÇÃO", "ESTADO", "COMUNIDADE", "MUNICIPIO"]:
        if col in df.columns:
            df[col] = df[col].fillna("SEM INFORMAÇÃO").astype(str).str.upper().str.strip()
    return df

df = load_data()

# =========================
# 🔹 PALETTE
# =========================
COLOR_MAP = {
    "SIM":             "#1A5276",
    "NÃO":             "#922B21",
    "SEM INFORMAÇÃO":  "#626567",
}

CARD_BG = {
    "SIM":             "linear-gradient(135deg, #1A5276 0%, #2E86C1 100%)",
    "NÃO":             "linear-gradient(135deg, #922B21 0%, #C0392B 100%)",
    "SEM INFORMAÇÃO":  "linear-gradient(135deg, #4D5656 0%, #717D7E 100%)",
}

FONT_MAIN    = "Barlow, sans-serif"
FONT_DISPLAY = "Barlow Condensed, sans-serif"


# =========================
# 🔹 STYLE HELPERS
# =========================
def _label_style():
    return {
        "display": "block",
        "fontFamily": FONT_DISPLAY,
        "fontWeight": "600",
        "fontSize": "0.68rem",
        "letterSpacing": "0.14em",
        "textTransform": "uppercase",
        "color": "#7F8C8D",
        "marginBottom": "6px",
    }

def _dropdown_style():
    return {
        "fontFamily": FONT_MAIN,
        "fontSize": "0.88rem",
        "color": "#1C2833",
    }


# =========================
# 🔹 LAYOUT
# =========================
app.layout = html.Div(style={
    "background": "#F0F2F5",
    "minHeight": "100vh",
    "fontFamily": FONT_MAIN,
}, children=[

    # ── Header ────────────────────────────────────────────────────────────
    html.Div(style={
        "position": "relative",
        "overflow": "hidden",
        "background": "linear-gradient(135deg, #0B2545 0%, #13315C 40%, #1B4F72 100%)",
        "boxShadow": "0 4px 24px rgba(0,0,0,0.35)",
    }, children=[

        # Decorative background circles
        html.Div(style={
            "position": "absolute", "top": "-60px", "right": "-60px",
            "width": "260px", "height": "260px",
            "borderRadius": "50%",
            "background": "rgba(255,255,255,0.04)",
            "pointerEvents": "none",
        }),
        html.Div(style={
            "position": "absolute", "bottom": "-40px", "left": "32%",
            "width": "180px", "height": "180px",
            "borderRadius": "50%",
            "background": "rgba(255,255,255,0.03)",
            "pointerEvents": "none",
        }),

        # Frosted inner strip
        html.Div(style={
            "display": "flex",
            "alignItems": "center",
            "gap": "28px",
            "padding": "22px 40px",
            "backdropFilter": "blur(10px)",
            "WebkitBackdropFilter": "blur(10px)",
            "borderBottom": "1px solid rgba(255,255,255,0.08)",
        }, children=[

            # Logo
            html.Img(
                src=f"data:image/jpeg;base64,{logo_b64}" if logo_b64 else "",
                style={
                    "height": "64px",
                    "objectFit": "contain",
                    "filter": "drop-shadow(0 2px 8px rgba(0,0,0,0.4))",
                    "display": "block" if logo_b64 else "none",
                }
            ),

            # Vertical divider
            html.Div(style={
                "width": "1px",
                "height": "52px",
                "background": "rgba(255,255,255,0.2)",
                "flexShrink": "0",
                "display": "block" if logo_b64 else "none",
            }),

            # Title block
            html.Div([
                html.Div("FUNASA", style={
                    "fontFamily": FONT_DISPLAY,
                    "fontWeight": "700",
                    "fontSize": "0.68rem",
                    "letterSpacing": "0.22em",
                    "color": "rgba(255,255,255,0.5)",
                    "marginBottom": "4px",
                    "textTransform": "uppercase",
                }),
                html.H1("Mapeamento Salta Z", style={
                    "fontFamily": FONT_DISPLAY,
                    "fontWeight": "800",
                    "fontSize": "2rem",
                    "color": "#FFFFFF",
                    "margin": "0",
                    "letterSpacing": "-0.01em",
                    "lineHeight": "1.1",
                }),
                html.Div("Painel de Monitoramento de Comunidades", style={
                    "fontFamily": FONT_MAIN,
                    "fontWeight": "300",
                    "fontSize": "0.82rem",
                    "color": "rgba(255,255,255,0.55)",
                    "marginTop": "5px",
                    "letterSpacing": "0.04em",
                }),
            ]),

            html.Div(style={"flex": "1"}),

            # Total badge
            html.Div([
                html.Div(f"{len(df):,}", style={
                    "fontFamily": FONT_DISPLAY,
                    "fontWeight": "700",
                    "fontSize": "1.6rem",
                    "color": "#FFFFFF",
                    "lineHeight": "1",
                }),
                html.Div("registros totais", style={
                    "fontFamily": FONT_MAIN,
                    "fontSize": "0.68rem",
                    "color": "rgba(255,255,255,0.45)",
                    "letterSpacing": "0.06em",
                    "textTransform": "uppercase",
                }),
            ], style={
                "textAlign": "right",
                "background": "rgba(255,255,255,0.07)",
                "border": "1px solid rgba(255,255,255,0.13)",
                "borderRadius": "10px",
                "padding": "10px 18px",
            }),
        ]),
    ]),

    # ── Body ──────────────────────────────────────────────────────────────
    html.Div(style={"padding": "28px 36px"}, children=[

        # ── Filters ───────────────────────────────────────────────────────
        html.Div(style={
            "display": "flex",
            "gap": "20px",
            "flexWrap": "wrap",
            "background": "#FFFFFF",
            "borderRadius": "12px",
            "padding": "20px 24px",
            "marginBottom": "22px",
            "boxShadow": "0 1px 6px rgba(0,0,0,0.07)",
            "borderLeft": "4px solid #1A5276",
            "alignItems": "flex-end",
        }, children=[

            html.Div([
                html.Label("ESTADO", style=_label_style()),
                dcc.Dropdown(
                    id="filter-estado",
                    options=[{"label": "Todos os estados", "value": "TODOS"}] +
                            [{"label": e, "value": e} for e in sorted(df["ESTADO"].unique())],
                    value="TODOS",
                    clearable=False,
                    style=_dropdown_style(),
                )
            ], style={"flex": "1", "minWidth": "200px"}),

            html.Div([
                html.Label("COMUNIDADE", style=_label_style()),
                dcc.Dropdown(
                    id="filter-comunidade",
                    options=[{"label": "Todas as comunidades", "value": "TODOS"}],
                    value="TODOS",
                    clearable=False,
                    style=_dropdown_style(),
                )
            ], style={"flex": "2", "minWidth": "260px"}),

        ]),

        # ── Stat Cards ────────────────────────────────────────────────────
        html.Div(id="stat-cards", style={
            "display": "flex",
            "gap": "16px",
            "flexWrap": "wrap",
            "marginBottom": "22px",
        }),

        # ── Map Panel ─────────────────────────────────────────────────────
        html.Div(style={
            "background": "#FFFFFF",
            "borderRadius": "12px",
            "overflow": "hidden",
            "boxShadow": "0 2px 12px rgba(0,0,0,0.09)",
            "border": "1px solid #E0E4EA",
        }, children=[
            html.Div(style={
                "padding": "14px 22px",
                "borderBottom": "1px solid #EEF0F4",
                "display": "flex",
                "alignItems": "center",
                "gap": "10px",
            }, children=[
                html.Div(style={
                    "width": "4px", "height": "20px",
                    "background": "linear-gradient(180deg, #1A5276, #2E86C1)",
                    "borderRadius": "2px",
                }),
                html.Span("Distribuição Geográfica", style={
                    "fontFamily": FONT_DISPLAY,
                    "fontWeight": "600",
                    "fontSize": "1rem",
                    "color": "#1C2833",
                    "letterSpacing": "0.02em",
                }),
                html.Span(id="map-subtitle", style={
                    "fontFamily": FONT_MAIN,
                    "fontSize": "0.78rem",
                    "color": "#95A5A6",
                    "marginLeft": "6px",
                }),
            ]),
            dcc.Graph(
                id="mapa",
                config={
                    "scrollZoom": True,
                    "displayModeBar": True,
                    "displaylogo": False,
                    "modeBarButtonsToRemove": ["toImage"],
                },
                style={"height": "560px"},
            ),
        ]),

        # ── Footer ────────────────────────────────────────────────────────
        html.Div(style={
            "marginTop": "18px",
            "display": "flex",
            "justifyContent": "space-between",
            "alignItems": "center",
        }, children=[
            html.Div("Fundação Nacional de Saúde – FUNASA", style={
                "fontFamily": FONT_MAIN,
                "fontSize": "0.72rem",
                "color": "#AEB6BF",
                "letterSpacing": "0.05em",
                "textTransform": "uppercase",
            }),
            html.Div("Dados sujeitos à atualização", style={
                "fontFamily": FONT_MAIN,
                "fontSize": "0.72rem",
                "color": "#AEB6BF",
                "fontStyle": "italic",
            }),
        ]),
    ]),
])


# =========================
# 🔹 CALLBACKS
# =========================

@app.callback(
    Output("filter-comunidade", "options"),
    Output("filter-comunidade", "value"),
    Input("filter-estado", "value"),
)
def update_comunidades(estado):
    df_t = df if estado == "TODOS" else df[df["ESTADO"] == estado]
    opts = [{"label": "Todas as comunidades", "value": "TODOS"}] + \
           [{"label": c, "value": c} for c in sorted(df_t["COMUNIDADE"].unique())]
    return opts, "TODOS"


@app.callback(
    Output("mapa", "figure"),
    Output("stat-cards", "children"),
    Output("map-subtitle", "children"),
    Input("filter-estado", "value"),
    Input("filter-comunidade", "value"),
)
def update_dashboard(estado, comunidade):

    # ── Apply filters ───────────────────────────
    df_f = df.copy()
    if estado != "TODOS":
        df_f = df_f[df_f["ESTADO"] == estado]
    if comunidade != "TODOS":
        df_f = df_f[df_f["COMUNIDADE"] == comunidade]

    total = len(df_f)
    subtitle = f"— {total:,} ponto{'s' if total != 1 else ''} exibido{'s' if total != 1 else ''}"

    # ── Stat cards ──────────────────────────────
    contagem = df_f["FUNCIONANDO"].value_counts()
    cards = []
    order = ["SIM", "NÃO", "SEM INFORMAÇÃO"]
    labels = {
        "SIM": "Funcionando",
        "NÃO": "Não Funcionando",
        "SEM INFORMAÇÃO": "Sem Informação",
    }

    for key in order:
        val = int(contagem.get(key, 0))
        pct = f"{val / total * 100:.1f}%" if total > 0 else "—"

        cards.append(html.Div(style={
            "flex": "1",
            "minWidth": "160px",
            "background": CARD_BG.get(key, CARD_BG["SEM INFORMAÇÃO"]),
            "borderRadius": "12px",
            "padding": "22px 24px",
            "boxShadow": "0 4px 14px rgba(0,0,0,0.12)",
            "color": "#FFFFFF",
            "position": "relative",
            "overflow": "hidden",
        }, children=[
            html.Div(style={
                "position": "absolute", "top": "-20px", "right": "-20px",
                "width": "90px", "height": "90px",
                "borderRadius": "50%",
                "background": "rgba(255,255,255,0.08)",
                "pointerEvents": "none",
            }),
            html.Div(f"{val:,}", style={
                "fontFamily": FONT_DISPLAY,
                "fontWeight": "800",
                "fontSize": "2.8rem",
                "lineHeight": "1",
                "letterSpacing": "-0.02em",
            }),
            html.Div(labels.get(key, key), style={
                "fontFamily": FONT_MAIN,
                "fontWeight": "600",
                "fontSize": "0.78rem",
                "textTransform": "uppercase",
                "letterSpacing": "0.1em",
                "marginTop": "6px",
                "opacity": "0.85",
            }),
            html.Div(pct + " do total filtrado", style={
                "fontFamily": FONT_MAIN,
                "fontWeight": "300",
                "fontSize": "0.73rem",
                "opacity": "0.6",
                "marginTop": "4px",
            }),
        ]))

    # ── Map traces ──────────────────────────────
    traces = []
    for func_val, group in df_f.groupby("FUNCIONANDO"):
        color = COLOR_MAP.get(func_val, "#626567")
        customdata = list(zip(
            group["COMUNIDADE"],
            group["MUNICIPIO"],
            group["ESTADO"],
            group["SITUAÇÃO"],
            group["FUNCIONANDO"],
        ))
        traces.append(go.Scattermap(
            lat=group["lat"],
            lon=group["lon"],
            mode="markers",
            name=func_val,
            marker=dict(size=9, color=color, opacity=0.85, allowoverlap=True),
            customdata=customdata,
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Município: %{customdata[1]}<br>"
                "Estado: %{customdata[2]}<br>"
                "Situação: %{customdata[3]}<br>"
                "Funcionando: %{customdata[4]}"
                "<extra></extra>"
            ),
        ))

    # ── Zoom ────────────────────────────────────
    if total > 0:
        lat_c = df_f["lat"].mean()
        lon_c = df_f["lon"].mean()
        span = max(
            df_f["lat"].max() - df_f["lat"].min(),
            df_f["lon"].max() - df_f["lon"].min(),
        )
        zoom = max(2, min(12, 7 - (span / 5)))
    else:
        lat_c, lon_c, zoom = -14, -52, 4

    fig = go.Figure(traces)
    fig.update_layout(
        map=dict(
            style="carto-positron",
            center=dict(lat=lat_c, lon=lon_c),
            zoom=zoom,
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(
            title=dict(
                text="<b>Funcionamento</b>",
                font=dict(family=FONT_DISPLAY, size=12, color="#1C2833"),
            ),
            font=dict(family=FONT_MAIN, size=12, color="#1C2833"),
            bgcolor="rgba(255,255,255,0.94)",
            bordercolor="#D5D8DC",
            borderwidth=1,
            x=0.01, y=0.99,
            xanchor="left", yanchor="top",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT_MAIN),
        uirevision="map-state",
    )

    return fig, cards, subtitle


# =========================
# 🔹 RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
