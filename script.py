# important libraries
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import html, dcc
import geopandas as gpd
import pandas as pd
import numpy as np
import folium
import dash
import json
import os


""" Load the Dataset """

DATASETS_file = "data/"
csv_file = "accidents_df_preproced.csv"
csv_file_path = os.path.join(DATASETS_file, csv_file)

accidents_df = pd.read_csv(filepath_or_buffer=csv_file_path)


""" Preprocess the Data """

# Create a new column named "merge_severity" by merging the severities of level 1 and level 2
accidents_df["merge_severity"] = accidents_df["Severity"].replace({1: 2})


""" Create Plotly Graphs """

## per Hour Graphs

# per Hour Barplot
def per_hour_barplot(df=accidents_df, width=900, height=500):
       
       # Amount of accidents per hour of the day and by level of severity
       acdnts_per_Hour_2 = df.loc[(df["merge_severity"] == 2)].groupby(by=["Start_Hour"]).count()["ID"]
       acdnts_per_Hour_3 = df.loc[(df["merge_severity"] == 3)].groupby(by=["Start_Hour"]).count()["ID"]
       acdnts_per_Hour_4 = df.loc[(df["merge_severity"] == 4)].groupby(by=["Start_Hour"]).count()["ID"]
       
       # Create the figure
       fig_1 = go.Figure(data=[
                               go.Bar(name="level 1-2", x=[i for i in range(0, 24)], y=acdnts_per_Hour_2.values, marker_color="#fedd84"),
                               go.Bar(name="level 3", x=[i for i in range(0, 24)], y=acdnts_per_Hour_3.values, marker_color="#feba5e"),
                               go.Bar(name="level 4", x=[i for i in range(0, 24)], y=acdnts_per_Hour_4.values, marker_color="#c41a3c"),
                              ]
                        )

       fig_1.update_layout(
                           title={
                                  "text":"Number of Accidents per Hour of the Day", 
                                  "font": {
                                           "size": 20,
                                           "color": "#FF8D00"
                                           },
                                  "xanchor": "center",
                                  "x": 0.5,
                                 },
                           xaxis={
                                  "showgrid": False,
                                  "tick0": 0, 
                                  "dtick": 1,
                                  "color": "#FF8D00"
                                 },
                           yaxis={
                                  "showgrid": False,
                                  "color": "#FF8D00"},
                           font={"size": 16}, 
                           legend={
                                   "traceorder": "reversed",
                                   "x": 0.861,
                                   "y": 0.99,
                                   "bgcolor": "#AAD3DF",
                                   "bordercolor": "#0f2537",
                                   "borderwidth": 2,
                                  },
                           legend_title_text="Severity",
                           legend_font_color="#0f2537",
                           autosize=False,
                           width=width,
                           height=height,
                           paper_bgcolor="#0f2537",
                           plot_bgcolor="#AAD3DF",
                           margin={
                                   "l": 15,
                                   "r": 10,
                                   "b": 0,
                                   "t": 60
                                  },
                           barmode="stack",
                          ),
       
       fig_1.update_traces(marker={"line": {
                                            "width": 2,
                                            "color": "black",
                                           },
                                  }
                          )
       return fig_1
   
# per Hour Lineplot
def per_hour_lineplot(df=accidents_df):

       # Total amount of accidents per hour of the Day
       tot_acdnts_per_Hour = df.groupby(by="Start_Hour").count()["ID"]

       # Amount of accidents with severity level 4 per hour of the day 
       acdnts_per_Hour_4 = df.loc[df["merge_severity"] == 4].groupby(by=["Start_Hour"]).count()["ID"]
       
       # Calculate percentages
       perc_per_hour_4 = []
       for total_count, count_sev_4 in list(zip(tot_acdnts_per_Hour.values, acdnts_per_Hour_4.values)):
              percent = (count_sev_4/total_count)*100
              perc_per_hour_4.append(round(number=percent, ndigits=2))
              
       # Create lineplot
       fig = go.Figure(data=[
                             go.Scatter(
                                        x=[i for i in range(0, 24)],
                                        y=perc_per_hour_4,
                                        mode="lines+markers",
                                        line={
                                              "color": "#0f2537",
                                              "width": 2
                                             },
                                       )
                             ]
                      )

       fig.update_layout(
                         title={
                                "text":"Percentage of Severity level 4 per Hour", 
                                "font": {
                                         "size": 20,
                                         "color": "#FF8D00"
                                        },
                                "xanchor": "center",
                                "x": 0.5,
                                },
                         xaxis={
                                "range": [-1, 24],
                                "zeroline": False,
                                "showgrid": False, 
                                "tickmode": "array",                            
                                "tickvals": [i for i in range(0, 24)],
                                "color": "#FF8D00"
                                },
                         yaxis={
                                "showgrid": False,
                                "color": "#FF8D00"},
                         font={"size": 16}, 
                         autosize=False,
                         width=1250,
                         height=300,
                         paper_bgcolor="#0f2537",
                         plot_bgcolor="#AAD3DF",
                         margin={
                                 "l": 15,
                                 "r": 10,
                                 "b": 0,
                                 "t": 30
                                },
                      ),
       return fig
 

