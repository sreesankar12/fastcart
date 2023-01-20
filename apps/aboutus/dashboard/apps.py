from django.urls import path
from oscar.core.application import OscarDashboardConfig
from oscar.core.loading import get_class


class DashboardConfig(OscarDashboardConfig):
    name = 'apps.aboutus.dashboard'
    label = 'aboutus_dashboard'
    namespace = 'aboutus-dashboard'
    default_permissions = ['is_staff']

    def ready(self):
        # self.aboutus_update_view = get_class('aboutus.dashboard.views', 'DashboardAboutusUpdateView')
        self.faq_create_view = get_class('aboutus.dashboard.views', 'FaqCreateView')
        self.faq_list_view = get_class('aboutus.dashboard.views', 'FaqListView')
        self.faq_detail_view = get_class('aboutus.dashboard.views', 'FaqDetailView')
        self.faq_update_view = get_class('aboutus.dashboard.views', 'FaqUpdateView')
        self.faq_delete_view = get_class('aboutus.dashboard.views', 'FaqDeleteView')
        # self.terms_update_view = get_class('aboutus.dashboard.views', 'DashboardTermsUpdateView')

    def get_urls(self):
        urls = [
            # path('update/', self.aboutus_update_view.as_view(), name='about-update'),
            path('faq-add/', self.faq_create_view.as_view(), name='faq-add'),
            path('faq-list/', self.faq_list_view.as_view(), name='faq-list'),
            path('faq-list/<pk>/', self.faq_detail_view.as_view(), name='faq-detail'),
            path('faq-list/<pk>/update', self.faq_update_view.as_view(), name='faq-update'),
            path('faq-list/<pk>/delete', self.faq_delete_view.as_view(), name='faq-delete'),
            # path('update-terms/', self.terms_update_view.as_view(), name='terms-update'),
        ]
        return self.post_process_urls(urls)
