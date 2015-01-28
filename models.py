from django.db import models
from django.contrib.auth.models import User
import uuid
from django.contrib.gis.db import models
from autoslug import AutoSlugField

def get_upload_file_name(instance, filename):
    path_os = str(os.path.join(os.path.dirname(__file__), 'static/uploaded_files/').replace('\\','/'))
    print "El path_os -> %s" % path_os
    path = path_os + "%s_%s" % (str(uuid.uuid4()).replace('.', '_'), filename)
    
    return path

class UserProfile(models.Model):
   
    user = models.OneToOneField(User)
    email_verified = models.BooleanField()
    user_name = models.CharField(max_length=20, blank=True)
    full_name = models.CharField(max_length=50, blank=True)
    full_name_searchable = models.BooleanField()
    user_bio = models.TextField(blank=True)
    user_home_city = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=50, blank=True)
    website = models.CharField(max_length=250, blank=True)
    interests = models.CharField(max_length=5000, blank=True)
    user_photo = models.CharField(max_length=500, null=True, blank=True)       
    pro = models.BooleanField(default=False)
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u) [0])

class TourPoints(models.Model):    
    tour_point_id = models.AutoField(primary_key=True)    
    deprecated = models.NullBooleanField(null=True, blank=True)
    redirect_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)    
    description = models.CharField(max_length=50000, null=True, blank=True)
    address_1 = models.CharField(max_length=250, null=True, blank=True)
    address_2 = models.CharField(max_length=250, null=True, blank=True)    
    city = models.CharField(max_length=250, null=True, blank=True)    
    region = models.CharField(max_length=250, null=True, blank=True)    
    country_code = models.CharField(max_length=250, null=True, blank=True)   
    telephone_number = models.CharField(max_length=250, null=True, blank=True)    
    official_website = models.CharField(max_length=250, null=True, blank=True)    
    contact_email = models.CharField(max_length=250, null=True, blank=True)    
    latitude = models.DecimalField(blank=True, null=True, decimal_places=10, max_digits=19)
    longitude = models.DecimalField(blank=True, null=True, decimal_places=10, max_digits=19)
    geo_point = models.GeometryField(blank=True, null=True, geography=True)    
    geo_polygon = models.GeometryField(blank=True, null=True, geography=True)    
    social_1 = models.CharField(max_length=250, null=True, blank=True)
    social_2 = models.CharField(max_length=250, null=True, blank=True)
    social_3 = models.CharField(max_length=250, null=True, blank=True)
    social_4 = models.CharField(max_length=250, null=True, blank=True)
    social_5 = models.CharField(max_length=250, null=True, blank=True) 
    crossstreet = models.CharField(max_length=250, null=True, blank=True)    
    last_updated = models.IntegerField(null=True, blank=True)
    postcode = models.CharField(max_length=250, null=True, blank=True)    
    created_by = models.ForeignKey('auth.User', db_column='created_by')
    cover_image_url = models.CharField(max_length=250, blank=True, null=True)
    image_1_url = models.CharField(max_length=250, blank=True, null=True)
    image_2_url = models.CharField(max_length=250, blank=True, null=True)
    image_3_url = models.CharField(max_length=250, blank=True, null=True)
    image_4_url = models.CharField(max_length=250, blank=True, null=True)
    image_5_url = models.CharField(max_length=250, blank=True, null=True)
    audio_url = models.CharField(max_length=250, blank=True, null=True)
    audio_file = models.CharField(max_length=250, blank=True, null=True)
    video_url = models.CharField(max_length=1000, blank=True, null=True)
    video_file = models.CharField(max_length=1000, blank=True, null=True)
    sunday_open = models.CharField(max_length=1000, blank=True, null=True)
    sunday_close = models.CharField(max_length=1000, blank=True, null=True)
    monday_open = models.CharField(max_length=1000, blank=True, null=True)
    monday_close = models.CharField(max_length=1000, blank=True, null=True)
    tuesday_open = models.CharField(max_length=1000, blank=True, null=True)
    tuesday_close = models.CharField(max_length=1000, blank=True, null=True)
    wednesday_open = models.CharField(max_length=1000, blank=True, null=True)
    wednesday_close = models.CharField(max_length=1000, blank=True, null=True)
    thursday_open = models.CharField(max_length=1000, blank=True, null=True)
    thursday_close = models.CharField(max_length=1000, blank=True, null=True)
    friday_open = models.CharField(max_length=1000, blank=True, null=True)
    friday_close = models.CharField(max_length=1000, blank=True, null=True)
    saturday_open = models.CharField(max_length=1000, blank=True, null=True)
    saturday_close = models.CharField(max_length=1000, blank=True, null=True)
    additional_info = models.CharField(max_length=5000, blank=True, null=True) 
    objects = models.GeoManager()
    class Meta:
        db_table = 'tour_points'

