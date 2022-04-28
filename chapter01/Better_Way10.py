# 대입식을 사용해 반복을 피하라

# 대입식은 영어로 assignment expression 이며 왈러스 연산자 라고도 부른다
# 파이썬 3.8에 새롭게 도입된 구문이다.

# 일반 대입문은 a = b 라고 쓰며 'a 이퀄 b' 라고 읽는다.
# 왈러스 연산자는 a:=b 라고 쓰며 'a 왈러스 b' 라고 읽는다

# 대입식은 대입문이 쓰일 수 없는 위치에서 변수에 값을 대입할 수 있으므로 유용하다.

# 예를들어 주스바에서 사용할 신선한 과일 바구니를 관리한다고 하자. 
# 과일 바구니의 내용물을 정의하면 다음과 같다.
fresh_fruit = {
    '사과': 10,
    '바나나': 8,
    '레몬': 5
}

# 고객이 레모네이드를 주문했다면 레몬이 최소 1개는 있어야한다
# 개수를 읽어와서 그 값이 0이 아닌지 검사하는 코드다

def make_lemonamde(count):
    pass

def out_of_stock():
    pass

count = fresh_fruit.get('레몬', 0)
if count:
    make_lemonamde(count)
else:
    out_of_stock()
    
# 간단해 보이지만 문제가 많다.
# count 변수는 if문의  첫 번째 블록 안에서만 쓰인다.
# if 앞에서 count를 정의하면 else 블록이나 그 이후의 코드에서 
# count 변수에 접근해야 할 필요가 있는 것 처럼 보이기 때문에 변수가 중요해보인다.
# 하지만 그렇지 않다.

# 값을 가져와서 그 값이 0인지 아닌지 검사한 후 사용하는 패턴이 자주 발생한다.
# count가 여러 번 쓰이는 경우를 해결하기 위해 개발자가 가독성을 해치는 갖가지 꼼수를 사용해왔다.(Better_Way05 참고)
# 다행히 대입식이 추가되면서 제대로 처리할 수 있게됐다.

if count := fresh_fruit.get('레몬', 0):
    make_lemonamde(count)
else:
    out_of_stock()
    
# 한줄 더 짧기도 하지만, count가 if문의 첫 번째 블록에만 의미가 있다는 점이 명확히 보이기 때문에 이 코드가 더 읽기 쉽다.


# 파이썬에는 유연한 switch/case 문이 없다는 점이 자주 당황하게 만드는 원인 중 하나다.
# 이런 유형의 기능을 흉내내는 일반적인 스타일은 if, elif, else문을 더 깊게 내포시키는 것이다.

count = fresh_fruit('바나나', 0)
if count>=2:
    pieces = slice_bananas(count)
    to_enjoy = make_smoothies(pieces)
else:
    count = fresh_fruit.get('사과', 0)
    if count>=4:
        to_enjoy = make_cider(count)
    else:
        count = fresh_fruit.get('레몬', 0)
        if count:
            to_enjoy = make_lemonamde(count)
        else:
            to_enjoy = '아무것도 없음'
            

#  이와 같이 지저분한 요소가 흔하다.
# 왈러스 연산자를 사용하면 switch/case문과 같은 다중 선택 전용 구문과 거의 비슷한 느낌이 드는 우아한 해법을 만들 수 있다.

if(count := fresh_fruit('바나나', 0)) >=2:
    pieces = slice_bananas(count)
    to_enjoy = make_smoothies(pieces)
elif (count := fresh_fruit.get('사과', 0)) >=4:
    to_enjoy = make_cider(count)
elif (count := fresh_fruit.get('레몬', 0)):
    to_enjoy = make_lemonamde(count)
else:
    to_enjoy = '아무것도 없음'
    
    

# do/while 루프가 없다는 점도 당황하게 만든다.

bottles = []
fresh_fruit = pick_fruit()
while fresh_fruit:
    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)
    fresh_fruit = pick_fruit()

print(bottles)

# 이 코드는 fresh_fruit = pick_fruite() 호출을 두 번(한 번은 루프 직전에 초기화하면서, 다른 한 번은 루프 끝에서) 하므로 반복적이다.
# 이 상황에서 코드 재사용을 향상시키기 위한 전략은
# 무한 루프 - 중간에서 끝내기(loop-and-a-half) 를 사용하는 것이다.
# 이 관용을 사용하면 코드 반복을 없앨 수 있지만, while 루프를 맹목적인 무한 루프로 만들기 때문데 while 루프의 유용성이 줄어든다.
# 이 방식에는 루프 흐름 제어가 모두 break문에 달려있다.

bottles = []
while True:                     # 무한 루프(Loop)
    fresh_fruit = pick_fruit()
    if not fresh_fruit:         # 중간에서 끝내기(And a half)
        break
    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)

print(bottles)

# 왈러스 연산자를 사용하면 대입하고 조건을 검색할 수 있으므로 무한 루프 - 중간에서 끝내기 관용의 필요성이 줄어든다.
# 이 해법이 더 짧고 읽기 쉽기 때문에 이 방식을 우선적으로 사용해야한다.

bottles = []
while fresh_fruit := pick_fruit():
    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)

print(bottles)