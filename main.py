import pygame
import pytmx
import sys
from game import run_game
from login import setup_login_page


def show_login(window, action_var, entry_1, entry_2):
    entry_1.delete(0, "end")
    entry_2.delete(0, "end")
    action_var.set("")

    window.deiconify()
    window.lift()
    window.wait_variable(action_var)

    action = action_var.get()
    if action not in {"login", "signup"}:
        return None
    
    window.withdraw()

    return {
        "action": action,
        "username": entry_1.get(),
        "password": entry_2.get()
    }



def main():
    window, action_var, entry_1, entry_2 = setup_login_page()

    while True:
        login_result = show_login(window, action_var, entry_1, entry_2)
        if login_result is None:
            break

        logout = run_game(login_result)
        if not logout:
            break

    window.destroy()


if __name__ == "__main__":
    main()