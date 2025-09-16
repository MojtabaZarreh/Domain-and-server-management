from ninja import NinjaAPI
from .models import Certificate
from ninja import Schema
from typing import Optional
from ninja.errors import HttpError
from datetime import datetime
from account.auth import APIKeyAuth

api = NinjaAPI(
            urls_namespace="certificate_api",
            auth=APIKeyAuth() 
            )

class CertificateIn(Schema):
    name: str
    issuer: str
    expiration_date: str
    description: str = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@api.get("/ssl")
def certificate_list(request):
    certificate = Certificate.objects.all().values("id", "name", "issuer", "expiration_date", "description")
    return list(certificate)

@api.post("/ssl")
def create_certificate(request, certificate: CertificateIn):
    cert = Certificate.objects.create(
        **certificate.dict(
            exclude_unset=True
        )
    )
    return {"name": cert.name, "issuer": cert.issuer}

@api.delete("/ssl/{certificate_id}")
def delete_certificate(request, certificate_id: int):
    try:
        cert = Certificate.objects.get(id=certificate_id)
        cert.delete()
        return {"success": True}
    except Certificate.DoesNotExist:
        raise HttpError(404, f"Certificate with id {certificate_id} not found.")

@api.put("/ssl/{certificate_id}", response=CertificateIn)
def update_certificate(request, certificate_id: int, certificate: CertificateIn):
    try:
        cert = Certificate.objects.get(id=certificate_id)
        for attr, value in certificate.dict(exclude_unset=True).items():
            setattr(cert, attr, value)
        cert.save()
        return cert
    except Certificate.DoesNotExist:
        raise HttpError(404, f"Certificate with id {certificate_id} not found.")
