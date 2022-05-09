# 컴프리헨션 내부에 제어 하위식을 세 개 이상 사용하지 말라

# 컴프리헨션은 루프를 여러 수준으로 내포하도록 허용한다
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row]

squared = [[x**2 for x in row] for row in matrix]
print(squared)

# 만약 이런 컴프리헨션 안에 다른 루프가 들어 있으면  코드가 너무 길어져서 여러 줄로 나눠 써야한다
my_lists = [
    [[1, 2, 3], [4, 5, 6]],
    [[7, 8, 9], [1, 2, 3]],
    [[4, 5, 6], [7, 8, 9]],
]
flat = [x for sublist1 in my_lists
        for sublist2 in sublist1
        for x in sublist2]

# 이 정도가 되면 다중 컴프리헨션이 다른 대안에 비해 더 길어진다
# 다음은 일반 루프문을 사용해 같은 결과를 만드는 코드이다
# 들여쓰기로 인해 3단계 리스트 컴프리헨션보다 루프가 더 명확해보인다
flat = []
for sublist1 in my_lists:
    for sublist2 in sublist1:
        flat.extend(sublist2)
        
        
        
# 컴프리헨션은 여러 if 조건을 허용한다
# 여러 조건을 같은 수준의 루프에 사용하면 암시적으로 and 식을 의미한다

a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
b = [x for x in a if x > 4 if x % 2 == 0]
c = [x for x in a if x > 4 and x % 2 == 0]

# 만약 3으로 나눠 떨어지는 셀만 남기고, 합게가 10보다 더 큰 행을 남기고 싶다면
# 컴프리헨션을 사용해 표현하면 코드가 길어지지는 않지만 읽기가 매우 힘들다
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
filtered = [[x for x in row if x % 3 == 0]
            for row in matrix if sum(row) >= 10]
print(filtered)