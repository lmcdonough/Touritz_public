from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.constants import ALL
from models import *
from tastypie.authentication import BasicAuthentication, Authentication
from tastypie.authorization import Authorization, DjangoAuthorization
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.exceptions import BadRequest
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        allowed_methods = ['get', 'put', 'patch']
        authentication = BasicAuthentication()
        authorization= DjangoAuthorization()
        filtering = {
            'id': ALL,
            'last_login': ALL,
            'is_superuser': ALL,
            'first_name': ALL,
            'last_name': ALL,
            'email': ALL,
            'is_staff': ALL,
            'is_active': ALL,
            'date_joined': ALL,
            }

class UserProfileResource(ModelResource):
    user = fields.OneToOneField(UserResource, 'user')
    class Meta:
        queryset = UserProfile.objects.all()
        allowed_methods = ['get', 'put', 'patch']
        resource_name = 'user-profile'
        authentication = BasicAuthentication()
        authorization= DjangoAuthorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'email_verified': ALL,
            'user_name': ALL,
            'full_name': ALL,
            'user_bio': ALL,
            'user_home_city': ALL,
            'zip_code': ALL,
            'longitude': ALL,
            'last_updated': ALL,
            'website': ALL,
            'interests': ALL_WITH_RELATIONS,
            'user_photo': ALL_WITH_RELATIONS,
            }

class CreateUserResource(ModelResource):
    class Meta:
        object_class = User
        resource_name = 'register'
        fields = ['username', 'email']
        #allowed_methods = ['post']
        include_resource_uri = False
        authentication = Authentication()
        authorization = Authorization()
        queryset = User.objects.all()

    def obj_create(self, bundle, request=None, **kwargs):
        try:
            bundle = super(UserSignUpResource, self).obj_create(bundle)
            bundle.obj.set_password(bundle.data.get('password'))
            bundle.obj.save()
        except IntegrityError:
            raise BadRequest('Username already exists')

        return bundle
    
class TourPointsResource(ModelResource):
    created_by = fields.ForeignKey(UserResource, 'created_by')
    class Meta:
        queryset = TourPoints.objects.all()
        resource_name = 'tour-points'
        authentication = BasicAuthentication()
        authorization= DjangoAuthorization()
        filtering = {
            'tour_point_id': ALL,
            'title': ALL,
            'address_1': ALL,
            'city': ALL,
            'region': ALL,
            'country_code': ALL,
            'latitude': ALL,
            'longitude': ALL,
            'last_updated': ALL,
            'postcode': ALL,
            'created_by': ALL_WITH_RELATIONS,
            'image_1_url': ALL,
            'image_2_url': ALL,
            'image_3_url': ALL,
            'image_4_url': ALL,
            'image_5_url': ALL,            
            'audio_url': ALL,
            'audio_file': ALL,
            'video_url': ALL,
            'video_file': ALL,
            'sunday_open': ALL,
            'sunday_close': ALL,
            'monday_open': ALL,
            'monday_close': ALL,
            'tuesday_open': ALL,
            'tuesday_close': ALL,
            'wednesday_open': ALL,
            'wednesday_close': ALL,
            'thursday_open': ALL,
            'thursday_close': ALL,
            'friday_open': ALL,
            'friday_close': ALL,
            'saturday_open': ALL,
            'saturday_close': ALL,            
            }
        
class MediaResource(ModelResource):
    class Meta:
        queryset = Media.objects.all()
        resource_name = 'media'
        authentication = BasicAuthentication()
        authorization= DjangoAuthorization()
        filtering = {            
            'media_id': ALL,
            'media_type': ALL,
            'media_url': ALL,
            'category_created_by': ALL,
            'media_creation_time': ALL,
            'cover_image': ALL,
            }

class MediaAssociationsResource(ModelResource):
    media_id_num = fields.ForeignKey(MediaResource, 'media_id_num')
    tour_point_id_num = fields.ForeignKey(TourPointsResource, 'tour_point_id_num')
    class Meta:
        queryset = MediaAssociations.objects.all()
        resource_name = 'media-associations'
        authentication = BasicAuthentication()
        authorization= DjangoAuthorization()        
        filtering = {            
            'association_id': ALL,
            'media_id_num': ALL_WITH_RELATIONS,
            'tour_point_id_num': ALL_WITH_RELATIONS,
            }

