# from django.shortcuts import render

# # Create your views here.
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import *
# from .serializers import *
# # 
# # views.py

# from django.contrib.auth import get_user_model
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth.hashers import check_password
# from django.contrib.auth.hashers import make_password
# from django.contrib.auth import authenticate


# # from .serializers import UserFavouritePlanSerializer

# User = get_user_model()

# # class UserWithFavouritePlansAPIView(APIView):
# #     def get(self, request, user_id):
# #         try:
# #             user = User.objects.get(id=user_id)
# #         except User.DoesNotExist:
# #             return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

# #         serializer = UserFavouritePlanSerializer(user)
# #         return Response(serializer.data, status=status.HTTP_200_OK)

# #test
# # # 
# # class UserWithFavouritePlansAPIView(APIView):
# #     def get(self, request, user_id):
# #         try:
# #             user = UserInfo.objects.get(id=user_id)
# #         except UserInfo.DoesNotExist:
# #             return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

# #         serializer = UserFavouritePlanSerializer(user)
# #         return Response(serializer.data, status=status.HTTP_200_OK)

# #  


# class UserWithFavouritePlansAPIView(APIView):
#     def get(self, request, user_id):
#         try:
#             user = UserInfo.objects.get(id=user_id)
#         except UserInfo.DoesNotExist:
#             return Response({"message": "User not found"}, status=404)

#         serializer = UserFavouritePlanSerializer(user, context={'request': request})
#         return Response(serializer.data , status=status.HTTP_200_OK)

# class SignupAPIView(APIView):
#     def post(self, request):
#         full_name = request.data.get('full_name')
#         email = request.data.get('email')
#         mobile_number = request.data.get('mobile_number')
#         address = request.data.get('address')
#         password = request.data.get('password')

#         # Check if email or mobile already exists
#         if UserInfo.objects.filter(models.Q(email=email) | models.Q(mobile_number=mobile_number)).exists():
#             return Response({"error": "User already exists with this email or mobile number."}, status=400)

#         # Save user (with hashed password)
#         hashed_password = make_password(password)
#         user = UserInfo.objects.create(
#             full_name=full_name,
#             email=email,
#             mobile_number=mobile_number,
#             address=address,
#             password=hashed_password
#         )

#         return Response({"message": "Signup successful", "user_id": user.id}, status=201)


# class LoginAPIView(APIView):
#     def post(self, request):
#         identifier = request.data.get('email') or request.data.get('mobile_number')
#         password = request.data.get('password')

#         try:
#             # Allow login with either email or mobile number
#             user = UserInfo.objects.get(models.Q(email=identifier) | models.Q(mobile_number=identifier))

#             # ✅ Use check_password here!
#             if not check_password(password, user.password):
#                 return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)

#             # ✅ Generate JWT token
#             refresh = RefreshToken.for_user(user)

#             return Response({
#                 "message": "Login successful",
#                 "access": str(refresh.access_token),
#                 "refresh": str(refresh),
#                 "user": {
#                     "id": user.id,
#                     "full_name": user.full_name,
#                     "email": user.email,
#                     "mobile_number": user.mobile_number,
#                     "address": user.address,
#                     "is_active": user.is_active
#                 }
#             })

#         except UserInfo.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#         # class UserInfoAPIView(APIView):
# #     def get(self, request):
# #         users = UserInfo.objects.filter(is_active=True)
# #         serializer = UserInfoSerializer(users, many=True)
# #         return Response(serializer.data, status=status.HTTP_200_OK)

# #     def post(self, request):
# #         data = request.data.copy()
# #         data['is_active'] = True  # force is_active = True
# #         serializer = UserInfoSerializer(data=data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # add user favourite plan view
# # class AddFavouritePlanAPIView(APIView):
# #     def post(self, request):
# #         serializer = FavouritePlanCreateSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response({
# #                 "message": "Favourite plan added successfully",
# #                 "data": serializer.data
# #             }, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class AddFavouritePlanAPIView(APIView):
#     def post(self, request):
#         user_id = request.query_params.get('user')
#         plan_id = request.query_params.get('plan')

#         # ✅ Check if user exists
#         try:
#             user = UserInfo.objects.get(id=user_id)
#         except UserInfo.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#         # ✅ Check if plan exists
#         try:
#             plan = IndiaFRCSimPack.objects.get(id=plan_id)
#         except IndiaFRCSimPack.DoesNotExist:
#             return Response({"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND)

#         # ✅ Save favourite
#         favourite = UserFavouriteSimPlan.objects.create(user=user, plan=plan)

#         # ✅ Prepare response
#         user_data = {
#     "id": user.id,
#     "full_name": user.full_name,
#     "email": user.email
# }


#         plan_data = FullPlanSerializer(plan, context={'request': request}).data
#         plan_data["current_time"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

#         return Response({
#             "message": "Favourite plan added successfully",
#             "user": user_data,
#             "favourite_plan": plan_data
#         }, status=status.HTTP_201_CREATED)

