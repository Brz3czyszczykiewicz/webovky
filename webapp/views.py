from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from webapp.forms import CustomerForm, TripForm
from webapp.models import Customer
from . import models



#----------------
#LIST VIEWS
#----------------

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
    template_name = "customer_list"
    model = Customer


def destinations(request):
    all_trips = models.Trip.objects.all()
    return render(request, "destinationss.html", {"trip": all_trips})

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




#----------------
#CREATE VIEWS
#----------------

def customer_create(request):
    #class based form for customer registration, based on customer model, deitals in forms.py
    if request.method == "POST":
        print(request.POST)
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Poptávka odeslána")

    else:
        form = CustomerForm()

    return render(request, "customer_create.html", {"form": form})



def trip_create(request):
    #class based form for trip creation, based on trip model
    if request.method == "POST":
        pass
    else:
        form = TripForm

    return render(request, "trip_create.html", {"form": form})


#----------------
#UPDATE VIEWS
#----------------



#----------------
#DELETE VIEWS
#----------------


