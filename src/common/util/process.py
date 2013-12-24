from multiprocessing import Process, Queue

def process(fn, state=None):
    """
    fn: function to call, 1 arg if state is not None, 0 args otherwise
    state: optional state to pass to the function
    return: the queue which will be provided the return value of the function
    """

    queue = Queue(1)
    Process(target=process_fn, args=(fn, queue, state)).start()
    return queue

def process_fn(fn, queue, state):
    if state is not None:
        ret = fn(state)
    else:
        ret = fn()

    queue.put(ret)

def get_latest(queue):
    ret = None

    while not queue.empty():
        ret = queue.get()

    return ret
