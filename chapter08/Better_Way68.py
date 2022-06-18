# copyreg를 사용해 pickle을 더 신뢰성 있게 만들라

# pickle 내장 모듈을 사용하면 파이썬 객체를 바이트 스트림으로 직렬화 하거나
# 바이트 스트림을 파이썬 객체로 역직렬화할 수 있다

# 바이트 스트림은 서로 신뢰할 수 없는 당사자 사이의 통신에 사용하면 안된다
# pickle의 목적은 제어하는 프로그램들이 이진 채널을 통해 서로 파이썬 객체를 넘기는 데 있다.
class GameState:
    def __init__(self):
        self.level = 0
        self.lives = 4

state = GameState()
state.level += 1     # 플레이어가 레벨을 깼다
state.lives -= 1     # 플레이어가 재시도해야 한다

print(state.__dict__)

import pickle

state_path = 'game_state.bin'
with open(state_path, 'wb') as f:
    pickle.dump(state, f)

with open(state_path, 'rb') as f:
    state_after = pickle.load(f)

print(state_after.__dict__)

#
class GameState:
    def __init__(self):
        self.level = 0
        self.lives = 4
        self.points = 0 # 새로운 필드

state = GameState()
serialized = pickle.dumps(state)
state_after = pickle.loads(serialized)
print(state_after.__dict__)

with open(state_path, 'rb') as f:
    state_after = pickle.load(f)

print(state_after.__dict__)

assert isinstance(state_after, GameState)

# 위 방식 처럼 pickle을 사용하는 방식이 아주 간단한 수준을 벗어나는 순간, pickle 모듈의 동작은 예상할 수 없는 방식으로 망가지기 시작한다.

# 디폴트 애트리뷰트 값
# 가장 간단한 경우, 디폴트 인자가 있는 생성자를 사용하면 언피클 했을 때도 항상 필요한 모든 애트리뷰트를 포함시킬 수 있다.
class GameState:
    def __init__(self, level=0, lives=4, points=0):
        self.level = level
        self.lives = lives
        self.points = points

def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    return unpickle_game_state, (kwargs,)

def unpickle_game_state(kwargs):
    return GameState(**kwargs)

import copyreg

copyreg.pickle(GameState, pickle_game_state)

state = GameState()
state.points += 1000
serialized = pickle.dumps(state)
state_after = pickle.loads(serialized)
print(state_after.__dict__)

class GameState:
    def __init__(self, level=0, lives=4, points=0, magic=5):
        self.level = level
        self.lives = lives
        self.points = points
        self.magic = magic   # 추가한 필드

print('이전:', state.__dict__)
state_after = pickle.loads(serialized)
print('이후:', state_after.__dict__)

# 클래스 버전 지정
# 파이썬 객체의 필드를 제거해 예전 버전 객체와의 하위 호환성이 없어지는 경우도 발생한다
class GameState:
    def __init__(self, level=0, points=0, magic=5):
        self.level = level
        self.points = points
        self.magic = magic

# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#pickle.loads(serialized)

def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    kwargs['version'] = 2
    return unpickle_game_state, (kwargs,)

def unpickle_game_state(kwargs):
    version = kwargs.pop('version', 1)
    if version == 1:
        del kwargs['lives']
    return GameState(**kwargs)

copyreg.pickle(GameState, pickle_game_state)
print('이전:', state.__dict__)
state_after = pickle.loads(serialized)
print('이후:', state_after.__dict__)

# 안정적인 임포트 경로
# pickle을 할 때 마주칠수 있는 다른 문제점으로
# 클래스 이름이 바뀌어 코드가 깨지는 경우를 들 수 있다
class BetterGameState:
    def __init__(self, level=0, points=0, magic=5):
        self.level = level
        self.points = points
        self.magic = magic

pickle.loads(serialized)

print(serialized)

copyreg.pickle(BetterGameState, pickle_game_state)

state = BetterGameState()
serialized = pickle.dumps(state)
print(serialized)

