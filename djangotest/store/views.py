from django.shortcuts import render
from django.http import Http404
from .models import Store,Product

# Create your views here.
def productView(request,product_id):
    context = dict()
    try:
        context['product'] = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise Http404("Product does not exist.")
    return render(request=request,template_name='store/product.html',context=context)

def storeView(request,store_id):
    context = dict()
    try:
        context['store'] = Store.objects.get(pk=store_id)
        context['products'] = Product.objects.filter(store=context['store'])
    except Store.DoesNotExist:
        raise Http404("Store does not exist.")
    return render(request=request,template_name='store/store.html',context=context)