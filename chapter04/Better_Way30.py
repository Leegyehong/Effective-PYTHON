# 리스트를 반환하기보다는 제너레이터를 사용하라


# 시퀀스를 결과로 만들어내는 함수를 만들 때 가장 간단한 선택은 리스트를 반환하는 것이다
def index_words(text):
    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == ' ':
            result.append(index + 1)
    return result

address = '컴퓨터(영어: Computer, 문화어: 콤퓨터, 순화어:전산기)는 진공관'
result = index_words(address)
print(result[:10])

# 위 함수는 두 가지 문제가 있다

# 첫 번째 
# 코드에 노이즈가 많고 핵심을 알아보기 어렵다
# 새로운 결과를 찾을 때마다 append 메서드를 호출한다 -> 메서드 호출의 덩어리가 커서 추가될 값(index + 1)의 중요성을 희석함 

# 개선하는 방법은 '제너레이터'를 사용하는 것이다 
# 제너레이터는 yield 식을 사용하는 함수에 의해 만들어진다

def index_words_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1

# 이 함수가 호출되면 실제로 실행되지않고 즉시 이터레이터를 반환한다
it = index_words_iter(address)
print(next(it))
print(next(it))

# 제너레이터가 반환하는 이터레이터를 리스트 내장함수에 넘기면 필요할 때 제너레이터를 쉽게 리스트로 변환할 수 있다
result = list(index_words_iter(address))
print(result[:10])

# 두 번째
# 반환하기 전에 리스트에 모든 결과를 다 저장해야 한다는 것이다
# 입력이 매우 크면 프로그램이 메모리를 소진해서 중단될 수 있다


# 이 함수의 작업 메모리는 입력 중 가장 긴 줄의 길이로 제한된다
def index_file(handle):
    offset = 0
    for line in handle:
        if line:
            yield offset
        for letter in line:
            offset += 1
            if letter == ' ':
                yield offset
     
     
import itertools
with open('address.txt', 'r', encoding='utf-8') as f:
    it = index_file(f)
    results = itertools.islice(it, 0, 10)
    print(list(results))