# 인덱스를 사용하는 대신 대입을 사용해 데이터를 언패킹하라

snack_calories = {
    '감자칩' : 140,
    '팝콘' : 80,
    '땅콩' : 190
}  
items = tuple(snack_calories.items())
print(items) # (('감자칩', 140), ('팝콘', 80), ('땅콩', 190))

# 튜플에 있는 값은 숫자 인덱스를 사용하여 접근할 수 있다.
item = ('호박엿', '식혜')
first = item[0]
second = item[1]
print(first, '&', second) # 호박엿 & 식혜

# 튜플은 일단 만들어지면, 인덱스를 통해 새 값을 대입해서 튜플을 변경할 수 없다.
pair = ('약과', '호박엿')
pair[0] = '타래과' # TypeError: 'tuple' object does not support item assignment

# 파이썬에는 언패킹 구문이 있다.
# 언패킹 구문을 사용하면 한 문장 안에서 여러 값을 대입할 수 있다.
item = ('호박엿', '식혜')
fisrt, second = item
print(first, '&', second)

favorite_snacks = {
    '짭조름한 과자': ('프레즐', 100),
    '달콤한 과자': ('쿠키', 180),
    '채소': ('당근', 20)
}
((type1, (name1, cals1)),
(type2, (name2, cals2)),
(type3, (name3, cals3))) = favorite_snacks.items()

print(f'제일 좋아하는 {type1} 는 {name1}, {name1} 칼로리입니다.')
print(f'제일 좋아하는 {type2} 는 {name2}, {name2} 칼로리입니다.')
print(f'제일 좋아하는 {type3} 는 {name3}, {name3} 칼로리입니다.')


# 정렬에서의 언패킹

def bubble_sort(a):
    for _ in range(len(a)):
        for i in range(1, len(a)):
            if a[i] < a[i-1]:
                temp = a[i]
                a[i] = a[i-1]
                a[i-1] = temp
                
names = ['프레즐', '당근', '쑥갓', '베이컨']
bubble_sort(names)
print(names)

def bubble_sort(a):
    for _ in range(len(a)):
        for i in range(1, len(a)):
            if a[i] < a[i-1]:
                a[i-1], a[i] = a[i], a[i-1]
names = ['프레즐', '당근', '쑥갓', '베이컨']
bubble_sort(names)
print(names)

# 언패킹의 또다른 용례는 for루프와 컴프리핸션, 제너레이터식 이다.

snacks = [('베이컨', 350), ('도넛', 240), ('머핀', 190)]
for i in range(len(snacks)):
    item = snacks[i]
    name = item[0]
    calories = item[1]
    print(f'#{i+1}: {name} 은 {calories}칼로리입니다.')
    
# 구조 내부의 깊숙한 곳의 데이터를 인덱스로 찾으려면 코드가 길어진다.

for rank, (name, calories) in enumerate(snacks, 1):
    print(f'#{rank}: {name} 은 {calories}칼로리입니다.')
    
    