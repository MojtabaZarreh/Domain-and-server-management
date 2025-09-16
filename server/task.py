import sys 
import os
from datetime import datetime, date, timedelta
sys.path.append('/app')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django 
django.setup()
from server.models import Server 
from services.mail import send_email

today = date.today() 
warn_date = today + timedelta(days=7)
servers = Server.objects.filter(
    expiration_date__lte=warn_date,
    expiration_date__gte=today
)

if servers.exists():
    messages = [
        f"{server.name} expires on {server.expiration_date.strftime('%Y-%m-%d')}"
        for server in servers
    ]
    mail = "Server Expiration Warnings:\n" + "\n".join(messages) + ""
    print(mail)
    send_email(body=mail)
else:
    print("No servers expiring in the next 7 days.")