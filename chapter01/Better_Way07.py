# range보다는 enumerate를 사용하라

# list처럼 이터레이셔할 대상 데이터 구조가 있으면 시퀀스에 대해 바로 루프를 돌 수 있다.
flavor_list = ['바닐라', '초콜릿', '피칸', '딸기']
for flavor in flavor_list:
    print(f'{flavor} 맛있어요')
    
# 리스트를 이터레이션하면서 몇 번째 원소를 처리중인지 알아야  할 때가 있다.
for i in range(len(flavor_list)):
    flavor = flavor_list[i]
    print(f'{i+1}: {flavor}')
    
# 위 코드는 투박해보인다. list의 길이를 알아야 하고, 인덱스를 사용해 배열 원소에 접근해야한다.
# 단계가 여러 개이므로 코드를 읽기 어렵다.
# 파이썬은 이런 문제를 해결할 수 있는 enumerate 내장 함수를 제공한다.

it = enumerate(flavor_list)
print(next(it)) # (0, '바닐라')
print(next(it)) # (1, '초콜릿')

for i, flavor in enumerate(flavor_list):
    print(f'{i+1}: {flavor}')