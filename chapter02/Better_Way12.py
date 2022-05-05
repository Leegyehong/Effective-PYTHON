# 스트라이드와 슬라이스를 한 식에 함께 사용하지 말라

# 리스트[시작:끝:증가값]
x = [1, 2, 3, 4, 5, 6, 7, 8]
odds = x[::2]
evens = x[1::2]
print(odds)
print(evens)

# 스트라이드를 사용하는 구문은 종종 예기치 않은 동작이 일어나 버그를 야기할 수 있는 단점이 있다.
x = b'mongoose'
y = x[::-1]
print(y)
# 하지만 'utf-8' 인코딩한 문자열에서는 안됨

# -1 말고 다른 음수 증가값은?
x = [1, 2, 3, 4, 5, 6, 7, 8]
x[::2] # [1, 3, 5, 7]
x[::-2] # [8, 6, 4, 2]

# 슬라이싱 구문에 스트라이딩까지 들어가면 아주 혼란스럽다
# 이런 문제를 방지하기 위해 시작값이나 끝값을 증가값과 함께 사용하지 말 것을 권한다.