# DinoDex Arena (POO en Python)
**Proyecto de aprendizaje:** estilo “Pokémon”, pero con dinosaurios.  
**Objetivo:** aprender Programación Orientada a Objetos (POO) en Python construyendo un mini “engine” de combate, colección y captura, evolucionando el sistema por sprints.

---

## Visión general
En **DinoDex Arena** controlas un **Trainer** que:
- colecciona dinosaurios (**DinoDex**),
- arma un equipo (**Team**),
- participa en combates por turnos (**Battle**),
- usa habilidades (**Moves**) e items (**Items**),
- aplica estados (veneno, sangrado, etc.) (**Status Effects**),
- y guarda/carga la partida (**Persistencia JSON**).

La clave del proyecto es diseñar el sistema con **entidades claras** y **reglas encapsuladas**, evitando “clases Dios” y condicionales gigantes.

---

## Conceptos de POO que cubriremos (mapa de aprendizaje)

### 1) Clases base (fundamentos)
**Temas:** clases/objetos, constructores, `__repr__`, encapsulación ligera  
**Clases:**
- **`Species`**: plantilla (base stats, tipo, moves posibles)
- **`Dino`**: instancia concreta (cambia con el tiempo: HP, nivel, estados)
- **`Move`**: ataque/habilidad
- **`Trainer`**: contiene DinoDex, inventario y equipo

✅ Aquí practicamos: **plantilla vs objeto** (`Species` define, `Dino` vive y cambia).

---

### 2) Encapsulación y propiedades
**Temas:** `@property`, validaciones, invariantes, getters/setters  
- `Dino.hp` **no se setea directamente**.
- Se modifica mediante:
  - `take_damage(amount)`
  - `heal(amount)`
- Invariantes:
  - `0 <= hp <= max_hp`
- `Trainer.team` con límite (ej. 3 o 6 dinos).

---

### 3) Composición y agregación
**Temas:** relaciones entre objetos  
- `Trainer` **tiene** `Inventory` y `DinoDex`
- `Dino` **tiene** `Moveset` y `StatusEffects`
- `Battle` **tiene** turnos, RNG, log de eventos

✅ Aprendizaje: **dividir responsabilidades** y evitar meter todo en una sola clase.

---

### 4) Herencia y polimorfismo (lo divertido)
**Temas:** herencia, override, polimorfismo real  
**Opción A (recomendada):** polimorfismo en habilidades
- `Move` (base)
  - `DamageMove`
  - `StatusMove`
  - `HealMove`

Cada subclase implementa `apply(context)` de forma distinta.

> Nota: también es posible modelar herencia por tipo de dino, pero preferimos mantener a `Dino` simple y que la variedad viva en `Move`/`Effect`.

---

### 5) Abstracción formal: ABC / Protocol
**Temas:** interfaces, contratos, extensibilidad tipo “plug-in”  
- `Effect(ABC)` con hooks por turno:
  - `on_turn_start(...)`
  - `on_turn_end(...)`
  - implementaciones: `Poison`, `Bleed`, `Stun`, `Fear`
- `Item(ABC)` con:
  - `use(target)`
  - implementaciones: `MedKit`, `Trap`, `BuffInjector`

✅ Resultado: efectos/items “enchufables” sin `if/elif` interminables.

---

### 6) Excepciones personalizadas
**Temas:** diseño robusto, control de errores “de dominio”  
- `TeamFullError`
- `NotEnoughEnergyError`
- `DinoFaintedError`
- `InvalidMoveError`

---

### 7) Persistencia (colección real)
**Temas:** serialización, `to_dict/from_dict`, repositorios  
Guardar/leer:
- DinoDex del trainer
- Inventario
- Stats y progreso

En JSON:
- `Dino.to_dict()`
- `Trainer.save("save.json")`
- `Trainer.load("save.json")`

---

### 8) Tests (para que no se rompa al crecer)
**Temas:** `pytest`, pruebas de reglas, determinismo  
- daño con efectividad de tipos
- límites de equipo
- stacking de estados (¿se acumula veneno? ¿se refresca?)
- combate determinista con `seed`

---

## Mecánicas “POO completas” (para reforzar diseño)

