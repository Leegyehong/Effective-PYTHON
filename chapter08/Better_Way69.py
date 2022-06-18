# 정확도가 매우 중요한 경우에는 decimal을 사용하라


rate = 1.45
seconds = 3*60 + 42
cost = rate * seconds / 60
print(cost)

print(round(cost, 2))

from decimal import Decimal

rate = Decimal('1.45')
seconds = Decimal(3*60 + 42)
cost = rate * seconds / Decimal(60)
print(cost)

# Decimal 인스턴스에 값을 지정하는 방법은 두 가지가 있다
# 첫째, 숫자가 들어있는 str을 Decimal 생성자에 전달하는법
# 둘째, int나 float 인스턴스를 생성자에 전달하는법
print(Decimal('1.45'))
print(Decimal(1.45))

print('456')
print(456)

rate = Decimal('0.05')
seconds = Decimal('5')
small_cost = rate * seconds / Decimal(60)
print(small_cost)

print(round(small_cost, 2))

from decimal import ROUND_UP
rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
print(f'반올림 전: {cost} 반올림 후: {rounded}')

rounded = small_cost.quantize(Decimal('0.01'),
                              rounding=ROUND_UP)
print(f'반올림 전: {small_cost} 반올림 후: {rounded}')

