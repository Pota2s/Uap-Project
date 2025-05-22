from django.shortcuts import render,redirect
from django.http import Http404, HttpRequest
from . import models
from .forms import StoreForm,ProductForm

# Create your views here.
def productView(request : HttpRequest, product_id : int, store_id : int):
    context = dict()
    
    try:
        context['store'] = models.Store.objects.get(pk=store_id)
        context['store_members'] = models.StoreMember.objects.filter(store=context['store'])
    except models.Store.DoesNotExist:  
        raise Http404("Store does not exist.")

    try:
        context['product'] = models.Product.objects.get(pk=product_id)
    except models.Product.DoesNotExist:
        raise Http404("Product does not exist.")

    context['is_wishlisted'] = False

    try:
        models.WishList.objects.get(product=context['product'],user=request.user)
        context['is_wishlisted'] = True
    except models.WishList.DoesNotExist:
        context['is_wishlisted'] = False

    context['is_in_cart'] = False

    try:
        models.Order.objects.get(product=context['product'],user=request.user)
        context['is_in_cart'] = True
    except models.Order.DoesNotExist:
        context['is_in_cart'] = False

    context['is_owned'] = False
    try:
        models.LibraryItem.objects.get(product=context['product'],user=request.user)
        context['is_owned'] = True
    except models.LibraryItem.DoesNotExist:
        context['is_owned'] = False

    return render(request=request,template_name='store/product.html',context=context)

def storeView(request : HttpRequest,store_id : int):
    context = dict()
    try:
        context['store'] = models.Store.objects.get(pk=store_id)
        context['products'] = models.Product.objects.filter(store=context['store'])
        context['store_members'] = models.StoreMember.objects.filter(store=context['store'])
    except models.Store.DoesNotExist:
        raise Http404("Store does not exist.")
    return render(request=request,template_name='store/store.html',context=context)

def storeCreateView(request :HttpRequest):

    context = dict()
    context['form'] = StoreForm()

    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            if models.Store.objects.filter(name = form.cleaned_data['name']).exists():
                form.add_error('name','Store with this name already exists.')
                return render(request=request,template_name='store/store_create.html',context=context)

            models.Store.objects.create(
                name = form.cleaned_data['name'],
                description = form.cleaned_data['description'],
                owner = request.user
                )

            store = models.Store.objects.get(name = form.cleaned_data['name'])
            return redirect('store',store_id=store.id) # type: ignore

    return render(request=request,template_name='store/store_create.html',context=context)

def storeEditView(request : HttpRequest,store_id : int):
    store = models.Store.objects.get(pk=store_id)
    store_members = models.StoreMember.objects.filter(store=store)

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
    ctx['store'] = models.Store.objects.get(pk=store_id)
    store_members = models.StoreMember.objects.filter(store=ctx['store'])

    if request.user != ctx['store'].owner and request.user not in store_members:
        raise Http404("You are not the owner or a member of this store.")

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            if models.Product.objects.filter(store = store_id, name = form.cleaned_data['name']).exists():
                form.add_error('name','Product with this name already exists.')
                return render(request=request,template_name='store/product_create.html',context=ctx)

            models.Product.objects.create(
                name = form.cleaned_data['name'],
                description = form.cleaned_data['description'],
                price = form.cleaned_data['price'],
                store = models.Store.objects.get(pk=store_id)
                )
            
            product = models.Product.objects.get(name = form.cleaned_data['name'])
            return redirect('product',store_id = store_id,product_id=product.id)

    return render(request=request,template_name='store/product_create.html',context=ctx)

def productEditView(request : HttpRequest,product_id : int,store_id : int):
    ctx : dict = dict()
    ctx['form'] = ProductForm()
    store = models.Store.objects.get(pk=store_id)
    product = models.Product.objects.get(pk=product_id)
    store_members = models.StoreMember.objects.filter(store=store)

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

def addToWishList(request : HttpRequest,product_id : int,store_id : int):
    if request.user.is_authenticated:
        models.WishList.objects.get_or_create(user=request.user, product_id=product_id)
    return redirect('product',store_id=store_id,product_id=product_id) # type: ignore

def removeFromWishList(request : HttpRequest,product_id : int,store_id : int):
    if request.user.is_authenticated:
        models.WishList.objects.get(user=request.user, product_id=product_id).delete()
    return redirect('product',store_id=store_id,product_id=product_id) # type: ignore

def addToCart(request : HttpRequest,product_id : int,store_id : int):
    if request.user.is_authenticated:
        models.Order.objects.get_or_create(user=request.user, product_id=product_id)
    return redirect('product',store_id=store_id,product_id=product_id) # type: ignore

def removeFromCart(request : HttpRequest,product_id : int,store_id : int):
    if request.user.is_authenticated:
        models.Order.objects.get(user=request.user, product_id=product_id).delete()
    return redirect('product',store_id=store_id,product_id=product_id) # type: ignore

def cartView(request : HttpRequest):
    
    if not request.user.is_authenticated:
        return render(request=request,template_name='store/cart.html',context=dict())
    context = dict()
    context['cart'] = list(models.Order.objects.filter(user=request.user))
    if request.method == 'POST':
        for order in context['cart']:
            models.LibraryItem.objects.create(
                user = request.user,
                product = order.product
            )
            order.delete()
        return redirect('cart')

    context['total_price'] = 0.0
    for order in context['cart']:
        context['total_price'] += order.product.price # type: ignore

    return render(request=request,template_name='store/cart.html',context=context)

def globalStoreView(request : HttpRequest):
    ctx = dict()
    ctx['products'] = models.Product.objects.all().order_by('-id')
    return render(request=request,template_name='store/global_store.html',context=ctx)