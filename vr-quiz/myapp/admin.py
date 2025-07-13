from django.contrib import admin
from .models import SurveyResponse
from django.contrib.auth.models import User
# Register your models here.
# admin.site.register(SurveyResponse)

class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'player_name','gender', 'score', 'passed', 'created_at')
    list_filter = ('passed','gender', 'created_at')
    search_fields = ('id', 'player_name')
    
    def user_username(self, obj):
        return obj.user.username if obj.user else 'No user'
    user_username.short_description = 'Username'

admin.site.register(SurveyResponse, SurveyResponseAdmin)