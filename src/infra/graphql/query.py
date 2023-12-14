import strawberry
import typing
from infra.graphql.book_schema import BookResponse, BookSearch
from application.usecase.book_usecase import book_usecase

@strawberry.type
class Query:

    @strawberry.field
    async def get_all_books(self) -> typing.List[BookResponse]:
        return await book_usecase.get_books()

    @strawberry.field
    async def get_book_by_id(self, id:int) -> BookResponse:
        return await book_usecase.get_book_by_id(id)
    @strawberry.field
    async def get_book_by_any(self, book_search:BookSearch, number_of_books: int ) ->  typing.List[BookResponse]:
        return await book_usecase.get_book_by_any(book_search, number_of_books)
