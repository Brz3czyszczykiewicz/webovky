"""
URL configuration for CKWAPP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from webapp.views import (CustomerDetailView,
                          CustomerListingView, CustomerCreateView, TripCreateView,
                          work_in_progress, TripListingView, TripUpdateView,
                          TripDeleteView, send_image, TripDetailView, CustomerUpdateView,
                          CustomerDeleteView, TripAdminView)


app_name = 'webapp'

urlpatterns = [
    path('admin/', admin.site.urls),
#LISTING
    path("image/", send_image, name="send_image"),

    path("customer-list/", CustomerListingView.as_view(), name='customer_list'),

    path("trip-list/", TripListingView.as_view(), name="trip_list"),

    path("work-in-progress/", work_in_progress, name="work_in_progress"),


#DETAIL

    path("customer-detail/<int:pk>/", CustomerDetailView.as_view(), name='customer_detail'),
    path("trip-detail/<int:pk>/", TripDetailView.as_view(), name='trip_detail'),
    path("trip-admin-detail/<int:pk>/", TripAdminView.as_view(), name="trip_detail_admin"),

#CREATE
    path("trip-detail/<int:pk>/customer-create/", CustomerCreateView.as_view(), name='customer_create'),
    path("trip-create/", TripCreateView.as_view(), name="trip_create"),



#UPDATE
    path("trip-update/<int:pk>/", TripUpdateView.as_view(), name="trip_update"),
    path("customer-update/<int:pk>/", CustomerUpdateView.as_view(), name="customer_update"),



#DELETE
    path("trip-delete/<int:pk>/", TripDeleteView.as_view(), name="trip_delete"),
    path("customer-delete/<int:pk>/", CustomerDeleteView.as_view(), name="customer_delete")
]
