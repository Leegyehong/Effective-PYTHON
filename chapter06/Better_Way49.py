# __init_subclass__를 사용해 클래스 확장을 등록하라

# 메타클래스의 다른 용례로 프로그램이 자동으로 타입을 등록하는 것이 있다
# 간단한 식별자를 이용해 그에 해당하는 클래스를 찾는 역검색을 하고 싶을 때 이런 등록 기능이 유용

# 예를 들어 파이썬 object를 JSON으로 직렬화하는 직렬화 표현방식을 구현한다 치자
#  object를 JSON 문자열로 변환할 방법이 필요
import json

class Serializable:
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({'args': self.args})

# 불편 데이터 구조를 쉽게 직렬화 가능
class Point2D(Serializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point2D({self.x}, {self.y})'

point = Point2D(5, 3)
print('객체:', point)
print('직렬화한 값:', point.serialize())

# JSON 문자열을 역직렬화해서 문자열이 표현하는 객체를 구성
class Deserializable(Serializable):
    @classmethod
    def deserialize(cls, json_data):
        params = json.loads(json_data)
        return cls(*params['args'])

class BetterPoint2D(Deserializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return f'BetterPoint2D({self.x}, {self.y})'

before = BetterPoint2D(5, 3)
print('이전: ', before)
data = before.serialize()
print('직렬화한 값:', data)
after = BetterPoint2D.deserialize(data)
print('이후: ', after)

# 위 접근 방식은 데이터의 타입을 미리 알고 있는 경우에만 사용할 수 있다는 문제가 있다
# JSON으로 직렬화할 클래스가 아주 많더라도 JSON 문자열을 적당한 object로 역직렬화하는 함수는 공통으로 하나만 있는것이 이상적
# 공통함수를 만들고자 객체의 클래스 이름을 직렬화 함
# 클래스 이름을 다시 객체 생성자로 연결해주는 매핑을 유지할 수 있다
class BetterSerializable:
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args,
        })

    def __repr__(self):
        name = self.__class__.__name__
        args_str = ', '.join(str(x) for x in self.args)
        return f'{name}({args_str})'

registry = {}

def register_class(target_class):
    registry[target_class.__name__] = target_class

def deserialize(data):
    params = json.loads(data)
    name = params['class']
    target_class = registry[name]
    return target_class(*params['args'])

class EvenBetterPoint2D(BetterSerializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

register_class(EvenBetterPoint2D)

before = EvenBetterPoint2D(5, 3)
print('이전: ', before)
data = before.serialize()
print('직렬화한 값:', data)
after = deserialize(data)
print('이후: ', after)

# 이 방식의 문제점은 register_class의 호출을 잊어버릴 수 있다는 것
class Point3D(BetterSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x = x
        self.y = y
        self.z = z

point = Point3D(5, 9, -4)
data = point.serialize()
# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#deserialize(data)

# 이런 실수를 하기 쉽다
# 클래스 데코레이터도 마찬가지

# 프로그래머가 BetterSerializable을 사용한다는 의도를 감지하고 적절한 동작을 수행해
# 항상 제대로 register_class를 호출해주면 어떨까?
# 메타클래스는 하위 클래스가 정의될 때 class문을 가로채서 이런 동작을 수행할 수 있다

class Meta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        register_class(cls)
        return cls

class RegisteredSerializable(BetterSerializable,
                            metaclass=Meta):
    pass

class Vector3D(RegisteredSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x, self.y, self.z = x, y, z

before = Vector3D(10, -7, 3)
print('이전: ', before)
data = before.serialize()
print('직렬화한 값:', data)
print('이후: ', deserialize(data))

# 더 좋은 접근 방법은 __init_subclass__ 특별 클래스 메서드를 사용하는 것
class BetterRegisteredSerializable(BetterSerializable):
    def __init_subclass__(cls):
        super().__init_subclass__()
        register_class(cls)


class Vector1D(BetterRegisteredSerializable):
    def __init__(self, magnitude):
        super().__init__(magnitude)
        self.magnitude = magnitude

before = Vector1D(6)
print('이전: ', before)
data = before.serialize()
print('직렬화한 값:', data)
print('이후: ', deserialize(data))