from .models import Property 
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

class PropertySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Property 
        #geo_field = 'point_geom'
        fields = '__all__'