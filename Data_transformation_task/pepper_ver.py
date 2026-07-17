import json
import folium
#generate a dataset of all earthquakes that have taken place in california
#calculate risk score for each and write it to the data set file as a new field called risk and write into a new file called risk_earthquakes.json
# risk = mag^2 * 1/(depth+1)

def risk_score(mag, depth):
    return (mag ** 2) * (1/(depth+1))

def save_to_map(longitude, latitude):
    folium.CircleMarker(
        location=[
            latitude,
            longitude,
        ],
        radius=5 + quake["risk"] * 5,
        popup=f"Risk: {quake['risk']}",
        color="red",
        fill=True
    ).add_to(m)


#CODE HERE

curl -s "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson" $| jq -c '.features[]' $| grep "CA" $> "earthquake.json"


# make this a custom function given to users: cat "earthquake.json" $| sed "'s/,$//'" $| jq -c "'{id: .id, place: .properties.place, magnitude: .properties.mag, latitude: .geometry.coordinates[1], longitude: .geometry.coordinates[0], depth: .geometry.coordinates[2]}'" $> "cleaned_earthquake.json"
# then users can do: func() $> "cleaned_earthquakes.json"

#cat "earthquake.json" $| jq -c '{id: .id, place: .properties.place, magnitude: .properties.mag, latitude: .geometry.coordinates[1], longitude: .geometry.coordinates[0], depth: .geometry.coordinates[2]}' $> "cleaned_earthquakes.json"

data = awk "'{print $0}'" "earthquake.json"
print(type(data))
print(type(data[0]))
data_list = data.split("\n")
final_data = []
print(data_list)

for row in data_list: 
    if row == "":
        continue
    row_dict = json.loads(row)
    row_dict["risk"] = risk_score(row_dict["properties"]["mag"], row_dict["geometry"]["coordinates"][2])
    final_data.append(row_dict)

output = "\n".join(json.dumps(row) for row in final_data)

print(output)

# fix this -- NEED APPEND AND FIX FOR MULTILINE STRINGS
#x = echo output $> "new_earthquakes.json"
#print(x)


#visualization 

m = folium.Map(
    location=[37.5, -119.5],
    zoom_start=6
)

for quake in final_data:
    save_to_map(quake["geometry"]["coordinates"][0], quake["geometry"]["coordinates"][1])
    

m.save("earthquake_map.html")



