from django.shortcuts import render,redirect
from store_app.models import PRODUCT,Categories,Filter_Price,Color,Brand,Contact,Order,OrderItem
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
import razorpay
from django.views.decorators.csrf import csrf_exempt

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def BASE(request):
    return render(request, 'base.html')

def HOME(request):  # New view for the root URL
    product = PRODUCT.objects.filter(status = 'Publish')
    
    context = {'product': product}  
    return render(request, 'home.html',context)  # Make sure 'home.html' exists


def PRODUCT_view(request):
    product = PRODUCT.objects.filter(status='Publish')
    
    categories = Categories.objects.all()
    filter_Price = Filter_Price.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()
    
    CATID = request.GET.get('categories')
    PRICE_ID = request.GET.get('filter_Price')
    COLOR_ID = request.GET.get('color')
    BRAND_ID = request.GET.get('brand')
    
    ATOZ_ID = request.GET.get('atoz')
    ZTOA_ID = request.GET.get('ztoa')
    LTOH_ID = request.GET.get('ltoh')
    HTOL_ID = request.GET.get('htol')
    NEW_PRODUCT_ID = request.GET.get('new_product')
    OLD_PRODUCT_ID = request.GET.get('old_product')
    
    if CATID:
        product = product.filter(categories=CATID,status='Publish')
    
    if PRICE_ID:
        product = product.filter(filter_Price__price=PRICE_ID,status='Publish')
        
    if COLOR_ID:
        product = product.filter(color=COLOR_ID,status='Publish')
    
    if BRAND_ID:
        product = product.filter(brand=BRAND_ID,status='Publish')
    
    if ATOZ_ID:
        product = product.filter(status='Publish').order_by('name')
    
    if ZTOA_ID:
        product = product.filter(status='Publish').order_by('-name')
    
    if LTOH_ID:
        product = product.filter(status='Publish').order_by('price')
    
    if HTOL_ID:
        product = product.filter(status='Publish').order_by('-price')
    
    if NEW_PRODUCT_ID:
        product = product.filter(status='Publish',condition='New').order_by('-id')
        
    if OLD_PRODUCT_ID:
        product =  product.filter(status='Publish',condition='Old').order_by('-id')
    
    context = {
        'product': product,
        'categories': categories,
        'f_price': filter_Price,
        'color': color,
        'brand': brand,
    }
    return render(request, 'product.html', context)

def SEARCH(request):
    query = request.GET.get('query')
    
    product = PRODUCT.objects.filter(name__icontains = query)
    
    context = {
        'product':product,
    }
    return render(request,'search.html',context)

def PRODUCT_DETAILS(request,id):
    
    prod =  PRODUCT.objects.filter(id = id).first()
    
    context = {
        'prod':prod,
    }
    return  render(request,'product_single.html',context)

def CONTACT_PAGE(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        contact = Contact(
            name = name,
            email=email,
            subject=subject,
            message=message,
        )
    
        subject = subject
        message = message
        email_from = settings.EMAIL_HOST_USER
        
        try:
            send_mail(subject, message, email_from, ['your email id'])
            contact.save()
            return redirect('home')
        except Exception as e:
            print(f"Error sending email: {e}")
            return render(request, 'contact.html', {'error': 'Failed to send email. Please try again.'})
        
    return render(request,'contact.html')

def HANDLEREGISTER(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        FirstName = request.POST.get('FirstName')
        LastName = request.POST.get('lastName')
        
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password2')
        
        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match.'})
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = FirstName
            user.last_name = LastName
            user.save()
            return redirect('register')
        except Exception as e:
            print(f"Error creating user: {e}")
            return render(request, 'auth.html', {'error': 'Failed to register. Please try again.'})
    return render(request,'register.html')

def HANDLELOGIN(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials.'})
    return render(request,'login.html')

def HANDLELOGOUT(request):
    logout(request)
    response = redirect('home')  # Redirect to the register page or home page after logout

    # Delete all cookies
    for key in request.COOKIES:
        response.delete_cookie(key)

    return response



@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = PRODUCT.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = PRODUCT.objects.get(id=id)
    cart.remove(product)
    return redirect("cart")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = PRODUCT.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart")

@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = PRODUCT.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart")


@login_required(login_url="/login/")
def cart(request):
    
    return render(request, 'cart.html')

@login_required(login_url="/login/")
def CHECKOUT(request):
    amount_post = request.POST.get('amount')
    
    
    payment = client.order.create( 
        {"amount": amount_post + "00",  # Amount in paise
        "currency":"INR",
        "payment_capture":"1",
        })
    order_id = payment['id']
    
    context = {
        'order_id': order_id,
        'payment': payment,
    }
    return render(request, 'checkout.html',context)

def PLACE_ORDER(request):
    if request.method == "POST":
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id=uid)
        cart = request.session.get('cart')
        
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        amount = request.POST.get('total_amount')
        
        orderid = request.POST.get('order_id')
        payment = request.POST.get('payment')
        
        context = {
            'order_id': orderid,
            'amount': amount,
            'firstname': firstname,
            'phone': phone,
        }
        
        order = Order(
            first_name=firstname,
            last_name=lastname,
            country=country,
            address=address,
            city=city,
            state=state,
            zip_code=postcode,
            phone=phone,
            email=email,
            user=user,
            payment_id = orderid,
            amount = amount,
        )
        
        order.save()
        
        for i in cart:
            a = (int(cart[i]['price']) * int(cart[i]['quantity']))
            
            item = OrderItem(
                user=user,
                order=order,
                product=cart[i]['name'],
                image=cart[i]['image'],
                quantity=cart[i]['quantity'],
                price=cart[i]['price'],
                total=a,
            )
            item.save()
        return render(request, 'placeorder.html',context)
    context = {}
    return render(request, 'placeorder.html',context)

@csrf_exempt
def THANKYOU(request):
    if request.method == "POST":
        a = request.POST
        order_id = ""
        
        for key, value in a.items():
            if key == 'razorpay_order_id':
                order_id = value
                break
        
        order = Order.objects.filter(payment_id=order_id).first()
        if order:
            order.paid = True
            order.save()
    
    return render(request, 'thankyou.html')

def MY_ORDERS(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)
    
    order = OrderItem.objects.filter(user=user)
    
    context = {
        'order': order,
    }
    return render(request, 'my_order.html',context)
