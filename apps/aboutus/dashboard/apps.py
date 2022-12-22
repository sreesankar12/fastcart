from django.urls import path
from oscar.core.application import OscarDashboardConfig
from oscar.core.loading import get_class


class DashboardConfig(OscarDashboardConfig):
    name = 'apps.aboutus.dashboard'
    label = 'aboutus_dashboard'
    namespace = 'aboutus-dashboard'
    default_permissions = ['is_staff']

    def ready(self):
        self.aboutus_update_view = get_class('aboutus.dashboard.views', 'DashboardAboutusUpdateView')
        self.terms_update_view = get_class('aboutus.dashboard.views', 'DashboardTermsUpdateView')

    def get_urls(self):
        urls = [
            path('update/', self.aboutus_update_view.as_view(), name='about-update'),
            path('update-terms/', self.terms_update_view.as_view(), name='terms-update'),
        ]
        return self.post_process_urls(urls)
