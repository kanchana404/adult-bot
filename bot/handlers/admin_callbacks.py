"""Admin callback handlers for the bot."""
import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery
from datetime import datetime, timezone
from bot.db.repositories import UserRepository, NodeRepository, PaymentRepository, CryptoInvoiceRepository, UnifiedPaymentHistoryRepository
from bot.admin_keyboards import kb_admin_menu, kb_button_management
from bot.utils.user import is_admin_user

logger = logging.getLogger(__name__)
router = Router()

@router.callback_query(F.data == "admin_user_status")
async def admin_user_status(callback: CallbackQuery) -> None:
    """Handle admin user status callback."""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if not is_admin_user(user_id):
        await callback.answer("You don't have permission to use this feature.")
        return
    
    user_repo = UserRepository()
    
    try:
        # Get user statistics
        total_users = await user_repo.collection.count_documents({})
        logger.info(f"Admin user status - Total users: {total_users}")
        
        vip_users = await user_repo.collection.count_documents({"vip_tickets": {"$gt": 0}})
        logger.info(f"Admin user status - VIP users: {vip_users}")
        
        active_users = await user_repo.collection.count_documents({"last_activity": {"$gte": datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)}})
        logger.info(f"Admin user status - Active users: {active_users}")
        
        # Get recent users (last 24 hours)
        yesterday = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        recent_users = await user_repo.collection.count_documents({"created_at": {"$gte": yesterday}})
        logger.info(f"Admin user status - Recent users: {recent_users}")
        
        # Get users with referrals
        users_with_referrals = await user_repo.collection.count_documents({"referral_count": {"$gt": 0}})
        logger.info(f"Admin user status - Users with referrals: {users_with_referrals}")
        
        # Calculate percentages safely
        vip_percentage = (vip_users/total_users*100) if total_users > 0 else 0
        active_percentage = (active_users/total_users*100) if total_users > 0 else 0
        referral_percentage = (users_with_referrals/total_users*100) if total_users > 0 else 0
        growth_rate = (recent_users/total_users*100) if total_users > 0 else 0
        
        status_text = f"""👥 <b>USER STATUS REPORT</b>

📊 <b>Total Statistics:</b>
• Total Users: {total_users:,}
• VIP Users: {vip_users:,}
• Active Today: {active_users:,}
• New Today: {recent_users:,}
• Users with Referrals: {users_with_referrals:,}

📈 <b>User Distribution:</b>
• VIP Percentage: {vip_percentage:.1f}%
• Active Percentage: {active_percentage:.1f}%
• Referral Percentage: {referral_percentage:.1f}%

🔄 <b>Growth Metrics:</b>
• New Users Today: {recent_users:,}
• Daily Growth Rate: {growth_rate:.2f}%"""
        
        await callback.message.edit_caption(
            caption=status_text,
            reply_markup=kb_admin_menu()
        )
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error getting user status: {e}")
        await callback.answer("Error retrieving user status.")

