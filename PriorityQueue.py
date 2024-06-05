import heapq


class PriorityQueue:
    """
    A priority queue implementation with support for custom ordering.

    Attributes:
        - use_priority_func2 (bool): Indicates whether the priority queue uses two priority functions.
        - heap (list): The underlying heap data structure.
        - priority_func (function): The primary priority function used for ordering.
        - priority_func2 (function): The secondary priority function used for ordering if provided.

    Methods:
        - __init__: Initializes a PriorityQueue instance with specified priority functions.
        - append: Adds an item to the priority queue with its priority determined by the specified functions.
        - pop: Removes and returns the item with the highest priority from the priority queue.
        - peek: Returns the item with the highest priority without removing it from the priority queue.
        - remove: Removes a specific item from the priority queue.
        - heapify: Creates a heap from the provided list based on custom ordering.
        - copy_heap_to_list: Creates a copy of the priority queue's heap in the form of a list.
        - is_empty: Checks if the priority queue is empty.
        """

    use_priority_func2 = False

    def __init__(self, priority_func, priority_func2=None):
        """
        Initializes a PriorityQueue instance.

        Parameters:
            - priority_func (function): The primary priority function used for ordering.
            - priority_func2 (function): The secondary priority function used for ordering if provided.
        """

        self.heap = []
        self.priority_func = priority_func
        self.priority_func2 = priority_func2
        self.use_priority_func2 = priority_func2 is not None

    def append(self, item):
        """
        Adds an item to the priority queue with its priority determined by the specified functions.

        Parameters:
            - item: The item to be added to the priority queue.
        """

        # if 2 custom orderings are provided:
        if self.use_priority_func2:
            heapq.heappush(self.heap, (self.priority_func(item), self.priority_func2(item), item))
        # if 1 custom ordering is provided
        else:
            heapq.heappush(self.heap, (self.priority_func(item), item))

    def pop(self):
        """
        Removes and returns the item with the highest priority from the priority queue.

        Returns:
        The item with the highest priority.
        """

        # raise an exception if the heap is empty
        if self.is_empty():
            raise IndexError("pop from an empty priority queue")

        # if 2 custom orderings are used
        if self.use_priority_func2:
            # heappop returns a tuple that contains the custom ordering values and
            # the item, so we ignore the custom ordering values and only take the item
            _, _, item = heapq.heappop(self.heap)
            return item

        # if 1 custom ordering1 is used
        else:
            # heappop returns a tuple that contains the custom ordering values and
            # the item, so we ignore the custom ordering values and only take the item
            _, item = heapq.heappop(self.heap)
            return item

    def peek(self):
        """
        Returns the item with the highest priority without removing it from the priority queue.

        Returns:
        The item with the highest priority.
        """

        # raise an exception if the heap is empty
        if self.is_empty():
            raise IndexError("pop from an empty priority queue")

        # if 2 custom orderings are used
        if self.use_priority_func2:
            # heappop returns a tuple that contains the custom ordering values and
            # the item, so we ignore the custom ordering values and only take the item
            _, _, item = self.heap[0]
            return item
        else:
            # heappop returns a tuple that contains the custom ordering values and
            # the item, so we ignore the custom ordering values and only take the item
            _, item = self.heap[0]
            return item

    def remove(self, item):
        """
        Removes a specific item from the priority queue.

        Parameters:
            - item: The item to be removed from the priority queue.
        """

        # if 2 custom orderings are used
        if self.use_priority_func2:
            self.heap.remove((self.priority_func(item), self.priority_func2(item), item))

        # if 1 custom ordering1 is used
        else:
            self.heap.remove((self.priority_func(item), item))

    def heapify(self, list1):
        """
        Creates a heap from the provided list based on custom ordering.

        Parameters:
            - list1 (list): The list to be converted into a heap.
        """

        # create a list of tuples where each element contains the priority values
        # used for custom orderings, followed by the element to be added

        # if 2 custom orderings are used
        if self.use_priority_func2:
            self.heap = [(self.priority_func(process), self.priority_func2(process), process) for process in list1]
        # if 1 custom ordering1 is used
        else:
            self.heap = [(self.priority_func(process), process) for process in list1]

        # heapify the list created to be in the desired ordering
        heapq.heapify(self.heap)

    def copy_heap_to_list(self):
        """
        Creates a copy of the priority queue's heap in the form of a list.

        Returns:
            A list containing the items from the priority queue's heap.
        """
        if self.use_priority_func2:
            list_heap = [process[2] for process in self.heap]
        else:
            list_heap = [process[1] for process in self.heap]

        return list_heap

    def is_empty(self):
        """
        Checks if the priority queue is empty.

        Returns:
            True if the priority queue is empty, False otherwise.
        """
        return len(self.heap) == 0
