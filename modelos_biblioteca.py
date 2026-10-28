def agregar_categoria(categorias: set, nueva_categoria: str) -> set:
    """Agrega una categoría al conjunto de categorías y lo retorna.
 
    Los conjuntos ignoran los duplicados automáticamente.
    """
    categorias.add(nueva_categoria)
    return categorias
 
 
def registrar_libro(
    inventario: dict,
    isbn: str,
    titulo: str,
    autor: str,
    categoria: str,
    categorias: set,
) -> tuple[dict, set]:
    """Registra un libro en el inventario y su categoría en el registro de categorías.
 
    El libro se guarda como la tupla (titulo, autor, categoria) con el ISBN como clave.
    Retorna (inventario, categorias).
    """
    if isbn in inventario:
        raise ValueError(f"Ya existe un libro registrado con el ISBN {isbn}")
 
    libro = (titulo, autor, categoria)  # tupla: datos fijos que no deben cambiar
    inventario[isbn] = libro
    categorias = agregar_categoria(categorias, categoria)
    return inventario, categorias
 
 
def registrar_usuario(usuarios: dict, id_usuario: str, nombre: str) -> dict:
    """Registra un usuario usando su id como clave.
 
    Cada usuario es un diccionario interno con su nombre y una lista vacía
    de libros prestados. Retorna el registro de usuarios actualizado.
    """
    if id_usuario in usuarios:
        # Sobrescribirlo borraría los libros que el usuario ya tiene prestados
        raise ValueError(f"Ya existe un usuario registrado con el id {id_usuario}")
 
    usuarios[id_usuario] = {"nombre": nombre, "libros_prestados": []}
    return usuarios
 
 
def prestar_libro(isbn: str, id_usuario: str, inventario: dict, usuarios: dict) -> dict:
    """Presta un libro a un usuario.
 
    Verifica que el libro y el usuario existan. Si ambos existen, agrega el ISBN
    a la lista de libros prestados del usuario y elimina el libro del inventario
    (queda no disponible). Retorna el registro de usuarios actualizado.
 
    Levanta ValueError si el libro o el usuario no existen; en ese caso no se
    modifica nada.
    """
    if isbn not in inventario:
        raise ValueError(f"El libro con ISBN {isbn} no existe en el inventario (o ya fue prestado)")
    if id_usuario not in usuarios:
        raise ValueError(f"El usuario con id {id_usuario} no está registrado")
 
    usuarios[id_usuario]["libros_prestados"].append(isbn)
    del inventario[isbn]
    return usuarios
 