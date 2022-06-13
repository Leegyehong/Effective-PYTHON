# try/except/else/finally의 각 블록을 잘 활용하라

# 파이썬에서 예외를 처리하는 과정에서는 특정 동작을 수행하고 싶은 네 가지 경우가 있다
# try, except, else, finally 
# 각각은 서로 다른 목적에 쓰이며, 다양하게 조합하면 유용하다

# finally 
# 예외가 발생하더라도 정리코드를 실행해야 한다면 try/finally를 사용하라

def try_finally_example(filename):
    print('* 파일 열기')
    handle = open(filename, encoding='utf-8') # OSError 발생할 수 있음
    try:
        print('* 데이터 읽기')
        return handle.read()      # UnicodeDecodeError 발생할 수 있음
    finally:
        print('* close() 호출')
        handle.close()            # try 블록이 실행된 다음에는 항상 이 블록이 실행됨


filename = 'random_data.txt'

with open(filename, 'wb') as f:
    f.write(b'\xf1\xf2\xf3\xf4\xf5')  # 잘못된 utf-8 이진 문자열

# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#data = try_finally_example(filename)

# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#try_finally_example('does_not_exist.txt')


# else
# 코드에서 처리할 예외와 호출 스택을 거슬러 올라가며 전달할 예외를 명확히 구분하기 위해
# try/catch/else를 사용하라
# try에서 예외가 발생하지 않으면 elser가 실행됨
# else를 사용하면 try 안에 들어갈 코드를 최소화 한다
# try에 들어가는 코드가 줄어들면 발생할 여지가 있는 예외를 서로 구분할 수 있으므로 가독성이 좋아진다
import json

def load_json_key(data, key):
    try:
        print('* JSON 데이터 읽기')
        result_dict = json.loads(data)     # ValueError가 발생할 수 있음
    except ValueError as e:
        print('* ValueError 처리')
        raise KeyError(key) from e
    else:
        print('* 키 검색')
        return result_dict[key]            # KeyError가 발생할 수 있음

assert load_json_key('{"foo": "bar"}', 'foo') == 'bar'

# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#load_json_key('{"foo": bad payload', 'foo')

# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#load_json_key('{"foo": "bar"}', '존재하지 않음')


# 모든 요소를 한꺼번에 사용하기
# 복합적인 문장 안에 모든 요소를 다 넣고 싶다면
# try/except/else/finally 를 사용하라
UNDEFINED = object()

def divide_json(path):
    print('* 파일 열기')
    handle = open(path, 'r+')             # OSError가 발생할 수 있음
    try:
        print('* 데이터 읽기')
        data = handle.read()              # UnicodeDecodeError가 발생할 수 있음
        print('* JSON 데이터 읽기')
        op = json.loads(data)             # ValueError가 발생할 수 있음
        print('* 계산 수행')
        value = (
            op['numerator'] /
            op['denominator'])            # ZeroDivisionError가 발생할 수 있음
    except ZeroDivisionError as e:
        print('* ZeroDivisionError 처리')
        return UNDEFINED
    else:
        print('* 계산 결과 쓰기')
        op['result'] = value
        result = json.dumps(op)
        handle.seek(0)                    # OSError가 발생할 수 있음
        handle.write(result)              # OSError가 발생할 수 있음
        return value
    finally:
        print('* close() 호출')
        handle.close()                    # 어떤 경우든 실행됨

temp_path = 'random_data.json'

with open(temp_path, 'w') as f:
    f.write('{"numerator": 1, "denominator": 10}')

assert divide_json(temp_path) == 0.1

#
with open(temp_path, 'w') as f:
    f.write('{"numerator": 1, "denominator": 0}')

assert divide_json(temp_path) is UNDEFINED

#
with open(temp_path, 'w') as f:
    f.write('{"numerator": 1 bad data')

# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#divide_json(temp_path)

