from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import HttpResponseRedirect, reverse
from django.contrib import messages

import datetime

from .models import Product, ProductImage

def count_total_items(request):
    total_items = 0
    if 'cart' in request.session:
        total_items = len(request.session['cart'])
    return total_items

class ProductsView(ListView):
    # this is a must in ListView, it tells what model you want to use
    model = Product
    template_name = 'products/product_list.html'
    ordering = ['name']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = count_total_items(self.request)

        return context
        
    # contect_object_name
    # queryset = Product.objects.filter(name__contains='playstation')

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    
    def get_context_data(self, **kwargs):
        # this is a must
        context = super().get_context_data(**kwargs)
        self.request.session["session_last_visit"] = datetime.datetime.now().__str__()
        # your extra context
        context["related_products"] = Product.objects.filter(name__contains='playstation')
        context["last_visit"] = self.request.session['session_last_visit']
        context["cart"] = count_total_items(self.request)

        return context
    
    def post(self, request):
        id = request.POST.get("product")
        print(id)

class AddedToCartView(TemplateView):
    template_name="cart/added.html"
    id = None

    def get(self, request, id):
        cart_products = None
        try:
            if "cart" in request.session:
                cart_products = request.session['cart']
                # [{'id':1, 'quantity':2}, {'id':3, 'quantity':5}]
                cart_products.append({'id':id, 'quantity':1})
                request.session['cart'] = cart_products
            else:
                cart_products = []
                cart_products.append({'id':id, 'quantity':1})
                request.session['cart'] = cart_products
            
            messages.success(request, "Product successfully added to cart")
            return HttpResponseRedirect(reverse('cart'))

        except Exception as error:
            messages.error(request, error )
            return HttpResponseRedirect(reverse('products-detail', kwargs={'pk':id}))
        


class ShoppingCartView(TemplateView):
    template_name = 'cart/cart.html'

    def get(self, request):
        
        products = []
        if 'cart' in request.session:
            print(request.session['cart'])
            items_in_cart = request.session['cart']
            for item in items_in_cart:
                products.append(Product.objects.get(id=item['id']))
        
        return render(request, self.template_name, {'products_in_cart':products, 'cart':count_total_items(request)})       


class RemoveProductFromCartView(TemplateView):
    template_name = 'cart/remove.html'
    id = None

    def get(self, request, id):
        # get the list from the session store it in a local variable
        products_in_cart = []
        products_in_cart = request.session['cart']

        # remove the disctionary from the list
        del products_in_cart[id]

        # reassign the session cart with the new list
        request.session['cart'] = products_in_cart

        return render(request, self.template_name, {'cart': count_total_items(request)})



class CheckoutView(TemplateView):
    template_name="cart/checkout.html"

    def get(self, request):
        return render(request, self.template_name)