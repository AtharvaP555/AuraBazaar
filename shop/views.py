from django.http import HttpResponse
from django.shortcuts import render
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json


def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}

    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}             # was inside the loop — now fixed
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    thank = False
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        desc = request.POST.get('desc', '').strip()
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank': thank})


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '').strip()
        email = request.POST.get('email', '').strip()
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if order.exists():
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                response = json.dumps(
                    {"status": "success", "updates": updates, "itemsJson": order[0].items},
                    default=str
                )
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noItem"}')
        except Exception:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')


def prodView(request, myid):
    product = Product.objects.filter(id=myid).first()
    if not product:
        from django.http import Http404
        raise Http404("Product not found")
    return render(request, 'shop/prodView.html', {'product': product})


def checkout(request):
    if request.method == "POST":
        items = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address1', '').strip() + " " + request.POST.get('address2', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        zip_code = request.POST.get('zip', '').strip()
        phone = request.POST.get('phone', '').strip()
        order = Order(items=items, name=name, email=email, address=address,
                      city=city, state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        return render(request, 'shop/checkout.html', {'thank': True, 'id': order.order_id})
    return render(request, 'shop/checkout.html')


def searchMatch(query, item):
    q = query.lower()
    return (
        q in item.product_name.lower() or
        q in item.category.lower() or
        q in item.subcategory.lower() or
        q in item.description.lower()
    )


def search(request):
    query = request.GET.get('search', '').strip()
    allProds = []

    if len(query) >= 4:
        catprods = Product.objects.values('category', 'id')
        cats = {item['category'] for item in catprods}

        for cat in cats:
            prodtemp = Product.objects.filter(category=cat)
            prod = [item for item in prodtemp if searchMatch(query, item)]
            if prod:
                n = len(prod)
                nSlides = n // 4 + ceil((n / 4) - (n // 4))
                allProds.append([prod, range(1, nSlides), nSlides])

    if not allProds:
        params = {'allProds': [], 'msg': "Please make sure to enter a relevant search query"}
    else:
        params = {'allProds': allProds, 'msg': ""}

    return render(request, 'shop/search.html', params)