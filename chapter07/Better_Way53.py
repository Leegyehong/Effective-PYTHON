# 블록킹 I/O의 경우 스레드를 사용하고 병렬성을 피하라

# 파이썬 프로그램의 속도를 높이고 병렬 처리를 수행하고자 스레드를 사용한다면 크게 실망할 것이다

# 계산량이 많은 작업( 인수 찾기 알고리즘 )
def factorize(number):
    for i in range(1, number + 1):
        if number % i == 0:
            yield i

import time

numbers = [2139079, 1214759, 1516637, 1852285]
start = time.time()

for number in numbers:
    list(factorize(number))

end = time.time()
delta = end - start
print(f'총 {delta:.3f} 초 걸림')

# 다른 언어는 컴퓨터에 있는 모든 CPU코어를 활용할 수 있으므로 다중 스레드를 사용해 계산을 수행하는 것이 타당하다
# 이것을 파이썬으로 시도해보자 
def factorize(number):
    for i in range(1, number + 1):
        if number % i == 0:
            yield i

from threading import Thread

class FactorizeThread(Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))

import time

numbers = [2139079, 1214759, 1516637, 1852285]
start = time.time()

threads = []
for number in numbers:
    thread = FactorizeThread(number)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

end = time.time()
delta = end - start
print(f'총 {delta:.3f} 초 걸림')
# 놀랍게도 스레드를 하나만 써서 실행할 때보다 시간이 더 오래걸린다
# CPython 인터프리터에서 프로그램을 사용할 때 GIL 이 미치는 영향이다

# 그럼에도 불구하고 파이썬이 스레드를 지원하는 이유
# 첫째, 다중 스레드를 사용하면 프로그램이 동시에 여러 일을 하는것처럼 보이게 만듬
# 둘째, 블로킹 I/O를 다루기 위해서

# 예를 들어 직렬 포트를 통해 원격 제어 헬리콥터에 신호를 보낸다고 했을 때
# 이 동작을 대신해 느린 시스템 콜을 사용할 것이다
# 이 함수는 운영체제에게 0.1초동안 블록한 다음에 제어를 돌려달라고 요청하는데, 동기적으로 직렬포트를 사용할 때 벌어지는 상황
import select
import socket
import time

def slow_systemcall():
    select.select([socket.socket()], [], [], 0.1)

start = time.time()

for _ in range(5):
    slow_systemcall()

end = time.time()
delta = end - start
print(f'총 {delta:.3f} 초 걸림')

# 문제는 slow_systemcall() 을 실행하는 동안 프로그램이 아무런 진전을 이룰 수 없다는 것
# 이 프로그램의 주 실행 스레드는 select 시스템 콜에 의해 블록된다
# 신호를 보내는동안 헬리콥터가 다음에 어디로 이동할지 계산할 수 있어야한다

# 다음 코드에서는 slow_systemcall()을 여러 스레드에서 따로따로 호출한다
import select
import socket
import time
from threading import Thread

def slow_systemcall():
    select.select([socket.socket()], [], [], 0.1)

start = time.time()

threads = []
for _ in range(5):
    thread = Thread(target=slow_systemcall)
    thread.start()
    threads.append(thread)

def compute_helicopter_location(index):
    pass

for i in range(5):
    compute_helicopter_location(i)

for thread in threads:
    thread.join()

end = time.time()
delta = end - start
print(f'총 {delta:.3f} 초 걸림')
