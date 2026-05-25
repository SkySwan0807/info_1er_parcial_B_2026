# Infografia UPB I/2026 - 1er parcial B (Paint)

## Descripcion

Este repositorio contiene el codigo base para el proyecto de tipo B.

Implementa una version inicial de PAINT sobre `arcade`. El mecanismo de
dibujo esta basado en una lista de trazos: `self.traces` es una lista de
diccionarios, cada uno con la forma:

```python
{
    "tool": TOOL_NAME,
    "color": COLOR,
    "trace": [(x0, y0), (x1, y1), ..., (xn, yn)]
}
```

El proyecto fue completado implementando nuevas herramientas de dibujo,
guardado y carga de archivos JSON, ademas de una interfaz grafica
funcional.

---

## Funcionalidades implementadas

### Herramientas

- **PencilTool**
  - Herramienta base para dibujar lineas simples.

- **MarkerTool**
  - Dibuja lineas mas gruesas que el lapiz.

- **SprayTool**
  - Genera puntos aleatorios alrededor del cursor simulando pintura en
    aerosol.

- **EraserTool**
  - Elimina puntos cercanos al cursor sin borrar el trazo completo.

### Guardado y carga

- Guardado de dibujos en formato JSON.
- Carga automatica de dibujos desde un archivo JSON.

### Interfaz grafica

- Barra superior con botones:
  - Herramientas
  - Guardado

## Controles

### Mouse

- Click izquierdo + arrastre:
  - Dibujar con la herramienta activa.

### Teclado

- `1` → PencilTool
- `2` → MarkerTool
- `3` → SprayTool
- `4` → EraserTool

### Colores

- `A` → Rojo
- `S` → Verde
- `D` → Azul
- `Q` → Amarillo
- `W` → Negro

### Archivos

- `O` → Guardar dibujo

---

## Estructura de los trazos

Todos los dibujos se almacenan usando la siguiente estructura:

```python
{
    "tool": TOOL_NAME,
    "color": (R, G, B),
    "trace": [(x0, y0), (x1, y1), ..., (xn, yn)]
}
```

Al guardarse en JSON, las tuplas de colores se convierten en listas.
Durante la carga se restauran nuevamente como tuplas.

---

## Criterios de evaluacion

- [x] El programa arranca sin errores.
- [x] MarkerTool dibuja trazos mas gruesos.
- [x] SprayTool dibuja puntos dispersos.
- [x] EraserTool elimina puntos sin borrar trazos completos.
- [x] El guardado genera archivos JSON validos.
- [x] La carga restaura correctamente los dibujos.
- [x] No se agregaron dependencias externas.
- [x] Interfaz grafica funcional.

---

## Reglas

- Solo se puede usar:
  - `arcade`
  - Modulos de la libreria estandar (`json`, `random`, `math`, etc.)

- No se agregaron dependencias externas como:
  - `numpy`
  - `pygame`
  - `Pillow`

- La estructura del diccionario de trazos se mantiene compatible con el
  codigo base.

- El proyecto debe ejecutarse usando:

```bash
uv run main.py
```