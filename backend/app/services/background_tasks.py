# app/services/background_tasks.py
# Importing necessary modules
import asyncio
import time
from app.services.chat.context_manager import ChatContextManager

async def cleanup_conversation_histories(context_manager: ChatContextManager, max_age: int):
    # This coroutine function periodically cleans up conversation histories that are older than a specified age
    while True:  # Continuously run this cleanup process
        current_time = time.time()  # Get the current time in seconds since the epoch
        for user_id in context_manager.conversation_history:
            # Filter and retain messages in the conversation history that are within the max_age
            context_manager.conversation_history[user_id] = [
                (msg, ts) for msg, ts in context_manager.conversation_history[user_id]
                if current_time - ts <= max_age
            ]
        await asyncio.sleep(3600)  # Pause the coroutine for one hour before next iteration

async def start_background_tasks(context_manager: ChatContextManager):
    # This function starts the background task for cleaning up conversation histories
    max_age = 24 * 60 * 60  # Set maximum age of conversation history to keep (24 hours in seconds)
    asyncio.create_task(cleanup_conversation_histories(context_manager, max_age))  # Create and start the cleanup task
