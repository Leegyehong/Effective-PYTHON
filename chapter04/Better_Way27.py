# map과 filter 대신 컴프리헨션을 사용하라

# 리스트 컴프리헨션 : 시퀀스나 이터러블에서 새 리스트를 만들어내는 간결한 구문

a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares = []
for x in a:
    squares.append(x**2)

print(squares)

squares = [x**2 for x in a] # 리스트 컴프리헨션

print(squares)

# map 함수보다도 리스트 컴프리헨션이 더 명확함
alt = list(map(lambda x: x ** 2, a))


# 리스트 컴프리헨션은 map과 달리 입력 리스트에서 원소를 쉽게 필터링해 결과에서 원하는 원소를 제거할 수 있다
even_squares = [x**2 for x in a if x % 2 == 0]
print(even_squares)

# filter 내장 함수를 map과 함께 사용해서 같은 결과를 얻을 수 있지만, 코드를 읽기 어렵다
alt = map(lambda x: x**2, filter(lambda x: x % 2 == 0, a))

# 딕셔너리와 집합에도 리스트 컴프리헨션과 동등한 컴프리헨션이 있다
even_squares_dict = {x: x**2 for x in a if x % 2 == 0}
threes_cubed_set = {x**3 for x in a if x % 3 == 0}
print(even_squares_dict)
print(threes_cubed_set)

# 각각의 호출을 적절한 생성자로 감싸면 같은 결과를 map과 filter를 사용해 만들 수 있지만 코드가 길기때문에 여러줄에 나눠쓰고, 잡음이 늘어나므로 피해야한다
alt_dict = dict(map(lambda x: (x, x**2),
                filter(lambda x: x % 2 == 0, a)))
alt_set = set(map(lambda x: x**3,
              filter(lambda x: x % 3 == 0, a)))
