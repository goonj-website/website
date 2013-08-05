# Create your views here.
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response
from goonj.models import Timeline, TimelineStoryRelation, Story,Issue,CommunityRep,GovernmentDepartment,ChannelPartner,TopicChannel,Location,Photo, Loc_country, Loc_state,Loc_district,Loc_block,Loc_village, Campaigns, CampaignStoryRelation, Advertiser, AdvertiserType, Impressions, ClickCount, StoryTcRelation, LocationForMap
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import template
from django.db.models import Q
from django.db import IntegrityError
register = template.Library()
import datetime
from django import forms
#from gmapi import maps
#from gmapi.forms.widgets import GoogleMap
import datetime

now = datetime.datetime.now()


def capture(request,id):
    click = ClickCount.objects.get(id = id)
    type = click.adv_type.ad_type
    if type == "NETWORK_SPONSOR":
        click.Network_spon +=1
    elif type == "CHANNEL_SPONSOR":
        click.Channel_spon +=1
    elif type == "CAMPAIGN_SPONSOR":
        click.Campaign_spon +=1
    elif type == "INDEPENDENT":
        click.Independent +=1
    click.save() 
    return render_to_response('goonj/capture.html', {'click' : click })

def timelines(request):     #FOR TESTING ONLY
    (ind1,ind2,ind3,ind4,ns) = 0,0,0,0,0
    (ind1c,ind2c,ind3c,ind4c,nsc) = 0,0,0,0,0
    network = AdvertiserType.objects.filter(Q(ad_type ="NETWORK_SPONSOR"), Q(end_date__gt = now)| Q(end_date__isnull=True))
    if len(network) >0 :
        ns = Impressions.objects.get(adv_type_id = network[0].id)
        if (ns.Network_spon < network[0].max_impressions)|(network[0].max_impressions is None):
            ns.Network_spon += 1
            ns.save()
    independent = AdvertiserType.objects.filter(Q(ad_type ="INDEPENDENT"), Q(end_date__gt = now)| Q(end_date__isnull=True))
    length = len(independent)
    if (length > 0):
        ind1 = Impressions.objects.get(adv_type_id = independent[0].id)
        if (ind1.Independent < independent[0].max_impressions)|(independent[0].max_impressions is None):
            ind1.Independent += 1
            ind1.save()
    if length > 1:
        ind2 = Impressions.objects.get(adv_type_id = independent[1].id)
        if (ind2.Independent < independent[1].max_impressions)|(independent[1].max_impressions is None):
            ind2.Independent += 1
            ind2.save()
    if length > 2:
        ind3 = Impressions.objects.get(adv_type_id = independent[2].id)
        if (ind3.Independent < independent[2].max_impressions)|(independent[2].max_impressions is None):
            ind3.Independent += 1
            ind3.save()
    if length > 3:
        ind4 = Impressions.objects.get(adv_type_id = independent[3].id)
        if (ind4.Independent < independent[3].max_impressions)|(independent[3].max_impressions is None):
            ind4.Independent += 1
            ind4.save()
    if len(network) >0 :
        nsc = ClickCount.objects.get(adv_type_id = network[0].id)
    if (length > 0):
        ind1c = ClickCount.objects.get(adv_type_id = independent[0].id)
    if length > 1:
        ind2c = ClickCount.objects.get(adv_type_id = independent[1].id)
    if length > 2:
        ind3c = ClickCount.objects.get(adv_type_id = independent[2].id)
    if length > 3:
        ind4c = ClickCount.objects.get(adv_type_id = independent[3].id)
    stories = []
    publish_dates = []
    events = Timeline.objects.all()
    topic_channel_list = TopicChannel.objects.all()
    entries = []
    ctr = 1
    while ctr < 9:
        cult2 = []
        cult = StoryTcRelation.objects.filter(topic_channel_id = ctr)
        for c in cult:
            if c.story.date.date() == now.date():
                cult2.append(c)
        cult = len(cult2)
        entries.append(cult)
        ctr = ctr + 1
    entries = zip(topic_channel_list,entries)
    location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
    location_list_1 = location_list[0:8]
    location_list_2 = location_list[8:16]
    location_list_3 = location_list[16:]
    bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]
    #zero = datetime.datetime.now()
    for t in events:
        story_ids = TimelineStoryRelation.objects.filter(timeline_id = t.event_id) #Returns related story ids
        list_of_ids = []
        for id in story_ids:
            list_of_ids.append(id.story_id) #list of related story ids
        stories_for_event = Story.objects.filter(story_id__in = list_of_ids).order_by('-date')
        stories.append(stories_for_event)   #nth element is list of stories related to nth event
    for story_list in stories:
        dates = []
        for story in story_list:
            dates.append(story.date)
        publish_dates.append(max(dates))
    return render_to_response('goonj/events.html', {'topic_channel_list' : topic_channel_list, 'location_list': location_list,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist,'events' : events, 'stories_list' :stories, 'publish_dates' : publish_dates, 'ind1c' :ind1c,'ind2c' :ind2c,'ind3c' :ind3c,'ind4c' :ind4c, 'networkc' : nsc, 'entries' : entries})
    
def campaigns(request):
    (ind1,ind2,ind3,ind4,ns) = 0,0,0,0,0
    (ind1c,ind2c,ind3c,ind4c,nsc) = 0,0,0,0,0
    network = AdvertiserType.objects.filter(Q(ad_type ="NETWORK_SPONSOR"), Q(end_date__gt = now)| Q(end_date__isnull=True))
    if len(network) >0 :
        ns = Impressions.objects.get(adv_type_id = network[0].id)
        if (ns.Network_spon < network[0].max_impressions)|(network[0].max_impressions is None):
            ns.Network_spon += 1
            ns.save()
    independent = AdvertiserType.objects.filter(Q(ad_type ="INDEPENDENT"), Q(end_date__gt = now)| Q(end_date__isnull=True))
    length = len(independent)
    if (length > 0):
        ind1 = Impressions.objects.get(adv_type_id = independent[0].id)
        if (ind1.Independent < independent[0].max_impressions)|(independent[0].max_impressions is None):
            ind1.Independent += 1
            ind1.save()
    if length > 1:
        ind2 = Impressions.objects.get(adv_type_id = independent[1].id)
        if (ind2.Independent < independent[1].max_impressions)|(independent[1].max_impressions is None):
            ind2.Independent += 1
            ind2.save()
    if length > 2:
        ind3 = Impressions.objects.get(adv_type_id = independent[2].id)
        if (ind3.Independent < independent[2].max_impressions)|(independent[2].max_impressions is None):
            ind3.Independent += 1
            ind3.save()
    if length > 3:
        ind4 = Impressions.objects.get(adv_type_id = independent[3].id)
        if (ind4.Independent < independent[3].max_impressions)|(independent[3].max_impressions is None):
            ind4.Independent += 1
            ind4.save()
    if len(network) >0 :
        nsc = ClickCount.objects.get(adv_type_id = network[0].id)
    if (length > 0):
        ind1c = ClickCount.objects.get(adv_type_id = independent[0].id)
    if length > 1:
        ind2c = ClickCount.objects.get(adv_type_id = independent[1].id)
    if length > 2:
        ind3c = ClickCount.objects.get(adv_type_id = independent[2].id)
    if length > 3:
        ind4c = ClickCount.objects.get(adv_type_id = independent[3].id)
    stories = []
    publish_dates = []
    campaigns = Campaigns.objects.all()
    topic_channel_list = TopicChannel.objects.all()
    entries = []
    ctr = 1
    while ctr < 9:
        cult2 = []
        cult = StoryTcRelation.objects.filter(topic_channel_id = ctr)
        for c in cult:
            if c.story.date.date() == now.date():
                cult2.append(c)
        cult = len(cult2)
        entries.append(cult)
        ctr = ctr + 1
    entries = zip(topic_channel_list,entries)
    #location_list = Location.objects.all()
    location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
    location_list_1 = location_list[0:8]
    location_list_2 = location_list[8:16]
    location_list_3 = location_list[16:]
    bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]
    for c in campaigns:
        story_ids = CampaignStoryRelation.objects.filter(campaign_id = c.c_id) #Returns related story ids
        list_of_ids = []
        for id in story_ids:
            list_of_ids.append(id.story_id) #list of related story ids
        stories_for_event = Story.objects.filter(story_id__in = list_of_ids).order_by('-date')
        stories.append(stories_for_event)   #nth element is list of stories related to nth event
    for story_list in stories:
        dates = []
        for story in story_list:
            dates.append(story.date)
        publish_dates.append(max(dates))    
    return render_to_response('goonj/campaigns.html', {'topic_channel_list' : topic_channel_list, 'location_list': location_list,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist,'campaigns' : campaigns, 'stories_list' : stories, 'publish_dates' : publish_dates, 'ind1c' :ind1c,'ind2c' :ind2c,'ind3c' :ind3c,'ind4c' :ind4c, 'networkc' : nsc, 'entries' : entries}) 


