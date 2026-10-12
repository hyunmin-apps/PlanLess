# Study Glass — 날짜별 공부 계획

<img src="Resources/AppIcon.png" width="128" alt="Study Glass 아이콘">

그날 끝낼 분량을 확인하고 체크하는 미니멀 macOS 계획 앱입니다. **한 주의 일차별 목표를 펼쳐 보고, 날짜를 눌러 하루에 집중**합니다. 과목별 색상과 다크 모드, macOS 바탕화면 위젯을 제공합니다. 계정이나 외부 서버 없이 Mac에 저장합니다.

[다운로드](https://github.com/hyunmin-apps/StudyGlass/releases) · [버그 제보](https://github.com/hyunmin-apps/StudyGlass/issues) · [MIT 라이선스](LICENSE)

## 다운로드와 설치

**[설치 스크립트 다운로드](https://github.com/hyunmin-apps/StudyGlass/releases/download/v1.0.1/StudyGlass-1.0.1-Install.command)**

실행하고 안내에 동의하면 공식 ZIP의 SHA-256 및 서명 구조를 확인한 뒤 `~/Applications`에 설치하고 **Study Glass에만 격리 해제**를 적용합니다. 기존 앱은 ZIP으로 백업하고 교체하며, 직접 추가한 기록은 유지합니다. 관리자 암호는 필요하지 않습니다.

받은 파일을 **다운로드 폴더에 둔 상태로**, 터미널에 아래 한 줄 전체를 복사해 실행하세요. `$HOME`이 현재 사용자 폴더를 자동으로 가리키므로 사용자 이름을 바꿀 필요가 없습니다.

```bash
/bin/bash "$HOME/Downloads/StudyGlass-1.0.1-Install.command"
```

안내를 읽고 `y`를 입력하면 설치가 진행됩니다. `/bin/bash`만 먼저 실행하지 말고 **파일 경로까지 같은 줄로 실행**하세요. 파일이 다른 폴더에 있거나 이름 뒤에 `(1)` 등이 붙었다면 실제 파일 경로에 맞춰야 합니다.

**공증을 대체하지 않으며 설치자가 스크립트를 실행하는 단계는 필요합니다.** `/Applications`의 기존 앱은 자동 삭제하지 않습니다.

**설치 파일은 `.command` 하나만 받으면 됩니다.** 릴리스의 ZIP은 설치 스크립트가 자동 다운로드하는 앱 파일입니다. DMG와 별도 안내·검증 파일은 배포 페이지에 올리지 않습니다. `Source code`는 GitHub가 자동 표시하는 개발용 소스입니다.

업데이트 전 실행 중인 Study Glass를 **⌘Q로 종료**하세요. 설치 스크립트는 공식 ZIP의 고정 SHA-256과 서명 구조를 확인합니다.

## 기능

- 하루 보기 / 한 주 펼치기 / 이전·다음 주 / 오늘 이동.
- 과목명과 하루 목표 추가·수정·삭제. 같은 과목명은 앱과 위젯에서 같은 색상으로 표시.
- 미시작 → 학습 → 통과 → 미시작 순서의 체크와 자동 저장.
- 상세 지침을 필요할 때만 펼치는 다크 화면.
- macOS 정식 WidgetKit 위젯: 하루 목표 소·중·대, 주간 목표 대.
- 작은 앱 창·다른 창 위 고정은 정식 위젯과 별도로 제공.

처음 설치하면 빈 계획으로 시작합니다. 직접 목표를 추가하거나 AI 결과를 가져오세요. 업데이트는 직접 추가·가져온 계획을 유지합니다. 이전 버전에 내장된 예제 계획은 더 이상 표시하지 않습니다.

## 지원과 검증 범위

| 항목 | 범위 |
| --- | --- |
| Apple Silicon | Universal arm64 바이너리, 개발 Mac에서 앱과 위젯 UI 실행 확인 |
| Intel | Universal x86_64 바이너리 포함. CI 결과는 아래 링크 참조. 실제 Intel Mac 위젯 배치 검증은 별도 필요 |
| 최소 OS | macOS 14.0. 최소 버전 실기기 검증은 아직 하지 않음 |
| 서명 | 로컬 ad-hoc 서명. Developer ID·공증 없음 |

[빌드와 실행 CI](https://github.com/hyunmin-apps/StudyGlass/actions/workflows/build.yml) · [검증 기록](docs/verification.md)

위젯은 오늘 또는 가장 가까운 예정일을 표시합니다. 주간 위젯은 해당 날짜가 속한 월~일을 표시하며, 작은 크기에서는 내용이 요약됩니다. 앱 변경 사항은 위젯 갱신 시 반영되므로 즉시 표시를 보장하지 않습니다. 위젯 자체에서 체크하거나 주를 넘기는 기능은 아직 없습니다.

## 데이터와 개인정보

체크와 사용자 목표는 `~/Library/Application Support/StudyGlass/state.json`에 저장합니다. 앱이 위젯 전용 컨테이너의 `Documents/study-state.json`에 사본을 전달합니다. 로그인·광고·분석 수집·클라우드 동기화는 없습니다. 사용자의 실제 체크 상태와 메모는 소스나 설치 파일에 포함하지 않습니다.

업데이트 전 데이터 파일을 복사하면 백업할 수 있습니다. 앱을 교체해도 데이터 경로는 유지됩니다. 앱 삭제 시에는 바탕화면 위젯을 제거하고 앱을 휴지통으로 옮기세요. 사용자 데이터는 자동 삭제하지 않습니다.

## 소스 빌드

macOS와 Xcode Command Line Tools 또는 Xcode, Python 3이 필요합니다. 다운로드 의존성 없이 Apple 시스템 프레임워크로 빌드합니다.

```sh
./build.sh                       # arm64 + x86_64 Universal
./build.sh --arch arm64          # Apple Silicon만
./build.sh --arch x86_64         # Intel만
python3 tests/verify.py 'build/universal/Study Glass.app'
python3 scripts/package.py      # DMG, ZIP, SHA256SUMS, manifest
```

앱과 위젯을 각각 두 아키텍처로 컴파일하고 합친 뒤, 위젯 → 앱 순서로 서명합니다. `Widget/build-widget.sh`는 같은 전체 빌드를 호출하는 호환 명령입니다. 빌드는 사용 중인 설치 앱을 교체하지 않습니다.

## 배포

1. `VERSION`과 `CHANGELOG.md`를 갱신합니다.
2. Universal 빌드와 검증 후 `scripts/package.py`를 실행합니다.
3. CI의 Apple Silicon·Intel 결과를 확인합니다.
4. 해당 커밋에 버전 태그를 붙이고 `dist/`의 설치 스크립트와 앱 ZIP만 GitHub Release에 올립니다. DMG·해시·manifest는 로컬 검증용으로 보관합니다.

Developer ID 인증서와 Keychain의 notarytool 인증 프로필이 준비된 경우:

```sh
python3 scripts/notarize.py --identity 'Developer ID Application: NAME (TEAMID)' --keychain-profile studyglass-notary
```

이 경로는 hardened runtime과 timestamp를 사용해 위젯 → 앱 서명, Apple 공증, 티켓 부착, Gatekeeper 통과 확인, DMG 공증을 수행합니다. 공증 실패 시 패키징을 중단합니다. 현재 인증서가 없어 이 경로의 실제 Apple 공증 성공은 검증되지 않았습니다. GitHub의 배포 워크플로는 계속 시험판 전용입니다.

정식 서명 및 공증을 도입하기 전에는 사전 릴리스로 배포하고, 실제 검증 범위와 미검증 항목을 릴리스 설명에 기재합니다.

## 구성

- `Sources/main.swift`: macOS 창, 로컬 저장, 위젯 데이터 전달, 날짜 링크.
- `Resources/index.html`: 일별·주간 목표 화면.
- `Resources/plan.json`: 기본 예제 계획의 단일 원본.
- `Widget/StudyWidget.swift`: 정식 macOS 위젯.
- `Sources/icon.swift`: 앱 아이콘 원본 드로잉.
- `scripts/`: Universal 빌드와 배포 파일 생성.

날짜 중심 사용 흐름은 [todo mate](https://www.todomate.net/)와 [Things](https://culturedcode.com/things/features/)를 참고했습니다. 아이콘과 UI는 자체 작성했으며 해당 서비스의 리소스를 포함하지 않습니다.

### AI 결과로 계획 등록

앱 상단 **AI 계획 → 입력 양식 → 양식 복사**에서 형식을 복사하세요. GPT·Claude에 원하는 계획을 직접 요청하면서 양식을 함께 전달한 뒤, 받은 JSON을 앱에 붙여넣고 **미리보기 → 등록**을 누르면 날짜별 할 일이 추가됩니다.

앱은 AI에 요청을 보내지 않습니다. 기존 계획은 유지하며 날짜·과목·제목·세부 내용이 같은 항목은 건너뜁니다. 등록한 항목도 수정·삭제할 수 있습니다.
