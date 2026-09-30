import tkinter as tk
from dataclasses import dataclass

@dataclass
class DesktopNotifierConfiguration:
    title: str = "MAIL DETECTED"
    description: str = "CHECK YOUR MAILS!"
    position: str = "center"
    position_margin: int = 0

class DesktopNotifier:
    def __init__(self, configuration: DesktopNotifierConfiguration):
        self.message_title = configuration.title
        self.message_description = configuration.description
        self.message_position = configuration.position
        self.message_position_margin = configuration.position_margin

    def show_notification(self) -> None:
        root = tk.Tk()
        root.title(self.message_title)
        root.resizable(False, False)
        root.attributes("-topmost", True)

        root.geometry(f"400x180")

        container = tk.Frame(
            root,
            padx=20,
            pady=15
        )
        container.pack(fill="both", expand=True)

        message = tk.Label(
            container,
            text=self.message_description,
            font=("Segoe UI", 10),
            anchor="nw",
            justify="left",
            wraplength=350
        )
        message.grid(
            row=1,
            column=0,
            sticky="new"
        )

        dismiss_button = tk.Button(
            container,
            text="Dismiss",
            command=root.destroy,
            width=12
        )
        dismiss_button.grid(
            row=2,
            column=0,
            sticky="e",
            pady=(10, 0)
        )

        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self._position_window(root)

        root.mainloop()

    def _position_window(self, root: tk.Tk) -> None:
        root.attributes("-alpha", 0.0)
        root.update()

        titlebar = root.winfo_rooty() - root.winfo_y()
        border = root.winfo_rootx() - root.winfo_x()

        width = root.winfo_width() + 2 * border
        height = root.winfo_height() + titlebar + border

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x, y = self._compute_coordinates(screen_width, screen_height, width, height)

        root.geometry(f"+{x}+{y}")
        root.attributes("-alpha", 1.0)


    def _compute_coordinates(self, screen_width: int, screen_height: int, width: int, height: int) -> tuple[int, int]:
        margin = self.message_position_margin
        if self.message_position == "top-left":
            return (margin, margin)
        if self.message_position == "top-right":
            return (screen_width - width - margin, margin)
        if self.message_position == "bottom-left":
            return (margin, screen_height - height - margin)
        if self.message_position == "bottom-right":
            return (screen_width - width - margin, screen_height - height - margin)
        return ((screen_width - width) // 2, (screen_height - height) // 2)