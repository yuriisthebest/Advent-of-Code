import heapq


class PriorityQueue:
    def __init__(self, tag: str):
        self.queue = []
        self.sort_tag = tag

    def add(self, element):
        heapq.heappush(self.queue, (element.get(self.sort_tag), element))

    def take_first(self):
        element = heapq.heappop(self.queue)[1:]
        return element if len(element) > 1 else element[0]

    def __len__(self) -> int:
        return len(self.queue)

    def __repr__(self) -> str:
        return f"({self.queue}, size={len(self)})"
