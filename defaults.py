"""주제: 파이썬과 Git 기초. 기본 문제 8개."""
from quiz import Quiz


def default_quizzes():
    return [
        Quiz('Python에서 화면에 내용을 출력하는 함수는?', ['input()', 'print()', 'len()', 'int()'], 2),
        Quiz('정수를 나타내는 자료형은?', ['str', 'bool', 'int', 'list'], 3),
        Quiz('조건에 따라 다른 코드를 실행할 때 쓰는 문법은?', ['if', 'import', 'def', 'class'], 1),
        Quiz('함수를 정의하는 키워드는?', ['for', 'return', 'while', 'def'], 4),
        Quiz('클래스 인스턴스의 초기화에 사용하는 메서드는?', ['__init__', 'print', 'open', 'append'], 1),
        Quiz('JSON 객체와 대응하는 Python 자료형은?', ['tuple', 'dict', 'set', 'bool'], 2),
        Quiz('Git에서 변경 이력을 기록하는 명령은?', ['git pull', 'git clone', 'git commit', 'git status'], 3),
        Quiz('원격 저장소를 새 로컬 폴더로 복제하는 명령은?', ['git merge', 'git add', 'git push', 'git clone'], 4),
    ]
