from django.core.exceptions import PermissionDenied
from django.http.response import JsonResponse
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from .models import Transaction,Payment
from Cart.models import Cart
from Order.models import tbl_orders_mst,tbl_orders_details
from Items.models import tbl_creativeitems_mst
from Authentication.models import Address,User

from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from Home.views import creativeCategories

def initiate_payment(request):
    
    if request.method == "POST":
        try:
            payOn = request.POST['pay_mtd']
            # print(request.session.get("is_cartItem"))
            if not request.session.get("is_cartItem"):
                
                pid=request.session.get("product")
                qty=request.session.get("qty")
                itemObj=get_object_or_404(tbl_creativeitems_mst,crt_item_id=pid)
                crtItem=tbl_creativeitems_mst.objects.filter(crt_item_id=itemObj.crt_item_id)
                # print(crtItem)
                
                Addrs=Address.objects.get(user_id=request.user.user_id,is_default=True)
                person_name=Addrs.person_name
                contact_no=Addrs.contact_no
                delivery_address=Addrs.line1+"\n"+\
                    Addrs.line2+"\n"+\
                    Addrs.landmark+"\n"+\
                    str(Addrs.city)+","+\
                    str(Addrs.state)+"\n"+\
                    Addrs.pincode

                amt = float(itemObj.crt_item_price)*float(qty)
                    

                # print(product,p_ids,amt)
                orderMst=tbl_orders_mst(person_name=person_name,contact_no=contact_no,\
                        delivery_address=delivery_address,total_amt=amt,\
                        delivery_status=1,user=request.user)
                
                orderMst.save()

                
                Addrs=Address.objects.get(user_id=itemObj.user_id,is_default=True)
                person_name=Addrs.person_name
                contact_no=Addrs.contact_no
                    
                pickup_address=Addrs.line1+"\n"+\
                    Addrs.line2+"\n"+\
                    Addrs.landmark+"\n"+\
                    str(Addrs.city)+","+\
                    str(Addrs.state)+"\n"+\
                    Addrs.pincode
            
                tbl_orders_details.objects.create(crt_item_qty=qty,unit_price=itemObj.crt_item_price,\
                    pickup_address=pickup_address,item_status=1,order=orderMst,crt_item_mst=itemObj)       
                
                if payOn=="1": #POD
                    # print("POD")
                    orderMst.order_status=True
                    orderMst.save()
                    orderDetails = tbl_orders_details.objects.filter(order=orderMst)
                    totUserItemPrice = 0
                    for d in orderDetails:
                        totUserItemPrice += d.updateQty()
                        
                    del request.session['is_cartItem']
                    del request.session['product']
                    del request.session['qty']
                
                    orderMail("placeOrder",orderMst)
                    
                    messages.success(request, 'Order placed successfully.')
                    return redirect('Authentication:order_history')                
                
                elif payOn == "2":  #paytm
                    
                    merchant_key = settings.PAYTM_SECRET_KEY

                    params = (
                        ('MID', settings.PAYTM_MERCHANT_ID),
                        ('ORDER_ID', str(orderMst.order_id)),
                        ('CUST_ID', str(request.user.email)),
                        ('TXN_AMOUNT', str(amt)),
                        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
                        ('WEBSITE', settings.PAYTM_WEBSITE),
                        # ('EMAIL', request.user.email),
                        # ('MOBILE_N0', '9911223388'),
                        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
                        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
                        # ('PAYMENT_MODE_ONLY', 'NO'),
                    )

                    paytm_params = dict(params)
                    checksum = generate_checksum(paytm_params, merchant_key)
                    paytm_params['CHECKSUMHASH'] = checksum

                    return render(request, 'payments/redirect.html', context=paytm_params) 
            
            else:
                product = ""
                amt = 0
                cart_ids = ""
                p_ids = ""
                
                cartitems = Cart.objects.filter(user_id=request.user.user_id)

                if cartitems:
                    Addrs=Address.objects.get(user_id=request.user.user_id,is_default=True)
                    person_name=Addrs.person_name
                    contact_no=Addrs.contact_no
                    delivery_address=Addrs.line1+"\n"+\
                        Addrs.line2+"\n"+\
                        Addrs.landmark+"\n"+\
                        str(Addrs.city)+","+\
                        str(Addrs.state)+"\n"+\
                        Addrs.pincode
                    
                    for i in cartitems:
                        # product += str(i.crt_item.crt_item_name)+"\n"
                        # p_ids += str(i.crt_item.crt_item_id)+","
                        amt += float(i.crt_item.crt_item_price)*i.crt_item_qty
                        

                    # print(product,p_ids,amt)
                    orderMst=tbl_orders_mst(person_name=person_name,contact_no=contact_no,\
                            delivery_address=delivery_address,total_amt=amt,\
                            delivery_status=1,user=request.user)
                    
                    orderMst.save()

                    for i in cartitems:
                        Addrs=Address.objects.get(user_id=i.crt_item.user_id,is_default=True)
                        crtItemObj=tbl_creativeitems_mst.objects.get(crt_item_id=i.crt_item.crt_item_id)
                        person_name=Addrs.person_name
                        contact_no=Addrs.contact_no
                        
                        pickup_address=Addrs.line1+"\n"+\
                            Addrs.line2+"\n"+\
                            Addrs.landmark+"\n"+\
                            str(Addrs.city)+","+\
                            str(Addrs.state)+"\n"+\
                            Addrs.pincode
                    
                        tbl_orders_details.objects.create(crt_item_qty=i.crt_item_qty,unit_price=i.crt_item.crt_item_price,\
                            pickup_address=pickup_address,item_status=1,order=orderMst,crt_item_mst=crtItemObj)       
                    
                    if payOn=="1": #POD
                        # print("POD")
                        orderMst.order_status=True
                        orderMst.save()

                        orderDetails = tbl_orders_details.objects.filter(order=orderMst)
                        totUserItemPrice = 0
                        for d in orderDetails:
                            totUserItemPrice += d.updateQty()

                        cartitems = Cart.objects.filter(user_id=request.user.user_id)
                        cartitems.delete()
                        
                        del request.session['is_cartItem']
                        del request.session['product']
                        

                        status=orderMail("placeOrder",orderMst)
                        # print(status)
                        messages.success(request, 'Order placed successfully.')
                        return redirect('Authentication:order_history')                
                    elif payOn == "2":  #paytm
                        # print("paytm")
                    
                        merchant_key = settings.PAYTM_SECRET_KEY

                        params = (
                            ('MID', settings.PAYTM_MERCHANT_ID),
                            ('ORDER_ID', str(orderMst.order_id)),
                            ('CUST_ID', str(request.user.email)),
                            ('TXN_AMOUNT', str(amt)),
                            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
                            ('WEBSITE', settings.PAYTM_WEBSITE),
                            # ('EMAIL', request.user.email),
                            # ('MOBILE_N0', '9911223388'),
                            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
                            ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
                            # ('PAYMENT_MODE_ONLY', 'NO'),
                        )

                        paytm_params = dict(params)
                        checksum = generate_checksum(paytm_params, merchant_key)

                        paytm_params['CHECKSUMHASH'] = checksum
                        # print('SENT: ', checksum)
                        #print(paytm_params)
                        # print(request.session.get("is_cartItem"))     



                        return render(request, 'payments/redirect.html', context=paytm_params) 
                               
                else:
                    return redirect("Home:Items:creativestore")

        except Exception as e:
            print(e)
            # print(request.POST.get('next', '/'))
            next = request.POST.get('next', '/')
            messages.error(request, 'Some error occured, Try again.'+str(e))
            return redirect(next)





