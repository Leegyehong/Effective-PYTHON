# I/O를 할 때는 코루틴을 사용해 동시성을 높여라

# 파이썬은 높은 I/O 동시성을 처리하기 위해 코루틴을 사용한다
# 코루틴을 사용하면 동시에 실행되는 것처럼 보이는 함수를 아주 많이 쓸 수 있다
# 코루틴은 async 와 await 키워드를 사용해 구현된다

# await 에서 일시중단되고, 일시 중단된 대기 가능성이 해결된 다음에 asyncs 로부터 실행을 재개한다
# 여러 분리된 asyncs 함수가 서로 장단을 맞춰 실행되면 마치 모든 async함수가 동시에 실행되는 것처럼 보인다

from queue import Queue
from threading import Thread
from threading import Lock
import time

from queue import Queue
# 파이썬 3.6이하에서는 실행되지 않는다.

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
logic_queue = ClosableQueue()
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
    # 여기서 블러킹 I/O를 수행한다
    #data = my_socket.recv(100)
    return count

async def game_logic(state, neighbors):
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY # 살아 있는 이웃이 너무 적음: 죽음
        elif neighbors > 3:
            return EMPTY # 살아 있는 이웃이 너무 많음: 죽음
    else:
        if neighbors == 3:
            return ALIVE # 다시 생성됨

    # 여기서 I/O를 수행한다
    #data = await my_socket.recv(100)
    return state

async def step_cell(y, x, get, set):
    state = get(y, x)
    neighbors = count_neighbors(y, x, get)
    next_state = await game_logic(state, neighbors)
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

import asyncio

async def simulate(grid):
    next_grid = Grid(grid.height, grid.width)

    tasks = []
    for y in range(grid.height):
        for x in range(grid.width):
            task = step_cell(
                y, x, grid.get, next_grid.set)  # 팬아웃
            tasks.append(task)

    await asyncio.gather(*tasks)  # 팬인

    return next_grid
# step_cell을 호출해도 이 함수가 즉시 호출되지 않는다 
# => 대신 step_cell 호출은 나중에 await 식에 사용될 수 있는 coroutine 인스턴스를 반환한다
# asyncio 내장 라이브러리가 제공하는 gather 함수는 팬인을 수행한다
# => gather에 대해 적용한 await 식은 이벤트 루프가 step_cell 코루틴을 동시에 실행하면서 step_cell 코루틴이 완료될 때마다 simulate 코루틴 실행을 재개하라고 요청한다
# 모든 실행이 단일 스레드에서 이뤄지므로 Grid 인스턴스에 락을 사용할 필ㄹ요가 없다  
grid = Grid(5, 9)
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)

columns = ColumnPrinter()
for i in range(5):
    columns.append(str(grid))
    # python 3.7이상에서만 asyncio.run을 제공함
    grid = asyncio.run(simulate(grid)) # 이벤트 루프를 실행한다

print(columns)