from django.views.generic import TemplateView, DetailView

from e_motion.common.models import ContactInfo


class HomeView(TemplateView):
    template_name = 'common/home.html'


class ContactDetailView(DetailView):
    model = ContactInfo
    template_name = 'common/contacts.html'
    context_object_name = 'contact'