# Math Breakout Adventure

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.6%2B-yellow.svg)
![Pygame](https://img.shields.io/badge/pygame-required-red.svg)

## Descripción

Math Breakout Adventure es un juego educativo que combina la diversión del clásico juego Breakout con desafíos matemáticos. Los jugadores deben romper ladrillos con una pelota y resolver problemas matemáticos para avanzar. Perfecto para estudiantes que desean practicar sus habilidades matemáticas de una manera entretenida.


## Características

- ✅ Mecánica clásica de Breakout combinada con desafíos matemáticos
- ✅ Dificultad progresiva: los problemas matemáticos se vuelven más complejos con cada nivel
- ✅ Diferentes operaciones matemáticas: suma, resta, multiplicación y división (en niveles avanzados)
- ✅ Sistema de vidas y puntuación
- ✅ Efectos visuales y sonoros para una experiencia inmersiva
- ✅ Ladrillos coloridos con diferentes patrones según el nivel

## Requisitos

- Python 3.6 o superior
- Pygame
- NumPy

## Instalación

### Opción 1: Instalación desde GitHub Releases

1. Descarga el último [release](https://github.com/tuusuario/math-breakout-adventure/releases) del juego
2. Descomprime el archivo descargado
3. Ejecuta el juego con Python:
```bash
cd math-breakout-adventure
python breakout_matematico.py
```

### Opción 2: Instalación desde el código fuente

1. Clona este repositorio:
```bash
git clone https://github.com/tuusuario/math-breakout-adventure.git
cd math-breakout-adventure
```

2. Instala las dependencias:
```bash
pip install pygame numpy
```

3. Ejecuta el juego:
```bash
python breakout_matematico.py
```

### Opción 3: Instalación usando Make

Si tienes Make instalado, puedes usar el Makefile incluido:

```bash
make setup  # Instala las dependencias en un entorno virtual
make run    # Ejecuta el juego
```

## Estructura de directorios

```
math-breakout-adventure/
│
├── breakout_matematico.py  # Archivo principal del juego
├── README.md               # Este archivo
├── LICENSE.md              # Licencia MIT
├── CHANGELOG.md            # Historial de cambios
├── Makefile                # Utilidades para desarrollo
└── sounds/                 # Carpeta con efectos de sonido
    ├── brick_hit.wav       # Sonido al romper un ladrillo
    ├── wrong_answer.wav    # Sonido al responder incorrectamente
    └── game_over.wav       # Sonido de fin del juego
```

## Cómo jugar

1. Usa las teclas de flecha izquierda (←) y derecha (→) para mover la paleta.
2. Evita que la pelota caiga por debajo de la pantalla.
3. Rompe los ladrillos con la pelota.
4. Cuando la pelota golpea un ladrillo, aparecerá un problema matemático.
5. Responde correctamente para eliminar el ladrillo y ganar puntos.
6. Respuestas incorrectas te costarán una vida.
7. El juego termina cuando pierdes todas tus vidas o completas todos los niveles.

## Niveles y Dificultad

- El juego comienza con operaciones básicas (suma y resta).
- En niveles superiores (a partir del nivel 3), se introducen multiplicaciones más complejas.
- En los niveles más avanzados, se añaden problemas de división.
- La velocidad de la pelota aumenta con cada nivel, haciendo que el juego sea progresivamente más desafiante.

## Personalización

Puedes modificar varios aspectos del juego editando las constantes al inicio del archivo `breakout_matematico.py`:

- Dimensiones de la pantalla
- Tamaño de la paleta, la bola y los ladrillos
- Colores de los elementos del juego
- Número de vidas inicial
- Velocidad de la pelota

## Desarrollo

### Linting

Para verificar la calidad del código, ejecuta:

```bash
make lint
```

### Tests

Para ejecutar las pruebas (cuando estén disponibles):

```bash
make test
```

### Limpieza

Para limpiar archivos temporales y el entorno virtual:

```bash
make clean
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Haz un fork del repositorio
2. Crea una rama para tu función (`git checkout -b feature/amazing-feature`)
3. Haz commit de tus cambios (`git commit -m 'Añadir una función increíble'`)
4. Haz push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

Por favor, asegúrate de que tu código pase todas las pruebas de CI antes de enviar el PR.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE.md) para más detalles.

## Créditos

Desarrollado como un proyecto educativo para promover el aprendizaje de matemáticas a través del juego.

## Historial de Versiones

Consulta el [CHANGELOG](CHANGELOG.md) para ver el historial completo de cambios.
