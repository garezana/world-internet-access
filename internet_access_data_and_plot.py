import urllib.request, json, pandas as pd, re, os
from operator import itemgetter
from pathlib import Path

path = os.path.abspath(os.path.dirname(__file__))
str_path = "my_path"

with urllib.request.urlopen("https://raw.githubusercontent.com/iancoleman/cia_world_factbook_api/master/data/factbook.json") as url:
    data = json.load(url)
    json_string = json.dumps(data)

list_of_lists = []
for i in data["countries"]:
    country_name=data["countries"][i]["data"]["name"]
    if(data["countries"][i]["data"].get("communications")):
        if (data["countries"][i]["data"]["communications"].get("internet")):
            if (data["countries"][i]["data"]["communications"]["internet"].get("users")):
                country_int_data = data["countries"][i]["data"]["communications"]["internet"]["users"]
                country_code = data["countries"][i]["data"]["communications"]["internet"].get("country_code")
                if country_code:
                    country_code = re.search("(?<=\.)[a-z]{2}", country_code).group(0) #cleaning data
                interney_dat_tup = (country_name , country_code) + itemgetter("total","percent_of_population", "date" )(country_int_data)
                list_of_lists.append(interney_dat_tup)

internet_country_df=pd.DataFrame(list_of_lists, columns=["country_name", "country_code", "total", "percent_of_population", "date"])
internet_country_df.to_csv( path / Path("internet_country_df.csv"), index=False)


#Median
internet_country_df["percent_of_population"][1:].median(skipna = True)


#Plotting map
from pygal.maps.world import World
wm = World()
wm.force_uri_protocol = 'http'
wm.title="World Map of Internet Access"

all_countries_internet_access = internet_country_df[['country_code', 'percent_of_population']].set_index('country_code').T.to_dict("records")
wm.add('Internet Access', all_countries_internet_access[0])
wm.render_to_file(path / Path("internet_world_map_2019.svg"))



