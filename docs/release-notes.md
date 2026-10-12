## 설치

**[설치 파일 다운로드](https://github.com/hyunmin-apps/StudyGlass/releases/download/v1.0.0/StudyGlass-1.0.0-Install.command)** — 이 파일 하나만 받으세요.

1. 실행 중인 Study Glass를 **⌘Q로 종료**합니다.
2. 받은 파일을 다운로드 폴더에 두고 터미널에서 아래 한 줄을 실행합니다.

```bash
/bin/bash "$HOME/Downloads/StudyGlass-1.0.0-Install.command"
```

3. 안내를 확인하고 `y`를 입력하면 설치와 앱 실행이 진행됩니다.

macOS 14 이상 · Apple Silicon / Intel 공용. 기존 할 일과 체크 기록은 유지됩니다.

**Apple 공증 전 시험판입니다.** 동의하면 Study Glass 앱에만 격리 속성을 제거합니다. 시스템 전체 보안 설정은 변경하지 않습니다.

## 1.0.0 변경

- **AI 계획 가져오기**: 입력 양식을 복사해 GPT·Claude에 전달하고, 받은 JSON을 붙여넣어 날짜별 과목·할 일·세부 내용을 한 번에 등록합니다. 앱이 AI 요청을 대신 보내지는 않습니다.
- 등록 전 미리보기, 잘못된 날짜·양식 검사, 중복 항목 제외를 지원합니다.
- Mac에서 복사·붙여넣기 단축키를 지원합니다.


할 일 옆 **수정**에서 과목명·내용·세부 내용을 변경하거나 삭제할 수 있습니다. 기본 계획과 직접 추가한 할 일 모두 지원하며 주간 보기와 위젯에도 반영됩니다.

Assets의 ZIP은 설치 스크립트가 자동으로 받는 앱 파일입니다. 직접 다운로드할 필요 없습니다. `Source code`는 GitHub가 자동 표시하는 개발용 소스입니다.
