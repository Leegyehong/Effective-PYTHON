# 합성 가능한 클래스 확장이 필요하면 메타클래스보다는 클래스 데코레이터를 사용하라

# 메타클래스를 사용하면 클래스 생성을 다양한 방법으로 커스텀화할 수 있지만
# 처리할 수 없는 경우가 있다

#  어떤 클래스의 모든 메서드를 감싸서 메서드에 전달되는 인자, 리턴 값, 예외를 모두 출력하는 경우
from functools import wraps

def trace_func(func):
    if hasattr(func, 'tracing'):  # 단 한번만 데코레이터를 적용한다
        return func

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            result = e
            raise
        finally:
            print(f'{func.__name__}({args!r}, {kwargs!r}) -> '
                  f'{result!r}')

    wrapper.tracing = True
    return wrapper
# 이 데코레이터를 새 dict 하위 클래스에 속한 여러 특별 메서드에 적용할 수 있다
class TraceDict(dict):
    @trace_func
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @trace_func
    def __setitem__(self, *args, **kwargs):
        return super().__setitem__(*args, **kwargs)

    @trace_func
    def __getitem__(self, *args, **kwargs):
        return super().__getitem__(*args, **kwargs)


trace_dict = TraceDict([('안녕', 1)])
trace_dict['거기'] = 2
trace_dict['안녕']
try:
    trace_dict['존재하지 않음']
except KeyError:
    pass # 키 오류가 발생할 것으로 예상함

# 이 코드의 문제점은 꾸미려는 모든 메서드를 데코레이터를 써서 재정의해야함
# 이런 불필요한 중복으로 인해 가독성도 나빠지고, 실수를 저지르기도 쉬움
# 나중에 dict 상위 클래스에 메서드를 추가하면, TraceDict에서 그 메서드를 재정의하기 전까지는 데코레이터 적용이 되지않음

# 이 문제를 해결하는 방법은 메타클래스를 사용해 모든 메서드를 자동으로 감싸는 것
import types

trace_types = (
    types.MethodType,
    types.FunctionType,
    types.BuiltinFunctionType,
    types.BuiltinMethodType,
    types.MethodDescriptorType,
    types.ClassMethodDescriptorType)


class TraceMeta(type):
    def __new__(meta, name, bases, class_dict):
        klass = super().__new__(meta, name, bases, class_dict)

        for key in dir(klass):
            value = getattr(klass, key)
            if isinstance(value, trace_types):
                wrapped = trace_func(value)
                setattr(klass, key, wrapped)

        return klass


class TraceDict(dict, metaclass=TraceMeta):
    pass

trace_dict = TraceDict([('안녕', 1)])
trace_dict['거기'] = 2
trace_dict['안녕']
try:
    trace_dict['존재하지 않음']
except KeyError:
    pass # 키 오류가 발생할 것으로 예상함


# 이 코드는 잘  작동한다

# 하지만 메타클래스를 사용하는 접근 방식은 적용 대상 클래스에 대한 제약이 너무 많다
# 이런 문제를 해결하고자 클래스 데코레이터를 지원한다

def my_class_decorator(klass):
    klass.extra_param = '안녕'
    return klass

@my_class_decorator
class MyClass:
    pass

print(MyClass)
print(MyClass.extra_param)

def trace(klass):
    for key in dir(klass):
        value = getattr(klass, key)
        if isinstance(value, trace_types):
            wrapped = trace_func(value)
            setattr(klass, key, wrapped)
    return klass


@trace
class TraceDict(dict):
    pass

trace_dict = TraceDict([('안녕', 1)])
trace_dict['거기'] = 2
trace_dict['안녕']
try:
    trace_dict['존재하지 않음']
except KeyError:
    pass # 키 오류가 발생할 것으로 예상함