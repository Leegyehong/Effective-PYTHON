# 여러 이터레이터에 대해 나란히 루프를 수행하려면 zip을 사용하라

# 리스트 컴프리헨션을 사용하면 새로운 list를 파생시키기 쉽다.
names = ['Mike', '이계홍', 'Ronaldo']
counts = [len(n) for n in names]
print(counts)

# 만들어진 list의 각 원소는 소스 list에서 같은 인덱스 위치에 있는 원소와 관련이 있다.
# 두 리스트를 동시에 이터레이션할 경우 names 소스 리스트의 길이를 사용해 이러테이션할 수 있다.

longest_name = None
max_count = 0

for i in range(len(names)):
    count = counts[i]
    if count > max_count:
        longest_name = names[i]
        max_count = count

print(longest_name)

# 문제는 위 루프가 시각적으로 잡음이 많다.
# 인덱스 i를 사용해  가져오는 연산이 두 번 일어난다.
# enumerate를 사용하면 약간 나아지지만 여전히 이상적이지 않다.

for i, name in enumerate(names):
    count = counts[i]
    if count > max_count:
        longest_name = name
        max_count = count
        
        
# 이런 코드를 더 깔끔하게 만들 수 있도록 zip 함수를 제공한다.
# zip은 둘 이상의 이터레이터를 지연 계산 제너레이터를 사용해 묶어준다.

for name, count in zip(names, counts):
    if count > max_count:
        longest_name = name
        max_count = count
        
