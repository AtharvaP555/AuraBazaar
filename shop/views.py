from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json
import re


def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}

    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    return render(request, 'shop/index.html', {'allProds': allProds})


def about(request):
    return render(request, 'shop/about.html')

@require_http_methods(["GET", "POST"])
def contact(request):
    thank = False
    errors = {}

    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        desc = request.POST.get('desc', '').strip()

        if not name or len(name) > 50:
            errors['name'] = 'Name is required and must be under 50 characters.'
        if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
            errors['email'] = 'Enter a valid email address.'
        if not re.match(r'^\+?[\d\s\-]{7,20}$', phone):
            errors['phone'] = 'Enter a valid phone number.'
        if not desc or len(desc) > 1000:
            errors['desc'] = 'Message is required and must be under 1000 characters.'

        if not errors:
            Contact(name=name, email=email, phone=phone, desc=desc).save()
            thank = True

    return render(request, 'shop/contact.html', {'thank': thank, 'errors': errors})


@require_http_methods(["GET", "POST"])
def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '').strip()
        email = request.POST.get('email', '').strip()

        if not orderId.isdigit() or not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
            return HttpResponse('{"status":"error"}', content_type='application/json')

        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if order.exists():
                updates = list(
                    OrderUpdate.objects
                    .filter(order_id=orderId)
                    .values('update_desc', 'timestamp')
                )
                payload = [{'text': u['update_desc'], 'time': u['timestamp']} for u in updates]
                response = json.dumps(
                    {"status": "success", "updates": payload, "itemsJson": order[0].items},
                    default=str
                )
                return HttpResponse(response, content_type='application/json')
            else:
                return HttpResponse('{"status":"noItem"}', content_type='application/json')
        except Exception:
            return HttpResponse('{"status":"error"}', content_type='application/json')

    return render(request, 'shop/tracker.html')


def prodView(request, myid):
    product = Product.objects.filter(id=myid).first()
    if not product:
        raise Http404("Product not found")
    return render(request, 'shop/prodView.html', {'product': product})

@require_http_methods(["GET", "POST"])
def checkout(request):
    if request.method == "POST":
        errors = {}
        items = request.POST.get('itemsJson', '').strip()
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        address = (request.POST.get('address1', '').strip()
                   + ' ' + request.POST.get('address2', '').strip()).strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        zip_code = request.POST.get('zip', '').strip()
        phone = request.POST.get('phone', '').strip()

        if not name:
            errors['name'] = 'Name is required.'
        if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
            errors['email'] = 'Enter a valid email address.'
        if not address:
            errors['address'] = 'Address is required.'
        if not city:
            errors['city'] = 'City is required.'
        if not state:
            errors['state'] = 'State is required.'
        if not re.match(r'^\d{4,10}$', zip_code):
            errors['zip'] = 'Enter a valid zip code.'
        if not re.match(r'^\+?[\d\s\-]{7,20}$', phone):
            errors['phone'] = 'Enter a valid phone number.'
        if not items or items == '{}':
            errors['items'] = 'Your cart is empty.'

        if not errors:
            order = Order(items=items, name=name, email=email, address=address,
                          city=city, state=state, zip_code=zip_code, phone=phone)
            order.save()
            OrderUpdate(order_id=order.order_id,
                        update_desc="The order has been placed").save()
            return render(request, 'shop/checkout.html', {'thank': True, 'id': order.order_id})

        return render(request, 'shop/checkout.html', {'errors': errors})

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
        params = {'allProds': [], 'msg': 'Please enter a more specific search query (min 4 characters).'}
    else:
        params = {'allProds': allProds, 'msg': ''}

    return render(request, 'shop/search.html', params)