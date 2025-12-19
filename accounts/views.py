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
from products.models import *
from django.db.models import Sum
from django.db.models import Avg

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

    user_id = request.session.get('pre_otp_user_id')
    if not user_id:
        return redirect('login')
    
    if request.method == "POST":
        otp_input = request.POST.get("otp")
        try:
            user = CustomUser.objects.get(id=user_id)
            token = OTPToken.objects.get(user=user)
            
            
            if (token.token == otp_input) and (token.expired_at > timezone.now()):
                
                login(request, user)
                
                
                del request.session['pre_otp_user_id']
                
                token.delete()
                
                return redirect('home') 
            else:
                messages.error(request, "Invalid or expired OTP")
                
        except OTPToken.DoesNotExist:
            messages.error(request, "Something went wrong. Please try login again.")
            
    return render(request, 'accounts/verify_otp.html')


def logout_view(request):
    logout(request)
    return redirect("login")

def home_view(request):
    products = product.objects.all().annotate(avg_rating=Avg('reviews__rating'))
    context = {
        'products': products,
    }
    return render(request, 'accounts/home.html', context)

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

 

from .forms import RegisterForm, UserProfileForm

@login_required(login_url='login')
def userPage(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('user')
    else:
        form = UserProfileForm(instance=user)
    
    context = {'form': form}
    return render(request, 'accounts/user.html', context)

def request_password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(f"DEBUG: Password reset request for email: {email}")
        try:
            users = CustomUser.objects.filter(email=email)
            if users.count() > 1:
                print(f"DEBUG: Multiple users found for email: {email}")
                messages.error(request, "Multiple accounts found with this email. Please contact support.")
                return redirect('request_password_reset')
            
            user = users.first()
            if not user:
                print(f"DEBUG: No user found with email: {email}")
                messages.error(request, "No account found with this email.")
                return redirect('request_password_reset')

            print(f"DEBUG: User found: {user.username}")
            # Generate and send OTP
            try:
                send_otp_email(user)
                # Store email in session to verify later
                request.session['reset_email'] = email
                print(f"DEBUG: OTP sent successfully to {email}")
                messages.success(request, f"An OTP has been sent to {email}")
                return redirect('reset_password_confirm')
            except Exception as e:
                print(f"DEBUG: EMAIL ERROR: {e}")
                messages.error(request, f"Failed to send reset email: {str(e)}")
                return redirect('request_password_reset')
        except Exception as e:
            print(f"DEBUG: UNEXPECTED ERROR: {e}")
            messages.error(request, "An unexpected error occurred. Please try again.")
            return redirect('request_password_reset')
            
    return render(request, 'accounts/request_password_reset.html')

def reset_password_confirm(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        email = request.session.get('reset_email')
        if not email:
            messages.error(request, "Session expired. Please try again.")
            return redirect('request_password_reset')
            
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('reset_password_confirm')
            
        try:
            user = CustomUser.objects.get(email=email)
            otp_record = OTPToken.objects.filter(user=user).last()
            
            if otp_record and otp_record.token == otp_input and otp_record.expired_at > timezone.now():
                user.set_password(new_password)
                user.save()
                otp_record.delete()
                del request.session['reset_email']
                messages.success(request, "Password reset successfully. You can now login.")
                return redirect('login')
            else:
                messages.error(request, "Invalid or expired OTP.")
                
        except CustomUser.DoesNotExist:
             messages.error(request, "User not found.")
             
    return render(request, 'accounts/reset_password_confirm.html')


# def HomePage(request):
#     return render(request, 'accounts/home_page.html')
