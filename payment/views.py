# # import json
# # import time
# # import requests
# # import base64
# # import hmac
# # import hashlib

# # from django.http import JsonResponse
# # from django.views.decorators.csrf import csrf_exempt

# # # ------------------------------------------------------------------------------
# # # 🧪 Dummy Operator & Plan Data (for India SIM Management)
# # # ------------------------------------------------------------------------------

# # DUMMY_OPERATORS = {
# #     1: {"name": "Jio"},
# #     2: {"name": "Airtel"},
# # }

# # DUMMY_PLANS = {
# #     1: {"title": "Unlimited 1.5GB/day", "price": 239},
# #     2: {"title": "Data Booster", "price": 98},
# # }

# # # ------------------------------------------------------------------------------
# # # 🔐 BillDesk Config (Use actual credentials in production)
# # # ------------------------------------------------------------------------------

# # BILLDESK_MERCHANT_ID = "YourMerchantID"
# # BILLDESK_SECRET_KEY = b"YourSecretKey"  # Must be in bytes
# # BILLDESK_CLIENT_ID = "YourClientID"
# # BILLDESK_ORDER_CREATE_URL = "https://pguat.billdesk.io/payments/ve1_2/orders/create"
# # BILLDESK_RETURN_URL = "https://yourwebsite.com/payment/response"

# # # ------------------------------------------------------------------------------
# # # 🔏 Generate JWS-HMAC Signature
# # # ------------------------------------------------------------------------------

# # def generate_signed_billdesk_payload(payload_dict):
# #     header = {
# #         "alg": "HS256",
# #         "clientid": BILLDESK_CLIENT_ID
# #     }
# #     header_encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
# #     payload_encoded = base64.urlsafe_b64encode(json.dumps(payload_dict).encode()).decode().rstrip("=")
# #     data = f"{header_encoded}.{payload_encoded}"
# #     signature = hmac.new(BILLDESK_SECRET_KEY, data.encode(), hashlib.sha256).digest()
# #     signature_encoded = base64.urlsafe_b64encode(signature).decode().rstrip("=")
# #     return f"{data}.{signature_encoded}"

# # # ------------------------------------------------------------------------------
# # # 🚀 Main API: SIM Plan Checkout (COD / FULL / PARTIAL Payment)
# # # ------------------------------------------------------------------------------

# # @csrf_exempt
# # def sim_plan_checkout_view(request):
# #     if request.method != 'POST':
# #         return JsonResponse({"error": "Only POST method allowed"}, status=405)

# #     try:
# #         # 🔍 Extract input
# #         data = json.loads(request.body)
# #         user = request.user
# #         operator_id = data.get("operator_id")
# #         plan_id = data.get("plan_id")
# #         connection_mode = data.get("connection_mode")
# #         payment_mode = data.get("payment_mode")

# #         operator = DUMMY_OPERATORS.get(operator_id)
# #         plan = DUMMY_PLANS.get(plan_id)

# #         if not operator:
# #             return JsonResponse({"error": "Invalid operator_id"}, status=404)
# #         if not plan:
# #             return JsonResponse({"error": "Invalid plan_id"}, status=404)

# #         # 🧾 Order Info
# #         order_details = {
# #             "user_account_name": getattr(user, "username", "guest_user"),
# #             "sim_operator_name": operator["name"],
# #             "sim_plan_title": plan["title"],
# #             "sim_plan_price": plan["price"],
# #             "sim_connection_mode": connection_mode,
# #             "payment_mode_selected": payment_mode,
# #             "order_created_timestamp": int(time.time())
# #         }

# #         # 🧾 COD (No Payment)
# #         if payment_mode == "cod":
# #             return JsonResponse({
# #                 "payment_status": "success",
# #                 "payment_message": "Order placed using Cash on Delivery.",
# #                 "user_order_details": order_details
# #             })

# #         # 💳 Prepare Payment Payload
# #         payable_amount = "50.00" if payment_mode == "partial" else f"{plan['price']:.2f}"
# #         order_id = f"ORDER{int(time.time())}"

# #         # 🧪 Dummy Payment Response (since real BillDesk not working)
# #         return JsonResponse({
# #             "payment_status": "pending",
# #             "payment_message": "Redirect to BillDesk (dummy response used)",
# #             "payment_gateway_order_id": order_id,
# #             "payment_auth_token": "DummyAuthToken123456",
# #             "payment_merchant_id": BILLDESK_MERCHANT_ID,
# #             "payment_flow_type": "payments",
            
# #             "payment_amount": payable_amount,
# #             "user_order_details": order_details
# #         })

# #     except Exception as e:
# #         return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=500)


# import json
# import time
# import base64
# import hmac
# import hashlib
# import requests

# from django.http import JsonResponse
# from django.views import View
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator

# # --------------------------------------------------------------------------
# # 🧪 Dummy Data for India SIM Management
# # --------------------------------------------------------------------------

# DUMMY_OPERATORS = {
#     1: {"name": "Jio"},
#     2: {"name": "Airtel"},
# }

# DUMMY_PLANS = {
#     1: {"title": "Unlimited 1.5GB/day", "price": 239},
#     2: {"title": "Data Booster", "price": 98},
# }

# # --------------------------------------------------------------------------
# # 🔐 Dummy BillDesk Config (Replace in real use)
# # --------------------------------------------------------------------------

# BILLDESK_MERCHANT_ID = "YourMerchantID"
# BILLDESK_SECRET_KEY = b"YourSecretKey"
# BILLDESK_CLIENT_ID = "YourClientID"
# BILLDESK_ORDER_CREATE_URL = "https://pguat.billdesk.io/payments/ve1_2/orders/create"
# BILLDESK_RETURN_URL = "https://yourwebsite.com/payment/response"

