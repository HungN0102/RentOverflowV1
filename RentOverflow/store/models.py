from django.contrib.gis.db import models
from django.urls import reverse

# Create your models here.
class Property(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=250, unique=True)
    price = models.DecimalField(max_digits=16, decimal_places=2)
    
    address = models.CharField(max_length=250, blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    propertyType = models.CharField(max_length=250, blank=True,null=True)
    bedrooms = models.IntegerField(blank=True,null=True)
    bathrooms= models.IntegerField(blank=True,null=True)
    furnishedType = models.CharField(max_length=250, blank=True,null=True)
    listingDate = models.DateTimeField(blank=True,null=True)
    petFriendly= models.CharField(max_length=250, blank=True,null=True)
    smokers= models.CharField(max_length=250, blank=True,null=True)
    gardens= models.CharField(max_length=250, blank=True,null=True)
    parking= models.CharField(max_length=250, blank=True,null=True)
    deposit = models.DecimalField(max_digits=16, decimal_places=2, blank=True,null=True)
    letAvailableDate = models.DateTimeField(blank=True,null=True)

    point_geom = models.PointField(srid=4326)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name_plural = 'properties'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("property_info", kwargs={"pk": self.pk})
    
class Image(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'images'

    def __str__(self):
        return self.property.title
