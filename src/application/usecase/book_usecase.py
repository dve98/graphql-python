from infra.repository.google_repository import google_repository, GoogleRepository
from infra.repository.book_repository import book_repository, BookRepository

class BookUsecase:

    def __init__(self, book_repository: BookRepository, google_repository:GoogleRepository):
        self.book_repository = book_repository
        self.google_repository = google_repository


    async def get_books(self):
        books = await self.book_repository.get_all()
        return books
    async def get_book_by_id(self, id: int):
        book = await self.book_repository.search_by_id(id)
        return book
    async def get_book_by_any(self, book_search, number_of_books):
        database_response = await self.book_repository.search_by_any(book_search)
        google_response= await google_repository.search(book_search)
        response = database_response + google_response
        if len(response) > number_of_books:
            response = response[:number_of_books]

        return response

    async def create(self, id):
        google_response= await google_repository.search_by_id(id)
        libro_nuevo = await self.book_repository.create(google_response)
        return libro_nuevo.libro_id

    async def delete(self, id):
        libro_borrado = await self.book_repository.delete(id)

        if libro_borrado:
            return "Borrado exitosamente"

        return "No se ha borrado compruebe que el id ingresado existe"


book_usecase = BookUsecase(book_repository,google_repository)