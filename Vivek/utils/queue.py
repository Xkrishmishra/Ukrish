import os
from asyncio import Queue as AsyncQueue
from asyncio import QueueEmpty
from typing import Any, Dict, List, Optional

from .functions import MelodyError


class QueueManager:

    def __init__(self):
        self.queues: Dict[int, AsyncQueue] = {}

    async def add(self, chat_id: int, **params: Any):
        """Asynchronously add a set of parameters to the queue for a given chat_id."""
        if chat_id not in self.queues:
            self.queues[chat_id] = AsyncQueue()
        await self.queues[chat_id].put(params)

    async def get(self, chat_id: int) -> Optional[Dict[str, Any]]:
        """Asynchronously return the first stored item for the given chat_id without removing it."""
        if chat_id in self.queues and not self.queues[chat_id].empty():
            first_item = await self.queues[chat_id].get()
            await self.queues[chat_id].put(first_item)

            for _ in range(self.queues[chat_id].qsize() - 1):
                item = await self.queues[chat_id].get()
                await self.queues[chat_id].put(item)
            return first_item
        return None

    async def remove(self, chat_id: int) -> Optional[Dict[str, Any]]:
        """Asynchronously remove the first set of parameters for the given chat_id, and delete file if file_path exists."""
        if chat_id in self.queues:
            try:
                params = await self.queues[chat_id].get()
                file_path = params.get("file_path")
                if file_path and os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except:
                        pass
                return params
            except QueueEmpty:
                raise MelodyError(f"No parameters to remove for chat_id {chat_id}")
        else:
            raise MelodyError(f"No queue found for chat_id {chat_id}")

    async def next(self, chat_id: int) -> Optional[Dict[str, Any]]:
        """Asynchronously remove the first item and return the next item in the queue."""
        await self.remove(chat_id)
        return await self.get(chat_id)

    async def clear(self, chat_id: int):
        """Asynchronously clear the entire queue for a given chat_id, deleting files if file_path exists."""
        if chat_id in self.queues:
            while not self.queues[chat_id].empty():
                try:
                    params = await self.queues[chat_id].get()
                    file_path = params.get("file_path")
                    if file_path and os.path.exists(file_path):
                        try:
                            os.remove(file_path)
                        except:
                            pass
                except QueueEmpty:
                    break
            self.queues.pop(chat_id, None)

    async def has(self, chat_id: int) -> bool:
        """Check asynchronously if there is a queue for a given chat_id."""
        return chat_id in self.queues and not self.queues[chat_id].empty()

    async def get_queues(self, chat_id: int) -> List[Dict[str, Any]]:
        """Asynchronously return all items in the queue for the given chat_id without removing any."""
        items = []
        if chat_id in self.queues and not self.queues[chat_id].empty():
            for _ in range(self.queues[chat_id].qsize()):
                item = await self.queues[chat_id].get()
                items.append(item)
                await self.queues[chat_id].put(item)
        return items


Queue = QueueManager()
