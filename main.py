import builtins
from datetime import datetime

from bot import main

_original_print = builtins.print


def _print_with_datetime(*args, **kwargs):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _original_print(f"[{timestamp}]", *args, **kwargs)


builtins.print = _print_with_datetime

if __name__ == "__main__":
    main()
