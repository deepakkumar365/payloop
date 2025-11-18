import sys
import os
from datetime import datetime, timedelta, date
from decimal import Decimal
from sqlalchemy import text

sys.path.insert(0, os.path.dirname(__file__))

from app.db.database import SessionLocal
from app.models.user import User, UserRole
from app.models.customer import Customer, CollectionCycle, PaymentType
from app.models.shop import Shop
from app.models.payment import Payment
from app.models.loan import Loan, LoanRepaymentFrequency, LoanPayment
from app.models.subscription import Subscription, Bill, BillPayment, BillingCycle, BillStatus
from app.models.usage import UsageBasedBilling, UsageRecord, UsageBill, UsageBillPayment, UsageBillingStatus
from app.core.security import get_password_hash


def clear_all_data(db):
    """Clear all existing data from tables"""
    try:
        db.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
        db.commit()
        print("[OK] Truncated all tables and reset sequences")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error truncating tables: {e}")
        return False
    return True


def seed_users(db):
    """Create sample users"""
    users_data = [
        {
            "email": "superadmin@payloop.com",
            "username": "superadmin",
            "full_name": "Super Admin User",
            "role": "SUPERADMIN",
            "password": "superadmin123"
        },
        {
            "email": "admin@payloop.com",
            "username": "admin",
            "full_name": "Admin User",
            "role": "ADMIN",
            "password": "admin123"
        },
        {
            "email": "agent1@payloop.com",
            "username": "agent1",
            "full_name": "John Agent",
            "role": "AGENT",
            "password": "agent123"
        },
        {
            "email": "agent2@payloop.com",
            "username": "agent2",
            "full_name": "Sarah Agent",
            "role": "AGENT",
            "password": "agent123"
        },
        {
            "email": "agent3@payloop.com",
            "username": "agent3",
            "full_name": "Mike Agent",
            "role": "AGENT",
            "password": "agent123"
        }
    ]
    
    try:
        users = []
        for user_data in users_data:
            user = User(
                email=user_data["email"],
                username=user_data["username"],
                full_name=user_data["full_name"],
                role=user_data["role"],
                hashed_password=get_password_hash(user_data["password"]),
                is_active=True
            )
            users.append(user)
            db.add(user)
        
        db.commit()
        print(f"[OK] Created {len(users)} users")
        return users
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error creating users: {e}")
        return []


def seed_customers(db, users):
    """Create sample customers with payment types"""
    agents = [u for u in users if u.role == "AGENT"]
    if not agents:
        print("[ERROR] No agents available to assign customers")
        return []
    
    customers_data = [
        {
            "name": "ABC Retail Store",
            "phone": "+91-9876543210",
            "address": "123 Main Street, Mumbai",
            "payment_type": PaymentType.LOAN,
            "collection_cycle": CollectionCycle.DAILY,
            "collection_amount": Decimal("1000.00"),
            "agent_id": agents[0].id
        },
        {
            "name": "XYZ Trading Co.",
            "phone": "+91-9876543211",
            "address": "456 Market Road, Delhi",
            "payment_type": PaymentType.SUBSCRIPTION,
            "collection_cycle": CollectionCycle.WEEKLY,
            "collection_amount": Decimal("5000.00"),
            "agent_id": agents[1].id if len(agents) > 1 else agents[0].id
        },
        {
            "name": "Star Electronics",
            "phone": "+91-9876543212",
            "address": "789 Tech Park, Bangalore",
            "payment_type": PaymentType.USAGE_BASED,
            "collection_cycle": CollectionCycle.DAILY,
            "collection_amount": Decimal("1500.00"),
            "agent_id": agents[2].id if len(agents) > 2 else agents[0].id
        },
        {
            "name": "Prime Distribution",
            "phone": "+91-9876543213",
            "address": "321 Business Avenue, Pune",
            "payment_type": PaymentType.LOAN,
            "collection_cycle": CollectionCycle.MONTHLY,
            "collection_amount": Decimal("25000.00"),
            "agent_id": agents[0].id
        },
        {
            "name": "Metro Trading House",
            "phone": "+91-9876543214",
            "address": "654 Commerce Street, Kolkata",
            "payment_type": PaymentType.SUBSCRIPTION,
            "collection_cycle": CollectionCycle.WEEKLY,
            "collection_amount": Decimal("8000.00"),
            "agent_id": agents[1].id if len(agents) > 1 else agents[0].id
        },
        {
            "name": "Smart Retail Ltd",
            "phone": "+91-9876543215",
            "address": "987 Shopping Complex, Hyderabad",
            "payment_type": PaymentType.USAGE_BASED,
            "collection_cycle": CollectionCycle.DAILY,
            "collection_amount": Decimal("2000.00"),
            "agent_id": agents[2].id if len(agents) > 2 else agents[0].id
        }
    ]
    
    try:
        customers = []
        for customer_data in customers_data:
            customer = Customer(
                name=customer_data["name"],
                phone=customer_data["phone"],
                address=customer_data["address"],
                payment_type=customer_data["payment_type"],
                collection_cycle=customer_data["collection_cycle"],
                collection_amount=customer_data["collection_amount"],
                agent_id=customer_data["agent_id"]
            )
            customers.append(customer)
            db.add(customer)
        
        db.commit()
        print(f"[OK] Created {len(customers)} customers")
        return customers
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error creating customers: {e}")
        return []


