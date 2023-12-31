from django.contrib.gis.geos import Point, Polygon
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect,HttpResponse, HttpResponseRedirect

from django.core.paginator import Paginator
from django.core.serializers import serialize

from .forms import searchForm

import re
import json
from django.http import JsonResponse

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

from django.utils import timezone
from datetime import timedelta

# import models
from django.contrib.auth.models import User
from account.models import UserFavorites
from .models import Property


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
    # user
    userfavorites = None
    user = None
    if request.user.is_authenticated:
       user = User.objects.get(id=request.user.id)
       userfavorites = get_object_or_404(UserFavorites, user=user)
       userfavorites = list(userfavorites.favorite.values_list('id', flat=True))

    # search location
    search = request.GET.get('search')
    if search is None or search == '':
        properties = Property.objects.all()
    else:
        properties = get_closest_properties(search)

    search_location = request.GET.get("location-search")
    if search_location is None:
        search_location = search
    
    # Filter by Polygon
    polygonSearch = request.GET.get('polygonSearch')
    if polygonSearch is not None and polygonSearch != '' and polygonSearch != 'None':
        polygonSearchArea = eval(polygonSearch)
        polygonSearchArea = convert_list_to_polygon(polygonSearchArea)
        properties = properties.filter(point_geom__within=polygonSearchArea)

    # Get selected value
    min_bed = str(request.GET.get("min-bed"))
    min_bed_number = get_number(min_bed)

    max_bed = str(request.GET.get("max-bed"))
    max_bed_number = get_number(max_bed)
    
    min_price = str(request.GET.get("min-price"))
    min_price_number = get_number(min_price)
    
    max_price = str(request.GET.get("max-price"))
    max_price_number = get_number(max_price)

    added_date = str(request.GET.get("added-date"))
    added_date_number = convert_days(added_date)

    property_type = str(request.GET.get("property-type"))
    pet_friendly = str(request.GET.get("pet-friendly"))
    parking = str(request.GET.get("parking"))
    garden = str(request.GET.get("garden"))
    furnish_type = str(request.GET.get("furnish-type"))
    distance_slider = str(request.GET.get("distance-slider"))
    distance_slider_number = get_number(str(request.GET.get("distance-slider")))

    sortSelect = str(request.GET.get("sortSelect"))
    
    # CLOSEST TO DISTANCE
    if search_location != '' and search_location is not None:
        properties = get_closest_properties(search_location)

    # MAIN 4 FILTERS
    if min_bed_number != 'Choose...' and min_bed_number is not None:
        properties = properties.filter(bedrooms__gte=min_bed_number)

    if max_bed != 'Choose...' and max_bed_number is not None:
        properties = properties.filter(bedrooms__lte=max_bed_number)

    if min_price_number != 'Choose...' and min_price_number is not None:
        properties = properties.filter(price__gte=min_price_number)

    if max_price_number != 'Choose...' and max_price_number is not None:
        properties = properties.filter(price__lte=max_price_number)

    # SORT SELECT

    if sortSelect == 'Price: Low to high':
        properties = properties.order_by('price')
    elif sortSelect == 'Price: High to low':
        properties = properties.order_by('-price')
    elif sortSelect == 'Bedroom: Low to high':
        properties = properties.order_by('bedrooms')
    elif sortSelect == 'Bedroom: High to low':
        properties = properties.order_by('-bedrooms')
    else:
        properties = properties.order_by('created_at')

    # POLYGON
    if polygonSearch is not None and polygonSearch != '' and polygonSearch != 'None':
        properties = properties.filter(point_geom__within=polygonSearchArea)

    # EXTRA FILTERS
    # added-date
    if added_date_number is not None:
        now = timezone.now()
        filter_day = now - timedelta(days=added_date_number)
        properties = properties.filter(created_at__gte=filter_day)

    # propertyType
    if property_type != 'Choose...' and property_type != 'None':
        properties = properties.filter(propertyType__contains=property_type)

    # petFriendly
    if pet_friendly != 'Choose...' and pet_friendly != 'None':
        properties = properties.filter(petFriendly__contains=pet_friendly)

    # parking
    if parking != 'Choose...' and parking != 'None':
        properties = properties.filter(parking__contains=parking)

    # gardens
    if garden != 'Choose...' and garden != 'None':
        properties = properties.filter(gardens__contains=garden)

    # furnish_type
    if furnish_type != 'Choose...' and furnish_type != 'None':
        properties = properties.filter(furnishedType__contains=furnish_type)

    # distance-slider
    if distance_slider_number is not None and search_location != '' and search_location is not None:
        properties = properties.filter(distance__lt=D(km=distance_slider_number)).order_by('distance')


    p = Paginator(properties, 20)
    page = request.GET.get('page')
    properties_page = p.get_page(page) 

    request.session['property_filters'] = {
        'page': page,
        'search':search,
        'min_bed': min_bed,
        'max_bed': max_bed,
        'min_price': min_price,
        'max_price': max_price,
        'sortSelect': sortSelect,
        'polygonSearch':polygonSearch,
        'added_date':added_date,
        'property_type':property_type,
        'pet_friendly':pet_friendly,
        'parking':parking,
        'garden':garden,
        'furnish_type':furnish_type,
        'distance_slider':distance_slider
    }


    return render(request, 'store/property_list.html', {'properties': properties,
                                                        'search':search_location,
                                                        'min_bed':min_bed,
                                                        'max_bed':max_bed,
                                                        'min_price':min_price,
                                                        'max_price':max_price,
                                                        'sortSelect':sortSelect,
                                                        'properties_page': properties_page,
                                                        'polygonSearch':polygonSearch,
                                                        'added_date': added_date,
                                                        'property_type': property_type,
                                                        'pet_friendly':pet_friendly,
                                                        'parking':parking,
                                                        'garden':garden,
                                                        'furnish_type':furnish_type,
                                                        'distance_slider':distance_slider,
                                                        'user':user,
                                                        'userfavorites':userfavorites
                                                        })

