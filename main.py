import fire

from deps.cli_funcs import cli_interface
from deps.gui_funcs import gui_interface
from deps.utils import load_config


def main():
    fire.Fire({
        "gui": lambda: gui_interface(load_config()),
        "cli": lambda: cli_interface(load_config())
    }, 'gui')


if __name__ == '__main__':
    main()
