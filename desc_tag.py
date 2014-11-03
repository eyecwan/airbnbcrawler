import requests
import bs4
import room_detail
import pickle
import sys



city = sys.argv[1]
readorwrite = sys.argv[2]
search_url = 'https://www.airbnb.com/s/'
#city = 'Chiang-Mai'
city_url = search_url + city
criteria_url = city_url +  'room_types%5B%5D=Entire+home%2Fapt&room_types%5B%5D=Private+room&price_min=1000'
url = criteria_url


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

	
def save_room_as_file(url):	
	rooms = []

	for url in get_place_data_np(url,50)['room_url']:
		#[u'/rooms/3452178?s=dvwq', u'/rooms/3452178?s=dvwq',
		full_url = 'https://www.airbnb.com' + url 
		print "handle room",url
		room = room_detail.get_room_desc(full_url)
		if room not in rooms:
			rooms.append(room)
	with open("room_desc_" + city,'wb') as f:
		pickle.dump(rooms,f)
	return rooms

'''
for r in save_room_as_file(url):
	print r['description']
'''

#print len(save_room_as_file(url))


def read_room_from_file(city):
	rooms = []
	with open('room_desc_' + city ,'rb') as f:
		rooms = pickle.load(f)
	return rooms

rooms = []
		
if readorwrite == 'write':
	save_room_as_file(url)
elif readorwrite == 'read':
	rooms = read_room_from_file(city)
	for i in rooms:
		print i['description']
		
		
#for i in china france russia uk; do echo $i; python desc_tag.py "$i" read | tee "room_desc_${i}_txt"; done