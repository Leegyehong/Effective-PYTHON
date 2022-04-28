# bytes와 str의 차이를 알아두라
# 문자열 데이터의 시퀀스를 표현하는 두 가지 타입이 있다. (bytes와 str)


# bytes 타입의 인스턴스에는 부호가 없는 8바이트 데이터가 그대로 들어간다. (종종 아스키 인코딩을 사용해 내부 문자를 표시)
a = b'h\x65llo'
print(list(a)) # [104, 101, 108, 108, 111]
print(a)  # b'hello'

# str 인스턴스에는 사람이 사용하는 언어의 문자를 표현하는 유니코드 코드 포인트가 들어 있다.
b = 'a\u0300 propos'
print(list(b)) # ['a', '̀', ' ', 'p', 'r', 'o', 'p', 'o', 's']
print(b) # à propos


# str의 encode메서드, bytes의 decode메서드를 호출할 때 여러분이 원하는 인코딩 방식을 지정할 수도 있고, 시스템 디폴트 인코딩을 받아들일 수도 있다.

# 프로그램을 작성할 때 유니코드 데이터를 인코딩하거나 디코딩하는 부분을 인터페이스의 가장 먼 경계 지점에 위치시켜라 => 유니코드 샌드위치
# 프로그램 핵심 부분은 유니코드 데이터가 들어 있는 str을 사용해야하고 문자 인코딩에 대해서 어떠한 가정도 해서는 안된다.
# => 이런 방식을 사용하면 다양한 텍스트 인코딩을 입력 데이터로 받아들일 수 있고, 출력 텍스트 인코딩은 한가지로만 엄격히 제한한다.


# bytes나 str 인스턴스를 받아서 항상 str로 반환하는 함수

def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value # str 인스턴스

print(repr(to_str(b'foo'))) #foo
print(repr(to_str(b'bar'))) #bar
print(repr(to_str(b'\xed\x95\x9c'))) #한


# bytes나 str 인스턴스를 받아서 항상 bytes를 반환
def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value # bytes 인스턴스

print(repr(to_bytes(b'foo'))) # b'foo'
print(repr(to_bytes('bar'))) # b'bar'
print(repr(to_bytes('한글'))) # b'\xed\x95\x9c\xea\xb8\x80'

# 이진 8비트 값과 유니코드 문자열을 다룰 때 기억해야 할 2가지의 문제점
# 1) bytes나 str이 똑같이 작동하는 것처럼 보이지만 서로 호환되지 않기 때문에 전달 중인 문자 시퀀스가 어떤 타입인지 알아야한다.
#   + 연산자를 사용하여 bytes를 bytes에 더하거나 str을 str에 더하기 가능
print(b'one' + b'two') # b'onetwo'
print('one' + 'two') # onetwo

#   하지만 str인스턴스를 bytes 인스턴스에 더할 수는 없다.
#   이항 연산자 또한 마찬가지이다.

# 2) 파일 핸들과 관련한 연산들이 디폴트로 유니코드 문자열을 요구하고 이진 바이트 문자열을 요구하지 않는다.

#   이진 데이터를 파일에 기록하고 싶다고 할 때 다음은 오류가 발생한다.
with open('data.bin', 'w') as f:
    f.write(b'\xf1\xf2\xf3\xf4\xf5')
    
#   이유는 'wb'가 아닌 'w'로 열었기 때문
#   읽을 때 또한 마찬가지이다.

# 다른 방법으로는 open 함수의 encoding 파라미터를 명시한다.
with open('data.bin', 'r', encoding='cp1512') as f:
    data = f.read()

# 하지만 예외는 없지만 결과는 이진 데이터를 읽었을 때와는 다를 것이다.
# 따라서 시스템의 디폴트 인코딩이 어떻게 다른지 항상 검사하자.
# python -c 'import locale; print( locale.getpreferredencoding() ) 

import locale
locale.getpreferredencoding()