# None을 반환하기보다는 예외를 발생시켜라

# 프로그래머들은 유틸리티 함수를 작성할 때 반환 값을 None으로 하면서 이 값에 특별한 의미를 부여하려는 경향을 나타낸다


def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
    
# 위 경우에서 0 으로 나누는 경우 결과가 정해져 있지 않으므로 None을 반환하는 것이 자연스러워 보인다
# 이 함수를 사용하는 코드는 반환 값을 적절히 해석하면 된다

x, y = 1, 0
result = careful_divide(x, y)
if result is None:
    print('Invalid inputs')
else:
    print('Result is %.1f' % result)
    
# 그런데 함수가 반환한 결과를 if문 등의 조건에서 평가할 때 0 값이 문제가 될 수 있다
# None 인지 검사하는 대신, 실수로 빈 값을 False로 취급하는 검사를 실행할 수 있다

x, y = 0, 5
result = careful_divide(x, y)
if not result:
    print('Invalid inputs')  # 이 코드가 실행되는데 사실 실행되면 안된다
else:
    assert False
    

# False와 동등한 반환 값을 잘못 해석하는 경우는 None이 특별한 의미를 가지는 파이썬 코드에서 흔히 있는 실수이다
# 그래서 careful_divide 같은 함수에서 실수할 가능성을 줄이는 방법은 두가지이다

# 첫번째
# 반환 값을 2-튜플 로 분리한다
# 튜플의 첫 번째 부분은 연산이 성공인지 실패인지를 표시하고, 두 번째 부분은 성공한 경우 실제 결괏값을 저장한다

def careful_divide(a, b):
    try:
        return True, a / b
    except ZeroDivisionError:
        return False, None
    
    
x, y = 5, 0
success, result = careful_divide(x, y)
if not success:
    print('Invalid inputs')
    
# 하지만 이 방법의 문제점은 호출하는 쪽에서 첫 번째 부분을 쉽게 무시할 수 있다는 것이다

x, y = 5, 0
_, result = careful_divide(x, y)
if not result:
    print('Invalid inputs')
    
# 이런 실수를 줄일 수 있는 두번째 방법

# 두번째
# 특별한 경우에 결코 None을 반환하지 않는다
# 대신 Exception을 호출한 쪽으로 발생시켜서 호출자가 이를 처리하게 한다

def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs')

x, y = 5, 2
try:
    result = careful_divide(x, y)
except ValueError:
    print('Invalid inputs')
else:
    print('Result is %.1f' % result)
    

# 이 접근 방법을 확장해서 타입 애너테이션을 사용하는 코드에도 적용할 수 있다
# 함수의 반환 값이 항상 float라고 지정할 수 있고, 그에 따라 None이 결코 반환되지 않음을 알릴 수 있다

def careful_divide(a: float, b: float) -> float:
    """Divides a by b.
    Raises:
        ValueError: When the inputs cannot be divided.
    """
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs')

try:
    result = careful_divide(1, 0)
    assert False
except ValueError:
    pass  # Expected
