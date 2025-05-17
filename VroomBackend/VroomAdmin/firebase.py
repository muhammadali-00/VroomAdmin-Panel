from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("/home/mikealpha/Downloads/vroom-9bd63-firebase-adminsdk-fbsvc-1bae427737.json")
firebase_admin.initialize_app(cred)

from VroomBackend.VroomAdmin.APIs.drivers_api import router as drivers_router  # ✅ Now it's safe
from VroomBackend.VroomAdmin.APIs.admin_roles_api import adminroles_router as adminroles_router
from VroomBackend.VroomAdmin.APIs.admin_users_api import router as adminuser_router
from VroomBackend.VroomAdmin.APIs.rider_api import router as rider_router
from VroomBackend.VroomAdmin.APIs.rides_api import router as rides_router
from VroomBackend.VroomAdmin.APIs.transactions_api import router as transactions_router
from VroomBackend.VroomAdmin.APIs.riderWallet_api import router as riderwallet_router
from VroomBackend.VroomAdmin.APIs.driverWallet_api import router as driverWallet_router
from VroomBackend.VroomAdmin.APIs.payments_api import router as payments_router
from VroomBackend.VroomAdmin.APIs.pricing_and_zones_api import router as pricing_and_zones_roiter
from VroomBackend.VroomAdmin.APIs.promotions import router as promotions_router
from VroomBackend.VroomAdmin.APIs.complain_and_support_tickets_api import router as complainandSupportTickets_router
from VroomBackend.VroomAdmin.APIs.notifications_api import router as notifications_router
from VroomBackend.VroomAdmin.APIs.driver_Onboarding_Queue_api import router as  driverOnboardingQueue_router

app = FastAPI()

# Register routers
app.include_router(drivers_router, prefix="/drivers", tags=["Drivers"])
app.include_router(adminroles_router, prefix="/admin-roles", tags=["Admin Roles"])
app.include_router(adminuser_router, prefix="/admin-users", tags=["Admin Users"])
app.include_router(rider_router, prefix="/rider", tags=["Riders"])
app.include_router(rides_router, prefix="/rides", tags=["Rides"])
app.include_router(transactions_router, prefix="/transactions", tags=["Transactions"])
app.include_router(riderwallet_router,prefix="/rider-wallet", tags=["Rider Wallet"])
app.include_router(driverWallet_router,prefix="/driver-wallet", tags=["Driver Wallet"])
app.include_router(payments_router, prefix="/payments", tags=["Payments"])
app.include_router(pricing_and_zones_roiter,prefix="/pricing-and-zones", tags=["Pricing and Zones"])
app.include_router(promotions_router, prefix="/promotions", tags=["Promotions"])
app.include_router(complainandSupportTickets_router, prefix="/complain-and-support-tickets", tags=["Complain and Support Tickets"])
app.include_router(notifications_router, prefix="/notifications", tags=["Notifications"])
app.include_router(driverOnboardingQueue_router, prefix="/driverOnboardingQueue", tags=["Driver Onboarding Queue"])