@csrf_exempt
def callback(request):
    # context={}
    # context['categories']=creativeCategories()
    # print(creativeCategories())
    if request.method == 'POST':
        
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
            received_data['is_creative'] = True
            received_data['categories'] = creativeCategories()
            # print(received_data)
            payed_order_id=int(*received_data['ORDERID'])
            txt_id = str(*received_data['TXNID'])
            pay_mode = str(*received_data['PAYMENTMODE'])
            pay_amt = float(*received_data['TXNAMOUNT'])
            payment_remark="Buyer's payment for the order."
            
            order=tbl_orders_mst.objects.get(order_id=payed_order_id)
            order.order_status=True
            order.save()

            orderDetails = tbl_orders_details.objects.filter(order=order)
            totUserItemPrice = 0
            for d in orderDetails:
                totUserItemPrice += d.updateQty()
                
            paymentObj=Payment(transaction_id=txt_id,payment_mode=pay_mode,payment_amt=pay_amt,payment_status=2,payment_remark=payment_remark,order=order)
            paymentObj.save()

            status=orderMail("placeOrder",order)
            # print(status)
            
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'payments/callback.html', context=received_data)
        return render(request, 'payments/callback.html', context=received_data)
    else:
        # return render(request, 'payments/callback.html', {"is_creative":True,"categories":creativeCategories()})
        raise PermissionDenied

