# send로 제너레이터에 데이터를 주입하지 말라

# 예를 들어 소프트웨어 라디오를 사용해 신호를 내보낸다고 하자


import math

def wave(amplitude, steps):
    step_size = 2 * math.pi / steps   # 2라디안/단계 수
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        output = amplitude * fraction
        yield output

#
def transmit(output):
    if output is None:
        print(f'출력: None')
    else:
        print(f'출력: {output:>5.1f}')

def run(it):
    for output in it:
        transmit(output)

run(wave(3.0, 8))

# 기본 파형을 생성하는 한 이 코드는 잘 작동한다
# 하지만 별도의 입력을 사용해 진폭을 지속적으로 변경해야 한다면 이 코드는 쓸모가 없다
# 파이썬 제너레이터는 send 메서드를 지원하다
# 이 메서드는 yield 식을 양방향 채널로 격상시켜준다

def my_generator():
    received = yield 1
    print(f'받은 값 = {received}')

it = iter(my_generator())
output = next(it)  # 첫 번째 제너레이터 출력을 얻는다
print(f'출력값 = {output}')

try:
    next(it)  # 종료될 때까지 제너레이터를 실행한다
except StopIteration:
    pass

it = iter(my_generator())
output = it.send(None)     # 첫 번째 제너레이터 출력을 얻는다
print(f'출력값 = {output}')

try:
    it.send('안녕!')    # 값을 제너레이터에 넣는다
except StopIteration:
    pass

# 이것을 활용해 입력 시그널을 바탕으로 변조할 수 있다


import math
def wave_modulating(steps):
    step_size = 2 * math.pi / steps
    amplitude = yield                # 초기 진폭을 받는다
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        output = amplitude * fraction
        amplitude = yield output     # 다음 진폭을 받는다
        
def run_modulating(it):
    amplitudes = [
        None, 7, 7, 7, 2, 2, 2, 2, 10, 10, 10, 10, 10]
    for amplitude in amplitudes:
        output = it.send(amplitude)
        transmit(output)

run_modulating(wave_modulating(12))

# yield from 식이 단순한 경우를 잘 처리하므로 합성해보자

def complex_wave_modulating():
    yield from wave_modulating(3)
    yield from wave_modulating(4)
    yield from wave_modulating(5)

run_modulating(complex_wave_modulating())

# 중간중간 None이 보인다
# 내포된 제너레이터에 대한 yield from 식이 끝날 때마다 다음 yield from 식이 실행된다
# 각각의 내포된 제너레이터는 send 메서드 호출로부터 값을 받기 위해 아무런 값도 만들어내지 않는 단순한 yield식으로 시작한다

def wave_cascading(amplitude_it, steps):
    step_size = 2 * math.pi / steps
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        amplitude = next(amplitude_it) # 다음 입력 받기
        output = amplitude * fraction
        yield output

#
def complex_wave_cascading(amplitude_it):
    yield from wave_cascading(amplitude_it, 3)
    yield from wave_cascading(amplitude_it, 4)
    yield from wave_cascading(amplitude_it, 5)

#
def run_cascading():
    amplitudes = [7, 7, 7, 2, 2, 2, 2, 10, 10, 10, 10, 10]
    it = complex_wave_cascading(iter(amplitudes))
    for amplitude in amplitudes:
        output = next(it)
        transmit(output)

run_cascading()