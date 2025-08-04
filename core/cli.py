# core/cli.py

import os
import msvcrt

from core.config_loader import load_config, get_nested, get_rendered
from core.menu_registry import discover_actions, get_label
from core.utils.error_handler import non_fatal

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def display_menu_header(menu_titie,app_title=None):

    if app_title is None:
        app_title="APPLICATION NAME"

    clear_screen()
    print(app_title)
    print(menu_titie)
    print()

def start_cli():
    
    ui = load_config("ui_text.json")
    actions = discover_actions()

    no_fatal_error = True

    while no_fatal_error:

        # Display Main Menu Header
        display_menu_header(
            get_nested(ui,"main_menu.title","UNTITLED"),
            get_nested(ui,"program_title","PROGRAM TITLE")
        )

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
            non_fatal(get_rendered(ui,"prompts.invalid_choice_continue",choice=choice))
            continue

        no_fatal_error = handle_action(ui, selected)

def handle_action(ui, action) -> bool:

    # Display Sub-Menu Header
    subtitle = get_label(ui, action["label_key"])
    display_menu_header(
        subtitle,
        get_nested(ui,"program_title","PROGRAM TITLE")
    )

    # Unknown Action Invoked
    executor = action["executor"]
    if executor is None: 
        non_fatal(get_nested(ui,"prompts.not_implemented","NOT IMPLEMENTED"))
        return True
    
    try:

        answers = executor()  # True is completed successfully, False if fatal error occurred, None if Operation abourted

        if answers is None:            
            return True

        if answers.get("requires_confirmation", False):
            print()
            print(get_nested(ui,"messages.review_answers", "REVIEW ANSWERS:  "))
            print()
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
                return True
        else:
            print(ui.get("please_wait", "\nInitiating {action}: ")
                .replace("{action}", subtitle))
            try:
                return answers["execute"]()
                #print(ui.get("action_success", "{action} completed successfully.").replace("{action}", subtitle))
            except Exception as e:
                print(ui.get("action_failed", "{action} failed: {error}")
                    .replace("{action}", subtitle)
                    .replace("{error}", str(e)))
                raise
            msvcrt.getch()
    except Exception as e:
        print(f"Error collecting input: {e}")
        raise
    # finally:
    #     return True