def orderMail(typeFor,order):
    
    if typeFor == "placeOrder":
        emailmessage="Your order with Order ID : "+str(order.order_id)+" has been placed successfully."+"\nYour can check your order details at "\
            + "http://127.0.0.1:8000/accounts/dashboard/orders/history/"
        
        emailmessage+="\n\nThank You."
        try:

            mail_subject = "Order Placed Successfully."
            message = render_to_string('Order/order-mail.html', {
                'message':str("\n")+emailmessage,
                'user':User.objects.get(user_id=order.user_id),
                'type':"placeOrder",
            })


            to_email = order.user.email
            email = EmailMessage(
                        mail_subject, message, to=[to_email,]
            )
            email.send()

        except Exception as e:
            
            print("MAIL EXCEPTION : "+str(e))
            return False     
        else:
            return True
                
def clearSession(request):
    if request.is_ajax():

        #  print(request.session.get("is_cartItem"))
        # print(request.session.get("product"))
        cart=request.session.get("product")
        
        # print(cart[0]['user_id'])
        if request.session.get("is_cartItem"):
            cartitems = Cart.objects.filter(user_id=cart[0]['user_id'])
            cartitems.delete()
            del request.session['is_cartItem']
            del request.session['product']
            
        else:
            del request.session['is_cartItem']
            del request.session['product']
            del request.session['qty']  

        return JsonResponse({"status":True})
    else:
        raise PermissionDenied
# def initiate_payment(request):
#     if request.method == "GET":
#         return render(request, 'payments/pay.html')
#     try:
#         username = request.POST['username']
#         password = request.POST['password']
#         amount = int(request.POST['amount'])
#         user = authenticate(request, username=username, password=password)
#         if user is None:
#             raise ValueError
#         auth_login(request=request, user=user)
#     except:
#         return render(request, 'payments/pay.html', context={'error': 'Wrong Accound Details or amount'})

#     transaction = Transaction.objects.create(made_by=user, amount=amount)
#     transaction.save()
#     merchant_key = settings.PAYTM_SECRET_KEY

#     params = (
#         ('MID', settings.PAYTM_MERCHANT_ID),
#         ('ORDER_ID', str(transaction.order_id)),
#         ('CUST_ID', str(transaction.made_by.email)),
#         ('TXN_AMOUNT', str(transaction.amount)),
#         ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
#         ('WEBSITE', settings.PAYTM_WEBSITE),
#         # ('EMAIL', request.user.email),
#         # ('MOBILE_N0', '9911223388'),
#         ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
#         ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
#         # ('PAYMENT_MODE_ONLY', 'NO'),
#     )

#     paytm_params = dict(params)
#     checksum = generate_checksum(paytm_params, merchant_key)

#     transaction.checksum = checksum
#     transaction.save()

#     paytm_params['CHECKSUMHASH'] = checksum
#     print('SENT: ', checksum)
    
#     return render(request, 'payments/redirect.html', context=paytm_params)