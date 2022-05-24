# 지연 계산 애트리뷰트가 필요하면 __getattr__, __getattribute__, __setattr__을 사용하라

# 파이썬 object 훅을 사용하면 시스템을 서로 접합하는 제너릭 코드를 쉽게 작성할 수 있다
# 데이터베이스 레코드를 파이썬 객체로 표현하고 싶다면?

# 데이터베이스에는 이미 스키마 집합이 있다
# 우리가 만들 레코드에 대응하는 코드도 데이터베이스 스키마가 어떤 모습인지 알아야한다
# 하지만 파이썬에서 데이터베이스와 객체를 연결해주는 코드가 특정 스키마만 표현할 필요는 없다

# 어떻게 스키마를 표현하는 클래스를 더 일반화할 수 있을까?
# @property 메서드, 디스크립터 등은 미리 정의해야만 사용할 수 있으므로 사용할 수 없다

# __getattr__ 이라는 특별메서드를 사용해 이런 동적 기능을 활용할 수 있다
# __getattr__ 정의가 있으면, 객체의 인스턴스 딕셔너리에서 찾을 수 없는 애트리뷰트에 접근할 때마다 __getattr__이 호출된다

class LazyRecord:
    def __init__(self):
        self.exists = 5

    def __getattr__(self, name):
        value = f'{name}의 값'
        setattr(self, name, value)
        return value

data = LazyRecord()
print('이전:', data.__dict__)
print('foo:', data.foo)
print('이후:', data.__dict__)

# 여기서 무한 재귀를 피하고 실제 프로퍼티 값을 가져오기 위해 상위 클래스의 __getattr__ 구현을 사용했다는 점을 유의해라
class LoggingLazyRecord(LazyRecord):
    def __getattr__(self, name):
        print(f'* 호출: __getattr__({name!r}), '
              f'인스턴스 딕셔너리 채워 넣음')
        result = super().__getattr__(name)
        print(f'* 반환: {result!r}')
        return result

data = LoggingLazyRecord()
print('exists: ', data.exists)
print('첫 번째 foo: ', data.foo)
print('두 번째 foo: ', data.foo)

# 데이터베이스에 트랜잭션이 필요하다고 할 때
# 유효한 레코드가 있는지, 트랜잭션이 열려있는지 확인해야한다
#  기존 애트리뷰트를 확인하는 빠른 경로로 객체의 인스턴스 딕셔너리를 사용하기 때문에
# __getattr__ 훅으로는 이런 기능을 안정적으로 만들 수 없다

# 이와 같은 고급 사용법을 제공하기 위해 파이썬은 __getattribute__ 라는 다른 object 훅을 제공한다
# 애트리뷰트에 접근할 때마다 호출된다
# 심지어 애트리뷰트 디렉터리에 존재하는 애트리뷰트에 접근 할 때도 호출된다
class ValidatingRecord:
    def __init__(self):
        self.exists = 5
    def __getattribute__(self, name):
        print(f'* 호출: __getattr__({name!r})')
        try:
            value = super().__getattribute__(name)
            print(f'* {name!r} 찾음, {value!r} 반환')
            return value
        except AttributeError:
            value = f'{name}을 위한 값'
            print(f'* {name!r}를 {value!r}로 설정')
            setattr(self, name, value)
            return value

data = ValidatingRecord()
print('exists: ', data.exists)
print('첫 번째 foo: ', data.foo)
print('두 번째 foo: ', data.foo)

class MissingPropertyRecord:
    def __getattr__(self, name):
        if name == 'bad_name':
            raise AttributeError(f'{name}을 찾을 수 없음')
        return 1 # 무조건 1 반환

data = MissingPropertyRecord()
# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#data.bad_name


# hasattr 내장 함수를 통해 프로퍼티가 존재하는지 검사하는 기능과
# getattr 내장함수를 통해 프로퍼티 값을 꺼내오는 기능에 의존할 때도 있다
# 이 두 함수도 __getattr__을 호출하기 전에 애트리뷰트 이름을 인스턴스 딕셔너리에서 검색한다

data = LoggingLazyRecord() # __getattr__을 구현
print('이전: ', data.__dict__)
print('최초에 foo가 있나: ', hasattr(data, 'foo'))
print('이후: ', data.__dict__)
print('다음에 foo가 있나: ', hasattr(data, 'foo'))

#
data = ValidatingRecord() # __getattribute__를 구현
print('최초에 foo가 있나: ', hasattr(data, 'foo'))
print('다음에 foo가 있나: ', hasattr(data, 'foo'))

# 파이썬 객체에 값이 대인된 경우
# 이 값을 데이터베이스에 다시 저장하고 싶다면?
# __setattr__을 사용하면, 이런 기능을 비슷하게 구현할 수 있다
class SavingRecord:
    def __setattr__(self, name, value):
        # 데이터를 데이터베이스 레코드에 저장한다
        super().__setattr__(name, value)

class LoggingSavingRecord(SavingRecord):
    def __setattr__(self, name, value):
        print(f'* 호출: __setattr__({name!r}, {value!r})')
        super().__setattr__(name, value)

data = LoggingSavingRecord()
print('이전: ', data.__dict__)
data.foo = 5
print('이후: ', data.__dict__)
data.foo = 7
print('최후:', data.__dict__)

#
class BrokenDictionaryRecord:
    def __init__(self, data):
        self._data = {}
    def __getattribute__(self, name):
        print(f'* 호출: __getattribute__({name!r})')
        return self._data[name]

data = Brokedata = BrokenDictionaryRecord({'foo': 3})
# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#data.foo

# 위 코드는 재귀를 수행하다가 죽어버린다
# 이 문제는 __getattribute__가 self.data에 접근해서 __getattribute__가 다시 호출되기 때문
# 해결방법은 super().__getattribute__를 호출해 값을 가져오는 것이다
class DictionaryRecord:
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, name):
        print(f'* 호출: __getattribute__({name!r})')
        data_dict = super().__getattribute__('_data')
        return data_dict[name]

data = DictionaryRecord({'foo': 3})
print('foo: ', data.foo)

