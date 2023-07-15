import os
import csv
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RentOverflow.settings")
django.setup()

from django.contrib.gis.geos import Point
from store.models import Property

# Specify the path to your CSV file
csv_file_path = "data.csv"

# Open the CSV file
with open(csv_file_path, "r") as file:
    reader = csv.DictReader(file)

    # Define a starting primary key value
    starting_pk = 1

    # Iterate over each row in the CSV file
    for row in reader:
        # Create a new Property object for each row
        property_obj = Property(
            pk=starting_pk,  # Assign a primary key value
            title=row["title"],
            price=float(row["price"]),
            address=row["address"],
            description=row["description"],
            propertyType=row["propertyType"],
            bedrooms=int(row["bedrooms"]),
            bathrooms=int(row["bathrooms"]),
            furnishedType=row["furnishedType"],
            petFriendly=row["petFriendly"],
            smokers=row["smokers"],
            gardens=row["gardens"],
            parking=row["parking"],
            deposit=float(row["deposit"]),
            point_geom=Point(y=float(row["latitude"]), x=float(row["longitude"]))  # Assuming the latitude and longitude are provided in the CSV
        )

        # Save the Property object to the database
        property_obj.save()

        # Increment the primary key value
        starting_pk += 1

print("Data insertion complete.")