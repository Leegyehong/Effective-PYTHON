# for나 while 루프 뒤에 else블록을 사용하지 말라

for i in range(3):
    print('Loop', i)
else:
    print('Else block!')
    
    
# else 블록은 루프가 끝나자마자 실행된다.
# else를 배운 프로그래머들은 '루프가 정상적으로 완료되지 않으면 else블록을 실행하라' 라고 가정하기 쉽다
# 하지만 실제 else블록은 반대로 동작한다. break문을 사용하면 else블록이 실행되지 않는다.

for i in range(3):
    print('Loop', i)
    if i ==1:
        break
else:
    print('Else block!')

# 놀라운 점은 빈 시퀀스에 대한 루프는 실행된다

for x in []:
    print('이 줄은 실행 x')
else:
    print('For Else block!')

# while문의 조건이 False인 경우도 실행된다.
while False:
    print('이 줄은 실행 x')
else:
    print('While Else block!')
    
# 이유는 루프를 사용해 검색을 수행할 경우, 루프 바로 뒤에 있는 else 블록이 그와 같이 동작해야 유용하기 때문
# 예를 들어 서로소(두 수의 공약수가 1밖에 없음) 인지 알아보고 싶다면 모든 수를 두 수를 나눌 수 있는지 검사하면 된다.
# 루프가 break를 만나지 않으면 두 수가 서로소 이므로 else블록이 실행된다.

a = 4
b = 9
for i in range(2, min(a,b)+1):
    print('검사 중', i)
    if a % i == 0 and b % i ==0:
        print('서로소 아님')
        break
else:
    print('서로소')
    
# 하지만 실전에서 이런 식으로 코드를 작성하지 않을 것이다.
# 대신에 도우미 함수를 작성할 것이다.

# 1) 원하는 조건을 찾자마자 빠르게 함수를 return 하는 방식

def coprime(a, b):
    for i in range(2, min(a,b)+1):
        if a % i == 0 and b % i ==0:
            return False
    return True

# 2) 루프 안에서 원하는 대상을 찾았는지 나타내는 결과 변수를 도입

def coprime(a, b):
    is_coprime = True
    for i in range(2, min(a,b)+1):
        if a % i == 0 and b % i ==0:
            is_coprime = False
            break
    return is_coprime

# 두 접근 모두 코드를 처음 보는 사람에게는 훨씬 더 명확해 보인다.
# 상황에 따라 둘 다 좋은 선택이 될 수 있다.
# 하지만 else블록을 사용함으로써 얻을 수 있는 표현력보다는 미래에 이 코드를 이해하려는 사람(자신 포함)이 느끼게 될 부담감이 더 크다
# 파이썬에서 루프와 같은 간단한 구성요소는 그 자체로 의미가 명확해야한다.