# 변수 위치 인자를 사용해 시각적인 잠음을 줄여라

# 위치 인자를 가변적으로 받을 수 있으면 함수 호출이 더 깔끔해지고 시각적 잡음도 줄어든다
# 이런 위치 인자를 가변 인자(varargs), 스타 인자(star args)라고 부르기도 한다

def log(message, values):
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{message}: {values_str}')

log('My numbers are', [1, 2])
log('Hi there', [])

# 로그에 남길 값이 없을 때도 빈 리스트를 넘겨야 한다면 귀찮을 뿐 아니라 코드 잡음도 많다
# 이럴 때 두 번째 인자를 완전히 생략하면 좋다
# 파이썬에서는 마지막 위치 인자 이름 앞에 *를 붙이면 된다

def log(message, *values):  # 유일하게 달라진 부분
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{message}: {values_str}')

log('My numbers are', 1, 2)
log('Hi there')  # 훨씬 좋다

# 가변적인 위치 인자를 받는데는 두 가지 문제점이 있다

# 첫 번째
# 선택적인 위치 인자가 함수에 전달되기 전에 항상 튜플로 변환된다
# 이렇게 만들어진 튜플은 제너레이터가 만들어낸 모든 값을 포함하며 이로 인해 메모리를 많이 소비하거나 프로그램이 중단될수도있다

def my_generator():
    for i in range(10):
        yield i

def my_func(*args):
    print(args)

it = my_generator()
my_func(*it)

# 두 번째
# 함수에 새로운 위치 인자를 추가하면 해당 함수를 호출하는 모든 코드를 변경해야만 한다

def log(sequence, message, *values):
    if not values:
        print(f'{sequence} - {message}')
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{sequence} - {message}: {values_str}')

log(1, 'Favorites', 7, 33)      # 새 코드에서 가변 인자 사용, 문제 없음
log(1, 'Hi there')              # 새 코드에서 가변 인자 없이 메시지만 사용, 문제 없음
log('Favorite numbers', 7, 33)  # 예전 방식 코드는 깨짐