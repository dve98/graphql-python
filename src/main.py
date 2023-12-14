import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from infra.graphql.query import Query
from infra.graphql.mutation import Mutation

def init_app():
    apps = FastAPI(
        title="Biblioteca David",
        description="Fast API",
        version="1.0.0"
    )

    @apps.on_event("startup")
    async def startup():
        print("asd")
        # await db.startup()


    @apps.on_event("shutdown")
    async def shutdown():
        print("asd")
        # await db.shutdown()

    @apps.get("/")
    async def read_root():


        return "prueba"
        # return "rows"

    schema = strawberry.Schema(query=Query, mutation = Mutation)
    graphql_app = GraphQLRouter(schema)
    apps.include_router(graphql_app, prefix = "/graphql")

    return apps


app =  init_app()
