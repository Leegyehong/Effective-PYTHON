# 간단한 인터페이스의 경우 클래스 대신 함수를 받아라

# 파이썬 내장 API 중 상당수는 함수를 전달해서 동작을 원하는 대로 바꿀 수 있게 해준다
# API가 실행되는 과정에서 전달한 함수를 실행하는 경우를 '훅' 이라고 한다

# 예) 리스트 타입의 sort 메서드는 정렬 시 각 인덱스에 대응하는 비교 값을 결정하는 선택적인 key 인자를 받는다
# 다음 코드가 key 훅으로 len 내장함수를 전달해서 이름이 들어있는 리스트를 길이에 따라 정렬한다
names = ['소크라테스', '아르키메데스', '플라톤', '아리스토텔레스']
names.sort(key=len)
print(names)

# 파이썬은 함수를 '일급 시민 객체'로 취급하기 때문에 함수를 훅으로 사용할 수 있다
def log_missing():
    print('키 추가됨')
    return 0

from collections import defaultdict
current = {'초록': 12, '파랑': 3}
increments = [
    ('빨강', 5),
    ('파랑', 17),
    ('주황', 9),
]
result = defaultdict(log_missing, current)
print('이전:', dict(result))
for key, amount in increments:
    result[key] += amount
print('이후:', dict(result))

# log_missing과 같은 함수를 사용할 수 있으면 정해진 동작과 side effect를 분리할 수 있기 때문에 API를 더 쉽게 만들 수 있다
# 예를 들어 defaultdict에 전달하는 디폴트 값 훅이 존재하지 않는 키에 접근한 총횟수를 세고 싶다면
# 방법 중 하나는 클로저를 사용하는 것

def increment_with_report(current, increments):
    added_count = 0

    def missing():
        nonlocal added_count  # 상태가 있는 클로저
        added_count += 1
        return 0

    result = defaultdict(missing, current)
    for key, amount in increments:
        result[key] += amount

    return result, added_count

result, count = increment_with_report(current, increments)
assert count == 2

# 상태를 다루기 위한 훅으로 클로저를 사용하면 상태가 없는 함수에 비해 읽고 이해하기 어렵다
# 다른 접근 방법은 추적하고 싶은 상태를 저장하는 작은 클래스를 정의하는 것이다
class CountMissing:
    def __init__(self):
        self.added = 0

    def missing(self):
        self.added += 1
        return 0

counter = CountMissing()
result = defaultdict(counter.missing, current) # 메서드 참조
for key, amount in increments:
    result[key] += amount
assert counter.added == 2


# 클래스로 상태가 있는 클러저와 같은 동작을 제공하는 것이 더 깔끔하다
# 하지만 클래스 자체만 놓고 보면 목적이 무엇인지 분명히 알기는 어렵다
# 이런 경우를 더 명확히 표현하기 위해 파이썬에서는 클래스에 __call__ 특별 메서드를 정의할 수 있다

class BetterCountMissing:
    def __init__(self):
        self.added = 0

    def __call__(self):
        self.added += 1
        return 0


counter = BetterCountMissing()
assert counter() == 0
assert callable(counter)

counter = BetterCountMissing()
result = defaultdict(counter, current) # __call__에 의존함
for key, amount in increments:
    result[key] += amount
assert counter.added == 2