import time
from profilehooks import profile
from multiprocessing import Process
from utils.load import load_answers
from utils.colors import TextColors as Tc
from years.AoC2021.tasks import TASKS2021
from years.AoC2022.tasks import TASKS2022
from years.AoC2023.tasks import TASKS2023
from years.AoC2024.tasks import TASKS2024

# Constants
PARALLEL_COMPUTATION = False
TASKS = {
    # 2021: TASKS2021,
    # 2022: TASKS2022,
    # 2023: TASKS2023,
    2024: TASKS2024
}


def asses_task(task: type, answers: dict, year: int) -> None:
    """
    Run a task 4 times (part 1 test, part 1 task, part 2 test, part 2 task)
    Test if the answers of each run correspond to the correct answers

    :param task: Task object able to run a task
    :param answers: The correct answers of the given task
    :param year: The year when this task was asked
    """
    t = task()
    pred = t.run_all()
    true = answers[task.__name__]
    assert pred[0][0] == true[0] or true[0] == 0, \
        f"({year}, {task.__name__}) Part 1 has failed on the test data. Expected: {true[0]}, got: {pred[0][0]}"
    assert pred[0][1] == true[1] or true[1] == 0, \
        f"({year}, {task.__name__}) Part 1 has failed on the real data. Expected: {true[1]}, got: {pred[0][1]}"
    assert pred[1][0] == true[2] or true[2] == 0, \
        f"({year}, {task.__name__}) Part 2 has failed on the test data. Expected: {true[2]}, got: {pred[1][0]}"
    assert pred[1][1] == true[3] or true[3] == 0, \
        f"({year}, {task.__name__}) Part 2 has failed on the real data. Expected: {true[3]}, got: {pred[1][1]}"


@profile(stdout=False, filename="CodePerformance.prof")
def run_all_tasks():
    start = time.perf_counter()
    num_tests = 0
    processes = []
    for year_num in TASKS.keys():
        # Find the answers of the current year
        year_answers = load_answers(year_num)

        # Compute task results (unknown answers have a value of -1)
        for i, current_task in enumerate(TASKS[year_num]):
            num_tests += 1
            if PARALLEL_COMPUTATION:
                p = Process(target=asses_task, args=(current_task, year_answers, year_num))
                p.start()
                processes.append(p)
            else:
                asses_task(current_task, year_answers, year_num)
    # Wait for processes to stop and report success
    for process in processes:
        process.join()
    end = time.perf_counter()
    print(f"\n{Tc.OKGREEN}*** {num_tests} tests completed successfully in {end - start:.2f} sec***{Tc.ENDC}")


if __name__ == "__main__":
    run_all_tasks()
