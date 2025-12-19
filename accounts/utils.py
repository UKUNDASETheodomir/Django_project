import secrets
import token
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import OTPToken

def generate_otp(user):
    token = secrets.randbelow(1000000)
    token = f"{token:06d}" 
    expiration_time = timezone.now() + timezone.timedelta(minutes=5)

    OTPToken.objects.update_or_create(
        user=user, 
        defaults={
            'token': token,
            'created_at': timezone.now(),
            'expired_at': expiration_time, 
        }
    )
    return token

def send_otp_email(user):
    token = generate_otp(user)
    subject = "Your Security Code"
    message = f"Hello {user.username},\n\nYour One-Time Password (OTP) is: {token}\n\nThis code expires in 5 minutes."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False
    )