from django.apps import AppConfig


class GalleryConfig(AppConfig):
    # myapp/apps.py
    name = 'gallery'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Album'))
        registry.register(self.get_model('Photo'))
        registry.register(self.get_model('Tag'))