def seed_shops(db, customers):
    """Create sample shops"""
    shops_data = [
        {
            "name": "ABC Main Store",
            "address": "123 Main Street, Mumbai",
            "phone": "+91-9876543220",
            "customer_id": customers[0].id if customers else None,
            "is_direct_payer": False
        },
        {
            "name": "ABC Outlet",
            "address": "124 Main Street, Mumbai",
            "phone": "+91-9876543221",
            "customer_id": customers[0].id if customers else None,
            "is_direct_payer": False
        },
        {
            "name": "XYZ Warehouse",
            "address": "457 Market Road, Delhi",
            "phone": "+91-9876543222",
            "customer_id": customers[1].id if len(customers) > 1 else None,
            "is_direct_payer": False
        },
        {
            "name": "Star Main Branch",
            "address": "790 Tech Park, Bangalore",
            "phone": "+91-9876543223",
            "customer_id": customers[2].id if len(customers) > 2 else None,
            "is_direct_payer": False
        },
        {
            "name": "Star Service Center",
            "address": "791 Tech Park, Bangalore",
            "phone": "+91-9876543224",
            "customer_id": customers[2].id if len(customers) > 2 else None,
            "is_direct_payer": False
        },
        {
            "name": "Direct Vendor",
            "address": "Direct Location",
            "phone": "+91-9876543225",
            "customer_id": None,
            "is_direct_payer": True
        }
    ]
    
    try:
        shops = []
        for shop_data in shops_data:
            shop = Shop(
                name=shop_data["name"],
                address=shop_data["address"],
                phone=shop_data["phone"],
                customer_id=shop_data["customer_id"],
                is_direct_payer=shop_data["is_direct_payer"],
                is_active=True
            )
            shops.append(shop)
            db.add(shop)
        
        db.commit()
        print(f"[OK] Created {len(shops)} shops")
        return shops
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error creating shops: {e}")
        return []


def seed_payments(db, customers, shops, users):
    """Create sample payment records"""
    if not users or len(users) < 2:
        print("[ERROR] Not enough users to create payments")
        return []
    
    agents = [u for u in users if u.role == "AGENT"]
    if not agents:
        print("[ERROR] No agents available to record payments")
        return []
    
    payments_data = []
    base_date = datetime.utcnow() - timedelta(days=30)
    
    for i, customer in enumerate(customers[:3]):
        for day in range(0, 30, 5):
            payment_date = base_date + timedelta(days=day)
            shop = next((s for s in shops if s.customer_id == customer.id), None)
            agent = agents[i % len(agents)]
            
            payment = {
                "customer_id": customer.id,
                "shop_id": shop.id if shop else None,
                "amount": Decimal(str(float(customer.collection_amount) * 0.9)),
                "collected_by_id": agent.id,
                "payment_date": payment_date,
                "notes": f"Payment collected on {payment_date.strftime('%Y-%m-%d')}"
            }
            payments_data.append(payment)
    
    try:
        payments = []
        for payment_data in payments_data:
            payment = Payment(
                customer_id=payment_data["customer_id"],
                shop_id=payment_data["shop_id"],
                amount=payment_data["amount"],
                collected_by_id=payment_data["collected_by_id"],
                payment_date=payment_data["payment_date"],
                notes=payment_data["notes"]
            )
            payments.append(payment)
            db.add(payment)
        
        db.commit()
        print(f"[OK] Created {len(payments)} payment records")
        return payments
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error creating payments: {e}")
        return []


