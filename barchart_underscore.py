import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# CSV-bestand inlezen
df = pd.read_csv("Animal_Shelter_Animals.csv")

# Datumkolom omzetten naar datetime
df["intakedate"] = pd.to_datetime(df["intakedate"])

# Jaar uit de datum halen
df["year"] = df["intakedate"].dt.year

# Groeperen per jaar en categorie en het aantal tellen
grouped = df.groupby(["year", "speciesname"]).size().reset_index(name="count")

# Tabel herstructureren
table = grouped.pivot(index="year", columns="speciesname", values="count")

# Ontbrekende waarden opvullen met 0
table = table.fillna(0)

# Data opnieuw in lange vorm zetten voor Plotly
plotly_df = table.reset_index().melt(
    id_vars="year",
    var_name="speciesname",
    value_name="count"
)

# Alleen top 10 per jaar behouden
plotly_df = (
    plotly_df.sort_values(["year", "count"], ascending=[True, False])
    .groupby("year")
    .head(10)
)

# Dash app maken
app = Dash(__name__)
server = app.server

# Layout van de website
app.layout = html.Div([
    html.H1("Animal Shelter Bar Chart Race"),

    dcc.Graph(id="bar-chart-race"),

    dcc.Interval(
        id="interval-component",
        interval=1000,
        n_intervals=0
    )
])

# Beschikbare jaren
years = sorted(plotly_df["year"].unique())

# Callback voor animatie
@app.callback(
    Output("bar-chart-race", "figure"),
    Input("interval-component", "n_intervals")
)
def update_graph(n):

    # Jaar kiezen
    year = years[n % len(years)]

    # Data van dat jaar
    current_df = plotly_df[plotly_df["year"] == year]

    # Sorteren zodat grootste bovenaan staat
    current_df = current_df.sort_values("count", ascending=True)

    # Grafiek maken
    fig = px.bar(
        current_df,
        x="count",
        y="speciesname",
        orientation="h",
        text="count",
        title=f"Top 10 diersoorten in {year}"
    )

    # Layout aanpassen
    fig.update_layout(
        xaxis_title="Aantal dieren",
        yaxis_title="Diersoort",
        transition_duration=500
    )

    # Waarden mooi tonen
    fig.update_traces(textposition="outside")

    return fig

# App starten
if __name__ == "__main__":
    app.run_server(debug=True)
