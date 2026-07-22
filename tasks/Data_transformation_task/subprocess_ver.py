import json
import subprocess
import folium

# --- 1. Define Functions ---

def risk_score(mag, depth):
    # Handle potential null or negative values smoothly
    if mag is None:
        mag = 0
    if depth is None or depth < 0:
        depth = 0
    return (mag ** 2) * (1 / (depth + 1))

def save_to_map(m, longitude, latitude, risk):
    folium.CircleMarker(
        location=[latitude, longitude],
        radius=5 + (risk * 5),
        popup=f"Risk: {risk:.2f}",
        color="red",
        fill=True
    ).add_to(m)


# --- 2. Execute Shell Pipeline via Subprocess ---

# This pulls the data, extracts individual features, filters for CA, and writes to earthquake.json
pipeline_cmd = (
    'curl -s "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson" '
    '| jq -c \'.features[]\' '
    '| grep "CA" > "earthquake.json"'
)

print("Fetching and filtering earthquake data...")
subprocess.run(pipeline_cmd, shell=True, check=True)


# --- 3. Process Data inside Python ---

final_data = []

# Read line-by-line directly from the generated file (safer than using awk via python)
with open("earthquake.json", "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        
        try:
            row_dict = json.loads(line)
            
            # Extract attributes from GeoJSON structure
            mag = row_dict["properties"]["mag"]
            lon = row_dict["geometry"]["coordinates"][0]
            lat = row_dict["geometry"]["coordinates"][1]
            depth = row_dict["geometry"]["coordinates"][2]
            
            # Calculate and append risk
            calculated_risk = risk_score(mag, depth)
            row_dict["risk"] = calculated_risk
            
            final_data.append(row_dict)
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            # Skip any malformed lines or missing data fields safely
            continue


# --- 4. Write Results to Output JSON ---

with open("risk_earthquakes.json", "w") as f:
    for row in final_data:
        f.write(json.dumps(row) + "\n")

print(f"Successfully processed {len(final_data)} earthquakes into 'risk_earthquakes.json'.")


# --- 5. Generate Folium Map Visualization ---

m = folium.Map(
    location=[37.5, -119.5],
    zoom_start=6
)

for quake in final_data:
    save_to_map(
        m=m,
        longitude=quake["geometry"]["coordinates"][0],
        latitude=quake["geometry"]["coordinates"][1],
        risk=quake["risk"]
    )

m.save("earthquake_map.html")
print("Map successfully saved to 'earthquake_map.html'.")