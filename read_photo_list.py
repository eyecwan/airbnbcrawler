# -*- coding: utf-8 -*- 
import pickle
import re
import string
import os

photo_list = []
images = []
keywords = {}
room_photo_filename = 'room_photo_finland'

with open(room_photo_filename,'rb') as f:
	photo_list = pickle.load(f)

for i in photo_list:
		print i['url']

def en_cn_keywords(str,d):
	i = str.find(d)
	return str[:i],str[i+1:]
		
with open('keywords.txt') as f:
	keywords['keyword'] = f.read().splitlines()

for idx,i in enumerate(keywords['keyword']):
	en,cn = en_cn_keywords(i,'|')
	keywords['keyword'][idx] = {'en':en,'cn':cn}
	
	
with open('keywords_id.txt') as f:
	keywords['id'] = f.read().splitlines()
	
'''
set @next_id = (SELECT IF(MAX(id)+1 IS NULL, 1, MAX(id)+1) FROM piwigo_images);

INSERT  INTO piwigo_images (id,file,name,date_available,path,representative_ext,storage_category_id,added_by) VALUES(@next_id,'53737798_95705af3.jpg','53737798 95705af3','2014-10-20 16:33:47','./galleries/deco/stockholm/53737798_95705af3.jpg',NULL,'2','1');

INSERT  INTO piwigo_image_category(image_id,category_id) VALUES(@next_id,'2')

TRUNCATE TABLE piwigo_user_cache_categories;
TRUNCATE TABLE piwigo_user_cache;


TRUNCATE TABLE piwigo_image_category;
TRUNCATE TABLE piwigo_images;


TRUNCATE TABLE piwigo_categories;
TRUNCATE TABLE piwigo_image_tag;
TRUNCATE TABLE piwigo_tags;

	
eyecwan@E7D4C9EFE84440 /cygdrive/c/EasyPHP-DevServer/data/localweb/projects/piwigo
$ ls ./galleries/deco/stockholm/* > photo_list

eyecwan@E7D4C9EFE84440 /cygdrive/c/EasyPHP-DevServer/data/localweb/projects/piwigo
$ pwd
/cygdrive/c/EasyPHP-DevServer/data/localweb/projects/piwigo

'''	

def piwigo_images_import():
	with open('C:\EasyPHP-DevServer\data\localweb\projects\piwigo\photo_list') as f:
		images = f.read().splitlines()	
		

	for i in images:
		print "set @next_id = (SELECT IF(MAX(id)+1 IS NULL, 1, MAX(id)+1) FROM piwigo_images);"
		print "INSERT  INTO piwigo_images (id,file,name,date_available,path,representative_ext,storage_category_id,added_by) VALUES(@next_id,\'%s\',\'%s\',\'2014-10-20 16:33:47\',\'%s\',NULL,\'2\',\'1\');" % (os.path.basename(i),os.path.splitext(os.path.basename(i))[0],i)
		print "INSERT  INTO piwigo_image_category(image_id,category_id) VALUES(@next_id,'2');"
	
'''	
  
insert keywords from files


SELECT id
  FROM piwigo_tags
  WHERE name = 'edison'
  
INSERT  INTO piwigo_tags
  (name,url_name)
  VALUES('edison','edison');
  
INSERT  INTO piwigo_image_tag
  (image_id,tag_id)
  VALUES('7','6')

'''  

def tags_import(keywords):
	for i in keywords['keyword']:
		print "SELECT id FROM piwigo_tags WHERE name = '" + i + "';"
		print "INSERT  INTO piwigo_tags (name,url_name) VALUES('" + i + "','" + i + "');"

#  mysql -u root photo < keyword_id.sql  | grep -v id > keywords_id.txt



	
'''
add tags based on the image name

insert into piwigo_image_tag (image_id,tag_id)value((select id from piwigo_images where file = '29415174_2005532a.jpg'),'10')
'''

def image_name(url,p_image_id):
	name = p_image_id.findall(url)[0]
	name = string.replace(name,'/','_') + '.jpg'
	return name
	
def piwigo_image_tag_import(photo_list,keywords):
	p_url= re.compile('(^http.+\.jpg?).*')
	p_image_id = re.compile('pictures/(.+?)_original')

	for photo in photo_list:
		for idx,kw in enumerate(keywords['keyword']):
			if kw in photo['caption'].lower():
				#print "found tag:",kw,keywords['id'][idx],image_name(photo['url'],p_image_id)
				print "insert into piwigo_image_tag (image_id,tag_id) value((select id from piwigo_images where file = '" + image_name(photo['url'],p_image_id) + "'),'" +keywords['id'][idx] + "')" +  ";"



'''
get the keywords from captions
'''
def string_to_list(str):
	word_list = re.sub("[^\w]"," ", str).split()
	return word_list

def keywords_from_captions(photo_list):
	word_list = []	
	for i in photo_list:
		word_list += string_to_list(i['caption'])

	for i in word_list:
		print i.lower()
#  python read_photo_list.py  | sort | uniq -c | sort -nr | head -n 100
		
#print len(photo_list)
#keywords_from_captions(photo_list)
#tags_import(keywords)
#	python read_photo_list.py  | grep ^INSERT > insert_tags.sql
#	python read_photo_list.py  | grep ^SELECT  > keyword_id.sql
#	mysql -u root photo < keyword_id.sql  | grep -v id > keywords_id.txt
#piwigo_image_tag_import(photo_list,keywords)
