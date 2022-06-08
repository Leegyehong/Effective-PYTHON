# 요구에 따라 팬아웃을 진행하려면 새로운 스레드를 생성하지 말라

# 파이썬에서 병렬 I/O를 실행하고 싶을 때는 자연스레 스레드를 가장 먼저 고려하게된다
# 여러 동시 실행 흐름을 만들어내는 팬아웃을 수행하고자 스레드를 사용할 경우 중요한 단점과 마주하게 된다

# 이 단점을 보기 위해 생명 게임을 계속 다룬다

from queue import Queue
from threading import Thread
from threading import Lock
import time

ALIVE = '*'
EMPTY = '-'

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


class LockingGrid(Grid):
    def __init__(self, height, width):
        super().__init__(height, width)
        self.lock = Lock()

    def __str__(self):
        with self.lock:
            return super().__str__()

    def get(self, y, x):
        with self.lock:
            return super().get(y, x)

    def set(self, y, x, state):
        with self.lock:
            return super().set(y, x, state)

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
    #여기서 블로킹 I/O를 수행한다.
    #data = my_socket.recv(100)
    return state

def step_cell(y, x, get, set):
    state = get(y, x)
    neighbors = count_neighbors(y, x, get)
    next_state = game_logic(state, neighbors)
    set(y, x, next_state)


def simulate_threaded(grid):
    next_grid = LockingGrid(grid.height, grid.width)

    threads = []
    for y in range(grid.height):
        for x in range(grid.width):
            args = (y, x, grid.get, next_grid.set)
            thread = Thread(target=step_cell, args=args)
            thread.start()  # 팬아웃
            threads.append(thread)

    for thread in threads:
        thread.join()  # 팬인

    return next_grid

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


grid = LockingGrid(5, 9)            # 바뀐부분
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)

columns = ColumnPrinter()
for i in range(5):
    columns.append(str(grid))
    grid = simulate_threaded(grid)  # 바뀐부분

print(columns)
# step_cell 을 그대로 사용하고, 구동 코드가 LockingGrid와 simulate_threaded 구현을 사용하도록 두 줄만 바꾸면
# 그리드 클래스를 구동할 수 있다

# 코드는 예상대로 잘 작동하며, 스레드 사이에 I/O가 병렬화 됐다
# 하지만 이 코드에는 세 가지 큰 문제점이 있다
# 1. 단일 스레드 코드보다 스레드를 사용하는 코드가 읽기 어렵다
# -> 복잡도 때문에 시간이 지남에 따라 스레드를 사용한 코드를 확장하고 유지보수 하기도 어렵다

# 2. 스레드는 메모리를 많이 사용하며, 스레드 하나당 약 8MB가 더 필요하다
# -> 이 예제처럼 스레드를 45개 정도만 사용하는 경우에는 문제가 되지 않지만 게임 그리드 크기가 10000셀이면 감당할 수 없다

# 3. 스레드를 시작하는 비용이 비싸고, 컨텍스트 전환에 비용이 들기 때문에 성능에 부정적인 영향을 미친다

# 게다가 이 코드는 잘못됐을 때 디버깅하기가 어렵다

# 지속적으로 새로운 동시성 함수를 시작하고 끝내야 하는 경우
# 스레드는 적절한 해법이 아니다