from ninja import NinjaAPI, Schema
from django.contrib.auth import authenticate
from .models import APIKey
from .auth import APIKeyAuth

api = NinjaAPI(urls_namespace="account_api")

class LoginSchema(Schema):
    username: str
    password: str

class APIKeyOut(Schema):
    key: str
    expires: str
    
class UserOut(Schema):
    id: int
    username: str
    email: str

@api.post("/login", response=APIKeyOut)
def login(request, data: LoginSchema):
    user = authenticate(username=data.username, password=data.password)
    if not user:
        return api.create_response(request, {"detail": "Invalid credentials"}, status=401)
    api_key = APIKey.create_key(user)
    return {"key": api_key.key, "expires": api_key.expires.isoformat()}

@api.get("/me", response=UserOut, auth=APIKeyAuth())
def me(request):
    return request.auth