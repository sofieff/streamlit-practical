import plotly.express as px
import pandas as pd

def generate_scatter_plot(df: pd.DataFrame):
    """Generates a scatter plot and returns the figure."""
    fig = px.scatter(
        df,
        x="GDP per capita",
        y="Life Expectancy (IHME)",
        hover_name="year",
        log_x=True,
        size="Life Expectancy (IHME)",
        color="year",
        title="GDP per Capita vs Life Expectancy (IHME)",
        labels={
            "GDP per capita": "GDP per Capita (log scale)",
            "Life Expectancy (IHME)": "Life Expectancy (IHME)"
        }
    )
    return fig


