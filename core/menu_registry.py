import importlib
import os
import json

def discover_actions(action_path="actions"):
    base_dir = os.path.dirname(__file__) # This points to core/
    actions_folder = os.path.join(base_dir,action_path)

    registry = []
    for filename in os.listdir(actions_folder):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            module_path = ".".join(["core",action_path,module_name])
            try:
                mod = importlib.import_module(f"{module_path}")
                registry.append({
                    "id": getattr(mod, "menu_id", module_name),
                    "label_key": getattr(mod, "label_key", f"main_menu.{module_name}"),
                    "executor": getattr(mod, "execute", None)
                })
            except Exception as e:
                print(f"Error loading module {module_name}: {e}")
                raise
    return registry

def get_label(ui_text, key_path, default="(missing label)"):
    section, key = key_path.split(".")
    return ui_text.get(section, {}).get(key, default)

def standardize_action_output(workflow_func, answers=None, requires_confirmation=True,**metadata):
    """
    Wraps a workflow function and optional answers into a standardized action output.

    Parameters:
        workflow_func (callable): The function that performs the action.
        answers (dict, optional): Any collected user input.
        metadata (dict): Optional metadata like description, confirmation flags, etc.

    Returns:
        dict: A standardized action output with keys:
            - answers (if provided)
            - execute (callable)
            - any extra metadata
    """
    output = {
        "execute": workflow_func, "requires_confirmation": requires_confirmation
    }
    if answers:
        output.update(answers)
    output.update(metadata)
    return output