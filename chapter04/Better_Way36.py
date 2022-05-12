# 이터레이터나 제너레이터를 다룰 때는 itertools를 사용하라

# itertools 내장 모듈에는 이터레이터를 조직화하거나 사용할 때 쓸모 있는 여러 함수가 있다

# 여러 이터레이터 연결하기
import itertools

# 1) chain
it = itertools.chain([1, 2, 3], [4, 5, 6])
print(list(it))

# 2) repeat
it = itertools.repeat('안녕', 3)
print(list(it))

# 3) cycle
it = itertools.cycle([1, 2])
result = [next(it) for _ in range (10)]
print(result)

# 4) tee
it1, it2, it3 = itertools.tee(['하나', '둘'], 3)
print(list(it1))
print(list(it2))
print(list(it3))

# 5) zip_longest
keys = ['하나', '둘', '셋']
values = [1, 2]

normal = list(zip(keys, values))
print('zip:', normal)

it = itertools.zip_longest(keys, values, fillvalue='없음')
longest = list(it)
print('zip_longest:', longest)


# 이터레이터에서 원소 거르기

# 1) islice
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
first_five = itertools.islice(values, 5)
print('앞에서 다섯 개:', list(first_five))

middle_odds = itertools.islice(values, 2, 8, 2)
print('중간의 홀수들:', list(middle_odds))

# 2) takewhile
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
less_than_seven = lambda x: x < 7
it = itertools.takewhile(less_than_seven, values)
print(list(it))

# 3) dropwhile
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
less_than_seven = lambda x: x < 7
it = itertools.dropwhile(less_than_seven, values)
print(list(it))

# 4) filterfalse
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = lambda x: x % 2 == 0

filter_result = filter(evens, values)
print('Filter:', list(filter_result))

filter_false_result = itertools.filterfalse(evens, values)
print('Filter false:', list(filter_false_result))

# 이터레이터에서 원소의 조합 만들어내기

# 1) accumulate
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
sum_reduce = itertools.accumulate(values)
print('합계:', list(sum_reduce))

def sum_modulo_20(first, second):
    output = first + second
    return output % 20

modulo_reduce = itertools.accumulate(values, sum_modulo_20)
print('20으로 나눈 나머지의 합계:', list(modulo_reduce))

# 2) product
single = itertools.product([1, 2], repeat=2)
print('리스트 한 개:', list(single))

multiple = itertools.product([1, 2], ['a', 'b'])
print('리스트 두 개:', list(multiple))

# 3) permutations
it = itertools.permutations([1, 2, 3, 4], 2)
print(list(it))

# 4) combinations
it = itertools.combinations([1, 2, 3, 4], 2)
print(list(it))

# 5) combinations_with_replacement
it = itertools.combinations_with_replacement([1, 2, 3, 4], 2)
print(list(it))
