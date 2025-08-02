# core/cli.py

import os
import msvcrt
from core.config_loader import load_config
from core.menu_registry import discover_actions, get_label

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def start_cli():
    ui = load_config("ui_text.json")
    actions = discover_actions()

    while True:
        clear_screen()
        print(ui.get("program_title", "PROGRAM TITLE"))
        print(ui.get("main_menu_title", "Main Menu"))
        print()

        for i, action in enumerate(actions, 1):
            label = get_label(ui, action["label_key"])
            print(f"{i}. {label}")
        print(f"{len(actions)+1}. Quit Application\n")

        choice = input(ui.get("prompt_main_menu", "Please enter the number of the action you'd like to perform: ")).strip()

        if choice == str(len(actions)+1):
            break

        try:
            index = int(choice) - 1
            selected = actions[index]
        except (ValueError, IndexError):
            input("Invalid choice. Press any key to continue...")
            continue

        handle_action(ui, selected)

def handle_action(ui, action):
    clear_screen()
    subtitle = get_label(ui, action["label_key"])
    print(ui.get("program_title", "PROGRAM TITLE"))
    print(subtitle)
    print()

    executor = action["executor"]
    if executor is None:
        print("This action is not yet implemented.")
        msvcrt.getch()
        return
    try:
        answers = executor()
        if answers.get("requires_confirmation", False):
            print(ui.get("review_answers", "Please review your answers:"))
            for key, val in answers.items():
                if key not in {"execute", "requires_confirmation"}:
                    print(f"{key}: {val}")
            print()

            decision = input(ui.get("confirm_prompt", "Press 1 to initiate, 2 to edit, or 3 to cancel: ")).strip()
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