# # --------------------------------------------------------------------------
# # 🔏 BillDesk Signature Generator (JWS-HMAC)
# # --------------------------------------------------------------------------

# def generate_signed_billdesk_payload(payload_dict):
#     header = {
#         "alg": "HS256",
#         "clientid": BILLDESK_CLIENT_ID
#     }
#     header_encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
#     payload_encoded = base64.urlsafe_b64encode(json.dumps(payload_dict).encode()).decode().rstrip("=")
#     data = f"{header_encoded}.{payload_encoded}"
#     signature = hmac.new(BILLDESK_SECRET_KEY, data.encode(), hashlib.sha256).digest()
#     signature_encoded = base64.urlsafe_b64encode(signature).decode().rstrip("=")
#     return f"{data}.{signature_encoded}"

# # --------------------------------------------------------------------------
# # 🚀 Class-Based View: SIM Plan Checkout (GET + POST)
# # --------------------------------------------------------------------------

# @method_decorator(csrf_exempt, name='dispatch')
# class SimPlanCheckoutView(View):

#     def get(self, request):
#         return JsonResponse({
#             "message": "Available SIM Operators and Plans",
#             "sim_operators": DUMMY_OPERATORS,
#             "sim_plans": DUMMY_PLANS
#         }, status=200)

#     def post(self, request):
#         try:
#             data = json.loads(request.body)
#             user = request.user
#             operator_id = data.get("operator_id")
#             plan_id = data.get("plan_id")
#             connection_mode = data.get("connection_mode")
#             payment_mode = data.get("payment_mode")

#             operator = DUMMY_OPERATORS.get(operator_id)
#             plan = DUMMY_PLANS.get(plan_id)

#             if not operator:
#                 return JsonResponse({"error": "Invalid operator_id"}, status=404)
#             if not plan:
#                 return JsonResponse({"error": "Invalid plan_id"}, status=404)

#             # 🧾 Order Details Dictionary
#             order_details = {
#                 "user_account_name": getattr(user, "username", "guest_user"),
#                 "sim_operator_name": operator["name"],
#                 "sim_plan_title": plan["title"],
#                 "sim_plan_price": plan["price"],
#                 "sim_connection_mode": connection_mode,
#                 "payment_mode_selected": payment_mode,
#                 "order_created_timestamp": int(time.time())
#             }

#             # COD Handling
#             if payment_mode == "cod":
#                 return JsonResponse({
#                     "payment_status": "success",
#                     "payment_message": "Order placed using Cash on Delivery.",
#                     "remaining_due_amount": 0,
#                     "user_order_details": order_details
#                 })

#             # Payment Info
#             payable_amount = "50.00" if payment_mode == "partial" else f"{plan['price']:.2f}"
#             order_id = f"ORDER{int(time.time())}"

#             # 🧮 Remaining Amount for Partial
#             remaining_due_amount = 0
#             if payment_mode == "partial":
#                 remaining_due_amount = round(plan["price"] - 50, 2)

#             # 🔁 Dummy BillDesk response (no real API call)
#             return JsonResponse({
#                 "payment_status": "pending",
#                 "payment_message": "Redirect to BillDesk (dummy response used)",
#                 "payment_gateway_order_id": order_id,
#                 "payment_auth_token": "DummyAuthToken123456",
#                 "payment_merchant_id": BILLDESK_MERCHANT_ID,
#                 "payment_flow_type": "payments",
#                 "payment_amount": payable_amount,
#                 "remaining_due_amount": remaining_due_amount,
#                 "user_order_details": order_details
#             })

#         except Exception as e:
#             return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=500)



# add


from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from user.models import UserFavouriteSimPlan, UserInfo
from indiaSimManagement.models import IndiaFRCSimPack
import json, time

@method_decorator(csrf_exempt, name='dispatch')
class FavouriteSimPlanCheckoutView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            favourite_sim_plan_id = data.get("favourite_sim_plan_id")
            payment_mode = data.get("payment_mode")

            if not (user_id and favourite_sim_plan_id and payment_mode):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # ✅ Get the favourite record (plan + user)
            try:
                favourite = UserFavouriteSimPlan.objects.select_related('user', 'plan').get(
                    id=favourite_sim_plan_id, user_id=user_id
                )
            except UserFavouriteSimPlan.DoesNotExist:
                return JsonResponse({"error": "Favourite plan not found"}, status=404)

            user = favourite.user
            plan = favourite.plan

            # ✅ Extract accurate data
            plan_price = float(plan.amount.pack_amount)
            plan_title = plan.plan_description
            operator_name = plan.operator.operator_name if plan.operator else "Unknown"
            connection_mode = plan.connection

            order_id = f"ORDER{int(time.time())}"
            payable_amount = 50.00 if payment_mode == "partial" else plan_price
            remaining_due = round(plan_price - 50.00, 2) if payment_mode == "partial" else 0.00
            next_payment = "COD or Online" if payment_mode == "partial" else "none"

            # ✅ Build response
            return JsonResponse({
                "payment_status": "success" if payment_mode == "cod" else "pending",
                "payment_message": "Order placed using COD" if payment_mode == "cod" else "Proceed to payment gateway",
                "payment_amount": payable_amount,
                "remaining_due_amount": remaining_due,
                "next_payment_mode": next_payment,
                "payment_gateway_order_id": None if payment_mode == "cod" else order_id,
                "favourite_plan_details": {
                    "user_name": user.full_name,
                    "sim_operator": operator_name,
                    "sim_plan_title": plan_title,
                    "price": plan_price,
                    "connection_mode": connection_mode
                }
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