## per Day of the Week Graphs

# per Day of the Week Barplot
def per_day_barplot(df=accidents_df, width=900, height=500):
      # Amount of accidents per day of the week and by level of severity
      acdnts_per_Day_2 = df.loc[df["merge_severity"] == 2].groupby(by=["Start_Day_Week"]).count()["ID"]
      acdnts_per_Day_3 = df.loc[df["merge_severity"] == 3].groupby(by=["Start_Day_Week"]).count()["ID"]
      acdnts_per_Day_4 = df.loc[df["merge_severity"] == 4].groupby(by=["Start_Day_Week"]).count()["ID"]
      
      fig = go.Figure(data=[
                            go.Bar(name="level 1-2", x=[i for i in range(0, 24)], y=acdnts_per_Day_2.values, marker_color="#fedd84"),
                            go.Bar(name="level 3", x=[i for i in range(0, 24)], y=acdnts_per_Day_3.values, marker_color="#feba5e"),
                            go.Bar(name="level 4", x=[i for i in range(0, 24)], y=acdnts_per_Day_4.values, marker_color="#c41a3c"),
                            ]
                     )

      fig.update_layout(
                        title={
                               "text":"Number of Accidents per Day of the Week", 
                               "font": {
                                             "size": 20,
                                             "color": "#FF8D00"
                                             },
                               "xanchor": "center",
                               "x": 0.5,
                               },
                        xaxis={
                               "showgrid": False, 
                               "tickmode": "array",
                               "tickvals": [i for i in range(0, 7)],
                               "ticktext": [
                                            "Mon", 
                                            "Tue", 
                                            "Wed", 
                                            "Thu", 
                                            "Fri", 
                                            "Sat", 
                                            "Sun"
                                             ],
                               "color": "#FF8D00"
                               },
                        yaxis={
                               "showgrid": False,
                               "color": "#FF8D00"},
                        legend={
                                "traceorder": "reversed",
                                "x": 0.861,
                                "y": 0.99,
                                "bgcolor": "#AAD3DF",
                                "bordercolor": "#0f2537",
                                "borderwidth": 2,
                               },
                        font={"size": 16}, 
                        legend_title_text="Severity",
                        legend_font_color="#0f2537",
                        autosize=False,
                        width=width,
                        height=height,
                        paper_bgcolor="#0f2537",
                        plot_bgcolor="#AAD3DF",
                        margin={
                                "l": 15,
                                "r": 10,
                                "b": 0,
                                "t": 60
                               },
                        barmode="stack",
                      ),
      
      fig.update_traces(marker={"line": {
                                         "width": 2,
                                         "color": "#0f2537"
                                        }
                               }
                       )
      return fig

