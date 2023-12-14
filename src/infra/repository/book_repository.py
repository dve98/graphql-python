from sqlmodel import Session, create_engine, select 
from infra.database.library_tables import Libro, Autor,Categoria,LibrosAutores,LibrosCategorias
from infra.database.config import db
from sqlalchemy.orm import declarative_base, Session, relationship,selectinload
from application.model.book_model import Libro as BookModel
from utils.mapper import convertir_libro_sqlmodel_a_pydantic, convertir_libro_pydantic_a_sqlmodel
class BookRepository:
    async def get_all(self):

        async with db as session:
            stmt = (
                select(Libro)
                .options(
                    selectinload(Libro.autores),
                    selectinload(Libro.categorias),
                )
            )
            results = await session.execute(stmt)
            results =results.scalars().all()
            books = [convertir_libro_sqlmodel_a_pydantic(libro, 'Base de datos') for libro in results]

            return books
    
    async def search_by_any(self,book_search):
        nombre_autor: str = book_search.autor
        nombre_categoria: str = book_search.categoria
        titulo_libro: str = book_search.titulo
        descripcion: str = book_search.descripcion
        subtitulo: str = book_search.subtitulo
        editor: str = book_search.editor
        async with db as session:
            stmt = (
                select(Libro)
                .options(
                    selectinload(Libro.autores),
                    selectinload(Libro.categorias),
                )
            )

            if nombre_autor:
                stmt = stmt.join(LibrosAutores).join(Autor).filter(Autor.nombre_autor.ilike(f"%{nombre_autor}%"))

            if nombre_categoria:
                stmt = stmt.join(LibrosCategorias).join(Categoria).filter(Categoria.nombre_categoria.ilike(f"%{nombre_categoria}%"))

            if titulo_libro:
                stmt = stmt.filter(Libro.titulo.ilike(f"%{titulo_libro}%"))

            if descripcion:
                stmt = stmt.filter(Libro.descripcion.ilike(f"%{descripcion}%"))

            if subtitulo:
                stmt = stmt.filter(Libro.subtitulo.ilike(f"%{subtitulo}%"))

            if editor:
                stmt = stmt.filter(Libro.editor.ilike(f"%{editor}%"))


            results = await session.execute(stmt)
            results = results.scalars().all()

            books = [convertir_libro_sqlmodel_a_pydantic(libro, 'Base de datos') for libro in results]
       

            return books

    async def search_by_id(self, id: int):
        async with db as session:
            stmt = (
                select(Libro)
                .options(
                    selectinload(Libro.autores),
                    selectinload(Libro.categorias),
                )
                .where(Libro.libro_id == id)
            )
            results = await session.execute(stmt)
            results = results.scalars().one()

            book = convertir_libro_sqlmodel_a_pydantic(results, 'Base de datos')
            return book
    

    async def create(self,book):

        book = convertir_libro_pydantic_a_sqlmodel(book)
        lista_autores = [autor.nombre_autor for autor in book.autores]
        lista_categorias = [categoria.nombre_categoria for categoria in book.categorias]

        async with db as session:
            stmt = (
                select(Autor)
                .filter(Autor.nombre_autor.in_(lista_autores))
            )
            result = await session.execute(stmt)
            autores_encontrados = result.scalars().all()

            stmt = (
                select(Categoria)
                .filter(Categoria.nombre_categoria.in_(lista_categorias))
            )
            result = await session.execute(stmt)
            categorias_encontradas = result.scalars().all()

        autores_en_bd=set([obj.nombre_autor for obj in autores_encontrados]) & set([obj.nombre_autor for obj in book.autores])
        autores_nuevos =  [obj for obj in book.autores if obj.nombre_autor not in autores_en_bd]
        autores_encontrados += autores_nuevos

        categorias_en_bd=set([obj.nombre_categoria for obj in categorias_encontradas]) & set([obj.nombre_categoria for obj in book.categorias])
        categorias_nuevos =  [obj for obj in book.categorias if obj.nombre_categoria not in categorias_en_bd]
        categorias_encontradas += categorias_nuevos

        book.autores=autores_encontrados
        book.categorias= categorias_encontradas

        async with db as session:
            async with session.begin():
                session.add(book)
            await db.commit_rollback()
            await session.refresh(book)
            return book

    async def delete(self,id):

        async with db as session:
            libro = await session.get(Libro, id)
            if libro:
                await session.delete(libro)
                await db.commit_rollback()
                return True
            return False

book_repository = BookRepository()