# 내장 타입을 여러 단계로 내포시키기보다는 클래스를 합성하라


# 파이썬 내장 딕셔너리 타입을 사용하면 객체의 생명 주기 동안 동적인 내부 상태를 잘 유지할 수 있다
# *동적 : 어떤 값이 들어올지 미리 알 수 없는 식별자들을 유지해야 한다는 뜻

# 미리 정의된 애트리뷰트를 사용하는 대신 딕셔너리에 이름을 저장하는 클래스를 정의할 수 있다

class SimpleGradebook:
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = []

    def report_grade(self, name, score):
        self._grades[name].append(score)

    def average_grade(self, name):
        grades = self._grades[name]
        return sum(grades) / len(grades)

book = SimpleGradebook()
book.add_student('아이작 뉴턴')
book.report_grade('아이작 뉴턴', 90)
book.report_grade('아이작 뉴턴', 95)
book.report_grade('아이작 뉴턴', 85)

print(book.average_grade('아이작 뉴턴'))

# 딕셔너리와 관련 내장 타입은 사용하기 너무 쉬우므로 과하게 확장하면서 깨지기 쉬운 코드를 작성할 위험성이 있다
# 위 코드에서 전체 성적이 아닌 과목별 성적을 리스트로 저장하고 싶다면
# _grades 딕셔너리를 변경해서 학생 이름이 다른 딕셔너리에 매핑하게 하고, 이 딕셔너리가 다시 과목을 성적의 리스트 값에 매핑하게 해야한다
from collections import defaultdict

class BySubjectGradebook:
    def __init__(self):
        self._grades = {}  # 외부 dict

    def add_student(self, name):
        self._grades[name] = defaultdict(list)  # 내부 dict

    def report_grade(self, name, subject, grade):
        by_subject = self._grades[name]
        grade_list = by_subject[subject]
        grade_list.append(grade)

    def average_grade(self, name):
        by_subject = self._grades[name]
        total, count = 0, 0
        for grades in by_subject.values():
            total += sum(grades)
            count += len(grades)
        return total / count

book = BySubjectGradebook()
book.add_student('알버트 아인슈타인')
book.report_grade('알버트 아인슈타인', '수학', 75)
book.report_grade('알버트 아인슈타인', '수학', 65)
book.report_grade('알버트 아인슈타인', '체육', 90)
book.report_grade('알버트 아인슈타인', '체육', 95)
print(book.average_grade('알버트 아인슈타인'))

# 위 코드는 다단계 딕셔너리를 처리해야하므로 report_grade와 average_grade 메서드가 복잡해지지만, 아직은 충분히 복잡도 관리를 할 수 있다

# 여기서 요구사항이 또 바뀌어
# 각 점수의 가중치를 함께 저장해서 중간고사와 기말고사가 다른 쪽지 시험보다 성적에 더 큰 영향을 끼치게 하고싶다
# 가장 안쪽에 있는 딕셔너리가 과목을 성적의 리스트로 매핑하던 것을
# (성적, 가중치) 튜플의 리스토로 매핑하도록 변경한다

class WeightedGradebook:
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = defaultdict(list)

    def report_grade(self, name, subject, score, weight):
        by_subject = self._grades[name]
        grade_list = by_subject[subject]
        grade_list.append((score, weight))

    def average_grade(self, name):
        by_subject = self._grades[name]
        score_sum, score_count = 0, 0

        for subject, scores in by_subject.items():
            subject_avg, total_weight = 0, 0

            for score, weight in scores:
                subject_avg += score * weight
                total_weight += weight

            score_sum += subject_avg / total_weight
            score_count += 1

        return score_sum / score_count
    
book = WeightedGradebook()
book.add_student('알버트 아인슈타인')
book.report_grade('알버트 아인슈타인', '수학', 75, 0.05)
book.report_grade('알버트 아인슈타인', '수학', 65, 0.15)
book.report_grade('알버트 아인슈타인', '수학', 70, 0.80)
book.report_grade('알버트 아인슈타인', '체육', 100, 0.40)
book.report_grade('알버트 아인슈타인', '체육', 85, 0.60)
print(book.average_grade('알버트 아인슈타인'))

# report_grade 단순한 변경만 일어났지만
# 변경된 average_grade 메서드는 루프 안에 루프가 쓰이면서 읽기 어려워졌다

# 클래스로 리팩터링하기
