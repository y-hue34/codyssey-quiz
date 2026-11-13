"""실제 QuizGame에 자동 입력을 제공하여 전체 메뉴 흐름을 재현한다.

실행: 프로젝트 루트에서 python docs/demo_walkthrough.py
사용자 state.json과 분리된 임시 폴더에서 실행한다.
"""
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from game import QuizGame


def run_session(path, values):
    answers = iter(values)

    def automated_input(prompt=''):
        value = next(answers)
        print(prompt + value)
        return value

    with patch('builtins.input', side_effect=automated_input):
        game = QuizGame(path)
        game.run()
        return game


def main():
    print('자동 입력을 이용한 실제 프로그램 검증 기록 (직접 입력한 터미널 캡처 아님)')
    # 임시 폴더를 프로젝트 안에 생성하여 실행 환경의 기본 TEMP 권한에 의존하지 않는다.
    root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix='quiz-evidence-', dir=root) as temporary:
        path = Path(temporary) / 'state.json'
        print('\n=== 1차 실행: 입력 오류 → 목록 → 추가 → 플레이 → 점수 → 종료 ===')
        first = run_session(path, [
            '', 'abc', '9', ' 3 ', '4', '2', '', 'Git의 준비 영역에 파일을 추가하는 명령은?',
            'git add', 'git pull', 'git log', 'git clone', '0', '1', '3', '1',
            '', 'abc', '0', '5', '2', '3', '1', '4', '1', '2', '3', '4', '2', '4', '5',
        ])
        assert len(first.quizzes) == 9 and first.best_score == 89
        print('\n=== 2차 실행: 재실행 후 문제 9개와 최고 점수 89점 유지 ===')
        second = run_session(path, ['3', '4', '5'])
        assert len(second.quizzes) == 9 and second.best_score == 89
        print('\n검증 완료: 메뉴 1~5, 입력 재시도, 정답/오답, 저장과 재실행 모두 확인')


if __name__ == '__main__':
    main()
