import threading
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import emulation as piko


THEME_BG = "#AEAEAE"
THEME_FG = "#1a1a1a"
THEME_ACCENT = "#0b4c2b"
THEME_ACCENT_FG = "#117744"
THEME_FIELD_BG = "#ffffff"
THEME_FONT = ("Helvetica", 10)


def apply_theme(root):
    """Apply the project theme as defaults; per-widget options override these."""
    root.configure(bg=THEME_BG)
    root.option_add("*background", THEME_BG)
    root.option_add("*foreground", THEME_FG)
    root.option_add("*font", THEME_FONT)
    root.option_add("*Entry.background", THEME_FIELD_BG)
    root.option_add("*Text.background", THEME_FIELD_BG)
    root.option_add("*Listbox.background", THEME_FIELD_BG)
    root.option_add("*Button.background", THEME_ACCENT)
    root.option_add("*Button.foreground", THEME_ACCENT_FG)
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    style.configure(".", background=THEME_BG, foreground=THEME_FG, fieldbackground=THEME_FIELD_BG, font=THEME_FONT)


class Application:
    def __init__(self, root) -> None:
        self.root = root
        root.title("PIKO-tkinter")
        root.geometry("1040x720")
        root.update_idletasks()
        root.geometry(
            f"+{(root.winfo_screenwidth() - 1040) // 2}"
            f"+{(root.winfo_screenheight() - 720) // 2}"
        )
        apply_theme(root)

        self.overview = tk.Frame(root, relief="sunken", bd=2)
        self.overview.place(x=520, y=30, width=520, height=690)

        self.PIKO_header = tk.Label(root, text="<PIKO program here>", font=("Helvetica", 14))
        self.PIKO_header.place(x=0, y=0, width=520, height=30)

        self.kao_ongo = tk.Text(root, bg="#111111", fg="#FFFFFF")
        self.kao_ongo.place(x=10, y=30, width=500, height=620)

        self.kao_ongo_output = tk.Label(root, text="<PIKO stuff here>", font=("Helvetica", 14))
        self.kao_ongo_output.place(x=520, y=0, width=520, height=30)

        self.execute = tk.Button(root, text="EKSEKJUT", command=self.on_execute, font=("Helvetica", 13))
        self.execute.place(x=10, y=660, width=170, height=40)

        self.text4 = tk.Text(self.overview, state="disabled")
        self.text4.place(x=20, y=25, width=480, height=320)

        self.text5 = tk.Text(self.overview, state="disabled")
        self.text5.place(x=20, y=370, width=480, height=250)

        self.entry2 = tk.Entry(self.overview, state="readonly")
        self.entry2.place(x=20, y=640, width=480, height=30)

        self.interupt_bt = tk.Button(root, text="INTERAPT", command=self.interrupt, bg="#4c2b0b", fg="#774411", font=("Helvetica", 13), state="disabled")
        self.interupt_bt.place(x=340, y=660, width=170, height=40)

        piko.output_terminal = False

    def on_execute(self) -> None:
        """Runs on click. Starts the slow work without freezing the window."""
        self.input_code = self.kao_ongo.get("1.0", "end-1c")
        self.execute.configure(state="disabled")  # so a double click can't start it twice
        self.interupt_bt.configure(state="normal")
        piko.running = True
        piko.interrupt_outside = False

        threading.Thread(target=self._on_execute_work, daemon=True).start()

    def _on_execute_work(self) -> None:
        result, error = None, None
        try:
            piko.wait_time = 0.000001
            piko.parse_text(self.input_code, is_file=False)
            piko.console()
        except Exception as e:
            error = e
        self.root.after(0, self._on_execute_done, result, error)

    def _on_execute_done(self, result, error) -> None:
        self.execute.configure(state="normal")
        self.interupt_bt.configure(state="disabled")
        if error is not None:
            messagebox.showerror("Something went wrong", str(error))
            return
        # TODO: show the result

    def interrupt(self) -> None:
        piko.interrupt_outside = True
        self.interupt_bt.configure(state="disabled")
        self.execute.configure(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
