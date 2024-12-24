from utils.decorators import timer, debug
from utils.task import Task


class Task24(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 24

    def preprocess(self, data: list) -> tuple:
        values = {}
        connections = {}
        for line in data:
            if line == "":
                continue
            if len(line) == 2:
                values[line[0][:-1]] = line[1] == "1"
            else:
                connections[line[4]] = (line[1], line[0], line[2])
        return values, connections

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: tuple) -> int:
        values, connections = data
        return self.compute_wire_result(connections, values)

    def compute_wire_result(self, connections: dict, values: dict) -> int:
        i = 0
        bits = ""
        while f'z{i:02d}' in connections:
            result, values = self.find_value(values, connections, f'z{i:02d}')
            bits += "1" if result else "0"
            i += 1
        return int(bits[::-1], 2)

    @staticmethod
    def do_operation(operation: str, value_1: bool, value_2: bool) -> bool:
        match operation:
            case "AND":
                return value_1 and value_2
            case "OR":
                return value_1 or value_2
            case "XOR":
                return value_1 != value_2

    def find_value(self, values: dict, connections: dict, key: str) -> tuple:
        if key in values:
            return values[key], values
        else:
            op, key1, key2 = connections[key]
            val1, values = self.find_value(values, connections, key1)
            val2, values = self.find_value(values, connections, key2)
            result = self.do_operation(op, val1, val2)
            values[key] = result
            return result, values

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: tuple) -> str:
        """
        Notes and observations:


        Normal behavior of blocks:
        x and y XOR and 'AND', to nodes we call XOR and 'AND'

        XOR 'XORS' to Z, together with PREV
        XOR also 'ANDS' with PREV to TEMP

        AND 'ORs' to NEXT with TEMP
        NEXT is the PREV for the next block
        -------------------------------------------------

        z06 receives with OR from AND, so z06 and NEXT are swapped.
        Z = zo6, AND is vkd, TEMP is vsv, PREV = scp
        NEXT is called fhc
        It is jnt OR VSV = zo6. vkd XOR scp = fhc
        (zo6, fhc)

        x11
        XOR ANDs to Z and XOR XORs to temp (nmm XOR rmc -> qhj)
        (z11, qhj)

        x23
        XOR does the OR and 'AND' does the XOR and 'AND'
        x and y already go to the wrong places
        (ggt, mwh)

        x35
        AND = Z
        (z35, hqk)
        """
        supress_print = True
        if not supress_print:
            # Print the network for Mermaid online
            values, connections = data
            i = 0
            order_x = {con: connections[con]
                       for con in connections if 'x' in connections[con][1] or 'x' in connections[con][2]}
            for key in order_x:
                i += 1
                ops = connections[key]
                low = ops[1] if ops[1] < ops[2] else ops[2]
                high = ops[1] if not ops[1] < ops[2] else ops[2]
                print(f"{low} --->|{ops[0]}| {key}")
                print(f"{high} --->|{ops[0]}| {key}")
            for key in sorted(connections):
                if key in order_x:
                    continue
                i += 1
                ops = connections[key]
                low = ops[1] if ops[1] < ops[2] else ops[2]
                high = ops[1] if not ops[1] < ops[2] else ops[2]
                print(f"{low} --->|{ops[0]}| {key}")
                print(f"{high} --->|{ops[0]}| {key}")
        return ",".join(sorted(['z06', 'fhc', 'z11', 'qhj', 'ggt', 'mwh', 'z35', 'hqk']))


if __name__ == "__main__":
    # Load task
    t = Task24()

    # Run task
    t.run_all()
