from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Profile(models.Model):
    ROLE_CHOICES = [
        ('commuter', 'Commuter'),
        ('police', 'Traffic Police (Staff)'), # Renamed 'authority' to 'police' to match views
        ('engineer', 'Road Engineer'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='commuter')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

class Incident(models.Model):
    INCIDENT_TYPES = [
        ('accident', 'Accident'),
        ('hazard', 'Hazard'),
        ('heavy_traffic', 'Heavy Traffic'),
        ('road_closure', 'Road Closure'),
        ('construction', 'Construction'),
        ('other', 'Other'),
    ]
    
    SEVERITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'), # Added rejected status
        ('resolved', 'Resolved'),
    ]
    
    title = models.CharField(max_length=200)
    incident_type = models.CharField(max_length=20, choices=INCIDENT_TYPES)
    severity = models.IntegerField(choices=SEVERITY_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(4)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    description = models.TextField()
    
    # Location fields
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    location_name = models.CharField(max_length=200, blank=True, null=True)
    
    # Media
    image = models.ImageField(upload_to='incidents/', blank=True, null=True)
    
    # Status and verification
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_incidents')
    verified_at = models.DateTimeField(null=True, blank=True)
    
    # Reporting
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_incidents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional metadata
    is_active = models.BooleanField(default=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_incident_type_display()} ({self.get_status_display()})"

class RoadStatus(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('diversion', 'Diversion'),
        ('construction', 'Under Construction'), # Simplified name to match views
        ('partially_open', 'Partially Open'),
    ]
    
    road_name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    description = models.TextField(help_text="Detailed description of the road status")
    
    # Location fields for mapping
    start_latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    start_longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    end_latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    end_longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    
    # Alternative route suggestion
    alternative_route = models.TextField(blank=True, null=True, help_text="Suggested alternative route")
    
    # Metadata
    effective_date = models.DateTimeField(default=timezone.now, help_text="When does this status take effect")
    expected_end_date = models.DateTimeField(null=True, blank=True, help_text="Expected end date if applicable")
    
    # Tracking
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='road_updates')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Road Statuses"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.road_name} - {self.get_status_display()}"

# --- Signals to Automate Profile Creation ---

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Check if profile exists before saving to avoid errors during migrations
    if hasattr(instance, 'profile'):
        instance.profile.save()