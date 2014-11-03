import requests
import bs4
import room_detail
import re
import string
import os
import subprocess
import pickle
import test
import sys


search_url = 'https://www.airbnb.com/s/'
city = 'norway'
city = sys.argv[1]
city_url = search_url + city
criteria_url = city_url +  '?room_types%5B%5D=Entire+home%2Fapt&price_min=1500'
#criteria_url = city_url +  '?room_types%5B%5D=Entire+home%2Fapt&room_types%5B%5D=Private+room&price_min=1000'
url = criteria_url
list_page_no = 56



image_postfix = '?interpolation=lanczos-none&size=x_large&output-format=jpg&output-quality=70'


def get_place_data(url):
	print "room list url:", url
	place_data = {}
	response = requests.get(url)
	soup = bs4.BeautifulSoup(response.text)
	place_data['title'] = [i.attrs.get('title') for i in  soup.select('div.h5.listing-name.text-truncate.row-space-top-1')]
	place_data['room_url'] = [i.attrs.get('href') for i in  soup.select('div.panel-body.panel-card-section a.text-normal.link-reset')]
	'''	
			<div class="panel-body panel-card-section">
			  <div class="media">
				  <a href="/users/show/13783557"
					 class="pull-right media-photo media-round card-profile-picture card-profile-picture-offset" rel="nofollow">
					<img src="https://a0.muscache.com/ic/users/13783557/profile_pic/1404075688/original.jpg?interpolation=lanczos-none&amp;crop=w:w;*,*&amp;crop=h:h;*,*&amp;resize=68:*&amp;output-format=jpg&amp;output-quality=70" alt="">
				  </a>
				<a href="/rooms/3452178?s=ES3Q" class="text-normal">
				  <div title="Studio at the heart of Stockholm" class="h5 listing-name text-truncate row-space-top-1">
					Studio at the heart of Stockholm
				  </div>
				</a>
				<div class="text-muted listing-location text-truncate"><a href="/rooms/3452178?s=ES3Q" class="text-normal link-reset">
		Entire home/apt &middot; 5 reviews &middot; Södermalm, Stockholm
	</a>
	</div>
			  </div>
	'''
	return place_data
	
def get_place_data_np(url,page):
	place_data = {}
	place_data['room_url'] = []
	place_data['title'] = []
	for i in range(1,page+1):
		page_url = url + '&page=' + str(i)
		new_place_data = get_place_data(page_url)
 		for i in new_place_data.keys():
			place_data[i] = place_data[i] + new_place_data[i]
	return place_data

def get_place_data_n_price(base_url,price_min,price_max,n):
	#?price_min=576&price_max=2426
	jump = (price_max- price_min)/n
	for i in range(0,n-1):
		price_url  = base_url + '&price_min=' + str(price_min+jump*i) + '&price_max=' + str(price_min+jump*(i+1))
		print price_url
		get_place_data_np(price_url,list_page_no)
	
def save_room_photos_as_file(url):	
	rooms = []
	room_photos = []

	for url in get_place_data_np(url,list_page_no)['room_url']:
		#[u'/rooms/3452178?s=dvwq', u'/rooms/3452178?s=dvwq',
		full_url = 'https://www.airbnb.com' + url 
		print "handle room",url
		room = room_detail.get_room_detail(full_url)
		if room != None and (room['url'] not in [r.get('url',None) for r in rooms]):
			room_photo = room_detail.get_room_photo(room['photo_meta_data'])
			room_photos = room_photos + room_photo
			room['photo_meta_data'] = room['photo_meta_data'].encode('utf-8')
			rooms.append(room)
	
	
	print len(rooms),len(room_photos)
	
	with open("room_photo_"+ city,'wb') as f:
		pickle.dump(room_photos,f)
		
	with open("rooms_"+ city,'wb') as f:
		pickle.dump(rooms,f)

def save_room_photo(url,city_name):	
	rooms = []
	room_photos = []
	room_photos_uniq = []

	print "handle room",url
	room = room_detail.get_room_detail(url)
	room_photo = room_detail.get_room_photo(room['photo_meta_data'])
	room_photos = room_photos + room_photo
	
	del room['photo_meta_data']
	if room not in rooms:
		rooms.append(room)
		
	for i in room_photos:
		if i not in room_photos_uniq:
			room_photos_uniq.append(i)
			
	with open("room_photo_"+ city_name,'wb') as f:
		pickle.dump(room_photos_uniq,f)
		
	#print rooms
	
save_room_photos_as_file(url)
#save_room_photo('https://www.airbnb.com/rooms/2901787?s=U_3X','oslo')
#save_room_photo('https://www.airbnb.com/rooms/2758051?s=W5ua','helsinkl')
#save_room_photo('https://www.airbnb.com/rooms/1356348?s=sDW2','gothenborg')
#save_room_photo('https://www.airbnb.com/rooms/1150687?s=67Zo','iceland')

