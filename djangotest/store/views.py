from django.shortcuts import render,redirect
from django.http import Http404
from .models import Store,Product
from .forms import StoreForm

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

def register(request):

    context = dict()
    context['form'] = StoreForm()

    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            if Store.objects.filter(name = form.cleaned_data['name']).exists():
                form.add_error('name','Store with this name already exists.')
                return render(request=request,template_name='store/register.html',context=context)
            
            Store.objects.create(
                name = form.cleaned_data['name'],
                description = form.cleaned_data['description'],
                owner = request.user
                )
            
            store = Store.objects.get(name = form.cleaned_data['name'])
            return redirect('store',store_id=store.id) # type: ignore

    return render(request=request,template_name='store/register.html',context=context)

def storeEditView(request,store_id):
    store = Store.objects.get(pk=store_id)
    if request.user != store.owner:
        raise Http404("You are not the owner of this store.")
    context = dict()
    context['store'] = store
    context['form'] = StoreForm(instance=store)
    if request.method == 'POST':
        form = StoreForm(request.POST,instance=store)
        if form.is_valid():
            store.name = form.cleaned_data['name']
            store.description = form.cleaned_data['description']
            store.save()
            return redirect('store',store_id=store.id) # type: ignore

    return render(request=request,template_name='store/store_edit.html',context=context)
