# 애트리뷰트를 리팩터링하는 대신 @property를 사용하라

# @property의 고급 활용법이자 흔히 사용하는 기법으로는
# 간단한 수치 애트리뷰트를 그때그때 요청에 따라 계산해 제공하도록 바꾸는 것을 들 수 있다
# 이 기법은 기존 클래스를 호출하는 코드를 전혀 바꾸지 않고도 클래스 애트리뷰트의 기존 동작을 변경할 수 있기때문에 유용하다

# 일반 파이썬 객체를 사용해 리키 버킷 흐름 제어 알고리즘을 구현한다고 치자
from datetime import datetime, timedelta

# Bucket 클래스는 남은 가용 용량과 가용 용량의 잔존 시간을 표현
class Bucket:
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.quota = 0

    def __repr__(self):
        return f'Bucket(quota={self.quota})'
# 리키 버킷 알고리즘은 시간을 일정한 간격으로 구분하고('주기')
# 가용 용량을 소비할 때마다 시간을 검사해서 주기가 달라질 경우에는 
# 이전 주기에 미사용한 가용 용량이 새로운 주기로 넘어오지 못하게 막는다

def fill(bucket, amount):
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount

def deduct(bucket, amount):
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        return False # 새 주기가 시작됐는데 아직 버킷 할당량이 재설정되지 않았다
    if bucket.quota - amount < 0:
        return False # 버킷의 가용 용량이 충분하지 못하다
    else:
        bucket.quota -= amount
        return True  # 버킷의 가용 용량이 충분하므로 필요한 분량을 사용한다

bucket = Bucket(60)
fill(bucket, 100)
print(bucket)

if deduct(bucket, 99):
    print('99 용량 사용')
else:
    print('가용 용량이 작아서 99 용량을 처리할 수 없음')
print(bucket)

if deduct(bucket, 3):
    print('3 용량 사용')
else:
    print('가용 용량이 작아서 3 용량을 처리할 수 없음')
print(bucket)

# 이 구현의 문제점은 버킷이 시작될 때 가용 용량이 얼마인지 알 수 없다는 것
# 이러한 문제를 해결하기 위해 이번 주기에 재설정된 가용 용량인 max_quota와 
# 이번 주기에 버킷에서 소비한 용량의 합계인 quota_consumed를 추적하도록 클래스를 변경한다


class NewBucket:
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0

    def __repr__(self):
        return (f'NewBucket(max_quota={self.max_quota}, '
                f'quota_consumed={self.quota_consumed})')

    @property
    def quota(self):
        return self.max_quota - self.quota_consumed

    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            # 새로운 주기가 되고 가용 용량을 재설정하는 경우
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            # 새로운 주기가 되고 가용 용량을 추가하는 경우
            assert self.quota_consumed == 0
            self.max_quota = amount
        else:
            # 어떤 주기 안에서 가용 용량을 소비하는 경우
            assert self.max_quota >= self.quota_consumed
            self.quota_consumed += delta


bucket = NewBucket(60)
print('최초', bucket)
fill(bucket, 100)
print('보충 후', bucket)

if deduct(bucket, 99):
    print('99 용량 사용')
else:
    print('가용 용량이 작아서 99 용량을 처리할 수 없음')
print('사용 후', bucket)

if deduct(bucket, 3):
    print('3 용량 사용')
else:
    print('가용 용량이 작아서 3 용량을 처리할 수 없음')

print('여전히', bucket)
