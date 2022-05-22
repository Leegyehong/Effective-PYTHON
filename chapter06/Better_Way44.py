# 세터와 게터 메서드 대신 평범한 애트리뷰트를 사용하라


# 다른 언어를 사용하다 파이썬을 접한 프로그래머들은 클래스에서 게터나 세터를 정의하곤한다
class OldResistor:
    def __init__(self, ohms):
        self._ohms = ohms

    def get_ohms(self):
        return self._ohms

    def set_ohms(self, ohms):
        self._ohms = ohms
# 세터와 게터를 사용하기는 쉽지만, 이런 코드는 파이썬답지 못하다

r0 = OldResistor(50e3)
print('이전:', r0.get_ohms())
r0.set_ohms(10e3)
print('이후:', r0.get_ohms())
# 특히 필드 값을 증가시키는 연상 등의 경우에는 이런 메서드를 사용하면 지저분해진다
r0.set_ohms(r0.get_ohms() - 4e3)
assert r0.get_ohms() == 6e3
# 하지만 이런 유틸리티 메서드를 사용하면 클래스 인터페이스를 설계할 때
# 도움이 되기도 한다 ( 캡슐화하고, 필드 사용을 검증, 경계를 설정하기 쉬움)

# 파이썬에서는 명시적인 세터나 게터 메서드를 구현할 필요가 전혀 없다
# 대신 다음 코드와 같이 항상 단순한 공개 애트리뷰트로부터 구현을 시작하자

class Resistor:
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0

r1 = Resistor(50e3)
r1.ohms = 10e3

r1.ohms += 5e3
# 이렇게 사용하면 필드를 제자리에서 증가시키는 등의 연산이 더 자연스럽고 명확해진다

# 나중에 애트리뷰트가 설정될 때 특별한 기능을 수행해야 한다면
# 애트리뷰트를 @property 데코레이터와 대응한 setter 애트리뷰트로 옮겨갈 수 있다

# Registor에서 valtage 프로퍼티에 값을 대입하면 current값이 바뀐다
# 코드가 제대로 작동하려면 세터와 게터의 이름이 우리가 의도한 프로퍼티 이름과 일치해야한다
class VoltageResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms

# voltage 프로퍼티에 대입하면 voltage 세터 메서드가 호출되고
# 이 메서드는 current 애트리뷰트를 변경된 값에 맞춰 갱신한다
r2 = VoltageResistance(1e3)
print(f'이전: {r2.current:.2f} 암페어')
r2.voltage = 10
print(f'이후: {r2.current:.2f} 암페어')

# 모든 값이 0 보다 큰지 확인하는 클래스
class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError(f'저항 > 0이어야 합니다. 실제 값: {ohms}')
        self._ohms = ohms

r3 = BoundedResistance(1e3)
# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#r3.ohms = 0

# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#BoundedResistance(-5)

# @property를 사용해 부모 클래스에서 정의된 애트리뷰트를 불변으로 만들 수도 있다
class FixedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError("Ohms는 불변객체입니다")
        self._ohms = ohms

r4 = FixedResistance(1e3)
# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#r4.ohms = 2e3

# @property를 사용해 세터와 게터를 구현할 때는 
# 게터나 세터 구현이 예기치 않은 동작을 수행하지 않도록 만들어야한다
# 예를 들어 게터 프로퍼티 메서드 안에서 다른 애트리뷰트를 설정하면 안 된다.
class MysteriousResistor(Resistor):
    @property
    def ohms(self):
        self.voltage = self._ohms * self.current
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        self._ohms = ohms

r7 = MysteriousResistor(10)
r7.current = 0.01
print(f'이전: {r7.voltage:.2f}')
r7.ohms
print(f'이후: {r7.voltage:.2f}')
