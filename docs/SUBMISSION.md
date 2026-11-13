# 제출 체크리스트

## 로컬 완성 후 GitHub에 올리기

GitHub 웹에서 빈 저장소를 생성합니다. 저장소 주소와 작성자 정보를 본인 값으로 바꿔 실행합니다.

```powershell
git config user.name "본인 이름"
git config user.email "본인 이메일"
git remote add origin https://github.com/ACCOUNT/codyssey-quiz.git
git push -u origin main
```

이미 origin이 등록되어 있으면 `git remote -v`로 먼저 확인합니다. 비밀번호·토큰을 코드나 README에 적지 마세요.

## 실제 원격 clone/pull 실습

기존 저장소의 상위 폴더에서 다음을 실행합니다. 아래 폴더명은 예시입니다.

```powershell
git clone https://github.com/ACCOUNT/codyssey-quiz.git codyssey-quiz-copy
cd codyssey-quiz-copy
git config user.name "본인 이름"
git config user.email "본인 이메일"
Add-Content README.md "`nGitHub 복제 및 동기화 실습을 완료했습니다."
git add README.md
git commit -m "Docs: 복제 저장소에서 동기화 실습 기록"
git push
cd ../codyssey-quiz
git pull --ff-only
git log --oneline --graph --all
```

## 제출 자료

- GitHub 저장소 URL
- Python 버전, VS Code 및 Git 설정 화면 캡처
- 퀴즈 추가, 목록, 플레이 결과, 점수 화면 캡처
- 종료 후 다시 실행해 추가 문제와 점수가 유지되는 화면
- `git log --oneline --graph --all` 화면

`docs/validation.txt`는 자동 검증의 실제 출력입니다. 실행 화면 캡처를 대체했다고 간주하지 않습니다. GitHub 미연결 상태에서 원격 push/clone/pull을 완료했다고 주장하지 않습니다.
