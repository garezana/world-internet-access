from pygal.maps.world import World
import urllib.request
import json
import pandas as pd
import re
import os
from operator import itemgetter
from pathlib import Path

path = os.path.abspath(os.path.dirname(__file__))
str_path = "my_path"

with urllib.request.urlopen("https://raw.githubusercontent.com/iancoleman/cia_world_factbook_api/master/data/factbook.json") as url:
    data = json.load(url)
    json_string = json.dumps(data)

list_of_lists = []
for country in data["countries"]:
    country_name = data["countries"][country]["data"]["name"]
    base_country_data = data["countries"][country]["data"]
    if base_country_data.get("communications"):
        if base_country_data["communications"].get("internet"):
            if base_country_data["communications"]["internet"].get("users"):
                country_int_data = data["countries"][country]["data"]["communications"]["internet"]["users"]
                country_code = data["countries"][country]["data"]["communications"]["internet"].get(
                    "country_code")
                if country_code:
                    country_code = re.search(
                        "(?<=\.)[a-z]{2}", country_code).group(0)  # cleaning data
                interney_dat_tup = (country_name, country_code) + itemgetter(
                    "total", "percent_of_population", "date")(country_int_data)
                list_of_lists.append(interney_dat_tup)

internet_country_df = pd.DataFrame(list_of_lists, columns=[
                                   "country_name", "country_code", "total", "percent_of_population", "date"])
internet_country_df.to_csv(path / Path("internet_country_df.csv"), index=False)


# Median
print(internet_country_df["percent_of_population"][1:].median(skipna=True))


# Plotting map
wm = World()
wm.force_uri_protocol = 'http'
wm.title = "Percentage of Population with Internet Access by Country "


all_countries_internet_access = internet_country_df[[
    'country_code', 'percent_of_population']].set_index('country_code').T.to_dict("records")

first_quart= {}
second_quart={}
third_quart={}
fourth_quart={}
for country, percentage in all_countries_internet_access[0].items():
    if percentage < 24.99:
        first_quart[country]=(percentage)
    if percentage > 24.99 and percentage < 49.99:
        second_quart[country]=(percentage)
    if percentage > 49.99 and percentage < 74.99:
        third_quart[country]=(percentage)
    if percentage > 74.99:
        fourth_quart[country]=(percentage)


wm.add('75% - 100%', fourth_quart)
wm.add('50% - 74.99%', third_quart)
wm.add('25% - 49.99%', second_quart)
wm.add('0% - 24.99%',first_quart )





#wm.add('Internet Access', all_countries_internet_access[0])
wm.render_to_file(("internet_world_map_2019.svg"))
