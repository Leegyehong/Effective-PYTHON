# __set_name__으로 클래스 애트리뷰트를 표시하라

# 클래스가 정의된 후 클래스가 실제로 사용되기 이전인 시점에 프로퍼티를 변경하거나 표시할 수 있는 기능

# 애트리뷰터 사용을 좀 더 자세히 관찰하고자 디스크립터를 쓸 때 이런 접근방식을 활용함

# 애트리뷰트와 컬럼 이름을 연결하는 디스크립터
class Field:
    def __init__(self, name):
        self.name = name
        self.internal_name = '_' + self.name

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)

class Customer:
    # 클래스 애트리뷰트
    first_name = Field('first_name')
    last_name = Field('last_name')
    prefix = Field('prefix')
    suffix = Field('suffix')

cust = Customer()
print(f'이전: {cust.first_name!r} {cust.__dict__}')
cust.first_name = '유클리드'
print(f'이후: {cust.first_name!r} {cust.__dict__}')

# 하지만 이 클래스 정의는 중복이 많아보인다
# 클래스 안에서 왼쪽에 필드 이름을 이미 정의했는데 굳이 같은 정보가 들어 있는 문자열을
# Field 디스크립터에게 다시 전달해야 할 이유가 없다

# 이런 중복을 줄이기 위해 메타클래스를 사용할 수 있다
# 메타클래스를 사용하면 class 문에 직접 훅을 걸어서 class 본문이 끝나자마자 필요한 동작을 수행할 수 있다
class Meta(type):
    def __new__(meta, name, bases, class_dict):
        for key, value in class_dict.items():
            if isinstance(value, Field):
                value.name = key
                value.internal_name = '_' + key
        cls = type.__new__(meta, name, bases, class_dict)
        return cls

class DatabaseRow(metaclass=Meta):
    pass


class Field:
    def __init__(self):
        # 이 두 정보를 메타클래스가 채워 준다
        self.name = None
        self.internal_name = None

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)

class BetterCustomer(DatabaseRow):
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()

cust = BetterCustomer()
print(f'이전: {cust.first_name!r} {cust.__dict__}')
cust.first_name = '오일러'
print(f'이후: {cust.first_name!r} {cust.__dict__}')

# 이 접근 방법의 문제점은 DatabaseRow를 상송하는 것을 잊어버리거나 
# 클래스 계층 구조로 인한 제약 때문에 어쩔 수 없이 DatabaseRow를 상속할 수 없는 경우이다
# DatabaseRow를 상속하지 않으면 코드가 깨진다
class BrokenCustomer:
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()

cust = BrokenCustomer()
# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#cust.first_name = '메르센'

# 이 문제를 해결하는 방법은 디스크립터에 __set_name__ 특별 메서드를 사용하는 것
class Field:
    def __init__(self):
        self.name = None
        self.internal_name = None

    def __set_name__(self, owner, name):
        # 클래스가 생성될 때 모든 스크립터에 대해 이 메서드가 호출된다
        self.name = name
        self.internal_name = '_' + name

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


class FixedCustomer:
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()

cust = FixedCustomer()
print(f'이전: {cust.first_name!r} {cust.__dict__}')
cust.first_name = '메르센'
print(f'이후: {cust.first_name!r} {cust.__dict__}')