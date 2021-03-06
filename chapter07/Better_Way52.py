# 자식 프로세스를 관리하기 위해 subprocess를 사용하라

# 파이썬이 하위 프로세스를 실행하는 방법은 많다
# 자식프로세스를 관리할 때는 subprocess 내장 모듈을 사용하는 것이 가장 좋다

import subprocess

# 파이썬 3.6이나 그 이전 버전에서는 제대로 작동하지 않는다.(capture_output을 사용할 수 없음)
# 윈도우에서는 echo가 없는 경우 제대로 작동하지 않을 수 있다.
result = subprocess.run(['echo', '자식프로세스가 보내는 인사!'], capture_output=True, encoding='utf-8')

result.check_returncode() # 예외가 발생하지 않으면 문제 없이 잘 종료한 것이다
print(result.stdout) #

# 자식 프로세스는 부모 프로세스인 파이썬 인터프리터와 독립적으로 실행됨
# run 함수 대신 Popen 클래스를 사용해 하위 프로세스를 만들면, 파이썬이 다른 일을 하면서 주기적으로 자식 프로세스의 상태를 검사할 수 있다
import subprocess

# 윈도우에서는 sleep이 없는 경우 제대로 작동하지 않을 수 있다.
proc = subprocess.Popen(['sleep', '1'])
while proc.poll() is None:
    print('작업중...')
    # 시간이 걸리는 작업을 여기서 수행한다

print('종료 상태', proc.poll())

#  자식 프로세스와 부모를 분리하면 부모 프로세스가 원하는 개수만큼 많은 자식 프로세스를 병렬로 실행할 수 있다
import subprocess
import time

# 윈도우에서는 sleep이 없는 경우 제대로 작동하지 않을 수 있다.
start = time.time()
sleep_procs = []
for _ in range(10):
    proc = subprocess.Popen(['sleep', '1'])
    sleep_procs.append(proc)

for proc in sleep_procs:
    proc.communicate()

end = time.time()
delta = end - start
print(f'{delta:.3} 초만에 끝남')
# 순차적으로 실행됐다면 1초 이하의 값이 아닌 10초 이상 이었을 것이다

# 파이썬 프로그램의 데이터를 파이프를 사용해 하위 프로세스로 보내거나, 하위프로세스의 출력을 받을 수 있다
# 이를 통해 다른 프로그램을 사용해서 병렬적으로 작업을 수행할 수 있다
import subprocess
import os

# 시스템에 openssl을 설치하지 않은 경우에는 작동하지 않을 수 있다.
def run_encrypt(data):
    env = os.environ.copy()
    env['password'] = 'zf7ShyBhZOraQDdE/FiZpm/m/8f9X+M1'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
    proc.stdin.write(data)
    proc.stdin.flush() # 자식이 입력을 받도록 보장한다
    return proc

procs = []
for _ in range(3):
    data = os.urandom(10)
    proc = run_encrypt(data)
    procs.append(proc)

for proc in procs:
    out, _ = proc.communicate()
    print(out[-10:])


# 유닉스 파이프라인처럼 한 자식 프로세스의 출력을 다음 프로세스의 입력으로 계속 연결시켜서
# 여러 병렬 프로세스를 연쇄적으로 연결할 수도 있다
import subprocess
import os

# 시스템에 openssl을 설치하지 않은 경우에는 작동하지 않을 수 있다.
def run_encrypt(data):
    env = os.environ.copy()
    env['password'] = 'zf7ShyBhZOraQDdE/FiZpm/m/8f9X+M1'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
    proc.stdin.write(data)
    proc.stdin.flush() # 자식이 입력을 받도록 보장한다
    return proc

def run_hash(input_stdin):
    return subprocess.Popen(
        ['openssl', 'dgst', '-whirlpool', '-binary'],
        stdin=input_stdin,
        stdout=subprocess.PIPE)

encrypt_procs = []
hash_procs = []

for _ in range(3):
    data = os.urandom(100)

    encrypt_proc = run_encrypt(data)
    encrypt_procs.append(encrypt_proc)

    hash_proc = run_hash(encrypt_proc.stdout)
    hash_procs.append(hash_proc)

    # 자식이 입력 스트림에 들어오는 데이터를 소비하고 communicate() 메서드가
    # 불필요하게 자식으로부터 오는 입력을 훔쳐가지 못하게 만든다.
    # 또 다운스트림 프로세스가 죽으면 SIGPIPE를 업스트림 프로세스에 전달한다.
    encrypt_proc.stdout.close()
    encrypt_proc.stdout = None

for proc in encrypt_procs:
    proc.communicate()
    assert proc.returncode == 0

for proc in hash_procs:
    out, _ = proc.communicate()
    print(out[-10:])

assert proc.returncode == 0



# 자식 프로세스가 끝나지 않는 경우
# 블록이 되는 경우가 우려된다면 timeout 파라미터를 communicate메서드에 전달할 수 있다
import subprocess

# 윈도우에서는 sleep이 없으면 제대로 작동하지 않을 수 있다.
proc = subprocess.Popen(['sleep', '10'])
try:
    proc.communicate(timeout=0.1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()

print('종료 상태', proc.poll())
1