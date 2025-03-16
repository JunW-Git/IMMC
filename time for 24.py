from datetime import datetime, timedelta
import csv

# Define city time zones (GMT offsets in hours)
city_time_zones = {
    "Manchester": 0,
    "Madrid": 0,
    "Munich": 1,
    "Paris": 0,
    "Milan": 1,
    "Mexico City": -6,
    "Los Angeles": -8,
    "Miami": -5,
    "Avellando": -5,
    "Buenos Aires": -3,
    "Sao Paulo": -3,
    "Cairo": 2,
    "Pretoria": 2,
    "Tunis": 1,
    "Riyadh": 3,
    "Kawasaki": 9,
    "Al Nassr": 3,
    "Melbourne": 10,
    "Auckland": 12,
    "Sydney": 10,
    "Racing Club": -3,  # Argentina
    "Independiente": -3,  # Argentina
    "Toluca FC": -6,  # Mexico
    "Shanghai Port FC": 8  # China
}

def calculate_local_time(gmt_time, time_zone):
    """Convert GMT time to local time based on time zone."""
    return gmt_time + timedelta(hours=time_zone)

def is_within_match_hours(local_time):
    """Check if local time is within 6 PM to 10 PM."""
    return 18 <= local_time.hour < 22

def is_within_viewing_hours(local_time):
    """Check if local time is within 5 PM to 12 AM."""
    return 17 <= local_time.hour < 24

def find_best_gmt_time(country_x, time_zones):
    """Find the best GMT time for a match in Country X that maximizes coverage."""
    best_gmt_time = None
    max_coverage = 0

    # Iterate through every possible GMT time in a 24-hour day
    for hour in range(24):
        for minute in range(0, 60, 15):  # Check every 15 minutes for efficiency
            gmt_time = datetime(2023, 10, 1, hour, minute)  # Arbitrary date
            local_match_time = calculate_local_time(gmt_time, time_zones[country_x])

            # Check if the local match time is within 6 PM to 10 PM in Country X
            if is_within_match_hours(local_match_time):
                # Calculate the number of other countries where the local time is within 5 PM to 12 AM
                coverage = 0
                for other_city, tz in time_zones.items():
                    if other_city != country_x:
                        local_viewing_time = calculate_local_time(gmt_time, tz)
                        if is_within_viewing_hours(local_viewing_time):
                            coverage += 1

                # Track the best GMT time
                if coverage > max_coverage:
                    max_coverage = coverage
                    best_gmt_time = gmt_time

    return best_gmt_time, max_coverage

# Prepare the results for all cities
results = []

for country_x in city_time_zones.keys():
    best_gmt_time, max_coverage = find_best_gmt_time(country_x, city_time_zones)
    local_match_time = calculate_local_time(best_gmt_time, city_time_zones[country_x])
    results.append([country_x, best_gmt_time.strftime('%H:%M'), local_match_time.strftime('%H:%M'), max_coverage])

# Write the results to a CSV file
csv_filename = "match_schedule_all_cities.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(["City", "Best GMT Time", "Local Match Time", "Number of Countries Watching"])
    # Write the data rows
    for row in results:
        writer.writerow(row)

print(f"Results have been saved to {csv_filename}")