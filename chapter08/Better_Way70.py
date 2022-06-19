# 최적화하기 전에 프로파일링을 하라

# 파이썬의 동적인 특성으로 인해 실행 시간 성능이 예상과 달라 놀랄 때가 있다
# 느릴 것으로 예상한 연산이 실제로는 빠르거나
# 빠를 것으로 예상한 언어 기능이 실제로는 느린 경우

# 원인을 보는 가장 좋은 법근 방법은
# 프로그램을 최적화하기 전에 직관을 무시하고 직접 프로그램 성능을 측정하는 것
# 파이썬은 프로그램의 각 부분이 실행 시간을 얼마나 차지하는지 결저할 수 있게 해주는 프로파일러를 제공한다

def insertion_sort(data):
    result = []
    for value in data:
        insert_value(result, value)
    return result

def insert_value(array, value):
    for i, existing in enumerate(array):
        if existing > value:
            array.insert(i, value)
            return
    array.append(value)

from random import randint

max_size = 10**4
data = [randint(0, max_size) for _ in range(max_size)]
test = lambda: insertion_sort(data)

# 파이썬에는 두 가지 내장 프로파일러가 있다
# 하나는 순수하게 파이썬으로 작성(profile)
# 다른 하나는 C 확장 모듈(cProfile)
# cProfile이 더 낫다 -> 프로그램 성능에 최소로 영향을 미치기 때문

from cProfile import Profile

profiler = Profile()
profiler.runcall(test)

from pstats import Stats

stats = Stats(profiler)
stats.strip_dirs()
stats.sort_stats('cumulative')   # 누적 통계
stats.print_stats()

#
def insertion_sort(data):
    result = []
    for value in data:
        insert_value(result, value)
    return result

from bisect import bisect_left

def insert_value(array, value):
    i = bisect_left(array, value)
    array.insert(i, value)

from random import randint

max_size = 10**4
data = [randint(0, max_size) for _ in range(max_size)]
test = lambda: insertion_sort(data)

from cProfile import Profile

profiler = Profile()
profiler.runcall(test)

from pstats import Stats

stats = Stats(profiler)
stats.strip_dirs()
stats.sort_stats('cumulative')   # 누적 통계
stats.print_stats()

#
def my_utility(a, b):
    c = 1
    for i in range(100):
        c += a * b

def first_func():
    for _ in range(1000):
        my_utility(4, 5)

def second_func():
    for _ in range(10):
        my_utility(1, 3)

def my_program():
    for _ in range(20):
        first_func()
        second_func()

