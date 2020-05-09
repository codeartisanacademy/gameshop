from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
import datetime

from .models import Product, ProductImage

def count_total_items(request):
    return len(request.session['cart'])

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
        if 'cart' in self.request.session:
            context["cart"] =count_total_items(self.request)
            print(self.request.session['cart'])
        return context
    
    def post(self, request):
        id = request.POST.get("product")
        print(id)

class AddedToCartView(TemplateView):
    template_name="cart/added.html"
    id = None

    def get(self, request, id):
        cart_products = None
        if "cart" in request.session:
            cart_products = request.session['cart']
            # [{'id':1, 'quantity':2}, {'id':3, 'quantity':5}]
            cart_products.append({'id':id, 'quantity':1})
            
            request.session['cart'] = cart_products
        else:
            request.session['cart'] = []
            cart_products = request.session['cart']
            
        return render(request, self.template_name, {'product':len(cart_products)})


class ShoppingCartView(TemplateView):
    template_name = 'cart/cart.html'

    def get(self, request):
        products = []
        if 'cart' in request.session:
            items_in_cart = request.session['cart']
            for item in items_in_cart:
                products.append(Product.objects.get(id=item['id']))

        return render(request, self.template_name, {'products_in_cart':products})       

