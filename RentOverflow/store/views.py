from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect,HttpResponse, HttpResponseRedirect

from django.core.paginator import Paginator
from django.core.serializers import serialize

from .forms import searchForm
from .models import Property
from .serializers import PropertySerializer 

import re
import json
from django.http import JsonResponse

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def home(request):
    properties = Property.objects.all()
    properties = serialize('geojson', properties)
    form = searchForm()

    if request.method == 'POST':
        form = searchForm(request.POST)
        
        if form.is_valid():
            location = request.POST.get('location').lower()
            url = reverse('property_list')
            return HttpResponseRedirect(f"{url}?search={location}")

    return render(request, 'store/home.html', {'properties':properties,
                                               'form': form})




def property_list(request):
    search = request.GET.get('search')
    if search is None or search == '':
        properties = Property.objects.all()
    else:
        properties = get_closest_properties(search)

    search_location = request.GET.get("location-search")
    if search_location is None:
        search_location = search

    min_bed = str(request.GET.get("min-bed"))
    min_bed_number = get_number(min_bed)

    max_bed = str(request.GET.get("max-bed"))
    max_bed_number = get_number(max_bed)
    
    min_price = str(request.GET.get("min-price"))
    min_price_number = get_number(min_price)
    
    max_price = str(request.GET.get("max-price"))
    max_price_number = get_number(max_price)

    sortSelect = str(request.GET.get("sortSelect"))
    
    if search_location != '' and search_location is not None:
        properties = get_closest_properties(search_location)

    if min_bed_number != 'Choose...' and min_bed_number is not None:
        properties = properties.filter(bedrooms__gte=min_bed_number)

    if max_bed != 'Choose...' and max_bed_number is not None:
        properties = properties.filter(bedrooms__lte=max_bed_number)

    if min_price_number != 'Choose...' and min_price_number is not None:
        properties = properties.filter(price__gte=min_price_number)

    if max_price_number != 'Choose...' and max_price_number is not None:
        properties = properties.filter(price__lte=max_price_number)

    if sortSelect == 'Featured':
        pass

    if sortSelect == 'Price: Low to high':
        properties = Property.objects.all().order_by('price')

    if sortSelect == 'Price: High to low':
        properties = Property.objects.all().order_by('-price')

    if sortSelect == 'Bedroom: Low to high':
        properties = Property.objects.all().order_by('bedrooms')

    if sortSelect == 'Bedroom: High to low':
        properties = Property.objects.all().order_by('-bedrooms')

    p = Paginator(properties, 1)
    page = request.GET.get('page')
    properties_page = p.get_page(page) 

    return render(request, 'store/property_list.html', {'properties': properties,
                                                        'search':search_location,
                                                        'min_bed':min_bed,
                                                        'max_bed':max_bed,
                                                        'min_price':min_price,
                                                        'max_price':max_price,
                                                        'sortSelect':sortSelect,
                                                        'properties_page': properties_page
                                                        })

def property_info(request, pk):
    property = get_object_or_404(Property, pk=pk)
    context = {
        'property': property 
    }
    
    return render(request, 'store/property_info.html', context)


def get_number(string):
    match = re.search(r'\d+', string)
    if match:
        number = int(match.group())
        return number
    else:
        return None
    

def get_closest_properties(search):
    geolocator = Nominatim(user_agent='my-app')
    location = geolocator.geocode(search)
    search_lat = location.latitude
    search_lon = location.longitude

    reference_point = Point(x=search_lon, y=search_lat,srid=4326)
    # Query the three nearest properties
    nearest_properties = Property.objects.annotate(
        distance=Distance('point_geom', reference_point)
    ).order_by('distance')

    return nearest_properties