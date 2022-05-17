# 기능을 합성할 때는 믹스인 클래스를 사용하라

# 파이썬은 다중 상속을 처리할 수 있게 하지만, 다중 상속은 피하는 편이 좋다
# 다중 상속이 제공하는 편의와 캡술화가 필요하지만, 다중 상속으로 인해 발생할 수 있는 문제를 피하고 싶다면
# 믹스인(mix-in)을 고려해봐라

# 믹스인은 자식 클래스가 사용할 메서드 몇 개만 정의하는 클래스이다
# 파이썬에서는 타입과 상관없이 객체의 현재 상태를 쉽게 들여다볼 수 있으므로 믹스인 작성이 쉽다
# 제너릭인 기능을 믹스인 안에 한 번만 작성해두면 다른 여러 클래스에 적용할 수 있다
# 믹스인을 합성하거나 계층화해서 반복적인 코드를 최소화하고 재사용성을 최대화할 수 있다

# 예를 들어 메모리 내에 들어 있는 파이썬 객체를 직렬화에 사용할 수 있도록 딕셔너리로 바꾸고 싶을 때
# 제너릭하게 여러 클래스에 활용하면 어떨까

class ToDictMixin:
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output
    # _traverse_dict 메서드를 hasattr을 통한 동적인 애트리뷰트 접근과 isinstance를 사용한 타입 검사, __dict__를 통한 인스턴스 딕서너리 접근을 활용해 구현한다
    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value

# 이 믹스인을 사용해 이진트리를 딕셔너리 표현으로 변경하는 예제이다
class BinaryTree(ToDictMixin):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

tree = BinaryTree(10,
                  left=BinaryTree(7, right=BinaryTree(9)),
                  right=BinaryTree(13, left=BinaryTree(11)))
print(tree.to_dict())


# 믹스인의 가장 큰 장점은 제너릭 기능을 쉽게 연결할 수 있고 필요할 때 기존 기능을 다른 기능으로 오버라이드해 변경할 수 있다는 것이다

# 예를 들어
# 다음은 BinaryTree에 대한 참조를 저장하는 하위 클래스를 정의한다


class BinaryTreeWithParent(BinaryTree):
    # 이런 순환 참조가 있으면 원래의 TodictMixin.to_dict의 구현은 무한루프를 돈다
    def __init__(self, value, left=None,
                 right=None, parent=None):
        super().__init__(value, left=left, right=right)
        self.parent = parent
    # 방법은 _traverse 메서드를 오버라이드해 문제가 되는 값만 처리하게 만들어서 무한 루프를 돌지 못하게 하는 것이다
    def _traverse(self, key, value):
        if (isinstance(value, BinaryTreeWithParent) and
                key == 'parent'):
            return value.value  # 순환 참조 방지
        else:
            return super()._traverse(key, value)

root = BinaryTreeWithParent(10)
root.left = BinaryTreeWithParent(7, parent=root)
root.left.right = BinaryTreeWithParent(9, parent=root.left)
print(root.to_dict())

class NamedSubTree(ToDictMixin):
    def __init__(self, name, tree_with_parent):
        self.name = name
        self.tree_with_parent = tree_with_parent

my_tree = NamedSubTree('foobar', root.left.right)
print(my_tree.to_dict()) # 무한 루프없음

# 믹스인을 서로 합성할 수도 있다
# 임의의 클래스를 JSON으로 직렬화하는 제너릭 믹스인을 만들고 싶다면?
# 모든 클래스가 to_dict 메서드를 제공한다면 다음과 같은 제너릭 믹스인을 만들 수 있다

import json

class JsonMixin:
    @classmethod
    def from_json(cls, data):
        kwargs = json.loads(data)
        return cls(**kwargs)

    def to_json(self):
        return json.dumps(self.to_dict())

class DatacenterRack(ToDictMixin, JsonMixin):
    def __init__(self, switch=None, machines=None):
        self.switch = Switch(**switch)
        self.machines = [
            Machine(**kwargs) for kwargs in machines]

class Switch(ToDictMixin, JsonMixin):
    def __init__(self, ports=None, speed=None):
        self.ports = ports
        self.speed = speed

class Machine(ToDictMixin, JsonMixin):
    def __init__(self, cores=None, ram=None, disk=None):
        self.cores = cores
        self.ram = ram
        self.disk = disk

serialized = """{
    "switch": {"ports": 5, "speed": 1e9},
    "machines": [
        {"cores": 8, "ram": 32e9, "disk": 5e12},
        {"cores": 4, "ram": 16e9, "disk": 1e12},
        {"cores": 2, "ram": 4e9, "disk": 500e9}
    ]
}"""

deserialized = DatacenterRack.from_json(serialized)
roundtrip = deserialized.to_json()
assert json.loads(serialized) == json.loads(roundtrip)