#class MapForm(forms.Form):
#    map = forms.Field(widget=GoogleMap(attrs={'width':510, 'height':510}))

def MAPS(request):
    gmap = maps.Map(opts = {
        'center': maps.LatLng(38, -97),
        'mapTypeId': maps.MapTypeId.ROADMAP,
        'zoom': 3,
        'mapTypeControlOptions': {
             'style': maps.MapTypeControlStyle.DROPDOWN_MENU
        },
    })
    marker_list = LocationForMap.objects.all()
    #markers = []
    for m in marker_list:
        marker = maps.Marker(opts = {
            'map': gmap,
            'position': maps.LatLng(m.latitude, m.longitude),
        })
        maps.event.addListener(marker, 'mouseover', 'myobj.markerOver')
        maps.event.addListener(marker, 'mouseout', 'myobj.markerOut')
        info = maps.InfoWindow({
            'content': m.information,
            'disableAutoPan': False
        })
        info.open(gmap, marker) 
  #     markers.append(m)
#     cluster = maps.MarkerClusterer(gmap, markers)
    context = {'form': MapForm(initial={'map': gmap})}
    return render_to_response('goonj/maps.html', context)


def index(request):
    (ind1,ind2,ind3,ind4,ns) = 0,0,0,0,0
    (ind1c,ind2c,ind3c,ind4c,nsc) = 0,0,0,0,0
    network = AdvertiserType.objects.filter(Q(ad_type ="NETWORK_SPONSOR"), Q(end_date__gt = now)| Q(end_date__isnull=True))
    if len(network) >0 :
        ns = Impressions.objects.get(adv_type_id = network[0].id)
        if (ns.Network_spon < network[0].max_impressions)|(network[0].max_impressions is None):
            ns.Network_spon += 1
            ns.save()
    independent = AdvertiserType.objects.filter(Q(ad_type ="INDEPENDENT"), Q(end_date__gt = now)| Q(end_date__isnull=True))
    length = len(independent)
    if (length > 0):
        ind1 = Impressions.objects.get(adv_type_id = independent[0].id)
        if (ind1.Independent < independent[0].max_impressions)|(independent[0].max_impressions is None):
            ind1.Independent += 1
            ind1.save()
    if length > 1:
        ind2 = Impressions.objects.get(adv_type_id = independent[1].id)
        if (ind2.Independent < independent[1].max_impressions)|(independent[1].max_impressions is None):
            ind2.Independent += 1
            ind2.save()
    if length > 2:
        ind3 = Impressions.objects.get(adv_type_id = independent[2].id)
        if (ind3.Independent < independent[2].max_impressions)|(independent[2].max_impressions is None):
            ind3.Independent += 1
            ind3.save()
    if length > 3:
        ind4 = Impressions.objects.get(adv_type_id = independent[3].id)
        if (ind4.Independent < independent[3].max_impressions)|(independent[3].max_impressions is None):
            ind4.Independent += 1
            ind4.save()
    if len(network) >0 :
        nsc = ClickCount.objects.get(adv_type_id = network[0].id)
    if (length > 0):
        ind1c = ClickCount.objects.get(adv_type_id = independent[0].id)
    if length > 1:
        ind2c = ClickCount.objects.get(adv_type_id = independent[1].id)
    if length > 2:
        ind3c = ClickCount.objects.get(adv_type_id = independent[2].id)
    if length > 3:
        ind4c = ClickCount.objects.get(adv_type_id = independent[3].id)
    lsl = Story.objects.all().order_by('-date')[:13]
    top_story_list = Story.objects.all().order_by('-views_count')[:5]
    topic_channel_list = TopicChannel.objects.all()
    entries = []
    ctr = 1
    while ctr < 9:
        cult2 = []
        cult = StoryTcRelation.objects.filter(topic_channel_id = ctr)
        for c in cult:
            if c.story.date.date() == now.date():
                cult2.append(c)
        cult = len(cult2)
        entries.append(cult)
        ctr = ctr + 1
    entries = zip(topic_channel_list,entries)
    location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
    location_list_1 = location_list[0:8]
    location_list_2 = location_list[8:16]
    location_list_3 = location_list[16:]
    bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]
    other9 = []
    for st in lsl: 
        #if (st.top_story != True):
            other9.append(st)
    return render_to_response('goonj/index (copy).html', {'l0': other9[1],'l1': other9[2],'l2': other9[3],'l3': other9[4],'l4': other9[5],'l5': other9[6],'l6': other9[7],'l7': other9[8],'l8': other9[9],'l9': other9[10],'l10': other9[11],'l11': other9[12],'top_story_list' : top_story_list, 'topic_channel_list' : topic_channel_list, 'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist,'crep0' : other9[1].community_rep.all(), 'crep1' : other9[2].community_rep.all(), 'crep2' : other9[3].community_rep.all(), 'crep3' : other9[4].community_rep.all(), 'crep4' : other9[5].community_rep.all(), 'crep5' : other9[6].community_rep.all(), 'crep6' : other9[7].community_rep.all(), 'crep7' : other9[8].community_rep.all(), 'crep8' : other9[9].community_rep.all(), 'crep9' : other9[10].community_rep.all(),'crep10' : other9[11].community_rep.all(),'crep11' : other9[12].community_rep.all(),'ts': other9[0], 'crepTS' : other9[0].community_rep.all(),'ind1c' :ind1c,'ind2c' :ind2c,'ind3c' :ind3c,'ind4c' :ind4c, 'networkc' : nsc, 'entries' : entries})   

def about(request):
    (ind1,ind2,ind3,ind4,ns) = 0,0,0,0,0
    (ind1c,ind2c,ind3c,ind4c,nsc) = 0,0,0,0,0
    network = AdvertiserType.objects.filter(Q(ad_type ="NETWORK_SPONSOR"), Q(end_date__gt = now)| Q(end_date__isnull=True))
    if len(network) >0 :
        ns = Impressions.objects.get(adv_type_id = network[0].id)
        if (ns.Network_spon < network[0].max_impressions)|(network[0].max_impressions is None):
            ns.Network_spon += 1
            ns.save()
    independent = AdvertiserType.objects.filter(Q(ad_type ="INDEPENDENT"), Q(end_date__gt = now)| Q(end_date__isnull=True))
    length = len(independent)
    if (length > 0):
        ind1 = Impressions.objects.get(adv_type_id = independent[0].id)
        if (ind1.Independent < independent[0].max_impressions)|(independent[0].max_impressions is None):
            ind1.Independent += 1
            ind1.save()
    if length > 1:
        ind2 = Impressions.objects.get(adv_type_id = independent[1].id)
        if (ind2.Independent < independent[1].max_impressions)|(independent[1].max_impressions is None):
            ind2.Independent += 1
            ind2.save()
    if length > 2:
        ind3 = Impressions.objects.get(adv_type_id = independent[2].id)
        if (ind3.Independent < independent[2].max_impressions)|(independent[2].max_impressions is None):
            ind3.Independent += 1
            ind3.save()
    if length > 3:
        ind4 = Impressions.objects.get(adv_type_id = independent[3].id)
        if (ind4.Independent < independent[3].max_impressions)|(independent[3].max_impressions is None):
            ind4.Independent += 1
            ind4.save()
    if len(network) >0 :
        nsc = ClickCount.objects.get(adv_type_id = network[0].id)
    if (length > 0):
        ind1c = ClickCount.objects.get(adv_type_id = independent[0].id)
    if length > 1:
        ind2c = ClickCount.objects.get(adv_type_id = independent[1].id)
    if length > 2:
        ind3c = ClickCount.objects.get(adv_type_id = independent[2].id)
    if length > 3:
        ind4c = ClickCount.objects.get(adv_type_id = independent[3].id)
    #location_list = Location.objects.all()
    topic_channel_list = TopicChannel.objects.all()
    entries = []
    ctr = 1
    while ctr < 9:
        cult2 = []
        cult = StoryTcRelation.objects.filter(topic_channel_id = ctr)
        for c in cult:
            if c.story.date.date() == now.date():
                cult2.append(c)
        cult = len(cult2)
        entries.append(cult)
        ctr = ctr + 1
    entries = zip(topic_channel_list,entries)
    location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
    location_list_1 = location_list[0:8]
    location_list_2 = location_list[8:16]
    location_list_3 = location_list[16:]
    bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]

    return render_to_response('goonj/about.html', {'topic_channel_list' : topic_channel_list, 'location_list': location_list,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist, 'ind1c' :ind1c,'ind2c' :ind2c,'ind3c' :ind3c,'ind4c' :ind4c, 'networkc' : nsc, 'entries' : entries}) 

def contact(request):
    (ind1,ind2,ind3,ind4,ns) = 0,0,0,0,0
    (ind1c,ind2c,ind3c,ind4c,nsc) = 0,0,0,0,0
    network = AdvertiserType.objects.filter(Q(ad_type ="NETWORK_SPONSOR"), Q(end_date__gt = now)| Q(end_date__isnull=True))
    if len(network) >0 :
        ns = Impressions.objects.get(adv_type_id = network[0].id)
        if (ns.Network_spon < network[0].max_impressions)|(network[0].max_impressions is None):
            ns.Network_spon += 1
            ns.save()
    independent = AdvertiserType.objects.filter(Q(ad_type ="INDEPENDENT"), Q(end_date__gt = now)| Q(end_date__isnull=True))
    length = len(independent)
    if (length > 0):
        ind1 = Impressions.objects.get(adv_type_id = independent[0].id)
        if (ind1.Independent < independent[0].max_impressions)|(independent[0].max_impressions is None):
            ind1.Independent += 1
            ind1.save()
    if length > 1:
        ind2 = Impressions.objects.get(adv_type_id = independent[1].id)
        if (ind2.Independent < independent[1].max_impressions)|(independent[1].max_impressions is None):
            ind2.Independent += 1
            ind2.save()
    if length > 2:
        ind3 = Impressions.objects.get(adv_type_id = independent[2].id)
        if (ind3.Independent < independent[2].max_impressions)|(independent[2].max_impressions is None):
            ind3.Independent += 1
            ind3.save()
    if length > 3:
        ind4 = Impressions.objects.get(adv_type_id = independent[3].id)
        if (ind4.Independent < independent[3].max_impressions)|(independent[3].max_impressions is None):
            ind4.Independent += 1
            ind4.save()
    if len(network) >0 :
        nsc = ClickCount.objects.get(adv_type_id = network[0].id)
    if (length > 0):
        ind1c = ClickCount.objects.get(adv_type_id = independent[0].id)
    if length > 1:
        ind2c = ClickCount.objects.get(adv_type_id = independent[1].id)
    if length > 2:
        ind3c = ClickCount.objects.get(adv_type_id = independent[2].id)
    if length > 3:
        ind4c = ClickCount.objects.get(adv_type_id = independent[3].id)
    topic_channel_list = TopicChannel.objects.all()
    entries = []
    ctr = 1
    while ctr < 9:
        cult2 = []
        cult = StoryTcRelation.objects.filter(topic_channel_id = ctr)
        for c in cult:
            if c.story.date.date() == now.date():
                cult2.append(c)
        cult = len(cult2)
        entries.append(cult)
        ctr = ctr + 1
    entries = zip(topic_channel_list,entries)
    #location_list = Location.objects.all()
    location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
    location_list_1 = location_list[0:8]
    location_list_2 = location_list[8:16]
    location_list_3 = location_list[16:]
    bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]

    return render_to_response('goonj/contact.html', {'topic_channel_list' : topic_channel_list, 'location_list': location_list,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist,'ind1c' :ind1c,'ind2c' :ind2c,'ind3c' :ind3c,'ind4c' :ind4c, 'networkc' : nsc, 'entries' : entries}) 

