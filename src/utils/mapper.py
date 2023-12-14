from infra.database.library_tables import Autor as AutorSQLModel, Categoria as CategoriaSQLModel, Libro as LibroSQLModel
from application.model.book_model import Libro , Autor , Categoria

def convertir_libro_sqlmodel_a_pydantic(libro_sqlmodel: LibroSQLModel, fuente: str) -> Libro:
    return Libro(
        id=str(libro_sqlmodel.libro_id),
        titulo=libro_sqlmodel.titulo,
        subtitulo=libro_sqlmodel.subtitulo,
        fecha_publicacion=libro_sqlmodel.fecha_publicacion,
        editor=libro_sqlmodel.editor,
        descripcion=libro_sqlmodel.descripcion,
        imagen_url=libro_sqlmodel.imagen_url,
        autores=[convertir_autor_sqlmodel_a_pydantic(autor) for autor in libro_sqlmodel.autores] if libro_sqlmodel.autores else [],
        categorias=[convertir_categoria_sqlmodel_a_pydantic(categoria) for categoria in libro_sqlmodel.categorias] if libro_sqlmodel.categorias else [],
        fuente=fuente 
    )

def convertir_autor_sqlmodel_a_pydantic(autor_sqlmodel: AutorSQLModel) -> Autor:
    return Autor(nombre_autor=autor_sqlmodel.nombre_autor)

def convertir_categoria_sqlmodel_a_pydantic(categoria_sqlmodel: CategoriaSQLModel) -> Categoria:
    return Categoria(nombre_categoria=categoria_sqlmodel.nombre_categoria)


def convertir_libro_pydantic_a_sqlmodel(libro_pydantic: Libro) -> LibroSQLModel:
    return LibroSQLModel(
        titulo=libro_pydantic.titulo,
        subtitulo=libro_pydantic.subtitulo,
        fecha_publicacion=libro_pydantic.fecha_publicacion,
        editor=libro_pydantic.editor,
        descripcion=libro_pydantic.descripcion,
        imagen_url=libro_pydantic.imagen_url,
        autores=[convertir_autor_pydantic_a_sqlmodel(autor) for autor in libro_pydantic.autores] if libro_pydantic.autores else [],
        categorias=[convertir_categoria_pydantic_a_sqlmodel(categoria) for categoria in libro_pydantic.categorias] if libro_pydantic.categorias else []
    )

def convertir_autor_pydantic_a_sqlmodel(autor_pydantic: Autor) -> AutorSQLModel:
    return AutorSQLModel(nombre_autor=autor_pydantic.nombre_autor)

def convertir_categoria_pydantic_a_sqlmodel(categoria_pydantic: Categoria) -> CategoriaSQLModel:
    return CategoriaSQLModel(nombre_categoria=categoria_pydantic.nombre_categoria)