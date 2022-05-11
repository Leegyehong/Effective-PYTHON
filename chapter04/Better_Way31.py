# 인자에 대해 이터레이션할 때는 방어적이 돼라

# 객체가 원소로 들어있는 리스트를 함수가 파라미터로 받았을 때, 이 리스트를 여러 번 이터레이션하는 것이 중요할 때가 종종 있다

def normalize(numbers):
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

#
visits = [15, 35, 80]
percentages = normalize(visits)
print(percentages)

# 위 함수는 데이터가 들어있는 리스트가 입력으로 들어오면 잘 작동한다

# 규모 확장성을 높이려면 파일에서 데이터를 읽어야한다

def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)

# 놀랍게도 normalize함수에 read_visits가 반환한 값을 전달하면 아무 결과도 나오지 않는다
# 이유는 이터레이터가 결과를 단 한 번만 만들어내기 때문이다
it = read_visits('my_numbers.txt')
percentages = normalize(it)
print(percentages)

it = read_visits('my_numbers.txt')
print(list(it))
print(list(it)) # 이미 모든 원소를 다 소진했다

# 이 문제를 해결하기 위해 입력 이터레이터를 명시적으로 소진시키고 이터레이터의 전체 내용을 리스트에 넣을 수 있다

def normalize_copy(numbers):
    numbers_copy = list(numbers) # 이터레이터 복사
    total = sum(numbers_copy)
    result = []
    for value in numbers_copy:
        percent = 100 * value / total
        result.append(percent)
    return result

#
it = read_visits('my_numbers.txt')
percentages = normalize_copy(it)
print(percentages)

# 하지만 이 방식은 복사하는 과정에서 메모리 부족으로 인해 프로그램이 중단될 수도 있다
# 이 문제를 해결하는 다른 방법은 호출될 때마다 새로 이터레이터를 반환하는 함수를 받는 것이다
def normalize_func(get_iter):
    total = sum(get_iter())  # 새 이터레이터
    result = []
    for value in get_iter(): # 새 이터레이터
        percent = 100 * value / total
        result.append(percent)
    return result

#
path = 'my_numbers.txt'
percentages = normalize_func(lambda: read_visits(path))
print(percentages)
assert sum(percentages) == 100.0

# 작동하기는 하지만, 람다 함수를 넘기는 것은 보기 좋지 않다
# 더 나은 방법은 이터레이터 프로토콜을 구현한 새로운 컨테이너 클래스를 제공하는 것이다

class ReadVisits:
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)

#
visits = ReadVisits(path)
percentages = normalize(visits)
print(percentages)
assert sum(percentages) == 100.0