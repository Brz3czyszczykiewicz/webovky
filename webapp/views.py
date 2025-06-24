from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from webapp.forms import CustomerForm, TripForm, TripImageForm, CustomerNameSearchForm
from webapp.models import Customer, Trip, TripImage, FreeImage
from . import models
from django.http import FileResponse
from django.urls import reverse_lazy

from .utils.context_processors.group_access import UserRightsMixin


#----------------
#MIXINS AND TESTS
#----------------
@login_required
def send_image(request):
    image_path = 'webapp/media/město.jpg'
    return FileResponse(open(image_path, 'rb'), content_type='image/jpeg')


class TripShowPicturesMixin:
    """
    adds database images into context in text form {settings.MEDIA_URL}{file.name}
    form_valid needed for js, "selected_images" - html input, makes long string out
    of names of images user clicked on

    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["images_in_media"] = Trip.get_directory_images()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        trip = self.object
        print(trip)
        #need to watch for crash here or make selecting some mandatory (Attribute error)
        selected = self.request.POST.get("selected_images_available")
        if selected:
            print(selected)
            selected_images = [name.strip() for name in selected.split(",") if name.strip()]
            for name in selected_images:
                TripImage.objects.create(
                    relation=trip,
                    image=name,
                    caption="",
                )

        to_be_removed = self.request.POST.get("selected_images_attached")
        if to_be_removed:
            filenames = to_be_removed.split(",")
            TripImage.objects.filter(
                relation=self.object,
                image__in=filenames
            ).delete()

        return response

#----------------
#LIST VIEWS
#----------------

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ["trips"] = Trip.objects.all()[:9]
        return context



class CustomerListingView(LoginRequiredMixin, UserRightsMixin, ListView):
    template_name = "customer_list.html"
    model = Customer
    paginate_by = 15
    access_rights = ["test"]
    query_string = None




    def get(self, request, *args, **kwargs):
        print("GET: ", self.request.GET)
        self.query_string = self.request.GET.get("search")
        print(self.query_string)
        print("KWARGS: ", self.kwargs)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context ["trips"] = Trip.objects.all()
        context ["form"] = CustomerNameSearchForm()
        context.update(self.get_context_rights())
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        #add whatever hardcoded
        queryset = queryset.search(self.query_string)
        return queryset


class TripListingView(LoginRequiredMixin, ListView):
    template_name= "trip_list.html"
    model = Trip

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["customers"] = Customer.objects.all()
        return context

class Gallery(ListView):
    template_name="gallery.html"
    model = Trip
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["images"] = Trip.get_directory_images()
        return context




#------------------------
#DETAIL VIEWS
#------------------------

class CustomerDetailView(LoginRequiredMixin, DetailView):
    #lists every customer in database
    template_name = "customer_detail.html"
    model = Customer

    def get_context_data(self, **kwargs):
        print("ContactDetailView -> get_context_data")
        kontext = super().get_context_data(**kwargs)
        print(kontext)
        return kontext

def work_in_progress(request):
    return render(request, "work_in_progress.html")


class TripDetailView(DetailView):
    #presentation to outsider
    template_name = "trip_detail.html"
    model = Trip
    context_object_name = "trip"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip = self.object
        context["trip_images"] = trip.trip_images.all()
        return context


class TripAdminView(LoginRequiredMixin, TripDetailView):
    template_name = "trip_detail_admin.html"
    model = Trip

    def get_context_data(self, **kwargs):
        #selects only customers which signed for particular trip
        context = super().get_context_data(**kwargs)
        trip = self.get_object()
        context["customers"] = trip.customer_trip.all()
        return context


#----------------
#CREATE VIEWS
#----------------

class CustomerCreateView(CreateView):
# class based form for customer registration, based on customer model, details in forms.py
    template_name = "customer_create.html"
    form_class = CustomerForm
    model = Customer
    success_url = "/webapp/customer-list/"

    def dispatch(self, request, *args, **kwargs):
        """
        CustomerCreateView will only get triggered by the user when accessing through trip detail
        purpose of this function is to get trip pk so reservation can be linked with specific trip
        later in form valid
        """
        pk = self.kwargs.get("pk")
        #condition for testing purposes, if view is accessed through detail it will never be used
        if pk is not None:
            self.trip = get_object_or_404(Trip, pk=pk)
        else:
            self.trip = None
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trip"] = self.trip
        return context

    def form_valid(self, form):
        if self.trip:
            form.instance.customer_trip = self.trip
        return super().form_valid(form)



class TripCreateView(LoginRequiredMixin, TripShowPicturesMixin, CreateView):
    #class based form for trip creation, based on trip model
    template_name = "trip_create_alt.html"
    form_class = TripForm
    model = Trip
    success_url = "/webapp/trip-list/"

class UploadImageView(LoginRequiredMixin, CreateView):
    """
    frontend option for adding extra images to the database so they can be
    linked to trips later
    """
    template_name = "image_upload.html"
    model = FreeImage
    form_class = TripImageForm
    success_url = "/webapp/gallery/"



#----------------
#UPDATE VIEWS
#----------------
class TripUpdateView(LoginRequiredMixin, TripShowPicturesMixin, UpdateView):
    template_name = "trip_update.html"
    form_class = TripForm
    model = Trip
    success_url = "/webapp/trip-list/"

    def get_context_data(self, **kwargs):
        """
        add all TripImage instances attached to Trip
        """
        context = super().get_context_data(**kwargs)
        context["attached"] = self.object.trip_images.all()
        return context




class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "customer_create.html"
    form_class = CustomerForm
    model = Customer
    success_url = "/webapp/customer-list/"



#----------------
#DELETE VIEWS
#----------------

class TripDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "trip_delete.html"
    model = Trip
    success_url = "/webapp/trip-list/"

class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    template_name="customer_delete.html"
    model = Customer
    success_url = "/webapp/customer-list/"


