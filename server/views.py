from datetime import datetime
from typing import Optional
from ninja import NinjaAPI, Schema
from .models import Server
from account.auth import APIKeyAuth

api = NinjaAPI(urls_namespace="server_api", auth=APIKeyAuth())

class ServerIn(Schema):
    name: str
    ip_address: str
    expiration_date: datetime
    location: Optional[str] = None
    description: Optional[str] = None

class ServerOut(Schema):
    id: int
    name: str
    ip_address: str
    location: Optional[str] = None
    description: Optional[str] = None
    expiration_date: datetime
    created_at: datetime


# class ServerStatusUpdate(Schema):
#     status: str


@api.get("/servers", response=list[ServerOut])
def server_list(request):
    return Server.objects.all()

@api.post("/servers", response=list[ServerIn])
def create_server(request, data: ServerIn):
    obj = Server.objects.create(
        **data.dict(
            exclude_unset=True
        )
    )
    return Server.objects.all()


@api.delete("/servers/{server_id}")
def delete_server(request, server_id: int):
    try:
        server = Server.objects.get(id=server_id)
        server.delete()
        return {"success": True}
    except Server.DoesNotExist:
        return {"error": f"Server with id {server_id} not found."}

@api.put("/servers/{server_id}", response=ServerOut)
def update_server(request, server_id: int, data: ServerIn):
    try:
        server = Server.objects.get(id=server_id)
        server.name = data.name
        server.ip_address = data.ip_address
        server.location = data.location
        server.description = data.description
        server.expiration_date = data.expiration_date
        server.save()
        return server
    except Server.DoesNotExist:
        return {"error": f"Server with id {server_id} not found."}