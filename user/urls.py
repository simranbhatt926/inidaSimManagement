from django.urls import path
from .views import *

urlpatterns = [
    # path('user-info/', UserInfoAPIView.as_view(), name='user-info'),
    path('signup/', SignupAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view(), name='logout'),

    path('user-favourites/<int:user_id>/', UserWithFavouritePlansAPIView.as_view(), name='user-favourite-plans'),
    path('add-favourite/', AddFavouritePlanAPIView.as_view(), name='add-favourite'),
    path('cancel-favourite/', CancelFavouritePlanAPIView.as_view(), name='cancel-favourite'),
]
