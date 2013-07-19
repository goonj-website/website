from django.db import models
import datetime

# Create your models here.
class Loc_country(models.Model):
    name = models.CharField(max_length=50)

class Loc_state(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Loc_country,blank=True,null=True)

class Loc_district(models.Model):
    name = models.CharField(max_length=50)
    state = models.ForeignKey(Loc_state,blank=True,null=True)

class Loc_block(models.Model):
    name = models.CharField(max_length=50)
    district = models.ForeignKey(Loc_district,blank=True,null=True)

class Loc_village(models.Model):
    village = models.CharField(max_length=50,blank=True,null=True)
    country = models.ForeignKey(Loc_country)
    state = models.ForeignKey(Loc_state, blank=True,null=True)
    district = models.ForeignKey(Loc_district, blank=True, null=True)
    block = models.ForeignKey(Loc_block, blank=True,null=True)

class Location(models.Model) :
    location_id = models.IntegerField(primary_key=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=8,blank=True, null = True)
    latitude = models.DecimalField(max_digits=12, decimal_places=8,blank=True, null = True)
    village = models.CharField(max_length=100, blank=True, null = True)
    district = models.CharField(max_length=100)
    block = models.CharField(max_length=100,blank=True, null = True)
    def __unicode__(self):
        return self.district

class ChannelPartner(models.Model):
    channel_partner_id = models.IntegerField(primary_key=True)
    cp_name = models.CharField(max_length=100)
    cp_email = models.EmailField(max_length=75, blank=True, null = True)
    cp_description = models.CharField(max_length=500)
    cp_website = models.URLField(verify_exists= False, max_length =200, blank=True, null = True)
    cp_phone_number = models.CharField(max_length=20, blank=True, null = True)
    def __unicode__(self):
        return self.cp_name


class TopicChannel(models.Model) :
    topic_channel_id = models.IntegerField(primary_key=True)
    topic = models.CharField(max_length=100)
    topic_description = models.CharField(max_length=1000)
    topic_photo = models.FileField(upload_to = "images", blank=True, null = True)       
    cp_ids = models.ManyToManyField(ChannelPartner,through='TcCpRelation',blank=True, null = True)          
    def __unicode__(self):
        return self.topic
    
class CommunityRep(models.Model):
    community_rep_id = models.IntegerField(primary_key=True)
    cr_name = models.CharField(max_length=100)
    cr_photo = models.FileField(upload_to = "images", blank=True, null = True)
    cr_phone_number = models.CharField(max_length=20, blank=True, null = True)
    role = models.CharField(max_length=100)
    cr_email = models.EmailField(max_length=75, blank=True, null = True)
    cr_location = models.ForeignKey(Location)
    def __unicode__(self):
        return self.cr_name

class GovernmentDepartment(models.Model):
    LEVEL_CHOICES = (
        ('VILLAGE', 'Village'),
        ('BLOCK', 'Block'),
        ('DISTRICT', 'District'),
        ('STATE', 'State'),
    )
    gd_id = models.IntegerField(primary_key=True)   
    gd_location = models.ForeignKey(Location)
    gd_name = models.CharField(max_length=100)
    gd_email = models.EmailField(max_length=75, blank=True, null = True)
    level = models.CharField(max_length=8, choices = LEVEL_CHOICES) 
    person_name = models.CharField(max_length=100, blank=True, null = True)
    gd_phone_number = models.CharField(max_length=20, blank=True, null = True)
    def __unicode__(self):
        return self.gd_name

class Photo(models.Model):
    photo_id = models.IntegerField(primary_key=True)
    photo = models.FileField(upload_to = "images", blank=True, null = True)
    date_taken = models.DateTimeField(blank=True, null = True)
    photographer_name = models.CharField(max_length=100, blank=True, null = True)

