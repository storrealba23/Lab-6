import math


def parsear_producto(linea: str) -> dict:
    """Convierte una línea "codigo,nombre,precio,cantidad" en un diccionario.
 
    Retorna {"codigo": str, "nombre": str, "precio": float, "cantidad": int}.
    Levanta ValueError si el formato o los tipos no son válidos.
    """
    # 1) La entrada debe ser un str
    if not isinstance(linea, str):
        raise ValueError("La línea debe ser un string")
 
    # 2) Debe haber exactamente 4 campos separados por coma
    partes = linea.split(",")
    if len(partes) != 4:
        raise ValueError(
            f"Se esperaban 4 campos separados por coma, pero hay {len(partes)}: {linea!r}"
        )
 
    # 3) Limpiar espacios alrededor de cada campo
    codigo, nombre, precio_texto, cantidad_texto = [p.strip() for p in partes]
 
    # 4) Convertir y validar el precio
    try:
        precio = float(precio_texto)
    except ValueError:
        raise ValueError(f"Precio inválido: {precio_texto!r}")
    # "nan" e "inf" se convierten a float sin error, pero no son precios válidos
    if not math.isfinite(precio) or precio < 0:
        raise ValueError(f"El precio debe ser un número finito mayor o igual a 0: {precio_texto!r}")
 
    # 5) Convertir y validar la cantidad
    try:
        cantidad = int(cantidad_texto)
    except ValueError:
        raise ValueError(f"Cantidad inválida: {cantidad_texto!r}")
    if cantidad < 0:
        raise ValueError(f"La cantidad debe ser mayor o igual a 0: {cantidad_texto!r}")
 
    return {"codigo": codigo, "nombre": nombre, "precio": precio, "cantidad": cantidad}
 
def resumen_de_producto(linea: str) -> str:
    """Devuelve "CODIGO - NOMBRE: $VALOR" con VALOR = precio * cantidad (1 decimal)."""
    producto = parsear_producto(linea)
    valor = round(producto["precio"] * producto["cantidad"], 1)
    return f"{producto['codigo']} - {producto['nombre']}: ${valor}"

def _validar_lineas(lineas: list) -> None:
    """Verifica que `lineas` sea una lista no vacía de strings.
 
    Levanta ValueError si no cumple.
    """
    if not isinstance(lineas, list) or len(lineas) == 0:
        raise ValueError("Se esperaba una lista no vacía de líneas")
    for linea in lineas:
        if not isinstance(linea, str):
            raise ValueError(f"Todos los elementos deben ser str, se encontró: {linea!r}")

def resumen_de_lotes(lineas: list) -> list:
    """Devuelve la lista de resúmenes de cada producto."""
    _validar_lineas(lineas)
    salida = []
    for linea in lineas:
        salida.append(resumen_de_producto(linea))
    return salida
 
 
def valor_de_lote(lineas: list) -> float:
    """Devuelve el valor total del inventario (suma de precio * cantidad), a 1 decimal."""
    _validar_lineas(lineas)
    total = 0.0
    for linea in lineas:
        producto = parsear_producto(linea)
        total += producto["precio"] * producto["cantidad"]
    return round(total, 1)
 
 
def producto_maximo_valor(lineas: list) -> str:
    """Devuelve el resumen del producto con mayor precio * cantidad.
 
    En caso de empate gana el primero que alcanzó el máximo.
    """
    _validar_lineas(lineas)
 
    # Se inicializa con el primer producto
    mejor = parsear_producto(lineas[0])
    mejor_valor = mejor["precio"] * mejor["cantidad"]
 
    # Se recorre el resto; la comparación estricta (>) conserva al primero en empates
    for linea in lineas[1:]:
        producto = parsear_producto(linea)
        valor = producto["precio"] * producto["cantidad"]
        if valor > mejor_valor:
            mejor = producto
            mejor_valor = valor
 
    # Mismo formato que resumen_de_producto
    valor_redondeado = round(mejor_valor, 1)
    return f"{mejor['codigo']} - {mejor['nombre']}: ${valor_redondeado}"
 
 
# ---------------------------------------------------------------------------
# Pruebas: se ejecutan solo con `python parseo.py`, no al importar el módulo
# ---------------------------------------------------------------------------
def _espera_value_error(funcion, *args) -> bool:
    """Devuelve True si funcion(*args) levanta ValueError."""
    try:
        funcion(*args)
    except ValueError:
        return True
    return False
 
 
