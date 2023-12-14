import strawberry
import typing
from infra.graphql.book_schema import BookResponse, BookSearch
from application.usecase.book_usecase import book_usecase

@strawberry.type
class Mutation:

    @strawberry.mutation
    async def create(self, id:str) -> str:
        return await book_usecase.create(id)
    @strawberry.mutation
    async def delete(self, id:str) -> str:
        return await book_usecase.delete(id)
