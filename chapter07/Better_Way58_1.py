# 동시성과 Queue를 사용하기 위해 코드를 어떻게 리팩토링해야 하는지 이해하라

# Queue 클래스를 사용해 파이프라인을 스레드로 실행하게 구현해볼 것이다
# 일반적인 접근 방법은
# 생명 게임의 세대마다 셀당 하나씩 스레드를 생성하는 대신
# 필요한 병렬 I/O숫자에 맞춰 미리 정해진 작업자 스레드를 만든다
# 프로그램은 이를 통해 자원 사용을 제어하고, 새로운 스레드를 자주 시작하면서 생기는 부가 비용을 덜 수 있다

# 이를 위해 작업자 스레드와 game_logic 함수 사이의 통신에 ClosableQueue 인스턴스 두 개를 사용한다

from queue import Queue
from threading import Thread
from threading import Lock
import time

from queue import Queue

class ClosableQueue(Queue):
    SENTINEL = object()

    def close(self):
        self.put(self.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return   # 스레드를 종료시킨다
                yield item
            finally:
                self.task_done()

in_queue = ClosableQueue()
out_queue = ClosableQueue()

class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue, **kwargs):
        super().__init__(**kwargs)
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)

ALIVE = '*'
EMPTY = '-'

class SimulationError(Exception):
    pass

class Grid:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

    def get(self, y, x):
        return self.rows[y % self.height][x % self.width]

    def set(self, y, x, state):
        self.rows[y % self.height][x % self.width] = state

    def __str__(self):
        output = ''
        for row in self.rows:
            for cell in row:
                output += cell
            output += '\n'
        return output

def count_neighbors(y, x, get):
    n_ = get(y - 1, x + 0) # 북(N)
    ne = get(y - 1, x + 1) # 북동(NE)
    e_ = get(y + 0, x + 1) # 동(E)
    se = get(y + 1, x + 1) # 남동(SE)
    s_ = get(y + 1, x + 0) # 남(S)
    sw = get(y + 1, x - 1) # 남서(SW)
    w_ = get(y + 0, x - 1) # 서(W)
    nw = get(y - 1, x - 1) # 북서(NW)
    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    return count

def game_logic(state, neighbors):
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY # 살아 있는 이웃이 너무 적음: 죽음
        elif neighbors > 3:
            return EMPTY # 살아 있는 이웃이 너무 많음: 죽음
    else:
        if neighbors == 3:
            return ALIVE # 다시 생성됨
    # 여기서 블러킹 I/O를 수행
    #data = my_socket.recv(100)
    return state

def game_logic_thread(item):
    y, x, state, neighbors = item
    try:
        next_state = game_logic(state, neighbors)
    except Exception as e:
        next_state = e
    return (y, x, next_state)

# 스레드를 미리 시작한다
threads = []
for _ in range(5):
    thread = StoppableWorker(
        game_logic_thread, in_queue, out_queue)
    thread.start()
    threads.append(thread)

def step_cell(y, x, get, set):
    state = get(y, x)
    neighbors = count_neighbors(y, x, get)
    next_state = game_logic(state, neighbors)
    set(y, x, next_state)

class ColumnPrinter:
    def __init__(self):
        self.columns = []

    def append(self, data):
        self.columns.append(data)

    def __str__(self):
        row_count = 1
        for data in self.columns:
            row_count = max(
                row_count, len(data.splitlines()) + 1)

        rows = [''] * row_count
        for j in range(row_count):
            for i, data in enumerate(self.columns):
                line = data.splitlines()[max(0, j - 1)]
                if j == 0:
                    padding = ' ' * (len(line) // 2)
                    rows[j] += padding + str(i) + padding
                else:
                    rows[j] += line

                if (i + 1) < len(self.columns):
                    rows[j] += ' | '

        return '\n'.join(rows)

def simulate_pipeline(grid, in_queue, out_queue):
    for y in range(grid.height):
        for x in range(grid.width):
            state = grid.get(y, x)
            neighbors = count_neighbors(y, x, grid.get)
            in_queue.put((y, x, state, neighbors))  # 팬아웃
    in_queue.join()
    out_queue.close()
    next_grid = Grid(grid.height, grid.width)
    for item in out_queue:  # 팬인
        y, x, next_state = item
        if isinstance(next_state, Exception):
            raise SimulationError(y, x) from next_state
        next_grid.set(y, x, next_state)

    return next_grid

grid = Grid(5, 9)
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)

columns = ColumnPrinter()
for i in range(5):
    columns.append(str(grid))
    grid = simulate_pipeline(grid, in_queue, out_queue)

print(columns)

for thread in threads:
    in_queue.close()
for thread in threads:
    thread.join()

# 이 코드의 결과는 이전과 같다
# 하지만 여전히 많은 문제가 남아 있다
# - simulate_pipeline 함수가 더 따라가기 어렵다
# - 코드의 가독성을 개선하려면 ClosableQueue와 StoppableWorker라는 추가 지원 클래스가 필요하며, 이에 따라 복잡도가 늘어난다
# - 병렬성을 활용해 필요에 따라 자동으로 시스템 규모가 확장되지 않는다 => 미리 부하를 예측해서 잠재적인 병렬성수준을 미리 지정해야함
# - 디버깅을 활성화하려면 발생한 예외를 작업 스레드에서 수동으로 잡아 Queue를 통해 전달함으로써 주 스레드에서 다시 발생시켜야함

# 이 코드를 병렬화하려면 count_neighbors를 별도의 스레드에서 실행하는 단계를 파이프라인에 추가해야함