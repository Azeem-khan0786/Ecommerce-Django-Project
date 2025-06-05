from django.apps import AppConfig


class AlibabaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Alibaba'
    def ready(self):
        import Alibaba.signals

