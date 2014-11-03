import pickle
import sys
import os

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
city_name = sys.argv[1]

photo_list = []
room_list = []

room_photo_filename = 'room_photo_' + city_name
room_filename = 'rooms_' + city_name




with open(room_photo_filename,'rb') as f:
	photo_list = pickle.load(f)
	
with open(room_filename,'rb') as f:
	room_list = pickle.load(f)
	
def sort_photo():
	print "add"
	for i in room_list:
		room_id = i['url'].split("/")[-1]
		price = int(i['price'].replace("$",""))
		try:
			print room_id,price,price/int(i['nb_bedroom']),price/int(i['nb_guest'])		
		except Exception,e:
			print e
			

print len(room_list)
 

def search():
	while True:

		input = raw_input('search for something: type id\n')
		type,id = input.split(' ')
		room_id = ''
		if type =='photo':
			for i in photo_list:
				if id in i['url']:
					room_id =  i['room_id']
					print room_id

		for i in room_list:
			if room_id in i['url']:
				print i
				price = int(i['price'].replace("$",""))
				print "price, per bedroom,per guest",price,price/int(i['nb_bedroom']),price/int(i['nb_guest'])

				
#sort_photo()
search()