class ToursResource(ModelResource):
    created_by = fields.ForeignKey(UserResource, 'created_by')
    created_by_profile = fields.ForeignKey(UserProfileResource, 'created_by_profile')
    class Meta:
        queryset = Tours.objects.all()
        resource_name = 'tours'
        authentication = BasicAuthentication()
        authorization= DjangoAuthorization()        
        filtering = {
            'tour_id': ALL,
            'tour_name': ALL,
            'city': ALL,
            'featured': ALL,
            'region': ALL,
            'country_code': ALL,
            'last_updated': ALL,
            'postcode': ALL,
            'created_by': ALL_WITH_RELATIONS,
            'created_by_profile': ALL_WITH_RELATIONS,
            'front_page': ALL,
            'tour_name_slug': ALL,
            'cover_image_url': ALL,
            'image_250_url': ALL,
            'image_200_url': ALL,
            'image_320_url': ALL,
            'image_640_url': ALL,
            'city': ALL,
            'description': ALL,
            'tour_points_number': ALL,
            'time': ALL,
            'telephone_number': ALL,
            'official_website': ALL,
            'contact_email': ALL,
            'sunday_open': ALL,
            'sunday_close': ALL,
            'monday_open': ALL,
            'monday_close': ALL,
            'tuesday_open': ALL,
            'tuesday_close': ALL,
            'wednesday_open': ALL,
            'wednesday_close': ALL,
            'thursday_open': ALL,
            'thursday_close': ALL,
            'friday_open': ALL,
            'friday_close': ALL,
            'saturday_open': ALL,
            'saturday_close': ALL,
            'tour_created_by_display': ALL,
            'tour_created_by_display_image': ALL,
            'tour_created_by_display_description': ALL,       
            
            }
        
class TourAndPointAssociationsResource(ModelResource):
    tour_id_num = fields.ForeignKey(ToursResource, 'tour_id_num')
    tour_point_id_num = fields.ForeignKey(TourPointsResource, 'tour_point_id_num', full=True)
    class Meta:
        queryset = TourAndPointAssociations.objects.all()
        resource_name = 'tour-point-associations'
        authentication = BasicAuthentication()
        authorization= DjangoAuthorization()
        filtering = {            
            'association_id': ALL,
            'tour_id_num': ALL_WITH_RELATIONS,
            'tour_point_id_num': ALL_WITH_RELATIONS,
            }
         
class TourCategoriesResource(ModelResource):
    category_created_by = fields.ForeignKey(UserResource, 'category_created_by')
    class Meta:
        queryset = TourCategories.objects.all()
        resource_name = 'tour-categories'
        authentication = BasicAuthentication()
        authorization= DjangoAuthorization()
        filtering = {            
            'category_id': ALL,
            'category_name': ALL,
            'category_slug': ALL,
            'category_created_by': ALL_WITH_RELATIONS,
            'featured': ALL,
            'creation_time': ALL,
            }
        
class BookMarksResource(ModelResource):
    user_id_num = fields.ForeignKey(UserResource, 'user_id_num')
    tour_id_num = fields.ForeignKey(ToursResource, 'tour_id_num')
    class Meta:
        queryset = BookMarks.objects.all()
        resource_name = 'bookmarks'
        authentication = BasicAuthentication()
        authorization= DjangoAuthorization()
        filtering = {            
            'bookmark_id': ALL,
            'user_id_num': ALL_WITH_RELATIONS,
            'tour_id_num': ALL_WITH_RELATIONS,
            }

class CategoryAssociationsResource(ModelResource):
    tour_id_num = fields.ForeignKey(ToursResource, 'tour_id_num')
    category_id_num = fields.ForeignKey(TourCategoriesResource, 'category_id_num')
    class Meta:
        queryset = CategoryAssociations.objects.all()
        resource_name = 'category-associations'
        authentication = BasicAuthentication()
        authorization= DjangoAuthorization()
        filtering = {            
            'association_id': ALL,
            'tour_id_num': ALL_WITH_RELATIONS,
            'category_id_num': ALL_WITH_RELATIONS,
            }
        
class TestsResource(ModelResource):
    class Meta:
        queryset = Tests.objects.all()
        resource_name = 'tests'
        authentication = BasicAuthentication()
        authorization= Authorization()
