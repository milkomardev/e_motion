from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DeleteView

from e_motion.common.forms import GalleryImageForm
from e_motion.common.models import ContactInfo, GalleryImage


class HomeView(TemplateView):
    template_name = 'common/home.html'


def contact_detail(request):
    contact = ContactInfo.objects.first()
    return render(request, 'common/contacts.html', {'contact': contact})


class GalleryListView(ListView):
    model = GalleryImage
    template_name = 'common/gallery-list.html'
    context_object_name = 'images'


class GalleryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = GalleryImage
    form_class = GalleryImageForm
    template_name = 'common/gallery-add-image.html'
    success_url = reverse_lazy('gallery-list')

    def test_func(self):
        return self.request.user.has_perm("common.add_galleryimage")


class GalleryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = GalleryImage
    template_name = 'common/gallery-delete-image.html'
    success_url = reverse_lazy('gallery-list')

    def test_func(self):
        return self.request.user.has_perm("common.delete_galleryimage")