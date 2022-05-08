# 함수가 여러 값을 반환하는 경우 절대로 네 값 이상 언패킹하지 말라


# 언패킹을 사용하면 함수가 둘 이상의 값을 반환할 수 있다.
def get_stats(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    return minimum, maximum

lengths = [63, 73, 72, 60, 67, 66, 71, 61, 72, 70]

minimum, maximum = get_stats(lengths) 

# 하지만 평균, 중앙값, 개수 등 여러가지를 요구한다고 가정하면 get_stats를 다음과 같이 확장해야한다.
def get_stats(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    count = len(numbers)
    average = sum(numbers) / count

    sorted_numbers = sorted(numbers)
    middle = count // 2
    if count % 2 == 0:
        lower = sorted_numbers[middle - 1]
        upper = sorted_numbers[middle]
        median = (lower + upper) / 2
    else:
        median = sorted_numbers[middle]

    return minimum, maximum, average, median, count

minimum, maximum, average, median, count = get_stats(lengths)

print(f'Min: {minimum}, Max: {maximum}')
print(f'Average: {average}, Median: {median}, Count {count}')

# 이 코드에는 두 가지 문제가 있다

# 첫 번째는 모든 리턴 값이 number이기 때문에 순서를 혼동하기 쉽다

# 올바른사용
minimum, maximum, average, median, count = get_stats(lengths)
# 실수로 중앙값과 평균값을 바꿔 썼다
minimum, maximum, median, average, count = get_stats(lengths)

# 두 번째 문제는 함수를 호출하는 부분과 리턴 값을 언패킹 하는 부분이 길고, 여러 가지 줄로 바꿀 수 있어서 가독성이 나쁘다
minimum, maximum, average, median, count = get_stats(
    lengths)

minimum, maximum, average, median, count = \
    get_stats(lengths)

(minimum, maximum, average,
 median, count) = get_stats(lengths)

(minimum, maximum, average, median, count
    ) = get_stats(lengths)
