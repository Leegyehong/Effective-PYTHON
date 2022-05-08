# 위치로만 인자를 지정하게 하거나 키워드로만 인자를 지정하게 해서 함수 호출을 명확하게 만들라

# 키워드를 사용해 인자를 넘기는 기능은 파이썬 함수의 강력한 기능이다
# 키워드 인자의 유연성을 활용하면 코드를 처음 읽는 사람도 더 명확하게 용례를 이해할 수 있다

def safe_division(number, divisor,
                  ignore_overflow,
                  ignore_zero_division):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

# float 나눗셈의 오버플로우를 무시하고 대신 0 을 반환함
result = safe_division(1.0, 10**500, True, False)
print(result)

# 0으로 나눈 경우 발생하는 오류를 무시하고 무한대를 반환
result = safe_division(1.0, 0, False, True)
print(result)

# 위 함수의 문제는 어떤 예외를 무시할지 결정하는 두 불 변수의 위치를 혼동하기 쉽다
# 이로 인해 추적하기 힘든 버그가 생길 수 있다
# 이 코드의 가독성을 향상 시키는 방법은 키워드 인자를 사용하는 것

def safe_division_b(number, divisor,
                    ignore_overflow=False,        # Changed
                    ignore_zero_division=False):  # Changed
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise
        
result = safe_division_b(1.0, 10**500, ignore_overflow=True)
print(result)

result = safe_division_b(1.0, 0, ignore_zero_division=True)
print(result)

# 문제는 이런 식으로 키워드 인자를 사용하는 것이 선택적인 사항이라 호출하는 쪽에서 명확성을 위해 키워드 인자를 꼭 쓰도록 강요할 수 없다
# save_division_b 에서도 위치 인자를 통해 예전 방식으로 호출 할 수 있다

# 복잡한 함수의 경우 호출자가 키워드만 사용하는 인자를 통해 의도를 명확히 밝히도록 요구하는 편이 좋다   
def safe_division_c(number, divisor, *,  # Changed
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

# 위치인자를 사용하면 오류가 발생한다

try:
    safe_division_c(1.0, 10**500, True, False)
except:
    logging.exception('Expected')
else:
    assert False
    

result = safe_division_c(1.0, 0, ignore_zero_division=True)
assert result == float('inf')

try:
    result = safe_division_c(1.0, 0)
except ZeroDivisionError:
    pass  # Expected
else:
    assert False
    
    
# 위 함수의 문제점은 호출하는 쪽에서 필수 인자(number, divisor)를 호출하면서 위치와 키워드를 혼용할 수 있다
assert safe_division_c(number=2, divisor=5) == 0.4
assert safe_division_c(divisor=5, number=2) == 0.4
assert safe_division_c(2, divisor=5) == 0.4

# / 기호는 위치로만 지정하는 인자의 끝을 표시한다
def safe_division_d(numerator, denominator, /, *,  # Changed
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        return numerator / denominator
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise
        
assert safe_division_d(2, 5) == 0.4

safe_division_d(numerator=2, denominator=5)


# /와 * 기호 사이에 있는 모든 파라미터는 위치를 사용해 전달할 수도 있고 키워드로 사용해 전달할 수도 있다

def safe_division_e(numerator, denominator, /,
                    ndigits=10, *,                # Changed
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        fraction = numerator / denominator        # Changed
        return round(fraction, ndigits)           # Changed
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise
        
result = safe_division_e(22, 7)
print(result)

result = safe_division_e(22, 7, 5)
print(result)

result = safe_division_e(22, 7, ndigits=2)
print(result)