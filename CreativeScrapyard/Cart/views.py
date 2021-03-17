
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from Home.views import creativeCategories
from Items.models import tbl_creativeitems_mst,tbl_crtimages
from django.db.models import Count
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse


# Create your views here.

@login_required
def addToCart(request):
    template = 'Cart/cart.html'
    context={}
    context['is_creative']=True
    cartitems = Cart.objects.filter(user_id=request.user.user_id)

    context['cartitems'] = cartitems
    context['categories'] = creativeCategories()
    # prd = tbl_creativeitems_mst.objects.filter(cart__in=cartitems)
    # image = tbl_crtimages.objects.filter(crt_item_details_id__in=prd,is_primary=True)

    # context['image']=prd

    if request.user.is_authenticated:    
        if request.method == 'POST':
            
            pid = request.POST.get("crt_item_id",None)
            qty = request.POST.get("crt_item_qty",None)
            is_exist = Cart.objects.filter(crt_item_id=pid,user_id=request.user.user_id)
            

            if len(is_exist)>0:
                messages.error(request,'Item already exist in Cart')
            else:
                product = get_object_or_404(tbl_creativeitems_mst,crt_item_id=pid)
                
                if (product.user==request.user):
                    messages.warning(request, 'Ohh! Are you trying to buy your own item. We dont do that here.')
                    next = request.POST.get('next', '/')
                    return redirect(next)

                    

                user = get_object_or_404(User,user_id=request.user.user_id)
                cart = Cart(crt_item_qty=qty,crt_item=product,user=user)
                cart.save()
                messages.success(request,'{} Added in your Cart'.format(product.crt_item_name))
                return redirect("Home:Items:Cart:addToCart")

    return render(request,template,context)

def changeQty(request):
    if request.is_ajax() and request.method == "POST":
    
        cart_id = request.POST.get("cart_id",None)
        crt_item_qty = request.POST.get("cart_qty",None)

        cart_obj = get_object_or_404(Cart,cart_id=cart_id)
        cart_obj.crt_item_qty = crt_item_qty
        cart_obj.save()
        return JsonResponse({"changed":True})

    else:
        raise PermissionDenied

def removeCartItem(request):
    if request.is_ajax() and request.method == "POST":
    
        cart_id = request.POST.get("cart_id",None)
    
        cart_obj = get_object_or_404(Cart,cart_id=cart_id)
        cart_obj.delete()
        return JsonResponse({"changed":True})

    else:
        raise PermissionDenied


def getTotal(request):
    items = Cart.objects.filter(user_id=request.user.user_id)
    total,quantity = 0,0
    if items:
        for item in items:
            total += item.crt_item.crt_item_price * item.crt_item_qty
            quantity += item.crt_item_qty
        
        response = {'total':total,'quan':quantity}
    else:
        response = {}
    return JsonResponse(response) 

        