def seed_loans(db, customers, users):
    """Create sample loans"""
    agents = [u for u in users if u.role == "AGENT"]
    if not agents:
        print("[ERROR] No agents available")
        return []
    
    loan_customers = [c for c in customers if c.payment_type == PaymentType.LOAN]
    if not loan_customers:
        print("[WARNING] No loan customers available")
        return []
    
    loans_data = []
    base_date = datetime.utcnow() - timedelta(days=60)
    
    for i, customer in enumerate(loan_customers):
        principal = Decimal("50000.00")
        interest_rate = Decimal("5.00")
        interest_amount = principal * interest_rate / 100
        total_repayable = principal + interest_amount
        
        loan = {
            "customer_id": customer.id,
            "principal_amount": principal,
            "interest_rate": interest_rate,
            "total_repayable_amount": total_repayable,
            "repayment_frequency": LoanRepaymentFrequency.MONTHLY,
            "start_date": base_date,
            "end_date": base_date + timedelta(days=365),
            "notes": f"Loan for {customer.name}"
        }
        loans_data.append(loan)
    
    try:
        loans = []
        for loan_data in loans_data:
            db_loan = Loan(**loan_data)
            loans.append(db_loan)
            db.add(db_loan)
            
            db.flush()
            
            agent = agents[len(loans) % len(agents)]
            payment_date = base_date + timedelta(days=30)
            loan_payment = LoanPayment(
                loan_id=db_loan.id,
                customer_id=db_loan.customer_id,
                amount_paid=Decimal("10000.00"),
                pending_balance=db_loan.total_repayable_amount - Decimal("10000.00"),
                payment_date=payment_date,
                payment_mode="CASH",
                recorded_by_id=agent.id,
                notes="First installment"
            )
            db.add(loan_payment)
        
        db.commit()
        print(f"[OK] Created {len(loans)} loans with payments")
        return loans
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error creating loans: {e}")
        return []


def seed_subscriptions(db, customers, users):
    """Create sample subscriptions"""
    agents = [u for u in users if u.role == "AGENT"]
    if not agents:
        print("[ERROR] No agents available")
        return []
    
    sub_customers = [c for c in customers if c.payment_type == PaymentType.SUBSCRIPTION]
    if not sub_customers:
        print("[WARNING] No subscription customers available")
        return []
    
    subscriptions_data = []
    base_date = datetime.utcnow() - timedelta(days=30)
    
    for i, customer in enumerate(sub_customers):
        subscription = {
            "customer_id": customer.id,
            "subscription_amount": Decimal("10000.00"),
            "billing_cycle": BillingCycle.MONTHLY,
            "start_date": base_date,
            "end_date": None,
            "notes": f"Monthly subscription for {customer.name}"
        }
        subscriptions_data.append(subscription)
    
    try:
        subscriptions = []
        for sub_data in subscriptions_data:
            db_sub = Subscription(**sub_data)
            subscriptions.append(db_sub)
            db.add(db_sub)
            
            db.flush()
            
            agent = agents[len(subscriptions) % len(agents)]
            bill_start = base_date
            bill_end = bill_start + timedelta(days=30)
            bill_number = f"BILL-{db_sub.customer_id}-{bill_start.strftime('%Y%m%d')}"
            
            bill = Bill(
                subscription_id=db_sub.id,
                customer_id=db_sub.customer_id,
                bill_number=bill_number,
                billing_period_start=bill_start,
                billing_period_end=bill_end,
                amount_due=Decimal("10000.00"),
                previous_pending_balance=Decimal("0.00"),
                total_amount_to_collect=Decimal("10000.00"),
                status=BillStatus.PENDING,
                notes="Monthly billing"
            )
            db.add(bill)
            
            db.flush()
            
            bill_payment = BillPayment(
                bill_id=bill.id,
                customer_id=db_sub.customer_id,
                amount_paid=Decimal("5000.00"),
                payment_date=bill_start + timedelta(days=5),
                payment_mode="UPI",
                recorded_by_id=agent.id,
                notes="Partial payment"
            )
            db.add(bill_payment)
        
        db.commit()
        print(f"[OK] Created {len(subscriptions)} subscriptions with bills")
        return subscriptions
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error creating subscriptions: {e}")
        return []


