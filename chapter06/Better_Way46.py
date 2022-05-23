# 재사용 가능한 @property 메서드를 만들려면 디스크립터를 사용하라

# @property 내장기능의 가장 큰 문제점은 재사용성이다
# 데코레이션하는 메서드를 같은 클래스에 속하는 여러 애트리뷰트로 사용할 수는 없다
# 서로 무관한 클래스 사이에서 @property 데코레이터를 적용한 메서드를 재사용할 수도 없다

# ex) 학생의 숙제 점수가 백분율값인지 검증하고 싶다
class Homework:
    def __init__(self):
        self._grade = 0

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        if not (0 <= value <= 100):
            raise ValueError(
                '점수는 0과 100 사이입니다')
        self._grade = value

galileo = Homework()
galileo.grade = 95

# 이제 이 학생에게 시험 점수를 부여하고 싶다고 하자
# 시험과목은 여러 개, 각 과목마다 별도의 점수를 부여함

class Exam:
    def __init__(self):
        self._writing_grade = 0
        self._math_grade = 0

    @staticmethod
    def _check_grade(value):
        if not (0 <= value <= 100):
            raise ValueError(
                '점수는 0과 100 사이입니다')

    @property
    def writing_grade(self):
        return self._writing_grade

    @writing_grade.setter
    def writing_grade(self, value):
        self._check_grade(value)
        self._writing_grade = value

    @property
    def math_grade(self):
        return self._math_grade

    @math_grade.setter
    def math_grade(self, value):
        self._check_grade(value)
        self._math_grade = value
        
# 이런 식으로 계속 확장하려면, 시험 과목을 이루는 각 부분마다
# 새로운 @property를 지정하고 관련 검증 메서드를 작성해야한다
# 이런 경우 파이썬에서 적용할 수 있는 더 나은 방법은 디스크립터를 사용하는 것이다
# 디스크립터 클래스는 __get__과 __set__ 메서드를 제공한다
class Grade:
    def __init__(self):
        self._value = 0
    def __get__(self, instance, instance_type):
        return self._value
    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError(
                '점수는 0과 100 사이입니다')
        self._value = value

class Exam:
    # 클래스 애트리뷰트
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

first_exam = Exam()
first_exam.writing_grade = 82
first_exam.science_grade = 99
print('쓰기', first_exam.writing_grade)
print('과학', first_exam.science_grade)

second_exam = Exam()
second_exam.writing_grade = 75
print(f'두 번째 쓰기 점수 {second_exam.writing_grade} 맞음')
print(f'첫 번째 쓰기 점수 {first_exam.writing_grade} 틀림; '
      f'82점이어야 함')

# 위 구현이 잘못 동작하는 이유
# writing_grade 클래스 애트리뷰트로 한 Grade 인스턴스를 모든 Exam 인스턴스가 공유한다는 점
# 이를 해결하려면
# Grade 클래스가 각각의 유일한 Exam 인스턴스에 대해 따로 값을 추적하게 해야한다

class Grade:
    def __init__(self):
        self._values = {}

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError(
                '점수는 0과 100 사이입니다')
        self._values[instance] = value


class Exam:
    # 클래스 애트리뷰트
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

first_exam = Exam()
first_exam.writing_grade = 82
first_exam.science_grade = 99
print('쓰기', first_exam.writing_grade)
print('과학', first_exam.science_grade)

second_exam = Exam()
second_exam.writing_grade = 75
print(f'두번째 쓰기 점수 {second_exam.writing_grade} 맞음')
print(f'첫번째 쓰기 점수 {first_exam.writing_grade} 맞음')

# 여전히 한 가지 함정이 존재한다
# 바로 메모리를 누수(leak) 시킨다
# _values라는  딕셔너리는 프로그램이 실행되는 동안 __set__ 호출에 전달된
# 모든 인스턴스에 대한 참조를 저장하고 있다
# 이로 인해 참조 카운터가 절대로 0이 될 수 없고, 가비지 컬랙터가 메모리를 재활용하지 못한다

# 이 문제를 해결하기 위해 weakref 내장 모듈을 사용할 수 있다
# WeakKeyDictionary 라는 특별한 클래스를 제공한다

from weakref import WeakKeyDictionary
class Grade:
    def __init__(self):
        self._values = WeakKeyDictionary()

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError(
                '점수는 0과 100 사이입니다')
        self._values[instance] = value


class Exam:
    # 클래스 애트리뷰트
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

first_exam = Exam()
first_exam.writing_grade = 82
second_exam = Exam()
second_exam.writing_grade = 75
print(f'첫 번째 쓰기 점수 {first_exam.writing_grade} 맞음')
print(f'두 번째 쓰기 점수 {second_exam.writing_grade} 맞음')