class Story(models.Model):
    location = models.ForeignKey(Loc_village,blank=True, null = True)   
    topic_channel = models.ManyToManyField(TopicChannel,through='StoryTcRelation',blank=True, null = True)
    channel_partner = models.ManyToManyField(ChannelPartner,through='StoryCpartRelation',blank=True, null = True)
    community_rep = models.ManyToManyField(CommunityRep,through='StoryCrepRelation',blank=True, null = True)
    TYPE_CHOICES = (
        ('EVENT', 'Event'),
        ('NON-EVENT', 'Non-event'),
    )
    story_type = models.CharField(max_length=9, choices = TYPE_CHOICES)
    story_id = models.IntegerField(primary_key=True)
    detail_id = models.IntegerField(blank=True, null=True)
    ai_id = models.IntegerField(blank=True, null=True)
    tags = models.CharField(max_length=1000, blank=True, null=True)
    title = models.CharField(max_length=1000)
    transcript = models.CharField(max_length=10000, blank=True, null = True)
    audio = models.FileField(upload_to = "audio", blank=True, null = True)
    photo_id = models.ManyToManyField(Photo,through='StoryPhotoRelation')
    #photo = models.FileField(upload_to = "images", blank=True, null = True)     list needed
    video = models.FileField(upload_to = "video", blank=True, null = True)
    views_count = models.IntegerField()
    date = models.DateTimeField('date posted')
    rating = models.IntegerField()
    top_story = models.BooleanField()
    related_stories = models.IntegerField(blank=True, null = True)      #relation to same class, needed
    def __unicode__(self):
        return self.title   

class StoryTcRelation(models.Model):
  #  stc_id = models.AutoField(primary_key= True)
    story = models.ForeignKey(Story)
    topic_channel = models.ForeignKey(TopicChannel)
    unique_together = (("story","topic_channel"),)

class StoryCpartRelation(models.Model):
    scp_id = models.IntegerField(primary_key= True)
    story = models.ForeignKey(Story)
    channel_partner = models.ForeignKey(ChannelPartner)

class StoryCrepRelation(models.Model):
    scr_id = models.IntegerField(primary_key= True)
    story = models.ForeignKey(Story)
    community_rep = models.ForeignKey(CommunityRep)

class Issue(models.Model):
    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('Close', 'Close'),
    )
    issue_id = models.IntegerField(primary_key= True)
    issue_name = models.CharField(max_length=100)
    issue_description = models.CharField(max_length=200)
    audio_media = models.FileField(upload_to = "audio", blank=True, null = True)
    photo_media = models.FileField(upload_to = "images", blank=True, null = True)
    video_media = models.FileField(upload_to = "video", blank=True, null = True)
    status = models.CharField(max_length=5, choices = STATUS_CHOICES)
    story_id = models.ManyToManyField(Story,through='IssueStoryRelation')
    def __unicode__(self):
        return self.issue_name

class IssueStoryRelation(models.Model):
    is_id = models.IntegerField(primary_key = True)
    story = models.ForeignKey(Story)
    issue = models.ForeignKey(Issue)
    #def __unicode__(self):
    #   return self.is_id

class StoryPhotoRelation(models.Model):
    sp_id = models.IntegerField(primary_key = True)
    story = models.ForeignKey(Story)
    photo = models.ForeignKey(Photo)


class TcCpRelation(models.Model):
    tccp_id = models.IntegerField(primary_key = True)
    topic_channel = models.ForeignKey(TopicChannel)
    channel_partner = models.ForeignKey(ChannelPartner)

class Delegation(models.Model):
    delegation_id = models.IntegerField(primary_key= True)
    DELEGATION_CHOICES = (
        ('Govt Dept', 'Govt Dept'),
        ('Community-Rep', 'Community-Rep'),
        ('Channel-Partner', 'Channel-Partner'),
    )
    delegation = models.CharField(max_length=15, choices = DELEGATION_CHOICES)
    agent_id = models.IntegerField()
    status_update = models.CharField(max_length= 500)
    def __unicode__(self):
        return self.status_update
        
