import os
import csv
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RentOverflow.settings")
django.setup()

from django.contrib.gis.geos import Point
from django.core.files import File
from store.models import Image, Property

folder_path = 'prepare_data/images/'
image_file_names = os.listdir(folder_path)

for file_name in image_file_names:
    imageId = file_name.split("_")[1]
    image_file_path = folder_path + file_name

    try:
        property_obj = Property.objects.get(imageId=imageId)
    except Property.DoesNotExist:
        print(f"Property with imageId {imageId} does not exist. Skipping...")
        continue

    image_obj = Image(property=property_obj)
    
    if image_file_path:
        image_obj.image = File(open(image_file_path, 'rb'))
    
    image_obj.save()

print("Data insertion complete.")
