from utils.decorators import timer, debug_shape
from utils.task import Task


class Task9(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 9

    def preprocess(self, data: list) -> tuple:
        blocks = {}
        empties = []
        combined = []
        for i, num in enumerate(data[0]):
            if i % 2 == 0:
                blocks[i // 2] = int(num)
                empty = int(data[0][i+1]) if len(data[0]) > i + 1 else 0
                combined.append([i // 2, int(num), empty])
            else:
                empties.append(int(num))
        return [blocks, empties], combined

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        checksum = 0
        blocks, empties = data[0]
        empties.append(0)
        current_last_id = max(blocks)
        last_id_left_over = blocks[current_last_id]
        # Follow the true index of the filesystem
        i = 0
        for current_id in [block_id for block_id in range(len(blocks))]:
            length = blocks[current_id]
            # print(current_id, length)
            # Calculate position of existing blocks
            for j in range(i, i + length):
                # If we have snooped for the end of the current block, find when to end
                if current_id >= current_last_id and last_id_left_over <= j - i:
                    # print("Ending there", current_id, current_last_id, last_id_left_over, j, j-i)
                    return checksum
                # print(current_id, j, current_id * j, checksum, "read")
                checksum += current_id * j
            i += length
            # Fill the empties with the last blocks
            after_cooldown = empties[current_id]
            for k in range(i, i + after_cooldown):
                # print(current_last_id, k, current_last_id * k, checksum, "snoop")
                checksum += current_last_id * k
                last_id_left_over -= 1
                if last_id_left_over == 0:
                    current_last_id -= 1
                    last_id_left_over = blocks[current_last_id]
                    if current_id == current_last_id:
                        # print("Ending here")
                        return checksum
            i += after_cooldown

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        combined = data[1]
        for current_id in [block_id for block_id in range(len(combined))][::-1]:
            # Find current size of file
            current_file = [file for file in combined if file[0] == current_id][0]
            size = current_file[1]
            # Find place to fit it
            for i, file in enumerate(combined):
                if file[0] == current_id:
                    break
                if size <= file[2]:
                    # Increase the gap behind the one in front of current file
                    file_pos = combined.index(current_file)
                    combined[file_pos - 1][2] += current_file[1] + current_file[2]
                    # Remove the current file
                    combined.remove(current_file)
                    # Set the gap behind current file to the new gap and add it in the correct order
                    current_file[2] = file[2] - size
                    combined.insert(i + 1, current_file)
                    # Remove the gap from the file in front
                    file[2] = 0

        # Calculate checksum based on new order
        i = 0
        checksum = 0
        for file in combined:
            for j in range(i, i + file[1]):
                checksum += file[0] * j
            i += file[1] + file[2]
        return checksum


if __name__ == "__main__":
    # Load task
    t = Task9()

    # Run task
    t.run_all()
