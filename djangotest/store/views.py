from django.shortcuts import render,redirect
from django.http import Http404, HttpRequest
from .models import Store,Product,StoreMember
from .forms import StoreForm,ProductForm

# Create your views here.
def productView(request : HttpRequest,product_id : int,store_id : int):
    context = dict()
    try:
        context['product'] = Product.objects.get(pk=product_id)
        context['store'] = Store.objects.get(pk=store_id)
        context['store_members'] = StoreMember.objects.filter(store=context['store'])
    except Product.DoesNotExist:
        raise Http404("Product does not exist.")
    return render(request=request,template_name='store/product.html',context=context)

def storeView(request : HttpRequest,store_id : int):
    context = dict()
    try:
        context['store'] = Store.objects.get(pk=store_id)
        context['products'] = Product.objects.filter(store=context['store'])
        context['store_members'] = StoreMember.objects.filter(store=context['store'])
    except Store.DoesNotExist:
        raise Http404("Store does not exist.")
    return render(request=request,template_name='store/store.html',context=context)

def storeCreateView(request :HttpRequest):

    context = dict()
    context['form'] = StoreForm()

    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            if Store.objects.filter(name = form.cleaned_data['name']).exists():
                form.add_error('name','Store with this name already exists.')
                return render(request=request,template_name='store/store_create.html',context=context)

            Store.objects.create(
                name = form.cleaned_data['name'],
                description = form.cleaned_data['description'],
                owner = request.user
                )
            
            store = Store.objects.get(name = form.cleaned_data['name'])
            return redirect('store',store_id=store.id) # type: ignore

    return render(request=request,template_name='store/store_create.html',context=context)

def storeEditView(request : HttpRequest,store_id : int):
    store = Store.objects.get(pk=store_id)
    store_members = StoreMember.objects.filter(store=store)

    if request.user != store.owner and request.user not in store_members:
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

def productCreateView(request : HttpRequest,store_id):
    ctx = dict()
    ctx['form'] = ProductForm()
    ctx['store'] = Store.objects.get(pk=store_id)
    store_members = StoreMember.objects.filter(store=ctx['store'])

    if request.user != ctx['store'].owner and request.user not in store_members:
        raise Http404("You are not the owner or a member of this store.")

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            if Product.objects.filter(store = store_id, name = form.cleaned_data['name']).exists():
                form.add_error('name','Product with this name already exists.')
                return render(request=request,template_name='store/product_create.html',context=ctx)

            Product.objects.create(
                name = form.cleaned_data['name'],
                description = form.cleaned_data['description'],
                price = form.cleaned_data['price'],
                store = Store.objects.get(pk=store_id)
                )
            
            product = Product.objects.get(name = form.cleaned_data['name'])
            return redirect('product',store_id = store_id,product_id=product.id)

    return render(request=request,template_name='store/product_create.html',context=ctx)

def productEditView(request : HttpRequest,product_id : int,store_id : int):
    ctx : dict = dict()
    ctx['form'] = ProductForm()
    store = Store.objects.get(pk=store_id)
    product = Product.objects.get(pk=product_id)
    store_members = StoreMember.objects.filter(store=store)

    if request.user != store.owner and request.user not in store_members:
        raise Http404("You are not the owner or a member of this store.")
    
    if request.method == 'POST':
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            product.name = form.cleaned_data['name']
            product.description = form.cleaned_data['description']
            product.price = form.cleaned_data['price']
            product.thumbnail = form.cleaned_data['thumbnail']
            product.save()
            return redirect('product',store_id=store_id,product_id=product.id)
    
    return render(request=request,template_name='store/product_edit.html',context=ctx)

