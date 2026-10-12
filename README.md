# Study Glass — 날짜별 공부 계획

<img src="Resources/AppIcon.png" width="128" alt="Study Glass 아이콘">

그날 끝낼 분량을 확인하고 체크하는 미니멀 macOS 계획 앱입니다. **한 주의 일차별 목표를 펼쳐 보고, 날짜를 눌러 하루에 집중**합니다. 과목별 색상과 다크 모드, macOS 바탕화면 위젯을 제공합니다. 계정이나 외부 서버 없이 Mac에 저장합니다.

[다운로드](https://github.com/hyunmin-apps/StudyGlass/releases) · [버그 제보](https://github.com/hyunmin-apps/StudyGlass/issues) · [MIT 라이선스](LICENSE)

## 다운로드와 설치

**[설치 스크립트 다운로드](https://github.com/hyunmin-apps/StudyGlass/releases/download/v0.1.2/StudyGlass-0.1.2-Install.command)**

실행하고 안내에 동의하면 공식 ZIP의 SHA-256 및 서명 구조를 확인한 뒤 `~/Applications`에 설치하고 **Study Glass에만 격리 해제**를 적용합니다. 기존 앱은 백업하며 기록은 유지합니다. 관리자 암호는 필요하지 않습니다.

`.command` 자체가 차단되면 터미널에 `/bin/bash `를 입력하고 받은 파일을 드래그한 뒤 Enter를 누르세요. 스크립트의 출처와 내용을 확인한 후 실행하세요. **공증을 대체하지 않으며 설치자가 스크립트를 실행하는 단계는 필요합니다.** `/Applications`의 기존 앱은 자동 삭제하지 않습니다.

아래는 수동 설치 방법입니다.

[Releases](https://github.com/hyunmin-apps/StudyGlass/releases)에서 `StudyGlass-0.1.2-macOS-universal-UNNOTARIZED-preview.dmg`를 받으세요. **동일한 파일이 Apple Silicon과 Intel Mac을 지원합니다. macOS 14 Sonoma 이상이 필요합니다.**

1. DMG를 열고 `Study Glass.app`을 `Applications`로 복사합니다.
2. 앱을 한 번 실행합니다. Apple이 확인할 수 없다는 경고가 나오면 아래 첫 실행 안내를 따릅니다.
3. 바탕화면 우클릭 → **위젯 편집 → Study Glass**에서 하루 목표 또는 주간 목표를 추가합니다.
4. 위젯의 날짜를 눌러 앱을 열고 목표를 확인합니다. 체크 변경은 앱에서 합니다.

Developer ID 서명·Apple 공증 전 **시험 릴리스**입니다. macOS가 다운로드한 앱의 실행을 차단할 수 있습니다. ZIP은 DMG와 같은 앱의 대체 배포 형식입니다. 다운로드 파일의 무결성은 함께 제공하는 `SHA256SUMS.txt`로 확인할 수 있습니다.

### 첫 실행이 차단될 때

현재 배포는 **Apple 공증 전 시험판**입니다. 경고 없는 정식 배포가 아니며 Intel 호환성과는 별개의 문제입니다.

공식 배포 파일을 신뢰하고 실행하려는 경우, 경고에서 **완료** → **시스템 설정 → 개인정보 보호 및 보안 → 보안 → 그래도 열기**를 선택한 뒤 macOS 확인 절차를 진행하세요. [Apple의 공식 안내](https://support.apple.com/102445)를 참고하세요. 관리되는 Mac에서는 허용되지 않을 수 있습니다.

DMG는 **Finder에서 더블클릭**합니다. 터미널에 파일 이름만 입력하는 것은 실행 명령이 아닙니다. ZIP에도 같은 설치 안내를 포함했습니다. ‘손상됨’이나 ‘컴퓨터를 손상시킴’ 경고는 별도로 확인해야 합니다.

[전체 설치 안내](docs/INSTALL.txt) · [배포 오류 분석](docs/distribution-incident.md)

## 기능

- 하루 보기 / 한 주 펼치기 / 이전·다음 주 / 오늘 이동.
- 과목명과 하루 목표 추가. 같은 과목명은 같은 색상으로 표시.
- 미시작 → 학습 → 통과 → 미시작 순서의 체크와 자동 저장.
- 상세 지침을 필요할 때만 펼치는 다크 화면.
- macOS 정식 WidgetKit 위젯: 하루 목표 소·중·대, 주간 목표 대.
- 작은 앱 창·다른 창 위 고정은 정식 위젯과 별도로 제공.

0.1.0에는 **2026년 10월 12~22일 공부 계획 42개**가 예제로 포함됩니다. 주간 목표를 따로 만드는 구조가 아니라, 날짜별 목표를 한 주 단위로 모아 봅니다. 기본 예제는 앱에서 편집·삭제할 수 없고, 직접 추가한 목표는 삭제할 수 있습니다. 기본 계획을 바꾸려면 `Resources/plan.json`을 수정해 다시 빌드합니다.

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
4. 해당 커밋에 버전 태그를 붙이고 `dist/`의 DMG·ZIP·해시·manifest를 GitHub Release에 올립니다.

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
