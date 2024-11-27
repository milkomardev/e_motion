from django.shortcuts import render
from django.views.generic import TemplateView

from e_motion.common.models import ContactInfo


class HomeView(TemplateView):
    template_name = 'common/home.html'


def contact_detail(request):
    contact = ContactInfo.objects.first()
    return render(request, 'common/contacts.html', {'contact': contact})