@router.callback_query(F.data == "admin_revenue_status")
async def admin_revenue_status(callback: CallbackQuery) -> None:
    """Handle admin revenue status callback."""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if not is_admin_user(user_id):
        await callback.answer("You don't have permission to use this feature.")
        return
    
    try:
        # Get payment statistics
        payment_repo = PaymentRepository()
        crypto_repo = CryptoInvoiceRepository()
        unified_repo = UnifiedPaymentHistoryRepository()
        
        # Telegram Stars payments
        total_stars_payments = await payment_repo.collection.count_documents({"status": "paid"})
        logger.info(f"Admin revenue status - Stars payments: {total_stars_payments}")
        
        total_stars_amount = await payment_repo.collection.aggregate([
            {"$match": {"status": "paid"}},
            {"$group": {"_id": None, "total": {"$sum": "$stars_amount"}}}
        ]).to_list(length=1)
        stars_total = total_stars_amount[0]["total"] if total_stars_amount else 0
        logger.info(f"Admin revenue status - Stars total: {stars_total}")
        
        # Crypto payments
        total_crypto_payments = await crypto_repo.collection.count_documents({"status": "paid"})
        logger.info(f"Admin revenue status - Crypto payments: {total_crypto_payments}")
        
        total_crypto_amount = await crypto_repo.collection.aggregate([
            {"$match": {"status": "paid"}},
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ]).to_list(length=1)
        crypto_total = total_crypto_amount[0]["total"] if total_crypto_amount else 0
        logger.info(f"Admin revenue status - Crypto total: {crypto_total}")
        
        # Total tickets sold
        total_tickets_stars = await payment_repo.collection.aggregate([
            {"$match": {"status": "paid"}},
            {"$group": {"_id": None, "total": {"$sum": "$tickets_amount"}}}
        ]).to_list(length=1)
        tickets_from_stars = total_tickets_stars[0]["total"] if total_tickets_stars else 0
        
        total_tickets_crypto = await crypto_repo.collection.aggregate([
            {"$match": {"status": "paid"}},
            {"$group": {"_id": None, "total": {"$sum": "$tickets_amount"}}}
        ]).to_list(length=1)
        tickets_from_crypto = total_tickets_crypto[0]["total"] if total_tickets_crypto else 0
        
        # Today's revenue
        today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        today_stars = await payment_repo.collection.count_documents({"status": "paid", "paid_at": {"$gte": today}})
        today_crypto = await crypto_repo.collection.count_documents({"status": "paid", "paid_at": {"$gte": today}})
        
        # Calculate percentages safely
        total_payments = total_stars_payments + total_crypto_payments
        stars_percentage = (total_stars_payments/total_payments*100) if total_payments > 0 else 0
        crypto_percentage = (total_crypto_payments/total_payments*100) if total_payments > 0 else 0
        
        revenue_text = f"""💰 <b>REVENUE STATUS REPORT</b>

⭐ <b>Telegram Stars:</b>
• Total Payments: {total_stars_payments:,}
• Total Stars: {stars_total:,}
• Tickets Sold: {tickets_from_stars:,}
• Today's Payments: {today_stars:,}

🪙 <b>Crypto Payments:</b>
• Total Payments: {total_crypto_payments:,}
• Total Amount: {crypto_total:.2f}
• Tickets Sold: {tickets_from_crypto:,}
• Today's Payments: {today_crypto:,}

📊 <b>Summary:</b>
• Total Payments: {total_payments:,}
• Total Tickets Sold: {tickets_from_stars + tickets_from_crypto:,}
• Today's Total: {today_stars + today_crypto:,}

💡 <b>Payment Methods:</b>
• Stars: {stars_percentage:.1f}%
• Crypto: {crypto_percentage:.1f}%"""
        
        await callback.message.edit_caption(
            caption=revenue_text,
            reply_markup=kb_admin_menu()
        )
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error getting revenue status: {e}")
        await callback.answer("Error retrieving revenue status.")

@router.callback_query(F.data == "admin_button_management")
async def admin_button_management(callback: CallbackQuery) -> None:
    """Handle admin button management callback."""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if not is_admin_user(user_id):
        await callback.answer("You don't have permission to use this feature.")
        return
    
    management_text = """🎨 <b>BUTTON MANAGEMENT</b>

Manage dynamic style selection buttons:

📋 <b>Available Actions:</b>
• List All Buttons - View all current buttons
• Add New Button - Create a new style button
• Delete Button - Remove an existing button
• Button Stats - View usage statistics

💡 <b>Commands:</b>
• /nodes - List all buttons
• /addnode "Name" "ID" - Add button
• /delnode "ID" - Delete button

Use the buttons below or commands to manage buttons."""
    
    await callback.message.edit_caption(
        caption=management_text,
        reply_markup=kb_button_management()
    )
    await callback.answer()

