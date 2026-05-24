import sys
import arcade
from tool import PencilTool
from tool import MarkerTool
from tool import SprayTool
from tool import EraserTool
import json

WIDTH = 800
HEIGHT = 600
TITLE = "Paint"

COLORS = {
    "black": arcade.color.BLACK,
    "red": arcade.color.RED,
    "blue": arcade.color.BLUE,
    "yellow": arcade.color.YELLOW,
    "green": arcade.color.GREEN,
}


class Paint(arcade.View):
    def __init__(self, load_path: str | None = None):
        super().__init__()
        self.background_color = arcade.color.LIGHT_GRAY
        self.tool = PencilTool()
        self.used_tools = {self.tool.name: self.tool}
        self.color = arcade.color.BLUE
        self.thickness = 1
        self.pixels = 1

        if load_path is not None:

            with open(load_path, "r") as file:
                self.traces = json.load(file)

            for trace in self.traces:
                if trace["tool"] == "MARKER":
                    self.used_tools["MARKER"] = MarkerTool()
                elif trace["tool"] == "SPRAY":
                    self.used_tools["SPRAY"] = SprayTool()
                elif trace["tool"] == "PENCIL":
                    self.used_tools["PENCIL"] = PencilTool()
        else:
            self.traces = []

    def on_key_press(self, symbol: int, modifiers: int):
        # Seleccion de herramientas con las teclas numericas
        if symbol == arcade.key.KEY_1:
            self.tool = PencilTool()
        elif symbol == arcade.key.KEY_2:
            ### KEY_2 -> MarkerTool (su implementacion) ###
            self.tool = MarkerTool()
            self.thickness = 8
        elif symbol == arcade.key.KEY_3:
            ### KEY_3 -> SprayTool (su implementacion) ###
            self.tool = SprayTool()
            self.thickness = 10
            self.pixels = 12
        elif symbol == arcade.key.KEY_4:
            ### KEY_4 -> EraserTool (su implementacion) ###
            self.thickness = 10
            self.tool = EraserTool(self.thickness)
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

        self.used_tools[self.tool.name] = self.tool

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.traces.append({
                "tool": self.tool.name,
                "color": self.color,
                "trace": [(x, y)],
                "thickness": self.thickness,
                "pixels": self.pixels
            })

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        if self.traces:
            if self.tool.name == "SPRAY":
                self.tool.spray_points(self.traces[-1], x, y)
            elif self.tool.name == "ERASER":
                self.tool.erase_traces(self.traces, x, y)
            else:
                self.traces[-1]["trace"].append((x, y))

    def on_draw(self):
        self.clear()
        for tool in self.used_tools.values():
            if tool.name != "ERASER":
                tool.draw_traces(self.traces)


if __name__ == "__main__":
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    # Invocacion: python main.py [ruta/a/dibujo.json]
    if len(sys.argv) > 1:
        app = Paint(sys.argv[1])
    else:
        app = Paint()
    window.show_view(app)
    arcade.run()