def team(request):
    (ind1,ind2,ind3,ind4,ns) = 0,0,0,0,0
    (ind1c,ind2c,ind3c,ind4c,nsc) = 0,0,0,0,0
    network = AdvertiserType.objects.filter(Q(ad_type ="NETWORK_SPONSOR"), Q(end_date__gt = now)| Q(end_date__isnull=True))
    if len(network) >0 :
        ns = Impressions.objects.get(adv_type_id = network[0].id)
        if (ns.Network_spon < network[0].max_impressions)|(network[0].max_impressions is None):
            ns.Network_spon += 1
            ns.save()
    independent = AdvertiserType.objects.filter(Q(ad_type ="INDEPENDENT"), Q(end_date__gt = now)| Q(end_date__isnull=True))
    length = len(independent)
    if (length > 0):
        ind1 = Impressions.objects.get(adv_type_id = independent[0].id)
        if (ind1.Independent < independent[0].max_impressions)|(independent[0].max_impressions is None):
            ind1.Independent += 1
            ind1.save()
    if length > 1:
        ind2 = Impressions.objects.get(adv_type_id = independent[1].id)
        if (ind2.Independent < independent[1].max_impressions)|(independent[1].max_impressions is None):
            ind2.Independent += 1
            ind2.save()
    if length > 2:
        ind3 = Impressions.objects.get(adv_type_id = independent[2].id)
        if (ind3.Independent < independent[2].max_impressions)|(independent[2].max_impressions is None):
            ind3.Independent += 1
            ind3.save()
    if length > 3:
        ind4 = Impressions.objects.get(adv_type_id = independent[3].id)
        if (ind4.Independent < independent[3].max_impressions)|(independent[3].max_impressions is None):
            ind4.Independent += 1
            ind4.save()
    if len(network) >0 :
        nsc = ClickCount.objects.get(adv_type_id = network[0].id)
    if (length > 0):
        ind1c = ClickCount.objects.get(adv_type_id = independent[0].id)
    if length > 1:
        ind2c = ClickCount.objects.get(adv_type_id = independent[1].id)
    if length > 2:
        ind3c = ClickCount.objects.get(adv_type_id = independent[2].id)
    if length > 3:
        ind4c = ClickCount.objects.get(adv_type_id = independent[3].id)
    topic_channel_list = TopicChannel.objects.all()
    entries = []
    ctr = 1
    while ctr < 9:
        cult2 = []
        cult = StoryTcRelation.objects.filter(topic_channel_id = ctr)
        for c in cult:
            if c.story.date.date() == now.date():
                cult2.append(c)
        cult = len(cult2)
        entries.append(cult)
        ctr = ctr + 1
    entries = zip(topic_channel_list,entries)
    #location_list = Location.objects.all()
    location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
    location_list_1 = location_list[0:8]
    location_list_2 = location_list[8:16]
    location_list_3 = location_list[16:]
    bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]
    return render_to_response('goonj/team.html', {'topic_channel_list' : topic_channel_list, 'location_list': location_list,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist,'ind1c' :ind1c,'ind2c' :ind2c,'ind3c' :ind3c,'ind4c' :ind4c, 'networkc' : nsc, 'entries' : entries}) 

