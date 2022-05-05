# __missing__을 사용해 키에 따라 다른 디폴트 값을 생성하는 방법을 알아두라

# setdefault나 defaultdict 모두 사용하기 적당하지 않은 경우도 있다.

pictures = {}
path = 'profile_1234.png'

if (handle := pictures.get(path)) is None:
    try:
        handle = open(path, 'a+b')
    except OSError:
        print(f'Failed to open path {path}')
        raise
    else:
        pictures[path] = handle

handle.seek(0)
image_data = handle.read()

print(pictures)
print(image_data)

# 파일 핸들이 이미 딕셔너리 안에 있으면 이 코드는 딕셔너리를 단 한번만 읽는다
# 파일 핸들이 없으면 get을 사용해 한번 읽고 else절에서 핸들을 딕셔너리에 대입한다

# 하지만 딕셔너리를 더 많이 읽고 내포되는 블록 깊이가 더 깊어지는 단점이 있다

pictures = {}
path = 'profile_9991.png'


try:
    handle = pictures.setdefault(path, open('a+b'))
except OSError:
    print(f'경로를 열 수 없습니다 {path}')
    raise
else:
    pictures[path] = handle

handle.seek(0)
image_data = handle.read()

# 이 코드는 문제가 많다
# open이 딕셔너리에 경로가 있는지 없는지 관계없이 항상 호출된다
# open이 예외를 던질 수 있으므로 이 예외를 처리해야한다
# 하지만 이 예외를 같은 줄에 있는 setdefault가 던지는 예외와 구분하지 못할 수도 있다

from collections import defaultdict

def open_picture(profile_path):
    try:
        return open(profile_path, 'a+b')
    except OSError:
        print(f'Failed to open path {profile_path}')
        raise

pictures = defaultdict(open_picture)
handle = pictures[path]
handle.seek(0)
image_data = handle.read()

# 문제는 defaultdict 생성자에 전달한 함수는 인자를 받을 수 없다는 데 있다
# 이런 상황에서는 setdefault와 defaultdict 모두 필요한 기능을 제공하지 못한다

# 이런 상황이 흔히 발생하기 때문에 파이썬은 다른 해법을 내장해 제공한다
# dict타입의 하위 클래스를 만들고 __missing__ 특별 메서드를 구현하면 키가 없는 경우를 처리하는 로직을 커스텀화 할 수 있다.

class Pictures(dict):
    def __missing__(self, key):
        value = open_picture(key)
        self[key] = value
        return value

pictures = Pictures()
handle = pictures[path]
handle.seek(0)
image_data = handle.read()
print(pictures)
print(image_data)