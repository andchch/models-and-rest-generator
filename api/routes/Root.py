from uuid import UUID

from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy import select, update

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api.database_integration import get_async_session
from api.database_models import App, Status
from api.models.Root import *
from api.kafka_integration import send_kafka_message

router = APIRouter(
    prefix='/Root',
    tags=['Root']
)


@router.post('')
async def create_document(document: Root, session: Session = Depends(get_async_session)):
    if document.kind != 'Root':
        raise HTTPException(status_code=400, detail='Kind mismatch')
    json = document.dict()

    try:
        new_document = App(
            kind=document.kind,
            name=document.name,
            version=document.version,
            description=document.description,
            state=Status.new,
            json=json,
        )
        session.add(new_document)
        await session.commit()

        send_kafka_message('Root', 'Successful creation', new_document.json)

    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail='Database error: ' + str(e))

    return {'status': 'success'}


@router.put('/{uuid}/specification/')
async def update_specification(uuid: UUID, specification: Dict[str, Any],
                               session: Session = Depends(get_async_session)):
    request = select(App).where(App.kind == 'Root', App.UUID == uuid)
    response = await session.execute(request)
    document = response.scalars().first()
    if document is None:
        raise HTTPException(status_code=404, detail='Document not found')
    else:
        old_json = document.json
        new_json = old_json.copy()
        new_json['configuration']['specification'] = specification

        request = update(App).where(App.kind == 'Root', App.UUID == uuid).values(json=new_json)
        await session.execute(request)
        await session.commit()

        send_kafka_message('Root', 'Specification updated', new_json)

        return {'status': 'success'}


@router.put('/{uuid}/settings/')
async def update_settings(uuid: UUID, settings: Dict[str, Any],
                          session: Session = Depends(get_async_session)):
    request = select(App).where(App.kind == 'Root', App.UUID == uuid)
    response = await session.execute(request)
    document = response.scalars().first()
    if document is None:
        raise HTTPException(status_code=404, detail='Document not found')
    else:
        old_json = document.json
        new_json = old_json.copy()
        new_json['configuration']['settings'] = settings
        request = update(App).where(App.kind == 'Root', App.UUID == uuid).values(json=new_json)

        await session.execute(request)
        await session.commit()

        send_kafka_message('Root', 'Settings updated', new_json)

        return {'status': 'success'}


@router.put('/{uuid}/state/')
async def update_state(uuid: UUID, new_state: Status, session: Session = Depends(get_async_session)):
    request = select(App).where(App.kind == 'Root', App.UUID == uuid)
    result = await session.execute(request)
    document = result.scalars().first()
    if document is None:
        raise HTTPException(status_code=404, detail='Document not found')
    else:
        document.state = new_state
        await session.commit()

        send_kafka_message('Root', 'State updated', document.json)

        return {'status': 'success'}


@router.delete('/{uuid}/')
async def delete_document(uuid: UUID, session: Session = Depends(get_async_session)):
    request = select(App).where(App.kind == 'Root', App.UUID == uuid)
    result = await session.execute(request)
    document = result.scalars().first()
    if document is None:
        raise HTTPException(status_code=404, detail='Document not found')
    else:
        await session.delete(document)
        await session.commit()

        send_kafka_message('Root', 'Document deleted', document.json)

        return {'status': 'success'}


@router.get('/{uuid}/')
async def get_document(uuid: UUID, session: Session = Depends(get_async_session)):
    request = select(App).where(App.kind == 'Root', App.UUID == uuid)
    result = await session.execute(request)
    document = result.scalars().first()
    if document is None:
        raise HTTPException(status_code=404, detail='Document not found')
    else:
        send_kafka_message('Root', 'Document was recieved', document.json)
        return {'status': 'success', 'document': document.json}


@router.get('/{uuid}/state/')
async def get_state(uuid: UUID, session: Session = Depends(get_async_session)):
    request = select(App).where(App.kind == 'Root', App.UUID == uuid)
    result = await session.execute(request)
    document = result.scalars().first()
    if document is None:
        raise HTTPException(status_code=404, detail='Document not found')
    else:
        send_kafka_message('Root', 'State was recieved', document.json)
        return {'status': 'success', 'state': document.state}