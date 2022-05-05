# 딕셔너리 삽입 순서에 의존할 때는 조심하라

# Python 3.5 이전
baby_names = {
    'cat': 'kitten',
    'dog': 'puppy' 
}
print(baby_names) # { 'dog': 'puppy', 'cat': 'kitten'}

# 딕셔너리를 만들 때 cat, dog 순으로 삽입했지만 출력하면 역으로 출력됨
# 지금은 삽입 순서를 유지한다.

# 하지만 딕셔너리를 처리할 때는 삽입 순서 관련 동작이 항상 성립한다고 가정해서는 안된다.
# 파이썬에서는 프로그래머가 list, dict등의 표준 프로토콜을 흉내 내는 커스텀 컨테이너 타입을 쉽게 정의할 수 있다.


votes = {
    'otter': 1281,
    'polar bear': 587,
    'fox': 863,
}

def populate_ranks(votes, ranks):
    names = list(votes.keys())
    names.sort(key=votes.get, reverse=True)
    for i, name in enumerate(names, 1):
        ranks[name] = i

def get_winner(ranks):
    return next(iter(ranks))

ranks = {}
populate_ranks(votes, ranks)
print(ranks)
winner = get_winner(ranks)
print(winner)

# 여기서 등수가 아닌 알파벳순으로 표시를 해야한다면?
# collections.abc 모듈을 사용하여 딕서너리와 비슷하지만 내용을 알파벳 순서대로 이터레이션 해주는 클래스를 새로 정의할 수 있다.

# SortedDict는 표준 딕셔너리의 프로토콜을 지키므로, 앞에서 정의한 함수를 호출하면서 SortedDict 인스턴스를 표준 dict 위치에 사용해도 아무런 오류가 발생하지않는다.
# 하지만 결과는 요구 사항에 맞지 않는다.

from collections.abc import MutableMapping

class SortedDict(MutableMapping):
    def __init__(self):
        self.data = {}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        keys = list(self.data.keys())
        keys.sort()
        for key in keys:
            yield key

    def __len__(self):
        return len(self.data)

sorted_ranks = SortedDict()
populate_ranks(votes, sorted_ranks)
print(sorted_ranks.data) # {'otter': 1, 'fox': 2, 'polar bear': 3}
winner = get_winner(sorted_ranks)
print(winner) # fox


# 여기서 문제는 get)winner의 구현이 populate_ranks의 삽입 순서에 맞게 딕셔너리를 이터레이션한다고 가정했다는데 있다.
# dict 대신 SortedDict를 사용하므로 이 가정은 더이상 성립하지 않는다.

# 이러한 문제를 해결하는 세 가지 방법이 있다.

# 첫번째 -> ranks 딕셔너리가 어떤 특정 순서로 가정하지 않고 get_winner 함수를 구현하는 것
def get_winner(ranks):
    for name, rank in ranks.items():
        if rank == 1:
            return name

winner = get_winner(sorted_ranks)
print(winner)


# 두번째 -> 함수 맨 앞에 ranks의 타입이 우리가 원하는 타입인지 검사하는 코드를 추가한다.
# 이 해법은 보수적인 접근 방법 보다 실행 성능이 좋을 것이다.


def get_winner(ranks):
    if not isinstance(ranks, dict):
        raise TypeError('dict 인스턴스가 필요합니다.')
    return next(iter(ranks))

get_winner(sorted_ranks)


# 세번째 -> 타입 이터레이션을 사용해서 get_winner에 전달되는 값이 딕셔너리와 비슷한 동작을 하는 MutableMapping 인스턴스가 아니라 dict 인스턴스가 되도록 강제하는 것

from typing import Dict, MutableMapping

def populate_ranks(votes: Dict[str, int],
                   ranks: Dict[str, int]) -> None:
    names = list(votes.keys())
    names.sort(key=votes.get, reverse=True)
    for i, name in enumerate(names, 1):
        ranks[name] = i

def get_winner(ranks: Dict[str, int]) -> str:
    return next(iter(ranks))

from typing import Iterator, MutableMapping

class SortedDict(MutableMapping[str, int]):
    def __init__(self) -> None:
        self.data: Dict[str, int] = {}

    def __getitem__(self, key: str) -> int:
        return self.data[key]

    def __setitem__(self, key: str, value: int) -> None:
        self.data[key] = value

    def __delitem__(self, key: str) -> None:
        del self.data[key]

    def __iter__(self) -> Iterator[str]:
        keys = list(self.data.keys())
        keys.sort()
        for key in keys:
            yield key

    def __len__(self) -> int:
        return len(self.data)

votes = {
    'otter': 1281,
    'polar bear': 587,
    'fox': 863,
}

sorted_ranks = SortedDict()
populate_ranks(votes, sorted_ranks)
print(sorted_ranks.data)
winner = get_winner(sorted_ranks)
print(winner)