def seed_usage_billing(db, customers, users):
    """Create sample usage-based billing"""
    agents = [u for u in users if u.role == "AGENT"]
    if not agents:
        print("[ERROR] No agents available")
        return []
    
    usage_customers = [c for c in customers if c.payment_type == PaymentType.USAGE_BASED]
    if not usage_customers:
        print("[WARNING] No usage-based customers available")
        return []
    
    billings_data = []
    base_date = datetime.utcnow() - timedelta(days=30)
    
    for i, customer in enumerate(usage_customers):
        billing = {
            "customer_id": customer.id,
            "service_name": "Milk Delivery" if i % 2 == 0 else "Newspaper Delivery",
            "rate_per_unit": Decimal("50.00") if i % 2 == 0 else Decimal("6.00"),
            "rate_type": "PER_DAY",
            "start_date": base_date,
            "end_date": None,
            "notes": f"Usage-based billing for {customer.name}"
        }
        billings_data.append(billing)
    
    try:
        billings = []
        for billing_data in billings_data:
            db_billing = UsageBasedBilling(**billing_data)
            billings.append(db_billing)
            db.add(db_billing)
            
            db.flush()
            
            for day in range(25):
                usage_date = base_date.date() + timedelta(days=day)
                usage_record = UsageRecord(
                    usage_billing_id=db_billing.id,
                    customer_id=db_billing.customer_id,
                    usage_date=usage_date,
                    quantity_used=Decimal("1.00"),
                    notes=f"Usage on {usage_date}"
                )
                db.add(usage_record)
            
            db.flush()
            
            agent = agents[len(billings) % len(agents)]
            bill_start = base_date.date()
            bill_end = bill_start + timedelta(days=29)
            bill_number = f"UBILL-{db_billing.customer_id}-{bill_start.strftime('%Y%m%d')}"
            
            total_days = 25
            total_quantity = Decimal("25.00")
            rate = db_billing.rate_per_unit
            amount_due = total_quantity * rate
            
            usage_bill = UsageBill(
                usage_billing_id=db_billing.id,
                customer_id=db_billing.customer_id,
                bill_number=bill_number,
                billing_period_start=bill_start,
                billing_period_end=bill_end,
                total_usage_days=total_days,
                total_quantity_used=total_quantity,
                rate_per_unit=rate,
                amount_due=amount_due,
                previous_pending_balance=Decimal("0.00"),
                total_amount_to_collect=amount_due,
                status=UsageBillingStatus.PENDING,
                notes="Monthly usage billing"
            )
            db.add(usage_bill)
            
            db.flush()
            
            usage_payment = UsageBillPayment(
                usage_bill_id=usage_bill.id,
                customer_id=db_billing.customer_id,
                amount_paid=amount_due / 2,
                payment_date=base_date + timedelta(days=5),
                payment_mode="CASH",
                recorded_by_id=agent.id,
                notes="Partial payment"
            )
            db.add(usage_payment)
        
        db.commit()
        print(f"[OK] Created {len(billings)} usage-based billings with records and bills")
        return billings
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error creating usage billing: {e}")
        return []


def main():
    """Main seeding function"""
    db = SessionLocal()
    
    try:
        print("\n" + "="*60)
        print("PayLoop Database Seeding - Multi-Model Payment System")
        print("="*60 + "\n")
        
        clear_all_data(db)
        users = seed_users(db)
        customers = seed_customers(db, users)
        shops = seed_shops(db, customers)
        seed_payments(db, customers, shops, users)
        seed_loans(db, customers, users)
        seed_subscriptions(db, customers, users)
        seed_usage_billing(db, customers, users)
        
        print("\n" + "="*60)
        print("Seeding completed successfully!")
        print("="*60)
        print("\nTest Credentials:")
        print("-" * 60)
        print("Superadmin: username=superadmin, password=superadmin123")
        print("Admin:      username=admin, password=admin123")
        print("Agent 1:    username=agent1, password=agent123")
        print("Agent 2:    username=agent2, password=agent123")
        print("Agent 3:    username=agent3, password=agent123")
        print("-" * 60)
        print("\nPayment Types Configured:")
        print("-" * 60)
        print("Loan Customers: ABC Retail Store, Prime Distribution")
        print("Subscription Customers: XYZ Trading Co., Metro Trading House")
        print("Usage-Based Customers: Star Electronics, Smart Retail Ltd")
        print("-" * 60 + "\n")
        
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
