from utils.paths import PATHS
import json


def __load_json(file_path: str):
    """
    Load a json file

    :param file_path: Path to file to load
    :return: Data from the json
    """
    with open(file_path) as f:
        return json.load(f)


def __load_txt(file_path: str):
    """
    Load a txt file

    :param file_path: Path to file to load
    :return: Data from txt in formatted list
    """
    with open(file_path) as f:
        data = []
        for line in f:
            line = line.strip("\n")
            line = line.split(" ")
            if len(line) == 1:
                line = line[0]
            data.append(line)
    return data


def __load_task(func, extension: str, year: int, task_num: int):
    folder = PATHS[year]
    test = func(f"{folder}\\task{task_num}_test.{extension}")
    task = func(f"{folder}\\task{task_num}_data.{extension}")
    return test, task


def load_task_json(year: int, task_num: int):
    """
    Load a task (test and task data) from json files

    :param year: The year from which the task is
    :param task_num: The task number
    :return: Two datasets from the json files
    """
    return __load_task(__load_json, "json", year, task_num)


def load_task_txt(year: int, task_num: int):
    """
    Load a task (test and task data) from txt files

    :param year: The year from which the task is
    :param task_num: The task number
    :return: Two datasets from the json files
    """
    return __load_task(__load_txt, "txt", year, task_num)


if __name__ == "__main__":
    # Example loads
    print(load_task_json(2021, 1))
    print(load_task_txt(2021, 2))