def _probar() -> None:
    # --- parsear_producto: casos válidos ---
    assert parsear_producto("A1,Lapiz,2.5,10") == {
        "codigo": "A1", "nombre": "Lapiz", "precio": 2.5, "cantidad": 10,
    }
    # Espacios alrededor de los campos
    assert parsear_producto("  B2 , Cuaderno , 3 , 4 ") == {
        "codigo": "B2", "nombre": "Cuaderno", "precio": 3.0, "cantidad": 4,
    }
    # Tipos de los campos
    p = parsear_producto("C3,Regla,1.2,0")
    assert isinstance(p["precio"], float) and isinstance(p["cantidad"], int)
    # Precio y cantidad en 0 son válidos
    assert parsear_producto("D4,Goma,0,0")["precio"] == 0.0
 
    # --- parsear_producto: casos inválidos ---
    assert _espera_value_error(parsear_producto, 123)             # no es str
    assert _espera_value_error(parsear_producto, None)            # no es str
    assert _espera_value_error(parsear_producto, "A1,Lapiz,2.5")  # faltan campos
    assert _espera_value_error(parsear_producto, "A1,Lapiz,2.5,10,extra")  # sobran campos
    assert _espera_value_error(parsear_producto, "")              # línea vacía
    assert _espera_value_error(parsear_producto, "A1,Lapiz,abc,10")  # precio no numérico
    assert _espera_value_error(parsear_producto, "A1,Lapiz,2.5,diez")  # cantidad no numérica
    assert _espera_value_error(parsear_producto, "A1,Lapiz,2.5,3.5")  # cantidad no entera
    assert _espera_value_error(parsear_producto, "A1,Lapiz,-1,10")  # precio negativo
    assert _espera_value_error(parsear_producto, "A1,Lapiz,2.5,-3")  # cantidad negativa
    assert _espera_value_error(parsear_producto, "A1,Lapiz,nan,10")  # precio NaN
    assert _espera_value_error(parsear_producto, "A1,Lapiz,inf,10")  # precio infinito
 
    # --- resumen_de_producto ---
    assert resumen_de_producto("A1,Lapiz,2.5,10") == "A1 - Lapiz: $25.0"
    assert resumen_de_producto("B2,Cuaderno,3.25,3") == "B2 - Cuaderno: $9.8"  # 9.75 -> 9.8
    assert resumen_de_producto("D4,Goma,0,5") == "D4 - Goma: $0.0"
    assert _espera_value_error(resumen_de_producto, "linea mala")
 
    # --- _validar_lineas ---
    assert _validar_lineas(["A1,Lapiz,2.5,10"]) is None
    assert _espera_value_error(_validar_lineas, [])               # lista vacía
    assert _espera_value_error(_validar_lineas, "A1,Lapiz,2.5,10")  # no es lista
    assert _espera_value_error(_validar_lineas, ["A1,Lapiz,2.5,10", 5])  # elemento no str
    assert _espera_value_error(_validar_lineas, None)
 
    lineas = [
        "A1,Lapiz,2.5,10",       # 25.0
        "B2,Cuaderno,3.0,4",     # 12.0
        "C3,Mochila,40.0,1",     # 40.0
        "D4,Regla,1.0,40",       # 40.0  (empata con la mochila)
    ]
 
    # --- resumen_de_lotes ---
    assert resumen_de_lotes(lineas) == [
        "A1 - Lapiz: $25.0",
        "B2 - Cuaderno: $12.0",
        "C3 - Mochila: $40.0",
        "D4 - Regla: $40.0",
    ]
    assert _espera_value_error(resumen_de_lotes, [])
    assert _espera_value_error(resumen_de_lotes, ["A1,Lapiz,2.5,10", "mala"])
 
    # --- valor_de_lote ---
    assert valor_de_lote(lineas) == 117.0
    assert valor_de_lote(["A1,X,0.1,3"]) == 0.3   # 0.1 * 3 = 0.30000000000000004 -> 0.3
    assert isinstance(valor_de_lote(lineas), float)
    assert _espera_value_error(valor_de_lote, [])
    assert _espera_value_error(valor_de_lote, ["A1,Lapiz,2.5,10", "mala"])
 
    # --- producto_maximo_valor ---
    # Empate entre Mochila y Regla (40.0): debe ganar la primera (Mochila)
    assert producto_maximo_valor(lineas) == "C3 - Mochila: $40.0"
    assert producto_maximo_valor(["A1,Lapiz,2.5,10"]) == "A1 - Lapiz: $25.0"
    assert producto_maximo_valor(["A1,X,1,1", "B2,Y,5,5"]) == "B2 - Y: $25.0"
    assert _espera_value_error(producto_maximo_valor, [])
    assert _espera_value_error(producto_maximo_valor, ["mala"])
 
    print("Todas las pruebas de parseo.py pasaron correctamente.")
    print()
    print("Ejemplo de uso:")
    for resumen in resumen_de_lotes(lineas):
        print(" ", resumen)
    print("  Valor total del inventario:", valor_de_lote(lineas))
    print("  Producto de mayor valor:   ", producto_maximo_valor(lineas))
 
 
if __name__ == "__main__":
    _probar()
 