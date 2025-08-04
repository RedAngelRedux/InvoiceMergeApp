# core/utils/uiux.py
from pathlib import Path

def file_exists(filename) -> bool:
    path = Path(filename)
    if path.exists(): return True
    else: return False

def folder_exists(foldername) -> bool:
    if not file_exists(foldername): 
        return False
    else:
        path = Path(foldername)
        if path.is_dir(): 
            return True
        else: 
            return False

def prompt_filename(
    prompt="Enter a file name",
    cancel_keyword="cancel",
    default=None,
    validate_exists=False,
    validate_is_folder=False,
    allowed_extensions=None,
    max_retries=3
):
    """
    Prompts the user for a file or folder name with optional validation.

    Args:
        prompt (str): The prompt message.
        cancel_keyword (str): Keyword to cancel the operation.
        default (str): Default value to use if user presses Enter.
        validate_exists (bool): Whether to check if the path exists.
        validate_is_folder (bool): If True, validates that the path is a folder.
        allowed_extensions (list[str]): List of allowed file extensions (e.g. ['.csv', '.txt']).
        max_retries (int): Max number of invalid attempts before aborting.

    Returns:
        str or None: The valid path, or None if cancelled or retries exceeded.
    """
    attempts = 0

    while attempts < max_retries:
        suffix = f" (or type '{cancel_keyword}' to abort)"
        if default:
            suffix += f" [default: {default}]"
        user_input = input(f"{prompt}{suffix}: ").strip()

        if not user_input and default:
            user_input = default

        if user_input.lower() == cancel_keyword:
            confirm = input("Are you sure you want to cancel? (y/n): ").strip().lower()
            if confirm == "y":
                print("Operation cancelled.")
                return None
            else:
                continue

        if not user_input:
            print("Please enter a valid path.")
            attempts += 1
            continue

        path = Path(user_input)

        if validate_exists and not path.exists():
            print("Path not found. Please enter a valid path.")
            attempts += 1
            continue

        if validate_is_folder and not path.is_dir():
            print("Expected a folder, but got a file. Please enter a valid folder path.")
            attempts += 1
            continue

        if allowed_extensions and not path.suffix.lower() in allowed_extensions:
            print(f"Invalid file extension. Allowed: {', '.join(allowed_extensions)}")
            attempts += 1
            continue

        return str(path)

    print()
    print("*** Too many invalid attempts. Operation aborted ***")
    return None