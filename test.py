import requests
import bs4
import re
import sys

url = 'https://www.airbnb.com/rooms/2976632'




def get_room_detail(url):
	room = {}
	response =  requests.get(url)
	soup = bs4.BeautifulSoup(response.text)
	room['title'] = soup.select('title')[0]
	if soup.select('div.expandable-content.expandable-content-long'):
		room['description'] = soup.select('div.expandable-content.expandable-content-long')[0]
	room['location'] = [i.attrs.get('data-location') for i in  soup.select('div[id="display-address"]')]
	room['photo_meta_data'] = soup.select('meta#_bootstrap-room_options')[0]
	room['url'] = url
	#print room
	return room

	
def get_room_photo(photo_meta_data):
	photo_list = []
	
	p_caption = re.compile('"caption":"(.+?)"|&quot;caption&quot;:&quot;(.+?)&quot;')
	p_url = re.compile('"url":"(.+?)"|&quot;url&quot;:&quot;(.+?)&quot;')
	p_host = re.compile('"hostingId":([0-9]+?),|&quot;hostingId&quot;:([0-9]+?),')
	
	# "caption":"Large comfortable bed and modern decor"
	# "url":"https://a0.muscache.com/ic/pictures/43680412/cde379d4_original.jpg?interpolation=lanczos-none&amp;size=xx_large&amp;output-format=jpg&amp;output-quality=70",
	# "hostingId":975837,
	room_id =  ''.join(p_host.findall(str(photo_meta_data))[0])
	
	for idx, item in enumerate(p_caption.findall(str(photo_meta_data))):
		photo_list.append({'caption':''.join(item)})
	for idx, item in enumerate(p_url.findall(str(photo_meta_data))):
		photo_list[idx]['url'] = ''.join(item)
		photo_list[idx]['room_id'] = room_id
	#print photo_list
	return photo_list
	

def get_room_desc(url):
	room = {}
	response =  requests.get(url)
	soup = bs4.BeautifulSoup(response.text)
	room['url'] = url
	room['title'] = soup.select('title')[0].get_text().encode('utf-8')
	if soup.select('div.expandable-content.expandable-content-long'):
		room['description'] = soup.select('div.expandable-content.expandable-content-long')[0].get_text().encode('utf-8')
	else:
		room['description'] = u''
	return room


def get_room_test(url):
	'''
	print soup.select('div#price_amount')[0].get_text(strip=True).encode('utf-8')
	print soup.select('div#display-address a[href=#neighborhood]')[0].get_text(strip=True).encode('utf-8')
	

	<meta property="airbedandbreakfast:location:latitude" content="59.31796632519322">
    <meta property="airbedandbreakfast:location:longitude" content="18.07438709919946">
	<meta property="airbedandbreakfast:locality" content="Stockholm">
    <meta property="airbedandbreakfast:region" content="Stockholm County">
    <meta property="airbedandbreakfast:country" content="Sweden">
    <meta property="airbedandbreakfast:city" content="Stockholm">
	<meta property="airbedandbreakfast:rating" content="5.0">

	'''
	room = {}
	response =  requests.get(url)
	soup = bs4.BeautifulSoup(response.text)
	
	summary_tag =  soup.select('div.col-9 div.row.row-condensed.text-muted.text-center')[1].select('div.col-3')
	nb_guest,nb_bedroom,nb_bed = summary_tag[1].get_text(strip=True),summary_tag[2].get_text(strip=True),summary_tag[3].get_text(strip=True)
	
	room['nb_guest'] = nb_guest.split(' ', 1)[0]
	room['nb_bedroom'] = nb_bedroom.split(' ', 1)[0]
	room['nb_bed'] = nb_bed.split(' ', 1)[0]
	room['price'] = soup.select('div#price_amount')[0].get_text(strip=True)
	room['address'] = soup.select('div#display-address a[href=#neighborhood]')[0].get_text(strip=True)
	room['latitude'] = soup.find('meta', attrs={'property': 'airbedandbreakfast:location:latitude', 'content': True})['content']
	room['longitude'] = soup.find('meta', attrs={'property': 'airbedandbreakfast:location:longitude', 'content': True})['content']
	room['country'] = soup.find('meta', attrs={'property': 'airbedandbreakfast:country', 'content': True})['content']
	room['city'] =  soup.find('meta', attrs={'property': 'airbedandbreakfast:city', 'content': True})['content']
	room['rating'] = soup.find('meta', attrs={'property': 'airbedandbreakfast:rating', 'content': True})['content']
	print room

'''
	url =  sys.argv[1]
	get_room_test(url)
	'''