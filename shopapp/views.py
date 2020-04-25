from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
import datetime

from .models import Product, ProductImage

class ProductsView(ListView):
    # this is a must in ListView, it tells what model you want to use
    model = Product
    template_name = 'products/product_list.html'
    ordering = ['name']
    
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
        context["cart"] = self.request.session['cart']
        return context
    
    def post(self, request):
        id = request.POST.get("product")
        print(id)

class AddedToCartView(TemplateView):
    template_name="cart/added.html"
    id = None

    def get(self, request, id):
        request.session['cart'] = id
        return render(request, self.template_name, {'product':request.session['cart']})








# Create your views here.
"""class ProductsView(ListView):
    model = Product
    template_name = 'products/product_list.html'


class ProductDetail(DetailView):
    model = Product
    template_name = ''"""