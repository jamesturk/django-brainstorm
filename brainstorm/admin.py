from django.contrib import admin
from brainstorm.models import Subsite, Idea

class SubsiteAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')

class IdeaAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'subsite')
    list_filter = ('subsite',)

admin.site.register(Subsite, SubsiteAdmin)
admin.site.register(Idea, IdeaAdmin)