# per Day of the Lineplot
def per_day_lineplot(df=accidents_df):
       
       # Total amount of accidents per day of the week
       tot_acdnts_per_Day = df.groupby(by=["Start_Day_Week"]).count()["ID"]

       # Amount of accidents with severity level 4 per day of the week 
       acdnts_per_Day_4 = df.loc[df["merge_severity"] == 4].groupby(by=["Start_Day_Week"]).count()["ID"]       
       
       # Calculate percentages
       perc_per_day_4 = []
       for total_count, count_sev_4 in list(zip(tot_acdnts_per_Day.values, acdnts_per_Day_4.values)):
              percent = (count_sev_4/total_count)*100
              perc_per_day_4.append(round(number=percent, ndigits=2))
              
       # Create lineplot
       fig = go.Figure(data=[
                             go.Scatter(
                                        x=[i for i in range(0, 7)],
                                        y=perc_per_day_4,
                                        mode="lines+markers",
                                        line={
                                               "color": "#0f2537",
                                               "width": 2
                                              },
                                       )
                            ]
                      )

       fig.update_layout(
                         title={
                                "text":"Percentage of Severity level 4 per Day", 
                                "font": {
                                         "size": 20,
                                         "color": "#FF8D00"
                                        },
                                "xanchor": "center",
                                "x": 0.5,
                                },
                         xaxis={
                                "range": [-0.5, 6.5],
                                "zeroline": False,
                                "showgrid": False, 
                                "tickmode": "array",                            
                                "tickvals": [i for i in range(0, 7)],
                                "ticktext": [
                                             "Mon", 
                                             "Tue", 
                                             "Wed", 
                                             "Thu", 
                                             "Fri", 
                                             "Sat", 
                                             "Sun"
                                              ],
                                "color": "#FF8D00"
                                },
                         yaxis={
                                "showgrid": False,
                                "color": "#FF8D00"
                                },
                         font={"size": 16}, 
                         autosize=False,
                         width=1250,
                         height=300,
                         paper_bgcolor="#0f2537",
                         plot_bgcolor="#AAD3DF",
                         margin={
                                 "l": 15,
                                 "r": 10,
                                 "b": 0,
                                 "t": 30
                                },
                      ),
       return fig
   
   
## per Month of the Years 2016-2020

# per Month Barplot
def per_month_barplot(df=accidents_df, width=900, height=500):
       
       # Find the amount of accidents per month of the year and by level of severity
       acdnts_per_Month_2 = df.loc[df["merge_severity"] == 2].groupby(by=["Start_Month"]).count()["ID"]
       acdnts_per_Month_3 = df.loc[df["merge_severity"] == 3].groupby(by=["Start_Month"]).count()["ID"]
       acdnts_per_Month_4 = df.loc[df["merge_severity"] == 4].groupby(by=["Start_Month"]).count()["ID"]
       
       fig = go.Figure(data=[
                             go.Bar(name="level 1-2", x=[i for i in range(0, 24)], y=acdnts_per_Month_2.values, marker_color="#fedd84"),
                             go.Bar(name="level 3", x=[i for i in range(0, 24)], y=acdnts_per_Month_3.values, marker_color="#feba5e"),
                             go.Bar(name="level 4", x=[i for i in range(0, 24)], y=acdnts_per_Month_4.values, marker_color="#c41a3c"),
                            ]
                      )

       fig.update_layout(
                         title={
                                "text":"Number of Accidents per Month", 
                                "font": {
                                         "size": 20,
                                         "color": "#FF8D00"
                                        },
                                "xanchor": "center",
                                "x": 0.5,
                                },
                         xaxis={
                                "showgrid": False, 
                                "tickmode": "array",
                                "tickvals": [i for i in range(0, 12)],
                                "ticktext": [
                                             "Jun", "Feb", "Mar", 
                                             "Apr", "May", "Jun", 
                                             "Jul", "Aug", "Sep", 
                                             "Oct", "Nov", "Dec" 
                                            ],
                                "color": "#FF8D00"
                                },
                         yaxis={
                                "showgrid": False,
                                "color": "#FF8D00"},
                         legend={
                                 "traceorder": "reversed",
                                 "x": 0.0052,
                                 "y": 0.99,
                                 "bgcolor": "#AAD3DF",
                                 "bordercolor": "#0f2537",
                                 "borderwidth": 2,
                                },
                         font={"size": 16}, 
                         legend_title_text="Severity",
                         legend_font_color="#0f2537",
                         autosize=False,
                         width=width,
                         height=height,
                         paper_bgcolor="#0f2537",
                         plot_bgcolor="#AAD3DF",
                         margin={
                                 "l": 15,
                                 "r": 10,
                                 "b": 0,
                                 "t": 60
                                },
                         barmode="stack",
                         ),
      
       fig.update_traces(marker={"line": {
                                          "width": 2,
                                          "color": "#0f2537"
                                         }
                                }
                        )
       return fig

