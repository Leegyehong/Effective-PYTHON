# __init_subclass__ 를 사용해 하위 클래스를 검증하라

# 메타클래스의 가장 간단한 활용법 중 하나는 어떤 클래스가 제대로 구현됐는지 검증하는 것
# 새로운 하위클래스가 정의될 때마다 검증 코드를 수행하는 신뢰성 있는 방법을 제공

# 클래스 검증 코드를 __init__ 메서드 안에서 실행하는 경우가 종종 있다
# 프로그램 시작 시 클래스가 정의된 모듈을 처음 임포트할 때와 같은 시점에 검증이 이뤄지기 때문에 예외가 훨씬 더 빨리 발생할 수 있다
# 일반적인 객체의 메타클래스는 type을 상속해 졍의된다
# __new__ 메서드를 통해 자신과 연관된 클래스의 내용을 받는다
class Meta(type):
    def __new__(meta, name, bases, class_dict):
        print(f'* 실행: {name}의 메타 {meta}.__new__')
        print('기반클래스들:', bases)
        print(class_dict)
        return type.__new__(meta, name, bases, class_dict)

class MyClass(metaclass=Meta):
    stuff = 123

    def foo(self):
        pass

class MySubclass(MyClass):
    other = 567

    def bar(self):
        pass


# 연관된 클래스가 정의되기 전에 이 클래스의 모든 파라미터를 검증하려면
# Meta.__new__에 기능을 추가해야한다
class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        # Polygon 클래스의 하위 클래스만 검증한다
        if bases:
            if class_dict['sides'] < 3:
                raise ValueError('다각형 변은 3개 이상이어야 함')
        return type.__new__(meta, name, bases, class_dict)

class Polygon(metaclass=ValidatePolygon):
    sides = None # 하위 클래스는 이 애트리뷰트에 값을 지정해야 한다
    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180

class Triangle(Polygon):
    sides = 3

class Rectangle(Polygon):
    sides = 4

class Nonagon(Polygon):
    sides = 9

assert Triangle.interior_angles() == 180
assert Rectangle.interior_angles() == 360
assert Nonagon.interior_angles() == 1260

# 이 검증은 class문에서 3보다 작은 경우 class 정의문의 본문이 실행된 직후 예외를 발생시킨다
# 이는 2 이하인 경우인 클래스를 정의하면 프로그램이 아예 시작되지도 않는다는 뜻
print('class 이전')

# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#class Line(Polygon):
#    print('sides 이전')
#    sides = 2
#    print('sides 이후')

print('class 이후')


# 다행히 파이썬 3.6에는 메타클래스를 정의하지 않고 같은 동작을 구현할 수 있는 더 단순한 구문
# __init_subclass__ 이 추가됐다 
class BetterPolygon:
    sides = None  # 하위클래스에서 이 애트리뷰트의 값을 지정해야 함

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls.sides < 3:
            raise ValueError('다각형 변은 3개 이상이어야 함')

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180

class Hexagon(BetterPolygon):
    sides = 6

assert Hexagon.interior_angles() == 720
# 하위 클래스를 잘못 정의하면 앞의 예제와 똑같은 예외를 볼 수 있다
print('class 이전')

# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#class Point(BetterPolygon):
#    sides = 1

print('class 이후')

# 표준 파이썬 메타클래스 방식의 또 다른 문제점은 
# 클래스 정의마다 메타클래스를 단 하나만 지정할 수 있다는 것이다
class ValidateFilled(type):
    def __new__(meta, name, bases, class_dict):
        # Filled 클래스의 하위 클래스만 검증한다
        if bases:
            if class_dict['color'] not in ('red', 'green'):
                raise ValueError('지원하지 않는 color 값')
        return type.__new__(meta, name, bases, class_dict)

class Filled(metaclass=ValidateFilled):
    color = None  # 모든 하위 클래스에서 이 애트리뷰트의 값을 지정해야 한다

# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#class RedPentagon(Filled, Polygon):
#    color = 'red'
#    sides = 5

# Polygon 메타클래스와 Filled 메타클래스를 함께 사용하려고 시도하면 이해하기 힘든 오류메시지를 볼 수 있다
# 검증을 여러 단계로 만들기 위해 복잡한 메타클래스 type 정의를 복잡한 계층으로 설계함으로써 이런 문제를 해결할 수도 있다

class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        # 루트 클래스가 아닌 경우만 검증한다
        if not class_dict.get('is_root'):
            if class_dict['sides'] < 3:
                raise ValueError('다각형 변은 3개 이상이어야 함')
        return type.__new__(meta, name, bases, class_dict)

class Polygon(metaclass=ValidatePolygon):
    is_root = True
    sides = None  # 하위 클래스에서 이 애트리뷰트 값을 지정해야 한다

class ValidateFilledPolygon(ValidatePolygon):
    def __new__(meta, name, bases, class_dict):
        # 루트 클래스가 아닌 경우만 검증한다
        if not class_dict.get('is_root'):
            if class_dict['color'] not in ('red', 'green'):
                raise ValueError('지원하지 않는 color 값')
        return super().__new__(meta, name, bases, class_dict)

class FilledPolygon(Polygon, metaclass=ValidateFilledPolygon):
    is_root = True
    color = None  # 하위 클래스에서 이 애트리뷰트 값을 지정해야 한다

class GreenPentagon(FilledPolygon):
    color = 'green'
    sides = 5

greenie = GreenPentagon()
assert isinstance(greenie, Polygon)

# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
# 색 오류
#class OrangePentagon(FilledPolygon):
#    color = 'orange'
#    sides = 5

# 하지만 이런 접근 방식은 합성성(composability)를 해친다
# 검증 로직을 다른 클래스 계층 구조에서 적용하려면 모든 로직을 중복정의해야하므로, 코드 재사용이 줄어들고 불필요한 코드가 늘어난다

# __init_subclass__ 특별 클래스 메서드를 사용하면 이 문제도 해결할 수 있다
# super 내장 함수를 사용해 부모나 형재자매 클래스 __init_subclass__를 호출해주는 한, 클래스 계층구조를 쉽게 정의할 수 있다
class Filled:
    color = None  # 하위 클래스에서 이 애트리뷰트 값을 지정해야 한다

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls.color not in ('red', 'green', 'blue'):
            raise ValueError('지원하지 않는 color 값')

class RedTriangle(Filled, Polygon):
    color = 'red'
    sides = 3

ruddy = RedTriangle()
assert isinstance(ruddy, Filled)
assert isinstance(ruddy, Polygon)

#
print('class 이전')

# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#class BlueLine(Filled, Polygon):
#    color = 'blue'
#    sides = 2

print('class 이후')

#
print('class 이전')

# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#class BeigeSquare(Filled, Polygon):
#    color = 'beige'
#    sides = 4

print('class 이후')


# 심지어 다이아몬드 상속 구조에서도 사용할 수 있다
class Top:
    def __init_subclass__(cls):
        super().__init_subclass__()
        print(f'{cls}의 Top')

class Left(Top):
    def __init_subclass__(cls):
        super().__init_subclass__()
        print(f'{cls}의 Left')


class Right(Top):
    def __init_subclass__(cls):
        super().__init_subclass__()
        print(f'{cls}의 Right')


class Bottom(Left, Right):
    def __init_subclass__(cls):
        super().__init_subclass__()
        print(f'{cls}의 Bottom')