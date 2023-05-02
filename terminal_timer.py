import time
from functools import wraps
from yaspin import yaspin
from yaspin.spinners import Spinners


def loading_spinner_decorator(func):
    # Function Name
    func_name = func.__name__

    # Package Name
    package_name = func.__module__

    text = f"{package_name}.{func_name}"

    @wraps(func)
    def wrapper(*args, **kwargs):
        with yaspin(Spinners.bouncingBar, text=text, color="cyan") as sp:
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            time_elapsed = end_time - start_time

            sp.ok(f"✅ {time_elapsed:.2f}s")
        # print(f"Function completed in {time_elapsed:.2f} seconds")
        return result

    return wrapper


# Example usage
@loading_spinner_decorator
def my_function():
    time.sleep(2)


if __name__ == "__main__":
    my_function()
