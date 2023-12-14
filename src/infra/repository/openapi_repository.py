import httpx
from application.model.book_model import Libro,Autor, Categoria
from typing import Optional, List



class OpenapiRepository:
    def __init__(self):
        self.base_url_search = "https://openlibrary.org/search.json"
        self.base_url_details = "https://openlibrary.org/works"

    async def search_books_async(self, url,limit):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

            if response.status_code == 200:
                data = response.json()
                return data.get("docs", [])
            else:
                return None

    async def get_book_details_async(self, book_id):
        url = f"{self.base_url_details}/{book_id}.json"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

            if response.status_code == 200:
                data = response.json()
                return data
            else:
                return None
    async def search_by_id(self, id):

        book_datails = await self.get_book_details_async(id)
        if book_datails is None:
            return None 
        base_url = self.base_url_search +'?'
        base_url += f"q={id}&"
        base_url += f"limit={1}"

        result = await self.search_books_async(base_url,1)
        libro = await self.construir_libro(result)
        if libro is None:
            return None
        
        libro = libro[0] if len(libro)>0 else None
        return libro


    async def search_and_get_books_async(self, book, limit):
        
        url = self.construir_url_libro(book, limit)
        result = await self.search_books_async(url,limit)
        libros = await self.construir_libro(result)
        return libros

        
    def construir_url_libro(self, libro: Libro, limit: Optional[int] = None) -> str:

        base_url = self.base_url_search +'?'

        # Agregar parámetros según los atributos del libro
        if hasattr(libro, 'descripcion'):
            base_url += f"q={libro.descripcion}&"
        if hasattr(libro, 'subtitulo'):
            base_url += f"{libro.subtitulo}&"
        if hasattr(libro, 'titulo') and libro.titulo:
            base_url += f"title={libro.titulo}&"

        if hasattr(libro, 'autores') and libro.autores:
            for autor in libro.autores:
                base_url += f"author={autor.nombre_autor}&"

        if hasattr(libro, 'categorias') and libro.categorias:
            for categoria in libro.categorias:
                base_url += f"subject={categoria.nombre_categoria}&"

        if hasattr(libro, 'editor') and libro.editor:
            base_url += f"publisher={libro.editor}&"
        if limit:
            base_url += f"limit={limit}&"
        # Eliminar el último "&" si está presente
        if base_url.endswith("&"):
            base_url = base_url[:-1]
        return base_url


    async def construir_libro(self, result):
        if result:
            libros = []
            for doc in result:
                title = doc.get("title", "N/A")
                subtitle = doc.get("subtitle", "")
                author_name = doc.get("author_name", ["N/A"])[0]
                book_id = doc.get("key", "").replace("/works/", "")

                # Obtener detalles del libro utilizando el ID
                book_details = await self.get_book_details_async(book_id)

                # Obtener el valor del campo 'description'
                description_value = ''
                if book_details.get("description"):
                    description_value = book_details.get("description")
                    if type(description_value) is dict:
                        description_value =description_value.get("value")
                        
                # Construir el objeto Libro
                libro = Libro(
                    id=book_id,
                    titulo=title,
                    subtitulo=subtitle,
                    autores=[Autor(nombre_autor=author_name)],
                    fecha_publicacion=book_details.get("first_publish_year"),
                    editor=book_details.get("publishers", ["N/A"])[0],
                    descripcion=description_value,
                    imagen_url=f"https://covers.openlibrary.org/b/id/{book_id}-L.jpg",
                    categorias=[Categoria(nombre_categoria=category) for category in book_details.get("subject", [])],
                    fuente="Open Library"
                )

                libros.append(libro)

            return libros
        else:
            return None

openapi_repository = OpenapiRepository()