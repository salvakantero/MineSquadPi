# CLAUDE.md - Contexto del Proyecto MineSquad Pi

## Descripcion General

**MineSquad Pi v1.1** es un juego retro 2D de puzzle/accion inspirado en Buscaminas, desarrollado en **Python 3 + Pygame**. Ambientado en la Segunda Guerra Mundial, el jugador debe desactivar campos minados usando pistas numericas.

## Tecnologias

- **Lenguaje:** Python 3
- **Framework:** Pygame
- **Persistencia:** pickle (config.dat, scores.dat)
- **Mapas:** JSON (formato Tiled)
- **Plataformas:** Windows, Linux, Raspberry Pi 500+ (con soporte RGB keyboard)

## Estructura Principal

```
minesquad.py      - Punto de entrada, game loop principal
game.py           - Sistema central (sprites, colisiones, UI)
player.py         - Logica del jugador
enemy.py          - Logica de enemigos (IA, animacion)
map.py            - Carga/renderizado de mapas JSON
menu.py           - Sistema de menus
camera.py         - Sistema de camara/scroll
config.py         - Gestion de configuracion persistente
constants.py      - Constantes globales
enums.py          - Enumeraciones
scoreboard.py     - HUD/marcador
hotspot.py        - Items/power-ups
shot.py           - Proyectiles
explosion.py      - Pool de explosiones
keyboardrgb.py    - Control RGB teclado Pi 500+
font.py           - Fuentes personalizadas
intro.py          - Secuencia de intro
jukebox.py        - Gestor de musica
```

## Recursos

- `images/` - Graficos (assets, sprites, fonts, tiles)
- `sounds/` - Audio (fx/*.wav, music/*.ogg)
- `maps/` - 9 niveles (map0.json - map8.json)
- `dist/` - Binarios compilados

## Arquitectura

- **Game Loop:** eventos -> update -> draw -> colisiones
- **Sprite Groups:** [0]=explosiones, [1]=enemigos, [2]=hotspots, [3]=proyectiles
- **Surfaces:** srf_menu (240x198), srf_map (240x176), srf_sboard (240x22) - escaladas x3
- **Movimiento:** tile-based (16x16 px por celda), mapa 30x40 celdas
- **Estados Player:** IDLE/WALK + direccion (UP/DOWN/LEFT/RIGHT)
- **Object Pool:** ExplosionPool reutiliza objetos

## Mecanica del Juego

- Campo con minas ocultas, revelar celdas al moverse
- Numeros indican minas adyacentes
- Marcar minas con balizas (beacons) limitadas
- 3 escenarios x 3 niveles = 9 niveles totales:
  1. El Alamein (desierto) - Escorpiones, Serpientes, Soldados
  2. Dia D (Normandia) - Proyectiles, Cangrejos, Soldados
  3. Ardenas (nieve) - Esquiadores, Jabalies, Soldados

## Personajes

- **BLAZE:** Movimiento lento, mas energia
- **PIPER:** Movimiento rapido, menos energia

## Controles

- Classic (flechas), Gamer (WASD), Retro (QAOP), Joypad
- B/Coma = baliza, Espacio = disparar, M = mute, ESC = pausa

## Ejecucion

```bash
python minesquad.py
```

## Compilacion

```bash
pip install pygame pyinstaller
pyinstaller --onefile --windowed --icon=minesquad.png minesquad.py
```

## Notas Importantes

- Resolucion base: 800x640 (windowed), soporta fullscreen 4:3 y 16:9
- Efectos visuales: scanlines (CRT), screen shake, fog en celdas ocultas
- Pi 500+: deteccion automatica, efectos RGB en teclado
- Licencia: GPL v3
- Autor: salvaKantero
