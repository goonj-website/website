#!/usr/local/bin/python 

import subprocess
import urllib, urllib2, json
import datetime
import MySQLdb,sys

media_dir='/Users/DipaChowdhury/Desktop/UploadCode/testing/Media'
remote_media_dir='/usr/local/voicesite/fsmedia'
server='10.22.5.46'
port='3306'
username='root'
password='goonjWebsite'
db_name='mobilevoicedb'

#note current time
now = datetime.datetime.now()

# read date from file
f = open("C:/Users/sherlock/Desktop/GV/UploadCode/nfile","r+")
date = f.read()
f.close()

print "Date read ",date

url = "http://10.208.26.135/vapp/mnews/get_news_json/10/"
#url for home:
#url = "http://voice.gramvaani.org/vapp/mnews/get_news_json/10/"
# also calculate date 3 days back here alongwith the url to update transcript
prev_month = now.month
prev_year = now.year

if now.day == 1 or now.day == 2 or now.day == 3:
	if now.month == 1:
		prev_year = now.year - 1
		prev_month = 12
	else:
		prev_month = now.month - 1
	prev_day = 28
else:
	prev_day = now.day-3

prev_date = str(prev_year) + "/" + str(prev_month) + "/" + str(prev_day) + "/"+ str(now.hour) + "/"+ str(now.minute) + "/"

print "Previous date to update transcripts",prev_date

prevURL = url + prev_date

# get the url for the needed data

url = url + date

# add new	 date
curr_date = str(now.year) + "/" + str(now.month) + "/" + str(now.day) + "/"+ str(now.hour) + "/"+ str(now.minute) + "/"
#f.seek(0,0)
f = open("C:/Users/sherlock/Desktop/GV/UploadCode/nfile","w")
f.write(curr_date)
f.close()

print "Date written ",curr_date

#send get request

#uresponse=unicode(response,'utf-8')
response = urllib2.urlopen(url)
#uresponse=unicode(response,'utf-8')
#ujsonResponse=unicode(jsonResponse,'utf-8')
jsonResponse = json.loads(response.read(),encoding='utf-8')
#ujsonResponse=unicode(jsonResponse,'utf-8')


print "Got the JSON response"

# get the older stories too now
prevResponse = urllib2.urlopen(prevURL)

prevJsonResponse = json.loads(prevResponse.read(),encoding='utf-8')

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
                                user = "root",
                                passwd = "",
                                db = "mobilevoiceDB")
except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit (1)

cursor = conn.cursor ()

for s in jsonResponse:


	story_id = json.dumps(s['pk'])
#	title = str(json.dumps(s['fields']['title']))
#	title = title.replace('\"','')
#	title=title.encode('utf-8')
#	transcript = str(json.dumps(s['fields']['transcript']))
#	transcript = transcript.replace('\"','')
#	transcript=transcript.encode('utf-8')
	title=s['fields']['title']
	title=title.encode('utf-8')
	transcript=s['fields']['transcript']
	transcript=transcript.encode('utf-8')
	date = str(json.dumps(s['fields']['time']))
	date = date.replace('\"','')
	ai_id = json.dumps(s['fields']['ai'])
	detail_id = json.dumps(s['fields']['detail']['pk'])
	tags = str(json.dumps(s['fields']['tags']))
	tags = tags.replace('\"','')
	is_comment = str(json.dumps(s['fields']['is_comment']))
	is_comment = is_comment.replace('\"','')
	is_src_caller = str(json.dumps(s['fields']['is_src_caller']))
	is_src_caller = is_src_caller.replace('\"','')
	state = str(json.dumps(s['fields']['state']))
	state = state.replace('\"','')
	location_text=s['fields']['location_text']
	location=s['fields']['location']
	
	audio = 'audio/recordings/' + ai_id + '/' + detail_id + '.mp3'


	if(is_src_caller == "false"):
		is_src_caller = 0

	if(is_src_caller == "true"):
		is_src_caller=1
		
	if(is_comment == "false"):
		is_comment = 0

	if(is_comment == "true"):
		is_comment=1

	print story_id
	print title
	print transcript
	print date
	print tags	
	
	cursor.execute ("SET character_set_results = 'utf8', character_set_client = 'utf8', character_set_connection = 'utf8', character_set_database = 'utf8', character_set_server = 'utf8'")


	if ((state == 'ARC') or (state == 'PUB')):

		cursor.execute (u"INSERT INTO " + " mobilevoices_story " + u""" (location_id,story_type,story_id, detail_id, ai_id, tags, title,transcript,audio,video,views_count,date,rating,top_story,related_stories,is_comment,is_src_caller,location_text)
		 VALUES(%s, 'NON_EVENT',%s,%s,%s,%s,%s,%s,%s,NULL,0,%s,3,0,NULL,%s,%s,%s) """,(location,story_id,detail_id,ai_id,tags,title,transcript,audio,date,is_comment,is_src_caller,location_text))

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



#location
for s in prevJsonResponse:
        cursor.execute ("SET character_set_results = 'utf8', character_set_client = 'utf8', character_set_connection = 'utf8', character_set_database = 'utf8', character_set_server = 'utf8'")

        story_id = json.dumps(s['pk'])
        transcript=s['fields']['transcript']
        transcript=transcript.encode('utf-8')
	#transcript=""  
	#print "Transcript recieved at second fetch is below"
	#print transcript

        cursor.execute(u"UPDATE mobilevoices_story SET transcript=%s WHERE story_id=%s", (transcript,story_id))
        conn.commit()

	


conn.commit()
cursor.close ()
conn.close ()



print "All data entered too, exiting....."
