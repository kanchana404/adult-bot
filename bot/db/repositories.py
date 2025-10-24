"""Repository layer for database operations."""
from typing import Optional, List
from datetime import datetime, timezone
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from bot.db.mongo import get_database
from bot.db.models import User, Referral, Transaction, Payment, CryptoInvoice, UnifiedPaymentHistory, ProcessImg, BotJobsPhoto, BotJobsVideo

class UserRepository:
    """Repository for user operations."""
    
    def __init__(self):
        self.collection: AsyncIOMotorCollection = get_database().users
    
    async def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return await self.collection.find_one({"_id": user_id})
    
    async def create_user(self, user: User) -> None:
        """Create a new user."""
        await self.collection.insert_one(user)
    
    async def update_user(self, user_id: int, update_data: dict) -> None:
        """Update user data."""
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Repository: Updating user {user_id} with data: {update_data}")
        
        result = await self.collection.update_one({"_id": user_id}, {"$set": update_data})
        logger.info(f"Repository: Update result: {result}")
    
    async def increment_referral_count(self, user_id: int) -> None:
        """Increment user's referral count."""
        await self.collection.update_one(
            {"_id": user_id}, 
            {"$inc": {"referral_count": 1}}
        )
    
    async def add_referral_tickets(self, user_id: int, tickets: str) -> None:
        """Add tickets to user's referral earnings."""
        # Get current user to calculate new referral_ticket_earned
        user = await self.get_user(user_id)
        if user:
            current_earned = float(user["referral_ticket_earned"])
            new_earned = current_earned + float(tickets)
            
            await self.collection.update_one(
                {"_id": user_id}, 
                {"$inc": {"tickets": 1}, "$set": {"referral_ticket_earned": str(new_earned)}}
            )
    
    async def increment_tickets(self, user_id: int, amount: int) -> None:
        """Increment user's tickets."""
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Repository: Incrementing {amount} tickets for user {user_id}")
        
        result = await self.collection.update_one(
            {"_id": user_id}, 
            {"$inc": {"tickets": amount}}
        )
        logger.info(f"Repository: Update result: {result}")
    
    async def update_last_activity(self, user_id: int) -> None:
        """Update user's last activity timestamp."""
        await self.collection.update_one(
            {"_id": user_id}, 
            {"$set": {"last_activity": datetime.now(timezone.utc)}}
        )

class ReferralRepository:
    """Repository for referral operations."""
    
    def __init__(self):
        self.collection: AsyncIOMotorCollection = get_database().referrals
    
    async def create_referral(self, referrer_id: int, referred_user_id: int) -> None:
        """Create a referral record."""
        referral: Referral = {
            "_id": ObjectId(),
            "referrer_id": referrer_id,
            "referred_user_id": referred_user_id,
            "created_at": datetime.now(timezone.utc)
        }
        await self.collection.insert_one(referral)
    
    async def get_referral_count(self, user_id: int) -> int:
        """Get referral count for a user."""
        return await self.collection.count_documents({"referrer_id": user_id})
    
    async def check_referral_exists(self, referrer_id: int, referred_user_id: int) -> bool:
        """Check if referral already exists."""
        return await self.collection.find_one({
            "referrer_id": referrer_id,
            "referred_user_id": referred_user_id
        }) is not None

class TransactionRepository:
    """Repository for transaction operations."""
    
    def __init__(self):
        self.collection: AsyncIOMotorCollection = get_database().transactions
    
    async def create_transaction(self, transaction: Transaction) -> None:
        """Create a new transaction."""
        await self.collection.insert_one(transaction)
    
    async def get_user_transactions(self, user_id: int, limit: int = 100) -> List[Transaction]:
        """Get user's transactions."""
        cursor = self.collection.find({"user_id": user_id}).sort("created_at", -1).limit(limit)
        return await cursor.to_list(length=limit)

class PaymentRepository:
    """Repository for payment operations."""
    
    def __init__(self):
        self.collection: AsyncIOMotorCollection = get_database().payments
    
    async def create_payment(self, payment: Payment) -> None:
        """Create a new payment record."""
        await self.collection.insert_one(payment)
    
    async def get_payment_by_payload(self, payload: str) -> Optional[Payment]:
        """Get payment by payload."""
        return await self.collection.find_one({"payload": payload})
    
    async def update_payment_status(self, payload: str, telegram_payment_id: str) -> None:
        """Mark payment as paid."""
        await self.collection.update_one(
            {"payload": payload},
            {
                "$set": {
                    "status": "paid",
                    "paid_at": datetime.now(timezone.utc),
                    "telegram_payment_id": telegram_payment_id
                }
            }
        )
    
    async def get_user_payments(self, user_id: int, limit: int = 50) -> List[Payment]:
        """Get user's payment history."""
        cursor = self.collection.find({"user_id": user_id}).sort("created_at", -1).limit(limit)
        return await cursor.to_list(length=limit)
    
    async def cancel_payment(self, payload: str) -> None:
        """Cancel a payment."""
        await self.collection.update_one(
            {"payload": payload},
            {"$set": {"status": "cancelled"}}
        )

