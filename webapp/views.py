from django.shortcuts import render, redirect
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
        context ["trips"] = Trip.objects.all()
        return context


class CustomerListBaseView(TemplateView):
    template_name = "customer_list_base.html"

    def get(self, request, *args, **kwargs):
        customers = Customer.objects.all()
        if self.extra_context:
            self.extra_context["customers"] = customers
        else:
            self.extra_context = {"customers": customers}
        return super().get(request, *args, **kwargs)

class CustomerListingView(ListView):
    template_name = "customer_list.html"
    model = Customer




class TripListingView(ListView):
    template_name= "trip_list.html"
    model = Trip


#------------------------
#DETAIL VIEWS
#------------------------

class CustomerDetailView(TemplateView):
    #lists every customer in database
    template_name = "customer_detail.html"

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



#----------------
#CREATE VIEWS
#----------------

def customer_create(request):
    #class based form for customer registration, based on customer model, details in forms.py
    if request.method == "POST":
        print(request.POST)
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home_page")

    else:
        form = CustomerForm()

    return render(request, "customer_create.html", {"form": form})



def trip_create(request):
    #class based form for trip creation, based on trip model
    if request.method == "POST":
        form = TripForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/webapp/trip-list/")
    else:
        form = TripForm

    return render(request, "trip_create.html", {"form": form})


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
    model = CustomerAdmin
    success_url = "/webapp/customer-list/"


