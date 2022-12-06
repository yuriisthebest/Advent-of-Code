import os
import shutil


def generate_year(year: int) -> None:
    """
    Create all files and folders for the supplied year
    This includes: Python files for tasks, data files for inputs, answers json,

    :param year: The year to generate a folder for
    """
    template_folder = os.path.dirname(os.getcwd()) + f"\\templates\\"
    new_folder = os.path.dirname(os.getcwd()) + f"\\years\\AoC{year}\\"
    new_data_folder = new_folder + "data\\"
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
    if not os.path.exists(new_data_folder):
        os.makedirs(new_data_folder)
    # Init file
    with open(new_folder + "__init__.py", 'w'):
        pass
    # Task files
    for day in range(1, 26):
        with open(template_folder + "task_template.py", 'r') as template_file:
            template = template_file.read()
        template = template.replace('8000', str(year))
        template = template.replace('9999', str(day))
        with open(new_folder + f"task_{day}.py", 'w') as task_file:
            task_file.write(template)
    # Tasks collection
    with open(template_folder + "tasks_template.py", 'r') as template_file:
        template = template_file.read()
    template = template.replace('9999', str(year))
    with open(new_folder + "tasks.py", 'w') as tasks:
        tasks.write(template)
    # Answers JSON
    shutil.copy2(template_folder + "answers.json", new_data_folder)
    # txt files
    for day in range(1, 26):
        # TODO: Use API to automatically fill data
        with open(new_data_folder + f"task{day}_data.txt", 'w'):
            pass
        with open(new_data_folder + f"task{day}_test.txt", 'w'):
            pass
    print(f"Successfully created an AoC folder for: {year}")


if __name__ == "__main__":
    generate_year(6000)
