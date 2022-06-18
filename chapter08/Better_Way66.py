# 재사용 가능한 try/finally 동작을 원한다면 contextlib과 with 문을 사용하라

# with문은 코드가 특별한 컨텍스트 안에서 실행되는 경우를 표현한다
# ex) 뮤텍스를 with문 안에서 사용하면 락을 소유했을 때만 코드가 실행된다는 것을 의미
import logging

def my_function():
    logging.debug('디버깅 데이터')
    logging.error('이 부분은 오류 로그')
    logging.debug('추가 디버깅 데이터')
# 프로그램의 디폴트 로그 수준은 WARNING이다
# 위 함수를 실행하면 error 메시지만 출력됨

# 컨텍스트 매니저를 정의하면 이 함수의 로그 수준을 일시적으로 높일 수 있다
from contextlib import contextmanager

@contextmanager
def debug_logging(level):
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield
    finally:
        logger.setLevel(old_level)

with debug_logging(logging.DEBUG):
    print('* 내부:')
    my_function()

print('* 외부:')
my_function()

# with와 대상 변수 함께 사용하기
with open('my_output.txt', 'w') as handle:
    handle.write('데이터입니다!')

# as 대상 변수에게 값을 제동하도록 하기 위해 필요한 일은 컨텍스트 매니저 안에서 yield 값을 넘기는 것뿐이다. 
@contextmanager
def log_level(level, name):
    logger = logging.getLogger(name)
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield logger
    finally:
        logger.setLevel(old_level)

# 맨 처음 log_level을 사용해 로그를 출력하는 경우
# 메시지가 표시되지 않는 경우가 있음
# 이럴때 메인 스레드에서 우선 아래 문장을 실행하면 정상작동함
logging.basicConfig()

with log_level(logging.DEBUG, 'my-log') as logger:
    logger.debug(f'대상: {logger.name}!')
    logging.debug('이 메시지는 출력되지 않습니다')

logger = logging.getLogger('my-log')
logger.debug('디버그 메시지는 출력되지 않습니다')
logger.error('오류 메시지는 출력됩니다')

with log_level(logging.DEBUG, 'other-log') as logger:
    logger.debug(f'대상: {logger.name}!')
    logging.debug('이 메시지는 출력되지 않습니다')

