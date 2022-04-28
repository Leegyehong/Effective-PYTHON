# 복잡한 식을 쓰는 대신 도우미 함수를 작성하라.

from urllib.parse import parse_qs

my_values = parse_qs('빨강=5&파랑=0&초록=',keep_blank_values=True)
print(repr(my_values)) #{'빨강': ['5'], '파랑': ['0'], '초록': ['']}

print('빨강:', my_values.get('빨강')) # 빨강: ['5']
print('초록:', my_values.get('빨강')) # 초록: ['']
print('투명도:', my_values.get('투명도')) # 투명도: None

red = my_values.get('빨강', [''])[0] or 0
green = my_values.get('초록', [''])[0] or 0
opacity = my_values.get('투명도', [''])[0] or 0

# 이 식은 어려운 데다 원하는 모든 기능을 제공하지도 못한다.
# 파라미터 값을 정수로 변환하여 즉시 수식에 활용하길 바란다.
# 그렇게 하려면 int 함수로 감싸줘야한다.

red = int(my_values.get('빨강', [''])[0] or 0)

# 코드를 읽기 어렵다. 또한 시각적 잡음이 많다.
# 코드를 이해하기 쉽지 않아, 새로 읽는 사람이 이 식이 실제로 어떤 일을 하는지 이해 하기위해서는 많은 시간을 투자해야한다.
# 코드를 짧게 유지하면 멋지기는 하지만, 모든 내용을 한줄에 우겨 넣기 위해 노력할 만큼의 가치는 없다.

# 파이썬에는 이런 경우를 명확하게 표현할 수 있다.
red_str = my_values.get('빨강', [''])
red = int(red_str[0]) if red_str[0] else 0

# 위 코드가 훨씬 좋다. 하지만 여러 줄로 나눠 쓴 완전한 if/else 문 보다는 덜 명확하다.

green_str = my_values.get('초록', [''])
if green_str[0]:
    green = int(green_str[0])
else:
    green = 0
    

# 이 로직을 반복 적용하려면 꼭 도우미 함수를 작성해야한다.

def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found[0]:
        return int(found[0])
    return default

green = get_first_int(my_values, '초록')