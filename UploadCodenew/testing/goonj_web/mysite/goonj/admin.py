from goonj.models import Location, Story, TopicChannel, CommunityRep, GovernmentDepartment, ChannelPartner, StoryTcRelation,StoryCpartRelation,StoryCrepRelation,Issue,Delegation, IssueStoryRelation, Photo, StoryPhotoRelation, TcCpRelation,Loc_country, Loc_state, Loc_district, Loc_block, Loc_village
from django.contrib import admin

admin.site.register(Location)

admin.site.register(Loc_country)

admin.site.register(Loc_state)

admin.site.register(Loc_district)

admin.site.register(Loc_block)

admin.site.register(Loc_village)

admin.site.register(TopicChannel)

admin.site.register(CommunityRep)

admin.site.register(Story)

admin.site.register(GovernmentDepartment)

admin.site.register(ChannelPartner)

admin.site.register(StoryTcRelation)

admin.site.register(StoryCpartRelation)

admin.site.register(StoryCrepRelation)

admin.site.register(Issue)

admin.site.register(Delegation)

admin.site.register(IssueStoryRelation)

admin.site.register(Photo)

admin.site.register(StoryPhotoRelation)

admin.site.register(TcCpRelation)
