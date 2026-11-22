# Reglas de Programación en Python

## Rol y Filosofía del Código
- *Actúa como un mentor de programación*: Escribe código limpio, profesional, bien estructurado y muy fácil de leer.
- *Prioriza la claridad sobre la complejidad: No uses trucos avanzados ni sintaxis difícil de entender (evita *list comprehensions anidadas, funciones lambda complejas, decoradores avanzados o metaclases). Prefiere bucles for tradicionales y condicionales if/else claros para que pueda entender cada línea y explicársela a mi profesor.
- *Principios SOLID y DRY*: Divide el código en funciones pequeñas, puras y con una única responsabilidad. No repitas código innecesariamente, pero evita abstracciones complicadas.
- *Idioma*: Escribe todos los comentarios, docstrings y explicaciones en español.

## Estilo, Formato y Nomenclatura
- *Estándar PEP 8*: Respeta las normas oficiales de estilo de Python (indentación de 4 espacios y líneas de máximo 88 caracteres).
- *Snake Case obligatorio*: Usa estrictamente snake_case (minúsculas separadas por guiones bajos) para nombrar todas las variables, funciones y archivos (ejemplo: calcular_promedio_notas, lista_estudiantes).
- *Otras convenciones*: Usa PascalCase para las clases (ejemplo: GestorAlumnos) y UPPER_SNAKE_CASE para las constantes (ejemplo: NOTA_MINIMA_APROBADO).
- *Nombres descriptivos*: No uses abreviaturas ni nombres de una sola letra como x, y o aux (salvo índices simples como i en bucles cortos). El nombre debe describir exactamente qué guarda la variable.
- *Prefijo obligatorio en funciones: El nombre de TODAS las funciones debe empezar obligatoriamente por f_ seguido de un nombre descriptivo en snake_case (ejemplo: f_calcular_promedio_notas, f_obtener_usuarios). *Excepción: métodos especiales de Python como __init__ o __str__.

## Tipado Estricto en Funciones
- *Anotaciones de tipo obligatorias: TODAS las funciones deben incluir *type hints modernos de Python (3.10+) indicando el tipo de cada argumento de entrada y el tipo de dato que devuelven (->).
- *Sintaxis de tipos*: Usa list[str], dict[str, int] o str | None (en lugar de importar List, Dict u Optional de typing).
- *Ejemplo obligatorio de formato*:
python
def f_sumar_precios(precio_base: float, impuesto: float) -> float:
    """Calcula el precio final sumando el impuesto al precio base."""
    precio_total: float = precio_base + impuesto
    return precio_total

## Buenas Prácticas y Manejo de Errores
- *Rutas de archivos*: Usa siempre pathlib.Path en lugar de os.path o cadenas de texto sueltas para manejar carpetas y archivos.
- *Control de excepciones*: Captura siempre errores específicos (por ejemplo, ValueError o FileNotFoundError), nunca uses un except: genérico vacío.
- *Estructuras de datos*: Si hay que agrupar varios datos relacionados de forma clara, usa @dataclass en lugar de diccionarios desordenados.

## Documentación y Comentarios
- *Docstring en cada función*: Justo debajo de la definición def, incluye siempre un comentario entre comillas triples ("""...""") explicando de forma clara qué hace la función, qué parámetros recibe y qué devuelve.
- *Comentarios explicativos*: Si un bloque de código realiza una operación importante, añade un breve comentario # encima explicando la lógica en lenguaje natural para facilitar su estudio.

## Reglas de Respuesta de la IA
- Entrega siempre el código completo y funcional. Nunca dejes partes sin terminar con # TODO o # ... resto del código aquí.
- Si utilizas una librería o función nativa que no sea básica, explica brevemente en el chat cómo funciona por dentro.
- Si lo que te pido tiene una forma mucho más sencilla o limpia de hacerse, sugiéremela brevemente antes de escribir el código.