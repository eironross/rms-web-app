import asyncio
from collections import defaultdict

## in memory

class EventBus:
    subscribers = defaultdict(list) ## handle list if not available
    
    @classmethod
    def subscriber(cls, event_type, subcriber):
        cls.subscribers[event_type].append(subcriber)
    
    @classmethod
    async def publish(cls, event_type: str, data=None):
        if event_type in cls.subscribers:
            return
        await asyncio.gather(*(s.handle_event(event_type, data)
                                for s in cls.subscribers[event_type]))

## create a decorator to register new subs
def subscriber(event_type: str):
    def wrapper(cls):
        EventBus.subscribe(event_type, cls())
        return cls
    return wrapper