class Media(models.Model):
    media_id = models.AutoField(primary_key=True)
    media_type = models.SmallIntegerField(blank=True)
    media_url = models.CharField(max_length=250, blank=True)
    media_creation_time = models.IntegerField(blank=True)
    media_created_by = models.CharField(max_length=250, blank=True)
    cover_image = models.CharField(max_length=250, blank=True)
    class Meta:
        db_table = 'media'

class MediaAssociations(models.Model):
    association_id = models.AutoField(primary_key=True)
    media_id_num = models.ForeignKey('touritz_app.Media', db_column='media_id_num')
    tour_point_id_num = models.ForeignKey('touritz_app.TourPoints', db_column='tour_point_id_num')
    class Meta:
        db_table = 'media_associations'
    
class Tours(models.Model):
    tour_id = models.AutoField(primary_key=True)
    tour_name = models.CharField(max_length=250, null=True, blank=True)    
    tour_name_slug = models.CharField(max_length=250, blank=True, null=True)
    cover_image_url = models.CharField(max_length=250, blank=True, null=True)
    image_250_url = models.CharField(max_length=250, blank=True, null=True)
    image_200_url = models.CharField(max_length=250, blank=True, null=True)
    image_320_url = models.CharField(max_length=250, blank=True, null=True)
    image_640_url = models.CharField(max_length=250, blank=True, null=True)
    cover_image_url = models.CharField(max_length=250, blank=True, null=True)    
    city = models.CharField(max_length=250, null=True, blank=True)
    description = models.CharField(max_length=10000, null=True, blank=True)
    tour_points_number = models.IntegerField(blank=True, null=True)
    time = models.IntegerField(blank=True, null=True)
    region = models.CharField(max_length=250, blank=True, null=True)    
    country_code = models.CharField(max_length=250, blank=True, null=True)   
    telephone_number = models.CharField(max_length=250, blank=True, null=True)    
    official_website = models.CharField(max_length=250, blank=True, null=True)    
    contact_email = models.CharField(max_length=250, blank=True, null=True)    
    social_1 = models.CharField(max_length=250, blank=True, null=True)
    social_2 = models.CharField(max_length=250, blank=True, null=True)
    social_3 = models.CharField(max_length=250, blank=True, null=True)
    social_4 = models.CharField(max_length=250, blank=True, null=True)
    social_5 = models.CharField(max_length=250, blank=True, null=True) 
    crossstreet = models.CharField(max_length=250, blank=True, null=True)    
    last_updated = models.IntegerField(blank=True, null=True)
    postcode = models.CharField(max_length=250, blank=True, null=True)    
    created_by = models.ForeignKey('auth.User', db_column='created_by')
    created_by_profile = models.ForeignKey('UserProfile', db_column='created_by_profile')
    creation_time = models.IntegerField(blank=True, null=True)
    featured = models.NullBooleanField(null=True, blank=True)
    front_page = models.NullBooleanField(null=True, blank=True)
    sunday_open = models.CharField(max_length=1000, blank=True, null=True)
    sunday_close = models.CharField(max_length=1000, blank=True, null=True)
    monday_open = models.CharField(max_length=1000, blank=True, null=True)
    monday_close = models.CharField(max_length=1000, blank=True, null=True)
    tuesday_open = models.CharField(max_length=1000, blank=True, null=True)
    tuesday_close = models.CharField(max_length=1000, blank=True, null=True)
    wednesday_open = models.CharField(max_length=1000, blank=True, null=True)
    wednesday_close = models.CharField(max_length=1000, blank=True, null=True)
    thursday_open = models.CharField(max_length=1000, blank=True, null=True)
    thursday_close = models.CharField(max_length=1000, blank=True, null=True)
    friday_open = models.CharField(max_length=1000, blank=True, null=True)
    friday_close = models.CharField(max_length=1000, blank=True, null=True)
    saturday_open = models.CharField(max_length=1000, blank=True, null=True)
    saturday_close = models.CharField(max_length=1000, blank=True, null=True)
    tour_created_by_display = models.CharField(max_length=1000, blank=True, null=True)
    tour_created_by_display_image = models.CharField(max_length=1000, blank=True, null=True)
    tour_created_by_display_description = models.CharField(max_length=1000, blank=True, null=True)
    additional_info_hours = models.CharField(max_length=5000, blank=True, null=True)
    photo_top_left = models.CharField(max_length=1000, blank=True, null=True)
    photo_bottom_left = models.CharField(max_length=1000, blank=True, null=True)
    photo_center = models.CharField(max_length=1000, blank=True, null=True)
    photo_top_right = models.CharField(max_length=1000, blank=True, null=True)
    photo_bottom_right = models.CharField(max_length=1000, blank=True, null=True)
    photo_panoramic = models.CharField(max_length=1000, blank=True, null=True)
    photo_panoramic_cropped = models.CharField(max_length=1000, blank=True, null=True)
    cover_photo_orientation = models.NullBooleanField(null=True, blank=True)
    published = models.NullBooleanField(null=True, blank=True)
    class Meta:
        db_table = 'tours'
        
