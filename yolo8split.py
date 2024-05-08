import os
import shutil
import numpy as np
from sklearn.model_selection import train_test_split

# Directory containing your files
data_dir = 'subcell7'

# Splitting proportions
train_size = 0.70
test_size = 0.15
val_size = 0.15  # Implicitly, but good to specify

# A dictionary to keep track of data by class
class_files = {}

# Read all files and sort them by class based on the text file content
for filename in os.listdir(data_dir):
    if filename.endswith('.txt'):
        class_label = None
        with open(os.path.join(data_dir, filename), 'r') as file:
            class_label = file.readline().split()[0]  # Assumes class label is the first entry

        if class_label not in class_files:
            class_files[class_label] = []
        image_filename = filename.replace('.txt', '.png')
        class_files[class_label].append((image_filename, filename))

# Function to split data
def split_data(files, train_size, test_size, val_size):
    # Ensure the sum of split sizes is approximately 1
    assert abs((train_size + test_size + val_size) - 1) < 0.01, "Proportions must sum to 1"

    # Split into training and temp (test + val)
    train_files, temp_files = train_test_split(files, train_size=train_size, random_state=42)
    # Split temp into test and validation
    relative_test_size = test_size / (test_size + val_size)
    test_files, val_files = train_test_split(temp_files, test_size=relative_test_size, random_state=42)
    return train_files, test_files, val_files

# Creating directories for the splits and classes
for split in ['train', 'test', 'val']:
    for cls in class_files:
        os.makedirs(os.path.join(data_dir, split, cls), exist_ok=True)

# Split the files for each class and move/copy them to their respective folders
for cls, files in class_files.items():
    train_files, test_files, val_files = split_data(files, train_size, test_size, val_size)
    for file_group, split_name in zip([train_files, test_files, val_files], ['train', 'test', 'val']):
        for img_file, txt_file in file_group:
            # Copying image and text file to the appropriate directory
            shutil.copy(os.path.join(data_dir, img_file), os.path.join(data_dir, split_name, cls))
            # shutil.copy(os.path.join(data_dir, txt_file), os.path.join(data_dir, split_name, cls))