def reports(request):
    topic_channel_list = TopicChannel.objects.all()
    entries = []
    ctr = 1
    while ctr < 9:
        cult2 = []
        cult = StoryTcRelation.objects.filter(topic_channel_id = ctr)
        for c in cult:
            if c.story.date.date() == now.date():
                cult2.append(c)
        cult = len(cult2)
        entries.append(cult)
        ctr = ctr + 1
    entries = zip(topic_channel_list,entries)
    #location_list = Location.objects.all()
    location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
    location_list_1 = location_list[0:8]
    location_list_2 = location_list[8:16]
    location_list_3 = location_list[16:]
    bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]
    (ind1,ind2,ind3,ind4,ns) = 0,0,0,0,0
    (ind1c,ind2c,ind3c,ind4c,nsc) = 0,0,0,0,0
    network = AdvertiserType.objects.filter(Q(ad_type ="NETWORK_SPONSOR"), Q(end_date__gt = now)| Q(end_date__isnull=True))
    if len(network) >0 :
        ns = Impressions.objects.get(adv_type_id = network[0].id)
        if (ns.Network_spon < network[0].max_impressions)|(network[0].max_impressions is None):
            ns.Network_spon += 1
            ns.save()
    independent = AdvertiserType.objects.filter(Q(ad_type ="INDEPENDENT"), Q(end_date__gt = now)| Q(end_date__isnull=True))
    length = len(independent)
    if (length > 0):
        ind1 = Impressions.objects.get(adv_type_id = independent[0].id)
        if (ind1.Independent < independent[0].max_impressions)|(independent[0].max_impressions is None):
            ind1.Independent += 1
            ind1.save()
    if length > 1:
        ind2 = Impressions.objects.get(adv_type_id = independent[1].id)
        if (ind2.Independent < independent[1].max_impressions)|(independent[1].max_impressions is None):
            ind2.Independent += 1
            ind2.save()
    if length > 2:
        ind3 = Impressions.objects.get(adv_type_id = independent[2].id)
        if (ind3.Independent < independent[2].max_impressions)|(independent[2].max_impressions is None):
            ind3.Independent += 1
            ind3.save()
    if length > 3:
        ind4 = Impressions.objects.get(adv_type_id = independent[3].id)
        if (ind4.Independent < independent[3].max_impressions)|(independent[3].max_impressions is None):
            ind4.Independent += 1
            ind4.save()
    if len(network) >0 :
        nsc = ClickCount.objects.get(adv_type_id = network[0].id)
    if (length > 0):
        ind1c = ClickCount.objects.get(adv_type_id = independent[0].id)
    if length > 1:
        ind2c = ClickCount.objects.get(adv_type_id = independent[1].id)
    if length > 2:
        ind3c = ClickCount.objects.get(adv_type_id = independent[2].id)
    if length > 3:
        ind4c = ClickCount.objects.get(adv_type_id = independent[3].id)
    return render_to_response('goonj/reports.html', {'topic_channel_list' : topic_channel_list, 'location_list': location_list,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist, 'ind1c' :ind1c,'ind2c' :ind2c,'ind3c' :ind3c,'ind4c' :ind4c, 'networkc' : nsc, 'entries' : entries}) 
    
def govt_dept(request,gd_id):
    try:
        gdept = GovernmentDepartment.objects.get(pk=gd_id)
    except GovernmentDepartment.DoesNotExist:
        raise Http404
    else:
        topic_channel_list = TopicChannel.objects.all()
        entries = []
        ctr = 1
        while ctr < 9:
            cult2 = []
            cult = StoryTcRelation.objects.filter(topic_channel_id = ctr)
            for c in cult:
                if c.story.date.date() == now.date():
                    cult2.append(c)
            cult = len(cult2)
            entries.append(cult)
            ctr = ctr + 1
        entries = zip(topic_channel_list,entries)
        #location_list = Location.objects.all()
        location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
        location_list_1 = location_list[0:8]
        location_list_2 = location_list[8:16]
        location_list_3 = location_list[16:]
        bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]
        (ind1,ind2,ind3,ind4,ns) = 0,0,0,0,0
        (ind1c,ind2c,ind3c,ind4c,nsc) = 0,0,0,0,0
        network = AdvertiserType.objects.filter(Q(ad_type ="NETWORK_SPONSOR"), Q(end_date__gt = now)| Q(end_date__isnull=True))
        if len(network) >0 :
            ns = Impressions.objects.get(adv_type_id = network[0].id)
            if (ns.Network_spon < network[0].max_impressions)|(network[0].max_impressions is None):
                ns.Network_spon += 1
                ns.save()
        independent = AdvertiserType.objects.filter(Q(ad_type ="INDEPENDENT"), Q(end_date__gt = now)| Q(end_date__isnull=True))
        length = len(independent)
        if (length > 0):
            ind1 = Impressions.objects.get(adv_type_id = independent[0].id)
            if (ind1.Independent < independent[0].max_impressions)|(independent[0].max_impressions is None):
                ind1.Independent += 1
                ind1.save()
        if length > 1:
            ind2 = Impressions.objects.get(adv_type_id = independent[1].id)
            if (ind2.Independent < independent[1].max_impressions)|(independent[1].max_impressions is None):
                ind2.Independent += 1
                ind2.save()
        if length > 2:
            ind3 = Impressions.objects.get(adv_type_id = independent[2].id)
            if (ind3.Independent < independent[2].max_impressions)|(independent[2].max_impressions is None):
                ind3.Independent += 1
                ind3.save()
        if length > 3:
            ind4 = Impressions.objects.get(adv_type_id = independent[3].id)
            if (ind4.Independent < independent[3].max_impressions)|(independent[3].max_impressions is None):
                ind4.Independent += 1
                ind4.save()
        if len(network) >0 :
            nsc = ClickCount.objects.get(adv_type_id = network[0].id)
        if (length > 0):
            ind1c = ClickCount.objects.get(adv_type_id = independent[0].id)
        if length > 1:
            ind2c = ClickCount.objects.get(adv_type_id = independent[1].id)
        if length > 2:
            ind3c = ClickCount.objects.get(adv_type_id = independent[2].id)
        if length > 3:
            ind4c = ClickCount.objects.get(adv_type_id = independent[3].id)
        return render_to_response('goonj/gd.html', {'gd' : gdept, 'topic_channel_list' : topic_channel_list, 'location_list': location_list,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist,'ind1c' :ind1c,'ind2c' :ind2c,'ind3c' :ind3c,'ind4c' :ind4c, 'networkc' : nsc, 'entries' : entries}) 

def topic_channel(request,topic_channel_id):
    try:
        topicc = TopicChannel.objects.get(pk=topic_channel_id)
    except TopicChannel.DoesNotExist:
        raise Http404
    else:
        (ind1,ind2,ind3,ind4,ns,imp) = 0,0,0,0,0,0
        (ind1c,ind2c,ind3c,ind4c,nsc) = 0,0,0,0,0
        network = AdvertiserType.objects.filter(Q(ad_type ="NETWORK_SPONSOR"), Q(end_date__gt = now)| Q(end_date__isnull=True))
        if len(network) >0 :
            ns = Impressions.objects.get(adv_type_id = network[0].id)
            if (ns.Network_spon < network[0].max_impressions)|(network[0].max_impressions is None):
                ns.Network_spon += 1
                ns.save()
        independent = AdvertiserType.objects.filter(Q(ad_type ="INDEPENDENT"), Q(end_date__gt = now)| Q(end_date__isnull=True))
        length = len(independent)
        if (length > 0):
            ind1 = Impressions.objects.get(adv_type_id = independent[0].id)
            if (ind1.Independent < independent[0].max_impressions)|(independent[0].max_impressions is None):
                ind1.Independent += 1
                ind1.save()
        if length > 1:
            ind2 = Impressions.objects.get(adv_type_id = independent[1].id)
            if (ind2.Independent < independent[1].max_impressions)|(independent[1].max_impressions is None):
                ind2.Independent += 1
                ind2.save()
        if length > 2:
            ind3 = Impressions.objects.get(adv_type_id = independent[2].id)
            if (ind3.Independent < independent[2].max_impressions)|(independent[2].max_impressions is None):
                ind3.Independent += 1
                ind3.save()
        if length > 3:
            ind4 = Impressions.objects.get(adv_type_id = independent[3].id)
            if (ind4.Independent < independent[3].max_impressions)|(independent[3].max_impressions is None):
                ind4.Independent += 1
                ind4.save()
        if len(network) >0 :
            nsc = ClickCount.objects.get(adv_type_id = network[0].id)
        if (length > 0):
            ind1c = ClickCount.objects.get(adv_type_id = independent[0].id)
        if length > 1:
            ind2c = ClickCount.objects.get(adv_type_id = independent[1].id)
        if length > 2:
            ind3c = ClickCount.objects.get(adv_type_id = independent[2].id)
        if length > 3:
            ind4c = ClickCount.objects.get(adv_type_id = independent[3].id)
        cs = AdvertiserType.objects.filter(ad_type ="CHANNEL_SPONSOR", end_date__isnull=True,Topic_channel = topic_channel_id)
        if len(cs) >0 :
            imp = Impressions.objects.get(adv_type_id = cs[0].id)
            imp.Channel_spon += 1
            imp.save()
            imp = ClickCount.objects.get(adv_type_id = cs[0].id)
        topic_channel_list = TopicChannel.objects.all()
        entries = []
        ctr = 1
        while ctr < 9:
            cult2 = []
            cult = StoryTcRelation.objects.filter(topic_channel_id = ctr)
            for c in cult:
                if c.story.date.date() == now.date():
                    cult2.append(c)
            cult = len(cult2)
            entries.append(cult)
            ctr = ctr + 1
        entries = zip(topic_channel_list,entries)
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
        return render_to_response('goonj/topic_channel.html', { 'channel' : imp , 'tc' : topicc, 'story_list' : stories, 'topic_channel_list' : topic_channel_list, 'location_list': location_list,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist, 'ind1c' :ind1c,'ind2c' :ind2c,'ind3c' :ind3c,'ind4c' :ind4c, 'networkc' : nsc, 'entries' : entries}) 
    
