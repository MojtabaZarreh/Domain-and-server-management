import sys 
import os
from datetime import datetime, date, timedelta
sys.path.append('/app')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django 
django.setup()
from certificate.models import Certificate 
from services.mail import send_email

today = date.today() 
warn_date = today + timedelta(days=7)
certificates = Certificate.objects.filter(
    expiration_date__lte=warn_date,
    expiration_date__gte=today
)

if certificates.exists():
    messages = [
        f"{certificate.name} expires on {certificate.expiration_date.strftime('%Y-%m-%d')}"
        for certificate in certificates
    ]
    mail = "Certificate Expiration Warnings:\n" + "\n".join(messages) + ""
    print(mail)
    send_email(body=mail)
else:
    print("No certificates expiring in the next 7 days.")