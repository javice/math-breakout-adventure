# Release 1.0.0 - Math Breakout Adventure

¡Bienvenido al primer lanzamiento oficial de Math Breakout Adventure! Esta versión inicial trae toda la diversión del clásico juego Breakout combinada con desafíos matemáticos educativos.

## ¿Qué hay en esta versión?

### Características principales
- Juego completo de Breakout con mecánicas pulidas
- Sistema de desafíos matemáticos con dificultad progresiva
- Compatibilidad multiplataforma (Windows, macOS, Linux)
- Efectos visuales y sonoros
- Sistema de niveles y puntuación

### Archivos incluidos
- `breakout_matematico.py` - Archivo principal del juego
- `sounds/` - Directorio con efectos de sonido
- `README.md` - Documentación del proyecto
- `LICENSE.md` - Licencia MIT
- `CHANGELOG.md` - Historial de cambios

## Instalación

### Requisitos previos
- Python 3.6 o superior
- Pygame
- NumPy

### Pasos de instalación

1. Descarga el archivo ZIP de esta release
2. Descomprime el archivo en tu directorio preferido
3. Abre una terminal o línea de comandos en ese directorio
4. Instala las dependencias:
   ```
   pip install pygame numpy
   ```
5. Ejecuta el juego:
   ```
   python breakout_matematico.py
   ```

## Notas importantes

- Si experimentas problemas con los sonidos, asegúrate de que el directorio `sounds/` esté en el mismo directorio que el archivo principal del juego.
- El juego está configurado inicialmente para una resolución de 1024x768. Puedes modificar estas dimensiones editando las constantes al inicio del archivo `breakout_matematico.py`.
- Las teclas de control son las flechas izquierda y derecha del teclado.

## Problemas conocidos

- En algunos sistemas Linux, puede haber problemas con la inicialización del audio. Si encuentras este problema, intenta actualizar Pygame a la última versión.
- El juego no guarda las puntuaciones entre sesiones (esta característica está planeada para una versión futura).

## Próximas características

Estamos trabajando en las siguientes mejoras para futuras versiones:

- Sistema de guardado de puntuaciones
- Modos de juego adicionales
- Personalización de niveles
- Mejoras en la interfaz de usuario

## Agradecimientos

Gracias a todos los que han apoyado este proyecto educativo. Esperamos que disfrutes jugando Math Breakout Adventure tanto como nosotros disfrutamos creándolo.