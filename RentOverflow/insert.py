import os 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RentOverflow.settings")

import django
django.setup()

from django.contrib.gis.geos import Point
from store.models import Property

print(os.getcwd())

# # Create a new Property object
# property_obj = Property(
#     title='Example Property',
#     price=100000,
#     address='123 Main St',
#     description='This is an example property',
#     propertyType='House',
#     bedrooms=3,
#     bathrooms=2,
#     furnishedType='Unfurnished',
#     petFriendly='Yes',
#     smokers='No',
#     gardens='Backyard',
#     parking='Garage',
#     deposit=5000,
#     point_geom=Point(y=51.477292, x=-0.019888)  # Example coordinates
# )

# Save the Property object to the database
# property_obj.save()