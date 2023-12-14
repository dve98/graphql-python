from infra.repository.google_repository import google_repository, GoogleRepository
from infra.repository.book_repository import book_repository, BookRepository
from infra.repository.openapi_repository import openapi_repository, OpenapiRepository
import asyncio
class BookUsecase:

    def __init__(self, book_repository: BookRepository, 
                 google_repository:GoogleRepository,
                 openapi_repository: OpenapiRepository):
        self.book_repository = book_repository
        self.google_repository = google_repository
        self.openapi_repository = openapi_repository


    async def get_books(self):
        books = await self.book_repository.get_all()
        return books
    async def get_book_by_id(self, id: int):
        book = await self.book_repository.search_by_id(id)
        return book
    async def get_book_by_any(self, book_search, number_of_books):
        database_response = await self.book_repository.search_by_any(book_search,number_of_books)
        google =  self.google_repository.search(book_search,number_of_books)
        openapi =  self.openapi_repository.search_and_get_books_async(book_search, number_of_books) 

        busquedas_externas =  [google,openapi]
        completada, pendiente = await asyncio.wait(
            busquedas_externas,
            return_when=asyncio.FIRST_COMPLETED
        )
        for tarea in pendiente:
            tarea.cancel()
        busqueda_completada = completada.pop()
        response = await busqueda_completada
        response = database_response + response
        if len(response) > number_of_books:
            response = response[:number_of_books]

        return response

    async def create(self, id):
        google_response= await self.google_repository.search_by_id(id)
        openapi_response = await self.openapi_repository.search_by_id(id) 
        if(google_response == None and openapi_response == None):
            return "El id no existe"
        libro_nuevo = google_response if openapi_response is None else openapi_response
        libro_nuevo = await self.book_repository.create(libro_nuevo)
        return libro_nuevo.libro_id

    async def delete(self, id):
        libro_borrado = await self.book_repository.delete(id)

        if libro_borrado:
            return "Borrado exitosamente"

        return "No se ha borrado compruebe que el id ingresado existe"


book_usecase = BookUsecase(book_repository,google_repository,openapi_repository)