class CryptoInvoiceRepository:
    """Repository for crypto invoice operations."""
    
    def __init__(self):
        self.collection: AsyncIOMotorCollection = get_database().crypto_invoices
    
    async def create_invoice(self, invoice: CryptoInvoice) -> None:
        """Create a new crypto invoice record."""
        await self.collection.insert_one(invoice)
    
    async def get_invoice_by_id(self, invoice_id: str) -> Optional[CryptoInvoice]:
        """Get invoice by invoice ID."""
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Repository: Looking for invoice with ID: {invoice_id} (type: {type(invoice_id)})")
        
        result = await self.collection.find_one({"invoice_id": invoice_id})
        logger.info(f"Repository: Query result: {result}")
        
        return result
    
    async def update_invoice_status(self, invoice_id: str, status: str) -> None:
        """Update invoice status."""
        update_data = {"status": status}
        if status == "paid":
            update_data["paid_at"] = datetime.now(timezone.utc)
        
        await self.collection.update_one(
            {"invoice_id": invoice_id},
            {"$set": update_data}
        )
    
    async def get_user_invoices(self, user_id: int, limit: int = 50) -> List[CryptoInvoice]:
        """Get user's crypto invoice history."""
        cursor = self.collection.find({"user_id": user_id}).sort("created_at", -1).limit(limit)
        return await cursor.to_list(length=limit)
    
    async def cancel_invoice(self, invoice_id: str) -> None:
        """Cancel an invoice."""
        await self.collection.update_one(
            {"invoice_id": invoice_id},
            {"$set": {"status": "cancelled"}}
        )

class UnifiedPaymentHistoryRepository:
    """Repository for unified payment history operations."""
    
    def __init__(self):
        self.collection: AsyncIOMotorCollection = get_database().unified_payment_history
    
    async def create_payment_record(self, payment: UnifiedPaymentHistory) -> None:
        """Create a new unified payment record."""
        await self.collection.insert_one(payment)
    
    async def get_user_payment_history(
        self, 
        user_id: int, 
        page: int = 1, 
        per_page: int = 3
    ) -> tuple[List[UnifiedPaymentHistory], int]:
        """Get user's payment history with pagination."""
        skip = (page - 1) * per_page
        
        # Get total count
        total_count = await self.collection.count_documents({"user_id": user_id})
        
        # Get paginated results
        cursor = self.collection.find({"user_id": user_id}).sort("created_at", -1).skip(skip).limit(per_page)
        payments = await cursor.to_list(length=per_page)
        
        return payments, total_count
    
    async def get_payment_by_id(self, payment_id: str, payment_type: str) -> Optional[UnifiedPaymentHistory]:
        """Get payment by payment ID and type."""
        return await self.collection.find_one({
            "payment_id": payment_id,
            "payment_type": payment_type
        })

class ProcessImgRepository:
    """Repository for process image operations."""
    
    def __init__(self):
        self.collection: AsyncIOMotorCollection = get_database().process_img
    
    async def create_job(self, job: ProcessImg) -> ObjectId:
        """Create a new process image job."""
        result = await self.collection.insert_one(job)
        return result.inserted_id
    
    async def get_job(self, job_id: ObjectId) -> Optional[ProcessImg]:
        """Get process image job by ID."""
        return await self.collection.find_one({"_id": job_id})
    
    async def update_status(self, job_id: ObjectId, status: str, output_url: Optional[str] = None, time_taken: Optional[float] = None) -> None:
        """Update job status and optional output data."""
        update_data = {"status": status}
        if output_url is not None:
            update_data["output_url"] = output_url
        if time_taken is not None:
            update_data["time_taken"] = time_taken
        
        await self.collection.update_one({"_id": job_id}, {"$set": update_data})

class BotJobsPhotoRepository:
    """Repository for photo swap job operations."""
    
    def __init__(self):
        self.collection: AsyncIOMotorCollection = get_database().bot_jobs_photo
    
    async def create_job(self, job: BotJobsPhoto) -> str:
        """Create a new photo swap job and return job_id."""
        result = await self.collection.insert_one(job)
        return job["job_id"]
    
    async def get_job_by_chat_id(self, chat_id: str) -> Optional[BotJobsPhoto]:
        """Get photo swap job by chat ID."""
        return await self.collection.find_one({"chat_id": chat_id, "status": "pending"})
    
    async def update_target_photo(self, chat_id: str, target_photo_url: str) -> None:
        """Update job with target photo URL and set status to review."""
        await self.collection.update_one(
            {"chat_id": chat_id, "status": "pending"},
            {
                "$set": {
                    "target_photo_url": target_photo_url,
                    "status": "review"
                }
            }
        )
    
    async def update_status(self, chat_id: str, status: str, output_url: Optional[str] = None, time_taken: Optional[float] = None) -> None:
        """Update job status and optional output data."""
        update_data = {"status": status}
        if output_url is not None:
            update_data["output_url"] = output_url
        if time_taken is not None:
            update_data["time_taken"] = time_taken
        
        await self.collection.update_one({"chat_id": chat_id}, {"$set": update_data})

class BotJobsVideoRepository:
    """Repository for video swap job operations."""
    
    def __init__(self):
        self.collection: AsyncIOMotorCollection = get_database().bot_jobs_video
    
    async def create_job(self, job: BotJobsVideo) -> str:
        """Create a new video swap job and return job_id."""
        result = await self.collection.insert_one(job)
        return job["job_id"]
    
    async def get_job_by_id(self, job_id: str) -> Optional[BotJobsVideo]:
        """Get video swap job by job ID."""
        return await self.collection.find_one({"job_id": job_id})
    
    async def get_video_by_id(self, video_id: str) -> Optional[dict]:
        """Get video data by video ID for deep link lookup."""
        return await self.collection.find_one({"job_id": video_id})
    
    async def update_status(self, job_id: str, status: str, output_url: Optional[str] = None, time_taken: Optional[float] = None) -> None:
        """Update job status and optional output data."""
        update_data = {"status": status}
        if output_url is not None:
            update_data["output_url"] = output_url
        if time_taken is not None:
            update_data["time_taken"] = time_taken
        
        await self.collection.update_one({"job_id": job_id}, {"$set": update_data})

