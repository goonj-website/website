# Create your views here.
from django.template import RequestContext
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response
from goonj.models import Story,Issue,CommunityRep,GovernmentDepartment,ChannelPartner,TopicChannel,Location,Photo,Loc_country, Loc_state, Loc_district, Loc_block, Loc_village
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime

def index(request):
	#tops = Story.objects.filter(top_story=True).order_by('-date')[:1]
	#for s in tops:
	#	topstory = s
	lsl = Story.objects.all().order_by('-date')[:13]
	top_story_list = Story.objects.all().order_by('-views_count')[:5]
	topic_channel_list = TopicChannel.objects.all()
	#location_list = Location.objects.all()
	location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
	location_list_1 = location_list[0:8]
	location_list_2 = location_list[8:16]
	location_list_3 = location_list[16:]
	bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]


	other9 = []
	for st in lsl:
		#if (st.top_story != True):
			other9.append(st)
	return render_to_response('goonj/index (copy).html', {'l0': other9[1],'l1': other9[2],'l2': other9[3],'l3': other9[4],'l4': other9[5],'l5': other9[6],'l6': other9[7],'l7': other9[8],'l8': other9[9],'l9': other9[10],'l10': other9[11],'l11': other9[12],'top_story_list' : top_story_list, 'topic_channel_list' : topic_channel_list, 'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist,'crep0' : other9[1].community_rep.all(), 'crep1' : other9[2].community_rep.all(), 'crep2' : other9[3].community_rep.all(), 'crep3' : other9[4].community_rep.all(), 'crep4' : other9[5].community_rep.all(), 'crep5' : other9[6].community_rep.all(), 'crep6' : other9[7].community_rep.all(), 'crep7' : other9[8].community_rep.all(), 'crep8' : other9[9].community_rep.all(), 'crep9' : other9[10].community_rep.all(),'crep10' : other9[11].community_rep.all(),'crep11' : other9[12].community_rep.all(),'ts': other9[0], 'crepTS' : other9[0].community_rep.all()})	

def about(request):
	topic_channel_list = TopicChannel.objects.all()
	#location_list = Location.objects.all()
	location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
	location_list_1 = location_list[0:8]
        location_list_2 = location_list[8:16]
        location_list_3 = location_list[16:]
        bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]

	return render_to_response('goonj/about.html', {'topic_channel_list' : topic_channel_list, 'location_list': location_list,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist})

def contact(request):
	topic_channel_list = TopicChannel.objects.all()
	#location_list = Location.objects.all()
	location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
	location_list_1 = location_list[0:8]
        location_list_2 = location_list[8:16]
        location_list_3 = location_list[16:]
        bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]

	return render_to_response('goonj/contact.html', {'topic_channel_list' : topic_channel_list, 'location_list': location_list,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist})

def team(request):
        topic_channel_list = TopicChannel.objects.all()
        #location_list = Location.objects.all()
	location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
	location_list_1 = location_list[0:8]
        location_list_2 = location_list[8:16]
        location_list_3 = location_list[16:]
        bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]

        return render_to_response('goonj/team.html', {'topic_channel_list' : topic_channel_list, 'location_list': location_list,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist})

def reports(request):
        topic_channel_list = TopicChannel.objects.all()
        #location_list = Location.objects.all()
	location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
	location_list_1 = location_list[0:8]
        location_list_2 = location_list[8:16]
        location_list_3 = location_list[16:]
        bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]

        return render_to_response('goonj/reports.html', {'topic_channel_list' : topic_channel_list, 'location_list': location_list,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist})

def govt_dept(request,gd_id):
	try:
		gdept = GovernmentDepartment.objects.get(pk=gd_id)
	except GovernmentDepartment.DoesNotExist:
		raise Http404
	else:
		topic_channel_list = TopicChannel.objects.all()
		#location_list = Location.objects.all()
		location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
		location_list_1 = location_list[0:8]
	        location_list_2 = location_list[8:16]
        	location_list_3 = location_list[16:]
        	bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]

		return render_to_response('goonj/gd.html', {'gd' : gdept, 'topic_channel_list' : topic_channel_list, 'location_list': location_list,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist})

def topic_channel(request,topic_channel_id):
	try:
		topicc = TopicChannel.objects.get(pk=topic_channel_id)
	except TopicChannel.DoesNotExist:
		raise Http404
	else:
		topic_channel_list = TopicChannel.objects.all()
		#location_list = Location.objects.all()
		location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
		location_list_1 = location_list[0:8]
	        location_list_2 = location_list[8:16]
        	location_list_3 = location_list[16:]
        	bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]

		story_list = topicc.story_set.all().order_by('-date')
		paginator = Paginator(story_list,25)
		page = request.GET.get('page')
		try:
			stories = paginator.page(page)
		except PageNotAnInteger:
			stories = paginator.page(1)
		except EmptyPage:
			stories = paginator.page(paginator.num_pages)
		return render_to_response('goonj/topic_channel.html', {'tc' : topicc, 'story_list' : stories, 'topic_channel_list' : topic_channel_list, 'location_list': location_list,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist})
	
