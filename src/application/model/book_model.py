from pydantic import BaseModel
from typing import Optional, List


class Autor(BaseModel):
    nombre_autor: str

class Categoria(BaseModel):
    nombre_categoria: str

class Libro(BaseModel):
    id: Optional[str] 
    titulo: Optional[str] 
    subtitulo: Optional[str]
    fecha_publicacion: Optional[str]
    editor: Optional[str]
    descripcion: Optional[str]
    imagen_url: Optional[str]
    autores: Optional[List[Autor]] 
    categorias: Optional[List[Categoria]] 
    fuente: Optional[str] 