def channel_partner(request,channel_partner_id):
    try:
        channelp = ChannelPartner.objects.get(pk=channel_partner_id)
    except ChannelPartner.DoesNotExist:
        raise Http404
    else:
        topic_channel_list = TopicChannel.objects.all()
        entries = []
        ctr = 1
        while ctr < 9:
            cult2 = []
            cult = StoryTcRelation.objects.filter(topic_channel_id = ctr)
            for c in cult:
                if c.story.date.date() == now.date():
                    cult2.append(c)
            cult = len(cult2)
            entries.append(cult)
            ctr = ctr + 1
        entries = zip(topic_channel_list,entries)
        #location_list = Location.objects.all()
        location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
        location_list_1 = location_list[0:8]
        location_list_2 = location_list[8:16]
        location_list_3 = location_list[16:]
        bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]
        (ind1,ind2,ind3,ind4,ns) = 0,0,0,0,0
        (ind1c,ind2c,ind3c,ind4c,nsc) = 0,0,0,0,0
        network = AdvertiserType.objects.filter(Q(ad_type ="NETWORK_SPONSOR"), Q(end_date__gt = now)| Q(end_date__isnull=True))
        if len(network) >0 :
            ns = Impressions.objects.get(adv_type_id = network[0].id)
            if (ns.Network_spon < network[0].max_impressions)|(network[0].max_impressions is None):
                ns.Network_spon += 1
                ns.save()
        independent = AdvertiserType.objects.filter(Q(ad_type ="INDEPENDENT"), Q(end_date__gt = now)| Q(end_date__isnull=True))
        length = len(independent)
        if (length > 0):
            ind1 = Impressions.objects.get(adv_type_id = independent[0].id)
            if (ind1.Independent < independent[0].max_impressions)|(independent[0].max_impressions is None):
                ind1.Independent += 1
                ind1.save()
        if length > 1:
            ind2 = Impressions.objects.get(adv_type_id = independent[1].id)
            if (ind2.Independent < independent[1].max_impressions)|(independent[1].max_impressions is None):
                ind2.Independent += 1
                ind2.save()
        if length > 2:
            ind3 = Impressions.objects.get(adv_type_id = independent[2].id)
            if (ind3.Independent < independent[2].max_impressions)|(independent[2].max_impressions is None):
                ind3.Independent += 1
                ind3.save()
        if length > 3:
            ind4 = Impressions.objects.get(adv_type_id = independent[3].id)
            if (ind4.Independent < independent[3].max_impressions)|(independent[3].max_impressions is None):
                ind4.Independent += 1
                ind4.save()
        if len(network) >0 :
            nsc = ClickCount.objects.get(adv_type_id = network[0].id)
        if (length > 0):
            ind1c = ClickCount.objects.get(adv_type_id = independent[0].id)
        if length > 1:
            ind2c = ClickCount.objects.get(adv_type_id = independent[1].id)
        if length > 2:
            ind3c = ClickCount.objects.get(adv_type_id = independent[2].id)
        if length > 3:
            ind4c = ClickCount.objects.get(adv_type_id = independent[3].id)
        return render_to_response('goonj/cp.html', {'cp' : channelp, 'topic_channel_list' : topic_channel_list, 'location_list': location_list,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist, 'ind1c' :ind1c,'ind2c' :ind2c,'ind3c' :ind3c,'ind4c' :ind4c, 'networkc' : nsc, 'entries' : entries}) 

def community_rep(request,community_rep_id):
    try:
        communityr = CommunityRep.objects.get(pk=community_rep_id)
    except CommunityRep.DoesNotExist:
        raise Http404
    else:
        (ind1,ind2,ind3,ind4,ns) = 0,0,0,0,0
        (ind1c,ind2c,ind3c,ind4c,nsc) = 0,0,0,0,0
        network = AdvertiserType.objects.filter(Q(ad_type ="NETWORK_SPONSOR"), Q(end_date__gt = now)| Q(end_date__isnull=True))
        if len(network) >0 :
            ns = Impressions.objects.get(adv_type_id = network[0].id)
            if (ns.Network_spon < network[0].max_impressions)|(network[0].max_impressions is None):
                ns.Network_spon += 1
                ns.save()
        independent = AdvertiserType.objects.filter(Q(ad_type ="INDEPENDENT"), Q(end_date__gt = now)| Q(end_date__isnull=True))
        length = len(independent)
        if (length > 0):
            ind1 = Impressions.objects.get(adv_type_id = independent[0].id)
            if (ind1.Independent < independent[0].max_impressions)|(independent[0].max_impressions is None):
                ind1.Independent += 1
                ind1.save()
        if length > 1:
            ind2 = Impressions.objects.get(adv_type_id = independent[1].id)
            if (ind2.Independent < independent[1].max_impressions)|(independent[1].max_impressions is None):
                ind2.Independent += 1
                ind2.save()
        if length > 2:
            ind3 = Impressions.objects.get(adv_type_id = independent[2].id)
            if (ind3.Independent < independent[2].max_impressions)|(independent[2].max_impressions is None):
                ind3.Independent += 1
                ind3.save()
        if length > 3:
            ind4 = Impressions.objects.get(adv_type_id = independent[3].id)
            if (ind4.Independent < independent[3].max_impressions)|(independent[3].max_impressions is None):
                ind4.Independent += 1
                ind4.save()
        if len(network) >0 :
            nsc = ClickCount.objects.get(adv_type_id = network[0].id)
        if (length > 0):
            ind1c = ClickCount.objects.get(adv_type_id = independent[0].id)
        if length > 1:
            ind2c = ClickCount.objects.get(adv_type_id = independent[1].id)
        if length > 2:
            ind3c = ClickCount.objects.get(adv_type_id = independent[2].id)
        if length > 3:
            ind4c = ClickCount.objects.get(adv_type_id = independent[3].id)
        topic_channel_list = TopicChannel.objects.all()
        entries = []
        ctr = 1
        while ctr < 9:
            cult2 = []
            cult = StoryTcRelation.objects.filter(topic_channel_id = ctr)
            for c in cult:
                if c.story.date.date() == now.date():
                    cult2.append(c)
            cult = len(cult2)
            entries.append(cult)
            ctr = ctr + 1
        entries = zip(topic_channel_list,entries)
        #location_list = Location.objects.all()
        location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
        location_list_1 = location_list[0:8]
        location_list_2 = location_list[8:16]
        location_list_3 = location_list[16:]
        bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]
        return render_to_response('goonj/crep.html', {'crep' : communityr,'topic_channel_list' : topic_channel_list, 'location_list': location_list,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist,'ind1c' :ind1c,'ind2c' :ind2c,'ind3c' :ind3c,'ind4c' :ind4c, 'networkc' : nsc, 'entries' : entries}) 


