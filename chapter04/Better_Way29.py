# 대입식을 사용해 컴프리헨션 안에서 반복 작업을 피하라

# 컴프리헨션에서 같은 계산을 여러 위치에서 공유하는 경우가 흔하다

stock = {
    '못': 125,
    '나사못': 35,
    '나비너트': 8,
    '와셔': 24,
}

order = ['나사못', '나비너트', '클립']

def get_batches(count, size):
    return count // size

result = {}
for name in order:
    count = stock.get(name, 0)
    batches = get_batches(count, 8)
    if batches:
        result[name] = batches

print(result)

# 컴프리헨션을 사용하면 더 간결하게 표현할 수 있다
found = {name: get_batches(stock.get(name, 0), 8)
         for name in order
         if get_batches(stock.get(name, 0), 8)}
print(found)

# 앞의 코드보다는 짧지만 get_bathes가 반복된다는 단점이 있다
# 가독성도 나빠지고, 두 식을 항상 똑같이 변경해야하므로 실수할 가능성도 높아진다
# 예를들어 첫번째 get_batches 호출에서만 두 번째 인자를 4로 바꾸면 결과가 달라진다

has_bug = {name: get_batches(stock.get(name, 0), 4)
           for name in order
           if get_batches(stock.get(name, 0), 8)}

print('예상:', found)
print('실제: ', has_bug)

# 이러한 문제의 쉬운 해법은 왈러스 연산자를 사용하는 것이다
found = {name: batches for name in order
         if (batches := get_batches(stock.get(name, 0), 8))}



# 대입식을 컴프리헨션의 다른 부분에서 읽으려고 하면 오류가 발생한다
# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#result = {name: (tenth := count // 10)
#          for name, count in stock.items() if tenth > 0}

# 대입식을 조건 쪽으로 옮기고 대입식에서 만들어진 변수 이름을 참조하면 해결할 수 있다
result = {name: tenth for name, count in stock.items()
          if (tenth := count // 10) > 0}
print(result)