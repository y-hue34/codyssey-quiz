"""잘못된 입력은 안내하고 같은 질문으로 돌아간다."""


def read_number(prompt, minimum, maximum):
    while True:
        raw = input(prompt).strip()
        try:
            number = int(raw)
        except ValueError:
            print(f'{minimum}~{maximum} 사이의 숫자를 입력하세요.')
            continue
        if minimum <= number <= maximum:
            return number
        print(f'{minimum}~{maximum} 사이의 숫자를 입력하세요.')


def read_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print('빈 내용은 등록할 수 없습니다. 다시 입력하세요.')