@router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery) -> None:
    """Handle admin stats callback."""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if not is_admin_user(user_id):
        await callback.answer("You don't have permission to use this feature.")
        return
    
    user_repo = UserRepository()
    node_repo = NodeRepository()
    
    try:
        # Get comprehensive statistics
        total_users = await user_repo.collection.count_documents({})
        total_nodes = await node_repo.collection.count_documents({})
        
        # Get total button usage
        total_button_usage = await node_repo.collection.aggregate([
            {"$group": {"_id": None, "total": {"$sum": "$count"}}}
        ]).to_list(length=1)
        total_usage = total_button_usage[0]["total"] if total_button_usage else 0
        
        # Get most popular button
        most_popular = await node_repo.collection.find_one({}, sort=[("count", -1)])
        
        # Get total referrals safely
        total_referrals_result = await user_repo.collection.aggregate([
            {"$group": {"_id": None, "total": {"$sum": "$referral_count"}}}
        ]).to_list(length=1)
        total_referrals = total_referrals_result[0]["total"] if total_referrals_result else 0
        
        # Calculate metrics safely
        avg_usage_per_button = (total_usage/total_nodes) if total_nodes > 0 else 0
        usage_per_user = (total_usage/total_users) if total_users > 0 else 0
        
        stats_text = f"""📊 <b>COMPREHENSIVE BOT STATISTICS</b>

👥 <b>User Statistics:</b>
• Total Users: {total_users:,}
• Total Referrals: {total_referrals:,}

🎨 <b>Button Statistics:</b>
• Total Buttons: {total_nodes:,}
• Total Usage: {total_usage:,}
• Most Popular: {most_popular["node_name"] if most_popular else "N/A"} ({most_popular["count"] if most_popular else 0} uses)

📈 <b>Performance Metrics:</b>
• Average Usage per Button: {avg_usage_per_button:.1f}
• Usage per User: {usage_per_user:.1f}

🔄 <b>System Health:</b>
• Database Collections: Active
• Admin Commands: Available
• Dynamic Buttons: Enabled"""
        
        await callback.message.edit_caption(
            caption=stats_text,
            reply_markup=kb_admin_menu()
        )
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error getting comprehensive stats: {e}")
        await callback.answer("Error retrieving statistics.")

@router.callback_query(F.data == "admin_list_buttons")
async def admin_list_buttons(callback: CallbackQuery) -> None:
    """Handle admin list buttons callback."""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if not is_admin_user(user_id):
        await callback.answer("You don't have permission to use this feature.")
        return
    
    node_repo = NodeRepository()
    
    try:
        nodes = await node_repo.get_all_nodes()
        
        if not nodes:
            buttons_text = "📋 <b>DYNAMIC BUTTONS</b>\n\nNo buttons found. Use /addnode to create one."
        else:
            buttons_text = "📋 <b>DYNAMIC BUTTONS</b>\n\n"
            for i, node in enumerate(nodes, 1):
                buttons_text += f"{i}. <b>{node['node_name']}</b>\n"
                buttons_text += f"   ID: <code>{node['other_text']}</code>\n"
                buttons_text += f"   Usage: {node['count']:,} times\n"
                buttons_text += f"   Created: {node['created_at'].strftime('%Y-%m-%d')}\n\n"
        
        await callback.message.edit_caption(
            caption=buttons_text,
            reply_markup=kb_button_management()
        )
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error listing buttons: {e}")
        await callback.answer("Error retrieving buttons.")

@router.callback_query(F.data == "admin_button_stats")
async def admin_button_stats(callback: CallbackQuery) -> None:
    """Handle admin button stats callback."""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if not is_admin_user(user_id):
        await callback.answer("You don't have permission to use this feature.")
        return
    
    node_repo = NodeRepository()
    
    try:
        nodes = await node_repo.get_all_nodes()
        
        if not nodes:
            stats_text = "📈 <b>BUTTON STATISTICS</b>\n\nNo buttons found."
        else:
            total_usage = sum(node["count"] for node in nodes)
            most_popular = max(nodes, key=lambda x: x["count"])
            least_popular = min(nodes, key=lambda x: x["count"])
            
            stats_text = f"""📈 <b>BUTTON STATISTICS</b>

📊 <b>Overall Stats:</b>
• Total Buttons: {len(nodes):,}
• Total Usage: {total_usage:,}
• Average Usage: {total_usage/len(nodes):.1f}

🏆 <b>Top Performers:</b>
• Most Popular: {most_popular["node_name"]} ({most_popular["count"]:,} uses)
• Least Popular: {least_popular["node_name"]} ({least_popular["count"]:,} uses)

📈 <b>Usage Distribution:</b>
• High Usage (>100): {len([n for n in nodes if n["count"] > 100]):,}
• Medium Usage (10-100): {len([n for n in nodes if 10 <= n["count"] <= 100]):,}
• Low Usage (<10): {len([n for n in nodes if n["count"] < 10]):,}"""
        
        await callback.message.edit_caption(
            caption=stats_text,
            reply_markup=kb_button_management()
        )
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error getting button stats: {e}")
        await callback.answer("Error retrieving button statistics.")

