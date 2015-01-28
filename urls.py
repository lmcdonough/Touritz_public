from django.conf.urls import patterns, include, url
from touritz_app.api import *
from tastypie.api import Api
#from touritz_app.api.resources import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(UserProfileResource())
v1_api.register(TourPointsResource())
v1_api.register(MediaResource())
v1_api.register(ToursResource())
v1_api.register(TourCategoriesResource())
v1_api.register(BookMarksResource())
v1_api.register(UserResource())
v1_api.register(TestsResource())      
v1_api.register(MediaAssociationsResource())
v1_api.register(TourAndPointAssociationsResource())
v1_api.register(CategoryAssociationsResource())
v1_api.register(CreateUserResource())


urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    (r'^$', 'touritz_app.views.main'),
    url(r'^logout/$', 'touritz_app.views.logout'),
    url(r'^accounts/profile/$', 'touritz_app.views.profile'),
    url(r'^login/$', 'touritz_app.views.login_user'),
    url(r'^signup/$', 'touritz_app.views.signup'),
    url(r'^tours/$', 'touritz_app.views.tours'),
    url(r'^accounts/profile_photo/$', 'touritz_app.views.profile_photo'),
    url(r'^accounts/password/check_email/$', 'touritz_app.views.check_email'),    
    url(r'^profile/$', 'touritz_app.views.profile'),
    (r'^api/', include(v1_api.urls)),
    url(r'^api/v1/create_user/$', 'touritz_app.views.create_user'),
    url(r'^api/v1/delete_user/$', 'touritz_app.views.delete_user'),  
    url(r'^category/(?P<category_slug>.*)/$', 'touritz_app.views.category'),
    url(r'^tour/(?P<tour_name_slug>.*)/$', 'touritz_app.views.view_tour'),
    url(r'^save-tour/(?P<tour_id>.*)/$', 'touritz_app.views.bookmark_tour'),   
    url(r'^remove-tour/(?P<tour_id>.*)/$', 'touritz_app.views.remove_tour'),
    url(r'^profile/my-tours/$', 'touritz_app.views.my_tours'),
    url(r'^profile/create-tour/$', 'touritz_app.views.create_tour'),
    url(r'^profile/edit-tour/(?P<tour_id>.*)/$', 'touritz_app.views.edit_tour'),
    url(r'^profile/remove-tour/$', 'touritz_app.views.remove_actual_tour'),
    url(r'^profile/edit-actual-tour/$', 'touritz_app.views.edit_actual_tour'),
    url(r'^profile/remove-saved-tour/$', 'touritz_app.views.remove_saved_tour'),
    url(r'^profile/create-actual-tour/$', 'touritz_app.views.create_actual_tour'),
    url(r'^profile/find-location-results/$', 'touritz_app.views.find_location_results'),
    url(r'^profile/find-location-results-tour-point/$', 'touritz_app.views.find_location_results_tour_point'),
    url(r'^profile/create-tour-point/$', 'touritz_app.views.create_actual_tour_point'),
    url(r'^profile/update-tour-point/$', 'touritz_app.views.update_tour_point'),
    url(r'^profile/remove-existing-tour-point/$', 'touritz_app.views.remove_existing_tour_point'),
    url(r'^profile/update-tour-cover-photo/$', 'touritz_app.views.update_tour_cover_photo'),
    url(r'^profile/update-tour-point-cover-photo/$', 'touritz_app.views.update_tour_point_cover_photo'),
    url(r'^profile/edit-tour-points/(?P<tour_id>.*)/$', 'touritz_app.views.edit_tour_points'),                      
    url(r'^profile/preview-submit/(?P<tour_id>.*)/$', 'touritz_app.views.preview_submit'),
    url(r'^profile/new-panoramic/$', 'touritz_app.views.new_panoramic'),
    url(r'^profile/crop-panoramic/$', 'touritz_app.views.crop_panoramic'),
    url(r'^profile/publish-tour/$', 'touritz_app.views.publish_tour'),
    url(r'^custom-admin/$', 'touritz_app.views.custom_admin'),
    url(r'^custom-pro/$', 'touritz_app.views.custom_pro'),  
    url(r'^search/$', 'touritz_app.views.search_titles'),
    url(r'^search/$', include('haystack.urls')),

)
