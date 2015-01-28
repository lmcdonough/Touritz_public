import sys
from django.shortcuts import render_to_response, render, get_object_or_404
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.template import Context, Template, RequestContext
from django.template import resolve_variable
from django import forms
from  touritz_app.models import *
from touritz_app.forms import *
from django.contrib.auth import authenticate, login
from PIL import Image
import uuid
import os, mimetypes
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.contrib.auth import authenticate
import json
import urllib2
from django.http import HttpResponse
import uuid
from amazon_s3_tools import *
import glob
import re
import crop_images_tools
from haystack import *
from haystack.query import *
from django.contrib.auth.decorators import login_required
from urllib import urlretrieve
import time
from zencoder import Zencoder
from django.contrib.admin.views.decorators import staff_member_required

def main(request):
    user = request.user
    featured_categories = TourCategories.objects.filter(featured=True, order__isnull=False).order_by('order')[:8]
    featured_categories_list = TourCategories.objects.filter(featured=True, order__isnull=False).order_by('order').values_list('category_name')[:8]
    
    category_1 = featured_categories[0]
    category_1_id = category_1.category_name
    
    category_2 = featured_categories[1]
    category_2_id = category_2.category_name    

    category_3 = featured_categories[2]
    category_3_id = category_3.category_name

    category_4 = featured_categories[3]
    category_4_id = category_4.category_name

    category_5 = featured_categories[4]
    category_5_id = category_5.category_name

    category_6 = featured_categories[5]
    category_6_id = category_6.category_name    

    category_7 = featured_categories[6]
    category_7_id = category_7.category_name

    category_8 = featured_categories[7]
    category_8_id = category_8.category_name
    
    category_1_tours = CategoryAssociations.objects.filter(category_id_num__featured=True, category_id_num__category_name=category_1_id, tour_id_num__featured=True, tour_id_num__published=True)[:4]
    category_2_tours = CategoryAssociations.objects.filter(category_id_num__featured=True, category_id_num__category_name=category_2_id, tour_id_num__featured=True, tour_id_num__published=True)[:4]
    category_3_tours = CategoryAssociations.objects.filter(category_id_num__featured=True, category_id_num__category_name=category_3_id, tour_id_num__featured=True, tour_id_num__published=True)[:4]
    category_4_tours = CategoryAssociations.objects.filter(category_id_num__featured=True, category_id_num__category_name=category_4_id, tour_id_num__featured=True, tour_id_num__published=True)[:4]
    category_5_tours = CategoryAssociations.objects.filter(category_id_num__featured=True, category_id_num__category_name=category_5_id, tour_id_num__featured=True, tour_id_num__published=True)[:4]
    category_6_tours = CategoryAssociations.objects.filter(category_id_num__featured=True, category_id_num__category_name=category_6_id, tour_id_num__featured=True, tour_id_num__published=True)[:4]
    category_7_tours = CategoryAssociations.objects.filter(category_id_num__featured=True, category_id_num__category_name=category_7_id, tour_id_num__featured=True, tour_id_num__published=True)[:4]
    category_8_tours = CategoryAssociations.objects.filter(category_id_num__featured=True, category_id_num__category_name=category_8_id, tour_id_num__featured=True, tour_id_num__published=True)[:4]
  

    main_tours = Tours.objects.filter(front_page=True, published=True)
    #The primary key is not the user id so make sure to take care of that when creating tours
          
    args = {}
    args['user'] = user
    args['main_tours'] = main_tours
    args['featured_categories'] = featured_categories
    args['category_1_tours'] = category_1_tours
    args['category_2_tours'] = category_2_tours
    args['category_3_tours'] = category_3_tours
    args['category_4_tours'] = category_4_tours
    args['category_5_tours'] = category_5_tours
    args['category_6_tours'] = category_6_tours
    args['category_7_tours'] = category_7_tours
    args['category_8_tours'] = category_8_tours
    args.update(csrf(request))
    return render_to_response('index.html', args)

def logout(request): 
    auth.logout(request)
    return HttpResponseRedirect('/')

