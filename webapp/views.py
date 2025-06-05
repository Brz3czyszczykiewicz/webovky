from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from webapp.forms import CustomerForm, TripForm
from webapp.models import Customer, Trip, CustomerAdmin
from . import models
from django.http import FileResponse

#fucked up stuff

def send_image(request):
    image_path = 'webapp/media/město.jpg'
    return FileResponse(open(image_path, 'rb'), content_type='image/jpeg')


#----------------
#LIST VIEWS
#----------------

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ["trips"] = Trip.objects.all()[:6]
        return context



class CustomerListingView(ListView):
    template_name = "customer_list.html"
    model = Customer
    paginate_by = 15

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context ["trips"] = Trip.objects.all()
        return context


class TripListingView(ListView):
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

class CustomerDetailView(DetailView):
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
    template_name = "trip_detail.html"
    model = Trip
    context_object_name = "trip"

class TripAdminView(TripDetailView):
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



class TripCreateView(CreateView):
    #class based form for trip creation, based on trip model
    template_name = "trip_create.html"
    form_class = TripForm
    model = Trip
    success_url = "/webapp/trip-list/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["images_in_media"] = Trip.get_directory_images()
        return context


#----------------
#UPDATE VIEWS
#----------------
class TripUpdateView(UpdateView):
    template_name = "trip_update.html"
    form_class = TripForm
    model = Trip
    success_url = "/webapp/trip-list/"

class CustomerUpdateView(UpdateView):
    template_name = "customer_create.html"
    form_class = CustomerForm
    model = Customer
    success_url = "/webapp/customer-list/"



#----------------
#DELETE VIEWS
#----------------

class TripDeleteView(DeleteView):
    template_name = "trip_delete.html"
    model = Trip
    success_url = "/webapp/trip-list/"

class CustomerDeleteView(DeleteView):
    template_name="customer_delete.html"
    model = Customer
    success_url = "/webapp/customer-list/"


