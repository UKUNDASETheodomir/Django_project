from urllib import request
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from django.contrib import messages

from accounts.models import CustomUser
from .decorators import  vendor_required, customer_required
from orders.models import Order, OrderItem
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from products.models import product
from django.shortcuts import render, get_object_or_404


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.models import Group
from django.utils import timezone
from accounts.models import OTPToken, CustomUser
from .utils import send_otp_email


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user_type = form.cleaned_data.get('user_type')
            user.user_type = user_type
            user.save()

            if user_type == 'C':
                group = Group.objects.get(name='customer')
            else:
                group = Group.objects.get(name='vendor')

            user.groups.add(group)

            messages.success(request, f"Account created successfully")
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            request.session['pre_otp_user_id'] = user.id
        
            send_otp_email(user)
            return redirect('verify_login_otp')
        else:
            messages.info(request, "Invalid username or password")
    return render(request, 'accounts/login.html')
def verify_login_otp(request):
    # Check if we have a user waiting in the session
    user_id = request.session.get('pre_otp_user_id')
    if not user_id:
        return redirect('login')
    
    if request.method == "POST":
        otp_input = request.POST.get("otp")
        try:
            user = CustomUser.objects.get(id=user_id)
            token = OTPToken.objects.get(user=user)
            
            # Check logic: Code matches AND is not expired
            if (token.otp_code == otp_input) and (token.otp_expires_at > timezone.now()):
                # Success! Now we actually login
                login(request, user)
                
                # Cleanup
                del request.session['pre_otp_user_id']
                token.otp_code = None # Invalidate token
                token.save()
                
                return redirect('home') # Change to your dashboard URL
            else:
                messages.error(request, "Invalid or expired OTP")
                
        except OTPToken.DoesNotExist:
            messages.error(request, "Something went wrong. Please try login again.")
            
    return render(request, 'accounts/verify_otp.html')
# --- 2. PASSWORD RESET FLOW ---

def request_password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = CustomUser.objects.get(email=email)
            # Store email in session to pass to next step
            request.session['reset_email'] = email
            send_otp_email(user)
            return redirect('reset_password_confirm')
        except CustomUser.DoesNotExist:
            # Security: Don't reveal if user exists, just pretend we sent it
            messages.success(request, "If an account exists, an OTP has been sent.")
            
    return render(request, 'accounts/request_reset.html')

def reset_password_confirm(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('request_password_reset')

    if request.method == "POST":
        otp_input = request.POST.get("otp")
        new_password = request.POST.get("new_password")
        
        try:
            user = CustomUser.objects.get(email=email)
            token = OTPToken.objects.get(user=user)
            
            if (token.otp_code == otp_input) and (token.otp_expires_at > timezone.now()):
                # Set new password
                user.set_password(new_password)
                user.save()
                
                # Cleanup
                token.otp_code = None
                token.save()
                del request.session['reset_email']
                
                messages.success(request, "Password reset successful. Please login.")
                return redirect('login')
            else:
                messages.error(request, "Invalid or expired OTP")
                
        except (CustomUser.DoesNotExist, OTPToken.DoesNotExist):
             messages.error(request, "Error processing request.")

    return render(request, 'accounts/reset_confirm.html')



def logout_view(request):
    logout(request)
    return redirect("login")

def home_view(request):
    products= product.objects.all()
    return render(request, "accounts/home.html",{'products':products})

# @allowed_users(allowed_roles=['vendor'])
@login_required(login_url='login')
def dashboard(request):
    return render(request, "accounts/dashboard.html")


@vendor_required
def vendor_dashboard(request):
    # Get all products for the current vendor
    vendor_products = product.objects.filter(vendor=request.user)

    # Order them by the 'created_at' field to get the most recent ones first
    recent_products = vendor_products.order_by('-created_at')

    # Calculate statistics based only on the vendor's products
    total_pro = vendor_products.count()
    unav_pro = vendor_products.filter(status='unavailable').count()
    
    # TODO: Filter orders based on the vendor's products for accurate stats
    act_order = Order.objects.filter(status='active').count()
    pend_order = Order.objects.filter(status='pending').count()

    context = {"products": recent_products, 'total_pro': total_pro, "act_order": act_order, "pend_order": pend_order, 'unav_pro': unav_pro}
    return render(request,'accounts/vendor_dashboard.html',context)

@login_required(login_url='login')
def product_list(request):
    products = product.objects.all()
    return render(request, 'accounts/product_list.html', {'products': products})
@login_required(login_url='login')
def product_detail(request, id):
    prod = get_object_or_404(product, id=id)
    return render(request, 'accounts/product_detail.html', {'product': prod}) 

@login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
def userPage(request):
    return render(request, 'accounts/user.html')


# def HomePage(request):
#     return render(request, 'accounts/home_page.html')
