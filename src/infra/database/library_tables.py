from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class LibrosAutores(SQLModel, table=True):
    __tablename__ = 'libros_autores'

    id: int = Field(primary_key=True)
    libro_id: int = Field(foreign_key="libro.libro_id")
    autor_id: int = Field(foreign_key="autor.autor_id")

class LibrosCategorias(SQLModel, table=True):
    __tablename__ = 'libros_categorias'

    id: int = Field(primary_key=True)
    libro_id: int = Field(foreign_key="libro.libro_id")
    categoria_id: int = Field(foreign_key="categoria.categoria_id")

class Autor(SQLModel, table=True):
    autor_id : int = Field(primary_key=True)
    nombre_autor: str
    libros: List["Libro"] =  Relationship(back_populates="autores", link_model=LibrosAutores)

class Categoria(SQLModel, table=True):
    categoria_id : int = Field(primary_key=True)
    nombre_categoria: str
    libros: List["Libro"] =  Relationship(back_populates="categorias", link_model=LibrosCategorias)


class Libro(SQLModel, table=True):
    libro_id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    subtitulo: Optional[str]
    fecha_publicacion: Optional[str]
    editor: Optional[str]
    descripcion: Optional[str]
    imagen_url: Optional[str]
    autores: Optional[List[Autor]] = Relationship(back_populates="libros", link_model=LibrosAutores)
    categorias: Optional[List[Categoria]] = Relationship(back_populates="libros", link_model=LibrosCategorias)

