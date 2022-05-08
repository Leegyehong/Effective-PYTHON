# 변수 영역과 클로저의 상호작용 방식을 이해하라


# 숫자로 이루어진 list를 정렬하되, 정렬한 리스트의 앞쪽에는 우선순위를 부여한 몇몇 숫자를 위치시킨다고 가정하였을 때
# 이러한 경우를 해결하는 일반적인 방법은 리스트의 sort 메서드에 key 인자로 도우미 함수를 전달하는 방식

def sort_priority(values, group):
    def helper(x):
        if x in group:
            return (0, x)
        return (1, x)
    values.sort(key=helper)

numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = {2, 3, 5, 7}
sort_priority(numbers, group)
print(numbers)

# 이 함수가 예상대로 작동하는 이유 3가지

# 1. 파이썬이 클로저(closure)를 지원
#   a. 클로저란 자신이 정의된 영역 밖의 변수를 참조하는 함수. 이러한 점 때문에 helper 함수가 sort_priority의 group 인수에 접근

# 2. 파이썬에서 함수는 일급 객체(fist-class object)
#   a. 함수를 직접 참조하고 변수에 할당하고, 다른 함수에 인자로 전달하고 표현식과 if문 등에서 비교할 수 있다는 의미
#      따라서 sort 메서드에서 클로저 함수를 key 인수로 받음

# 3. 파이썬에서는 튜플을 비교하는 특정 규칙 존재
#   a. 먼저 인덱스 0 으로 아이템을 비교하고 그 다음으로 인덱스 1, 다음은 2로 진행 


# 이 함수가 우선순위가 높은 원소가 있는지 여부도 반환하게 만들어서 UI가 그에 따라 동작하게하면 좋다
# 이런 동작을 추가하는 것은 쉽다
# 각 원소가 어떤 그룹에 들어 있는지 결정하는 클로저 함수가 있으므로, 클로저를 사용해 우선수위가 높은 원소를 발견했음을 표시하는 플래그를 설정하여 반환한다

def sort_priority2(numbers, group):
    found = False
    def helper(x):
        if x in group:
            found = True  
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found

numbers = [8, 3, 1, 2, 5, 4, 7, 6]
found = sort_priority2(numbers, group)
print('Found:', found) # False
print(numbers) # [2, 3, 5, 7, 1, 4, 6, 8]

# 정렬된 결과는 올바르지만 found의 결과는 틀린 것을 확인할 수 있다
# 표현식에서 함수를 참조할 때 다음과 같은 순서로 scope를 탐색한다

# 1. 현재 함수의 scope
# 2. 현재 함수를 둘러싼 scope (현재 함수를 둘러싸고 있는 함수 등)
# 3. 현재 코드가 들어있는 모듈의 scope(global scope 이라고도 부름)
# 4. 내장 scope

def sort_priority2(numbers, group):
    found = False         # Scope: 'sort_priority2'
    def helper(x):
        if x in group:
            found = True  # Scope: 'helper' -- Bad!
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found

def sort_priority3(numbers, group):
    found = False
    def helper(x):
        nonlocal found  # Added
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found

numbers = [8, 3, 1, 2, 5, 4, 7, 6]
found = sort_priority3(numbers, group)
assert found
assert numbers == [2, 3, 5, 7, 1, 4, 6, 8]