import sys
import arcade
import json
from tool import PencilTool
from tool import MarkerTool
from tool import SprayTool
from tool import EraserTool
from values import TITLE
from values import WIDTH
from values import HEIGHT
from values import TOP_BAR_HEIGHT
from values import icon_names


class Paint(arcade.View):
    def __init__(self, load_path: str | None = None):
        super().__init__()
        self.background_color = arcade.color.LIGHT_GRAY
        # Herramientas (una sola instancia de cada una)
        self.pencil_tool = PencilTool()
        self.marker_tool = MarkerTool()
        self.spray_tool = SprayTool()
        self.eraser_tool = EraserTool()

        # Herramienta actual
        self.tool = self.pencil_tool

        # Herramientas usadas para dibujar
        self.used_tools = {
            "PENCIL": self.pencil_tool,
            "MARKER": self.marker_tool,
            "SPRAY": self.spray_tool
        }

        # Configuracion actual
        self.color = arcade.color.BLUE
        self.thickness = 1
        self.pixels = 4

        # Iconos
        self.icons = arcade.SpriteList()

        for i, name in enumerate(icon_names):

            sprite = arcade.Sprite(
                f"icons/{name}",
                scale=0.5
            )

            sprite.center_x = 13 + i * 25
            sprite.center_y = HEIGHT - (TOP_BAR_HEIGHT / 2)

            self.icons.append(sprite)

        # Cargar dibujo
        if load_path is not None:

            with open(load_path, "r") as file:
                self.traces = json.load(file)

        else:
            self.traces = []

    def on_key_press(self, symbol: int, modifiers: int):
        # Seleccion de herramientas con las teclas numericas
        if symbol == arcade.key.KEY_1:
            self.selectPencil()
        elif symbol == arcade.key.KEY_2:
            ### KEY_2 -> MarkerTool (su implementacion) ###
            self.selectMarker()
        elif symbol == arcade.key.KEY_3:
            ### KEY_3 -> SprayTool (su implementacion) ###
            self.selectSpray()
        elif symbol == arcade.key.KEY_4:
            ### KEY_4 -> EraserTool (su implementacion) ###
            self.selectEraser()
        # Seleccion de color con teclas asd
        elif symbol == arcade.key.A:
            self.color = arcade.color.RED
        elif symbol == arcade.key.S:
            self.color = arcade.color.GREEN
        elif symbol == arcade.key.D:
            self.color = arcade.color.BLUE
        elif symbol == arcade.key.Q:
            self.color = arcade.color.YELLOW
        elif symbol == arcade.key.W:
            self.color = arcade.color.BLACK
        elif symbol == arcade.key.O:
            self.selectSave()

        self.used_tools[self.tool.name] = self.tool

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if y > HEIGHT - (TOP_BAR_HEIGHT + 3):
            if 0 <= x <= 25:
                self.selectPencil()
            elif 25 < x <= 50:
                self.selectMarker()
            elif 50 < x <= 75:
                self.selectSpray()
            elif 75 < x <= 100:
                self.selectEraser()
            elif 100 <= x <= 125:
                self.selectSave()
        else:
            if button == arcade.MOUSE_BUTTON_LEFT:
                self.traces.append({
                    "tool": self.tool.name,
                    "color": self.color,
                    "trace": [(x, y)],
                    "thickness": self.thickness,
                    "pixels": self.pixels
                })

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        if y > HEIGHT - (TOP_BAR_HEIGHT + 3):
            return
        else:
            if self.traces:
                if self.tool.name == "SPRAY":
                    self.tool.spray_points(self.traces[-1], x, y)
                elif self.tool.name == "ERASER":
                    self.tool.erase_traces(self.traces, x, y)
                else:
                    self.traces[-1]["trace"].append((x, y))

    def on_draw(self):
        self.clear()
        
        # Barra superior
        arcade.draw_lrbt_rectangle_filled(
            0,
            WIDTH,
            HEIGHT - TOP_BAR_HEIGHT,
            HEIGHT,
            arcade.color.WHITE
        )
        
        # Linea separadora
        arcade.draw_line(
            0,
            HEIGHT - TOP_BAR_HEIGHT,
            WIDTH,
            HEIGHT - TOP_BAR_HEIGHT,
            arcade.color.BLACK,
            2
        )

        self.icons.draw()

        for tool in self.used_tools.values():
            if tool.name != "ERASER":
                tool.draw_traces(self.traces)

    def selectPencil(self):
        self.tool = self.pencil_tool = PencilTool()

    def selectMarker(self):
        self.tool = self.marker_tool        
        self.thickness = 8
    
    def selectSpray(self):
        self.tool = self.spray_tool
        self.thickness = 10
        self.pixels = 12

    def selectEraser(self):
        self.thickness = 10
        self.eraser_tool.set_radius(self.thickness)
        self.tool = self.eraser_tool

    def selectSave(self):
        number = 1

        while True:
            filename = f"paint{number}.json"

            try:
                with open(filename, "r"):
                    number += 1

            except FileNotFoundError:
                break

        with open(filename, "w") as file:
            json.dump(self.traces, file)

        print(f"Guardado en {filename}")


if __name__ == "__main__":
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    # Invocacion: python main.py [ruta/a/dibujo.json]
    if len(sys.argv) > 1:
        app = Paint(sys.argv[1])
    else:
        app = Paint()
    window.show_view(app)
    arcade.run()
