# from django.shortcuts import render

# # Create your views here.
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from .models import Checkout, Payment
# from .serializers import CheckoutSerializer, PaymentSerializer
# from user.models import *

# # class CheckoutCreateView(APIView):
# #     permission_classes = [permissions.IsAuthenticated]

# #     def post(self, request):
# #         user = request.user

# #         # Check: Kya user ka plan selected hai?
# #         if not user.plan:  # Assuming 'plan' is a field in your CustomUser model
# #             return Response(
# #                 {"error": "You must select a plan before checkout."},
# #                 status=status.HTTP_400_BAD_REQUEST
# #             )

# #         data = {
# #             "user": user.id,
# #             "plan": user.plan  # Automatically le lo jo user ne select kiya
# #         }

# #         serializer = CheckoutSerializer(data=data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=201)
# #         return Response(serializer.errors, status=400)
# # 
# # dont used coustom model

# # class CheckoutCreateView(APIView):
# #     permission_classes = [permissions.IsAuthenticated]

# #     def post(self, request):
# #         user = request.user

# #         # Check if the user has at least one favourite plan
# #         favourite = Favourite.objects.filter(user=user).last()  # You can use .first() or apply filter for latest

# #         if not favourite:
# #             return Response(
# #                 {"error": "Please select a plan before proceeding to checkout."},
# #                 status=status.HTTP_400_BAD_REQUEST
# #             )

# #         data = {
# #             "user": user.id,
# #             "plan": favourite.plan.id,  # Assuming plan is a FK
# #             "operator": favourite.operator.id,
# #             "connection_mode": favourite.connection_mode.id,
# #             "payment_method": request.data.get("payment_method")  # online, cod, partial
# #         }

# #         serializer = CheckoutSerializer(data=data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=201)
# #         return Response(serializer.errors, status=400)


# # Payment choices for validation
# VALID_PAYMENT_METHODS = ['FULL', 'COD', 'PARTIAL']


# class CheckoutPreviewAPIView(APIView):
#     """
#     Accepts checkout info and returns it as a structured preview.
#     No database operations are performed.
#     """

#     def post(self, request):
#         # Extract input fields
#         full_name = request.data.get('full_name')
#         mobile = request.data.get('mobile')
#         address = request.data.get('address')
#         payment_method = request.data.get('payment_method')
#         amount_paid = request.data.get('amount_paid')

#         # Basic validations (can be improved as needed)
#         errors = {}

#         if not full_name:
#             errors['full_name'] = 'This field is required.'
#         if not mobile:
#             errors['mobile'] = 'This field is required.'
#         if not address:
#             errors['address'] = 'This field is required.'
#         if payment_method not in VALID_PAYMENT_METHODS:
#             errors['payment_method'] = f'Choose one of {VALID_PAYMENT_METHODS}'
#         if amount_paid is None:
#             errors['amount_paid'] = 'This field is required.'

#         # Return errors if any
#         if errors:
#             return Response(errors, status=status.HTTP_400_BAD_REQUEST)

#         # Logic to check if fully paid
#         is_fully_paid = payment_method == "FULL"

#         # Prepare key-value dict response
#         preview_data = {
#             "full_name": full_name,
#             "mobile": mobile,
#             "address": address,
#             "payment_method": payment_method,
#             "amount_paid": float(amount_paid),
#             "is_fully_paid": is_fully_paid,
#             "note": "This is a preview only. No data has been saved."
#         }

#         return Response(preview_data, status=status.HTTP_200_OK)


# # 


# class FullPaymentView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         data = {
#             "checkout": request.data["checkout_id"],
#             "payment_type": "FULL",
#             "paid_now": request.data.get("paid_now", 0),
#             "transaction_id": request.data.get("transaction_id")
#         }
#         serializer = PaymentSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)

# class CodPaymentView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         data = {
#             "checkout": request.data["checkout_id"],
#             "payment_type": "COD"
#         }
#         serializer = PaymentSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)

# class PartialPaymentView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         data = {
#             "checkout": request.data["checkout_id"],
#             "payment_type": "PARTIAL",
#             "paid_now": 50,
#             "pay_later_mode": request.data.get("pay_later_mode"),
#             "transaction_id": request.data.get("transaction_id")
#         }
#         serializer = PaymentSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)



# add

