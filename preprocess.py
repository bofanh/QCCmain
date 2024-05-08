'''
Explanation of Key Components
OpenSlide Library: Used for accessing and navigating the .svs file.
GeoJSON Processing: This part of the script reads and interprets geographical annotation data related to regions on the slide.
Image Processing: Extracts specified regions from the whole slide image, converts them to RGB format, and saves them.
Annotation Conversion: Converts GeoJSON annotations to a format suitable for use with YOLO (a popular object detection model), including normalized bounding box coordinates.
File Handling: Saves each image and its corresponding annotation in a specified subdirectory.
This code is primarily used for preparing a dataset from annotated medical images for machine learning tasks, particularly object detection.


Inputs
Whole Slide Image (.svs file): The file DI-MH-694-05.svs is a high-resolution image typically used in digital pathology.
GeoJSON File: The file DI-MH-694-05.geojson contains annotations that describe specific regions of interest within the whole slide image. Each annotation includes a classification name and coordinates outlining the region.
Processing Steps
Load and Map Data: The script loads the whole slide image and the GeoJSON file. It maps predefined classification names (like 'Mitosis' and 'Kayrorrhexis') to numeric IDs.
Region Extraction and Image Processing: For each annotated region in the GeoJSON file, the script calculates the bounding box, extracts the corresponding region from the slide image, and converts it to RGB format.
Annotation Conversion: It converts the GeoJSON coordinates into a format suitable for YOLO (You Only Look Once) object detection models, including normalized bounding box coordinates.
Outputs
Processed Images: Images extracted from the specified regions in the whole slide image are saved in RGB format. Each image is named sequentially (e.g., image_0.png, image_1.png, etc.) and stored in the subcell5/ directory.
YOLO Format Annotations: For each image, a corresponding text file is created containing the YOLO formatted annotations, which include the class ID and normalized bounding box coordinates (e.g., image_0.txt, image_1.txt, etc.).
The script essentially transforms high-resolution pathology images and their respective annotations into a dataset ready for training in object detection tasks, specifically formatted for the YOLO model.

'''
import os 
cwd = os.getcwd()


import openslide
from PIL import Image
import json

#sub file path 

subfile = 'subcell7/' 

# Load SVS file
slide = openslide.OpenSlide('DI-MH-694-05.svs')

# Load GeoJSON file
with open('DI-MH-694-05_big.geojson', 'r') as file:
    geojson_data = json.load(file)


# Define a mapping from object names to class IDs
classification_to_id = {
    'Mitosis': 0,  # Example: 'cell' maps to 0
    'Kayrorrhexis': 1,  # Add other types as necessary
    # Add more mappings as needed
}

# Process each feature in the GeoJSON file
for index, feature in enumerate(geojson_data['features']):
    classification_name = feature['properties']['classification']['name']
    class_id = classification_to_id.get(classification_name, -1) # Default to -1 if not found
    
    coordinates = feature['geometry']['coordinates'][0]  # assuming one polygon per feature
    x_coords = [coord[0] for coord in coordinates]
    y_coords = [coord[1] for coord in coordinates]
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    # Define the dimensions of the region to extract
    width = max_x - min_x
    height = max_y - min_y

    # Read region from the whole slide image
    region = slide.read_region((int(min_x), int(min_y)), 0, (int(width), int(height)))
    region_image = region.convert('RGB')  # Convert from RGBA to RGB


    # Save the image
    image_filename = subfile + f'image_{index}.png'
    region_image.save(image_filename)

    # Calculate normalized bounding box coordinates for YOLO
    x_center = ((min_x + max_x) / 2 - min_x) / width
    y_center = ((min_y + max_y) / 2 - min_y) / height
    bbox_width = (max_x - min_x) / width
    bbox_height = (max_y - min_y) / height

    # Save annotations in YOLO format
    annotation_filename = subfile + f'image_{index}.txt'
    with open(annotation_filename, 'w') as f:
        f.write(f"{class_id} {x_center} {y_center} {bbox_width} {bbox_height}\n")

# Close the slide
slide.close()

print('images preprocess finished')