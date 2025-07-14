import logging

from uuid import UUID

from app.schemas.dto import (
    CreateServiceDTO, 
    UpdateServiceDTO
)
from app.schemas.responses import Response
from app.unit_of_work import ServiceUnitOfWork


logger = logging.getLogger(__name__)


class Service:
    def __init__(
        self,
        unit_of_work: ServiceUnitOfWork,
    ):
        self._uow = unit_of_work

    async def create_service(self, body: CreateServiceDTO):
        async with self._uow as uow:
            service = await uow.service_repository.create(body)
            await uow.commit()
        return service
    
    async def get_service(self, service_id: UUID):
        async with self._uow as uow:
            return await uow.service_repository.find_by_id(
                service_id, exception_on_none=True
            )
        
    async def get_all_services(self):
        async with self._uow as uow:
            return await uow.service_repository.find_all()
        
    async def update_service(self, service_id: UUID, body: UpdateServiceDTO):
        async with self._uow as uow:
            service = await uow.service_repository.find_by_id(
                service_id, exception_on_none=True
            )
            updated_service = await uow.service_repository.update(
                db_obj=service, obj_in=body
            )
            await uow.commit()

        return updated_service
    
    async def delete_service(self, service_id: UUID):
        async with self._uow as uow:
            await uow.service_repository.delete_by_id(service_id)
            await uow.commit()

        return Response(message="Service was succesfully deleted")
