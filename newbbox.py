import json
#sub file path 

subfile = 'subcell7/' 

# Load your existing GeoJSON data
geojson_path = 'DI-MH-694-05_big.geojson'
with open(geojson_path, 'r') as file:
    geojson_data = json.load(file)

# Function to calculate the bounding box from a list of coordinates
def get_bounding_box(coordinates):
    x_coords = [coord[0] for coord in coordinates]
    y_coords = [coord[1] for coord in coordinates]
    return [min(x_coords), min(y_coords), max(x_coords), max(y_coords)]

# Convert polygons to bounding boxes
for feature in geojson_data['features']:
    # Assume each feature's geometry is a polygon
    if feature['geometry']['type'] == 'Polygon':
        # Get the first (and usually only) ring of the polygon (ignoring holes)
        polygon_coordinates = feature['geometry']['coordinates'][0]
        bbox = get_bounding_box(polygon_coordinates)
        # Change the geometry type to 'Polygon' with bbox as a rectangular polygon
        feature['geometry'] = {
            'type': 'Polygon',
            'coordinates': [[[bbox[0], bbox[1]], [bbox[0], bbox[3]], [bbox[2], bbox[3]], [bbox[2], bbox[1]], [bbox[0], bbox[1]]]]
        }


# Save the modified GeoJSON data to a new file
new_geojson_path = subfile + 'new_geojson.geojson'
with open(new_geojson_path, 'w') as file:
    json.dump(geojson_data, file, indent=4)

print(f"New GeoJSON file with bounding boxes has been saved to: {new_geojson_path}")
