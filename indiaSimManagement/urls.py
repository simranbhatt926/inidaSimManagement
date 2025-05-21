
from django.urls import path

from .views import *
from . import views
# from django.urls import path

urlpatterns = [
    path('india-sim-plans/', IndiaSimPlansAPI.as_view(), name='india-sim-plans'),
    path('filter-sim-packs/', views.FilteredSimPacksAPIView.as_view(), name='filter_sim_packs'),
    path('bsnl-special-plans/', BSNLSpecialPlansAPI.as_view(), name='bsnl-special-plans'),
    path('india-sim-port-number/', SimPortAPI.as_view(), name='indian-sim-ports'),
    path('states/', views.StateListCreateAPIView.as_view(), name='state-list-create'),
    path('states/<int:pk>/', views.StateDetailAPIView.as_view(), name='state-detail'),
    path('cities/', views.CityListCreateAPIView.as_view(), name='city-list-create'),
    path('cities/<int:pk>/', views.CityDetailAPIView.as_view(), name='city-detail'),
    # path('upload-image/', ImageUploadAPIView.as_view(), name='upload-image'),
    path('favourites/', FavouriteFRCPlansAPIView.as_view(), name='favourite-frc-plans'),
    path('operator-plan/', OperatorFRCPlansAPIView.as_view(), name='favourite-frc-plans'),
    path('check_pin/', views.CheckPincode.as_view(),name='check-pincode'),
    # path('cart-add/', AddToCartAPIView.as_view(), name='add-to-cart'),
    # path('cart/', CartListAPIView.as_view(), name='view-cart'),
    # path('cart-delete/<int:pk>/', DeleteCartItemAPIView.as_view(), name='delete-cart-item'),
    path("similar-frc-plans/", similar_plans_view, name="similar-frc-plans"),
    # add favourite pane and operater name 
    path('favourites/by-operator/', FavouritePlansByOperatorAPIView.as_view(), name='favourite-plans-by-operator'),
    path('favourites-by-operator/', FavouritePlansByOperatorOnlyAPIView.as_view(), name='favourites-by-operator'),

]



