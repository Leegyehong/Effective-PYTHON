# C 스타일 형식 문자열을 str.format과 쓰기보다는 f-문자열을 통한 인터폴레이션을 사용하자

a = 0b10111011
b = 0xc5f

print('이진수 : %d, 십육진수 : %d' %(a,b)) #이진수 : 187, 십육진수 : 3167

# 다른 언어에서 써봤기 때문에 익숙하고 편하다는 이유로 C 스타일 형식 문자열을 사용한다.
# 하지만 파이썬에서 이러한 형식을 사용하는 데에 네 가지 문제점이 있다.

# 1) 형식화 식에서 오른쪽에 있는 tuple 내 데이터 값의 순서를 바꾸거나 값의 타입을 바꾸면 오류가 발생할 수 있다.

key = 'my_var'
value = 1.234
formatted = '%-10s = %.2f' %(key,value)
print(formatted) # my_var     = 1.23

reordered_tuple = '%-10s = %.2f' %(value,key)

# 2) 형식화를 하기 전에 값을 살짝 변경해야 한다면 식을 읽기가 어려워진다.

pantry = [
    ('아보카도', 1.25),
    ('바나나', 2.5),
    ('체리', 15)
]
for i, (item, count) in enumerate(pantry):
    print('#%d : %-10s = %.2f' %(i, item, count ))
    
    
# 값을 조금 바꿔서 출력된 메시지를 좀 더 쓸모있게 만들고 싶다면, tuple의 길이가 길어져서 여러줄에 나눠 써야하는데 가독성이 나빠진다.
for i, (item, count) in enumerate(pantry):
    print('#%d : %-10s = %.2f' %(
        i+1,
        item.title(),
        round(count)))
    

# 3) 형식화 문자열에서 같은 값을 여러 번 사용하고 싶다면 튜플에서 같은 값을 여러번 반복해야 한다.

template = '%s는 음식을 좋아해. %s가 요리하는 모습을 봐요'
name = '계홍'
formatted = template % (name, name)
print(formatted)


# 이런 문제를 해결하기 위해 파이썬의 % 연산자에는 튜플 대신 딕셔너리를 사용하는 기능이 추가됐다.
name = '계홍'

template = '%s는 음식을 좋아해. %s가 요리하는 모습을 봐요'
before = template % (name, name) # 튜플

template = '%(name)s는 음식을 좋아해. %(name)s가 요리하는 모습을 봐요'
after = template %{'name' : name}

# 딕셔너리를 사용하면 새로운 문제가 생긴다. 앞에서 설명한 두 번째 문제점인 살짝 바꿔야 하는경우 형식화 식이 더 길어진다

for i, (item, count) in enumerate(pantry):
    before = '#%d : %-10s = %.2f' %(
        i+1,
        item.title(),
        round(count))
    after = '#%(loop)d : %(item)-10s = %(count)d'%{
        'loop' : i+1,
        'item' : item.title(),
        'count' : round(count)
    }

#  4) 이러한 번잡함이 네 번째 문제점이다.
#  각 키를 최소 두번(한 번은 형식지정자, 한번은 딕셔너리 키) 반복하게 된다.



# 그래서 파이썬3 부터는 고급 문자열 형식화가 도입됐다. format을 통해 사용할 수 있다.
a = 1234.5678
formatted = format(a, ',.2f')
print(formatted)

key = 'my_var'
value = 1.234

formatted = '{} = {}'.format(key, value)
print(formatted)

# 위치 인덱스를 통해 첫 번째 문제점을 해결할 수 있다.
formatted = '{1} = {0}'.format(key, value)
print(formatted)

# 같은 위치 인덱스를 여러번 사용하여 세 번째 문제점도 해결된다.
name = '계홍'
formatted = '{0}는 음식을 좋아해. {0}가 요리하는 모습을 봐요'.format(name)
print(formatted)


# 아쉽지만 format 메서드도 두 번째 문제점과 네 번째 문제점은 해결하지 못한다.
# 또한 위치 지정자의 표현력 부족으로 인해 생기는 제약이 너무 커서 메서드의 가치를 떨어뜨린다.

# 웬만하면 str.format 메서드를 사용하지 말기를 권한다. 위 방법은 알아야 하지만, 
# 파이썬에서 새로 제공하는 f-문자열의 동작과 유용성을 이해하는데 도움을 주는 역사적인 유물로 간직하자.

key = 'my_var'
value = 1.234

formatted = f'{key} = {value}'
print(formatted)


formatted = f'{key:<10} = {value:.2f}'
print(formatted)

for i, (item, count) in enumerate(pantry):
    before = '#%d : %-10s = %d' %(
        i+1,
        item.title(),
        round(count))
    after = '#%(loop)d : %(item)-10s = %(count)d'%{
        'loop' : i+1,
        'item' : item.title(),
        'count' : round(count)
    }
    
    f_string = f'#{i+1} : {item.title():<10s} = {round(count)}'
    
    assert before == after == f_string