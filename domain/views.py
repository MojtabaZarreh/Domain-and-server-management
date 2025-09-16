from ninja import NinjaAPI
from .models import Domain, DomainAction
from ninja import Schema
from typing import Optional
from ninja.errors import HttpError
from datetime import datetime
from account.auth import APIKeyAuth

api = NinjaAPI(urls_namespace="domain_api", auth=APIKeyAuth())

class DomainSchema(Schema):
    name: str
    register: str
    status: str
    expiration_date: str
    description: str = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class DomainActionSchema(Schema):
    description: str
    created_at: Optional[datetime] = None
    
@api.get("/domains")
def domain_list(request):
    domains = Domain.objects.all().values("id", "name", "register", "status", "expiration_date", "description")
    return list(domains)

@api.post("/domains")
def create_domain(request, domain: DomainSchema):
    domains = Domain.objects.create(
        **domain.dict(
            exclude_unset=True
        )
    )
    return {"name": domains.name, "register": domains.register}

@api.delete("/domains/{domain_id}")
def delete_domain(request, domain_id: int):
    try:
        domain = Domain.objects.get(id=domain_id)
        domain.delete()
        return {"success": True}
    except Domain.DoesNotExist:
        raise HttpError(404, f"Domain with id {domain_id} not found.")
    
@api.put("/domains/{domain_id}", response=DomainSchema)
def update_domain(request, domain_id: int, domain: DomainSchema):
    try:
        domain_obj = Domain.objects.get(id=domain_id)
        for attr, value in domain.dict(exclude_unset=True).items():
            setattr(domain_obj, attr, value)
        domain_obj.save()
        return domain_obj
    except Domain.DoesNotExist:
        raise HttpError(404, f"Domain with id {domain_id} not found.")


@api.get("/domains/{domain_id}/actions")
def domain_actions(request, domain_id: int):
    actions = DomainAction.objects.filter(domain_id=domain_id).values("id", "description", "created_at")
    return list(actions)

@api.post("/domains/{domain_id}/actions")
def create_domain_action(request, domain_id: int, action: DomainActionSchema):
    try:
        domain = Domain.objects.get(id=domain_id)
        domain_action = DomainAction.objects.create(
            domain=domain,
            description=action.description
        )
        return list(DomainAction.objects.filter(id=domain_action.id).values("id", "description", "created_at"))
    except Domain.DoesNotExist:
        raise HttpError(404, f"Domain with id {domain_id} not found.")