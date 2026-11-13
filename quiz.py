"""개별 4지선다 퀴즈를 표현한다."""
from dataclasses import dataclass


@dataclass
class Quiz:
    question: str
    choices: list[str]
    answer: int

    def __post_init__(self):
        if not isinstance(self.question, str) or not self.question.strip():
            raise ValueError('문제가 비어 있습니다.')
        if (not isinstance(self.choices, list) or len(self.choices) != 4
                or any(not isinstance(c, str) or not c.strip() for c in self.choices)):
            raise ValueError('비어 있지 않은 선택지 4개가 필요합니다.')
        if type(self.answer) is not int or not 1 <= self.answer <= 4:
            raise ValueError('정답은 1~4 정수여야 합니다.')

    def display(self):
        print(self.question)
        for number, choice in enumerate(self.choices, 1):
            print(f'{number}. {choice}')

    def is_correct(self, answer):
        return self.answer == answer

    def to_dict(self):
        return {'question': self.question, 'choices': self.choices, 'answer': self.answer}

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError('퀴즈 데이터는 객체여야 합니다.')
        return cls(data['question'], data['choices'], data['answer'])
