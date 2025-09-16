import requests
import urllib3
from datetime import datetime
from typing import Optional
from ninja import NinjaAPI, Schema
from .models import Website
from account.auth import APIKeyAuth

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

api = NinjaAPI(urls_namespace="website_api", auth=APIKeyAuth())

class WebsiteIn(Schema):
    url: str
    description: Optional[str] = None

class WebsiteOut(Schema):
    id: int
    url: str
    status: str
    description: Optional[str]
    last_checked: Optional[datetime]
    created_at: Optional[datetime]
    
class WebsiteStatusUpdate(Schema):
    status: str


def ping(host: str) -> tuple[str, str]:
    if not host.startswith("http://") and not host.startswith("https://"):
        host = "http://" + host
    try:
        response = requests.get(host, timeout=5, verify=False)
        status = "up" if response.status_code == 200 else "down"
        return host, status
    except requests.RequestException:
        return host, "down"


@api.get("/websites", response=list[WebsiteOut])
def website_list(request):
    return Website.objects.all()

@api.post("/websites", response=WebsiteOut)
def create_website(request, data: WebsiteIn):
    host, status = ping(data.url)
    obj = Website.objects.create(
        url=host,
        description=data.description,
        status=status,
    )
    return obj

@api.delete("/websites/{website_id}")
def delete_website(request, website_id: int):
    try:
        website = Website.objects.get(id=website_id)
        website.delete()
        return {"success": True}
    except Website.DoesNotExist:
        return {"error": f"Website with id {website_id} not found."}
    
@api.patch("/websites/{website_id}", response=WebsiteOut)
def update_website(request, website_id: int, data: WebsiteStatusUpdate):
    try:
        website = Website.objects.get(id=website_id)
        if data.status is not None:
            website.status = data.status
            website.last_checked = datetime.now()
        website.save()
        return website
    except Website.DoesNotExist:
        return {"error": f"Website with id {website_id} not found."}