# per Month Lineplot
def per_month_lineplot(df=accidents_df):
              
       # Total amount of accidents per month of the year
       tot_acdnts_per_Month = df.groupby(by=["Start_Month"]).count()["ID"]

       # Amount of accidents per month of the year and with severity level 4
       acdnts_per_Month_4 = df.loc[df["merge_severity"] == 4].groupby(by=["Start_Month"]).count()["ID"]    

       # Calculate percentages
       perc_per_month_4 = []
       for total_count, count_sev in list(zip(tot_acdnts_per_Month.values, acdnts_per_Month_4.values)):
              percent = (count_sev/total_count)*100
              perc_per_month_4.append(round(number=percent, ndigits=2))
              
       # Create lineplot
       fig = go.Figure(data=[
                             go.Scatter(
                                        x=[i for i in range(0, 12)],
                                        y=perc_per_month_4,
                                        mode="lines+markers",
                                        line={
                                               "color": "#0f2537",
                                               "width": 2
                                          },
                                       )
                            ]
                      )

       fig.update_layout(
                         title={
                                "text":"Percentage of Severity level 4 per Month", 
                                "font": {
                                         "size": 20,
                                         "color": "#FF8D00"
                                        },
                                "xanchor": "center",
                                "x": 0.5,
                                },
                         xaxis={
                                "range": [-0.5, 11.5],
                                "zeroline": False,
                                "showgrid": False, 
                                "tickmode": "array",
                                "tickvals": [i for i in range(0, 12)],
                                "ticktext": [
                                             "Jun", "Feb", "Mar", 
                                             "Apr", "May", "Jun", 
                                             "Jul", "Aug", "Sep", 
                                             "Oct", "Nov", "Dec" 
                                              ],
                                "color": "#FF8D00"
                                },
                         yaxis={
                                "showgrid": False,
                                "color": "#FF8D00"
                                },
                         font={"size": 16}, 
                         autosize=False,
                         width=1250,
                         height=300,
                         paper_bgcolor="#0f2537",
                         plot_bgcolor="#AAD3DF",
                         margin={
                                 "l": 15,
                                 "r": 10,
                                 "b": 0,
                                 "t": 30
                                },
                     ),
       return fig


## over the Years 2016-2020

# over the Years Barplot
def per_year_barplot(df=accidents_df, width=900, height=500):
       # Amount of accidents per month of the year and by level of severity
       acdnts_per_Year_2 = df.loc[df["merge_severity"] == 2].groupby(by=["Start_Year"]).count()["ID"]
       acdnts_per_Year_3 = df.loc[df["merge_severity"] == 3].groupby(by=["Start_Year"]).count()["ID"]
       acdnts_per_Year_4 = df.loc[df["merge_severity"] == 4].groupby(by=["Start_Year"]).count()["ID"]
       
       fig = go.Figure(data=[
                             go.Bar(name="level 1-2", x=[i for i in range(0, 24)], y=acdnts_per_Year_2.values, marker_color="#fedd84"),
                             go.Bar(name="level 3", x=[i for i in range(0, 24)], y=acdnts_per_Year_3.values, marker_color="#feba5e"),
                             go.Bar(name="level 4", x=[i for i in range(0, 24)], y=acdnts_per_Year_4.values, marker_color="#c41a3c"),
                             ]
                      )

       fig.update_layout(
                         title={
                                "text":"Number of Accidents per Hour of the Day", 
                                "font": {
                                         "size": 20,
                                         "color": "#FF8D00"
                                         },
                                "xanchor": "center",
                                "x": 0.5,
                                },
                         xaxis={
                                "showgrid": False, 
                                "tickmode": "array",
                                "tickvals": [i for i in range(0, 5)],
                                "ticktext": [
                                             "2016", "2017",
                                             "2018", "2019",
                                             "2020"
                                              ],
                                "color": "#FF8D00"
                                },
                         yaxis={
                                "showgrid": False,
                                "color": "#FF8D00"},
                         legend={
                                 "traceorder": "reversed",
                                 "x": 0.0052,
                                 "y": 0.99,
                                 "bgcolor": "#AAD3DF",
                                 "bordercolor": "#0f2537",
                                 "borderwidth": 2,
                                },
                         font={"size": 16}, 
                         legend_title_text="Severity",
                         legend_font_color="#0f2537",
                         autosize=False,
                         width=width,
                         height=height,
                         paper_bgcolor="#0f2537",
                         plot_bgcolor="#AAD3DF",
                         margin={
                                 "l": 15,
                                 "r": 10,
                                 "b": 0,
                                 "t": 60
                                },
                         barmode="stack",
                        ),
      
       fig.update_traces(marker={"line": {
                                          "width": 2,
                                          "color": "#0f2537"
                                         }
                                }
                       )
       return fig

