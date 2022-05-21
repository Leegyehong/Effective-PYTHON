# 커스텀 컨테이너 타입은 collections.abc를 상속하라

# 모든 파이썬 클래스는 함수와 애트리뷰트를 함께 캡슐화하는 일종의 컨테이너이다

# 사용법이 간단한 클래스를 정의할 때는 파이썬 내장 리스트 타입의 하위 클래스를 만들고 싶은 것이 당연하다
class FrequencyList(list):
    def __init__(self, members):
        super().__init__(members)

    def frequency(self):
        counts = {}
        for item in self:
            counts[item] = counts.get(item, 0) + 1
 
        return counts
# list의 하위 클래스로 만듦으로써 리스트가 제공하는 모든 표준 함수를 사용할 수 있으며
# 이런 함수들의 의미가 낯익을 것이다
# 필요한 기능을 제공하는 메서드를 얼마든지 추가할 수 있다
foo = FrequencyList(['a', 'b', 'a', 'c', 'b', 'a', 'd'])
print('길이: ', len(foo))

foo.pop()
print('pop한 다음:', repr(foo))
print('빈도:', foo.frequency())

# 이제 리스트처럼 느껴지면서 인덱싱이 가능한 객체를 제공하고싶다
# 리스트의 하위클래스로 만들고 싶지는 않다고 가정해보자

# 다음 이진 트리 클래스를 시퀀스의 의미 구조를 사용해 다루는 클래스를 만들어 보자
class BinaryNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

# 어떻게 이 클래스가 시퀀스 타입처럼 작동하게 할까
# 파이썬에서 다음과 같이 시퀀스에 접근하는 코드는
bar = [1, 2, 3]
bar[0]
# bar.__getitem__(0) 으로 해석된다

# BinaryNode 클래스가 시퀀스 처럼 작동하게 하려면
# 트리 노드를 깊이 우선 순회하는 커스텀 __getitem__ 메서드 구현을 제공하면 된다

class IndexableNode(BinaryNode):
    def _traverse(self):
        if self.left is not None:
            yield from self.left._traverse()
        yield self
        if self.right is not None:
            yield from self.right._traverse()

    def __getitem__(self, index):
        for i, item in enumerate(self._traverse()):
            if i == index:
                return item.value
        raise IndexError(f'인덱스 범위 초과: {index}')


# left나 right 애트리뷰트를 사용해 순회할 수 있지만
# 추가로 리스트처럼 접근할 수도 있다

tree = IndexableNode(
    10,
    left=IndexableNode(
        5,
        left=IndexableNode(2),
        right=IndexableNode(
            6,
            right=IndexableNode(7))),
    right=IndexableNode(
        15,
        left=IndexableNode(11)))

print('LRR:', tree.left.right.right.value)
print('인덱스 0:', tree[0])
print('인덱스 1:', tree[1])
print('11이 트리 안에 있나?', 11 in tree)
print('17이 트리 안에 있나?', 17 in tree)
print('트리:', list(tree))

# 문제는 __getitem__ 을 작성하는 것만으로는
# 리스트 인스턴스에서 기대할 수 있는 모든 시퀀스 의미구조를 제공할수 없다는데 있다

class SequenceNode(IndexableNode):
    def __len__(self):
        for count, _ in enumerate(self._traverse(), 1):
            pass
        return count

tree = SequenceNode(
    10,
    left=SequenceNode(
        5,
        left=SequenceNode(2),
        right=SequenceNode(
            6,
            right=SequenceNode(7))),
    right=SequenceNode(
        15,
        left=SequenceNode(11))
)

print('트리 길이:', len(tree))
len(tree)
# __len__ 이라는 이름의 특별 메서드를 구현해야 제대로 작동한다


# 어떤 클래스가 올바른 시퀀스가 되려면 두 메서드(__getitem__, __len__)을 구현하는 것만으로는 충분하지않다
# count나 index 메서드도 들어있지 않다
# 자신만의 컨테이너 타입을 직접 정의하는 것은 생각보다 훨씬 어렵다


# 파이썬을 사용할 때 흔히 발생하는 이런 어려움을 덜어주기 위해
# 내장 collections.abs 모듈 안에는 컨테이너 타입에 저장해야 하는 전형적인 메서드를 모두 제공하는
# 추상 기반 클래스 정의가 여러가지 들어있다
# 필요한 메서드 구현을 잊어버리면 collections.abs 모듈이 실수한 부분을 알려준다

from collections.abc import Sequence

class BadType(Sequence):
    pass

# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#foo = BadType()

# SequenceNode에서 한 것처럼 collections.abc에서 가져온 추상 기반 클래스가 요구하는
# 모든 메서드를 구현하면 index나 count와 같은 추가 메서드 구현을 거저 얻을 수 있다
class BetterNode(SequenceNode, Sequence):
    pass

tree = BetterNode(
    10,
    left=BetterNode(
        5,
        left=BetterNode(2),
        right=BetterNode(
            6,
            right=BetterNode(7))),
    right=BetterNode(
        15,
        left=BetterNode(11))
)

print('7의 인덱스:', tree.index(7))
print('10의 개수:', tree.count(10))

# Set이나 MutableMapping 과 같이 파이썬에서 관례에 맞춰 구현해야 하는
# 특별 메서드가 훨씬 많은 더 복잡한 컨테이너 타입을 구현할 때는 이점이 더 커진다