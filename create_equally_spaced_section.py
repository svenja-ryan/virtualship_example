# %% Create equally spaced stations along geographic sections
#
# Instructions:
# 1. Edit `section_specs` to define your sections.
# 2. For each section, provide start/end latitude and longitude.
# 3. Use either `spacing_km` or `n_stations` for each section.
# 4. Run all cells in order.
# 5. Station locations will be saved to `section_stations.csv`.
#
# Coordinates must be given in decimal degrees:
#   latitude:  -90 to 90
#   longitude: -180 to 180
#
# Example:
#   "spacing_km": 10
# creates stations approximately every 10 km.
#
# Alternatively:
#   "n_stations": 20
# creates exactly 20 stations, including both endpoints.
#
# The output CSV contains:
#   section number
#   section name
#   station number
#   latitude
#   longitude
#   distance from section start in km


# %% Imports
from pathlib import Path
import csv
import math
from openpyxl import Workbook


# %% Function
def create_section(start_lat, start_lon, end_lat, end_lon, spacing_km=None, n_stations=None):
    radius_m = 6_371_000

    start_lat_rad, start_lon_rad = math.radians(start_lat), math.radians(start_lon)
    end_lat_rad, end_lon_rad = math.radians(end_lat), math.radians(end_lon)

    start = (
        math.cos(start_lat_rad) * math.cos(start_lon_rad),
        math.cos(start_lat_rad) * math.sin(start_lon_rad),
        math.sin(start_lat_rad),
    )

    end = (
        math.cos(end_lat_rad) * math.cos(end_lon_rad),
        math.cos(end_lat_rad) * math.sin(end_lon_rad),
        math.sin(end_lat_rad),
    )

    angle = math.acos(sum(a * b for a, b in zip(start, end)))
    distance_m = radius_m * angle

    if spacing_km is not None:
        n_stations = math.ceil(distance_m / (spacing_km * 1000)) + 1

    stations = []

    for i in range(n_stations):
        fraction = i / (n_stations - 1)

        if angle == 0:
            vector = start
        else:
            a = math.sin((1 - fraction) * angle) / math.sin(angle)
            b = math.sin(fraction * angle) / math.sin(angle)
            vector = tuple(a * x + b * y for x, y in zip(start, end))

        x, y, z = vector
        latitude = math.degrees(math.atan2(z, math.hypot(x, y)))
        longitude = math.degrees(math.atan2(y, x))

        stations.append({
            "station": i + 1,
            "latitude": latitude,
            "longitude": longitude,
            "distance_from_start_km": distance_m * fraction / 1000,
        })

    return stations


# %% Define sections
section_specs = [
    {
        "name": "71W",
        "start_lat": 41.50,
        "start_lon": -71.00,
        "end_lat": 40,
        "end_lon": -71,
        "spacing_km": 5,
    },
    {
        "name": "South",
        "start_lat": 36.6,
        "start_lon": -72.00,
        "end_lat": 38.4,
        "end_lon": -74.6,
        "n_stations": 10,
    },
]


# %% Create all stations
all_stations = []

for section_number, section in enumerate(section_specs, start=1):
    stations = create_section(
        start_lat=section["start_lat"],
        start_lon=section["start_lon"],
        end_lat=section["end_lat"],
        end_lon=section["end_lon"],
        spacing_km=section.get("spacing_km"),
        n_stations=section.get("n_stations"),
    )

    for station in stations:
        all_stations.append({
            "section": section_number,
            "section_name": section["name"],
            **station,
        })

    print(f"{section['name']}: {len(stations)} stations")



# %% Save coordinates to CSV

output_file = Path("section_coordinates.csv")

columns = [
    "latitude",
    "longitude",
]

with output_file.open("w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()

    for station in all_stations:
        writer.writerow({
            "latitude": station["latitude"],
            "longitude": station["longitude"],
        })

print(f"Saved {len(all_stations)} coordinates to {output_file}")