# over the Years Lineplot
def per_year_lineplot(df=accidents_df):
              
       # Total amount of accidents per month of the year
       tot_acdnts_per_Year = df.groupby(by=["Start_Year"]).count()["ID"]

       # Amount of accidents per month of the year and by level of severity
       acdnts_per_Year_4 = df.loc[df["merge_severity"] == 4].groupby(by=["Start_Year"]).count()["ID"]
       
       perc_per_year_4 = []
       for total_count, count_sev in list(zip(tot_acdnts_per_Year.values, acdnts_per_Year_4.values)):
              percent = (count_sev/total_count)*100
              perc_per_year_4.append(round(number=percent, ndigits=2))
              
       # Create lineplot
       fig = go.Figure(data=[
                             go.Scatter(
                                    x=[i for i in range(0, 5)],
                                    y=perc_per_year_4,
                                    mode="lines+markers",
                                    line={
                                          "color": "#0f2537",
                                          "width": 2
                                          },
                                      )
                           ]
                      )

       fig.update_layout(
                         title={
                                "text":"Percentage of Severity level 4 per Year", 
                                "font": {
                                         "size": 20,
                                         "color": "#FF8D00"
                                              },
                                "xanchor": "center",
                                "x": 0.5,
                                },
                         xaxis={
                                "range": [-0.25, 4.25],
                                "zeroline": False,
                                "showgrid": False, 
                                "tickmode": "array",
                                "tickvals": [i for i in range(0, 5)],
                                "ticktext": [
                                             "2016", "2017",
                                             "2018", "2019",
                                             "2020"
                                            ],
                                "color": "#FF8D00"
                                },
                         yaxis={
                                "showgrid": False,
                                "color": "#FF8D00"
                                },
                         font={"size": 16}, 
                         autosize=False,
                         width=1250,
                         height=300,
                         paper_bgcolor="#0f2537",
                         plot_bgcolor="#AAD3DF",
                         margin={
                                 "l": 15,
                                 "r": 10,
                                 "b": 0,
                                 "t": 30
                                },
                       ),
       return fig


## Total Accidents over the Years Indicator
def total_accidents_indicator(df=accidents_df):
      
      # Total accidents over a range of years, or per year
      tot_acdnts_per_Year = df.groupby(by=["Start_Year"]).count()["ID"]

      # Total accidents Indicator metric
      fig = go.Figure(data=[
                            go.Indicator(
                                         value=tot_acdnts_per_Year.values.sum(),
                                         number={"font": {
                                                          "color": "#c41a3c",
                                                          "size": 50
                                                         }
                                                },
                                        )
                        ]  
                    )
      
      fig.update_layout(
                        title={
                               "text":"Total<br>Accidents", 
                               "font": {
                                        "size": 20,
                                        "color": "#FF8D00"
                                       },
                               "xanchor": "center",
                               "x": 0.5,
                               "y": 0.8
                              },
                        autosize=False,
                        width=200,
                        height=200,
                        paper_bgcolor="#0f2537",
                       ),
      return fig


""" Choropleth Map """

## We will create the map using folium an we'll integrate the map with Dash app
## using the IFrame oject of plotly and calling the map as an HTML file

