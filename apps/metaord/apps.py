from django.apps import AppConfig

class MetaordConfig(AppConfig):
    name = 'metaord'
    verbose_name = "Metaord"

    def ready(self):
        import signals.handlers #noqa