def property_info(request, pk):
    property = get_object_or_404(Property, pk=pk)
    propertyGS = serialize('geojson', [property])
    context = {
        'property': property,
        'propertyGS':propertyGS,
        'current_url': request.build_absolute_uri()
    }

    filter_parameters = request.session.get('property_filters', {})
    print(filter_parameters)
    if filter_parameters:
        back_to_property_list_url = f"?page={filter_parameters.get('page', filter_parameters.get('page', ''))}"
        if filter_parameters.get('search', ''):
            back_to_property_list_url += f"&location-search={filter_parameters.get('search', '')}"
        back_to_property_list_url += f"&min-bed={filter_parameters.get('min_bed', '')}&max-bed={filter_parameters.get('max_bed', '')}"
        back_to_property_list_url += f"&min-price={filter_parameters.get('min_price', '')}&max-price={filter_parameters.get('max_price', '')}"
        back_to_property_list_url += f"&sortSelect={filter_parameters.get('sortSelect', '')}"
        back_to_property_list_url += f"&polygonSearch={filter_parameters.get('polygonSearch', '')}"
        back_to_property_list_url += f"&added-date={filter_parameters.get('added_date', '')}"
        back_to_property_list_url += f"&property-type={filter_parameters.get('property_type', '')}"
        back_to_property_list_url += f"&pet-friendly={filter_parameters.get('pet_friendly', '')}"
        back_to_property_list_url += f"&parking={filter_parameters.get('parking', '')}"
        back_to_property_list_url += f"&garden={filter_parameters.get('garden', '')}"
        back_to_property_list_url += f"&furnish-type={filter_parameters.get('furnish_type', '')}"
        back_to_property_list_url += f"&distance-slider={filter_parameters.get('distance_slider', '')}"

        context['back_to_property_list_url'] = back_to_property_list_url
    
    return render(request, 'store/property_info.html', context)


def favorite_listing(request):
    user = User.objects.get(id=request.user.id)
    userfavorites, _ = UserFavorites.objects.get_or_create(user=user)
    favorite_properties = userfavorites.favorite.all()

    propertiesGS = serialize('geojson', favorite_properties)

    context = {
        'properties': favorite_properties,
        'propertiesGS':propertiesGS
    }
    return render(request, 'store/favorite_listing.html', context)


# supporting definitions
def get_number(string):
    string = str(string)
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

def convert_list_to_polygon(coordinates):
    # Closing the polygon by repeating the first point
    coordinates.append(coordinates[0])

    # Converting the coordinates to tuples
    coordinates = [(coord[1], coord[0]) for coord in coordinates]

    # Creating the Polygon object
    polygon = Polygon(coordinates)
    return polygon

def convert_days(string):
    if string == 'Choose...':
        return None 
    if string == 'Last 24h':
        return 1
    if string == 'Last 3 days':
        return 3
    if string == 'Last 7 days':
        return 7
    if string == 'Last 14 days':
        return 14