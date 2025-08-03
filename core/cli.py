# core/cli.py

import os
import msvcrt

from core.config_loader import load_config, get_nested, get_rendered
from core.menu_registry import discover_actions, get_label

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def start_cli():
    
    ui = load_config("ui_text.json")
    actions = discover_actions()

    while True:

        # Display Main Menu Header
        clear_screen()
        print(ui.get("program_title", "PROGRAM TITLE"))
        print(get_nested(ui,"main_menu.title","UNTITLED"))
        print()

        for i, action in enumerate(actions, 1):
            label = get_label(ui, action["label_key"])
            print(f"{i}. {label}")
        print(f"{len(actions)+1}. Quit Application\n")

        choice = input(get_nested(ui,"prompts.select_menu_item","SELECT MENU ITEM")).strip()

        if choice == str(len(actions)+1):
            print(get_nested(ui,"messages.goodbye","GOODBYE"))
            break

        try:

            index = int(choice) - 1
            selected = actions[index]

        except (ValueError, IndexError):
            input(get_rendered(ui,"prompts.invalid_choice_continue",choice=choice))
            continue

        handle_action(ui, selected)

def handle_action(ui, action):

    # Display Sub-Menu Header
    clear_screen()
    subtitle = get_label(ui, action["label_key"])
    print(ui.get("program_title", "PROGRAM TITLE"))
    print(subtitle)
    print()

    # Unknown Action Invoked
    executor = action["executor"]
    if executor is None:
        print(get_nested(ui,"prompts.not_implemented","NOT IMPLEMENTED"))
        msvcrt.getch()
        return
    
    try:

        answers = executor()

        if answers is None:
            print(get_nested(ui,"prompts.not_implemented","NOT IMPLEMENTED"))
            msvcrt.getch()
            return

        if answers.get("requires_confirmation", False):
            print(get_nested(ui,"messages.review_answers", "REVIEW ANSWERS:  "))
            for key, val in answers.items():
                if key not in {"execute", "requires_confirmation"}:
                    print(f"{key}: {val}")
            print()

            decision = input(get_nested(ui,"prompts.confirm","1 TO ACCEPT, 2 TO EDIT, 3 TO CANCEL")).strip()
            if decision == "1":
                try:
                    result = answers["execute"]()
                    print(ui.get("action_success", "{action} completed successfully.").replace("{action}", subtitle))
                except Exception as e:
                    print(ui.get("action_failed", "{action} failed: {error}")
                        .replace("{action}", subtitle)
                        .replace("{error}", str(e)))
                    raise
                msvcrt.getch()
            elif decision == "2":
                handle_action(ui, action)
            else:
                return
        else:
            print(ui.get("please_wait", "Please wait while I {action}...")
                .replace("{action}", subtitle))
            try:
                result = answers["execute"]()
                print(ui.get("action_success", "{action} completed successfully.").replace("{action}", subtitle))
            except Exception as e:
                print(ui.get("action_failed", "{action} failed: {error}")
                    .replace("{action}", subtitle)
                    .replace("{error}", str(e)))
                raise
            msvcrt.getch()
    except Exception as e:
        print(f"Error collecting input: {e}")
        raise
    finally:
        return