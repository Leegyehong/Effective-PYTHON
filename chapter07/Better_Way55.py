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
