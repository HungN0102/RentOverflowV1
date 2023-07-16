import os
import csv
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RentOverflow.settings")
django.setup()

from django.contrib.gis.geos import Point
from store.models import Property

# Specify the path to your CSV file
csv_file_path = "final_data.csv"

# Open the CSV file
with open(csv_file_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        # Create a new Property object for each row
        property_obj = Property(
            title=row["Address"],
            price=float(row["Price"]),
            imageId=row['PropertyId'],
            address=row["Address"],
            description=row["Description"],
            propertyType=row["PropertyType"],
            bedrooms=int(float(row["Bedrooms"])) if row['Bedrooms'] != '' else None,
            bathrooms=int(float(row["Bathrooms"])) if row['Bathrooms'] != '' else None,
            furnishedType=row["FurnishedType"],
            petFriendly=row["PetFriendly"],
            smokers=row["Smokers"],
            gardens=row["Gardens"],
            parking=row["Parking"],
            deposit=float(row["Deposit"]) if row['Deposit'] != '' else None,
            point_geom=Point(y=float(row["latitude"]), x=float(row["longitude"]))  # Assuming the latitude and longitude are provided in the CSV
        )

        # Save the Property object to the database
        property_obj.save()

print("Data insertion complete.")