"""격리된 임시 폴더에서 실제 저장과 예외 흐름을 검증한다."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from game import QuizGame
from inputs import read_number
from quiz import Quiz


class GameTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'state.json'
        self.output = io.StringIO()
        self.capture = contextlib.redirect_stdout(self.output)
        self.capture.__enter__()
        self.addCleanup(self.capture.__exit__, None, None, None)

    def test_inputs_retry_and_trim(self):
        with patch('builtins.input', side_effect=['', 'abc', '0', '9', ' 2 ']):
            self.assertEqual(read_number('選択: ', 1, 5), 2)

    def test_add_and_restart(self):
        game = QuizGame(self.path)
        with patch('builtins.input', side_effect=['', '새 문제', 'a', 'b', 'c', 'd', 'abc', '5', '2']):
            game.add_quiz()
        restored = QuizGame(self.path)
        self.assertEqual(len(restored.quizzes), 9)
        self.assertEqual(restored.quizzes[-1].answer, 2)
        self.assertIsNone(restored.best_score)

    def test_perfect_score_persists_and_does_not_decrease(self):
        game = QuizGame(self.path)
        with patch('builtins.input', side_effect=[str(q.answer) for q in game.quizzes]):
            game.play()
        self.assertEqual(QuizGame(self.path).best_score, 100)
        with patch('builtins.input', side_effect=[str(q.answer % 4 + 1) for q in game.quizzes]):
            game.play()
        self.assertEqual(game.best_score, 100)

    def test_zero_score_is_distinct_from_unplayed(self):
        game = QuizGame(self.path)
        with patch('builtins.input', side_effect=[str(q.answer % 4 + 1) for q in game.quizzes]):
            game.play()
        self.assertEqual(QuizGame(self.path).best_score, 0)

    def test_corruption_is_backed_up(self):
        self.path.write_text('{broken', encoding='utf-8')
        game = QuizGame(self.path)
        self.assertEqual(len(game.quizzes), 8)
        self.assertTrue(game.save_state())
        self.assertEqual(self.path.with_suffix('.json.bak').read_text(), '{broken')

    def test_invalid_schema(self):
        for value in [[], {'quizzes': [], 'best_score': True}, {'quizzes': [{}], 'best_score': None}]:
            self.path.write_text(json.dumps(value), encoding='utf-8')
            self.assertEqual(len(QuizGame(self.path).quizzes), 8)

    def test_empty_quiz_list(self):
        game = QuizGame(self.path)
        game.quizzes = []
        game.play()
        game.list_quizzes()
        self.assertIn('퀴즈가 없습니다', self.output.getvalue())

    def test_eof_and_ctrl_c_save(self):
        for exception in (EOFError, KeyboardInterrupt):
            with patch('builtins.input', side_effect=exception):
                QuizGame(self.path).run()
            self.assertTrue(self.path.exists())

    def test_interrupted_quiz_is_not_added(self):
        game = QuizGame(self.path)
        with patch('builtins.input', side_effect=['2', '문제', KeyboardInterrupt]):
            game.run()
        self.assertEqual(len(QuizGame(self.path).quizzes), 8)

    def test_save_failure(self):
        game = QuizGame(self.path.parent / 'missing' / 'state.json')
        self.assertFalse(game.save_state())

    def test_quiz_validation(self):
        for answer in (0, 5, True, '1'):
            with self.assertRaises(ValueError):
                Quiz('문제', ['a', 'b', 'c', 'd'], answer)


if __name__ == '__main__':
    unittest.main(verbosity=2)