class Timeline(models.Model):
    event_id = models.IntegerField(primary_key = True)
    event = models.CharField(max_length = 1000)
    synopsis = models.CharField(max_length = 10000)
    location = models.ForeignKey(Location,blank=True, null = True)  
    date = models.DateTimeField('date initiated')
    tag = models.CharField(max_length = 100)
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    status_choices = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
    )
    status = models.CharField(max_length = 100, choices = status_choices, default = ACTIVE)
    def __unicode__(self):
        return self.event
    
    
class TimelineStoryRelation(models.Model):
    ts_id = models.IntegerField(primary_key = True)
    timeline = models.ForeignKey(Timeline)
    story = models.ForeignKey(Story)


class Campaigns(models.Model):
    c_id = models.IntegerField(primary_key = True)
    Campaign_name = models.CharField(max_length = 1000)
    description = models.CharField(max_length = 10000)
    location = models.ForeignKey(Location,blank=True, null = True)  
    date = models.DateTimeField('date initiated')
    tag = models.CharField(max_length = 100)
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    status_choices = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
    )
    status = models.CharField(max_length = 100, choices = status_choices, default = ACTIVE)
    def __unicode__(self):
        return self.Campaign_name

class CampaignStoryRelation(models.Model):
    cs_id = models.IntegerField(primary_key = True)
    campaign = models.ForeignKey(Campaigns)
    story = models.ForeignKey(Story)
    
class LocationForMap(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 1000)
    latitude = models.DecimalField(max_digits = 12, decimal_places = 8)
    longitude = models.DecimalField(max_digits = 12, decimal_places = 8)
    information = models.CharField(max_length = 10000) #Should replace this with foreign key relation to stories to find their title
    def __unicode__(self):
        return self.name


class Advertiser(models.Model):
  # id = models.IntegerField(primary_key = True)
    ad_name = models.CharField(max_length = 100)
    ad_address = models.CharField(max_length = 1000)
    url = models.URLField(max_length = 200)
    smallPhoto = models.FileField(upload_to = "images")
    bannerPhoto = models.FileField(upload_to = "images")
    def __unicode__(self):
        return self.ad_name
        

class AdvertiserType(models.Model) :
  # id = models.AutoField(primary_key= True)
    Advertiser = models.ForeignKey(Advertiser)
    SPONSOR_CHOICES = (
        ('NETWORK_SPONSOR', 'Network Sponsor'),
        ('CHANNEL_SPONSOR', 'Channel Sponsor'),
        ('CAMPAIGN_SPONSOR', 'Campaign Sponsor'),
        ('INDEPENDENT', 'Independent'),
    )
    ad_type = models.CharField(max_length=20, choices=SPONSOR_CHOICES)
    Topic_channel = models.ForeignKey(TopicChannel, blank = True, null = True)
    Campaign = models.ForeignKey(Campaigns, blank = True, null = True)
    start_date = models.DateTimeField('date started')
    end_date = models.DateTimeField('date ended', blank = True, null = True)
    max_impressions = models.IntegerField(blank=True, null = True)
    def __unicode__(self):
        return self.ad_type


class Impressions(models.Model):
  #  id = models.AutoField(primary_key = True)
    adv_type = models.ForeignKey(AdvertiserType)
    Network_spon = models.IntegerField(default = 0)
    Channel_spon = models.IntegerField(default = 0)
    Campaign_spon = models.IntegerField(default = 0)
    Independent = models.IntegerField(default = 0)

class ClickCount(models.Model):
  #  id = models.AutoField(primary_key = True)
    adv_type = models.ForeignKey(AdvertiserType)
    Network_spon = models.IntegerField(default = 0)
    Channel_spon = models.IntegerField(default = 0)
    Campaign_spon = models.IntegerField(default = 0)
    Independent = models.IntegerField(default = 0)