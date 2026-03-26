from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import Incident, RoadStatus, Profile
from .forms import IncidentReportForm, RoadStatusForm

# --- Permission Helpers ---
def is_authority(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'police'

def is_engineer(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'engineer'

# --- Authentication & Registration ---

def register(request):
    """Handles user sign up and assigns the selected role to their profile"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        selected_role = request.POST.get('role')
        if form.is_valid():
            user = form.save()
            profile = user.profile
            profile.role = selected_role
            profile.save()
            messages.success(request, f"Account created for {user.username}! Please log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# --- Main Map View ---

def home(request):
    """The Public Map View - Accessible to everyone without login"""
    incidents = Incident.objects.filter(status='verified')
    road_statuses = RoadStatus.objects.all()
    context = {
        'incidents': incidents,
        'road_statuses': road_statuses,
        'incident_count': incidents.count(),
        'road_status_count': road_statuses.count(),
    }
    return render(request, 'traffic/home.html', context)

# --- Incident Reporting (Commuters) ---

@login_required
def report_incident(request):
    """Allows logged-in users to submit a traffic incident"""
    if request.method == 'POST':
        form = IncidentReportForm(request.POST, request.FILES)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.reported_by = request.user
            incident.save()
            messages.success(request, "Incident reported! It will appear on the map after police verification.")
            return redirect('home')
    else:
        form = IncidentReportForm()
    return render(request, 'traffic/report_incident.html', {'form': form})

# --- Dashboards (Police & Engineers) ---

@login_required
@user_passes_test(is_authority)
def authority_dashboard(request):
    """Traffic Police view to Verify, Reject, or Resolve incidents"""
    if request.method == 'POST':
        incident_id = request.POST.get('incident_id')
        action = request.POST.get('action')
        incident = get_object_or_404(Incident, id=incident_id)

        if action == 'verify':
            incident.status = 'verified'
            incident.verified_at = timezone.now()
            incident.verified_by = request.user
            messages.success(request, f"Incident #{incident.id} verified.")
        elif action == 'reject':
            incident.status = 'rejected'
            messages.warning(request, f"Incident #{incident.id} rejected.")
        elif action == 'resolve':
            incident.status = 'resolved'
            incident.resolved_at = timezone.now()
            messages.info(request, f"Incident #{incident.id} marked as resolved.")
        
        incident.save()
        return redirect('authority_dashboard')

    context = {
        'pending_incidents': Incident.objects.filter(status='pending').order_by('-created_at'),
        'verified_incidents': Incident.objects.filter(status='verified').order_by('-verified_at')[:10],
    }
    return render(request, 'traffic/authority_dashboard.html', context)

@login_required
@user_passes_test(is_engineer)
def engineer_dashboard(request):
    """Engineer view to manage road status updates"""
    road_statuses = RoadStatus.objects.all().order_by('-updated_at')
    return render(request, 'traffic/engineer_dashboard.html', {'road_statuses': road_statuses})

@login_required
@user_passes_test(is_engineer)
def create_road_status(request):
    if request.method == 'POST':
        form = RoadStatusForm(request.POST)
        if form.is_valid():
            status = form.save(commit=False)
            status.updated_by = request.user
            status.save()
            messages.success(request, "Road status published.")
            return redirect('engineer_dashboard')
    else:
        form = RoadStatusForm()
    return render(request, 'traffic/create_road_status.html', {'form': form, 'edit_mode': False})

# --- NEW: Edit & Delete Road Status (For Engineers) ---

@login_required
@user_passes_test(is_engineer)
def edit_road_status(request, pk):
    """Allows engineers to update existing road status entries"""
    status_entry = get_object_or_404(RoadStatus, pk=pk)
    if request.method == 'POST':
        form = RoadStatusForm(request.POST, instance=status_entry)
        if form.is_valid():
            status = form.save(commit=False)
            status.updated_by = request.user
            status.save()
            messages.success(request, f"Road status for {status.road_name} updated.")
            return redirect('engineer_dashboard')
    else:
        form = RoadStatusForm(instance=status_entry)
    
    return render(request, 'traffic/create_road_status.html', {
        'form': form, 
        'edit_mode': True,
        'status_entry': status_entry
    })

@login_required
@user_passes_test(is_engineer)
def delete_road_status(request, pk):
    """Simple view to delete a status entry"""
    status_entry = get_object_or_404(RoadStatus, pk=pk)
    if request.method == 'POST':
        status_entry.delete()
        messages.error(request, "Road status entry deleted.")
    return redirect('engineer_dashboard')

# --- API Endpoints ---

def api_incidents(request):
    incidents = Incident.objects.filter(status='verified')
    data = [{
        'id': inc.id,
        'title': inc.title,
        'type': inc.incident_type,
        'lat': float(inc.latitude),
        'lng': float(inc.longitude),
        'severity': inc.severity,
        'description': inc.description
    } for inc in incidents]
    return JsonResponse(data, safe=False)

def api_road_statuses(request):
    statuses = RoadStatus.objects.all()
    data = []
    for rs in statuses:
        item = {
            'id': rs.id,
            'road_name': rs.road_name,
            'status': rs.status,
        }
        if rs.start_latitude and rs.end_latitude:
            item['coords'] = [
                [float(rs.start_latitude), float(rs.start_longitude)],
                [float(rs.end_latitude), float(rs.end_longitude)]
            ]
        data.append(item)
    return JsonResponse(data, safe=False)