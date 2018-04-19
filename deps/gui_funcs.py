import tkinter

from deps.utils import Config, dump_config


def gui_interface(config: Config):
    root = tkinter.Tk()
    root.title('Лабораторная работа №1')

    def on_closing():
        dump_config(config)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
