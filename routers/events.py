from fastapi import APIRouter, Body, HTTPException, status
from typing import List
from beanie import PydanticObjectId

from models.events import Event, EventUpdate
from database.connection import Database

event_routers = APIRouter(tags=["Events"])

event_database = Database(Event)


@event_routers.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    events = await event_database.get_all()
    return events


@event_routers.get("/{id}", response_model=Event)
async def retrieve_event(id: PydanticObjectId) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return event


# @event_routers.delete("/")
# async def delete_all_events() -> dict:
#     events.clear()
#     return {
#         "message": "Events deleted successfully"
#     }


@event_routers.delete("/{id}")
async def delete_event(id: PydanticObjectId) -> dict:
    event = await event_database.delete(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return {
        "message": "Event deleted successfully"
    }


@event_routers.post("/")
async def create_event(body: Event = Body(...)) -> dict:
    await event_database.save(body)
    return {
        "message": "Event created successfully"
    }


@event_routers.put("/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, body: EventUpdate) -> dict[str, str]:
    updated_event = await event_database.update(id, body)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return updated_event


