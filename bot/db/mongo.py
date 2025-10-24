"""MongoDB connection and database setup."""
import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from bot.config import MONGODB_URI, MONGODB_DB

logger = logging.getLogger(__name__)

# Global MongoDB client and database
client: AsyncIOMotorClient = None
database: AsyncIOMotorDatabase = None

async def init_mongodb() -> None:
    """Initialize MongoDB connection and create indexes."""
    global client, database
    
    try:
        client = AsyncIOMotorClient(MONGODB_URI)
        database = client[MONGODB_DB]
        
        # Test connection
        await client.admin.command('ping')
        logger.info("Connected to MongoDB successfully")
        
        # Create indexes
        await create_indexes()
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

async def create_indexes() -> None:
    """Create database indexes."""
    try:
        # Users collection indexes (_id is automatically indexed and unique)
        await database.users.create_index("referrer_id")
        
        # Referrals collection indexes
        await database.referrals.create_index([("referrer_id", 1), ("referred_user_id", 1)], unique=True)
        
        # Transactions collection indexes
        await database.transactions.create_index("user_id")
        await database.transactions.create_index("created_at")
        
        # ProcessImg collection indexes
        await database.process_img.create_index("chat_id")
        await database.process_img.create_index("status")
        await database.process_img.create_index("created_at")
        
        # BotJobsPhoto collection indexes
        await database.bot_jobs_photo.create_index("chat_id")
        await database.bot_jobs_photo.create_index("job_id", unique=True)
        await database.bot_jobs_photo.create_index("status")
        await database.bot_jobs_photo.create_index("created_at")
        
        # BotJobsVideo collection indexes
        await database.bot_jobs_video.create_index("chat_id")
        await database.bot_jobs_video.create_index("job_id", unique=True)
        await database.bot_jobs_video.create_index("status")
        await database.bot_jobs_video.create_index("created_at")
        
        logger.info("Database indexes created successfully")
        
    except Exception as e:
        logger.error(f"Failed to create indexes: {e}")
        raise

async def close_mongodb() -> None:
    """Close MongoDB connection."""
    global client
    if client:
        client.close()
        logger.info("MongoDB connection closed")

def get_database() -> AsyncIOMotorDatabase:
    """Get the database instance."""
    if database is None:
        raise RuntimeError("MongoDB not initialized. Call init_mongodb() first.")
    return database
