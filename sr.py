import pandas as pd
import numpy as np
import xarray as xr
import warnings
warnings.filterwarnings(
    "ignore", message=".*Passing method to Float64Index.get_loc is deprecated.*")

year = 2023
month = '09'
date = '12'
hour = '10'
min = '00'

filename = f'./NC_H09_{year}{month}{date}_{hour}{min}_R21_FLDK.06001_06001.nc'
ds = xr.open_dataset(filename)

lat_arr = []
lat_delta = []
lon_arr = []
lon_delta = []


# calculate lat
lat = 24
prev_lon = 0
for lon in np.arange(117, 123, 0.001):
    albedo_01_value = ds['albedo_01'].sel(
        longitude=lon, latitude=lat, method='nearest').values
    albedo_02_value = ds['albedo_02'].sel(
        longitude=lon, latitude=lat, method='nearest').values
    albedo_03_value = ds['albedo_03'].sel(
        longitude=lon, latitude=lat, method='nearest').values
    albedo_04_value = ds['albedo_04'].sel(
        longitude=lon, latitude=lat, method='nearest').values

    cur_val = (albedo_01_value, albedo_02_value,
               albedo_03_value, albedo_04_value)
    if lon > 117 and cur_val != prev_val:
        lon_delta = lon - prev_lon
        # print(lon_delta)
        # lon_delta_list.append(lon_delta)
        prev_lon = lon
        lon_arr.append(lon)

    prev_val = cur_val

prev_lon = 0
tmp = []
for i in lon_arr:
    delta = i - prev_lon
    # print(delta)
    if (delta > 0.03 and delta < 10):
        tmp.append((i+prev_lon)/2)
    prev_lon = i

lon_arr.extend(tmp)  # Add new midpoints to the original list
lon_arr.sort()       # Sort the list in place, do not assign the result

# calculate lon

lon = 118
prev_lat = 0
for lat in np.arange(21, 27, 0.001):
    albedo_01_value = ds['albedo_01'].sel(
        longitude=lon, latitude=lat, method='nearest').values
    albedo_02_value = ds['albedo_02'].sel(
        longitude=lon, latitude=lat, method='nearest').values
    albedo_03_value = ds['albedo_03'].sel(
        longitude=lon, latitude=lat, method='nearest').values
    albedo_04_value = ds['albedo_04'].sel(
        longitude=lon, latitude=lat, method='nearest').values

    cur_val = (albedo_01_value, albedo_02_value,
               albedo_03_value, albedo_04_value)
    if lat > 21 and cur_val != prev_val:
        lat_delta = lat - prev_lat
        # print(lat_delta)
        # lon_delta_list.append(lon_delta)
        prev_lat = lat
        lat_arr.append(lat)

    prev_val = cur_val

prev_lat = 0
tmp = []
for i in lat_arr:
    delta = i - prev_lat
    # print(delta)
    if (delta > 0.03 and delta < 10):
        tmp.append((i+prev_lat)/2)
    prev_lat = i

lat_arr.extend(tmp)  
lat_arr.sort()

# Write to file
with open('output.txt', 'w') as file:
    file.write("Latitude Delta Array:\n")
    file.write(str(lat_arr) + "\n\n")
    file.write("Longitude Delta Array:\n")
    file.write(str(lon_arr))


# Load the CSV file
# Replace 'path_to_your_file.csv' with the actual path to your CSV file
file_path = '海域水質測站2.csv'
data = pd.read_csv(file_path)

# Extract LAT and LON columns and create a 2D array
spots = data[['LAT', 'LON']].values.tolist()

# If you want to print the entire array
for item in spots:
    print(item)

# Write the array to a file
with open('output_coordinates.txt', 'w') as f:
    for coordinates in spots:
        f.write(f"[{coordinates[0]}, {coordinates[1]}],\n")





## classifying the spots
def find_closest(arr, coord):
    valid_indices = [i for i, x in enumerate(arr) if x < coord]

    if not valid_indices:
        return None

    closest_index = max(valid_indices, key=lambda i: arr[i])
    return closest_index




def classify_into_subgrid(lat_index, lon_index, lat, lon):
    lat_sub_division = (lat_arr[lat_index+1] - lat_arr[lat_index]) / 4
    lon_sub_division = (lon_arr[lon_index+1] - lon_arr[lon_index]) / 4

    lat_sub_index = int((lat - lat_arr[lat_index]) / lat_sub_division)
    lon_sub_index = int((lon - lon_arr[lon_index]) / lon_sub_division)

    if lat_sub_index == 4:
        lat_sub_index = 3
    if lon_sub_index == 4:
        lon_sub_index = 3

    return lat_sub_index * 4 + lon_sub_index

palace_grid_count = {i: 0 for i in range(16)}

# Classify each spot
for lat, lon in spots:
    lat_index = find_closest(lat_arr, lat)
    lon_index = find_closest(lon_arr, lon)
    subgrid_index = classify_into_subgrid(lat_index, lon_index, lat, lon)
    palace_grid_count[subgrid_index] += 1


print(palace_grid_count)

total_sum = sum(palace_grid_count.values())

print("Total sum of values:", total_sum)
