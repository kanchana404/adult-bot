#!/usr/bin/env python3
"""Test script to debug admin functions and check database data."""

import asyncio
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables
load_dotenv("bot/.env")

# Import after loading env
from bot.db.mongo import init_mongodb, close_mongodb, get_database
from bot.db.repositories import UserRepository, PaymentRepository, CryptoInvoiceRepository, NodeRepository

async def test_admin_data():
    """Test admin data retrieval functions."""
    try:
        # Initialize MongoDB connection
        await init_mongodb()
        print("✅ Connected to MongoDB")
        
        # Test User Repository
        user_repo = UserRepository()
        total_users = await user_repo.collection.count_documents({})
        print(f"📊 Total Users: {total_users}")
        
        if total_users > 0:
            # Get a sample user
            sample_user = await user_repo.collection.find_one({})
            print(f"👤 Sample User: {sample_user}")
            
            # Test VIP users
            vip_users = await user_repo.collection.count_documents({"vip_tickets": {"$gt": 0}})
            print(f"⭐ VIP Users: {vip_users}")
            
            # Test active users
            today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
            active_users = await user_repo.collection.count_documents({"last_activity": {"$gte": today}})
            print(f"🔄 Active Today: {active_users}")
            
            # Test recent users
            recent_users = await user_repo.collection.count_documents({"created_at": {"$gte": today}})
            print(f"🆕 New Today: {recent_users}")
            
            # Test referrals
            users_with_referrals = await user_repo.collection.count_documents({"referral_count": {"$gt": 0}})
            print(f"🔗 Users with Referrals: {users_with_referrals}")
        
        # Test Payment Repository
        payment_repo = PaymentRepository()
        total_stars_payments = await payment_repo.collection.count_documents({"status": "paid"})
        print(f"⭐ Stars Payments: {total_stars_payments}")
        
        if total_stars_payments > 0:
            # Test aggregation
            total_stars_amount = await payment_repo.collection.aggregate([
                {"$match": {"status": "paid"}},
                {"$group": {"_id": None, "total": {"$sum": "$stars_amount"}}}
            ]).to_list(length=1)
            stars_total = total_stars_amount[0]["total"] if total_stars_amount else 0
            print(f"⭐ Stars Total: {stars_total}")
        
        # Test Crypto Repository
        crypto_repo = CryptoInvoiceRepository()
        total_crypto_payments = await crypto_repo.collection.count_documents({"status": "paid"})
        print(f"🪙 Crypto Payments: {total_crypto_payments}")
        
        if total_crypto_payments > 0:
            # Test aggregation
            total_crypto_amount = await crypto_repo.collection.aggregate([
                {"$match": {"status": "paid"}},
                {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
            ]).to_list(length=1)
            crypto_total = total_crypto_amount[0]["total"] if total_crypto_amount else 0
            print(f"🪙 Crypto Total: {crypto_total}")
        
        # Test Node Repository
        node_repo = NodeRepository()
        total_nodes = await node_repo.collection.count_documents({})
        print(f"🎨 Total Nodes: {total_nodes}")
        
        if total_nodes > 0:
            # Test aggregation
            total_button_usage = await node_repo.collection.aggregate([
                {"$group": {"_id": None, "total": {"$sum": "$count"}}}
            ]).to_list(length=1)
            total_usage = total_button_usage[0]["total"] if total_button_usage else 0
            print(f"🎨 Total Button Usage: {total_usage}")
            
            # Get most popular button
            most_popular = await node_repo.collection.find_one({}, sort=[("count", -1)])
            if most_popular:
                print(f"🏆 Most Popular Button: {most_popular['node_name']} ({most_popular['count']} uses)")
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close MongoDB connection
        await close_mongodb()
        print("🔌 Disconnected from MongoDB")

if __name__ == "__main__":
    asyncio.run(test_admin_data())
