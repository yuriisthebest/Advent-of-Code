from utils.decorators import timer, debug
from utils.task import Task
from utils.colors import textcolors as tc


HEX_BITS = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


class Task16(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 16

    def preprocess(self, data: list) -> str:
        """
        Parse Hex string into Binary

        :param data: Hex string
        :return: Binary string formatted using BITS
        """
        return "".join([HEX_BITS[char] for char in data[0]])

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: str) -> int:
        """
        Decode the BITS structure and calculate the sum of all version numbers

        :param data: Binary string formatted using BITS
        :return: The sum of all package version numbers
        """
        return self.identify_packet(data)[0]

    def identify_packet(self, data: str):
        """
        Recursive function to parse the Buoyancy Interchange Transmission System (BITS)

        :param data: Binary string formatted using BITS
        :return: Sum of versions (part 1), Integer determined by operations (part 2), internal index i to track parsing
        """
        # Parse the version and type from the input string
        version = int(data[:3], 2)
        type_id = int(data[3:6], 2)
        # print(self.color(data, type_id, int(data[6])))  # Print each input string
        # Determine the literal value represented by a type id of 4
        if type_id == 4:
            num = ''
            i = 6
            lead = 1
            while lead == 1:
                lead = int(data[i])
                num += data[i+1: i+5]
                i += 5
            return version, int(num, 2), i

        # Check length type id bit to determine formatting
        if int(data[6]) == 0:
            total_length = int(data[7:22], 2)
            current_num = None
            i = 22
            # Parse sub-packages until the specified length of sub-packages is reached
            while i < total_length + 22:
                v, num, j = self.identify_packet(data[i:])
                current_num = self.process_type(type_id, current_num, num)
                version += v
                i += j
            return version, current_num, i

        total_packets = int(data[7:18], 2)
        i = 18
        num_packets = 0
        current_num = None
        # parse sub-packages until the specified amount of sub-packages is reached
        while num_packets < total_packets:
            v, num, j = self.identify_packet(data[i:])
            current_num = self.process_type(type_id, current_num, num)
            version += v
            i += j
            num_packets += 1
        return version, current_num, i

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: str) -> int:
        """
        Evaluate the BITS expression and compute the corresponding number

        :param data: Binary string formatted using BITS
        :return: Number encoded in the BITS transmission
        """
        return self.identify_packet(data)[1]

    @staticmethod
    def process_type(operator: int, current_num, new_num: int):
        """
        Determine the output of an operator based on their current number and a new number

        :param operator: Integer value representing an operator (+ * min max # > < =)
        :param current_num: The current number in memory of the operator
        :param new_num: A new number
        :return: Integer outcome of operator
        """
        if current_num is None:
            return new_num
        if operator == 0:
            return current_num + new_num
        if operator == 1:
            return current_num * new_num
        if operator == 2:
            return min(current_num, new_num)
        if operator == 3:
            return max(current_num, new_num)
        if operator == 4:
            raise ValueError("This should not happen")
        if operator == 5:
            return 1 if current_num > new_num else 0
        if operator == 6:
            return 1 if current_num < new_num else 0
        if operator == 7:
            return 1 if current_num == new_num else 0
        raise ValueError("Specified operator is not valid")

    @staticmethod
    def color(binary: str, type_id: int, length_id: int) -> str:
        """
        Color the characters to visualize the binary formatting
        """
        output = f"{tc.HEADER}{binary[:3]}{tc.WARNING}{binary[3:6]}"
        # Color numbers
        if type_id == 4:
            i = 6
            c = tc.OKGREEN
            while i < len(binary):
                output += f"{c}{binary[i:i+5]}"
                c = tc.OKBLUE if c == tc.OKGREEN else tc.OKGREEN
                i += 5
        # Color nested packages
        else:
            output += f"{tc.OKCYAN}{binary[6]}"
            end = 22 if length_id == 0 else 18
            output += f"{tc.FAIL}{binary[7:end]}{tc.OKGREEN}{binary[end:]}"
        return f"{output}{tc.ENDC}"


if __name__ == "__main__":
    # Load task
    t = Task16()

    # Run task
    t.run_all()
