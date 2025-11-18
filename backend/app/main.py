from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users, customers, shops, payments, loans, subscriptions, usage

app = FastAPI(title="PayLoop API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(customers.router, prefix="/api/customers", tags=["customers"])
app.include_router(shops.router, prefix="/api/shops", tags=["shops"])
app.include_router(payments.router, prefix="/api/payments", tags=["payments"])
app.include_router(loans.router, prefix="/api/loans", tags=["loans"])
app.include_router(subscriptions.router, prefix="/api/subscriptions", tags=["subscriptions"])
app.include_router(usage.router, prefix="/api/usage", tags=["usage"])

@app.get("/")
def root():
    return {"message": "Welcome to PayLoop API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