def story(request, story_id):
    try:
        s = Story.objects.get(pk=story_id)
    except Story.DoesNotExist:
        raise Http404
    else:
        now = datetime.datetime.now()
        imp = []
        (ind1,ind2,ind3,ind4,ns) = 0,0,0,0,0
        (ind1c,ind2c,ind3c,ind4c,nsc) = 0,0,0,0,0
        network = AdvertiserType.objects.filter(Q(ad_type ="NETWORK_SPONSOR"), Q(end_date__gt = now)| Q(end_date__isnull=True))
        if len(network) >0 :
            ns = Impressions.objects.get(adv_type_id = network[0].id)
            if (ns.Network_spon < network[0].max_impressions)|(network[0].max_impressions is None):
                ns.Network_spon += 1
                ns.save()
        independent = AdvertiserType.objects.filter(Q(ad_type ="INDEPENDENT"), Q(end_date__gt = now)| Q(end_date__isnull=True))
        length = len(independent)
        if (length > 0):
            ind1 = Impressions.objects.get(adv_type_id = independent[0].id)
            if (ind1.Independent < independent[0].max_impressions)|(independent[0].max_impressions is None):
                ind1.Independent += 1
                ind1.save()
        if length > 1:
            ind2 = Impressions.objects.get(adv_type_id = independent[1].id)
            if (ind2.Independent < independent[1].max_impressions)|(independent[1].max_impressions is None):
                ind2.Independent += 1
                ind2.save()
        if length > 2:
            ind3 = Impressions.objects.get(adv_type_id = independent[2].id)
            if (ind3.Independent < independent[2].max_impressions)|(independent[2].max_impressions is None):
                ind3.Independent += 1
                ind3.save()
        if length > 3:
            ind4 = Impressions.objects.get(adv_type_id = independent[3].id)
            if (ind4.Independent < independent[3].max_impressions)|(independent[3].max_impressions is None):
                ind4.Independent += 1
                ind4.save()
        if len(network) >0 :
            nsc = ClickCount.objects.get(adv_type_id = network[0].id)
        if (length > 0):
            ind1c = ClickCount.objects.get(adv_type_id = independent[0].id)
        if length > 1:
            ind2c = ClickCount.objects.get(adv_type_id = independent[1].id)
        if length > 2:
            ind3c = ClickCount.objects.get(adv_type_id = independent[2].id)
        if length > 3:
            ind4c = ClickCount.objects.get(adv_type_id = independent[3].id)
        s.views_count+=1
        s.save()
        ch = StoryTcRelation.objects.filter(story = story_id)
        for x in ch:
            temp = AdvertiserType.objects.filter( end_date__isnull=True, Topic_channel = x.topic_channel)
            if len(temp) >0 :
                cs = AdvertiserType.objects.get(Topic_channel = x.topic_channel)
                tmp = Impressions.objects.get(adv_type_id = cs.id)
                tmp.Channel_spon += 1
                tmp.save()
                imp.append(ClickCount.objects.get(adv_type_id = cs.id))

        topic_channel_list = TopicChannel.objects.all()
        entries = []
        ctr = 1
        while ctr < 9:
            cult2 = []
            cult = StoryTcRelation.objects.filter(topic_channel_id = ctr)
            for c in cult:
                if c.story.date.date() == now.date():
                    cult2.append(c)
            cult = len(cult2)
            entries.append(cult)
            ctr = ctr + 1
        entries = zip(topic_channel_list,entries)
        now = datetime.datetime.now()
        ctr = 1
        lentries = []
        while ctr < 24:
            locentry = []
            dist = Story.objects.filter(location__district_id = ctr)
            for t in dist:
                if (t.date.date() == now.date()):
                    locentry.append(t)
            lentry = len(locentry)
            lentries.append(lentry)
            ctr = ctr + 1
        l1 = lentries[0:8]
        l2 = lentries[8:16]
        l3 = lentries[16:]
        #location_list = Location.objects.all()
        location_list = Loc_district.objects.all()
        location_list_1 = location_list[0:8]
        location_list_2 = location_list[8:16]
        location_list_3 = location_list[16:]
        bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2], 'ctr1': t[3], 'ctr2': t[4], 'ctr3': t[5]} for t in zip(location_list_1, location_list_2, location_list_3,l1,l2,l3)]
        loc = s.location.district
        return render_to_response('goonj/story.html', {'channels' : imp,'story' : s, 'loc': loc, 'crep' : s.community_rep.all(), 'now': now,'photoList': s.photo_id.all(),'topic_channel_list' : topic_channel_list, 'location_list': location_list,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist,'ind1c' :ind1c,'ind2c' :ind2c,'ind3c' :ind3c,'ind4c' :ind4c, 'networkc' : nsc, 'entries' : entries, 'lentry' : lentries}) 

def issue(request, issue_id):
    try:
        i = Issue.objects.get(pk=issue_id)
    except Issue.DoesNotExist:
        raise Http404
    else:
        (ind1,ind2,ind3,ind4,ns) = 0,0,0,0,0
        (ind1c,ind2c,ind3c,ind4c,nsc) = 0,0,0,0,0
        network = AdvertiserType.objects.filter(Q(ad_type ="NETWORK_SPONSOR"), Q(end_date__gt = now)| Q(end_date__isnull=True))
        if len(network) >0 :
            ns = Impressions.objects.get(adv_type_id = network[0].id)
            if (ns.Network_spon < network[0].max_impressions)|(network[0].max_impressions is None):
                ns.Network_spon += 1
                ns.save()
        independent = AdvertiserType.objects.filter(Q(ad_type ="INDEPENDENT"), Q(end_date__gt = now)| Q(end_date__isnull=True))
        length = len(independent)
        if (length > 0):
            ind1 = Impressions.objects.get(adv_type_id = independent[0].id)
            if (ind1.Independent < independent[0].max_impressions)|(independent[0].max_impressions is None):
                ind1.Independent += 1
                ind1.save()
        if length > 1:
            ind2 = Impressions.objects.get(adv_type_id = independent[1].id)
            if (ind2.Independent < independent[1].max_impressions)|(independent[1].max_impressions is None):
                ind2.Independent += 1
                ind2.save()
        if length > 2:
            ind3 = Impressions.objects.get(adv_type_id = independent[2].id)
            if (ind3.Independent < independent[2].max_impressions)|(independent[2].max_impressions is None):
                ind3.Independent += 1
                ind3.save()
        if length > 3:
            ind4 = Impressions.objects.get(adv_type_id = independent[3].id)
            if (ind4.Independent < independent[3].max_impressions)|(independent[3].max_impressions is None):
                ind4.Independent += 1
                ind4.save()
        if len(network) >0 :
            nsc = ClickCount.objects.get(adv_type_id = network[0].id)
        if (length > 0):
            ind1c = ClickCount.objects.get(adv_type_id = independent[0].id)
        if length > 1:
            ind2c = ClickCount.objects.get(adv_type_id = independent[1].id)
        if length > 2:
            ind3c = ClickCount.objects.get(adv_type_id = independent[2].id)
        if length > 3:
            ind4c = ClickCount.objects.get(adv_type_id = independent[3].id)
        topic_channel_list = TopicChannel.objects.all()
        entries = []
        ctr = 1
        while ctr < 9:
            cult2 = []
            cult = StoryTcRelation.objects.filter(topic_channel_id = ctr)
            for c in cult:
                if c.story.date.date() == now.date():
                    cult2.append(c)
            cult = len(cult2)
            entries.append(cult)
            ctr = ctr + 1
        entries = zip(topic_channel_list,entries)
        #location_list = Location.objects.all()
        location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
        location_list_1 = location_list[0:8]
        location_list_2 = location_list[8:16]
        location_list_3 = location_list[16:]
        bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]
        return render_to_response('goonj/issue.html', {'issue' : i, 'story_list' : i.story_id.all().order_by('-date'),'topic_channel_list' : topic_channel_list, 'location_list': location_list,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist, 'ind1c' :ind1c,'ind2c' :ind2c,'ind3c' :ind3c,'ind4c' :ind4c, 'networkc' : nsc, 'entries' : entries}) 

