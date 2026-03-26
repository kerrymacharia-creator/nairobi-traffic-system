from django.apps import AppConfig

class TrafficConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'traffic'

    def ready(self):
        import traffic.signals  # This is fine as long as signals.py is fixed above