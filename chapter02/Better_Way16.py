# in을 사용하고 딕셔너리 키가 없을 때 KeyError를 처리하기보다는 get을 사용하라


# 딕셔너리와 상호작용하는 세 가지 기본 연산은 키나 키에 연관된 값에 접근하고, 대입하고, 삭제하는 것
# 딕셔너리는 동적이라 어떤 키에 접근하거나 키를 삭제할 때 그 키가 딕셔너리 없을 수도 있음
counters = {
    '품퍼니켈': 2,
    '사워도우': 1,
}


key = '밀'

if key in counters:
    count = counters[key]
else:
    count = 0

counters[key] = count + 1

print(counters)

# 키가 존재하면 그 값을 가져오고 존재하지 않으면 디폴트 값을 반환하는 흐름이 꽤 자주 일어난다.
# 그래서 dict 내장 타입에는 이런 작업을 수행하는 get 메서드가 들어있다
count = counters.get(key, 0)
counters[key] = count + 1

print(counters)


#  딕셔너리에 저장된 값이 리스트처럼 더 복잡한 값이라면?

votes = {
    '바게트': ['철수', '순이'],
    '치아비타': ['하니', '유리'],
}

key = '브리오슈'
who = '단이'

if key in votes:
    names = votes[key]
else:
    votes[key] = names = []

names.append(who)
print(votes)

# in을 사용하면 키가 있는 경우에는 키를 두 번 읽어야하고, 키가 없는 경우에는 값을 한 번 대입해야한다
# 값이 리스트인 경우 KeyError 예외가 발생한다는 사실에 의존하면
# 키가 있을 때는 키를 한 번만 읽고, 없을 때는 한 번 읽고 한번 대입하면 된다

key = 'rye'
who = 'Felix'

try:
    names = votes[key]
except KeyError:
    votes[key] = names = []

names.append(who)

print(votes)


# 마찬가지로 키가 있을 때는 리스트 값을 가져오기 위해 get메서드를 사용하고 없을 때는 대입을 사용할 수 있다.

key = 'wheat'
who = 'Gertrude'

names = votes.get(key)
if names is None:
    votes[key] = names = []

names.append(who)

print(votes)

# 대입식(BVetter Way 10) 을 사용하면 더 짧게 쓸 수 있다.
key = 'brioche'
who = 'Hugh'

if (names := votes.get(key)) is None:
    votes[key] = names = []

names.append(who)

print(votes)

# setdefault 방식은 가독성이 별로다
# 메서드 이름조차 동작을 직접적으로 드러내지 못한다. (값을 얻는 메서드인데 이름이 set임)

key = 'cornbread'
who = 'Kirk'

names = votes.setdefault(key, [])
names.append(who)

print(votes)
