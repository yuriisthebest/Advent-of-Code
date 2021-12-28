PATHS = {
    2020: "C:\\Users\\Yuri\\Documents\\Python\\Advent of Code\\years\\AoC2020",
    2021: "C:\\Users\\Yuri\\Documents\\Python\\Advent of Code\\years\\AoC2021"
}

if __name__ == "__main__":
    YEAR = 2021
    # Create data paths
    for TASK_NUM in range(7, 26):
        with open(f"{PATHS[YEAR]}\\task{TASK_NUM}_test.txt", 'w') as _:
            pass
        with open(f"{PATHS[YEAR]}\\task{TASK_NUM}_data.txt", 'w') as _:
            pass