def location(request, location_id):
    try:
        l = Location.objects.get(pk=location_id)
    except Location.DoesNotExist:
        raise Http404
    else:
        (ind1,ind2,ind3,ind4,ns) = 0,0,0,0,0
        (ind1c,ind2c,ind3c,ind4c,nsc) = 0,0,0,0,0
        network = AdvertiserType.objects.filter(Q(ad_type ="NETWORK_SPONSOR"), Q(end_date__gt = now)| Q(end_date__isnull=True))
        if len(network) >0 :
            ns = Impressions.objects.get(adv_type_id = network[0].id)
            if (ns.Network_spon < network[0].max_impressions)|(network[0].max_impressions is None):
                ns.Network_spon += 1
                ns.save()
        independent = AdvertiserType.objects.filter(Q(ad_type ="INDEPENDENT"), Q(end_date__gt = now)| Q(end_date__isnull=True))
        length = len(independent)
        if (length > 0):
            ind1 = Impressions.objects.get(adv_type_id = independent[0].id)
            if (ind1.Independent < independent[0].max_impressions)|(independent[0].max_impressions is None):
                ind1.Independent += 1
                ind1.save()
        if length > 1:
            ind2 = Impressions.objects.get(adv_type_id = independent[1].id)
            if (ind2.Independent < independent[1].max_impressions)|(independent[1].max_impressions is None):
                ind2.Independent += 1
                ind2.save()
        if length > 2:
            ind3 = Impressions.objects.get(adv_type_id = independent[2].id)
            if (ind3.Independent < independent[2].max_impressions)|(independent[2].max_impressions is None):
                ind3.Independent += 1
                ind3.save()
        if length > 3:
            ind4 = Impressions.objects.get(adv_type_id = independent[3].id)
            if (ind4.Independent < independent[3].max_impressions)|(independent[3].max_impressions is None):
                ind4.Independent += 1
                ind4.save()
        if len(network) >0 :
            nsc = ClickCount.objects.get(adv_type_id = network[0].id)
        if (length > 0):
            ind1c = ClickCount.objects.get(adv_type_id = independent[0].id)
        if length > 1:
            ind2c = ClickCount.objects.get(adv_type_id = independent[1].id)
        if length > 2:
            ind3c = ClickCount.objects.get(adv_type_id = independent[2].id)
        if length > 3:
            ind4c = ClickCount.objects.get(adv_type_id = independent[3].id)
        topic_channel_list = TopicChannel.objects.all()
        entries = []
        ctr = 1
        while ctr < 9:
            cult2 = []
            cult = StoryTcRelation.objects.filter(topic_channel_id = ctr)
            for c in cult:
                if c.story.date.date() == now.date():
                    cult2.append(c)
            cult = len(cult2)
            entries.append(cult)
            ctr = ctr + 1
        entries = zip(topic_channel_list,entries)
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
        return render_to_response('goonj/location.html', {'loc' : l,'topic_channel_list' : topic_channel_list, 'location_list': location_list, 'story_list' : stories,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist, 'ind1c' :ind1c,'ind2c' :ind2c,'ind3c' :ind3c,'ind4c' :ind4c, 'networkc' : nsc, 'entries' : entries}) 
        

def top10(request):
    top_story_list = Story.objects.all().order_by('-views_count')[:10]
    topic_channel_list = TopicChannel.objects.all()
    entries = []
    ctr = 1
    while ctr < 9:
        cult2 = []
        cult = StoryTcRelation.objects.filter(topic_channel_id = ctr)
        for c in cult:
            if c.story.date.date() == now.date():
                cult2.append(c)
        cult = len(cult2)
        entries.append(cult)
        ctr = ctr + 1
    entries = zip(topic_channel_list,entries)
    (ind1,ind2,ind3,ind4,ns) = 0,0,0,0,0
    (ind1c,ind2c,ind3c,ind4c,nsc) = 0,0,0,0,0
    network = AdvertiserType.objects.filter(Q(ad_type ="NETWORK_SPONSOR"), Q(end_date__gt = now)| Q(end_date__isnull=True))
    if len(network) >0 :
        ns = Impressions.objects.get(adv_type_id = network[0].id)
        if (ns.Network_spon < network[0].max_impressions)|(network[0].max_impressions is None):
            ns.Network_spon += 1
            ns.save()
    independent = AdvertiserType.objects.filter(Q(ad_type ="INDEPENDENT"), Q(end_date__gt = now)| Q(end_date__isnull=True))
    length = len(independent)
    if (length > 0):
        ind1 = Impressions.objects.get(adv_type_id = independent[0].id)
        if (ind1.Independent < independent[0].max_impressions)|(independent[0].max_impressions is None):
            ind1.Independent += 1
            ind1.save()
    if length > 1:
        ind2 = Impressions.objects.get(adv_type_id = independent[1].id)
        if (ind2.Independent < independent[1].max_impressions)|(independent[1].max_impressions is None):
            ind2.Independent += 1
            ind2.save()
    if length > 2:
        ind3 = Impressions.objects.get(adv_type_id = independent[2].id)
        if (ind3.Independent < independent[2].max_impressions)|(independent[2].max_impressions is None):
            ind3.Independent += 1
            ind3.save()
    if length > 3:
        ind4 = Impressions.objects.get(adv_type_id = independent[3].id)
        if (ind4.Independent < independent[3].max_impressions)|(independent[3].max_impressions is None):
            ind4.Independent += 1
            ind4.save()
    if len(network) >0 :
        nsc = ClickCount.objects.get(adv_type_id = network[0].id)
    if (length > 0):
        ind1c = ClickCount.objects.get(adv_type_id = independent[0].id)
    if length > 1:
        ind2c = ClickCount.objects.get(adv_type_id = independent[1].id)
    if length > 2:
        ind3c = ClickCount.objects.get(adv_type_id = independent[2].id)
    if length > 3:
        ind4c = ClickCount.objects.get(adv_type_id = independent[3].id)
    location_list = Location.objects.all()
    return render_to_response('goonj/most_popular.html', {'top_story_list': top_story_list,'topic_channel_list' : topic_channel_list, 'location_list': location_list, 'ind1c' :ind1c,'ind2c' :ind2c,'ind3c' :ind3c,'ind4c' :ind4c, 'networkc' : nsc, 'entries' : entries})  

def search(request):
    topic_channel_list = TopicChannel.objects.all()
    entries = []
    ctr = 1
    while ctr < 9:
        cult2 = []
        cult = StoryTcRelation.objects.filter(topic_channel_id = ctr)
        for c in cult:
            if c.story.date.date() == now.date():
                cult2.append(c)
        cult = len(cult2)
        entries.append(cult)
        ctr = ctr + 1
    entries = zip(topic_channel_list,entries)
    (ind1,ind2,ind3,ind4,ns) = 0,0,0,0,0
    (ind1c,ind2c,ind3c,ind4c,nsc) = 0,0,0,0,0
    network = AdvertiserType.objects.filter(Q(ad_type ="NETWORK_SPONSOR"), Q(end_date__gt = now)| Q(end_date__isnull=True))
    if len(network) >0 :
        ns = Impressions.objects.get(adv_type_id = network[0].id)
        if (ns.Network_spon < network[0].max_impressions)|(network[0].max_impressions is None):
            ns.Network_spon += 1
            ns.save()
    independent = AdvertiserType.objects.filter(Q(ad_type ="INDEPENDENT"), Q(end_date__gt = now)| Q(end_date__isnull=True))
    length = len(independent)
    if (length > 0):
        ind1 = Impressions.objects.get(adv_type_id = independent[0].id)
        if (ind1.Independent < independent[0].max_impressions)|(independent[0].max_impressions is None):
            ind1.Independent += 1
            ind1.save()
    if length > 1:
        ind2 = Impressions.objects.get(adv_type_id = independent[1].id)
        if (ind2.Independent < independent[1].max_impressions)|(independent[1].max_impressions is None):
            ind2.Independent += 1
            ind2.save()
    if length > 2:
        ind3 = Impressions.objects.get(adv_type_id = independent[2].id)
        if (ind3.Independent < independent[2].max_impressions)|(independent[2].max_impressions is None):
            ind3.Independent += 1
            ind3.save()
    if length > 3:
        ind4 = Impressions.objects.get(adv_type_id = independent[3].id)
        if (ind4.Independent < independent[3].max_impressions)|(independent[3].max_impressions is None):
            ind4.Independent += 1
            ind4.save()
    if len(network) >0 :
        nsc = ClickCount.objects.get(adv_type_id = network[0].id)
    if (length > 0):
        ind1c = ClickCount.objects.get(adv_type_id = independent[0].id)
    if length > 1:
        ind2c = ClickCount.objects.get(adv_type_id = independent[1].id)
    if length > 2:
        ind3c = ClickCount.objects.get(adv_type_id = independent[2].id)
    if length > 3:
        ind4c = ClickCount.objects.get(adv_type_id = independent[3].id)
    location_list = Location.objects.all()
    return render_to_response('search/search.html',{'topic_channel_list' : topic_channel_list, 'location_list': location_list, 'ind1c' :ind1c,'ind2c' :ind2c,'ind3c' :ind3c,'ind4c' :ind4c, 'networkc' : nsc, 'entries' : entries}) 

