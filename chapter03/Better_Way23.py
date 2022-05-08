# 키워드 인자로 선택적인 기능을 제공하라

# 파이썬에서도 함수를 호출할 때 위치에 따라 인자를 넘길 수 있다
def remainder(number, divisor):
    return number % divisor

assert remainder(20, 7) == 6

remainder(20, 7)
remainder(20, divisor=7)
remainder(number=20, divisor=7)
remainder(divisor=7, number=20)

# 위치 기반 인자를 지정하려면 키워드 인자보다 앞에 지정해야한다
remainder(20, number=7) # error

# 딕셔너리의 내용물을 사용해 함수를 호출하고 싶다면 ** 연산자를 사용할 수 있다
my_kwargs = {
	'number': 20,
	'divisor': 7,
}
remainder(**my_kwargs) 

# ** 연산자를 위치 인자나 키워드 인자와 섞어서 함수를 호출할 수도 있다, 다만 중복되는 인자가 없어야 한다
my_kwargs = {
	'divisor': 7,
}
remainder(number=20, **my_kwargs) 

# ** 연산자를 여러 번 사용할 수도 있다 다만 여러 딕셔너리에 겹치는 키가 없어야 한다
my_kwargs = {
	'number': 20,
}
other_kwargs = {
	'divisor': 7,
}
remainder(**my_kwargs, **other_kwargs)

# 아무 키워드 인자나 받는 함수를 만들고 싶다면, 모든 키워드 인자를 dict에 모아주는 **kwargs 라는 파라미터를 사용한다
def print_parameters(**kwargs):
    for key, value in kwargs.items():
        print(f'{key} = {value}')

print_parameters(alpha=1.5, beta=9, gamma=4)

# 키워드 인자가 제공하는 유연성을 활용하면 세가지 이점이 있다

# 첫 번째
# 코드를 처음 보는 사람들에게 함수 호출 의미를 명확히 알려줄 수 있다
# ex) remainder(20, 7) 이라는 호출을 보면 remainder 함수 구현을 보지 않고서는 어떤 인자가 number이고, divisor인지 알 수 없지만
#    키워드 인자를 사용하면 목적이 명확해진다

# 두 번째
# 함수 정의에서 디폴트 값을 지정할 수 있다
# 따라서 필요할 때는 원하는 함수 인자를 설정할 수 있는 기능을 제공하지만 그렇지 않은 대부분의 경우에는 디폴트 동작을 그냥 받아들여도 된다
# 이로 인해 코드 중복과 잡음이 줄어 든다

def flow_rate(weight_diff, time_diff):
    return weight_diff / time_diff

weight_diff = 0.5
time_diff = 3
flow = flow_rate(weight_diff, time_diff)
print(f'{flow:.3} kg per second')

# 위 함수에서 단위를 추가해보자

def flow_rate(weight_diff, time_diff, period):
    return (weight_diff / time_diff) * period

# 이렇게 바꾼 함수를 호출하려면 매번 period를 지정해줘야한다
# 잡음을 줄이기 위해 디폴트 값을 지정한다

def flow_rate(weight_diff, time_diff, period=1):
    return (weight_diff / time_diff) * period

flow_per_second = flow_rate(weight_diff, time_diff)
flow_per_hour = flow_rate(weight_diff, time_diff, period=3600)
print(flow_per_second)
print(flow_per_hour)

# 세 번째
# 어떤 함수를 사용하던 기존 호출자에게는 하위 호환성을 제공하면서 함수 파라미터를 확장할 수 있는 방법을 제공한다
# 이로 인해 기존 코드를 별도로 마이그레이션 하지 않아도 기능을 추가할 수 있고 이는 새로운 버그가 생길 여지가 줄어든다는 뜻이다


def flow_rate(weight_diff, time_diff,
              period=1, units_per_kg=1):
    return ((weight_diff * units_per_kg) / time_diff) * period

# units_per_kg 의 디폴트 값은 1로 모든 기존 호출 코드는 동작이 바뀌지 않는다
pounds_per_hour = flow_rate(weight_diff, time_diff,
                            period=3600, units_per_kg=2.2)
print(pounds_per_hour)

pounds_per_hour = flow_rate(weight_diff, time_diff, 3600, 2.2)
print(pounds_per_hour)