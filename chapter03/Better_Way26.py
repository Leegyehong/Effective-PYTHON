# functools.wrap을 사용해 함수 데코레이터를 정의하라

# 데코레이터는 자신이 감싸고 있는 함수가 호출되기 전과 후에 코드를 추가로 실행해준다
# 이는 데코레이터가 자신이 감싸고 있는 함수의 입력 인자, 반환 값, 함수에서 발생한 오류에 접근할 수 있다는 뜻이다

# 함수의 의미를  강화하거나 디버깅을 하거나 함수를 등록하는 등의 일에 유용하게 쓴다

def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__}({args!r}, {kwargs!r}) '
              f'-> {result!r}')
        return result
    return wrapper

# 이 에코레이터 함수를 적용할 때는 @ 기호를 사용한다

@trace
def fibonacci(n):
    """Return the n-th Fibonacci number"""
    if n in (0, 1):
        return n
    return (fibonacci(n - 2) + fibonacci(n - 1))

fibonacci = trace(fibonacci)
fibonacci(4)

# 이 함수에는 부작용이 있는데
# 데코레이터가 반환하는 함수의 이름이 fibonacci가 아니게 된다

import pickle
pickle.dumps(fibonacci)

from functools import wraps

def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__}({args!r}, {kwargs!r}) '
              f'-> {result!r}')
        return result
    return wrapper

@trace
def fibonacci(n):
    """Return the n-th Fibonacci number"""
    if n in (0, 1):
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)

help(fibonacci)
print(pickle.dumps(fibonacci))