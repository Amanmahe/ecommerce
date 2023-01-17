from django.shortcuts import render
from .models import product, Contact, Orders, OrderUpdate,register_table
from math import ceil
import json
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

# Create your views here.
from django.http import HttpResponse ,HttpResponseRedirect


def index(request):
    allProds = []
    catprods = product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)

def search(request):
    query= request.GET.get('search')
    allProds = []
    catprods = product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg":""}
    if len(allProds)==0 or len(query)<4:
        params={'msg':"Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)

def searchMatch(query, item):
    if query in item.product_name or query in item.category:
        return True
    else:
        return False

def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, 'shop/contact.html')





def productview(request, myid):

    # Fetch the product using the id
    product1 = product.objects.filter(id=myid)
    return render(request, 'shop/productview.html', {'product':product1[0]})

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')


def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
    return render(request, 'shop/checkout.html')

def register(request):
    if request.method=='POST':
        fname = request.POST['first']
        last = request.POST['last']
        un = request.POST['uname']
        pwd = request.POST['password']
        em = request.POST['email']
        con = request.POST['contact']
        tp = request.POST['utype']

        usr = User.objects.create_user(un,em,pwd)
        usr.first_name = fname
        usr.last_name = last
        if tp=='sell':
            usr.is_staff=True
        usr.save()

        reg = register_table(user=usr, contact_number=con)
        reg.save()
        return render(request,'shop/register.html',{'status':"{} Account  Created  Successfully".format(fname)})

    return render(request,'shop/register.html')

def check_user(request):
    if request.method=="GET":
        un = request.GET["usern"]
        check = User.objects.filter(username=un)
        if len(check) == 1:
            return HttpResponse("Exists")
        else:
            return HttpResponse("Not Exists")

def user_login(request):
    if request.method=='POST':
        un = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(username=un,password=pwd)
        if user:
            login(request,user)
            if user.is_superuser:
                return HttpResponseRedirect("/shop/admin")
            if user.is_staff:
                return HttpResponseRedirect("/shop/seller_dashboard")
            if user.is_active:
                return HttpResponseRedirect("/shop/cust_dashboard")
        else:
            return render(request,"shop/index.html",{"status": "Invalid Username or Password"})
    return HttpResponse("called")

def cust_dashboard(request):
    return render(request,"shop/cust_dashboard.html")

def seller_dashboard(request):
    return render(request,"shop/seller_dashboard.html")

