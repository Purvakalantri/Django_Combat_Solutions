from django.apps import AppConfig

class ComplaintsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.complaints'

    def ready(self):
        import src.complaints.signals.update_status
