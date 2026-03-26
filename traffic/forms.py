from django import forms
from .models import Incident, RoadStatus

class IncidentReportForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = [
            'title', 'incident_type', 'severity', 
            'description', 'location_name', 'latitude', 
            'longitude', 'image'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Multi-car collision near Museum Hill'}),
            'incident_type': forms.Select(attrs={'class': 'form-select'}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Provide more details about the situation...'}),
            'location_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Uhuru Highway Southbound'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

# FIXED: Removed underscore from Model_Form
class RoadStatusForm(forms.ModelForm):
    class Meta:
        model = RoadStatus
        fields = [
            'road_name', 'status', 'description', 
            'start_latitude', 'start_longitude', 
            'end_latitude', 'end_longitude', 
            'alternative_route', 'effective_date', 'expected_end_date'
        ]
        widgets = {
            'road_name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'alternative_route': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'effective_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'expected_end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'start_latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'start_longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'end_latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'end_longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
        }