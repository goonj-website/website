#!/usr/local/bin/python 

import subprocess
import urllib, urllib2, json
from datetime import datetime, timedelta
import MySQLdb,sys

#media_dir='/Users/DipaChowdhury/Desktop/UploadCode/testing/Media'
#remote_media_dir='/usr/local/voicesite/fsmedia'

db_uname='root'
db_pwd='junoon'
db_name='mobilevoices'

last_fetch_date_file = "last_fetch_date.txt"
remote_audio_url_base = "http://voice.gramvaani.org/fsmedia/recordings/"
base_url = "http://voice.gramvaani.org/vapp/mnews/get_news_json/10/"

# read date from file
f = open(last_fetch_date_file,"r+")
last_fetch_date_str = f.read()
f.close()
date_arr = last_fetch_date_str.split('/')
last_fetch_date = datetime(year = int(date_arr[0]), month = int(date_arr[1]), day = int(date_arr[2]))
print "Last fetch date/time = " + str(last_fetch_date_str)

url = base_url + last_fetch_date_str
response = urllib2.urlopen(url)
jsonResponse = json.loads(response.read(),encoding='utf-8')

# get the older stories too for updating transcripts
prev = last_fetch_date - timedelta(days=3)
prevURL = base_url + str(prev.year) + "/" + str(prev.month) + "/" + str(prev.day) + "/"+ str(prev.hour) + "/"+ str(prev.minute) + "/"
prevResponse = urllib2.urlopen(prevURL)
prevJsonResponse = json.loads(prevResponse.read(),encoding='utf-8')

print "Got the JSON response"

# jsonResponse is a list of dictionaries. each element in the list gives all info about one story
#test = json.dumps([s['geometry']['location'] for s in jsonResponse)
# parse json file to see if there is new data

# if new data
# command given by dinesh sir : rsync -auz -e ssh "telephony@$server:$remote_media_dir" "$media_dir"

#the line below works but it asks for password, ask about that
#process = subprocess.Popen(['sudo','rsync','-auz','-e','ssh',"mridu@"+server+":"+remote_media_dir ,media_dir])
#returncode = process.wait()
#if(returncode > 0):
#	print "Found an error",returncode
#else:
	#print "RSYNC done successfully"

# mysql query to enter the data into our database
try:
        conn = MySQLdb.connect (host = "localhost",
                                user = db_uname,
                                passwd = db_pwd,
                                db = db_name)
except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit (1)

cursor = conn.cursor ()

for story in jsonResponse:
	story_id = json.dumps(story['pk'])
	title=story['fields']['title']
	title=title.encode('utf-8')
	transcript=story['fields']['transcript']
	transcript=transcript.encode('utf-8')
	date = str(json.dumps(story['fields']['time']))
	date = date.replace('\"','')
	ai_id = json.dumps(story['fields']['ai'])
	detail_id = json.dumps(story['fields']['detail']['pk'])
	tags = str(json.dumps(story['fields']['tags']))
	tags = tags.replace('\"','')
	is_comment = str(json.dumps(story['fields']['is_comment']))
	is_comment = is_comment.replace('\"','')
	is_src_caller = str(json.dumps(story['fields']['is_src_caller']))
	is_src_caller = is_src_caller.replace('\"','')
	state = str(json.dumps(story['fields']['state']))
	state = state.replace('\"','')
	location_text=story['fields']['location_text']
	location=story['fields']['location']
	
	audio = 'audio/recordings/' + ai_id + '/' + detail_id + '.mp3'
	remote_audio_url = remote_audio_url_base + ai_id + '/' + detail_id + '.mp3'

	if(is_src_caller == "false"):
		is_src_caller = False
	else:
		is_src_caller = True
		
	if(is_comment == "false"):
		is_comment = False
	else:
		is_comment = True

	print "Inserting story " + story_id
	
	cursor.execute ("SET character_set_results = 'utf8', character_set_client = 'utf8', character_set_connection = 'utf8', character_set_database = 'utf8', character_set_server = 'utf8'")


	if ((state == 'ARC') or (state == 'PUB')):
		cursor.execute (u"INSERT INTO " + " mobilevoices_story " + u""" (location_id,story_type,story_id, detail_id, ai_id, tags, title,transcript,audio,video,views_count,date,rating,top_story,related_stories,is_comment,is_src_caller,location_text,remote_audio_url)
		 VALUES(%s, 'NON_EVENT',%s,%s,%s,%s,%s,%s,%s,NULL,0,%s,3,0,NULL,%s,%s,%s,%s) """,(location,story_id,detail_id,ai_id,tags,title,transcript,audio,date,is_comment,is_src_caller,location_text,remote_audio_url))

	conn.commit()

