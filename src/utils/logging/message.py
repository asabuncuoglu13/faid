# %%
import sys
# %%
def error_msg(msg):
    """
    Print an error message with red color and exit
    """
    print(f"\033[91m{msg}\033[0m")
    sys.exit(1)


# %%
def success_msg(msg):
    """
    Print a success message with green color
    """
    print(f"\033[92m{msg}\033[0m")


# %%
def info_msg(msg):
    """
    Print an info message with blue color
    """
    print(f"\033[94m{msg}\033[0m")


# %%
def warning_msg(msg):
    """
    Print a warning message with yellow color
    """
    print(f"\033[93m{msg}\033[0m")