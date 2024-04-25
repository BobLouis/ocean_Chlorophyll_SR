import pandas as pd

# Load the CSV file
# Replace 'path_to_your_file.csv' with the actual path to your CSV file
file_path = '海域水質測站2.csv'
data = pd.read_csv(file_path)

# Extract LAT and LON columns and create a 2D array
lon_lat_array = data[['LAT', 'LON']].values.tolist()

# If you want to print the entire array
for item in lon_lat_array:
    print(item)

# Write the array to a file
with open('output_coordinates.txt', 'w') as f:
    for coordinates in lon_lat_array:
        f.write(f"[{coordinates[0]}, {coordinates[1]}],\n")
