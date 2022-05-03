# 복잡한 기준을 사용해 정렬할 때는 key 파리미터를 사용하라

# sort는 기스트의 내용을 원소 타입에 따른 오름차순으로 정렬한다.

numbers = [93, 86, 11, 68, 70]
numbers.sort()
print(numbers)

# sort가 객체를 어떻게 처리할까

class Tool:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        
        
    def __repr__(self):
        return f'Tool({self.name!r}, {self.weight})'


tools =[
    Tool('수준계', 3.5),
    Tool('해머', 1.25),
    Tool('스크류드라이버', 0.5),
    Tool('끌', 0.25),
]

# sort 메서드 호출하는 객체 비교 특별 메서드가 정의돼 있지 않으므로 이런 타입의 객체를 정렬할 수 없다.
tools.sort() # error

# 이러한 상황을 지원하기 위해 sort에는 key라는 파라미터가 있다. 
# key는 함수여야한다. key 함수에는 정렬 중인 리스트의 원소가 전달되는데 return값은 비교 가능한 값이여야한다.

print('미정렬: ', repr(tools))
tools.sort(key = lambda x : x.name)
print('\n정렬: ', tools)

