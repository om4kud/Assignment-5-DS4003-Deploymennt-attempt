# Omisha Mondal om4kud
# import libraries
from dash import Dash, html, dcc 
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

# Load the dataset
data = pd.read_csv('gdp_pcap.csv')

# Initialize app 
# Uses a stylesheet
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # load the CSS stylesheet

app = Dash(__name__, external_stylesheets=stylesheets) # initialize the app
server = app.server

# Layout
app.layout = html.Div([
    html.H1("GDP Per Capita Graphing Tool", style={'font-weight': 'bold'}),  # Title
    html.P("This interactive app displays the GDP per capita for various selected countries over the selected years. Each country is represented by a unique color. The data for this graphing tool comes from the Gapminder Dataset."), # Description

    # Dropdown menu and slider side by side
    html.Div([
        # Dropdown menu for choosing countries
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in data['country']],
            multi=True,
            value=['Afghanistan'],  # default selection, however you can change this
            style={'width': '35%', 'display': 'inline-block'} # this allows me to manipulate the width of the dropdown
        ),

        # Add a margin between dropdown and slider so they can appear side by side
        html.Div(
            style={'width': '5%', 'display': 'inline-block'}
        ),

        # Slider for choosing years
        # Documentation: https://dash.plotly.com/dash-core-components/rangeslider
        html.Div(
            dcc.RangeSlider(
                id='year-slider',
                min=int(data.columns[1]),  # minimum year is '1800' in column for year
                max=int(data.columns[-1]),  # maximum year is '2100' in column for year
                value=[int(data.columns[1]), int(data.columns[-1])],  # default range
                marks={str(year): str(year) for year in range(int(data.columns[1]), int(data.columns[-1])+1, 20)}, # makes marks for the slider every 20 years
                step=None,
            ),
            style={'width': '60%', 'display': 'inline-block'} # this allows me to manipulate the width of the slider
        ),
    ], style={'width': '100%', 'margin-bottom': '20px'}),  # this lets me use the entire width and add a margin to the bottom

    # dcc.Graph(id='gdp-graph') # Graph
    html.Div([
        dcc.Graph(id='gdp-graph', style={'width': '100%'}) # Graph
    ])

])


# Callback function to update the graph by interacting with dropdown and slider
# Documentation: https://dash.plotly.com/basic-callbacks
# https://dash.plotly.com/advanced-callbacks

# Callbacks allow for user interaction. This allows me to interact with the slider and dropdown menu, and this will affect what shows up on graph.
@app.callback( 
    Output('gdp-graph', 'figure'), # the output is the thing I want to update
    [Input('country-dropdown', 'value'), # the dropdown and slider are what "triggers" the callback, thereby allowing me to change the figure
     Input('year-slider', 'value')] # the input 
)

# Documentation for the below chunk of code are:
# melt: https://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.melt.html
# https://plotly.com/python/px-arguments/
# laylout: https://plotly.com/python/reference/layout/


def interact_graph(chosen_countries, chosen_years):
    filtered_data = data[['country'] + [str(year) for year in range(chosen_years[0], chosen_years[1]+1)]] # This allows me to filter the data to whatever I choose as the range of years
    filtered_data = filtered_data[filtered_data['country'].isin(chosen_countries)] # Filters the data again so that we select the chosen countries from dropdown menu
    
    melted_data = pd.melt(filtered_data, id_vars='country', var_name='year', value_name='gdpPercap') # Melt the data so 'year' is its own separate column
    melted_data['gdpPercap'] = pd.to_numeric(melted_data['gdpPercap'], errors='coerce')  # convert gdpPercap values to numeric 
    
    melted_data = melted_data.groupby(['country', 'year'], as_index=False).agg({'gdpPercap': 'mean'}) #aggregates mean gdp with year
    melted_data = melted_data.sort_values(by='year') # sort data by 'year' 
    
    
    fig = px.line(melted_data, x='year', y='gdpPercap', color='country', title='Average GDP Per Capita by Decade') # Creates the Line Plot
    fig.update_layout(xaxis_title='Year', yaxis_title='Average GDP Per Capita') # lets me update the xaxis, yaxis, and title to my desired text
    
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run(jupyter_mode='tab', debug=True) # local host run