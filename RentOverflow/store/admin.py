from django.contrib.gis import admin
from .models import Property, Image

# Register your models here.
class CustomGeoAdmin(admin.GISModelAdmin):
    gis_widget_kwargs = {
        'attrs': {
            'default_zoom': 11, 
            'default_lat': 51.509865,
            'default_lon': -0.118092
        }
    }


# @admin.register(Property)
# class PropertyAdmin(CustomGeoAdmin):
#     prepopulated_fields = {
#         'slug': ('title',)
#     }

admin.site.register(Image)
admin.site.register(Property)