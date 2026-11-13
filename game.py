"""메뉴, 게임 진행, 점수 및 JSON 저장을 관리한다."""
import json
import os
from pathlib import Path

from defaults import default_quizzes
from inputs import read_number, read_text
from quiz import Quiz


class QuizGame:
    def __init__(self, state_path=None):
        self.state_path = Path(state_path) if state_path else Path(__file__).resolve().parent / 'state.json'
        self.quizzes = default_quizzes()
        self.best_score = None  # None: 아직 완료한 게임 없음, 0: 플레이 결과 0점
        self.load_state()

    def load_state(self):
        try:
            with self.state_path.open(encoding='utf-8') as file:
                data = json.load(file)
            if not isinstance(data, dict) or not isinstance(data['quizzes'], list):
                raise ValueError('잘못된 데이터 구조')
            quizzes = [Quiz.from_dict(item) for item in data['quizzes']]
            score = data['best_score']
            if score is not None and (type(score) is not int or not 0 <= score <= 100):
                raise ValueError('최고 점수 범위 오류')
            self.quizzes, self.best_score = quizzes, score
            print(f'저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개)')
        except FileNotFoundError:
            print('저장 파일이 없어 기본 퀴즈로 시작합니다.')
        except (OSError, UnicodeError, ValueError, KeyError, TypeError, RecursionError) as error:
            print(f'저장 파일을 읽을 수 없어 기본 데이터로 시작합니다: {error}')
            print('손상된 원본은 다음 저장 전에 state.json.bak으로 보관합니다.')
            self._backup_required = True

    def save_state(self):
        temporary = self.state_path.with_suffix('.json.tmp')
        try:
            if getattr(self, '_backup_required', False) and self.state_path.exists():
                # 기존 백업을 덮어쓰지 않는다.
                backup = self.state_path.with_suffix('.json.bak')
                index = 1
                while backup.exists():
                    backup = self.state_path.with_suffix(f'.json.bak{index}')
                    index += 1
                backup.write_bytes(self.state_path.read_bytes())
                self._backup_required = False
            data = {'quizzes': [quiz.to_dict() for quiz in self.quizzes], 'best_score': self.best_score}
            with temporary.open('w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
                file.write('\n')
            os.replace(temporary, self.state_path)
            return True
        except (OSError, UnicodeError) as error:
            print(f'저장하지 못했습니다. 폴더 권한과 저장 공간을 확인하세요: {error}')
            return False

    def show_menu(self):
        print('\n========== 파이썬 · Git 퀴즈 ==========')
        print('1. 퀴즈 풀기\n2. 퀴즈 추가\n3. 퀴즈 목록\n4. 점수 확인\n5. 종료')

    def play(self):
        if not self.quizzes:
            print('퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.')
            return
        correct = 0
        print(f'퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)')
        for number, quiz in enumerate(self.quizzes, 1):
            print(f'\n[문제 {number}]')
            quiz.display()
            answer = read_number('정답 입력 (1~4): ', 1, 4)
            if quiz.is_correct(answer):
                correct += 1
                print('정답입니다!')
            else:
                print(f'오답입니다. 정답: {quiz.answer}. {quiz.choices[quiz.answer - 1]}')
        score = round(correct / len(self.quizzes) * 100)
        print(f'결과: {len(self.quizzes)}문제 중 {correct}문제 정답! ({score}점)')
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print('새로운 최고 점수입니다!')
        self.save_state()

    def add_quiz(self):
        print('새로운 퀴즈를 추가합니다.')
        question = read_text('문제: ')
        choices = [read_text(f'선택지 {i}: ') for i in range(1, 5)]
        answer = read_number('정답 번호 (1~4): ', 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        if self.save_state():
            print('퀴즈를 추가하고 저장했습니다!')
        else:
            print('퀴즈는 현재 실행 중에만 유지됩니다. 종료 전 저장을 다시 시도합니다.')

    def list_quizzes(self):
        print(f'등록된 퀴즈 목록 (총 {len(self.quizzes)}개)')
        if not self.quizzes:
            print('퀴즈가 없습니다.')
        for number, quiz in enumerate(self.quizzes, 1):
            print(f'[{number}] {quiz.question}')

    def show_score(self):
        if self.best_score is None:
            print('아직 완료한 게임이 없습니다.')
        else:
            print(f'최고 점수: {self.best_score}점')

    def run(self):
        try:
            actions = {1: self.play, 2: self.add_quiz, 3: self.list_quizzes, 4: self.show_score}
            while True:
                self.show_menu()
                choice = read_number('선택: ', 1, 5)
                if choice == 5:
                    break
                actions[choice]()
        except (KeyboardInterrupt, EOFError):
            print('\n입력이 중단되어 저장 후 종료합니다. 진행 중인 게임과 미완성 퀴즈는 반영하지 않습니다.')
        finally:
            if self.save_state():
                print('데이터를 저장했습니다. 종료합니다.')
            else:
                print('저장 실패: 이번 실행의 변경사항이 디스크에 반영되지 않았습니다.')