class TourAndPointAssociations(models.Model):
    association_id = models.AutoField(primary_key=True)
    tour_id_num = models.ForeignKey('touritz_app.Tours', db_column='tour_id_num')
    tour_point_id_num = models.ForeignKey('touritz_app.TourPoints', db_column='tour_point_id_num')
    class Meta:
        db_table = 'tour_and_point_associations'

class TourCategories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=250, blank=True, null=True)
    category_slug = AutoSlugField(populate_from=lambda instance: instance.category_name, unique_with=['category_created_by__username'], slugify=lambda value: value.replace(' ','-'))
    category_created_by = models.ForeignKey('auth.User', db_column='created_by')
    creation_time = models.IntegerField(blank=True, null=True)
    featured = models.NullBooleanField(null=True, blank=True)
    order = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'tour_categories'

class CategoryAssociations(models.Model):
    association_id = models.AutoField(primary_key=True)
    tour_id_num = models.ForeignKey('touritz_app.Tours', db_column='tour_id_num')
    category_id_num = models.ForeignKey('touritz_app.TourCategories', db_column='category_id_num')
    class Meta:
        db_table = 'category_associations'

class BookMarks(models.Model):
    bookmark_id = models.AutoField(primary_key=True)
    user_id_num = models.ForeignKey('auth.User', db_column='user_id_num')
    tour_id_num = models.ForeignKey('touritz_app.Tours', db_column='tour_id_num')

class TemporaryPanoramic(models.Model):
    photo_id = models.AutoField(primary_key=True)
    time_created = models.IntegerField(blank=True, null=True)
    photo_panoramic = models.CharField(max_length=1000, blank=True, null=True)
    photo_panoramic_cropped = models.CharField(max_length=1000, blank=True, null=True)
    
class Tests(models.Model):
    test_id = models.AutoField(primary_key=True)
    field_1 =models.CharField(max_length=250, blank=True, null=True)

