from .models import *
from delivery.models import *
from datetime import datetime as date_
from pytz import timezone as time_
from payment.models import CCavenue_creds
import requests , time as t_, hashlib, json, random
from webpages.views.bill_desk import encrypt_and_sign_jws_with_hmac, verify_and_decrypt_jws_with_hmac
from .models import  PaymentRequest
from bills.models import Biller_api_response
from wallet.models import Wallet

def open_bill_desk(request,txn_id):
    print("customer_payment working collet amount 11111111111")
    #wallet_data = PaymentRequest.objects.get(user = request.user, txn_id = txn_id)
    ind_time = date_.now(time_("Asia/Kolkata")).strftime('%Y%m%d%H%M%S')

    # wallet_history = DeliveryBoyWalletHistory.objects.filter(username = user_)
    client_id = CCavenue_creds.objects.get(key_name = 'CLIENT_ID_LIVE').value
    merch_id = CCavenue_creds.objects.get(key_name = 'MID_LIVE').value
    check_sum_key = CCavenue_creds.objects.get(key_name = 'CHECKSUM_KEY').value
    test_url = CCavenue_creds.objects.get(key_name = 'BILL_DESK_PRODUCTION_URL').value
    my_ip = requests.get('http://ifconfig.me/ip').text.strip()
    random_number = random.randint(0, 30)
    hash_object = hashlib.sha256(str(random_number).encode())
    hashed_number = hash_object.hexdigest()
    txnid = hashed_number[0:30] + str(round(t_.time() * 1000))
    traceid = str(uuid.uuid4())[:6]
    traceid = ind_time+traceid        

    try:
        
        pay_request = PaymentRequest.objects.filter(user = request.user, txn_id = txn_id)
        print("pay_request111",pay_request)
        if pay_request.exists():
            pay_request = pay_request[0]
            
        else:
            pay_request = PaymentRequest.objects.get_or_create(txn_id = txn_id)[0]
            pay_request.user = user_
            pay_request.created_at = datetime_.now()
            print('xyz', pay_request.user)
            #print('mobile', pay_request.mobile_number)
            pay_request.txn_id = txn_id
            pay_request.save()
            #print('amount',pay_request.payable_amount)

        pay_request.was_success=False
        pay_request.txn_id=pay_request.main_order.txn_id
        print(pay_request.txn_id, "pay_request.txn_id")
        if pay_request.main_order:
            # if int(float(pay_request.main_order.ord_id.discount_coupon_amount)) > 0:
            #     origin_payment = float(pay_request.main_order.ord_id.product_amount) - float(pay_request.main_order.ord_id.discount_coupon_amount)
            # else:
            #     origin_payment = pay_request.main_order.ord_id.product_amount
            if isinstance(pay_request.main_order.ord_id.discount_coupon_amount, (int, float, str)):
                print('isinstance')

                # Ensure conversion to float safely
                discount_amount = float(pay_request.main_order.ord_id.discount_coupon_amount)

                if discount_amount > 0:
                    print('float value', pay_request.main_order.ord_id.discount_coupon_amount)
                    origin_payment = float(pay_request.main_order.ord_id.product_amount) - discount_amount
                else:
                    print('instance else block')
                    origin_payment = float(pay_request.main_order.ord_id.product_amount)
            else:
                origin_payment = float(pay_request.main_order.ord_id.product_amount)
                print('outside instance if')

            # origin_payment = pay_request.main_order.ord_id.product_amount
            print("origin_payment",origin_payment)
            if pay_request.main_order.ord_id.partial_paid:
                print("parti paid",pay_request.main_order.ord_id.partial_paid)
                print("is_parti_paid",pay_request.main_order.ord_id.is_partia_paid)
                if pay_request.main_order.ord_id.is_partia_paid == True:
                    origin_payment = float(pay_request.main_order.ord_id.payable_cod_amount)
                else:
                    # origin_payment = float(pay_request.main_order.ord_id.product_amount) - float(pay_request.main_order.ord_id.payable_partial_amount)
                    origin_payment=float(pay_request.main_order.ord_id.product_amount) - float(pay_request.main_order.ord_id.payable_cod_amount)
                # origin_payment = float(pay_request.main_order.ord_id.product_amount)
                print("origin_payment",origin_payment)
        try:
            user_wallet = Wallet.objects.get(user=request.user)
            print("user_wallet.wallet_amount111",user_wallet.wallet_amount)
            if user_wallet.wallet_amount < float(origin_payment):
                origin_payment = float(origin_payment) - user_wallet.wallet_amount
                print("origin_payment111",origin_payment)
        except Exception as e:
            origin_payment = str(float(origin_payment) - user_wallet.wallet_amount)
            print("origin_payment222",origin_payment)
        #print(pay_request.is_paid)
        #print(pay_request.is_active)
        pay_request.save()
        #print("save")
        if pay_request:

            try:        
                now = datetime_.utcnow()
                iso_date = now.strftime('%Y-%m-%dT%H:%M:%S')+ str('+05:30')
                user_agent = request.META.get('HTTP_USER_AGENT')
                print(traceid)
                domain = request.get_host()
                # #print(domain)
                pre_protocol = 'https://'
                if domain == '127.0.0.1:8000':
                    pre_protocol = 'http://'
                headers={
                        "content-type": "application/jose",
                        "client_id":client_id,
                        "bd-timestamp": ind_time,
                        "accept": "application/jose",
                        "bd-traceid": traceid
                        }
                
                payload = {
                    "mercid":merch_id,
                    "orderid":str(pay_request.main_order.ord_id.id)+traceid,
                    "amount":str(origin_payment),
                    "order_date":iso_date,
                    "currency":"356",
                    # "ru":"https://prune.co.in/api/delivery/verify-payment",
                    "ru":f"{pre_protocol}{domain}/bill_desk/resp/",
                    "additional_info":{
                    "additional_info1": str(pay_request.main_order.ord_id.mobile_number)
                    },
                    "itemcode":"DIRECT",
                    "device":{
                        "init_channel":"internet",
                        "ip":my_ip,
                        "user_agent": user_agent,
                        }

                }
                bill_order = pay_request.main_order
                if bill_order:
                    if bill_order.req_log:
                        domain = request.get_host()
                        url = f"https://{domain}/api/payment/custom-api?order_id={bill_order.id}"
                        print('request-url',url)
                        v = requests.get(url)
                        print('vvvvvvvvv',v)
                    if not bill_order.was_success:
                        bill_order.req_log = payload
                        bill_order.save()
                print(payload,"---------------------------")
                encoded = encrypt_and_sign_jws_with_hmac(json.dumps(payload),check_sum_key, client_id)
                pay_request.registered_for = encoded
                pay_request.trace_id = traceid +","+ind_time
                pay_request.save()
                print("test url", test_url)
                
                response = requests.post(test_url,  data=encoded, headers=headers)

                data_ = verify_and_decrypt_jws_with_hmac(response.text,check_sum_key)
                dict_data= json.loads(data_)
                print('dictttttttttt',dict_data)
                if response.status_code == requests.codes.ok:

                    print(type(dict_data), dict_data)
                    redirect_url=dict_data['links'][1]['href']
                    print(redirect_url, " redirect_url")
                    
                    print("redirect_url------------------------------------", redirect_url)
                    
                    pay_request.merch_id =  merch_id # type: ignore
                    pay_request.bd_order_id =  dict_data['links'][1]['parameters']['bdorderid']
                    pay_request.authOtoken =  dict_data['links'][1]['headers']['authorization']
                    pay_request.save()
                    return [merch_id,pay_request.bd_order_id,pay_request.authOtoken]
                    
                else:
                    print(dict_data,"---------------------")
                    Biller_api_response.objects.create(biller_id = "consumer_payment link",api_data = dict_data)
                    return []

            except Exception as e:
                print(e)
                print("errorrrrrrrrrrrrrrr")
                Biller_api_response.objects.create(biller_id = "consumer_payment link",api_data = str(e))
                return []
    except Exception as e:
        print(e)
        print("ttttttttttttttttt")
        Biller_api_response.objects.create(biller_id = "consumer_payment link",api_data = str(e))
        return []
    else:
        print("uruuuuuuuuu")
        Biller_api_response.objects.create(biller_id = "consumer_payment link",api_data = "Parameter Missing , delivery_payment")
        return []