def create_usa_map(df=accidents_df):

    # Group by State and count the accidents
    accidents_per_state = df.groupby(['State'])['Count'].sum().reset_index()
    
    # Load the US state population in a dataframe
    us_population = pd.read_csv("https://raw.githubusercontent.com/jakevdp/data-USstates/master/state-population.csv")
    uspop_2013 = us_population[(us_population['year'] == 2013) & (us_population['ages'] == 'total')]
    uspop_2013 = uspop_2013.drop(columns=['ages', 'year'])
    uspop_2013.columns = ['State', 'Population']

    # Merge accidents_per_state dataframe with uspop_2013 on "State" and calculate the accidents per 1k residents
    pop_df = accidents_per_state.merge(right=uspop_2013, how="inner", left_on="State", right_on="State")
    pop_df['Accident_per_1k_resident'] = round(number=(pop_df['Count']/pop_df['Population'])*1000, ndigits=2)
    
    # Load the US json file
    url = ("https://raw.githubusercontent.com/python-visualization/folium/master/examples/data")
    state_geo = f"{url}/us-states.json"
    gdf_state = gpd.read_file(state_geo)

    # Create the final dataframe by merging the gdf_state with the pop_df dataframes
    final_df = gdf_state.merge(right=pop_df, left_on="id", right_on="State", how="inner")
    
    # Create the map using Choropleth method of the folium class
    usa_map = folium.Map(location=[37, -102], zoom_start=4, control_scale=True)
    folium.Choropleth(
                      geo_data=final_df,
                      data=final_df,
                      columns=['State',"Accident_per_1k_resident"],
                      key_on="feature.properties.State",
                      fill_color='YlOrRd',
                      fill_opacity=1,
                      line_opacity=0.2,
                      legend_name="Accidents per 1k residents",
                      smooth_factor=0,
                      Highlight= True,
                      line_color = "black",
                      name = "Count",
                      show=True,
                      overlay=True,
                      nan_fill_color = "White"
                      ).add_to(usa_map)

    # Create the hovering option
    style_function = lambda x: {
                                'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1
                               }
    highlight_function = lambda x: {
                                    'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1
                                   }

    toolkit = folium.features.GeoJson(
                                      final_df,
                                      style_function=style_function, 
                                      control=False,
                                      highlight_function=highlight_function, 
                                      tooltip=folium.features.GeoJsonTooltip(
                                                                             fields=['State','Accident_per_1k_resident'],
                                                                             aliases=['State: ','# Accidents per 1k: '],
                                                                             style=(
                                                                                    """background-color: white; 
                                                                                       color: #333333; 
                                                                                       font-family: arial; 
                                                                                       font-size: 12px; 
                                                                                       padding: 10px;""") 
                                                                            )
                                    )

    usa_map.add_child(toolkit)
    usa_map.keep_in_front(toolkit)
    return usa_map


""" Dash Application """

min_year = accidents_df["Start_Year"].min()
max_year = accidents_df["Start_Year"].max()

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # external JavaScript files

app = dash.Dash(name=__name__, external_stylesheets=[dbc.themes.SUPERHERO])
server = app.server

app.layout = html.Div(children=[
                                html.H1(
                                        children="USA Traffic Accidents - Interactive Dashboard",
                                        style={
                                               "textAlign": "center",
                                               "fontWeight": "bold",
                                               "fontSize": 32,
                                               "color": "#FF8D00"
                                              }
                                       ),
                                html.Br(),
                                dcc.RangeSlider(
                                                id="range-slider",
                                                min=min_year,
                                                max=max_year,
                                                marks={
                                                       2016: {
                                                              "label": "2016",
                                                              "style": {
                                                                        "color": "#FF8D00",
                                                                        "margin-top": "-40px",
                                                                        "font-size": "14px"
                                                                        },
                                                             },
                                                       2017: {
                                                              "label": "2017",
                                                              "style": {
                                                                        "color": "#FF8D00",
                                                                        "margin-top": "-40px",
                                                                        "font-size": "14px"
                                                                        },
                                                             },
                                                       2018: {
                                                              "label": "2018",
                                                              "style": {
                                                                        "color": "#FF8D00",
                                                                        "margin-top": "-40px",
                                                                        "font-size": "14px"
                                                                        },
                                                             },
                                                       2019: {
                                                              "label": "2019",
                                                              "style": {
                                                                        "color": "#FF8D00",
                                                                        "margin-top": "-40px",
                                                                        "font-size": "14px"
                                                                        },
                                                             },
                                                       2020: {
                                                              "label": "2020",
                                                              "style": {
                                                                        "color": "#FF8D00",
                                                                        "margin-top": "-40px",
                                                                        "font-size": "14px"
                                                                        },
                                                             },
                                                      },
                                                value=[2017, 2019]
                                               ),
                                html.Div(children=[
                                                   html.Iframe(
                                                               id="choropleth", 
                                                               srcDoc="" , 
                                                               width="920",
                                                               height="439.1",
                                                               style={
                                                                      "backgroundColor": "lightblue",
                                                                     }
                                                              ),
                                                   ],
                                         style={
                                                "display": "inline-block",
                                                }
                                        ),
                                html.Div(children=[
                                                   dcc.Graph(
                                                             id="barplot", 
                                                             figure={}, 
                                                             style={
                                                                    "backgroundColor": "lightblue",
                                                                    "display": "inline-block",
                                                                    "marginLeft": "5px",
                                                                   }
                                                            ),
                                                  ],
                                         style={
                                                "display": "inline-block",
                                               }
                                        ),
                                html.Div(children=[
                                                   html.H5(
                                                          children="Time Reference",
                                                          style={
                                                                 "position": "absolute",
                                                                 "right": "4.9%",
                                                                 "bottom": "210px",
                                                                 "fontSize": "22px",
                                                                 "color": "#FF8D00"
                                                                 }
                                                          )
                                                  ]
                                        ),         
                                dcc.RadioItems(
                                               id="radio-items-b",
                                               options=[
                                                        "per Hour", 
                                                        "per Day", 
                                                        "per Month", 
                                                        "per Year"
                                                       ],
                                               value="per Hour",
                                               labelStyle ={
                                                            "display": "block",
                                                            "color": "#c41a3c",
                                                            "font-size": "20px",
                                                           },
                                               inputStyle={
                                                           "margin-right": "-112px",
                                                           },
                                               style={
                                                      "position": "absolute",
                                                      "right": "6.5%",
                                                      "bottom": "100px" 
                                                     }
                                              ),
                                html.Div(children=[
                                                   dcc.Graph(
                                                             id="lineplot",
                                                             figure={},
                                                            )
                                                  ],
                                          style={
                                                 "position": "absolute",
                                                 "left": "300px",
                                                 "bottom": "10px"
                                                }
                                        ),
                                html.Div(children=[
                                                   dcc.Graph(
                                                             id="indicator",
                                                             figure={},
                                                            )
                                                  ],
                                          style={
                                                 "position": "absolute",
                                                 "left": "50px",
                                                 "bottom": "50px"
                                                }
                                        )
                                ]
                     )

