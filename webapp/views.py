from django.shortcuts import render
from django.views.generic.base import TemplateView

from webapp.models import Customer


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

#------------------------
#DETAIL VIEWS
#------------------------

class CustomerDetailView(TemplateView):
    template_name = "customer_detail.html"

    def get_context_data(self, **kwargs):
        print("ContactDetailView -> get_context_data")
        kontext = super().get_context_data(**kwargs)
        print(kontext)
        return kontext


#----------------
#CREATE VIEWS
#----------------



#----------------
#UPDATE VIEWS
#----------------



#----------------
#DELETE VIEWS
#----------------


