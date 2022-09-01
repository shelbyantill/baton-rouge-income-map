import numpy as np
import pandas
import folium
import openpyxl
from folium.features import GeoJsonTooltip
import geopandas
import webbrowser

br_income_data= "income_data_visual_br.csv"
la_zip_code_data = "lazipcodes"

geojson = geopandas.read_file(la_zip_code_data)
geojson = geojson[["zcta5_code","geometry"]]

df = pandas.read_csv(br_income_data) #load data into data frame


df["Zip Code"]=df["Zip Code"].map(str)
df["Zip Code"]=df["Zip Code"].str.zfill(5)



df_final = geojson.merge(df, left_on="zcta5_code", right_on="Zip Code")
df_final = df_final[~df_final["geometry"].isna()]



map = folium.Map(location=[30.4515,-91.1], zoom_start=11.4, tiles="openstreetmap")


scale=(df_final["Total"].quantile((0,0.2,0.4,0.6,0.8,1))).tolist()

folium.Choropleth(
    geo_data= la_zip_code_data,
    data = df_final,
    columns = ["Zip Code","Total"],
    key_on="feature.properties.zcta5_code",
    threshold_scale=scale,
    fill_color="Purples",
    nan_fill_color="White",
    fill_opacity= 0.7,
    line_opacity=0.2,
    legend_name="Total Tax Payers - Baton Rouge Zip Codes in 2019-2020",
    highlight=True,
    line_color="black").add_to(map)

folium.features.GeoJson(
    data=df_final,
    name="Total Tax Payers",
    smooth_factor=2,
    style_function= lambda x:{"color":"black", "fillcolor":"transparent","weight":0.5},
    tooltip=folium.features.GeoJsonTooltip(
        fields=["Zip Code", "$1 under $25,000","$50,000 under $75,000", "$75,000 under $100,000","$100,000 under $200,000","$200,000 or more"],
        aliases=["Zip Code", "Incomes between $1 - $25,000","Incomes between $50,000 - $75,000", "Incomes between $75,000 - $100,000","Incomes between $100,000 - $200,000","Incomes greater than $200,000"],
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0EFEF"; border: 2px solid black; border-radius: 3px; box-shadow: 3px;
        """,
        max_width=800,),
            highlight_function=lambda x: {"weight": 3, "fillColor": "grey"},).add_to(map)




map.save("index.html")

