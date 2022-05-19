# 비공개 애트리뷰트보다는 공개 애트리뷰트를 사용하라

# 파이썬에서 클래스의 애트리뷰트에 대한 가시성은 공개(public)와 비공개(private), 두 가지밖에 없다
class MyObject:
    def __init__(self):
        self.public_field = 5
        self.__private_field = 10

    def get_private_field(self):
        return self.__private_field

foo = MyObject()
# 객체 뒤에 점 연산자(.)를 붙이면 공개 애트리 뷰트에 접근 가능
assert foo.public_field == 5
# 애트리뷰트 이름 앞에 밑줄 두 개(__) 붙이면 비공개 필드가 된다
# 비공개 필드를 포함하는 클래스 안에 있는 메서드에서는 해당 필드에 직접 접근 가능
assert foo.get_private_field() == 10

# 하지만 클래스 외부에서 비공개 필드에 접근하면 예외 발생
# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#foo.__private_field

# 클래스 메서드는 자신을 둘러싸고 있는 class 블록 내부에 들어 있기 때문에 비공개 필드에 접근 가능하다
class MyOtherObject:
    def __init__(self):
        self.__private_field = 71

    @classmethod
    def get_private_field_of_instance(cls, instance):
        return instance.__private_field

bar = MyOtherObject()
assert MyOtherObject.get_private_field_of_instance(bar) == 71

# 하위 클래스는 부모 클래스의 비공개 필드에 접글할 수 없다
class MyParentObject:
    def __init__(self):
        self.__private_field = 71

class MyChildObject(MyParentObject):
    def get_private_field(self):
        return self.__private_field

baz = MyChildObject()
# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#baz.get_private_field()

# _MyParentObject__private_field 라는 이름으로 바꾼다면 오류가 나지 않는다
# 문제없음
assert baz._MyParentObject__private_field == 71

print(baz.__dict__)

# 비공개 애트리뷰트에 대한 접근 구문이 실제로 가시성을 엄격하게 제한하지 않는 이유는 무엇일까
# 파이썬의 모토 => '우리는 모두 책임질줄 아는 성인이다' 
# 우리가 하고 싶은 일을 언어가 제한하면 안된다

# 이런 접근 방법은 잘못된 것
# 누군가는 이 클래스를 상속하면서 새로운 기능을 추가하거나
# 기존 메서드의 단점을 해결하기 위해 새로운 동작을 추가하기를 원한다
class MyStringClass:
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return str(self.__value)

foo = MyStringClass(5)
assert foo.get_value() == '5'
# 물론 여전히 비공개 필드에 접근할 수 있다
class MyIntegerSubclass(MyStringClass):
    def get_value(self):
        return int(self._MyStringClass__value)

foo = MyIntegerSubclass('5')
assert foo.get_value() == 5

# 하지만 자신의 클래스 정의를 변경하면 더 이상 비공개 애트리뷰트에 대한 참조가 바르지 않으므로 
# 하위 클래스가 깨질 것이다

class MyBaseClass:
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

class MyStringClass(MyBaseClass):
    def get_value(self):
        return str(super().get_value())  # 변경됨

class MyIntegerSubclass(MyStringClass):
    def get_value(self):
        return int(self._MyStringClass__value)  # 변경되지 않음

foo = MyIntegerSubclass(5)
# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#foo.get_value()


# 비공개 애트리뷰트를 사용할 지 진지하게 고민해야 하는 유일한 경우는
# 하위 클래스의 필드와 이름이 충돌할 수 있는 경우뿐
# 자식 클래스가 실수로 부모 클래스가 이미 정의한 애트리뷰트를 정의하면 충돌이 발생한다

class ApiClass:
    def __init__(self):
        self._value = 5

    def get(self):
        return self._value

class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello'  # 충돌

a = Child()
print(f'{a.get()} 와 {a._value} 는 달라야 합니다.')

# 주로 공개 API에 속한 클래스의 경우 신경 써야 하는 부분
# 이런 위험성을 줄이려면, 부모 클래스 쪽에서 자식 클래스의 애트리뷰트 이름이
# 자신의 애트리뷰트 이름과 겹치는 일을 방지하기 위해 비공개 애트리뷰트를 사용할 수 있다

class ApiClass:
    def __init__(self):
        self.__value = 5    # 밑줄 2개!

    def get(self):
        return self.__value # 밑줄 2개!

class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello' # OK!

a = Child()
print(f'{a.get()} 와 {a._value} 는 다릅니다.')