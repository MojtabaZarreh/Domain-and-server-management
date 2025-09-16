import sys 
import os
from datetime import datetime, date, timedelta
sys.path.append('/app')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django 
django.setup()
from domain.models import Domain 
from services.mail import send_email

today = date.today() 
warn_date = today + timedelta(days=7)
domains = Domain.objects.filter(
    expiration_date__lte=warn_date,
    expiration_date__gte=today
)

if domains.exists():
    messages = [
        f"{domain.name} expires on {domain.expiration_date.strftime('%Y-%m-%d')}"
        for domain in domains
    ]
    mail = "Domain Expiration Warnings:\n" + "\n".join(messages) + ""
    print(mail)
    send_email(body=mail)
else:
    print("No domains expiring in the next 7 days.")