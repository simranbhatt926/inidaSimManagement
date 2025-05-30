# from django.urls import path
# from .views import *

# urlpatterns = [
#     # path("checkout/", sim_plan_checkout_view, name="sim-plan-checkout"),
#     # path("checkout/", SimPlanCheckoutView.as_view(), name="sim-plan-checkout"),

#     # add

  
#     # path("fav-checkout/", FavouritePlanCheckoutView.as_view(), name="fav-checkout"),
#     # path("sim-checkout/", FavouriteSimPlanCheckoutView.as_view(), name="sim-checkout"),

# #   path("fav-checkout/", UserFavouriteSimPlan.as_view(), name="fav-checkout"),
#  path('sim-checkout/', FavouriteSimPlanCheckoutView.as_view(), name='sim-checkout'),
    
# ]

from django.urls import path
from .views import *

urlpatterns = [
    # path('my-favourite-plans/', UserFavouriteSimPlan.as_view(), name='my-fav-plans'),
    path("sim-checkout/", FavouriteSimPlanCheckoutView.as_view(), name="sim-checkout"),
]