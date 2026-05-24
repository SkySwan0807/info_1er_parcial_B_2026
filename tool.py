import arcade
from typing import Protocol
import random
import math
import copy

class Tool(Protocol):
    """
    Protocolo que define las operaciones que una herramienta debe ofrecer.

    Cada herramienta concreta tiene un `name` unico que coincide con el
    valor "tool" de las entradas en la lista de trazos.
    """
    name: str

    def draw_traces(self, traces: list[dict]):
        ...

    def get_name(self):
        return self.name


class PencilTool(Tool):
    name = "PENCIL"

    def draw_traces(self, traces: list[dict]):
        for trace in traces:
            if trace["tool"] != self.name:
                continue
            # draw_line_strip requiere al menos 2 puntos
            if len(trace["trace"]) < 2:
                continue
            arcade.draw_line_strip(trace["trace"], trace["color"])


class MarkerTool(Tool):
    """
    Marcador. Similar al lapiz pero con un grosor mayor.

    El grosor debera ser un argumento al __init__ con un default razonable
    (por ejemplo 8 pixeles).

    Pista: arcade.draw_line_strip no soporta grosor directamente, pero
    `arcade.draw_lines` o `arcade.draw_line` si lo aceptan.
    """
    name = "MARKER"


    def draw_traces(self, traces: list[dict]):

        for trace in traces:
            if trace["tool"] != self.name:
                continue

            points = trace["trace"]

            if len(points) < 2:
                continue

            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]

                arcade.draw_line(
                    x1,
                    y1,
                    x2,
                    y2,
                    trace["color"],
                    trace["thickness"]
                )


class SprayTool(Tool):
    """
    Spray. En cada punto del trazo dibuja N pixeles dispersos
    aleatoriamente dentro de un radio.

    El numero de pixeles por punto y el radio deberan ser argumentos al
    __init__ con defaults razonables (por ejemplo 12 pixeles dentro de un
    radio de 10).

    Pista: usar `random.uniform` para dispersar dentro del radio y
    `arcade.draw_point` para dibujar cada pixel.
    """
    name = "SPRAY"

    def spray_points(self, trace, x, y):
        spray_points = []

        for _ in range(trace["pixels"]):

            offset_x = random.uniform(-trace["thickness"], trace["thickness"])
            offset_y = random.uniform(-trace["thickness"], trace["thickness"])

            spray_points.append((x + offset_x, y + offset_y))

        trace["trace"].extend(spray_points)

    def draw_traces(self, traces):
        for trace in traces:
            if trace["tool"] != self.name:
                continue

            for x, y in trace["trace"]:
                arcade.draw_point(
                    x,
                    y,
                    trace["color"],
                    1
                )

class EraserTool(Tool):
    """
    Borrador. NO es una herramienta que dibuje: su efecto es modificar la
    lista de trazos al pasar el cursor sobre ellos.

    Comportamiento esperado:
    - Mientras el usuario arrastra el cursor con esta herramienta
      seleccionada, los PUNTOS de cualquier trazo que esten dentro de
      `radius` pixeles del cursor deben eliminarse.
    - El borrador NO elimina trazos enteros: solo los puntos cercanos.
    - Cuidado: si se elimina un punto en medio de un trazo, dibujarlo
      como una sola line_strip va a unir los extremos restantes con una
      linea cruzada incorrecta. Decida como manejar esto (por ejemplo,
      dividiendo el trazo en dos al borrar puntos intermedios).
    - El borrador no tiene draw_traces propio (no se dibuja a si mismo),
      pero puede necesitar un metodo extra para procesar la lista de
      trazos. La firma de ese metodo y como se invoca desde main.py
      forma parte del ejercicio.
    """
    name = "ERASER"

    def __init__(self, radius=10):

        self.radius = radius

    def erase_traces(self, traces, x, y):

        for trace in traces[:]:
            if trace["tool"] == "SPRAY":
                new_points = []

                for a, b in trace["trace"]:
                    d = math.hypot(x - a, y - b)

                    if d > self.radius:
                        new_points.append((a, b))

                trace["trace"] = new_points
            else:
                new_points = []
                new_points_2 = []
                trace_cut = False

                for a, b in trace["trace"]:
                    d = math.hypot(x - a, y - b)

                    if d > self.radius:
                        if not trace_cut:
                            new_points.append((a, b))
                        else:
                            new_points_2.append((a, b))
                    else:
                        trace_cut = True

                trace["trace"] = new_points

                if len(new_points_2) >= 2:
                    new_trace = copy.deepcopy(trace)
                    new_trace["trace"] = new_points_2
                    traces.append(new_trace)
                



    def draw_traces(self, traces):
        pass

