from django.shortcuts import render,redirect
from ecomapp.models import userdetails,product,carts,order
from ecomapp.models import category
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    categories = category.objects.all() 
    if request.user.is_authenticated:
        user_profile = userdetails.objects.get(user=request.user)
      
        return render(request, 'home.html', {'user_profile': user_profile, 'categories': categories})
    else:
        
        return render(request, 'home.html',{'categories': categories})

def login1(request):
    return render(request,'login.html')
def signup(request):
    return render(request,'signup.html')

def add_details(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        address=request.POST['address']
        email=request.POST['email']
        number=request.POST['num']
        img=request.FILES.get('photo')  
        uname=request.POST['uname']
        pswd=request.POST['pswd']
        cpswd=request.POST['cpswd']
        if pswd == cpswd:
            if User.objects.filter(username=uname).exists():
                messages.info(request, 'This username already exists!!!!')
                return redirect('signup')
            else:
                user=User.objects.create_user(
                    first_name=fname,
                    last_name=lname,
                    username=uname,
                    email=email,
                    password=pswd
                )
                user.save()
                u=User.objects.get(id=user.id)
                reg=userdetails.objects.create(
                    address=address,
                    phone=number,
                    prof_image=img,
                    user=u
                )
                reg.save()
                messages.success(request, 'Profile created successfully!')
                return redirect('home')
        else:
            messages.info(request, 'Password doesnt match')
            return redirect('signup')
    return render(request, 'login.html') 


def adminlogin(request):
    if request.method == "POST":
        username=request.POST['uname']
        password=request.POST['pswd']  
        user=authenticate(username=username, password=password)  
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('adminhome')
            else:
                login(request, user)
                return redirect('user_home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login1')
    return render(request, 'login.html')

def logout1(request):
    auth.logout(request)
    return redirect('home')

def adminhome(request):
    return render(request,'admin_home.html')

def add_cate(request):
    return render(request,'category.html')

def add_cate_details(request):
    if request.method=='POST':
        cate_name=request.POST.get('category_name')
        cate=category(category_name=cate_name)
        cate.save()
        messages.success(request,'Category Added Successfully!!!')
        return redirect('add_cate')
    
def add_pro(request):
    categories=category.objects.all()
    return render(request, 'products.html', {'categories': categories})

def add_pro_details(request):
    if request.method == 'POST':
        pname = request.POST.get('pname')
        des = request.POST.get('des')
        cate = request.POST.get('sel')
        price = request.POST.get('price')
        img = request.FILES.get('photo')
        prod_cate = category.objects.get(id=cate)
        prod = product(pname=pname, prdt_desc=des, price=price, category=prod_cate, prdt_image=img)
        prod.save()
        messages.success(request, 'Product Added')
        return redirect('add_pro')
    else:
        return render(request, 'admin_home.html')


def view_product(request):
    products=product.objects.all()  
    return render(request, 'view_product.html', {'products': products})

def delete_product(request, pk):
    pro=product.objects.get(id=pk)
    pro.delete()
    return redirect('view_product')

def view_user_details(request):
    allusers=userdetails.objects.all()
    return render(request, 'view_user.html', {'all_users': allusers})
def delete_user(request,pk):
    u=userdetails.objects.get(user_id=pk)
    user1=User.objects.get(id=pk)
    u.delete()
    user1.delete()
    return redirect('view_user_details')

def user_home(request):
        categories=category.objects.all() 
        count=carts.objects.values_list('quantity',flat=True).count()
        user_profile=userdetails.objects.get(user=request.user)
        return render(request,'userhome.html', {'user_profile':user_profile,'count':count,'categories':categories})

def productlist(request,pk):
        categories = category.objects.all() 
        cat=category.objects.get(id=pk)
        products = product.objects.filter(category=cat)
        count=carts.objects.values_list('quantity',flat=True).count()
        user_profile=userdetails.objects.get(user=request.user)
        return render(request, 'product_list.html', {'category':cat,'products':products,'user_profile': user_profile,'categories':categories,'count':count})

def view_productlist(request, pk):
    cate=category.objects.get(id=pk)
    products=product.objects.filter(category=cate)
    
    user_profile=userdetails.objects.get(user=request.user)
    return render(request, 'product_list.html', {'category': cate, 'products': products,'user_profile': user_profile})

def addtocart(request, product_id):
    if request.method == 'POST':
            prod_obj = product.objects.get(id=product_id)
            user = request.user
            cart_item, created = carts.objects.get_or_create(user=user, product=prod_obj)

            if not created:
                cart_item.quantity += 1
                cart_item.save()
            return redirect('cart') 
    
def cart(request):
    user = request.user
    cart_items = carts.objects.filter(user=user)
    total_amount = sum(item.quantity * item.product.price for item in cart_items)
    
    count=carts.objects.values_list('quantity',flat=True).count()

    categories = category.objects.all()
    user_profile = None
    if request.user.is_authenticated:
        user_profile = userdetails.objects.get(user=request.user)
    
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_amount': total_amount, 'categories': categories, 'user_profile': user_profile,'count':count})


def update_quantity(request):
    if request.method == 'POST':
        item_id=request.POST.get('item_id')
        action=request.POST.get('action')
        cart_item=carts.objects.get(id=item_id)

        if action == 'increment':
            cart_item.quantity += 1
        elif action == 'decrement':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1             
        cart_item.save()

    return redirect('cart')

def remove_item(request):
    if request.method == 'POST':
        item_id=request.POST.get('item_id')
        cart_item=carts.objects.get(id=item_id)
        cart_item.delete()

    return redirect('cart')

def place_order(request):
    if request.method == 'POST':
        full_name=request.POST.get('fullName')
        email=request.POST.get('email')
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        credit_card=request.POST.get('creditCard')
        expire_date=request.POST.get('expireDate')
        cvv=request.POST.get('cvv')

        orders=order(
            full_name=full_name,
            email=email,
            address=address,
            phone=phone,
            credit_card=credit_card,
            expire_date=expire_date,
            cvv=cvv
        )
        orders.save()
        return redirect('confirm_message')  
    else:
        return redirect('user_home') 

def confirm_message(request):
    categories = category.objects.all()
    count=carts.objects.values_list('quantity',flat=True).count()
    return render(request, 'checkout.html', {'categories': categories,'count':count})