# Create callback to connect the slider with the map and with the metric
@app.callback(
              Output(component_id="choropleth", component_property="srcDoc"),
              Output(component_id="indicator", component_property="figure"),
              [Input(component_id="range-slider", component_property= "value")],
             )

def update_map(slider_range):
       """ Function that updates values fron the slider to the graph. Also
           it changes between different severity levels with the use of radio items."""
           
       year_min, year_max  = slider_range
       df_updated = accidents_df.loc[(accidents_df["Start_Year"] >= year_min) & (accidents_df["Start_Year"] <= year_max)]

       # create the map
       usa_map = create_usa_map(df=df_updated)
       # usa_map.save(outfile="usa_states_map.html")
       # usa_map_source = open(file="usa_states_map.html", mode="r").read() 
       
       # create the indicator
       indicator = total_accidents_indicator(df=df_updated)
       
       return usa_map._repr_html_(), go.Figure(indicator)
       

# Create callback to connect the slider and the radio buttons with the graphs
@app.callback(
              Output(component_id="barplot", component_property="figure"),
              Output(component_id="lineplot", component_property="figure"),
              [Input(component_id="range-slider", component_property= "value")],
              [Input(component_id="radio-items-b", component_property="value")]
             )

def update_graphs(slider_range, radio_choice):
       """ Function that updates values from the slider to the graph. Also
           it changes between barplots with different choices of radio items."""
       
       year_min, year_max  = slider_range
       df_updated = accidents_df.loc[(accidents_df["Start_Year"] >= year_min) & (accidents_df["Start_Year"] <= year_max)]
       
       # Create the barplots
       if radio_choice == "per Hour":
              bar_fig = per_hour_barplot(df=df_updated, width=936, height=500)
              lin_fig = per_hour_lineplot(df=df_updated)
       elif radio_choice == "per Day":
              bar_fig = per_day_barplot(df=df_updated, width=936, height=500)
              lin_fig = per_day_lineplot(df=df_updated)
       elif radio_choice == "per Month":
              bar_fig = per_month_barplot(df=df_updated, width=936, height=500)
              lin_fig = per_month_lineplot(df=df_updated)
       else:  # per Year
              bar_fig = per_year_barplot(df=df_updated, width=936, height=500)
              lin_fig = per_year_lineplot(df=df_updated)

       return go.Figure(bar_fig), go.Figure(lin_fig)


if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)