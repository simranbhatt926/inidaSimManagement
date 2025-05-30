from payment.models import PaymentRequest, BillerDeskPaymentInitiate
import requests, json
from django.http import JsonResponse, HttpResponse

def indian_payment_check_status(request):
    print('script runiing indian sim payment..')
    print('ordrrrrrrrrr',request.GET.get('order_id'))
    main_order = BillerDeskPaymentInitiate.objects.get(id = request.GET.get('order_id'))
    payment = PaymentRequest.objects.filter(was_success = False, main_order = main_order)
    if payment.exists():
        payment = payment.first()
    else:
        payment = PaymentRequest.objects.get_or_create(was_success = False, main_order = main_order)
        
    bill_order = main_order
    print('main orderrrrrr',main_order)
    print('main bill_order', bill_order)
    try:
        if bill_order:
            print('billerrrid',bill_order.id)
            order_id = bill_order.id
            pay_load = {
                "order_id" : order_id
            }
            # domain = 'prune.co.in'
            # test_domain = 'sharingenv.prune.co.in'
            domain = request.get_host()
            print('domain......',domain)
            url = f"https://{domain}/api/payment/status-check/"
            
            header = {
                "Authorization" : "Token "+ bill_order.user.get_user_token()  #type:ignore
            }

            print('headerrrr',header)
            response = requests.get(url,data = pay_load, headers=header).json()
            bill_order.log = response
            bill_order.save()
            print(response, "mmmmmmmmmmmmmmmmmmm")
            print('status', request.GET.get('status'))
            print(',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,')
            if 'status' in response:
                if 'transaction_error_type' in response['status']:
                    if response['status']['transaction_error_type'] == 'success' and not bill_order.was_success:
                        print("transaction_error_type")
                        bill_order.was_success = True
                        prune_order = bill_order.ord_id
                        bill_order.save()
                        if prune_order:
                            print("i am in prune order")
                            payment.was_success = True
                            payment.save()
                            prune_order.payment_method = response['status']['payment_method_type']
                            prune_order.payment_status = 'Done'
                            prune_order.is_paid = True
                            prune_order.is_active = True
                            prune_order.save()
                            if str(prune_order.product_info["connection_mode"]).lower() == "prepaid" or prune_order.partial_paid:
                                print('------------kkkk--------------')
                                bill_order.user.add_balance(float(prune_order.payable_amount), "sim purchsed wallet recharge",bill_order = bill_order)
                            else:
                                print('---------------jjjjjjjjjjjjjjjjjj---------------------')
                                bill_order.user.add_balance(float(prune_order.payable_amount) - float(prune_order.conven_fee), "sim purchsed wallet recharge",bill_order = bill_order)
                                
                            if prune_order.partial_paid:
                                print('-----------ooooooooooooooo----------------------')
                                bill_order.user.deduct_balance(float(prune_order.payable_amount),  "Purchased new connection " + prune_order.product_info["operator"] + ' in ' + str(prune_order.mobile_number), "",bill_order = bill_order)
                            else:
                                print('-----------iiiiiiiiiii-----------------')
                                bill_order.user.deduct_balance(float(prune_order.product_amount),  "Purchased new connection " + prune_order.product_info["operator"] + ' in ' + str(prune_order.mobile_number), "",bill_order = bill_order)
                        
                        print(f'bill_order id - {bill_order.id} status check done')
                    else:
                        print(f'bill_order id - {bill_order.id} status check done payment failed in type is not success')
                        return HttpResponse({"message": "order is failed, type is not success"})
                else:
                    print(f'bill_order id - {bill_order.id} status check done payment failed, transaction_error_type')
                    print('---------.........')
                    return HttpResponse({"message": "order is failed, transaction_error_type"})
            else:
                print(f'bill_order id - {bill_order.id} status check done payment failed, status not in response')
                print('[[[.....]]]')
                return HttpResponse({"message": "order is failed, status not in response"})
        else:
            print(f'payment request id - {payment.id} does not have main order')
            print('....,,,,,,')
            return HttpResponse({"message": "order is not found"})
    except Exception as e:
        print("error indian sim - ",e)
