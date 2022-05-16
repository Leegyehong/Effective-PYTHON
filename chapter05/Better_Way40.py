# super로 부모 클래스를 초기화하라

# 자식 클래스에서 부모 클래스를 초기화 하는 오래된 방법은
# 자식 인스턴스에서 부모 클래스의 __init__ 메서드를 직접 호출하는 것

class MyBaseClass:
    def __init__(self, value):
        self.value = value

class MyChildClass(MyBaseClass):
    def __init__(self):
        MyBaseClass.__init__(self, 5)
        
# 이 접근 방법은 기본적인 클래스 계층의 경우에는 잘 작동하지만, 다른 경우에는 잘못될 수도 있다

# 어떤 클래스가 다중 상속에 의해 영향을 받은경우, 상위 클래스의 __init__메서드를 직접 호출하면
# 프로그램이 에측할 수 없는 방식으로 작동할 수 있다


class TimesTwo:
    def __init__(self):
        self.value *= 2

class PlusFive:
    def __init__(self):
        self.value += 5

#
class OneWay(MyBaseClass, TimesTwo, PlusFive):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)

foo = OneWay(5)
print('첫 번째 부모 클래스 순서에 따른 값은 (5 * 2) + 5 =', foo.value)


class AnotherWay(MyBaseClass, PlusFive, TimesTwo):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)

bar = AnotherWay(5)
print('두 번째 부모 클래스 순서에 따른 값은', bar.value)
# 부모 클래스를 나열하는 순서가 다르지만 호출 순서를 그대로 뒀기 때문에 결과가 똑같다
# 이런식으로 클래스 정의에 나열한 부모 클래스와 부모 생성자를 호출한 순서가 달라서 생기는 문제는
# 발견하기가 쉽지 않고, 처음 보고 이해하기 어려울 수 있다

# 다이아몬드 상속으로 인해 다른 문제가 생길 수도 있다
# 다이아몬드 상속이 이뤄지면 공통 조상클래스의 __init__메서드가 여러번 호출될 수 있기때문에
# 코드가 예기치 않은 방식으로 작동할 수 있다

class TimesSeven(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value *= 7

class PlusNine(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value += 9

class ThisWay(TimesSeven, PlusNine):
    def __init__(self, value):
        TimesSeven.__init__(self, value)
        PlusNine.__init__(self, value)

foo = ThisWay(5)
print('(5 * 7) + 9 = 44가 나와야 하지만 실제로는', foo.value)  # 14

# 이러한 문제를 해결하기 위해 파이썬에는 super라는 내장 함수와 표준 메서드 결정 순서가 있다

class TimesSevenCorrect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value *= 7

class PlusNineCorrect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value += 9

class GoodWay(TimesSevenCorrect, PlusNineCorrect):
    def __init__(self, value):
        super().__init__(value)

foo = GoodWay(5)
print('7 * (5 + 9) = 98이 나와야 하고 실제로도', foo.value)

# 순서가 거꾸로 된 것처럼 보일 것이다
# TimesSevenCorrect.__init__이 먼저 호출돼서 결과가 (5*7)+9=44 여야 하지 않을까 싶다
# 정답은 '아니오' 이다
# 이 클래스에 대한 MRO 정의를 따른다

mro_str = '\n'.join(repr(cls) for cls in GoodWay.mro())
print(mro_str)
# <class '__main__.GoodWay'>
# <class '__main__.TimesSevenCorrect'>
# <class '__main__.PlusNineCorrect'>
# <class '__main__.MyBaseClass'>
# <class 'object'>

# 또한 super함수에 두 가지 파라미터를 넘길 수 있다
# 첫 번째 파라미터는 접근하고 싶은 MRO 뷰를 제공할 부모 타입이고
# 두 번째 파라미터는 첫 번째 파라미터로 지정한 타입의 MRO 뷰에 접글할 때 사용할 인스턴스이다

class ExplicitTrisect(MyBaseClass):
    def __init__(self, value):
        super(ExplicitTrisect, self).__init__(value)
        self.value /= 3

class AutomaticTrisect(MyBaseClass):
    def __init__(self, value):
        super(__class__, self).__init__(value)
        self.value /= 3

class ImplicitTrisect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value /= 3

assert ExplicitTrisect(9).value == 3
assert AutomaticTrisect(9).value == 3
assert ImplicitTrisect(9).value == 3