# # cancel Favourite plan

# class CancelFavouritePlanAPIView(APIView):
#     def delete(self, request):
#         user_id = request.query_params.get('user')
#         plan_id = request.query_params.get('plan')

#         if not user_id or not plan_id:
#             return Response({"error": "Both 'user' and 'plan' parameters are required."}, status=400)

#         try:
#             user = UserInfo.objects.get(id=user_id)
#         except UserInfo.DoesNotExist:
#             return Response({"error": "User not found."}, status=404)

#         try:
#             fav = UserFavouriteSimPlan.objects.filter(user_id=user_id, plan_id=plan_id).first()
#             if not fav:
#                 return Response({"message": "No such favourite plan found for this user."}, status=404)
            
#             fav.delete()

#         except Exception as e:
#             return Response({"error": str(e)}, status=500)

#         # Get remaining favourite plans
#         remaining_links = UserFavouriteSimPlan.objects.filter(user=user)
#         remaining_plans = [link.plan for link in remaining_links]

#         if remaining_plans:
#             serialized_plans = FullPlanSerializer(remaining_plans, many=True, context={'request': request}).data
#         else:
#             serialized_plans = "No active favourite plans."

#         return Response({
#             "message": "1 favourite plan cancelled successfully.",
#             "user": {
#                 "id": user.id,
#                 "full_name": user.full_name,
#                 "email": user.email,
#                 "current_time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
#             },
#             "remaining_favourites": serialized_plans
#         }, status=200)


# 
# 
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import models
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime
from rest_framework.permissions import IsAuthenticated

from .models import UserInfo, IndiaFRCSimPack, UserFavouriteSimPlan
from .serializers import *


class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        full_name = request.data.get('full_name')
        email = request.data.get('email')
        mobile_number = request.data.get('mobile_number')
        address = request.data.get('address')
        password = request.data.get('password')

        if UserInfo.objects.filter(models.Q(email=email) | models.Q(mobile_number=mobile_number)).exists():
            return Response({"error": "User already exists with this email or mobile number."}, status=400)

        hashed_password = make_password(password)
        user = UserInfo.objects.create(
            full_name=full_name,
            email=email,
            mobile_number=mobile_number,
            address=address,
            password=hashed_password
        )

        return Response({"message": "Signup successful", "user_id": user.id}, status=201)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        identifier = request.data.get('email') or request.data.get('mobile_number')
        password = request.data.get('password')

        try:
            user = UserInfo.objects.get(models.Q(email=identifier) | models.Q(mobile_number=identifier))

            if not check_password(password, user.password):
                return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "Login successful",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "email": user.email,
                    "mobile_number": user.mobile_number,
                    "address": user.address,
                    "is_active": user.is_active
                }
            })

        except UserInfo.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class UserWithFavouritePlansAPIView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(UserInfo, id=user_id)
        serializer = UserFavouritePlanSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddFavouritePlanAPIView(APIView):
    def post(self, request):
        user_id = request.query_params.get('user')
        plan_id = request.query_params.get('plan')

        user = get_object_or_404(UserInfo, id=user_id)
        plan = get_object_or_404(IndiaFRCSimPack, id=plan_id)

        favourite = UserFavouriteSimPlan.objects.create(user=user, plan=plan)

        user_data = {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email
        }

        plan_data = FullPlanSerializer(plan, context={'request': request}).data
        plan_data["current_time"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        return Response({
            "message": "Favourite plan added successfully",
            "user": user_data,
            "favourite_plan": plan_data
        }, status=status.HTTP_201_CREATED)


class CancelFavouritePlanAPIView(APIView):
    def delete(self, request):
        user_id = request.query_params.get('user')
        plan_id = request.query_params.get('plan')

        if not user_id or not plan_id:
            return Response({"error": "Both 'user' and 'plan' parameters are required."}, status=400)

        user = get_object_or_404(UserInfo, id=user_id)
        fav = UserFavouriteSimPlan.objects.filter(user_id=user_id, plan_id=plan_id).first()

        if not fav:
            return Response({"message": "No such favourite plan found for this user."}, status=404)

        fav.delete()

        remaining_links = UserFavouriteSimPlan.objects.filter(user=user)
        remaining_plans = [link.plan for link in remaining_links]

        serialized_plans = (
            FullPlanSerializer(remaining_plans, many=True, context={'request': request}).data
            if remaining_plans else "No active favourite plans."
        )

        return Response({
            "message": "1 favourite plan cancelled successfully.",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "current_time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            },
            "remaining_favourites": serialized_plans
        }, status=200)




# logout

class LogoutAPIView(APIView):

    permission_classes = [IsAuthenticated]
    

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()  # Only works if blacklist app is installed

            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response({"error": "Invalid token or already logged out."}, status=status.HTTP_400_BAD_REQUEST)
