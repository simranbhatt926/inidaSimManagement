
import requests
from indiaSimManagement.serializers import FRCSimPackNewSerializer
from .models import IndiaFRCSimPack
    
class SimPlanService:

    @classmethod
    def get_plan_by_mode(cls,mode):
        try:
            queryset = IndiaFRCSimPack.objects.filter(
                is_active=True)
            if mode:
                mode = mode.capitalize()
                queryset = queryset.filter(connection=mode)
            
            queryset = queryset.order_by('amount__pack_amount', 'priority')
            print(queryset,'queryset')

            return cls._format_plans_response(queryset)
        except Exception as e:
            print(f"Error in get_operator_plans: {str(e)}")
            return {"selected_sim_packages_all": []}
    
    @classmethod
    def get_operator_plans(cls, operator, mode):
        """Get plans for specific operator in specific city"""
        print('kdkkdkkddk')
        try:
            queryset = IndiaFRCSimPack.objects.filter(
                is_active=True,
                operator__operator_name__iexact=operator,
            )
           
            
            if mode:
                mode = mode.capitalize()
                queryset = queryset.filter(connection=mode)
                
            queryset = queryset.order_by('amount__pack_amount', 'priority')
            return cls._format_plans_response(queryset)
            
        except Exception as e:
            print(f"Error in get_operator_plans: {str(e)}")
            return {"selected_sim_packages_all": []}
    
    @classmethod
    def get_mode_plans(cls,mode):
        try:
            queryset = IndiaFRCSimPack.objects.filter(
                is_active = True,
                mode=mode,
            )
        except:
            pass

    @classmethod
    def get_operator_state_plans(cls, operator, mode, state_id,city_id):
        """Get plans for specific operator in specific state"""
        try:
            queryset = IndiaFRCSimPack.objects.filter(
                is_active=True,
                operator__operator_name__iexact=operator,
                cities__id = city_id,
                states__id=state_id
            )
            
            if mode:
                mode = mode.capitalize()
                queryset = queryset.filter(connection=mode)
                
            queryset = queryset.order_by('amount__pack_amount', 'priority')
            return cls._format_plans_response(queryset)
            
        except Exception as e:
            print(f"Error in get_operator_state_plans: {str(e)}")
            return {"selected_sim_packages_all": []}

    @classmethod
    def get_state_city_plans(cls,mode, operator,state_obj,circle_id):
        """Get all plans for specific state"""
        try:
            queryset = IndiaFRCSimPack.objects.filter(
                is_active=True,
                states__id=state_obj,                
                cities__id = circle_id,
                operator__operator_name__iexact=operator,
            )
            if mode:
                mode = mode.capitalize()
                queryset = queryset.filter(connection=mode)
                
            queryset = queryset.order_by('amount__pack_amount', 'priority')
            return cls._format_plans_response(queryset)
            
        except Exception as e:
            print(f"Error in get_state_plans: {str(e)}")
            return {"selected_sim_packages_all": []}

    @classmethod
    def get_city_plans(cls, mode, city_id, state_id):
        """Get all plans for specific city"""
        try:
            queryset = IndiaFRCSimPack.objects.filter(
                is_active=True,
                cities__id=city_id,
                states__id=state_id
            )
            
            if mode:
                mode = mode.capitalize()
                queryset = queryset.filter(connection=mode)
                
            queryset = queryset.order_by('amount__pack_amount', 'priority')
            return cls._format_plans_response(queryset)
            
        except Exception as e:
            print(f"Error in get_city_plans: {str(e)}")
            return {"selected_sim_packages_all": []}

    @classmethod
    def _format_plans_response(cls, queryset):
        """Helper method to format plans response consistently"""
        response_data = {
            "selected_sim_packages_all": []
        }
        
        if not queryset:
            return response_data
            
        for plan in queryset:
            print('jjdjdjdjyyyy')
            # Format operator data
            operator_image = ""
            if plan.operator and plan.operator.operator_image:
                try:
                    operator_image = plan.operator.operator_image.url
                except Exception as e:
                    print(f"Error processing operator image: {str(e)}")
                    operator_image = ""

            operator_data = {
                "operator_name": plan.operator.operator_name if plan.operator else "",
                "operator_code": plan.operator.operator_code if plan.operator else "",
                "operator_image": operator_image
            }

            # Format validity
            validity_str = ""
            if plan.validity:
                validity_days = getattr(plan.validity, 'pack_validity', 0)
                validity_str = f"{validity_days} Days" if validity_days != 1 else f"{validity_days} Day"

            # Format amount safely
            try:
                amount_value = float(getattr(getattr(plan, 'amount', None), 'pack_amount', 0))
                amount_str = f"{amount_value:.1f}"
            except (TypeError, ValueError, AttributeError):
                amount_str = "0.0"

            plan_data = {
                "id": plan.pk,
                "operator": operator_data,
                "circle": ", ".join([city.city for city in plan.cities.all()]) if plan.cities.exists() else "",
                "validity": validity_str,
                "amount": amount_str,
                "connection": plan.connection,
                "plan_description": plan.plan_description,
                "plan_benefits": plan.plan_benefits,
                "india_sim_url": plan.india_sim_url,
                "talktime": plan.talktime,
                "sms": plan.sms,
                "data": plan.data,
                "source": plan.source if plan.source else None,
                "priority": plan.priority,
                "favourite_marked": bool(plan.favourite_marked),
                "extra_charge": plan.extra_charge if plan.extra_charge else "0",
                "selected_favourite": bool(plan.selected_favourite),
                "constants": [
                        {
                            "key": constant.key,
                            "value": constant.value
                        } for constant in plan.constants.all()
                    ]
            }

            response_data["selected_sim_packages_all"].append(plan_data)
        
        return response_data
    



class SimPortService:
    VALID_OPERATORS = {"vi", "bsnl", "jio", "airtel"}
    CURRENT_LOCATION_LOGO = "current_location_logo"

    @classmethod
    def get_sim_data(cls, mode, operator=None, circle="Delhi"):
        
        try:
    
            if operator and operator not in cls.VALID_OPERATORS:
                return None, {"error": "Invalid operator."}, 400

            mode = mode.capitalize()
            circle_data = list(Circle.objects.values_list('circle', flat=True).filter(is_active_to_buy=True))
            try:
                circle_id = Circle.objects.get(circle=circle)
            except:
                return f"cicle does not exists"

            queryset = IndiaFRCSimPack.objects.filter(
                connection=mode,
                circle__id=circle_id.id,
                is_active=True
            )

            if operator:
                queryset = queryset.filter(operator__operator_name__icontains=operator)

            queryset = queryset.order_by('amount__pack_amount', 'priority')

            if not queryset.exists():
                return None, {"message": "Plan not found"}, 404

            serializer = FRCSimPackNewSerializer(queryset, many=True)
            operator_plans = serializer.data


            context = {
                'port': 'Yes',
                'circle_data': circle_data,
                'scroll': False,
                'mode': mode,
                'operator': operator,
                "non_delivery": "Please Enter A Valid Pincode (Delhi NCR region only)",
                'current_location_logo': cls.CURRENT_LOCATION_LOGO,
                'simpacks': operator_plans,
            }

            return context, None, None

        except Exception as e:
            return None, {"error": f"An unexpected error occurred: {str(e)}"}, 500