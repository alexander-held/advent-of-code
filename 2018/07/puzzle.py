import fileinput
from itertools import count

x = [line.strip() for line in fileinput.input()]

requirement_map = [(line[36], line[5]) for line in x]  # tuples (step, requirement)
all_tasks = set("".join([r[0] + r[1] for r in requirement_map]))


def get_next_tasks(all_tasks: set, tasks_done: list, requirement_map: list):
    tasks_possible = set()
    for candidate in all_tasks - set(tasks_done):
        # get requirements for candidate
        requirements = set([r[1] for r in requirement_map if r[0] == candidate])
        if len(requirements - set(tasks_done)) == 0:
            tasks_possible.add(candidate)  # all (if any) requirements are satisfied
    return sorted(tasks_possible)  # next steps in alphabetic order


tasks_done = []
while len(tasks_done) < len(all_tasks):
    tasks_done.append(get_next_tasks(all_tasks, tasks_done, requirement_map)[0])

print(f"part 1: {''.join(tasks_done)}")


time_per_step = lambda c: ord(c) - 64 + 60
NUM_WORKERS = 5

tasks_done = []
active_tasks = [None] * NUM_WORKERS  # tracks active tasks
task_timer = [0] * NUM_WORKERS  # countdown timers for tasks done by both workers
for t in count():
    # find workers which finished their tasks (time <= 0)
    workers_done = [i for i, t in enumerate(task_timer) if t <= 0]
    for worker_id in workers_done:
        # previously active task of this worker is now done
        if active_tasks[worker_id] is not None:
            tasks_done.append(active_tasks[worker_id])
            active_tasks[worker_id] = None

    # second loop to assign new tasks to workers (separate loop to ensure tasks_done is
    # fully updated before doing so)
    for worker_id in workers_done:
        choices = get_next_tasks(all_tasks, tasks_done, requirement_map)
        # pick first available task that is not already being worked on
        next_task = next((task for task in choices if task not in active_tasks), None)
        if next_task is not None:
            active_tasks[worker_id] = next_task
            task_timer[worker_id] = time_per_step(next_task)

    # one second passes and timers advance
    task_timer = [t - 1 for t in task_timer]

    if len(tasks_done) == len(all_tasks):
        print(f"part 2: {t}")
        break
