from django.contrib import admin
# Change UserProfile to Profile here
from .models import Incident, RoadStatus, Profile 

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'created_at')
    list_filter = ('role',)

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('title', 'incident_type', 'severity', 'status', 'created_at')
    list_filter = ('status', 'incident_type', 'severity')
    search_fields = ('title', 'description')

@admin.register(RoadStatus)
class RoadStatusAdmin(admin.ModelAdmin):
    list_display = ('road_name', 'status', 'updated_at', 'updated_by')
    list_filter = ('status',)