### A) Tabla de efectividad de tipos
Objeto: `TypeChart`  
Método:
- `damage_multiplier(attacker_type, defender_type)`

✅ Fuerza a separar **datos/reglas** del resto del sistema.

### B) Estados por turnos
Ejemplo:
- `Poison(turns=3, damage_per_turn=...)`

Cada turno:
- `effect.tick(dino)` o hooks `on_turn_*`.

### C) Captura como estrategia (Strategy pattern)
- `CaptureStrategy`
  - `BasicTrap`
  - `AdvancedTrap`

Función/servicio:
- `attempt_capture(dino, strategy)`

✅ Patrón sin “teoría”: se siente natural por el gameplay.

---

## Roadmap por sprints (guía de trabajo)

### Sprint 0 — Setup del repo + estructura
**Objetivo:** dejar el proyecto listo para crecer.
- Estructura:
  - `src/dinodex/`
    - `domain/` (entidades)
    - `battle/` (motor de combate)
    - `persistence/` (JSON)
    - `cli/` (menú consola)
  - `tests/`
- Config base: `.gitignore`, `README`, entorno `.venv`, `pytest` (opcional desde el inicio)

**Entregable:** proyecto corre “hello world” del CLI y puede importar módulos.

---

### Sprint 1 — Dino + Species + Move (sin combate)
**Objetivo:** modelar entidades base.
- Crear dinos desde species
- imprimir stats de forma legible
- asignar 2 movimientos por dino

**Entregable:** instanciar un Trainer con 1–2 dinos y mostrar su estado.

---

### Sprint 2 — Battle 1v1 (daño simple)
**Objetivo:** primer loop de combate.
- turnos definidos por `speed`
- atacar y reducir HP
- termina cuando alguien cae

**Entregable:** combate 1v1 reproducible (sin tipos ni estados todavía).

---

### Sprint 3 — Tipos + efectividad + energía
**Objetivo:** reglas más “Pokémon”.
- `TypeChart` y multiplicadores
- coste de energía por `Move`
- errores cuando no hay energía (`NotEnoughEnergyError`)

**Entregable:** combate 1v1 con tipos y energía.

---

### Sprint 4 — Status Effects + Items
**Objetivo:** sistema de efectos por turnos + objetos.
- veneno / sangrado / stun (mínimo 2)
- `MedKit` (curación), `Trap` (para captura futura)
- hooks de `Effect` por turno

**Entregable:** combate con efectos persistentes y items.

---

### Sprint 5 — Captura + DinoDex + persistencia
**Objetivo:** coleccionar y guardar progreso.
- `attempt_capture(...)` con `CaptureStrategy`
- registrar dinos capturados en `DinoDex`
- `Trainer.save/load` a JSON

**Entregable:** capturar un dino y persistir el estado.

---

### Sprint 6 — Evolución / mutación + tests completos
**Objetivo:** “cierre” con features grandes y estabilidad.
- evolución o mutación por nivel o item
- suite de tests `pytest` para reglas clave
- determinismo en battle con `seed`

**Entregable:** juego estable con pruebas que protegen reglas.

---

## Estructura propuesta de carpetas
```
poo_python_learning/
  src/
    dinodex/
      __init__.py
      domain/
      battle/
      persistence/
      cli/
  tests/
  README.md
  .gitignore
```

---

## Reglas de diseño (para mantener el proyecto limpio)
- Preferir **composición** sobre herencia en entidades (herencia en habilidades/efectos).
- Evitar “clases Dios”: si una clase crece demasiado, dividir.
- Mantener el motor (`battle/`) separado del CLI (`cli/`).
- Toda regla importante debe tener al menos 1 test cuando lleguemos a Sprint 6.

---

## Cómo correr (cuando esté implementado)
> Estos comandos son una guía; los iremos afinando conforme agreguemos dependencias.

Crear venv:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
```

Ejecutar CLI (placeholder):
```bash
python -m dinodex.cli
```

Correr tests:
```bash
pytest -q
```

---

## Backlog (ideas opcionales)
- Arena 2v2 / equipos
- Rareza de especies + biomas de spawn
- Sistema de experiencia y nivel
- “AI” simple para enemigo (Strategy)
- Logs del combate exportables a JSON
