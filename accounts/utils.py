import secrets
import token
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import OTPToken

def generate_otp(user):
    # Generate a secure 6-digit code
    otp = secrets.randbelow(1000000)
    otp = f"{otp:06d}" # Ensures it is always 6 digits (e.g., 001234)
    
    # Save to database with 5-minute expiration
    token, created = OTPToken.objects.get_or_create(user=user)
    token.otp_code = otp
    token.otp_created_at = timezone.now()
    token.otp_expires_at = timezone.now() + timezone.timedelta(minutes=5)
    token.save()
    
    return otp

def send_otp_email(user):
    otp = generate_otp(user)
    subject = "Your Security Code"
    message = f"Hello {user.username},\n\nYour One-Time Password (OTP) is: {otp}\n\nThis code expires in 5 minutes."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    
    send_mail(subject, message, from_email, recipient_list)