#Topic Channel


	cursor.execute ("""INSERT INTO mobilevoices_storytcrelation (story_id, topic_channel_id) SELECT s.story_id, 4 FROM mobilevoices_story s, mobilevoices_topicchannel t WHERE ( s.tags LIKE "%adulteration%") OR ( s.tags LIKE "%anganwadi%") OR ( s.tags LIKE "%Anganbadi%") OR ( s.tags LIKE "%%ANM%") OR ( s.tags LIKE "%camp%") OR ( s.tags LIKE "%children%") OR ( s.tags LIKE "%disability%") OR ( s.tags LIKE "%disease%") OR ( s.tags LIKE "%epidemic%") OR ( s.tags LIKE "%family planning%") OR ( s.tags LIKE "%health%") OR ( s.tags LIKE "%hospitals%") OR ( s.tags LIKE "%hygiene%") OR ( s.tags LIKE "%insurance%") OR ( s.tags LIKE "%malaria%") OR ( s.tags LIKE "%NRHM%") OR ( s.tags LIKE "%nutrition%") OR ( s.tags LIKE "%pulse polio campaign%") OR ( s.tags LIKE "%sahiya%") OR ( s.tags LIKE "%sanitation%") OR ( s.tags LIKE "%sex-selective abortions%") OR ( s.tags LIKE "%vaccination%") ON DUPLICATE KEY UPDATE story_id = s.story_id""")

	cursor.execute("""INSERT INTO mobilevoices_storytcrelation (story_id, topic_channel_id) SELECT s.story_id, 1 FROM mobilevoices_story s, mobilevoices_topicchannel t WHERE ( s.tags LIKE "%community marriage%") OR ( s.tags LIKE "%culture%") OR ( s.tags LIKE "%entertainment%") OR ( s.tags LIKE "%fair%") OR ( s.tags LIKE "%festival%") OR ( s.tags LIKE "%folk song%") OR ( s.tags LIKE "%jokes%") OR ( s.tags LIKE "%language%") OR ( s.tags LIKE "%life skills%") OR ( s.tags LIKE "%personal expressions%") OR ( s.tags LIKE "%poetry, rhyme%") OR ( s.tags LIKE "%prayer%") OR ( s.tags LIKE "%rhyme%") OR ( s.tags LIKE "%song%") OR ( s.tags LIKE "%sports%") OR ( s.tags LIKE "%thought%") OR ( s.tags LIKE "%tribute%") ON DUPLICATE KEY UPDATE story_id = s.story_id""")

	cursor.execute("""INSERT INTO mobilevoices_storytcrelation (story_id, topic_channel_id) SELECT s.story_id, 2 FROM mobilevoices_story s, mobilevoices_topicchannel t WHERE ( s.tags LIKE "%addiction%") OR ( s.tags LIKE "%alcoholism%") OR ( s.tags LIKE "%bribe%") OR ( s.tags LIKE "%corruption%") OR ( s.tags LIKE "%crime%") OR ( s.tags LIKE "%dowry%") OR ( s.tags LIKE "%exploitation%") OR ( s.tags LIKE "%extortion%") OR ( s.tags LIKE "%fraud%") OR ( s.tags LIKE "%human trafficking%") OR ( s.tags LIKE "%injustice%") OR ( s.tags LIKE "%missing person report%") OR ( s.tags LIKE "%naxalism%") OR ( s.tags LIKE "%police%") OR ( s.tags LIKE "%scam%") OR ( s.tags LIKE "%substance abuse%") OR ( s.tags LIKE "%suicide%") OR ( s.tags LIKE "%violence%") ON DUPLICATE KEY UPDATE story_id = s.story_id""")

	cursor.execute("""INSERT INTO mobilevoices_storytcrelation (story_id, topic_channel_id) SELECT s.story_id, 8 FROM mobilevoices_story s, mobilevoices_topicchannel t WHERE ( s.tags LIKE "%education%") OR ( s.tags LIKE "%edutainment%") OR ( s.tags LIKE "%examination%") OR ( s.tags LIKE "%illiteracy%") OR ( s.tags LIKE "%information%") OR ( s.tags LIKE "%mid-day meal%") OR ( s.tags LIKE "%RTE%") OR ( s.tags LIKE "%school%") OR ( s.tags LIKE "%student%") OR ( s.tags LIKE "%teacher%") ON DUPLICATE KEY UPDATE story_id = s.story_id""")

	cursor.execute("""INSERT INTO mobilevoices_storytcrelation (story_id, topic_channel_id) SELECT s.story_id, 6 FROM mobilevoices_story s, mobilevoices_topicchannel t WHERE ( s.tags LIKE "%drought%") OR ( s.tags LIKE "%environment%") OR ( s.tags LIKE "%flood%") OR ( s.tags LIKE "%forest%") OR ( s.tags LIKE "%pollution%") OR ( s.tags LIKE "%water%") OR ( s.tags LIKE "%weather%") OR ( s.tags LIKE "%wildlife%") ON DUPLICATE KEY UPDATE story_id = s.story_id""")

	cursor.execute("""INSERT INTO mobilevoices_storytcrelation (story_id, topic_channel_id) SELECT s.story_id, 7 FROM mobilevoices_story s, mobilevoices_topicchannel t WHERE ( s.tags LIKE "%bandh%") OR ( s.tags LIKE "%campaign%") OR ( s.tags LIKE "%census%") OR ( s.tags LIKE "%civil services%") OR ( s.tags LIKE "%development, development issues%") OR ( s.tags LIKE "%discussion%") OR ( s.tags LIKE "%displacement%") OR ( s.tags LIKE "%election%") OR ( s.tags LIKE "%electricity%") OR ( s.tags LIKE "%forest rights, Forest Act%") OR ( s.tags LIKE "%governance%") OR ( s.tags LIKE "%government scheme%") OR ( s.tags LIKE "%inflation%") OR ( s.tags LIKE "%infrastructure, bridge%") OR ( s.tags LIKE "%irrigation%") OR ( s.tags LIKE "%justice%") OR ( s.tags LIKE "%municipality%") OR ( s.tags LIKE "%politics%") OR ( s.tags LIKE "%PRI, gram sabha%") OR ( s.tags LIKE "%railways%") OR ( s.tags LIKE "%roads%") OR ( s.tags LIKE "%subsidy%") OR ( s.tags LIKE "%UID%") ON DUPLICATE KEY UPDATE story_id = s.story_id""")

	cursor.execute("""INSERT INTO mobilevoices_storytcrelation (story_id, topic_channel_id) SELECT s.story_id, 5 FROM mobilevoices_story s, mobilevoices_topicchannel t WHERE ( s.tags LIKE "%employment%") OR ( s.tags LIKE "%tourism%") OR ( s.tags LIKE "%career%") OR ( s.tags LIKE "%cottage industry%") OR ( s.tags LIKE "%labour%") OR ( s.tags LIKE "%livelihood issues%") OR ( s.tags LIKE "%migration%") OR ( s.tags LIKE "%MNREGA%") OR ( s.tags LIKE "%pension%") OR ( s.tags LIKE "%poverty%") OR ( s.tags LIKE "%SHG%") OR ( s.tags LIKE "%stipend%") OR ( s.tags LIKE "%unemployment%") OR ( s.tags LIKE "%wage delays%") OR ( s.tags LIKE "%wages%") ON DUPLICATE KEY UPDATE story_id = s.story_id""")

	cursor.execute("""INSERT INTO mobilevoices_storytcrelation (story_id, topic_channel_id) SELECT s.story_id, 3 FROM mobilevoices_story s, mobilevoices_topicchannel t WHERE ( s.tags LIKE "%agriculture%") OR ( s.tags LIKE "%farmer%") OR ( s.tags LIKE "%livestock%") ON DUPLICATE KEY UPDATE story_id = s.story_id""")


print "Updating transcripts for ..."
for s in prevJsonResponse:
        cursor.execute ("SET character_set_results = 'utf8', character_set_client = 'utf8', character_set_connection = 'utf8', character_set_database = 'utf8', character_set_server = 'utf8'")

        story_id = json.dumps(s['pk'])
	print "Story id: " + str(story_id)

        transcript=s['fields']['transcript']
        transcript=transcript.encode('utf-8')
        cursor.execute(u"UPDATE mobilevoices_story SET transcript=%s WHERE story_id=%s", (transcript,story_id))
        conn.commit()

	


conn.commit()
cursor.close ()
conn.close ()

now = datetime.now()
curr_date_str = str(now.year) + '/' + str(now.month) + '/' + str(now.day) + '/' + str(now.hour) + '/' + str(now.minute) + '/'
f = open(last_fetch_date_file,"w")
f.write(curr_date_str)
f.close()

print "All data entered, exiting....."
