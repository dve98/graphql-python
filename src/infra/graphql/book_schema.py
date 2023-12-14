import strawberry
from typing import Optional, List
from infra.database.library_tables import  Autor
from strawberry.types import Info

def autores_string(root: "BookResponse", info: Info) -> str:
    return [autor.nombre_autor for autor in root.autores]

def categorias_string(root: "BookResponse", info: Info) -> str:
    return [categoria.nombre_categoria for categoria in root.categorias]

@strawberry.type
class BookResponse:
    id: str
    titulo: str
    subtitulo: Optional[str]
    fecha_publicacion: Optional[str]
    editor: Optional[str]
    descripcion: Optional[str]
    imagen_url: Optional[str]
    autores: List[str] =strawberry.field(resolver=autores_string)
    categorias: Optional[List[str]] =strawberry.field(resolver=categorias_string)
    fuente: Optional[str]



@strawberry.type
class Categoria:
    nombre_categoria: str 


@strawberry.input
class BookSearch:
    titulo: Optional[str] = ""
    subtitulo: Optional[str] = ""
    editor: Optional[str] = ""
    descripcion: Optional[str] = ""
    autor: Optional[str] = ""
    categoria: Optional[str] = ""