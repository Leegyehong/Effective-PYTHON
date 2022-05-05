# 내부 상태에서 원소가 없는 경우를 처리할 때는 setdefault보다 defaultdict를 사용하라

visits = {
    '미국': {'뉴욕', '로스엔젤레스'},
    '일본': {'하코네'},
}

# 딕셔너리 안에 나라 이름이 들어 있는지 여부와 관계없이 각 집합에 새 도시를 추가할 때 setdefault를 사용할 수 있다.
visits.setdefault('프랑스', set()).add('칸')

if (japan := visits.get('일본')) is None:       #
    visits['일본'] = japan = set()
japan.add('교토')

print(visits)

# 직접 딕셔너리 생성을 제어할 수 있다면 어떨까?

class Visits:
    def __init__(self):
        self.data = {}

    def add(self, country, city):
        city_set = self.data.setdefault(country, set())
        city_set.add(city)
        
visits = Visits()
visits.add('러시아', '예카테린부르크')
visits.add('탄자니아', '잔지바르')
print(visits.data)

# 하지만 Visits.add는 이상적이지 않다
# setdefault라는 이름은 여전히 헷갈리기 때문에 코드를 처음 읽는 사람은 바로 이해하기 어렵다

# 다행히 collections 모듈에 defaultdict 클래스는 키가 없을 때 자동으로 디폴트 값을 저장해서 간단히 처리할 수 있게 해준다

from collections import defaultdict

class Visits:
    def __init__(self):
        self.data = defaultdict(set)

    def add(self, country, city):
        self.data[country].add(city)

visits = Visits()
visits.add('영국', '바스')
visits.add('영국', '런던')
print(visits.data)