def channel_partner(request,channel_partner_id):
	try:
		channelp = ChannelPartner.objects.get(pk=channel_partner_id)
	except ChannelPartner.DoesNotExist:
		raise Http404
	else:
		topic_channel_list = TopicChannel.objects.all()
		#location_list = Location.objects.all()
		location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
		location_list_1 = location_list[0:8]
	        location_list_2 = location_list[8:16]
        	location_list_3 = location_list[16:]
        	bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]

		return render_to_response('goonj/cp.html', {'cp' : channelp, 'topic_channel_list' : topic_channel_list, 'location_list': location_list,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist})

def community_rep(request,community_rep_id):
	try:
		communityr = CommunityRep.objects.get(pk=community_rep_id)
	except CommunityRep.DoesNotExist:
		raise Http404
	else:
		topic_channel_list = TopicChannel.objects.all()
		#location_list = Location.objects.all()
		location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
		location_list_1 = location_list[0:8]
	        location_list_2 = location_list[8:16]
        	location_list_3 = location_list[16:]
        	bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]

		return render_to_response('goonj/crep.html', {'crep' : communityr,'topic_channel_list' : topic_channel_list, 'location_list': location_list,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist})


def story(request, story_id):
	try:
		s = Story.objects.get(pk=story_id)
	except Story.DoesNotExist:
		raise Http404
	else:
		s.views_count+=1
		s.save()
		topic_channel_list = TopicChannel.objects.all()
		now = datetime.datetime.now()
		#location_list = Location.objects.all()
		location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
		location_list_1 = location_list[0:8]
	        location_list_2 = location_list[8:16]
        	location_list_3 = location_list[16:]
        	bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]

		loc = s.location.district
		return render_to_response('goonj/story.html', {'story' : s, 'loc': loc, 'crep' : s.community_rep.all(), 'now': now,'photoList': s.photo_id.all(),'topic_channel_list' : topic_channel_list, 'location_list': location_list,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist})

def issue(request, issue_id):
	try:
		i = Issue.objects.get(pk=issue_id)
	except Issue.DoesNotExist:
		raise Http404
	else:
		topic_channel_list = TopicChannel.objects.all()
		#location_list = Location.objects.all()
		location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
		location_list_1 = location_list[0:8]
	        location_list_2 = location_list[8:16]
        	location_list_3 = location_list[16:]
        	bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]

		return render_to_response('goonj/issue.html', {'issue' : i, 'story_list' : i.story_id.all().order_by('-date'),'topic_channel_list' : topic_channel_list, 'location_list': location_list,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist})

def location(request, location_id):
	try:
		l = Loc_district.objects.get(pk=location_id)
	except Location.DoesNotExist:
		raise Http404
	else:
		topic_channel_list = TopicChannel.objects.all()
		#location_list = Location.objects.all()
		location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
		location_list_1 = location_list[0:8]
	        location_list_2 = location_list[8:16]
        	location_list_3 = location_list[16:]
        	bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]

		story_list = []
		villages = l.loc_village_set.all()
		for v in villages:
			story_list += v.story_set.all().order_by('-date')
		#story_list = l.story_set.all().order_by('-date')
                paginator = Paginator(story_list,25)
                page = request.GET.get('page')
                try:
                        stories = paginator.page(page)
                except PageNotAnInteger:
                        stories = paginator.page(1)
                except EmptyPage:
                        stories = paginator.page(paginator.num_pages)
		
		return render_to_response('goonj/location.html', {'loc' : l,'topic_channel_list' : topic_channel_list, 'location_list': location_list, 'story_list' : stories,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist})

def top10(request):
	top_story_list = Story.objects.all().order_by('-views_count')[:10]
	topic_channel_list = TopicChannel.objects.all()
	location_list = Location.objects.all().order_by('name')
	return render_to_response('goonj/most_popular.html', {'top_story_list': top_story_list,'topic_channel_list' : topic_channel_list, 'location_list': location_list})	

def search(request):
	topic_channel_list = TopicChannel.objects.all()
	#location_list = Location.objects.all()
	location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
	return render_to_response('search/search.html',{'topic_channel_list' : topic_channel_list, 'location_list': location_list})

def all_stories(request):
	topic_channel_list = TopicChannel.objects.all()
	#location_list = Location.objects.all()
	location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
	location_list_1 = location_list[0:8]
        location_list_2 = location_list[8:16]
        location_list_3 = location_list[16:]
        bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]

	story_list = Story.objects.all().order_by('-date')
        paginator = Paginator(story_list,25)
        page = request.GET.get('page')
        try:
        	stories = paginator.page(page)
        except PageNotAnInteger:
     		stories = paginator.page(1)
        except EmptyPage:
        	stories = paginator.page(paginator.num_pages)
	return render_to_response('goonj/all_stories.html',{'topic_channel_list' : topic_channel_list, 'location_list': location_list, 'story_list': stories,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist})

def all_issues(request):
	topic_channel_list = TopicChannel.objects.all()
	#location_list = Location.objects.all()
	location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
	location_list_1 = location_list[0:8]
        location_list_2 = location_list[8:16]
        location_list_3 = location_list[16:]
        bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]

	issue_list = Issue.objects.all()
	return render_to_response('goonj/all_issues.html',{'topic_channel_list' : topic_channel_list, 'location_list': location_list, 'issue_list': issue_list,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist})

