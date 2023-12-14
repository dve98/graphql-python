import httpx
from application.model.book_model import Libro,Autor, Categoria
from typing import Optional, List

base_url = "https://www.googleapis.com/books/v1/volumes"


def extraer_datos_desde_json(json_data):
    volume_info = json_data.get("volumeInfo")
    titulo = volume_info.get("title", "Título Desconocido")
    subtitulo = volume_info.get("subtitle")
    fecha_publicacion = volume_info.get("publishedDate")
    editor = volume_info.get("publisher")
    descripcion = volume_info.get("description")
    imagen_url = volume_info.get("imageLinks", {}).get("thumbnail")
    autores = volume_info.get("authors", [])
    categorias = volume_info.get("categories", [])
    id = json_data.get("id")

    return {
        "titulo": titulo,
        "subtitulo": subtitulo,
        "fecha_publicacion": fecha_publicacion,
        "editor": editor,
        "descripcion": descripcion,
        "imagen_url": imagen_url,
        "autores": autores,
        "categorias": categorias,
        "id":id
    }
def construir_libro(datos_libro):
    datos_libro = extraer_datos_desde_json(datos_libro)

    autores_obj = [Autor(nombre_autor=autor) for autor in datos_libro["autores"]]
    categorias_obj = [Categoria(nombre_categoria=categoria) for categoria in datos_libro["categorias"]]

    libro = Libro(
        titulo=datos_libro["titulo"],
        subtitulo=datos_libro["subtitulo"],
        fecha_publicacion=datos_libro["fecha_publicacion"],
        editor=datos_libro["editor"],
        descripcion=datos_libro["descripcion"],
        imagen_url=datos_libro["imagen_url"],
        autores = autores_obj,
        categorias = categorias_obj,
        id= datos_libro["id"],
        fuente = "google"
    )

    return libro

def construir_libros(lista_datos_libros):
    libros_construidos = []
    for datos_libro in lista_datos_libros:
        libro_construido = construir_libro(datos_libro)
        libros_construidos.append(libro_construido)
    return libros_construidos

def concatenar_atributos(libro) -> str:
    parametros = []

    if libro.subtitulo and libro.descripcion:
        parametros.append(f"{libro.subtitulo} {libro.descripcion}".strip())
    elif libro.subtitulo:
        parametros.append(libro.subtitulo)
    elif libro.descripcion:
        parametros.append(libro.descripcion)

    if libro.titulo:
        parametros.append(f"intitle:\"{libro.titulo}\"")

    if libro.autor:
        parametros.append(f"inauthor:\"{libro.autor}\"")

    if libro.editor:
        parametros.append(f"inpublisher:\"{libro.editor}\"")

    if libro.categoria:
        parametros.append(f"subject:\"{libro.categoria}\"")

    return '+'.join(parametros)

class GoogleRepository:
    async def search(self, book_search):    
        busqueda = concatenar_atributos(book_search)
        params = {'q': busqueda}
        async with httpx.AsyncClient() as client:
            response = await client.get(base_url, params = params)
            if response.status_code == 200:
                response= response.json()
                lista_libros = [item for item in response["items"]]        
                libros = construir_libros(lista_libros)
                return libros
    async def search_by_id(self, id):    
        async with httpx.AsyncClient() as client:
            response = await client.get(base_url+'/'+id)
            if response.status_code == 200:
                response= response.json()
                response = construir_libro(response)
                
                return response
google_repository = GoogleRepository()