import time
import functools
import numpy as np
from utils.colors import textcolors as tc


def timer(year: int, task: int):
    def timer_decorator(func):
        """Print the run-time of the given function"""
        @functools.wraps(func)
        def timer_wrapper(*args, **kwargs):
            start = time.perf_counter()
            value = func(*args, **kwargs)
            run_time = time.perf_counter() - start
            print(f"{tc.HEADER}Finished {tc.OKBLUE}({year}) task {task} {func.__name__!r}{tc.ENDC} in "
                  f"{tc.OKCYAN}{run_time:.4f} secs{tc.ENDC}")
            return value
        return timer_wrapper
    return timer_decorator


def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"{tc.HEADER}Calling {func.__name__}({tc.ENDC}{signature}{tc.HEADER}){tc.ENDC}")
        value = func(*args, **kwargs)
        print(f"{tc.OKBLUE}{func.__name__!r}{tc.ENDC} returned {tc.OKCYAN}{value!r}{tc.ENDC}")
        return value
    return wrapper_debug


def debug_shape(func):
    """Print the length of the function signature and the return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) if not hasattr(a, '__len__') else str(np.shape(a)) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"{tc.HEADER}Calling {func.__name__}({tc.ENDC}{signature}{tc.HEADER}){tc.ENDC}")
        value = func(*args, **kwargs)
        print(f"{tc.OKBLUE}{func.__name__!r}{tc.ENDC} returned {tc.OKCYAN}{value!r}{tc.ENDC}")
        return value
    return wrapper_debug


if __name__ == "__main__":
    @debug
    @timer(-1, 0)
    def run_test(init_m: int, init_n: int):
        def ackermann(m: int, n: int):
            if m == 0:
                return n + 1
            if n == 0:
                return ackermann(m - 1, 1)
            return ackermann(m - 1, ackermann(m, n - 1))

        return ackermann(init_m, init_n)

    for j in range(7):
        for i in [0, 1, 2, 3]:
            run_test(i, j)
