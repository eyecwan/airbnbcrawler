import pickle
import re
import string
import subprocess
import time
import sys

# find img/finland/ -type f -size 0 | xargs.exe rm -f;ls img/finland/ > download_list ;python download_image.py finland
# find img/iceland/ -type f -size 0 | xargs.exe rm -f;ls img/sweden/ > download_list ;python download_image.py iceland


city_name = sys.argv[1]

photo_list = []
photo_list_new = []
download_list = []
room_photo_filename = 'room_photo_' + city_name

image_postfix = '?interpolation=lanczos-none&size=x_large&output-format=jpg&output-quality=70'



with open(room_photo_filename,'rb') as f:
	photo_list = pickle.load(f)

with open('download_list') as f:
	download_list = f.read().splitlines()

p_image_id = re.compile('pictures/(.+?)_original')
p_url= re.compile('(^http.+\.jpg?).*')

print "downloaded:",len(download_list)
print "total:",len(photo_list)


for index,photo in enumerate(photo_list):
	image_url = p_url.findall(photo['url'])[0]
	image_url = image_url+image_postfix
	image_url = '\'' + image_url + '\''
	image_name = p_image_id.findall(image_url)[0]
	image_name = string.replace(image_name,'/','_')+'.jpg'
	#print photo['room_id'],image_name,photo['caption']
	if image_name not in download_list:
		photo_list[index]['download'] = 'no' 
	else:
		photo_list[index]['download'] = 'yes'
		#subprocess.Popen(["wget", image_url, "-O","img/copenhagen/" + image_name ])	
		
	
for index,photo in enumerate(photo_list):
	if photo['download'] == 'no':
		image_url = p_url.findall(photo['url'])[0]
		image_url = image_url+image_postfix
		image_url = '\"' + image_url + '\"'
		image_name = p_image_id.findall(image_url)[0]
		image_name = string.replace(image_name,'/','_')+'.jpg'
		subprocess.Popen(["wget",  image_url, "-O","img/" + city_name + '/' + image_name ])	
		if (index % 15 == 0):
			time.sleep(2)
