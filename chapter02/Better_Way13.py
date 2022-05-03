# 슬라이싱보다는 나머지를 모두 잡아내는 언패킹을 사용하라

car_ages = [0, 9, 4, 8, 7, 20, 19, 1, 6, 15]
car_ages_descending = sorted(car_ages, reverse=True)
oldest, second_oldest = car_ages_descending

# 기본 언패킹으로 맨 앞에서 원소를 두 개 가져오면 실행 시점에 예외가 발생한다.
# 파이썬을 처음 사용하는 사람은 이런 상황에서 인덱스와 슬라이싱을 자주 사용한다.

oldest = car_ages_descending[0]
second_oldest = car_ages_descending[1]
others = car_ages_descending[2:]

# 실제로는 잘 작동하지만 시각적으로 잡음이 있다.
# 또한 시퀀스의 원소를 여러 하위 집합으로 나누면 1 차이 나는 인덱스로 오류를 만들어내기 쉽다.


#이런 상황을 더 잘 다룰수 있도록 파이썬은 별표 식(starred expression)을 지원한다.

oldest, second_oldest, *others = car_ages_descending
print(oldest, second_oldest, others)

# 별표 식을 다른 위치에 쓸 수도 있다.
oldest, *others, youngest = car_ages_descending
print(oldest, youngest, others)

*others, second_youngest, youngest = car_ages_descending
print(youngest, second_youngest, others)

# 하지만 별표 식이 포함된 언패킹 대입을 처리하려면 필수인 부분이 적어도 하나는 있어야한다.
#   *others = car_ages_descending # error

# 한 수준의 언패킹 패턴에 별표 식을 두 개 이상 쓸 수도 없다.
#   first, *middle, *second_middle, last = [1, 2, 3, 4] error

# 하지만 여러 계층으로 이뤄진 구조를 할 때는 서로 다른 부분에 포함되는 한 여럿 사용해도 된다.
# 권하지는 않지만 직관을 키울 수 있다.

car_inventory = {
    '시내': ('그랜저', '아반떼', '티코'),
    '공항': ('제네시스 쿠페', '소나타', 'K5', '엑센트')
}
((loc1, (best1, *rest1)),
 (loc2, (best2, *rest2))) = car_inventory.items()

print(f'{loc1} 최고는 {best1}, 나머지는 {len(rest1)} 종')
print(f'{loc2} 최고는 {best2}, 나머지는 {len(rest2)} 종')