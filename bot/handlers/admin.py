"""Admin handler."""
import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from bot.config import ADMIN_IDS
from bot.db.repositories import UserRepository, ReferralRepository, NodeRepository
from bot.db.models import Node
from bot.utils.user import is_admin_user
from datetime import datetime, timezone
from bson import ObjectId

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("stats"))
async def admin_stats(message: Message) -> None:
    """Handle /stats command for admins."""
    user_id = message.from_user.id
    
    # Check if user is admin
    if not is_admin_user(user_id):
        await message.answer("You don't have permission to use this command.")
        return
    
    user_repo = UserRepository()
    referral_repo = ReferralRepository()
    
    try:
        # Get total user count
        total_users = await user_repo.collection.count_documents({})
        
        # Get total referrals
        total_referrals = await referral_repo.collection.count_documents({})
        
        # Get users with referrals
        users_with_referrals = await user_repo.collection.count_documents({"referral_count": {"$gt": 0}})
        
        stats_text = f"""📊 Bot Statistics

👥 Total Users: {total_users}
🔗 Total Referrals: {total_referrals}
👤 Users with Referrals: {users_with_referrals}"""
        
        await message.answer(stats_text)
        
    except Exception as e:
        logger.error(f"Error getting admin stats: {e}")
        await message.answer("Error retrieving statistics.")

@router.message(Command("nodes"))
async def admin_list_nodes(message: Message) -> None:
    """Handle /nodes command to list all dynamic buttons."""
    user_id = message.from_user.id
    
    # Check if user is admin
    if not is_admin_user(user_id):
        await message.answer("You don't have permission to use this command.")
        return
    
    node_repo = NodeRepository()
    
    try:
        nodes = await node_repo.get_all_nodes()
        
        if not nodes:
            await message.answer("No dynamic buttons found. Use /addnode to create one.")
            return
        
        nodes_text = "🎨 Dynamic Buttons:\n\n"
        for i, node in enumerate(nodes, 1):
            nodes_text += f"{i}. {node['node_name']}\n"
            nodes_text += f"   ID: {node['other_text']}\n"
            nodes_text += f"   Count: {node['count']}\n"
            nodes_text += f"   Created: {node['created_at'].strftime('%Y-%m-%d %H:%M')}\n\n"
        
        await message.answer(nodes_text)
        
    except Exception as e:
        logger.error(f"Error listing nodes: {e}")
        await message.answer("Error retrieving dynamic buttons.")

@router.message(Command("addnode"))
async def admin_add_node(message: Message) -> None:
    """Handle /addnode command to add a new dynamic button.
    Usage: /addnode "Button Name" "other_text"
    Example: /addnode "Lust Face" "q,2"
    """
    user_id = message.from_user.id
    
    # Check if user is admin
    if not is_admin_user(user_id):
        await message.answer("You don't have permission to use this command.")
        return
    
    try:
        # Parse command arguments
        args = message.text.split('"')[1::2]  # Extract text between quotes
        if len(args) != 2:
            await message.answer(
                "Usage: /addnode \"Button Name\" \"other_text\"\n"
                "Example: /addnode \"Lust Face\" \"q,2\""
            )
            return
        
        node_name = args[0].strip()
        other_text = args[1].strip()
        
        if not node_name or not other_text:
            await message.answer("Both button name and other_text are required.")
            return
        
        node_repo = NodeRepository()
        
        # Check if other_text already exists
        existing_node = await node_repo.get_node_by_other_text(other_text)
        if existing_node:
            await message.answer(f"Node with other_text '{other_text}' already exists.")
            return
        
        # Create new node
        node: Node = {
            "_id": ObjectId(),
            "node_name": node_name,
            "other_text": other_text,
            "count": 0,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        
        await node_repo.create_node(node)
        await message.answer(f"✅ Added new dynamic button: '{node_name}' with ID '{other_text}'")
        
    except Exception as e:
        logger.error(f"Error adding node: {e}")
        await message.answer("Error adding dynamic button. Check the format.")

@router.message(Command("delnode"))
async def admin_delete_node(message: Message) -> None:
    """Handle /delnode command to delete a dynamic button.
    Usage: /delnode "other_text"
    Example: /delnode "q,2"
    """
    user_id = message.from_user.id
    
    # Check if user is admin
    if not is_admin_user(user_id):
        await message.answer("You don't have permission to use this command.")
        return
    
    try:
        # Parse command arguments
        args = message.text.split('"')[1::2]  # Extract text between quotes
        if len(args) != 1:
            await message.answer(
                "Usage: /delnode \"other_text\"\n"
                "Example: /delnode \"q,2\""
            )
            return
        
        other_text = args[0].strip()
        
        if not other_text:
            await message.answer("other_text is required.")
            return
        
        node_repo = NodeRepository()
        
        # Check if node exists
        existing_node = await node_repo.get_node_by_other_text(other_text)
        if not existing_node:
            await message.answer(f"Node with other_text '{other_text}' not found.")
            return
        
        # Delete the node
        await node_repo.delete_node(existing_node["_id"])
        await message.answer(f"✅ Deleted dynamic button: '{existing_node['node_name']}' ({other_text})")
        
    except Exception as e:
        logger.error(f"Error deleting node: {e}")
        await message.answer("Error deleting dynamic button. Check the format.")


