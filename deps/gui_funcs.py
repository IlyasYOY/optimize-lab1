import re
import tkinter

from deps.utils import Config, dump_config, ALGORITHMS

float_match = re.compile("^[-+]?(\d+([.,]\d*)?|[.,]\d+)([eE][-+]?\d+)?$")


def gui_interface(config: Config):
    def validate(var: tkinter.StringVar, default: str):
        if float_match.match(var.get()) is None:
            var.set(default)
        else:
            f = float(var.get())
            if var is prec_entry_var:
                config.precision = f
            elif var is a_entry_var:
                config.a = f
            elif var is step_entry_var:
                if f > 0:
                    config.step = f
                else:
                    var.set(default)

    def on_closing():
        dump_config(config)
        root.destroy()

    root = tkinter.Tk()
    root.title('Лабораторная работа №1')

    # Algorithms chooser
    algorithm = tkinter.StringVar(root)
    for text in ALGORITHMS:
        radio_button = tkinter.Radiobutton(root)
        radio_button['text'] = text
        radio_button['variable'] = algorithm
        radio_button['value'] = text

        if not config.algorithm == text:
            radio_button.deselect()
        else:
            radio_button.select()

        def on_radio_button():
            config.algorithm = algorithm.get()

        radio_button['command'] = on_radio_button
        radio_button.pack()

    start_button = tkinter.Button(root, text='Начать алгоритм')
    start_button.pack()

    step_entry_var = tkinter.StringVar(root)
    step_entry = tkinter.Entry(root, textvariable=step_entry_var)
    step_entry.insert(0, str(config.step))
    step_entry_label = tkinter.Label(root, text='Шаг')

    step_entry_var.trace('w', lambda nm, idx, mode, var=step_entry_var: validate(var, str(config.step)))
    step_entry_label.pack()
    step_entry.pack()

    prec_entry_var = tkinter.StringVar(root)
    prec_entry = tkinter.Entry(root, textvariable=prec_entry_var)
    prec_entry.insert(0, str(config.precision))
    prec_entry_label = tkinter.Label(root, text='Точность')

    prec_entry_var.trace('w', lambda nm, idx, mode, var=prec_entry_var: validate(var, str(config.precision)))
    prec_entry_label.pack()
    prec_entry.pack()

    a_entry_var = tkinter.StringVar(root)
    a_entry = tkinter.Entry(root, textvariable=a_entry_var)
    a_entry.insert(0, str(config.a))
    a_entry_label = tkinter.Label(root, text='Параметр a')

    a_entry_var.trace('w', lambda nm, idx, mode, var=a_entry_var: validate(var, str(config.a)))

    a_entry_label.pack()
    a_entry.pack()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
