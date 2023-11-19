import geopandas as gpd
import requests

import folium
def getData(params):
    for i in range(10):
        print(i)
        response = requests.get(gbif_api_url, params=params)
    
        if response.status_code == 200:
            data = response.json()
            latitudes.extend([record["decimalLatitude"] for record in data["results"]])
            longitudes.extend([record["decimalLongitude"] for record in data["results"]])
            if len(data["results"]) < params["limit"]:
                break
            else:
                params["offset"] += params["limit"]
        else:
            print("Failed to retrieve data")
            break
Species = input("Enter a species name: ")  # User input for species name

# Use Geospatial data to draw the country boundary
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
country_data = world['geometry']

# Create an interactive map using Folium
m = folium.Map(location=[0, 0], zoom_start=2)


# Define GBIF API parameters, including the species name
gbif_api_url = "https://api.gbif.org/v1/occurrence/search"
params = {
    "hasCoordinate": "true",
    "limit": 300,
    "offset": 0,
    "scientificName": Species  # Include the species name in the query
}

latitudes = []
longitudes = []


getData(params)
    

# Add markers for biodiversity data
for lat, lon in zip(latitudes, longitudes):
    folium.CircleMarker(location=[lat, lon], radius=5, color='red').add_to(m)

# Display the map
m.save('interactive_map.html')