def all_stories(request):
    topic_channel_list = TopicChannel.objects.all()
    entries = []
    ctr = 1
    while ctr < 9:
        cult2 = []
        cult = StoryTcRelation.objects.filter(topic_channel_id = ctr)
        for c in cult:
            if c.story.date.date() == now.date():
                cult2.append(c)
        cult = len(cult2)
        entries.append(cult)
        ctr = ctr + 1
    entries = zip(topic_channel_list,entries)
    #location_list = Location.objects.all()
    location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
    location_list_1 = location_list[0:8]
    location_list_2 = location_list[8:16]
    location_list_3 = location_list[16:]
    bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]
    (ind1,ind2,ind3,ind4,ns) = 0,0,0,0,0
    (ind1c,ind2c,ind3c,ind4c,nsc) = 0,0,0,0,0
    network = AdvertiserType.objects.filter(Q(ad_type ="NETWORK_SPONSOR"), Q(end_date__gt = now)| Q(end_date__isnull=True))
    if len(network) >0 :
        ns = Impressions.objects.get(adv_type_id = network[0].id)
        if (ns.Network_spon < network[0].max_impressions)|(network[0].max_impressions is None):
            ns.Network_spon += 1
            ns.save()
    independent = AdvertiserType.objects.filter(Q(ad_type ="INDEPENDENT"), Q(end_date__gt = now)| Q(end_date__isnull=True))
    length = len(independent)
    if (length > 0):
        ind1 = Impressions.objects.get(adv_type_id = independent[0].id)
        if (ind1.Independent < independent[0].max_impressions)|(independent[0].max_impressions is None):
            ind1.Independent += 1
            ind1.save()
    if length > 1:
        ind2 = Impressions.objects.get(adv_type_id = independent[1].id)
        if (ind2.Independent < independent[1].max_impressions)|(independent[1].max_impressions is None):
            ind2.Independent += 1
            ind2.save()
    if length > 2:
        ind3 = Impressions.objects.get(adv_type_id = independent[2].id)
        if (ind3.Independent < independent[2].max_impressions)|(independent[2].max_impressions is None):
            ind3.Independent += 1
            ind3.save()
    if length > 3:
        ind4 = Impressions.objects.get(adv_type_id = independent[3].id)
        if (ind4.Independent < independent[3].max_impressions)|(independent[3].max_impressions is None):
            ind4.Independent += 1
            ind4.save()
    if len(network) >0 :
        nsc = ClickCount.objects.get(adv_type_id = network[0].id)
    if (length > 0):
        ind1c = ClickCount.objects.get(adv_type_id = independent[0].id)
    if length > 1:
        ind2c = ClickCount.objects.get(adv_type_id = independent[1].id)
    if length > 2:
        ind3c = ClickCount.objects.get(adv_type_id = independent[2].id)
    if length > 3:
        ind4c = ClickCount.objects.get(adv_type_id = independent[3].id)
    story_list = Story.objects.all().order_by('-date')
    paginator = Paginator(story_list,20)
    page = request.GET.get('page')
    try:
        stories = paginator.page(page)
    except PageNotAnInteger:
        stories = paginator.page(1)
    except EmptyPage:
        stories = paginator.page(paginator.num_pages)
    return render_to_response('goonj/all_stories.html',{'topic_channel_list' : topic_channel_list, 'location_list': location_list, 'story_list': stories,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist, 'ind1c' :ind1c,'ind2c' :ind2c,'ind3c' :ind3c,'ind4c' :ind4c, 'networkc' : nsc, 'entries' : entries}) 

def all_issues(request):
    topic_channel_list = TopicChannel.objects.all()
    entries = []
    ctr = 1
    while ctr < 9:
        cult2 = []
        cult = StoryTcRelation.objects.filter(topic_channel_id = ctr)
        for c in cult:
            if c.story.date.date() == now.date():
                cult2.append(c)
        cult = len(cult2)
        entries.append(cult)
        ctr = ctr + 1
    entries = zip(topic_channel_list,entries)
    #location_list = Location.objects.all()
    location_list = Loc_district.objects.exclude(name='Not Known').order_by('name')
    location_list_1 = location_list[0:8]
    location_list_2 = location_list[8:16]
    location_list_3 = location_list[16:]
    bigloclist = [{'loc1': t[0], 'loc2': t[1], 'loc3':t[2]} for t in zip(location_list_1, location_list_2, location_list_3)]
    issue_list = Issue.objects.all()
    (ind1,ind2,ind3,ind4,ns) = 0,0,0,0,0
    (ind1c,ind2c,ind3c,ind4c,nsc) = 0,0,0,0,0
    network = AdvertiserType.objects.filter(Q(ad_type ="NETWORK_SPONSOR"), Q(end_date__gt = now)| Q(end_date__isnull=True))
    if len(network) >0 :
        ns = Impressions.objects.get(adv_type_id = network[0].id)
        if (ns.Network_spon < network[0].max_impressions)|(network[0].max_impressions is None):
            ns.Network_spon += 1
            ns.save()
    independent = AdvertiserType.objects.filter(Q(ad_type ="INDEPENDENT"), Q(end_date__gt = now)| Q(end_date__isnull=True))
    length = len(independent)
    if (length > 0):
        ind1 = Impressions.objects.get(adv_type_id = independent[0].id)
        if (ind1.Independent < independent[0].max_impressions)|(independent[0].max_impressions is None):
            ind1.Independent += 1
            ind1.save()
    if length > 1:
        ind2 = Impressions.objects.get(adv_type_id = independent[1].id)
        if (ind2.Independent < independent[1].max_impressions)|(independent[1].max_impressions is None):
            ind2.Independent += 1
            ind2.save()
    if length > 2:
        ind3 = Impressions.objects.get(adv_type_id = independent[2].id)
        if (ind3.Independent < independent[2].max_impressions)|(independent[2].max_impressions is None):
            ind3.Independent += 1
            ind3.save()
    if length > 3:
        ind4 = Impressions.objects.get(adv_type_id = independent[3].id)
        if (ind4.Independent < independent[3].max_impressions)|(independent[3].max_impressions is None):
            ind4.Independent += 1
            ind4.save()
    if len(network) >0 :
        nsc = ClickCount.objects.get(adv_type_id = network[0].id)
    if (length > 0):
        ind1c = ClickCount.objects.get(adv_type_id = independent[0].id)
    if length > 1:
        ind2c = ClickCount.objects.get(adv_type_id = independent[1].id)
    if length > 2:
        ind3c = ClickCount.objects.get(adv_type_id = independent[2].id)
    if length > 3:
        ind4c = ClickCount.objects.get(adv_type_id = independent[3].id)
    return render_to_response('goonj/all_issues.html',{'topic_channel_list' : topic_channel_list, 'location_list': location_list, 'issue_list': issue_list,'location_list_1': location_list_1,'location_list_2': location_list_2,'location_list_3': location_list_3,'bigloclist': bigloclist, 'ind1c' :ind1c,'ind2c' :ind2c,'ind3c' :ind3c,'ind4c' :ind4c, 'networkc' : nsc, 'entries' : entries}) 


@register.inclusion_tag('goonj/timelines.html', takes_context = True)
def address(context):
    request = context['request']
    address = request.session['address']
    return {'address':address}
    
def add1(value):
    return value+1
    
register.filter('add1', add1)