from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
# from prune.authentication import JWTAuthentication
from .services import SimPlanService,SimPortService
from django.http import JsonResponse
# from userManagement.models import Cart
from .models import *
from .serializers import *


class IndiaSimPlansAPI(APIView):
  
    def get(self, request):
        mode     = request.query_params.get('mode', '').lower()
        operator = request.query_params.get('operator', '').lower()
        city     = request.query_params.get('city', '').lower()
        state    = request.query_params.get('state', '').lower()

        validation_error = self._validate_parameters(mode, operator)
        if validation_error:
            return validation_error

        try:
            if mode and not operator:
                plans = SimPlanService.get_plan_by_mode(mode)
                
            elif operator and mode and not state and not city:
                # Filter by operator and city
                plans = SimPlanService.get_operator_plans(operator, mode)
            elif operator and state and not city:

                state = state.upper()
                state_obj = State.objects.get(state__iexact=state)
                plans = SimPlanService.get_operator_state_plans(operator, mode, state_obj.id)
            elif state and operator and city:

                state_obj = State.objects.get(state__iexact=state)
                circle_id = City.objects.get(city__iexact=city)


                plans = SimPlanService.get_state_city_plans(mode, operator,state_obj.id,circle_id.id)
           
            else:
                # Default case (should be handled by validation)
                plans = {"selected_sim_packages_all": []}
            

            scheme = 'https' if request.is_secure() else 'http'
            domain = request.get_host()
            base_url = f"{scheme}://{domain}"

            for pack in plans.get('selected_sim_packages_all', []):
                operator = pack.get('operator', {})
                operator_image = operator.get('operator_image')
                if operator_image:
                    full_image_url = base_url + operator_image  # .lstrip('/') optional if path starts with '/'
                    print('Operator image URL:', full_image_url)
                    operator['operator_image'] = full_image_url  # Update image path to full URL




            return Response({
                'status': True,
                'mode': mode,
                'operator': operator,
                'state': state,
                'city': city,
                'sim_packs': plans.get("selected_sim_packages_all", []),
            })

        except City.DoesNotExist:
            return Response(
                {'status': False, 'message': 'City not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except State.DoesNotExist:
            return Response(
                {'status': False, 'message': 'State not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'status': False, 'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _validate_parameters(self, mode, operator):
        valid_modes = {"prepaid", "postpaid", ""}
        valid_operators = {"vi", "bsnl", "jio", "airtel", ""}

        if mode and mode not in valid_modes:
            return Response(
                {'status': False, 'message': 'Invalid mode'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if operator and operator not in valid_operators:
            return Response(
                {'status': False, 'message': 'Invalid operator'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return None



class FilteredSimPacksAPIView(APIView):
    def get(self, request):
        plan_type = request.query_params.get('plan_type')

        if plan_type == 'traveller':
            plans = IndiaFRCSimPack.objects.filter(traveller_plan=True, is_active=True)
        elif plan_type == 'best_data':
            plans = IndiaFRCSimPack.objects.filter(best_data_uasage=True, is_active=True)
        elif plan_type == 'affordable':
            plans = IndiaFRCSimPack.objects.filter(most_affordable=True, is_active=True)
        else:
            return Response({"error": "Invalid or missing 'plan_type' query parameter"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = IndiaFRCSimPackSerializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BSNLSpecialPlansAPI(APIView):
    def get(self, request):
        mode = request.query_params.get('mode', 'prepaid').capitalize()
        
        try:
            plans = SimPlanService.get_bsnl_plans(mode)
            return Response({
                'status': 'success',
                'mode': mode,
                'operator': 'bsnl',
                'plans': plans
            })
        except Exception as e:
            return Response(
                {'status': 'error', 'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SimPortAPI(APIView):
    def get(self, request):
        mode = request.query_params.get('mode', '').lower()
        print(mode,'mode')
        operator = request.query_params.get('operator', '').lower()
        circle = request.query_params.get('circle', 'Delhi')
        if mode not in ['prepaid', 'postpaid']:
            return JsonResponse({"error": "Invalid mode. Use prepaid or postpaid."}, status=400)
        operator = request.query_params.get('operator', '').lower()

        # Get circle from query params
        circle = request.GET.get('circle', 'Delhi')

        # Get data from service
        context, error, status = SimPortService.get_sim_data(mode, operator, circle)
        
        if error:
            return JsonResponse(error, status=status)

        return Response(context)
    

class StateListCreateAPIView(APIView):
    def get(self, request):
        states = State.objects.all()
        serializer = StateSerializer(states, many=True,context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = StateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StateDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return State.objects.get(pk=pk)
        except State.DoesNotExist:
            return None

    def get(self, request, pk):
        state = self.get_object(pk)
        if not state:
            return Response(
                {"error": "State not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = StateSerializer(state)
        return Response(serializer.data)

    def put(self, request, pk):
        state = self.get_object(pk)
        if not state:
            return Response(
                {"error": "State not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = StateSerializer(state, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        state = self.get_object(pk)
        if not state:
            return Response(
                {"error": "State not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = StateSerializer(state, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        state = self.get_object(pk)
        if not state:
            return Response(
                {"error": "State not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        state.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CityListCreateAPIView(APIView):
    def get(self, request):
        state_id = request.query_params.get('state_id')
        cities = City.objects.all()
        if state_id:
            cities = cities.filter(state_id=state_id)
        serializer = CitySerializer(cities, many=True,context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class CityDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return City.objects.get(pk=pk)
        except City.DoesNotExist:
            return None

    def get(self, request, pk):
        city = self.get_object(pk)
        if not city:
            return Response(
                {"error": "City not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CitySerializer(city)
        return Response(serializer.data)

    def put(self, request, pk):
        city = self.get_object(pk)
        if not city:
            return Response(
                {"error": "City not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CitySerializer(city, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        city = self.get_object(pk)
        if not city:
            return Response(
                {"error": "City not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CitySerializer(city, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        city = self.get_object(pk)
        if not city:
            return Response(
                {"error": "City not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        city.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# class ImageUploadAPIView(APIView):
#     def post(self, request):
#         serializer = ImageUploadSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "message": "Image uploaded successfully",
#                 "data": serializer.data
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# class ImageListAPIView(APIView):
#     def get(self, request):
#         images = ImageUpload.objects.filter(hero_section=True).order_by('-uploaded_at')
#         serializer = ImageUploadSerializer(images, many=True, context={'request': request})
#         return Response({
#             "message": "Hero section images retrieved successfully",
#             "data": serializer.data
#         }, status=status.HTTP_200_OK)



class FavouriteFRCPlansAPIView(APIView):
    def get(self, request):
        connection_mode = request.query_params.get('connection_mode', None)
        connection_mode = connection_mode.capitalize()
        print(connection_mode,'cnmode')

        # Start with active and favourite plans
        frc_plans = IndiaFRCSimPack.objects.filter(favourite_marked=True, is_active=True)

        # Filter by connection mode if provided
        if connection_mode in ['Prepaid', 'Postpaid']:
            frc_plans = frc_plans.filter(connection=connection_mode)


      
        serializer = IndiaFRCSimPackSerializer(frc_plans, many=True, context={'request': request})
        return Response({
            "message": "Favourite FRC plans retrieved successfully",
            "selected_sim_packages_all": serializer.data
        }, status=status.HTTP_200_OK)

    


class OperatorFRCPlansAPIView(APIView):
    def get(self, request):
        operator_id = request.query_params.get('operator')
        connection = request.query_params.get('connection')  # should be 'Prepaid' or 'Postpaid'
        connection = connection.capitalize()
        # Base queryset
        queryset = IndiaFRCSimPack.objects.filter(is_active=True)

        if operator_id:
            queryset = queryset.filter(operator__operator_name__iexact=operator_id)

        if connection in ['Prepaid', 'Postpaid']:
            queryset = queryset.filter(connection=connection)

        queryset = queryset.order_by('-priority')

        serializer = IndiaFRCSimPackSerializer(queryset, many=True, context={'request': request})
        return Response({
            "message": f"{operator_id} plans retrieved successfully",
            "sim_packs": serializer.data
        }, status=status.HTTP_200_OK)
    

class CheckPincode(APIView):
    permission_classes = [AllowAny]
    """
    Get all sim packs
    """
    def get(self, request, format=None):
        pin_code = request.GET.get('pin_code', None)
        accepted_pincode = AcceptedPinCode.objects.filter(pin_code=pin_code, is_active=True).first()
        if accepted_pincode:
            # pin_code_city = City.objects.filter(deliverypincode__pincode=pin_code, is_active=True).first()
            is_cod = False
            if accepted_pincode.is_cod == True:
                is_cod = True
            else:
                is_cod = False
            return  JsonResponse({"status":  True if accepted_pincode else False, "cod":is_cod}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"status":False, "cod":False}, status=status.HTTP_200_OK)


class ConversionData(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    """
    Get all contant
    """

    def get(self, request, format=None):
        try:
            print("00000000000000000000000")
            all_const = Constants.objects.all()
            dict_ = {}
            for key in all_const:
                dict_[key.key] = key.value

            return Response({"data" : dict_}, status=status.HTTP_200_OK)
        except:
            return Response({"error" : 'need any one value in key variable you sending'}, status=status.HTTP_400_BAD_REQUEST)




# class AddToCartAPIView(generics.CreateAPIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     serializer_class = CartSerializer

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# class CartListAPIView(generics.ListAPIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     serializer_class = CartSerializer

#     def get_queryset(self):
#         return Cart.objects.filter(user=self.request.user, is_ordered=False)

# class DeleteCartItemAPIView(generics.DestroyAPIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     serializer_class = CartSerializer
#     queryset = Cart.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user, is_ordered=False)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "success": True,
            "status": 200,
            "message": "Cart item deleted successfully."
        }, status=status.HTTP_200_OK)
    

from django.db.models import F, Q
def similar_plans_view(request):
    # print("Testhjjhjhjhjj")
    try:
        amount = float(request.GET.get("amount"))
        operator_name = request.GET.get("operator")  # e.g., 'JO' for Jio

        # Get the current operator
        current_operator = Operator.objects.filter(operator_name__iexact=operator_name).first()
        print(current_operator,'operator')

        if not current_operator:
            return JsonResponse({"error": "Invalid operator code"}, status=status.HTTP_400_BAD_REQUEST)

        # Define the range of amount ±30 to 50
        lower_limit = amount - 50
        upper_limit = amount + 50

        # Get packs for other operators (excluding the current one)
        other_packs = IndiaFRCSimPack.objects.filter(
            ~Q(operator=current_operator),
            amount__pack_amount__gte=lower_limit,
            amount__pack_amount__lte=upper_limit,
            is_active=True
        ).select_related('operator', 'amount', 'validity')

        # Serialize the data
        result = []
        for pack in other_packs:
            result.append({
                "id": pack.id,
                "operator": {
                    "operator_name": pack.operator.operator_name,
                    "operator_code": pack.operator.operator_code,
                    "operator_image": pack.operator.operator_image.url if pack.operator.operator_image else ""
                },
                "validity": pack.validity.pack_validity if pack.validity else "",
                "amount": str(pack.amount.pack_amount),
                "connection": pack.connection,
                "plan_description": pack.plan_description,
                "plan_benefits": pack.plan_benefits,
                "india_sim_url": pack.india_sim_url,
                "talktime": pack.talktime,
                "sms": pack.sms,
                "data": pack.data,
                "source": pack.source,
                "priority": pack.priority,
                "favourite_marked": pack.favourite_marked,
                "extra_charge": pack.extra_charge,
                "selected_favourite": pack.selected_favourite,
                "constants": []
            })

        return JsonResponse({"similar_packs": result}, safe=False, status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#  favourite plans by operator
class FavouritePlansByOperatorAPIView(APIView):
    def get(self, request):
        # operator_name = request.data.get('operator_name', None)
        
        # connection_mode = request.data.get('connection_mode', None)
        operator_name = request.query_params.get('operator_name', None)
        connection_mode = request.query_params.get('connection_mode', None)

        if not operator_name:
            return Response({
                "message": "operator_name parameter is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        if connection_mode:
            connection_mode = connection_mode.capitalize()
            if connection_mode not in ['Prepaid', 'Postpaid']:
                return Response({
                    "message": f"Invalid connection_mode '{connection_mode}'. Allowed values are: Prepaid, Postpaid"
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "connection_mode parameter is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Strict filtering: both must match
        frc_plans = IndiaFRCSimPack.objects.filter(
            favourite_marked=True,
            is_active=True,
            operator__operator_name__iexact=operator_name,
            connection=connection_mode
        )

        # If no plans found, return success message
        if not frc_plans.exists():
            return Response({
                "message": f"No favourite plans found for operator '{operator_name}' with connection mode '{connection_mode}'.",
                "selected_sim_packages_all": []
            }, status=status.HTTP_200_OK)

        serializer = IndiaFRCSimPackSerializer(frc_plans, many=True, context={'request': request})
        return Response({
            "message": f"Favourite FRC plans for operator '{operator_name}' with connection mode '{connection_mode}' retrieved successfully",
            "selected_sim_packages_all": serializer.data
        }, status=status.HTTP_200_OK)


# To filter using operator_code instead of name

class FavouritePlansByOperatorOnlyAPIView(APIView):
    def get(self, request):
        operator_name = request.query_params.get('operator_name', None)

        if not operator_name:
            return Response({
                "message": "operator_name parameter is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        frc_plans = IndiaFRCSimPack.objects.filter(
            favourite_marked=True,
            is_active=True,
            operator__operator_name__iexact=operator_name
        )

        if not frc_plans.exists():
            return Response({
                "message": f"No favourite plans found for operator '{operator_name}'.",
                "selected_sim_packages_all": []
            }, status=status.HTTP_200_OK)

        serializer = IndiaFRCSimPackSerializer(frc_plans, many=True, context={'request': request})
        return Response({
            "message": f"Favourite FRC plans for operator '{operator_name}' retrieved successfully",
            "selected_sim_packages_all": serializer.data
        }, status=status.HTTP_200_OK)
