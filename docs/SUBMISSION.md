# 제출 체크리스트

## 현재 완료 상태

- 공개 GitHub 저장소: https://github.com/y-hue34/codyssey-quiz
- 필수 퀴즈 기능, 기본 문제 8개, 클래스 분리, JSON 저장과 예외 처리 구현
- 자동 검증 11개 통과: `validation.txt`
- 기능별 커밋 10개 이상, `feature/quiz-play` 생성 및 main 병합 후 실제 GitHub push 완료
- 별도 폴더에서 GitHub clone, README 수정 및 commit/push, 원래 폴더에서 pull 완료
- 원격 동기화 증거: `git-practice.txt`
- 실제 프로그램 실행 출력: `01-menu-list.txt`, `02-add.txt`, `03-play.txt`, `04-restart-invalid-input.txt`
- 실행 로그·환경 기록·Git 그래프 파일의 VS Code 화면 캡처 5개: `screenshots/`
- 확인 필요: 직접 터미널 화면을 요구하는 경우 추가 캡처 필요. 현재 이미지는 로그 파일 표시 화면임
- 코디세이: 프로젝트 URL 및 main 브랜치 선택 후 저장 버튼 클릭. 이후 사용자가 네이토 사전평가를 실행해 2026-11-13 23:56:38에 75점(15/20)을 받았다고 결과를 제공함
- 해당 사전평가의 미통과 5개와 PASS 항목 개선 제안을 보완함: `ASSESSMENT_RESPONSE.md`
- 문서 보완 후 재평가 및 최종 평가 요청: 아직 실행하지 않음

실행 로그는 실제 프로그램 출력이며 스크린샷은 아닙니다. 커밋 작성자는 실제 구현 주체인 Codex로 기록했습니다.

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

`docs/validation.txt`는 자동 검증의 실제 출력입니다. 실행 화면 캡처를 대체했다고 간주하지 않습니다.
