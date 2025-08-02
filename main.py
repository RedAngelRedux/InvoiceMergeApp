from core.cli import start_cli

def main():

    try:
        start_cli()
    except Exception as e:
        print(f"An unexpected error occured:  {e}")
        
if __name__ == '__main__':
    main()