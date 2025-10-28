#!/usr/bin/env python3
"""Script to initialize sample dynamic button nodes for testing."""

import asyncio
import os
from datetime import datetime, timezone
from bson import ObjectId
from dotenv import load_dotenv

# Load environment variables
load_dotenv("bot/.env")

# Import after loading env
from bot.db.mongo import init_mongodb, close_mongodb, get_database
from bot.db.models import Node

async def init_sample_nodes():
    """Initialize sample nodes in the database."""
    try:
        # Initialize MongoDB connection
        await init_mongodb()
        print("Connected to MongoDB")
        
        # Get the node collection
        db = get_database()
        node_collection = db.node
        
        # Sample nodes based on the image description
        sample_nodes = [
            {
                "_id": ObjectId(),
                "node_name": "Lust Face",
                "other_text": "q,2",
                "count": 0,
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc)
            },
            {
                "_id": ObjectId(),
                "node_name": "Moonlight Seduction",
                "other_text": "a,1",
                "count": 0,
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc)
            },
            {
                "_id": ObjectId(),
                "node_name": "Succubus Tattoo",
                "other_text": "s,3",
                "count": 0,
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc)
            },
            {
                "_id": ObjectId(),
                "node_name": "Infernal Body Art",
                "other_text": "i,4",
                "count": 0,
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc)
            },
            {
                "_id": ObjectId(),
                "node_name": "Obsidian Skinwear",
                "other_text": "o,5",
                "count": 0,
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc)
            }
        ]
        
        # Clear existing nodes (optional)
        await node_collection.delete_many({})
        print("Cleared existing nodes")
        
        # Insert sample nodes
        result = await node_collection.insert_many(sample_nodes)
        print(f"Inserted {len(result.inserted_ids)} sample nodes")
        
        # Verify insertion
        count = await node_collection.count_documents({})
        print(f"Total nodes in database: {count}")
        
        # List all nodes
        nodes = await node_collection.find({}).to_list(length=None)
        print("\nSample nodes created:")
        for node in nodes:
            print(f"- {node['node_name']} (ID: {node['other_text']})")
        
    except Exception as e:
        print(f"Error initializing sample nodes: {e}")
    finally:
        # Close MongoDB connection
        await close_mongodb()
        print("Disconnected from MongoDB")

if __name__ == "__main__":
    asyncio.run(init_sample_nodes())