def login_user(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        user_info =  request.POST
        username = user_info['username']
        password = user_info['password']
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        print(user)
        data = {}
        if user is not None:
            # the password verified for the user
            print('password worked')
            if user.is_active == True:
                print('active user')
                args['active_user'] = ''                
                login(request, user)
                args['user'] =  user                
                #print(user.username)                
                data['success'] = '1'
                return HttpResponse(json.dumps(data), mimetype='application/json')
                #return HttpResponseRedirect('/', args)
            else:
                data['disabled'] = '1'
                print('disabled')                
                #args['disabled'] = 'disabled'                
                return HttpResponse(json.dumps(data), mimetype='application/json')
        else:            
            # the authentication system was unable to verify the username and password
            args['incorrect'] = 'incorrect'
            data['incorrect'] = '1'
            #print('incorrect')
            return HttpResponse(json.dumps(data), mimetype='application/json')
##            return render(request, 'login_context.html', args)   

def signup(request):
    args = {}
    data = {}
    args.update(csrf(request))
    if request.method == 'POST':
        new_user = request.POST
        username = new_user['username']
        email = new_user['email']
        password_text = new_user['password1']
        characters = '1234567890-_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if User.objects.filter(username=username).exists():
              data['username'] = 1
              data['email'] = 0
              data['invalid'] = 0
              return HttpResponse(json.dumps(data), mimetype='application/json')  
        elif User.objects.filter(email=email).exists():
            data['username'] = 0
            data['email'] = 1
            data['invalid'] = 0
            return HttpResponse(json.dumps(data), mimetype='application/json')
        elif not all((c in characters) for c in username):
            data['username'] = 0
            data['email'] = 0
            data['invalid'] = 1            
            return HttpResponse(json.dumps(data), mimetype='application/json')
        else:           
            user = User.objects.create_user(username, email, password_text)
            user = authenticate(username=username, password=password_text)
            args['new_user_created'] = 'success'
            login(request, user)
            args['user'] = user        
            return HttpResponseRedirect('/', args)

@login_required
def profile(request):
    args = {}
    args.update(csrf(request))
    featured_categories = TourCategories.objects.filter(featured=True).order_by('order')[:8]
    if request.method == 'POST':
        user = request.user
        profile = user.profile

        new_info = request.POST
        name = new_info['full_name']
##        username = new_info['user_name']
        user_bio = new_info['user_bio']
        user_home_city = new_info['user_home_city']
        user_zipcode = new_info['user_zipcode']
        user_website = new_info['user_website']
        user_interests = new_info['user_interests']


##        user.username = username
        user.save()
        profile.user_bio = user_bio
        profile.full_name = name
        profile.zip_code = user_zipcode
        profile.website = user_website
        profile.interests = user_interests
        profile.user_home_city = user_home_city
        existing = user.profile
        profile.user_photo = existing.user_photo
        profile.save()

        user = request.user
        profile = user.profile

        args['profile'] = profile
        args['user'] = user
        args['featured_categories'] = featured_categories
        return render(request, 'profile_2.html', args)
    else:
        user = request.user
        profile = user.profile
        args['featured_categories'] = featured_categories
        args['profile'] = profile
        args['user'] = user
        return render(request, 'profile_2.html', args)

def check_email(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        verify_email =request.POST
        test_email = verify_email['email']        
        if User.objects.filter(email=test_email).exists():
            args['send'] = 'send'
        else:
            args['send']  = 'invalid'
    return render(request, 'verify_email_context.html', args)
        
def tours(request):
    user = request.user
    args = {}
    args['user'] = user   
    args.update(csrf(request))
    return render_to_response('tours_dashboard.html', args)

@login_required
def profile_photo(request):
    user = request.user
    profile = user.profile
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':

        #delete old image
        if profile.user_photo != '':          
            image = profile.user_photo
            image_file = image.split('/')[-1:][0]
            delete_from_s3('touritz_static/images', image_file)
            profile.user_photo = ''
            profile.save()

        try:            
            tour_photo =request.FILES['file_upload_hidden']
            cover_photo = Image.open(tour_photo)        
            filetype = str(request.FILES['file_upload_hidden'].name[-4:])
            new_id =  str(uuid.uuid4()) + filetype      
            new_name = ('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/' + new_id)
            cover_photo.save(new_name)

            new_name_for_s3 = 'https://s3.amazonaws.com/touritz_static/images/' + new_id
            save_to_s3(new_name, 'touritz_static/images', new_id)
            
            existing = user.profile
            profile.user_photo = new_name_for_s3
            profile.email_verified = existing.email_verified
            profile.user_name = existing.user_name
            profile.full_name = existing.full_name
            profile.user_bio = existing.user_bio
            profile.user_home_city = existing.user_home_city
            profile.zip_code = existing.zip_code
            profile.website = existing.website
            profile.interests = existing.interests            
            profile.save()
        except:
            pass

    return HttpResponseRedirect('/accounts/profile/', args)

def category(request, category_slug):
    user = request.user
    featured_categories = TourCategories.objects.filter(featured=True).order_by('order')[:8]
    category = TourCategories.objects.get(category_slug=category_slug)
    category_id = category.category_id
    tours = CategoryAssociations.objects.filter(category_id_num=category_id, tour_id_num__published=True)
    
    args = {}

    args['user'] = user  
    args['category'] = category
    args['featured_categories'] = featured_categories
    args['tours'] = tours
    #args['featured_categories'] = featured_categories
    args.update(csrf(request))
    return render_to_response('category.html', args)


def view_tour(request, tour_name_slug):
    args = {}
    user = request.user
    featured_categories = TourCategories.objects.filter(featured=True).order_by('order')[:8]
    tour_record = Tours.objects.get(tour_name_slug=tour_name_slug)
    tour_id = tour_record.tour_id
    tour = Tours.objects.get(tour_id=tour_id)
    tour_points = TourAndPointAssociations.objects.filter(tour_id_num=tour_id)           
    try:
        bookmarked = BookMarks.objects.get(tour_id_num=tour, user_id_num=user)
        args['bookmarked'] = bookmarked
    except:
        pass

    args['og_meta'] = tour   
    args['user'] = user  
    args['tour'] = tour
    args['tour_points'] = tour_points
    args['featured_categories'] = featured_categories
    args.update(csrf(request))
    return render_to_response('view_tour.html', args)

def bookmark_tour(request, tour_id):
    user = request.user    
    user = User.objects.get(id=user.id)
    if request.method == 'POST':
        bookmark =request.POST
        tour = bookmark['tour']        
        tour = Tours.objects.get(tour_id = tour_id)
        new_bookmark = BookMarks()
        new_bookmark.tour_id_num = tour
        new_bookmark.user_id_num = user
        new_bookmark.save()        

    args = {}
    args['user'] = user 
    args.update(csrf(request))
    args['success'] = 'success'
    return render_to_response('view_tour.html', args)

def remove_tour(request, tour_id):
    user = request.user    
    user = User.objects.get(id=user.id)
    if request.method == 'POST':
        bookmark =request.POST
        tour = bookmark['tour']        
        tour = Tours.objects.get(tour_id = tour_id)
        new_bookmark = BookMarks.objects.get(tour_id_num=tour, user_id_num=user)
        new_bookmark.delete()     

    args = {}
    args['user'] = user 
    args.update(csrf(request))
    args['success'] = 'success'
    return render_to_response('view_tour.html', args)    

@login_required
def my_tours(request):    
    user = request.user
    featured_categories = TourCategories.objects.filter(featured=True).order_by('order')[:8]
    tours = BookMarks.objects.filter(user_id_num=user)

    if user.is_superuser:
        created_tours = Tours.objects.all()
    else:
        created_tours = Tours.objects.filter(created_by=user)
        
    
    args = {}
    args['created_tours'] = created_tours
    args['tours'] = tours
    args['featured_categories'] = featured_categories
    args['user'] = user 
    args.update(csrf(request))
    return render_to_response('my_tours.html', args)

def remove_saved_tour(request):
    user = request.user
    data = {}
    data['results'] = {}
    data['result'] = 1
    if request.method == 'POST':
        bookmark =request.POST
        tour_id = bookmark['tour_id']
        remove_these = BookMarks.objects.get(user_id_num=user, tour_id_num__tour_id=tour_id).delete()
        return HttpResponse(json.dumps(data), mimetype='application/json')  
        

    

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        new_user = simplejson.loads(request.body)
        username = new_user['username']
        email = new_user['email']
        password = new_user['password']
    args = {}
    if User.objects.filter(username=username).count():
        args['user_message'] = 'username already exists'
        return render_to_response('create_user_response.html', args)
    elif User.objects.filter(email=email).count():
        args['email_message'] = 'user with that email address already exists.'
        return render_to_response('create_user_response.html', args)
    else:
        args['success'] = 'user created.'
##        user = User.objects.create_user(username, email, password)
##        user.save()
        return render_to_response('create_user_response.html', args)

@csrf_exempt
def delete_user(request):
    args = {}
    if request.method == 'POST':
        new_user = simplejson.loads(request.body)
        username = new_user['username']
        email = new_user['email']
        password = new_user['password']
        user = authenticate(username=username, password=password)    
        if user is not None:
            user.is_active = False
            user.save()
            args['user_message'] = 'user has been removed.'            
        else:
            args['incorrect'] = 'incorrect username and/or password.'
        return render_to_response('delete_user_response.html', args)

@login_required
def create_tour(request):
    user = request.user
    profile = user.profile
    args = {}
    args.update(csrf(request))
    featured_categories = TourCategories.objects.filter(featured=True).order_by('order')[:8]
    all_categories = TourCategories.objects.all().order_by('category_name')
    args['featured_categories'] = featured_categories
    args['all_categories'] = all_categories
    print(all_categories)
    if not user.is_authenticated():
        return HttpResponseRedirect('/', args)
    else:
        args['user'] = user
        args.update(csrf(request))
    return render_to_response('create_tour.html', args)

@login_required
def edit_tour(request, tour_id):
    user = request.user
    args = {}
    args.update(csrf(request))
    featured_categories = TourCategories.objects.filter(featured=True).order_by('order')[:8]
    
    if not user.is_authenticated():
        return HttpResponseRedirect('/', args)
    else:
        user = request.user
        profile = user.profile
        args = {}
        args.update(csrf(request))
        tour = Tours.objects.get(tour_id=tour_id)
        tour_id = tour.tour_id      
        tour_points = TourAndPointAssociations.objects.filter(tour_id_num=tour_id)
        tour_point_values = TourPoints.objects.filter(tour_point_id=tour_id).values_list('tour_point_id')  
        tour_point_media_items = MediaAssociations.objects.filter(tour_point_id_num__in=tour_point_values)
        all_categories = TourCategories.objects.all()
        chosen_categories = CategoryAssociations.objects.filter(tour_id_num__tour_id=tour_id)
        args['chosen_categories'] = chosen_categories
        args['all_categories'] = all_categories
        args['featured_categories'] = featured_categories
        args['tour_point_media_items'] = tour_point_media_items
        args['existing_tour'] = tour
        args['existing_tour_points'] = tour_points
        args['user'] = user
    return render_to_response('create_tour.html', args)

@login_required
def create_actual_tour(request):
    user = request.user       
    data = {}
    data['results'] = {}    
  
    if request.method == 'POST':
        if user.is_authenticated():
            tour =request.POST
            title = tour['title']
            duration = tour['duration']
            if duration == '':
                duration = 0
            description = tour['description']
##            region = tour['state_input']
            website_original = str(tour['website_input'])
            length = len(website_original)
            if length > 5:
                website_strip = website_original.replace('http://', '')
                if website_strip[:4] != 'www.':
                    website = 'www.' + website_strip
                else:
                    website = website_strip
            else:
                website = None
            
            phone = tour['phone_number_input']
            location = tour['city']
            tour_created_by_display = tour['tour_created_by_input']
            tour_created_by_description = tour['tour_guide_description']            
            sunday_open_time = tour['sunday_open_time']
            sunday_close_time = tour['sunday_close_time']
            monday_open_time = tour['monday_open_time']
            monday_close_time = tour['monday_close_time']
            tuesday_open_time = tour['tuesday_open_time']
            tuesday_close_time = tour['tuesday_close_time']
            wednesday_open_time = tour['wednesday_open_time']
            wednesday_close_time = tour['wednesday_close_time']
            thursday_open_time = tour['thursday_open_time']
            thursday_close_time = tour['thursday_close_time']
            friday_open_time = tour['friday_open_time']
            friday_close_time = tour['friday_close_time']
            saturday_open_time = tour['saturday_open_time']
            saturday_close_time = tour['saturday_close_time']
            additional_tour_info = tour['additional_tour_info']
            photo_orientation = tour['photo_orientation']

            
            if tour['tour_id'] != '':
                new_tour = Tours.objects.get(tour_id= tour['tour_id'])
            elif tour['tour_id'] == '' and Tours.objects.filter(created_by=user, tour_name=title).exists():
                data['result'] = 2
                data['message'] = "Already Exists."
                return HttpResponse(json.dumps(data), mimetype='application/json')
            else:                
                new_tour = Tours()

            if request.POST['temp_pan_id'] != '':
                print('ran code')                
                pan_id = request.POST['temp_pan_id']
                temp_pan = TemporaryPanoramic.objects.get(photo_id=pan_id)
                new_tour.photo_panoramic = temp_pan.photo_panoramic
                print(new_tour.photo_panoramic)
                new_tour.photo_panoramic_cropped = temp_pan.photo_panoramic
                if temp_pan.photo_panoramic_cropped != None:
                    new_tour.photo_panoramic_cropped = temp_pan.photo_panoramic_cropped
                    
                new_tour.image_250_url = crop_images_tools.layout_1(temp_pan.photo_panoramic_cropped) 
                new_tour.image_200_url = crop_images_tools.layout_2(temp_pan.photo_panoramic_cropped) 
                new_tour.image_320_url = crop_images_tools.layout_3(temp_pan.photo_panoramic_cropped) 
                new_tour.image_640_url = crop_images_tools.layout_4(temp_pan.photo_panoramic_cropped) 

            if photo_orientation == '1':
                new_tour.cover_photo_orientation = True               
            if photo_orientation == '0':
                new_tour.cover_photo_orientation = False
             
            new_tour.official_website = website
            new_tour.sunday_open  = sunday_open_time
            new_tour.sunday_close = sunday_close_time
            new_tour.monday_open  = monday_open_time
            new_tour.monday_close = monday_close_time
            new_tour.tuesday_open  = tuesday_open_time
            new_tour.tuesday_close = tuesday_close_time
            new_tour.wednesday_open  = wednesday_open_time
            new_tour.wednesday_close = wednesday_close_time
            new_tour.thursday_open  = thursday_open_time
            new_tour.thursday_close = thursday_close_time
            new_tour.friday_open  = friday_open_time
            new_tour.friday_close = friday_close_time
            new_tour.saturday_open  = saturday_open_time
            new_tour.saturday_close = saturday_close_time
            new_tour.tour_created_by_display = tour_created_by_display
            new_tour.telephone_number = phone
            new_tour.tour_name = title
            new_tour.city = location
            new_tour.time = duration
            new_tour.description = description
            new_tour.tour_created_by_display_description = tour_created_by_description
          
            new_tour.created_by = user
            user_profile = UserProfile.objects.get(user=user)
            new_tour.created_by_profile = user_profile
            new_tour.additional_info_hours = additional_tour_info

            if tour['remove_photo_top_left_check'] == 'remove':
                #delete old images from s3
                image = new_tour.photo_top_left 
                image_file = image.split('/')[-1:][0]
                delete_from_s3('touritz_static/images', image_file)
                new_tour.photo_top_left = None
            if tour['remove_photo_bottom_left_check'] == 'remove':
                print('deleting bottom left')
                #delete old images from s3
                image = new_tour.photo_bottom_left 
                image_file = image.split('/')[-1:][0]
                delete_from_s3('touritz_static/images', image_file)
                new_tour.photo_bottom_left = None
            if tour['remove_photo_center_check'] == 'remove':
                #delete old images from s3
                image = new_tour.photo_center 
                image_file = image.split('/')[-1:][0]
                delete_from_s3('touritz_static/images', image_file)
                
                #delete old image from s3
                image = new_tour.image_250_url
                image_file = image.split('/')[-1:][0]
                delete_from_s3('touritz_static/images', image_file)

                #delete old image from s3
                image = new_tour.image_200_url
                image_file = image.split('/')[-1:][0]
                delete_from_s3('touritz_static/images', image_file)

                #delete old image from s3
                image = new_tour.image_320_url
                image_file = image.split('/')[-1:][0]
                delete_from_s3('touritz_static/images', image_file)

                #delete old image from s3
                image = new_tour.image_640_url
                image_file = image.split('/')[-1:][0]
                delete_from_s3('touritz_static/images', image_file)
                               
                new_tour.photo_center = None                
            if tour['remove_photo_top_right_check'] == 'remove':
                #delete old images from s3
                image = new_tour.photo_top_right 
                image_file = image.split('/')[-1:][0]
                delete_from_s3('touritz_static/images', image_file)
                new_tour.photo_top_right = None                
            if tour['remove_photo_bottom_right_check'] == 'remove':
                #delete old images from s3
                image = new_tour.photo_bottom_right 
                image_file = image.split('/')[-1:][0]
                delete_from_s3('touritz_static/images', image_file)
                new_tour.photo_bottom_right = None                
            if tour['remove_photo_panoramic_check'] == 'remove':
                #delete old images from s3
                image = new_tour.photo_panoramic 
                image_file = image.split('/')[-1:][0]
                delete_from_s3('touritz_static/images', image_file)        
                new_tour.photo_panoramic = None
            if tour['remove_photo_panoramic_check'] == 'remove':
                #delete old images from s3
                image = new_tour.photo_panoramic_cropped 
                image_file = image.split('/')[-1:][0]
                delete_from_s3('touritz_static/images', image_file)                        
                new_tour.photo_panoramic_cropped = None

            
            if Tours.objects.filter(tour_name = title).exists():
                new_slug_concat_sub = title + '-' + user.username
                new_slug_concat = new_slug_concat_sub.replace("'", '')
                new_slug = re.sub('[^0-9a-zA-Z]+', '-', new_slug_concat)                
                if new_slug.startswith('-'):
                    new_slug = new_slug[1:]
                if new_slug.endswith('-'):
                    new_slug = new_slug[:-1]
                new_tour.tour_name_slug = new_slug
                new_tour.save()                    
            else:
                new_title = title.replace("'", '')
                new_slug = re.sub('[^0-9a-zA-Z]+', '-', new_title)
                new_tour.tour_name_slug = new_slug
                if new_slug.startswith('-'):
                    new_slug = new_slug[1:]
                if new_slug.endswith('-'):
                    new_slug = new_slug[:-1]
                new_tour.tour_name_slug = new_slug
                new_tour.save()                      

                
            category_1 = 0
            category_2 = 0
            category_3 = 0
            existing_tour_id = 0
            
            if request.POST['chosen_category_1'] != 'undefined':
                category_1 = tour['chosen_category_1']

            if request.POST['chosen_category_2'] != 'undefined':
                category_2 = tour['chosen_category_2']

            if request.POST['chosen_category_3'] != 'undefined':
                category_3 = tour['chosen_category_3']
                
            if request.POST['tour_id'] != '':
                existing_tour_id = tour['tour_id']                

            if existing_tour_id != 0:
                CategoryAssociations.objects.filter(tour_id_num__tour_id=existing_tour_id).delete()
                
            try:
                if request.FILES['tour_photo']:
                    tour_photo =request.FILES['tour_photo']
                    filetype = str(request.FILES['tour_photo'].name[-4:])
                    cover_photo = Image.open(tour_photo)          
                    new_id =  str(uuid.uuid4()) + filetype    
                    new_name = ('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/' + new_id)
                    cover_photo.save(new_name)

                    new_name_for_s3 = 'https://s3.amazonaws.com/touritz_static/images/' + new_id
                    save_to_s3(new_name, 'touritz_static/images', new_id)

                    #delete old images from s3
                    image = new_tour.cover_image_url
                    image_file = image.split('/')[-1:][0]
                    delete_from_s3('touritz_static/images', image_file)

                    image = new_tour.image_250_url
                    image_file = image.split('/')[-1:][0]
                    delete_from_s3('touritz_static/images', image_file)

                    image = new_tour.image_200_url
                    image_file = image.split('/')[-1:][0]
                    delete_from_s3('touritz_static/images', image_file)

                    image = new_tour.image_320_url
                    image_file = image.split('/')[-1:][0]
                    delete_from_s3('touritz_static/images', image_file)                    

                    image = new_tour.image_640_url
                    image_file = image.split('/')[-1:][0]
                    delete_from_s3('touritz_static/images', image_file)
                    
                    new_tour.cover_image_url = new_name_for_s3                   
                    new_photo_url = new_tour.cover_image_url
                    ##additional sizes

                    new_tour.image_250_url = crop_images_tools.layout_1(new_name_for_s3) 
                    new_tour.image_200_url = crop_images_tools.layout_2(new_name_for_s3) 
                    new_tour.image_320_url = crop_images_tools.layout_3(new_name_for_s3) 
                    new_tour.image_640_url = crop_images_tools.layout_4(new_name_for_s3) 
                    new_tour.save()

                
                    files = glob.glob('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/*')
                    for f in files:
                        os.remove(f)
            except:
                new_tour.cover_image_url = tour['tour_cover_image_url']
                new_tour.save()
                new_photo_url = new_tour.cover_image_url

            try:
                if request.FILES['tour_guide_photo_input']:
                    tour_guide_file =request.FILES['tour_guide_photo_input']
                    filetype = str(request.FILES['tour_guide_photo_input'].name[-4:])
                    tour_guide_photo = Image.open(tour_guide_file)          
                    new_id =  str(uuid.uuid4()) + filetype    
                    new_name = ('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/' + new_id)
                    tour_guide_photo.save(new_name)

                    new_name_for_s3 = 'https://s3.amazonaws.com/touritz_static/images/' + new_id
                    save_to_s3(new_name, 'touritz_static/images', new_id)

                    #delete old image from s3
                    if new_tour.tour_created_by_display_image:
                        image = new_tour.tour_created_by_display_image
                        image_file = image.split('/')[-1:][0]
                        delete_from_s3('touritz_static/images', image_file)
                    
                    new_tour.tour_created_by_display_image = new_name_for_s3                   
                    #new_photo_url = new_tour.tour_created_by_display_image 
                    new_tour.save()
                
                    files = glob.glob('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/*')
                    for f in files:
                        os.remove(f)
            except:
                pass

            try:               
                if request.FILES['photo_top_left']:
                    photo_file =request.FILES['photo_top_left']
                    filetype = str(request.FILES['photo_top_left'].name[-4:])
                    new_photo = Image.open(photo_file)          
                    new_id =  str(uuid.uuid4()) + filetype    
                    new_name = ('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/' + new_id)
                    new_photo.save(new_name)

                    new_name_for_s3 = 'https://s3.amazonaws.com/touritz_static/images/' + new_id
                    save_to_s3(new_name, 'touritz_static/images', new_id)
                    
                    new_tour.photo_top_left = new_name_for_s3                   
                    #new_photo_url = new_tour.tour_created_by_display_image 
                    new_tour.save()

                
                    files = glob.glob('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/*')
                    for f in files:
                        os.remove(f)
            except:
                pass  

            try:
                if request.FILES['photo_bottom_left']:
                    photo_file =request.FILES['photo_bottom_left']
                    filetype = str(request.FILES['photo_bottom_left'].name[-4:])
                    new_photo = Image.open(photo_file)          
                    new_id =  str(uuid.uuid4()) + filetype    
                    new_name = ('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/' + new_id)
                    new_photo.save(new_name)

                    new_name_for_s3 = 'https://s3.amazonaws.com/touritz_static/images/' + new_id
                    save_to_s3(new_name, 'touritz_static/images', new_id)

                    new_tour.photo_bottom_left = new_name_for_s3                   
                   
                    new_tour.save()

                
                    files = glob.glob('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/*')
                    for f in files:
                        os.remove(f)
            except:
                pass

            try:
                if request.FILES['photo_center']:
                    photo_file =request.FILES['photo_center']
                    filetype = str(request.FILES['photo_center'].name[-4:])
                    new_photo = Image.open(photo_file)          
                    new_id =  str(uuid.uuid4()) + filetype    
                    new_name = ('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/' + new_id)
                    new_photo.save(new_name)

                    new_name_for_s3 = 'https://s3.amazonaws.com/touritz_static/images/' + new_id
                    save_to_s3(new_name, 'touritz_static/images', new_id)
                    
                    new_tour.photo_center = new_name_for_s3                   
                   
                    new_tour.save()
              
                    new_tour.image_250_url = crop_images_tools.layout_1(new_name_for_s3) 
                    new_tour.image_200_url = crop_images_tools.layout_2(new_name_for_s3) 
                    new_tour.image_320_url = crop_images_tools.layout_3(new_name_for_s3) 
                    new_tour.image_640_url = crop_images_tools.layout_4(new_name_for_s3) 
                    new_tour.save()
                
                    files = glob.glob('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/*')
                    for f in files:
                        os.remove(f)
            except:
                pass

            try:
                if request.FILES['photo_top_right']:
                    photo_file =request.FILES['photo_top_right']
                    filetype = str(request.FILES['photo_top_right'].name[-4:])
                    new_photo = Image.open(photo_file)          
                    new_id =  str(uuid.uuid4()) + filetype    
                    new_name = ('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/' + new_id)
                    new_photo.save(new_name)

                    new_name_for_s3 = 'https://s3.amazonaws.com/touritz_static/images/' + new_id
                    save_to_s3(new_name, 'touritz_static/images', new_id)
                    
                    new_tour.photo_top_right = new_name_for_s3                   
                    #new_photo_url = new_tour.tour_created_by_display_image 
                    new_tour.save()
                
                    files = glob.glob('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/*')
                    for f in files:
                        os.remove(f)
            except:
                pass

            try:
                if request.FILES['photo_bottom_right']:
                    photo_file =request.FILES['photo_bottom_right']
                    filetype = str(request.FILES['photo_bottom_right'].name[-4:])
                    new_photo = Image.open(photo_file)          
                    new_id =  str(uuid.uuid4()) + filetype    
                    new_name = ('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/' + new_id)
                    new_photo.save(new_name)

                    new_name_for_s3 = 'https://s3.amazonaws.com/touritz_static/images/' + new_id
                    save_to_s3(new_name, 'touritz_static/images', new_id)
                    
                    new_tour.photo_bottom_right = new_name_for_s3                   
                    #new_photo_url = new_tour.tour_created_by_display_image 
                    new_tour.save()

                
                    files = glob.glob('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/*')
                    for f in files:
                        os.remove(f)
            except:
                pass

            try:
                if request.FILES['panoramic_photo']:
                    photo_file =request.FILES['panoramic_photo']
                    filetype = str(request.FILES['panoramic_photo'].name[-4:])
                    new_photo = Image.open(photo_file)          
                    new_id =  str(uuid.uuid4()) + filetype    
                    new_name = ('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/' + new_id)
                    new_photo.save(new_name)

                    new_name_for_s3 = 'https://s3.amazonaws.com/touritz_static/images/' + new_id
                    save_to_s3(new_name, 'touritz_static/images', new_id)
                    
                    new_tour.photo_panoramic = new_name_for_s3                   
                    #new_photo_url = new_tour.tour_created_by_display_image 
                    new_tour.save()
                
                    files = glob.glob('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/*')
                    for f in files:
                        os.remove(f)
            except:
                pass    
            
            if category_1 != 0:
                add_category_1 = CategoryAssociations()
                category_to_add = TourCategories.objects.get(category_id=category_1)
                add_category_1.tour_id_num = new_tour
                add_category_1.category_id_num = category_to_add
                add_category_1.save()
            if category_2 != 0:
                print(category_2)
                add_category_2 = CategoryAssociations()
                category_to_add = TourCategories.objects.get(category_id=category_2)                
                add_category_2.tour_id_num = new_tour            
                add_category_2.category_id_num = category_to_add
                add_category_2.save()
            if category_3 != 0:
                add_category_3 = CategoryAssociations()
                category_to_add = TourCategories.objects.get(category_id=category_3)                
                add_category_3.tour_id_num = new_tour            
                add_category_3.category_id_num = category_to_add
                add_category_3.save()

            if photo_orientation == '1':
                new_tour.cover_photo_orientation = True
                new_tour.image_250_url = crop_images_tools.layout_1(new_tour.photo_panoramic_cropped) 
                new_tour.image_200_url = crop_images_tools.layout_2(new_tour.photo_panoramic_cropped) 
                new_tour.image_320_url = crop_images_tools.layout_3(new_tour.photo_panoramic_cropped) 
                new_tour.image_640_url = crop_images_tools.layout_4(new_tour.photo_panoramic_cropped)                
            if photo_orientation == '0':
                new_tour.cover_photo_orientation = False
                new_tour.image_250_url = crop_images_tools.layout_1(new_tour.photo_center) 
                new_tour.image_200_url = crop_images_tools.layout_2(new_tour.photo_center) 
                new_tour.image_320_url = crop_images_tools.layout_3(new_tour.photo_center) 
                new_tour.image_640_url = crop_images_tools.layout_4(new_tour.photo_center) 

            new_tour.save()
            print('went through code')
            data['tour_cover_photo'] = new_photo_url            
            data['tour_name'] = new_tour.tour_name
            data['tour_id'] = new_tour.tour_id
            data['result'] = 1
            new_url = '/profile/edit-tour-points/' + str(new_tour.tour_id)
            print(new_url)
            data['new_url'] = new_url
            
            return HttpResponse(json.dumps(data), mimetype='application/json')
        else:
            data['result'] = 0
            data['message'] = "Error."
            return HttpResponse(json.dumps(data), mimetype='application/json')

@login_required
def edit_tour_points(request, tour_id):
    user = request.user
    args = {}
    args.update(csrf(request))
  
    args['user'] = user
    featured_categories = TourCategories.objects.filter(featured=True).order_by('order')[:8]
    args['featured_categories'] = featured_categories
    removed = tour_id.split('/')
    corrected = int(removed[0])
    
    tour = Tours.objects.get(tour_id=corrected)
    args['existing_tour'] = tour
    tourpoints = TourAndPointAssociations.objects.filter(tour_id_num=tour)
    args['existing_tour_points'] = tourpoints

    return render_to_response('edit_tour_points.html', args)

@login_required    
def edit_actual_tour(request):
    user = request.user       
    data = {}
    data['results'] = {}    
            
    if request.method == 'POST':
        if user.is_authenticated():
            tour =request.POST
            title = tour['title']
            duration = tour['duration']
            description = tour['description']
            location_comma = tour['city']
            tour_id = tour['tour_id']
            location = location_comma.replace(' ', '').split(',')
            city = location[0]
            new_tour = Tours.objects.get(tour_id=tour_id)
            
            try:
                state = location[1]
                country = location[2]
                new_tour.region = state
                new_tour.country_code = country
            except:
                pass
            
            new_tour.tour_name = title
            new_tour.city = city
            new_tour.time = duration
            new_tour.description = description
            new_tour.created_by = user
            user_profile = UserProfile.objects.get(user=user)
            new_tour.created_by_profile = user_profile
            new_tour.save()
                
            data['tour_name'] = new_tour.tour_name
            data['tour_id'] = new_tour.tour_id
            data['result'] = 1
            return HttpResponse(json.dumps(data), mimetype='application/json')
        else:
            data['result'] = 0
            data['message'] = "Error."
            return HttpResponse(json.dumps(data), mimetype='application/json')            

@login_required
def update_tour_cover_photo(request):
    user = request.user
    data = {}  
    data['results'] = {}  
    if request.method == 'POST':
        if user.is_authenticated():
            photo_post = request.POST            
            tour = photo_post['tour_id']
            tour_photo =request.FILES['tour_photo']
            cover_photo = Image.open(tour_photo)
            filetype = str(request.FILES['tour_photo'].name[-4:])
            new_id =  str(uuid.uuid4()) + filetype      
            new_name = ('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/' + new_id)
            cover_photo.save(new_name)

            changed_tour = Tours.objects.get(tour_id=tour)
            if changed_tour.cover_image_url:                
                delete_from_s3('touritz_static/images', changed_tour.cover_image_url)  

            new_name_for_s3 = 'https://s3.amazonaws.com/touritz_static/images/' + new_id
            save_to_s3(new_name, 'touritz_static/images', new_id)

            #delete old image from s3
            if changed_tour.cover_image_url != '':
                image = changed_tour.cover_image_url
                image_file = image.split('/')[-1:][0]
                delete_from_s3('touritz_static/images', image_file)
                    
            changed_tour.cover_image_url = new_name_for_s3
            changed_tour.save()
            new_photo_url = changed_tour.cover_image_url
            files = glob.glob('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/*')
            for f in files:
                os.remove(f)
            data['tour_cover_photo'] = new_photo_url            
            data['result'] = 1
            return HttpResponse(json.dumps(data), mimetype='application/json')
        else:
            data['result'] = 0
            data['message'] = "Error."
            return HttpResponse(json.dumps(data), mimetype='application/json')     

@login_required
def update_tour_point_cover_photo(request):
    user = request.user
    data = {}  
    data['results'] = {}  
    if request.method == 'POST':
        if user.is_authenticated():
            photo_post = request.POST            
            tour = photo_post['tour_id']
            tour_point = photo_post['point_id']
            point_photo =request.FILES['point_photo']
            cover_photo = Image.open(point_photo)
            filetype = str(request.FILES['point_photo'].name[-4:])
            new_id =  str(uuid.uuid4()) + filetype        
            new_name = ('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/' + new_id)
            cover_photo.save(new_name)

            if TourPoints.objects.get(tour_point_id=tour_point):                
                point_cover_image_url = TourPoints.objects.get(tour_point_id=tour_point)
                if point_cover_image_url:
                    delete_from_s3('touritz_static/images', point_cover_image_url.cover_image_url)  
                new_name_for_s3 = 'https://s3.amazonaws.com/touritz_static/images/' + new_id
                save_to_s3(new_name, 'touritz_static/images', new_id)

                #delete old image from s3
                if point_cover_image_url.cover_image_url != '':
                    image = point_cover_image_url.cover_image_url
                    image_file = image.split('/')[-1:][0]
                    delete_from_s3('touritz_static/images', image_file)
            
                point_cover_image_url.cover_image_url = new_name_for_s3
                point_cover_image_url.save()
                data['tour_point_id'] = point_cover_image_url.tour_point_id
                new_photo_url = point_cover_image_url.cover_image_url
            else:
                new_point = TourPoints()
                new_name_for_s3 = 'https://s3.amazonaws.com/touritz_static/images/' + new_id
                save_to_s3(new_name, 'touritz_static/images', new_id)

                #delete old image from s3
                if new_point.cover_image_url != '':
                    image = new_tour.cover_image_url
                    image_file = image.split('/')[-1:][0]
                    delete_from_s3('touritz_static/images', image_file)
                
                new_point.cover_image_url = new_name_for_s3
                new_point.created_by = user
                user_profile = UserProfile.objects.get(user=user)           
                new_point.save()            

                tour_point_tour = Tours.objects.get(tour_id=tour)
                association = TourAndPointAssociations()
                association.tour_id_num = tour_point_tour
                association.tour_point_id_num = new_point
                association.save()            
                data['tour_point_id'] = new_point.tour_point_id                
                new_photo_url = new_point.cover_image_url

            files = glob.glob('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/*')
            for f in files:
                os.remove(f)
            data['point_cover_photo'] = new_photo_url            
            data['result'] = 1
            return HttpResponse(json.dumps(data), mimetype='application/json')
        else:
            data['result'] = 0
            data['message'] = "Error."
            return HttpResponse(json.dumps(data), mimetype='application/json')

@login_required        
def create_actual_tour_point(request):
    user = request.user       
    data = {}
    data['results'] = {}    
  
    if request.method == 'POST':
        if user.is_authenticated():
            tour_point =request.POST            
            name = tour_point['point_name']
            tour_id = tour_point['tour_id']
            description = tour_point['point_description']
            location = tour_point['point_address']
            latitude = tour_point['latitude']
            longitude = tour_point['longitude']
            website_original = tour_point['website']
            length = len(website_original)
            if length > 5:
                website_strip = website_original.replace('http://', '')
                if website_strip[:4] != 'www.':
                    website = 'www.' + website_strip
                else:
                    website = website_strip
            else:
                website = None
            phone_number = tour_point['phone_number']
            additional_info = tour_point['additional_info']
                        
            #location = location_comma.replace(' ', '').split(',')
            address = location[0]
            tour_point_tour = Tours.objects.get(tour_id=tour_id)
            number_of_points = tour_point_tour.tour_points_number                             
            #video_url = tour_point['add_video_input'].replace('"', '')
            
            
            if tour_point['tour_point_id_holder'] != '':
                new_tour_point = TourPoints.objects.get(tour_point_id=tour_point['tour_point_id_holder'])
            else:
                new_tour_point = TourPoints()

            new_tour_point.title = name
            new_tour_point.description = description
            new_tour_point.additional_info = additional_info
            new_tour_point.telephone_number = phone_number
            new_tour_point.official_website = website            
            if tour_point['remove_existing_video_input'] == 1:                
                new_tour_point.video_url = ''
                new_tour_point.video_file = ''
            try:
                new_tour_point.address_1 = location
            except:
                pass
            
            try:
                if tour_point['remove_additional_image_1_input'] == '1':
                    #delete old image from s3
                    image = new_tour_point.image_1_url
                    image_file = image.split('/')[-1:][0]
                    delete_from_s3('touritz_static/images', image_file)
                    new_tour_point.image_1_url = None
            except:
                pass
            try:
                if tour_point['remove_additional_image_2_input'] == '1':
                    #delete old image from s3
                    image = new_tour_point.image_2_url
                    image_file = image.split('/')[-1:][0]
                    delete_from_s3('touritz_static/images', image_file)
                    new_tour_point.image_2_url = None
            except:
                pass
            try:
                if tour_point['remove_additional_image_3_input'] == '1':
                    #delete old image from s3
                    image = new_tour_point.image_3_url
                    image_file = image.split('/')[-1:][0]
                    delete_from_s3('touritz_static/images', image_file)
                    new_tour_point.image_3_url = None
            except:
                pass
            try:
                if tour_point['remove_additional_image_4_input'] == '1':
                    #delete old image from s3
                    image = new_tour_point.image_4_url
                    image_file = image.split('/')[-1:][0]
                    delete_from_s3('touritz_static/images', image_file)
                    new_tour_point.image_4_url = None
            except:
                pass
            try:
                if tour_point['remove_additional_image_5_input'] == '1':
                    #delete old image from s3
                    image = new_tour_point.image_5_url
                    image_file = image.split('/')[-1:][0]
                    delete_from_s3('touritz_static/images', image_file)
                    new_tour_point.image_5_url = None
            except:
                pass
            try:
                if tour_point['remove_cover_image_input'] == '1':
                    #delete old image from s3
                    image = new_tour_point.cover_image_url
                    image_file = image.split('/')[-1:][0]
                    delete_from_s3('touritz_static/images', image_file)
                    new_tour_point.cover_image_url = None
            except:
                pass
            try:
                if tour_point['remove_existing_audio_input'] == '1':
                    #delete old image from s3
                    image = new_tour_point.audio_url
                    image_file = image.split('/')[-1:][0]
                    delete_from_s3('touritz_static/audio', image_file)
                    new_tour_point.audio_url = None
                    new_tour_point.audio_file = None
            except:
                pass
            try:
                if tour_point['remove_existing_video_input'] == '1':
                    #delete old image from s3
                    image = new_tour_point.video_url
                    image_file = image.split('/')[-1:][0]
                    delete_from_s3('touritz_static/video', image_file)
                    new_tour_point.video_url = None
                    new_tour_point.video_file = None
            except:
                pass            
                
            if request.FILES:
                try:
                    #cover image
                    if request.FILES['point_cover_image_input']:
                        point_photo =request.FILES['point_cover_image_input']
                        filetype = str(request.FILES['point_cover_image_input'].name[-4:])
                        cover_photo = Image.open(point_photo)
                        new_id =  str(uuid.uuid4()) + filetype      
                        new_name = ('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/' + new_id)
                        cover_photo.save(new_name)
                        new_name_for_s3 = 'https://s3.amazonaws.com/touritz_static/images/' + new_id
                        save_to_s3(new_name, 'touritz_static/images', new_id)
                
                        new_tour_point.cover_image_url = new_name_for_s3                                       
                except:
                    pass
                try:
                    #image 1
                    if request.FILES['additional_image_input_1']:
                       
                        point_photo =request.FILES['additional_image_input_1']
                        filetype = str(request.FILES['additional_image_input_1'].name[-4:])
                        cover_photo = Image.open(point_photo)
                        new_id =  str(uuid.uuid4()) + filetype       
                        new_name = ('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/' + new_id)
                        cover_photo.save(new_name)
                        new_name_for_s3 = 'https://s3.amazonaws.com/touritz_static/images/' + new_id
                        save_to_s3(new_name, 'touritz_static/images', new_id)
                        
                        new_tour_point.image_1_url = new_name_for_s3                       
                except:
                    pass                
                try:
                    #image 2
                    if request.FILES['additional_image_input_2']:
                        point_photo =request.FILES['additional_image_input_2']
                        filetype = str(request.FILES['additional_image_input_2'].name[-4:])
                        cover_photo = Image.open(point_photo)
                        new_id =  str(uuid.uuid4()) + filetype    
                        new_name = ('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/' + new_id)
                        cover_photo.save(new_name)
                        new_name_for_s3 = 'https://s3.amazonaws.com/touritz_static/images/' + new_id
                        save_to_s3(new_name, 'touritz_static/images', new_id)
                        
                        new_tour_point.image_2_url = new_name_for_s3                       
                except:
                    pass
                try:
                    #image 3
                    if request.FILES['additional_image_input_3']:
                        point_photo =request.FILES['additional_image_input_3']
                        filetype = str(request.FILES['additional_image_input_3'].name[-4:])
                        cover_photo = Image.open(point_photo)
                        new_id =  str(uuid.uuid4()) + filetype     
                        new_name = ('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/' + new_id)
                        cover_photo.save(new_name)
                        new_name_for_s3 = 'https://s3.amazonaws.com/touritz_static/images/' + new_id
                        save_to_s3(new_name, 'touritz_static/images', new_id)
                        
                        new_tour_point.image_3_url = new_name_for_s3                       
                except:
                    pass
                try:
                    #image 4
                    if request.FILES['additional_image_input_4']:
                        point_photo =request.FILES['additional_image_input_4']
                        filetype = str(request.FILES['additional_image_input_4'].name[-4:])
                        cover_photo = Image.open(point_photo)
                        new_id =  str(uuid.uuid4()) + filetype     
                        new_name = ('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/' + new_id)
                        cover_photo.save(new_name)
                        new_name_for_s3 = 'https://s3.amazonaws.com/touritz_static/images/' + new_id
                        save_to_s3(new_name, 'touritz_static/images', new_id)
                        
                        new_tour_point.image_4_url = new_name_for_s3                       
                except:
                    pass
                try:
                    #image 5
                    if request.FILES['additional_image_input_5']:
                        point_photo =request.FILES['additional_image_input_5']
                        filetype = str(request.FILES['additional_image_input_5'].name[-4:])
                        cover_photo = Image.open(point_photo)
                        new_id =  str(uuid.uuid4()) + filetype        
                        new_name = ('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/' + new_id)
                        cover_photo.save(new_name)
                        new_name_for_s3 = 'https://s3.amazonaws.com/touritz_static/images/' + new_id
                        save_to_s3(new_name, 'touritz_static/images', new_id)
                        
                        new_tour_point.image_5_url = new_name_for_s3                       
                except:
                    pass
                try:
                    #audio file
                    if request.FILES['add_audio_input']:
                        audio_file =request.FILES['add_audio_input']                
                        new_type= tour_point['add_audio_file_input'][-4:]
                        new_id =  str(uuid.uuid4()) + new_type                        
                        new_name = ('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/' + new_id)
                       #write file
                        with open(new_name, 'wb+') as the_file:
                            for chunk in request.FILES['add_audio_input'].chunks():
                                the_file.write(chunk)
                        new_name_for_s3 = 'https://s3.amazonaws.com/touritz_static/audio/' + new_id
                        save_to_s3(new_name, 'touritz_static/audio', new_id)
                        new_tour_point.audio_url = new_name_for_s3
                        
                        new_tour_point.audio_file = tour_point['add_audio_file_input']
                except:
                    pass                
                try:
                    #video file
                    if request.FILES['add_video_file_input']:
                        #audio_file =request.FILES['add_video_file_input']                
                        new_type= tour_point['add_video_filename'][-4:]
                        new_id_no_file_type =  str(uuid.uuid4())
                        new_id = new_id_no_file_type + new_type
                        new_name = ('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/' + new_id)
                       #write file
                        with open(new_name, 'wb+') as the_file:
                            for chunk in request.FILES['add_video_file_input'].chunks():
                                the_file.write(chunk)
                        new_name_for_s3 = 'https://s3.amazonaws.com/touritz_static/video/' + new_id
                        new_url_for_db = 'https://s3.amazonaws.com/touritz_static/video/' + new_id_no_file_type + '.mp4'
                        save_to_s3(new_name, 'touritz_static/video', new_id)
                        
                        new_tour_point.video_url = new_url_for_db
                        new_tour_point.video_file = tour_point['add_video_filename'][:-4] + '.mp4'                   
                        new_zen_id_url =  's3://touritz_static/video/' + new_id_no_file_type + '.mp4'
                        client = Zencoder('')                    
                        client.job.create(new_name_for_s3, outputs=[{'url': new_zen_id_url, 'public': 'true'}])                        
                except:
                    pass
                
                files = glob.glob('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/*')
                for f in files:
                    os.remove(f)
                        
            new_tour_point.created_by = user
            user_profile = UserProfile.objects.get(user=user)
            new_tour_point.latitude = latitude
            new_tour_point.longitude = longitude            
            new_tour_point.save()         

            if tour_point['tour_point_id_holder'] == '':
                association = TourAndPointAssociations()
                association.tour_id_num = tour_point_tour
                association.tour_point_id_num = new_tour_point
                association.save()


            tour_points = TourAndPointAssociations.objects.filter(tour_id_num=tour_point_tour)
            number_of_points = tour_points.count()
            tour_point_tour.tour_points_number = number_of_points
            tour_point_tour.save()            
            args = {}
            args['tour_point_id'] = new_tour_point.tour_point_id
            args['existing_tour'] = tour_point_tour
            args['existing_tour_points'] = tour_points
            args['user'] = user 
            args.update(csrf(request))
            new_url = '/profile/edit-tour-points/' + str(tour_id) + '/'
          
            #return render_to_response('edit_tour_points.html', args)
            return HttpResponseRedirect(new_url, args)

@login_required
def preview_submit(request, tour_id):
    user = request.user
    existing_tour = Tours.objects.get(tour_id=tour_id)
    existing_tour_points = TourAndPointAssociations.objects.filter(tour_id_num__tour_id=tour_id)
    featured_categories = TourCategories.objects.filter(featured=True).order_by('order')[:8]
    args = {}
    args['existing_tour'] = existing_tour
    args['existing_tour_points'] = existing_tour_points
    args['user'] = user
    args['featured_categories'] = featured_categories
    args.update(csrf(request))

    return render_to_response('preview_submit.html', args)
    
@login_required    
def update_tour_point(request):
    user = request.user       
    data = {}
    data['results'] = {}    
  
    if request.method == 'POST':
        if user.is_authenticated():
            tour_point =request.POST
            name = tour_point['point_name']
            tour_id = tour_point['tour_id']
            description = tour_point['point_description']
            location = tour_point['point_address']
            point_id = tour_point['point_id']
        

            new_tour_point = TourPoints.objects.get(tour_point_id=point_id)
            new_tour_point.title = name
            new_tour_point.description = description
            new_tour_point.address_1 = location
  
            
            new_tour_point.created_by = user
            user_profile = UserProfile.objects.get(user=user)           
            new_tour_point.save()                
            
            data['result'] = 1
            return HttpResponse(json.dumps(data), mimetype='application/json')
        else:
            data['result'] = 0
            data['message'] = "Error."
            return HttpResponse(json.dumps(data), mimetype='application/json')

@login_required
def remove_existing_tour_point(request):
    user = request.user       
    data = {}
    data['results'] = {}    
  
    if request.method == 'POST':
        if user.is_authenticated():
            tour_point =request.POST
            point_id = tour_point['point_id']
            tour_id = tour_point['tour_id']


            tour_point_tour = Tours.objects.get(tour_id=tour_id)
            new_tour_point = TourPoints.objects.get(tour_point_id=point_id)
            
            association = TourAndPointAssociations.objects.get(tour_id_num=tour_point_tour, tour_point_id_num=new_tour_point)
            association.delete()    
            new_tour_point.delete()

            number = TourAndPointAssociations.objects.filter(tour_id_num=tour_point_tour).count()
            tour_point_tour.tour_points_number = number
            tour_point_tour.save()            
              
            data['result'] = 1
            return HttpResponse(json.dumps(data), mimetype='application/json')
        else:
            data['result'] = 0
            data['message'] = "Error."
            return HttpResponse(json.dumps(data), mimetype='application/json')
        
@login_required
def find_location_results(request):
    data = {}
    data['results'] = {}
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            user = UserProfile.objects.get(user_id = request.user.id)
            data_from_js = request.POST
            city = str(data_from_js['city']).replace(' ', '%').replace(',', '%').replace('.', '%')
            query_string = 'https://maps.googleapis.com/maps/api/place/autocomplete/json?input=' + city + '&types=geocode&sensor=true&key=NA'
            
            jsonObj = json.load(urllib2.urlopen(query_string))
            data['cities'] = jsonObj
            data['result'] = 1
            return HttpResponse(json.dumps(data), mimetype='application/json')
        else:
            data['result'] = 0
            data['message'] = "User not authenticated."
            return HttpResponse(json.dumps(data), mimetype='application/json')
    else:
        data['result'] = 0
        data['message'] = "Error."
        return HttpResponse(json.dumps(data), mimetype='application/json')

@login_required
def find_location_results_tour_point(request):
    data = {}
    data['results'] = {}
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated():
            user = UserProfile.objects.get(user_id = request.user.id)
            data_from_js = request.POST
            city = str(data_from_js['city']).replace(' ', '%').replace(',', '%').replace('.', '%')
            query_string = 'https://maps.googleapis.com/maps/api/place/autocomplete/json?input=' + city + '&types=geocode&sensor=true&key=NA'
            jsonObj = json.load(urllib2.urlopen(query_string))
            data['cities'] = jsonObj
            data['result'] = 1
            return HttpResponse(json.dumps(data), mimetype='application/json')
        else:
            data['result'] = 0
            data['message'] = "User not authenticated."
            return HttpResponse(json.dumps(data), mimetype='application/json')
    else:
        data['result'] = 0
        data['message'] = "Error."
        return HttpResponse(json.dumps(data), mimetype='application/json')

def search_titles(request):
    tours = SearchQuerySet().autocomplete(content_auto=request.POST.get('search_text', ''))

    return render_to_response('ajax_search.html', {'tours': tours})


@login_required
def remove_actual_tour(request):
    user = request.user
    user_id = user.id
    data = {}
    data['results'] = {}    
    if request.method == 'POST':
        post =request.POST
        tour_id = post['tour']  
        tour = Tours.objects.get(tour_id=tour_id)
        if tour.photo_top_left:
            #delete old images from s3
            image = tour.photo_top_left 
            image_file = image.split('/')[-1:][0]
            delete_from_s3('touritz_static/images', image_file)
           
        if tour.photo_bottom_left:
            
            #delete old images from s3
            image = tour.photo_bottom_left 
            image_file = image.split('/')[-1:][0]
            delete_from_s3('touritz_static/images', image_file)
         
        if tour.photo_center:
            #delete old images from s3
            image = tour.photo_center 
            image_file = image.split('/')[-1:][0]
            delete_from_s3('touritz_static/images', image_file)

        if tour.image_250_url:
            #delete old image from s3
            image = tour.image_250_url
            image_file = image.split('/')[-1:][0]
            delete_from_s3('touritz_static/images', image_file)

        if tour.image_200_url:
            #delete old image from s3
            image = tour.image_200_url
            image_file = image.split('/')[-1:][0]
            delete_from_s3('touritz_static/images', image_file)

        if tour.image_320_url:
            #delete old image from s3
            image = tour.image_320_url
            image_file = image.split('/')[-1:][0]
            delete_from_s3('touritz_static/images', image_file)

        if tour.image_640_url:
            #delete old image from s3
            image = tour.image_640_url
            image_file = image.split('/')[-1:][0]
            delete_from_s3('touritz_static/images', image_file)                           
           
        if tour.photo_top_right:
            #delete old images from s3
            image = tour.photo_top_right 
            image_file = image.split('/')[-1:][0]
            delete_from_s3('touritz_static/images', image_file)
                          
        if tour.photo_bottom_right:
            #delete old images from s3
            image = tour.photo_bottom_right 
            image_file = image.split('/')[-1:][0]
            delete_from_s3('touritz_static/images', image_file)
                     
        if tour.photo_panoramic:
            #delete old images from s3
            image = tour.photo_panoramic 
            image_file = image.split('/')[-1:][0]
            delete_from_s3('touritz_static/images', image_file)        
            
        if tour.photo_panoramic_cropped:
            #delete old images from s3
            image = tour.photo_panoramic_cropped 
            image_file = image.split('/')[-1:][0]
            delete_from_s3('touritz_static/images', image_file)                        
            
                
        bookmarks = BookMarks.objects.filter(tour_id_num=tour_id)
        tour_point_associations = TourAndPointAssociations.objects.filter(tour_id_num=tour_id)
        tour_point_associations_list = TourAndPointAssociations.objects.filter(tour_id_num=tour_id).values_list('tour_point_id_num__tour_point_id')
        tour_points = TourPoints.objects.filter(tour_point_id__in=tour_point_associations_list)

        for tour_point in tour_points:
            try:
                if tour_point.image_1_url:
                    #delete old image from s3
                    image = tour_point.image_1_url
                    image_file = image.split('/')[-1:][0]
                    delete_from_s3('touritz_static/images', image_file)
                    
            except:
                pass
            try:
                if tour_point.image_2_url:
                    #delete old image from s3
                    image = tour_point.image_2_url
                    image_file = image.split('/')[-1:][0]
                    delete_from_s3('touritz_static/images', image_file)
                    
            except:
                pass
            try:
                if tour_point.image_3_url:
                    #delete old image from s3
                    image = tour_point.image_3_url
                    image_file = image.split('/')[-1:][0]
                    delete_from_s3('touritz_static/images', image_file)
                  
            except:
                pass
            try:
                if tour_point.image_4_url:
                    #delete old image from s3
                    image = tour_point.image_4_url
                    image_file = image.split('/')[-1:][0]
                    delete_from_s3('touritz_static/images', image_file)
                   
            except:
                pass
            try:
                if tour_point.image_5_url:
                    #delete old image from s3
                    image = tour_point.image_5_url
                    image_file = image.split('/')[-1:][0]
                    delete_from_s3('touritz_static/images', image_file)
                   
            except:
                pass
            try:
                if tour_point.cover_image_url:
                    #delete old image from s3
                    image = tour_point.cover_image_url
                    image_file = image.split('/')[-1:][0]
                    delete_from_s3('touritz_static/images', image_file)
                 
            except:
                pass
            try:
                if tour_point.audio_url:
                    #delete old image from s3
                    image = tour_point.audio_url
                    image_file = image.split('/')[-1:][0]
                    delete_from_s3('touritz_static/audio', image_file)

            except:
                pass
            try:
                if tour_point.video_url:
                    #delete old image from s3
                    image = tour_point.video_url
                    image_file = image.split('/')[-1:][0]
                    delete_from_s3('touritz_static/video', image_file)
                  
            except:
                pass
            
        bookmarks.delete()
        tour.delete()
        tour_point_associations.delete()
        tour_points.delete()
        data['result'] = 1
        data['message'] = "Success"
        return HttpResponse(json.dumps(data), mimetype='application/json')
    else:     
        data['result'] = 0
        data['message'] = "Fail"
        return HttpResponse(json.dumps(data), mimetype='application/json')    
        
   
@login_required
def new_panoramic (request):
    user = request.user
    user_id = user.id
    data = {}
    data['results'] = {}    
    if request.method == 'POST':
        try:
            if request.FILES['panoramic_photo']:
                try:
                    tour_id = request.POST['tour-id']                    
                    new_tour = Tours.objects.get(tour_id = tour_id)
                except:
                    pass
                photo_file =request.FILES['panoramic_photo']
                filetype = str(request.FILES['panoramic_photo'].name[-4:])
                new_photo = Image.open(photo_file)
                height = new_photo.size[1]
                if height < 400:             
                    data['error'] = 1
                    return HttpResponse(json.dumps(data), mimetype='application/json')
                else:
                    
                    new_id =  str(uuid.uuid4()) + filetype    
                    new_name = ('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/' + new_id)
                    try:
                        new_photo.save(new_name)
                    except IOError as err:
                        data['new_name'] = new_name
                        data['exc_no'] = err.errno
                        data['exc_str'] = err.strerror 
                        return HttpResponse(json.dumps(data), mimetype='application/json')

                    new_name_for_s3 = 'https://s3.amazonaws.com/touritz_static/images/' + new_id
                    save_to_s3(new_name, 'touritz_static/images', new_id)                    
             
                    try:
                        #delete old image from s3
                        if new_tour.photo_panoramic != '':
                            image = new_tour.photo_panoramic
                            image_file = image.split('/')[-1:][0]
                            delete_from_s3('touritz_static/images', image_file)
        
                        new_tour.photo_panoramic = new_name_for_s3                   
                        #new_photo_url = new_tour.tour_created_by_display_image 
                        new_tour.save()
                    except:                 
                        new_panoramic = TemporaryPanoramic()
                        current_time = round(time.time())
                        new_panoramic.time_created = current_time
                        new_panoramic.photo_panoramic = new_name_for_s3
                        new_panoramic.save()
                        new_id = new_panoramic.photo_id
                        data['new_id'] = new_id
                    
                    files = glob.glob('/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/*')
                    for f in files:
                        os.remove(f)
                     
                    data['new_panoramic_image'] = new_name_for_s3                  
                    return HttpResponse(json.dumps(data), mimetype='application/json')
        except:
            e = sys.exc_info()[0]

            data['error'] = 'Error: %s' % e
            return HttpResponse(json.dumps(data), mimetype='application/json')   

@login_required
def crop_panoramic (request):
    user = request.user
    user_id = user.id
    data = {}
    data['results'] = {}    
    if request.method == 'POST':
        tour_id = request.POST['tour-id']
        try:
            new_tour = Tours.objects.get(tour_id = tour_id)
            image_url = new_tour.photo_panoramic
        except:
            temp_panoramic_id = request.POST['temp_panoramic_id']
            pan_tour = TemporaryPanoramic.objects.get(photo_id=temp_panoramic_id)
            image_url = pan_tour.photo_panoramic
            
        crop_top = request.POST['crop_top']      
        image_thumb_size = request.POST['image_thumb_size']

        try:
            filetype = str(new_tour.photo_panoramic[-4:])
        except:
            filetype = str(pan_tour.photo_panoramic[-4:])
            
        name = str(uuid.uuid4()) + filetype
        path = '/home/ec2-user/touritz/touritz/touritz_app/static/temporary_uploaded_images/'
        filename = path + name
        urlretrieve(image_url, filename)
        image  = Image.open(filename)
        width  = image.size[0]
        height = image.size[1]

        aspect = width / float(height)
        
        ideal_width = 1170
        ideal_height = 400
        size_height = 1170
        size_width = ideal_width / float(aspect)
        
        size = size_width, size_width
        newheight = size_height / float(aspect)
        image = image.resize((1170, newheight), Image.ANTIALIAS)
        image.save(filename, "JPEG")

        test_ratio = float(110 / float(image_thumb_size))      
        new_crop_value = int(test_ratio*400)      
        width  = image.size[0]
        height = image.size[1]            
       
        crop_top_float = float(crop_top)
        height_float = float(height)
        percent_top = int(round(crop_top_float*height_float , 0))
        crop_bottom_val = 400
        height_diff = height - percent_top
        if height_diff < 400:
            crop_bottom_val = height_diff
        crop_bottom = int(round((percent_top + crop_bottom_val), 0))
        image.crop((0, percent_top, width, crop_bottom)).save(path + name)

        save_to_s3(filename, 'touritz_static/images', name)
        new_url = 'https://s3.amazonaws.com/touritz_static/images/' + name
        try:
            new_tour.photo_panoramic_cropped = new_url
            new_tour.save()
        except:           
            pan_tour.photo_panoramic_cropped = new_url
            pan_tour.save()
            
        filelist = glob.glob(path + '*.*')
        for f in filelist:
            os.remove(f)   

        data['new_panoramic_image'] = new_url
        return HttpResponse(json.dumps(data), mimetype='application/json')

@login_required
def publish_tour (request):
    user = request.user
    user_id = user.id
    data = {}
    if request.method == 'POST':
        tour_id = request.POST['tour_id']
        publish = request.POST['publish']
        if publish == '1':
            print('setting true')
            tour = Tours.objects.get(tour_id=tour_id)
            tour.published = True
            tour.save()
        if publish == '0':
            tour = Tours.objects.get(tour_id=tour_id)
            tour.published = False
            tour.save()        
        data['response'] = 'success'
        return HttpResponse(json.dumps(data), mimetype='application/json')            

@staff_member_required
@login_required
def custom_admin (request):
    featured_categories = TourCategories.objects.filter(featured=True).order_by('order')[:8]  
    user = request.user
    user_id = user.id
    data = {}
    args = {}
    tours = Tours.objects.all().order_by('tour_name')
    users = User.objects.all().order_by('username')
    args['featured_categories'] = featured_categories
    args['tours'] = tours
    args['users'] = users
    args['user'] = user
    args.update(csrf(request))
    return render_to_response('custom_admin.html', args)

@staff_member_required    
@login_required
def custom_pro (request):
    user = request.user
    user_id = user.id
    data = {}
    if request.method == 'POST':
        user_id = request.POST['user_id']
        status = request.POST['status']
        if status == '1':
            profile = UserProfile.objects.get(user_id=user_id)
            profile.pro = False
            profile.save()
        if status == '0':
            profile = UserProfile.objects.get(user_id=user_id)
            profile.pro = True
            profile.save()            
        data['result'] = '1'
        return HttpResponse(json.dumps(data), mimetype='application/json')   



        
