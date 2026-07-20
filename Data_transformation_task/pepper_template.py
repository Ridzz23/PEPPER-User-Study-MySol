# to run: pyExt <file_name>

import json
import math
import folium



def risk_score(magnitude, depth):
    return (magnitude ** 2) * (1/(depth+1))

def distance(lat1, lon1, lat2, lon2):

    R = 6371

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(dlon / 2) ** 2
    )

    return 2 * R * math.asin(math.sqrt(a))



def add_marker(quake, map):

    folium.CircleMarker(
        location=[
            quake["latitude"],
            quake["longitude"]
        ],
        radius=5 + quake["risk"],
        popup=(
            f"{quake['place']}<br>"
            f"Risk: {quake['risk']:.2f}<br>"
            f"Nearest city: {quake['nearest_city']}"
        ),
        color="red",
        fill=True
    ).add_to(map)



#------------------------------ START CODING FROM HERE ------------------------------



# TODO 1:
# Download earthquake data from USGS.
#
# Extract California earthquakes.
#
# Store the result in:
#
# earthquake.json
#
# Use:
#   curl
#   jq
#   grep
#   pipes
#   redirection
#
# (DATA)


curl -s "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson" $| jq -c '.features[]' $| grep "CA" $> "earthquake.json"


# ----------------------------- DATA CLEANING (part of starter code provided) -----------------------------

cat "earthquake.json" $| jq -c '{
        id: .id,
        place: .properties.place,
        magnitude: .properties.mag,
        latitude: .geometry.coordinates[1],
        longitude: .geometry.coordinates[0],
        depth: .geometry.coordinates[2]
    }' $> "cleaned_earthquakes.json"




# TODO 2:
# Load cleaned_earthquakes.json into Python.
#
# Calculate earthquake risk score for every earthquake.
#
# Store all earthquakes in:
#
# earthquakes
#
# (DATA)



# TODO 3:
# Load cities.json.
#
# Each city contains:
#
# {
#   city,
#   latitude,
#   longitude,
#   population
# }
#
# For every earthquake:
#
# 1. Find the nearest city.
# 2. Calculate:
#
# proximity_risk =
# population / (distance_to_city + 1)
#
# 3. Add:
#
# nearest_city
# distance
# proximity_risk
#
# to the earthquake dictionary.
#
# (DATA)



city_data = cat "cities.json"

cities = json.loads(city_data)

earthquake_data = cat "cleaned_earthquakes.json"

earthquakes = []

for row in earthquake_data.splitlines():

    if row == "":
        continue

    quake = json.loads(row)

    # Find nearest city
    closest_city = None
    closest_distance = float("inf")

    for city in cities:

        d = distance(
            quake["latitude"],
            quake["longitude"],
            city["latitude"],
            city["longitude"]
        )

        if d < closest_distance:
            closest_distance = d
            closest_city = city


    # Add city proximity information
    quake["nearest_city"] = closest_city
    quake["distance"] = closest_distance

    quake["proximity_risk"] = (
        closest_city["population"] /
        (closest_distance + 1)
    )


    # Add earthquake risk
    quake["risk"] = risk_score(
        quake["magnitude"],
        quake["depth"]
    )


    earthquakes.append(quake)
    


# TODO 4:
# Calculate final risk:
#
# final_risk =
#
# earthquake risk * (1 + proximity_risk / 100000)
#
#
# Create a list:
#
# high_risk_earthquakes
#
# containing earthquakes where:
#
# final_risk > 1.0
#
# (DATA)


high_risk_earthquakes = []


for quake in earthquakes:

    quake["risk"] = (
        quake["risk"] *
        (1 + quake["proximity_risk"] / 100000)
    )

    if quake["risk"] > 1.0:
        high_risk_earthquakes.append(quake)




def city_report():

    output = ""

    for quake in high_risk_earthquakes:
        output += (
            quake["nearest_city"]
            + "\n"
        )

    return output

# TODO 5:
# Python -> Shell pipeline
# Use the city_report() function, sort the output, prefix the line with the number of occurences, and write to a city_risk_summary.txt file (DATA)

city_report() $| sort $| uniq -c $> city_risk_summary.txt

# Note: here users may also want to rewrite uniq as a python function 


# TODO 6:
# Write all earthquakes with their calculated risk
# into:
#
# risk_earthquakes.json
#
#
# Each earthquake should be stored as a JSON object
# on its own line.
#
# (FS)


for quake in earthquakes:

    json.dumps(quake) $>> "risk_earthquakes.json"



#----------------------------------- MAP GENERATION -------------------------- (should we ask users to do this? how would it tie into FS or DATA)

m = folium.Map(
    location=[37.5, -119.5],
    zoom_start=6
)


for quake in high_risk_earthquakes:
    add_marker(quake, m)


m.save("earthquake_risk_map.html")