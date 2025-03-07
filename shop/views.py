from django.http import HttpResponse
from django.shortcuts import render
from .models import Product,Contact,Order,OrderUpdate
from math import ceil
import json

def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')  # Get all products with their category and id
    cats = {item['category'] for item in catprods}  # Extract unique categories

    for cat in cats:
        prod = Product.objects.filter(category=cat)  # Filter products by category
        n = len(prod)  # Number of products in this category
        nSlides = n // 4 + ceil((n / 4) - (n // 4))  # Calculate number of slides for this category
        allProds.append([prod, range(1, nSlides), nSlides])  # Append category products, slide range, and number of slides
        params = {'allProds': allProds}  # Pass the grouped products to the template
    return render(request,'shop/index.html', params)

def about(request):
    return render(request,'shop/about.html')

def contact(request):
    thank = False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request,'shop/contact.html',{'thank':thank})

def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noItem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')


def prodView(request,myid):
    #Fetching products using id
    product = Product.objects.filter(id=myid)
    print(product)
    return render(request,'shop/prodView.html',{'product':product[0]})

def checkout(request):
    if request.method == "POST":
        items = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip', '')
        phone = request.POST.get('phone', '')
        order = Order(items=items, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request,'shop/checkout.html')


def searchMatch(query,item):
    if query in item.product_name.lower() or query in item.category.lower() or query in item.subcategory.lower() or query in item.description.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')  # Get all products with their category and id
    cats = {item['category'] for item in catprods}  # Extract unique categories

    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)  # Filter products by category
        prod = [item for item in prodtemp if searchMatch(query,item)]
        n = len(prod)  # Number of products in this category
        nSlides = n // 4 + ceil((n / 4) - (n // 4))  # Calculate number of slides for this category
        if len(prod)!=0:
            allProds.append([prod, range(1, nSlides), nSlides])  # Append category products, slide range, and number of slides
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query) < 4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request,'shop/search.html',params)

