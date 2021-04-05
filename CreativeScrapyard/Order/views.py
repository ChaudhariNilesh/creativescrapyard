from django.contrib.auth import login
from django.core.mail import message
from django.http.response import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from CreativeScrapyard import settings
from Authentication.models import Address
from Cart.models import Cart
from Items.models import tbl_creativeitems_mst
from django.http import HttpResponseNotFound
from Home.views import creativeCategories,scrapCategories
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
# Create your views here.
@login_required
def checkout(request,action=None):
    template="Order/checkout.html"
    
    defaultAddress = Address.objects.get(user_id=request.user.user_id,is_default=True)
    addressList = Address.objects.filter(user_id=request.user.user_id)
    context={}
    cartitems=""
    crtItem=""
    shipping=0.00
    total = 0.0

    
    if action == "buy-now":
        if "product" in request.session and request.method == "GET":
            # print("hai")
            pid=request.session.get("product")
            qty=request.session.get("qty")
            itemObj=get_object_or_404(tbl_creativeitems_mst,crt_item_id=pid)

            crtItem=tbl_creativeitems_mst.objects.filter(crt_item_id=itemObj.crt_item_id)
            
        else:
            # print(request.POST)
            pid = request.POST.get("crt_item_id",None)
            qty = request.POST.get("crt_item_qty",None)
            
            itemObj=get_object_or_404(tbl_creativeitems_mst,crt_item_id=pid)
            if not (itemObj.user==request.user):
                # print("SAME USER")
                crtItem=tbl_creativeitems_mst.objects.filter(crt_item_id=itemObj.crt_item_id)
                
                request.session['product']=pid
                request.session['qty']=qty
                request.session['is_cartItem']=False
                
                total = itemObj.crt_item_price * int(qty)
                
                orderTotalAmt=shipping+float(total)
                context={
                    'is_creative':True,
                    'categories':creativeCategories(),
                    'defaultAddress':defaultAddress,
                    'addressList':addressList,
                    'total':total,
                    'shippingRate':shipping,
                    'orderTotalAmt':orderTotalAmt,
                    'crtItem':crtItem,
                }
            else:
                next = request.POST.get('next', '/')
                messages.warning(request, 'Ohh! Are you trying to buy your own item. We dont do that here.')
                return redirect(next)
            

    elif request.method == "POST" and action=="change-address" :
        addrsId = request.POST.get("addressRadio","")
        defaultAddress = Address.objects.get(user_id=request.user.user_id,is_default=True)
        defaultAddress.is_default=False
        defaultAddress.save()

        newDefAddress = Address.objects.get(address_id=addrsId)
        newDefAddress.is_default=True
        newDefAddress.save()

        # return redirect("Home:Items:Order:checkout")

    elif action == "cart" :
        cartitems = Cart.objects.filter(user_id=request.user.user_id)
        if cartitems:
            
            request.session['product']=list(cartitems.values())
            request.session['is_cartItem']=True
            # print(request.session.get("is_cartItem"))

            total = 0
            for item in cartitems:
                total += item.crt_item.crt_item_price * item.crt_item_qty
            orderTotalAmt=shipping+float(total)
            context={
                'is_creative':True,
                'defaultAddress':defaultAddress,
                'addressList':addressList,
                'cartitems':cartitems,
                'total':total,
                'shippingRate':shipping,
                'orderTotalAmt':orderTotalAmt,
                'crtItem':crtItem,
                'is_cartItem':True,
                'categories':creativeCategories(),
        }
        
        else:
            next = request.POST.get('next', '/')
            return redirect(next)
            
    else:
        return HttpResponseNotFound("404 Page not found.")

    return render(request,template,context)


@login_required
def orderHistory(request):
    template="Order/order-history.html"
    return render(request,template,{'is_creative':True})

@login_required
def orderTrack(request):
    template="Order/order-track.html"
    return render(request,template,{'is_creative':True})

@login_required
def orderCancel(request,id=None):
    if request.is_ajax() and id is not None:
        try:
            ord = tbl_orders_details.objects.get(order_details_id=id)
            ord.item_status = 3
            ord.save()
            
            crt=tbl_creativeitems_mst.objects.get(crt_item_id=ord.crt_item_mst.crt_item_id)
            qty=crt.crt_item_qty
            qty+=ord.crt_item_qty
            crt.crt_item_qty=qty
            if  crt.crt_item_status=="SOLD":
                crt.crt_item_status="ACTIVE"
                crt.save()
            
            st = orderMail("cancelOrder",ord)
            # print(st)
        except Exception as e:
            print(e)
            return JsonResponse({"status":False})
        else:
            return JsonResponse({"status":True})
    

@login_required
def orderReturn(request,id=None):
    if request.is_ajax() and id is not None:
        try:
            ord = tbl_orders_details.objects.get(order_details_id=id)
            ord.item_status = 5
            ord.save()
            
            crt=tbl_creativeitems_mst.objects.get(crt_item_id=ord.crt_item_mst.crt_item_id)
            qty=crt.crt_item_qty
            qty+=ord.crt_item_qty
            crt.crt_item_qty=qty
            if  crt.crt_item_status=="SOLD":
                crt.crt_item_status="ACTIVE"
                crt.save()
            
            orderMail("returnOrder",ord)
        except Exception as e:
            print(e)
            return JsonResponse({"status":False})
        else:
            return JsonResponse({"status":True})

def orderMail(typeFor,orderDet):
    
    if typeFor == "cancelOrder":
        emailmessage="Your order has been cancelled successfully."
        emailmessage+="\n\nThank You."
        try:

            mail_subject = "Order Cancelled"
            message = render_to_string('Order/order-mail.html', {
                'message':str("\n")+emailmessage,
                'user':User.objects.get(user_id=orderDet.order.user.user_id),
                'type':"cancelOrder",
            })


            to_email = orderDet.order.user.email
            email = EmailMessage(
                        mail_subject, message, to=[to_email,]
            )
            email.send()

        except Exception as e:
            
            print("MAIL EXCEPTION : "+str(e))
            return False     
        else:
            return True

    elif typeFor == "returnOrder":
        emailmessage="Your order has been returned successfully."
        emailmessage+="\n\nThank You."
        try:

            mail_subject = "Order Returned"
            message = render_to_string('Order/order-mail.html', {
                'message':str("\n")+emailmessage,
                'user':User.objects.get(user_id=orderDet.order.user.user_id),
                'type':"returnOrder",
            })


            to_email = orderDet.order.user.email
            email = EmailMessage(
                        mail_subject, message, to=[to_email,]
            )
            email.send()

        except Exception as e:
            
            print("MAIL EXCEPTION : "+str(e))
            return False     
        else:
            return True