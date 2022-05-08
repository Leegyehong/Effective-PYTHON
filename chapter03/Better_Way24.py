# None과 독스트링을 사용해 동적인 디폴트 인자를 지정하라

# 키워드 인자의 값으로 정적으로 정해지지 않는 타입의 값을 써야할 때가 있다
# 예를 들어 로그 메시지와 시간을 출력한다

from time import sleep
from datetime import datetime

def log(message, when=datetime.now()):
    print(f'{when}: {message}')

log('Hi there!')
sleep(0.1)
log('Hello again!')

# 하지만 디폴트 인자는 이런 식으로 작동하지 않는다
# 함수가 정의되는 시점에 datetime.now 가 단 한 번만 호출되기 때문에 타임스탬프가 항상 같다

# 이런 경우 디폴트 값으로 None을 지정하고 실제 동작을 독스트링에 문서화 하는 것이다
def log(message, when=None):
    """Log a message with a timestamp.
    Args:
        message: Message to print.
        when: datetime of when the message occurred.
            Defaults to the present time.
    """
    if when is None:
        when = datetime.now()
    print(f'{when}: {message}')

log('Hi there!')
sleep(0.1)
log('Hello again!')

    
# 디폴트 인자 값으로 None을 사용하는 것은 인자가 가변적인 경우 특히 중요하다

import json

def decode(data, default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default
    
foo = decode('잘못된 데이터')
foo['stuff'] = 5
bar = decode('또 잘못된 데이터')
bar['meep'] = 1
print('Foo:', foo)
print('Bar:', bar)

# datetime.now 의 경우와 같다
# 디폴트 값이 단 한 번만 평가되기 때문에 default에 지정된 딕셔너리가 호출된 decode 호출에 모두 공유된다

def decode(data, default=None):
    """Load JSON data from a string.
    Args:
        data: JSON data to decode.
        default: Value to return if decoding fails.
            Defaults to an empty dictionary.
    """
    try:
        return json.loads(data)
    except ValueError:
        if default is None:
            default = {}
        return default
    
foo = decode('잘못된 데이터')
foo['stuff'] = 5
bar = decode('또 잘못된 데이터')
bar['meep'] = 1
print('Foo:', foo)
print('Bar:', bar)

# 이 접근 방법은 타입 애녀테이션을 사용해도 잘 작동한다

from datetime import datetime
from time import sleep
from typing import Optional

def log_typed(message: str,
              when: Optional[datetime]=None) -> None:
    """Log a message with a timestamp.
    Args:
        message: Message to print.
        when: datetime of when the message occurred.
            Defaults to the present time.
    """
    if when is None:
        when = datetime.now()
    print(f'{when}: {message}')

log_typed('Hi there!')
sleep(0.1)
log_typed('Hello again!')