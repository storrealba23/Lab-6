import modelos_biblioteca as modelos
 
 
def main() -> None:
    # Estructuras base (vacías)
    inventario = {}      # dict: isbn -> (titulo, autor, categoria)
    usuarios = {}        # dict: id_usuario -> {"nombre": ..., "libros_prestados": [...]}
    categorias = set()   # set: géneros disponibles
 
    # --- agregar_categoria ---
    print("1) agregar_categoria")
    categorias = modelos.agregar_categoria(categorias, "Fantasía")
    categorias = modelos.agregar_categoria(categorias, "Historia")
    categorias = modelos.agregar_categoria(categorias, "Fantasía")  # duplicado: se ignora
    print("   Categorías:", sorted(categorias))
    assert categorias == {"Fantasía", "Historia"}
 
    # --- registrar_libro ---
    print("2) registrar_libro")
    inventario, categorias = modelos.registrar_libro(
        inventario, "978-0618640157", "El Señor de los Anillos", "J.R.R. Tolkien",
        "Fantasía", categorias,
    )
    inventario, categorias = modelos.registrar_libro(
        inventario, "978-0553293357", "Fundación", "Isaac Asimov",
        "Ciencia Ficción", categorias,
    )
    inventario, categorias = modelos.registrar_libro(
        inventario, "978-0393354324", "Armas, gérmenes y acero", "Jared Diamond",
        "Historia", categorias,
    )
    print("   Inventario:")
    for isbn, libro in inventario.items():
        print("    ", isbn, "->", libro)
    print("   Categorías:", sorted(categorias))
    assert len(inventario) == 3
    assert inventario["978-0553293357"] == ("Fundación", "Isaac Asimov", "Ciencia Ficción")
    assert isinstance(inventario["978-0553293357"], tuple)
    assert categorias == {"Fantasía", "Historia", "Ciencia Ficción"}
 
    # ISBN duplicado: debe rechazarse sin alterar el inventario
    try:
        modelos.registrar_libro(
            inventario, "978-0618640157", "Otro título", "Otro autor", "Fantasía", categorias,
        )
        raise AssertionError("Debió levantar ValueError por ISBN duplicado")
    except ValueError as error:
        print("   ISBN duplicado rechazado:", error)
    assert inventario["978-0618640157"][0] == "El Señor de los Anillos"
 
    # --- registrar_usuario ---
    print("3) registrar_usuario")
    usuarios = modelos.registrar_usuario(usuarios, "u1", "Ana")
    usuarios = modelos.registrar_usuario(usuarios, "u2", "Luis")
    print("   Usuarios:", usuarios)
    assert usuarios["u1"] == {"nombre": "Ana", "libros_prestados": []}
    # Cada usuario debe tener su propia lista (no compartida)
    assert usuarios["u1"]["libros_prestados"] is not usuarios["u2"]["libros_prestados"]
 
    try:
        modelos.registrar_usuario(usuarios, "u1", "Otra Ana")
        raise AssertionError("Debió levantar ValueError por id duplicado")
    except ValueError as error:
        print("   Id duplicado rechazado:", error)
    assert usuarios["u1"]["nombre"] == "Ana"
 
    # --- prestar_libro: caso exitoso ---
    print("4) prestar_libro")
    usuarios = modelos.prestar_libro("978-0618640157", "u1", inventario, usuarios)
    print("   Préstamos de Ana:", usuarios["u1"]["libros_prestados"])
    print("   Inventario tras el préstamo:", list(inventario))
    assert usuarios["u1"]["libros_prestados"] == ["978-0618640157"]
    assert "978-0618640157" not in inventario
    assert len(inventario) == 2
    assert usuarios["u2"]["libros_prestados"] == []   # el otro usuario no se afecta
 
    # El mismo usuario puede llevarse un segundo libro
    modelos.prestar_libro("978-0553293357", "u1", inventario, usuarios)
    assert usuarios["u1"]["libros_prestados"] == ["978-0618640157", "978-0553293357"]
 
    # --- prestar_libro: casos de error (no deben modificar nada) ---
    antes_inventario = dict(inventario)
    antes_prestamos = list(usuarios["u2"]["libros_prestados"])
 
    # Libro que no existe
    try:
        modelos.prestar_libro("000-0000000000", "u2", inventario, usuarios)
        raise AssertionError("Debió levantar ValueError por libro inexistente")
    except ValueError as error:
        print("   Libro inexistente:", error)
 
    # Libro ya prestado (ya no está en el inventario)
    try:
        modelos.prestar_libro("978-0618640157", "u2", inventario, usuarios)
        raise AssertionError("Debió levantar ValueError por libro ya prestado")
    except ValueError as error:
        print("   Libro ya prestado:", error)
 
    # Usuario que no existe (el libro sí existe y debe seguir disponible)
    try:
        modelos.prestar_libro("978-0393354324", "u99", inventario, usuarios)
        raise AssertionError("Debió levantar ValueError por usuario inexistente")
    except ValueError as error:
        print("   Usuario inexistente:", error)
 
    assert inventario == antes_inventario
    assert "978-0393354324" in inventario
    assert usuarios["u2"]["libros_prestados"] == antes_prestamos
 
    print()
    print("Todas las pruebas de biblioteca.py pasaron correctamente.")
 
 
if __name__ == "__main__":
    main()
 