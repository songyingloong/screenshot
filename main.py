import tkinter as tk
import pyautogui
from tkinter import filedialog


class Application:
    def __init__(self, with_mask=False, mask_color='blue'):
        self._x0, self._y0 = -1, -1
        self._x1, self._y1 = -1, -1
        self._rect = None

        self._with_mask, self._mask_color = with_mask, mask_color

        self._root = tk.Tk()
        # make the main window full-screen
        self._root.attributes('-fullscreen', True)
        # make the main window transparent
        self._root.attributes('-alpha', 0.3)

        self._canvas = tk.Canvas(self._root, bg='White', highlightthickness=1, cursor='cross')
        self._canvas.pack(fill=tk.BOTH, expand=True)
        self._canvas.bind("<ButtonPress-1>", self.on_button_press)
        self._canvas.bind("<B1-Motion>", self.on_button_move)
        self._canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def run(self):
        self._root.mainloop()

    def on_button_press(self, event):
        self._x0, self._y0 = event.x, event.y
        self._rect = self._canvas.create_rectangle(self._x0, self._y0, 1, 1, fill=self._mask_color)
        print(f'button pressed at ({self._x0}, {self._y0})')

    def on_button_move(self, event):
        cur_x, cur_y = event.x, event.y

        # expand rectangle as you drag the mouse
        self._canvas.coords(self._rect, self._x0, self._y0, cur_x, cur_y)

    def on_button_release(self, event):
        self._x1, self._y1 = event.x, event.y
        if not self._with_mask:
            self._root.attributes('-alpha', 0)
            self._root.update()

        print(f'button released at ({self._x1}, {self._y1})')

        # Trigger screenshot
        self.take_screenshot()

    def take_screenshot(self):
        if self._x0 < 0 or self._y0 < 0 or self._x1 < 0 or self._y1 < 0:
            print(f'Failed to detect rectangle: ({self._x0, self._y0, self._x1, self._y1})')
            self._root.quit()

        if self._x0 == self._x1 or self._y0 == self._y1:
            print(f"Failed to take screenshot because the rectangle's area is 0")

        if self._x0 < self._x1 and self._y0 < self._y1:
            pass
        elif self._x0 < self._x1 and self._y0 > self._y1:
            self._y0, self._y1 = self._y1, self._y0
        elif self._x0 > self._x1 and self._y0 > self._y1:
            self._x0, self._x1 = self._x1, self._x0
            self._y0, self._y1 = self._y1, self._y0
        else:
            self._x0, self._x1 = self._x1, self._x0

        region = (self._x0, self._y0, self._x1 - self._x0, self._y1 - self._y0)
        screenshot = pyautogui.screenshot(region=region)
        try:
            output = filedialog.asksaveasfilename(defaultextension='.png')
            screenshot.save(output)
        except Exception as e:
            print(e)
        finally:
            self._root.quit()


def main():
    app = Application()
    app.run()


if __name__ == '__main__':
    main()
