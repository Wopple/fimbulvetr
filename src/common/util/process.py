from multiprocessing import Process, Queue

# PUBLIC

def process(fn, queue=None, state=None):
    """
    Runs a function on a new process. The return value is passed to the queue
    returned by this function. An optional argument can be provided to the
    function.

    fn: function to call, 1 arg if state is not None, 0 args otherwise
    queue: optional queue to use as the result queue
    state: optional state to pass to the function
    return: the queue which will be provided the return value of the function
    """

    if queue is None:
        queue = Queue(1)

    Process(target=process_fn, args=(fn, queue, state)).start()
    return queue

def getLast(queue):
    """
    queue: queue to empty
    return: the last item in the queue
    """

    ret = None

    while not queue.empty():
        ret = queue.get()

    return ret

# PRIVATE

def process_fn(fn, queue, state):
    if state is not None:
        ret = fn(state)
    else:
        ret = fn()

    queue.put(ret)
