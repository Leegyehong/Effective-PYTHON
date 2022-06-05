# 스레드에서 데이터 경합을 피하기 위해 Lock을 사용하라


# GIL을 배운 뒤 코드에서 더이상 뮤텍스를 사용하지 않아도 되는 것으로 생각한다
# GIL이 다중 CPU에서 파이썬 스레드들이 병렬적으로 실행될수 없게 막는다면,
# 파이썬 스레드들이 프로그램의 데이터 구조에 동시에 접글할 수 없게 막는 락 역할도 해줘야 하지 않을까?

# 리스트나 딕셔너리 같은 몇가지 타입에 대해 테스트해보면 이런 가정이 성립되는 것 처럼 보인다
# 하지만 실제로는 전혀 그렇지 않다

# 병렬적으로 여러 가지 개수를 세는 프로그램
from threading import Thread
import select
import socket

class Counter:
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset

def worker(sensor_index, how_many, counter):
    for _ in range(how_many):
        # 센서를 읽는다
        counter.increment(1)

from threading import Thread

how_many = 10**5
counter = Counter()

threads = []
for i in range(5):
    thread = Thread(target=worker,
                    args=(i, how_many, counter))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

expected = how_many * 5
found = counter.count
print(f'카운터 값은 {expected}여야 하는데, 실제로는 {found} 입니다')
# 이 코드는 단순해보이고, 결과도 뻔할 것 같다
# 하지만 실제 실행한 결과는 예상과 전혀 다르다
# 파이썬 인터프리터 스레드는 어느 한 순간에 단 하나씩만 실행되는데, 어떻게 이와 같이 단순한 코드가 잘못될 수 있을까?

# 파이썬 인터프리터는 실행되는 모든 스레드를 강제로 공평하게 취급해서 각 스레드의 실행 시간을 거의 비슷하게 만든다
# 이를 위해 실행중인 스레드를 일시 중단 시키고 다른 스레드를 실행시키는 일을 반복한다
# 문제는 스레드를 언제 일시 중단 시킬지 알 수 없다는 점

