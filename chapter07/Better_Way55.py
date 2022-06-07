# Queue를 사용해 스레드 사이의 작업을 조율하라

# 동시에 여러 일을 수행한다면 각 작업을 잘 조율해야 한다
# 동시성 작업을 처리할 때 가장 유용한 방식은 함수 파이프라인이다

# 예를 들어 디지털 카메라에서 이미지 스트림을 계속 가져와 이미지 크기를 변경하고, 저장하고싶다면
# 3단계 파이프라인으로 나눠서 구성할 수 있다
def download(item):
    return item

def resize(item):
    return item

def upload(item):
    return item

# 가장 먼저 필요한 기능은 파이프라인의 단계마다 작업을 전달할 방법
# 스레드 안전한 producer-consumer 를 사용해 모델링할 수 있다
from collections import deque
from threading import Lock

class MyQueue:
    def __init__(self):
        self.items = deque()
        self.lock = Lock()

    def put(self, item):
        with self.lock:
            self.items.append(item)

    def get(self):
        with self.lock:
            return self.items.popleft()

# 다음 코드는 방금 본 것과 비슷한 큐에서 가져온 작업에 함수를 적용하고
# 그 결과를 다른 큐에 넣는 스레드를 통해 파이프라인의 각 단계를 구현한다
# 그리고 각 작업자가 얼마나 많이 새로운 입력을 폴링했고 얼마나 많이 작업을 완료했는지 추적한다
from threading import Thread
import time

class Worker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

    def run(self):
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                time.sleep(0.01) # 할 일이 없음
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1

download_queue = MyQueue()
resize_queue = MyQueue()
upload_queue = MyQueue()

done_queue = MyQueue()
threads = [
    Worker(download, download_queue, resize_queue),
    Worker(resize, resize_queue, upload_queue),
    Worker(upload, upload_queue, done_queue),
]

for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())

while len(done_queue.items) < 1000:
    # 기다리는 동안 유용한 작업을 수행한다
    pass

processed = len(done_queue.items)
polled = sum(t.polled_count for t in threads)
print(f'{processed} 개의 아이템을 처리했습니다, '
      f'이때 폴링을 {polled} 번 했습니다.')

# 작업이 끝나도 무한대기함. 프로그램을 강제종료시킬것

# 하지만 이것은 문제의 시작일 뿐
# 피해야 할 문제점이 세 가지 있다
# 첫째, 모든 작업이 다 끝났는지 검사하기 위해 추가로 done_queue에 대해 busy waiting 을 수행해야한다
# 둘째, Worker의 run 메서드가 루프를 무한히 반복한다 ( 현재 구현에서는 작업자 스레드에게 루프를 중단할 시점임을 알려줄 뚜렷한 방법이 없다 )
# 셋째, 파이프라인 진행이 막히면 프로그램이 임의로 중단될 수 있다

# 여기서 얻을 수 있는 교훈은 파이프라인이 나쁘다는 것이 아니라, 제대로 작동하는 생산자-소비자 큐를 직접 구현하기가 어렵다는 것
# 따라서 굳이 직접 할 필요가 없다

# Queue 내장 모듈에 있는 Queue클래스는 앞에서 설명한 모든 문제를 해결할 수 있는 기능을 제공한다
# Queue는 새로운 데이터가 나타날 때까지 get메서드가 블록되게 만들어서 작업자의 바쁜 대기 문제를 해결한다
from queue import Queue
from threading import Thread

my_queue = Queue()

def consumer():
    print('소비자 대기')
    my_queue.get()  # 다음에 보여줄 put()이 실행된 다음에 시행된다
    print('소비자 완료')

thread = Thread(target=consumer)
thread.start()

print('생산자 데이터 추가')
my_queue.put(object())     # 앞에서 본 get()이 실행되기 전에 실행된다.
print('생산자 완료')
thread.join()


# 파이프라인 중간이 막히는 경우를 해결하기 위해 Queue 클래스에서는 두 단계 사이에 허용할 수 있는
# 미완성 작업의 최대 개수를 지정할 수 있다
from queue import Queue
from threading import Thread
import time

my_queue = Queue(1)  # 버퍼 크기 1

def consumer():
    time.sleep(0.1)  # 대기
    my_queue.get()  # 두 번째로 실행됨
    print('소비자 1')
    my_queue.get()  # 네 번째로 실행됨
    print('소비자 2')
    print('소비자 완료')

thread = Thread(target=consumer)
thread.start()

my_queue.put(object()) # 첫 번째로 실행됨
print('생산자 1')
my_queue.put(object()) # 세 번째로 실행됨
print('생산자 2')
print('생산자 완료')
thread.join()


# Queue 클래스의 task_done 메서드를 통해 작업의 진행을 추적할 수 있다
from queue import Queue
from threading import Thread
import time

in_queue = Queue()

def consumer():
    print('소비자 대기')
    work = in_queue.get()  # 두 번째로 실행됨
    print('소비자 작업중')
    # Doing work
    print('소비자 완료')
    in_queue.task_done()  # 세 번째로 실행됨

thread = Thread(target=consumer)
thread.start()

print('생산자 데이터 추가')
in_queue.put(object())    # 첫 번째로 실행됨
print('생산자 대기')
in_queue.join()           # 네 번째로 실행됨
print('생산자 완료')
thread.join()

# 이 모든 동작을 Queue 하위 클래스에 넣고, 처리가 끝났음을 작업자 스레드에게 알리는 기능을 추가할 수 있다
# 다음 코드는 큐에 더 이상 다른 입력이 없음을 표시하는 특별한 센티넬 원소를 추가하는 close 메서드를 정의한다
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


class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)

download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()
threads = [
    StoppableWorker(download, download_queue, resize_queue),
    StoppableWorker(resize, resize_queue, upload_queue),
    StoppableWorker(upload, upload_queue, done_queue),
]

for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())

download_queue.close()

download_queue.join()
resize_queue.close()
resize_queue.join()
upload_queue.close()
upload_queue.join()
print(done_queue.qsize(), '개의 원소가 처리됨')

for thread in threads:
    thread.join()

# 이 접근 방법을 확장해 단계마다 여러 작업자를 사용할 수 있다
# 그러면 I/O 병렬성을 높일 수 있으므로 속도를 상당히 증가시킬 수 있다
# 이를 위해 먼저 다중 스레드를 시작하고 끝내는 도우미 함수를 만든다

from queue import Queue
from threading import Thread
import time

def download(item):
    return item

def resize(item):
    return item

def upload(item):
    return item

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


class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)


def start_threads(count, *args):
    threads = [StoppableWorker(*args) for _ in range(count)]
    for thread in threads:
        thread.start()
    return threads


def stop_threads(closable_queue, threads):
    for _ in threads:
        closable_queue.close()

    closable_queue.join()

    for thread in threads:
        thread.join()

download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()
download_threads = start_threads(
    3, download, download_queue, resize_queue)
resize_threads = start_threads(
    4, resize, resize_queue, upload_queue)
upload_threads = start_threads(
    5, upload, upload_queue, done_queue)

for _ in range(1000):
    download_queue.put(object())

stop_threads(download_queue, download_threads)
stop_threads(resize_queue, resize_threads)
stop_threads(upload_queue, upload_threads)

print(done_queue.qsize(), '개의 원소가 처리됨')
