# 객체를 제너릭하게 구성하려면 @classmethod를 통한 다형성을 활용하라

# 파이썬에서는 객체뿐 아니라 클래스도 다형성을 지원한다
# 왜 클래스가 다형성을 지원하면 좋을까

# 다형성을 사용하면 계층을 이루는 여러 클래스가 자신에게 맞는 유일한 메서드 버전을 구현할 수 있다

# 예를 들어 맵리듀스 구현을 하나 작성하고 있는데
# 입력 데이터를 표현할 수 있는 공통 클래스가 필요하다면?

# read 메서드가 들어있는 공통 클래스
class InputData:
    def read(self):
        raise NotImplementedError
# 디스크의 파일을 읽게 하도록 하위클래스를 만듬
class PathInputData(InputData):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        with open(self.path) as f:
            return f.read()
        

# 데이터를 소비하는 공통방법을 제공하는 맵리듀스 작업자(worker) 추상인터페이스를 정의
class Worker:
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError
# 다음은 원하는 맵 리듀스 기능(새줄 문자의 개수를 셈)을 구현하는 하위 클래스
class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result
        

# 하지만 각 부분을 어떻게 연결해야할까?
# 이해하기 쉬운 인터페이스와 추상화를 제공하는 멋진 클래스를 여럿 만들었지만,
# 객체를 생성해 활용해야만 이 모든게 쓸모 있게 된다

# 가장 간단한 접근 방법은 도우미 함수를 활용해 객체를 직접 만들고 연결하는 것이다
# 다음 코드는 디렉터리의 목록을 얻어서 그 안에 들어있는 파일마다 PathInputData 인스턴스를 만든다
import os

def generate_inputs(data_dir):
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name))

# generate_inputs를 통해 만든 InputData인스턴스 들을 사용하는 LineCountWorker 인스턴스를 만든다
def create_workers(input_list):
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers


from threading import Thread

# 이 worker 인스턴스의 map단계를 여러 스레드에 공급해서 실행할 수 있다
def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

    first, *rest = workers
    for worker in rest:
        first.reduce(worker)
    return first.result

# 마지막으로 지금까지 만든 모든 조각을 한 함수 안에 합쳐서 각 단계를 실행한다 
def mapreduce(data_dir):
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)
    return execute(workers)

import os
import random

def write_test_files(tmpdir):
    os.makedirs(tmpdir)
    for i in range(100):
        with open(os.path.join(tmpdir, str(i)), 'w') as f:
            f.write('\n' * random.randint(0, 100))

tmpdir = 'test_inputs'
write_test_files(tmpdir)

result = mapreduce(tmpdir)
print(f'총 {result} 줄이 있습니다.')

# 앞에서 정의한 mapreduce 함수의 가장 큰 문제점은 함수가 전혀 제너릭하지 않다는 것이다
# 다른 하위 클래스를 사용하고 싶다면 각 하위 클래스에 맞게 재작성 해야한다

# 다른 언어에서는 다형성을 활용해 이 문제를 해결할 수 있다

# 이 문제를 해결하는 가장 좋은 방법은 클래스 메서드(class method) 다형성을 사용하는 것이다

# 클래스 메서드라는 아이디어를 맵리듀스에  사용했던 클래스에 적용해보자
# InputData에 제너릭 @classmathod를 적용한 모습이다

class GenericInputData:
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError
# 다음 코드는 입력 파일이 들어있는 디렉터리를 찾기 config를 사용한다
class PathInputData(GenericInputData):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        with open(self.path) as f:
            return f.read()

    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))

# 비슷한 방식으로 GenericWorker 클래스 안에 create_workers 도우미 메서드를 추가할 수 있다
# 이 메서드는 GenericInputData의 하위 타입이여야하는 input_class를 파라미터로 받는다
# input_class는 필요한 입력을 생성해준다
# GenericWorker의 구체적인 하위 타입의 인스턴스를 만들 때는 cls()를 제너릭 생성자로 사용한다
class GenericWorker:
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers

# 위 코드에서 input_class.generate_inputs 호출이 클래스 다형성의 예다
# create_workers가 __init__을 직접 호출하지 않고 cls()를 호출함으로써 다른 방법으로 GenericWorker 객체를 만들 수 있다는 것도 알 수 있다

class LineCountWorker(GenericWorker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result

def mapreduce(worker_class, input_class, config):
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)

config = {'data_dir': tmpdir}
result = mapreduce(LineCountWorker, PathInputData, config)
print(f'총 {result} 줄이 있습니다.')
