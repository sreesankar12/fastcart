from oscar.core.application import OscarConfig
from django.urls import path, re_path
from oscar.core.loading import get_class


class AboutUsConfig(OscarConfig):
    name = 'apps.aboutus'
    namespace = 'apps.aboutus'

    def ready(self):
        super().ready()
        self.aboutus_view = get_class('aboutus.views', 'AboutUsView')
        self.terms_view = get_class('aboutus.views', 'TermsView')

    def get_urls(self):
        urls = super().get_urls()
        urls += [
            path('', self.aboutus_view.as_view(), name='aboutus'),
            path('terms', self.terms_view.as_view(), name='terms'),
        ]
        return self.post_process_urls(urls)
