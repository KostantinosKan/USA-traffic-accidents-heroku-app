# Exploratory Data Analysis of A Countrywide Traffic Accident Dataset (2016 - 2020) - Interactive Dashboard
In this repository I will take the results from my previous EDA analysis of USA traffic accidents, and I will integrate them into a dash application. Then, I will deploy this dash application to Heroku.

## Code and Resources Used
**Python version:** 3.10.2<br/>
**Packages:** Dash, Dash-Bootstrap-Components, GeoPandas, Folium, Plotly, Pandas, Numpy.<br/>

### Building the Interactive Dashboard
* Create plotly graphs using the graph_object library.
* Create choropleth map using the folium library.
* Create an Indicator of the total number of accidents.
* Integrate all the above in a Dash application. 

### Deploy the Dash Application to Heroku
Guide: https://github.com/indielyt/heroku_dash_gdal_test

### Results
![alt text](https://github.com/KostantinosKan/USA-traffic-accidents-heroku-app/blob/main/data/map.JPG?raw=true)
* In the above map we can see the number of accidents per 1k residents on each state of U.S.A.
* For more results and interactivity check my interactive dashboard on Heroku.
* dash application link: https://usa-traffic-accidents.herokuapp.com/