@router.callback_query(F.data == "admin_menu")
async def admin_menu(callback: CallbackQuery) -> None:
    """Handle admin menu callback."""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if not is_admin_user(user_id):
        await callback.answer("You don't have permission to use this feature.")
        return
    
    menu_text = """🔧 <b>ADMIN PANEL</b>

Welcome to the Admin Control Panel!

🎛️ <b>Available Features:</b>
• User Status - View user analytics and statistics
• Revenue Status - Track payment and revenue data
• Button Management - Manage dynamic style buttons
• Bot Statistics - Comprehensive system overview

Use the buttons below to access different admin functions."""
    
    await callback.message.edit_caption(
        caption=menu_text,
        reply_markup=kb_admin_menu()
    )
    await callback.answer()

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery) -> None:
    """Handle back to main menu callback."""
    user_id = callback.from_user.id
    
    # Get user data to show appropriate menu
    user_repo = UserRepository()
    user = await user_repo.get_user(user_id)
    user_language = user.get("language", "en") if user else "en"
    
    if is_admin_user(user_id):
        # Show admin menu
        menu_text = """🔧 <b>ADMIN PANEL</b>

Welcome to the Admin Control Panel!

🎛️ <b>Available Features:</b>
• User Status - View user analytics and statistics
• Revenue Status - Track payment and revenue data
• Button Management - Manage dynamic style buttons
• Bot Statistics - Comprehensive system overview

Use the buttons below to access different admin functions."""
        
        await callback.message.edit_caption(
            caption=menu_text,
            reply_markup=kb_admin_menu()
        )
    else:
        # Show regular menu
        from bot.keyboards import kb_main_menu
        from bot.languages import get_text
        
        menu_text = get_text(user_language, "main_menu.welcome")
        
        await callback.message.edit_caption(
            caption=menu_text,
            reply_markup=kb_main_menu(user_language)
        )
    
    await callback.answer()

@router.callback_query(F.data == "admin_add_button")
async def admin_add_button(callback: CallbackQuery) -> None:
    """Handle admin add button callback."""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if not is_admin_user(user_id):
        await callback.answer("You don't have permission to use this feature.")
        return
    
    add_text = """➕ <b>ADD NEW BUTTON</b>

To add a new dynamic button, use the command:

<code>/addnode "Button Name" "ID"</code>

📝 <b>Examples:</b>
• <code>/addnode "Lust Face" "q,2"</code>
• <code>/addnode "Moonlight Seduction" "a,1"</code>
• <code>/addnode "Succubus Tattoo" "s,3"</code>

💡 <b>Tips:</b>
• Button Name: Display text shown to users
• ID: Unique identifier (use format like "q,2", "a,1")
• Make sure the ID is unique and not already used

After adding, the button will appear in the style selection menu."""
    
    await callback.message.edit_caption(
        caption=add_text,
        reply_markup=kb_button_management()
    )
    await callback.answer()

@router.callback_query(F.data == "admin_delete_button")
async def admin_delete_button(callback: CallbackQuery) -> None:
    """Handle admin delete button callback."""
    user_id = callback.from_user.id
    
    # Check if user is admin
    if not is_admin_user(user_id):
        await callback.answer("You don't have permission to use this feature.")
        return
    
    delete_text = """🗑️ <b>DELETE BUTTON</b>

To delete a dynamic button, use the command:

<code>/delnode "ID"</code>

📝 <b>Examples:</b>
• <code>/delnode "q,2"</code>
• <code>/delnode "a,1"</code>
• <code>/delnode "s,3"</code>

⚠️ <b>Warning:</b>
• This action cannot be undone
• The button will be permanently removed
• Usage statistics will be lost

💡 <b>Tip:</b>
Use /nodes command to see all available button IDs before deleting."""
    
    await callback.message.edit_caption(
        caption=delete_text,
        reply_markup=kb_button_management()
    )
    await callback.answer()
