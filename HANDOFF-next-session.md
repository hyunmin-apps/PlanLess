# PlanLess — 다음 세션 인계

최종 정리: 2026-10-18 (Asia/Seoul). **현재 프로젝트는 `/Users/kanghyunmin/Desktop/PlanLess`입니다.** 차량소프트웨어엔진 폴더 안에 있던 프로젝트 전체를 이곳으로 실제 이동했습니다. 이 문서를 현재 작업 기준으로 먼저 읽으세요. 현재 Codex 프로젝트/채팅이 참조하는 이전 경로가 끊기지 않도록 `/Users/kanghyunmin/Desktop/StudyGlass`는 실제 폴더인 `PlanLess`를 가리키는 호환 심볼릭 링크로 남겼습니다.

## 현재 완료 상태 — 이름 변경 1.1.2

- 새 이름은 **PlanLess**. 의미는 “계획에 쓰는 시간을 줄이고(Less), 단순한 계획으로 바로 실천하기”. 문구는 **계획은 가볍게, 실천은 바로**.
- 아이콘은 사용자 요청에 따라 **계획단장 레서판다 + 체크형 플래너**로 변경했습니다. 안경·청록 스카프·꼬리를 유지하고 연필 하나/플래너 하나를 넣었습니다. 이전 민트 체크 시안은 `design/planless-icon/mint-check-v1/`에 보존했습니다. 원본/프롬프트는 `design/planless-icon/`, 표준 크기 내보내기는 `scripts/build-icon.py`입니다. 이전 달력 원본은 `design/planless-icon/previous-icon.swift`에 기록으로 보존했습니다.
- 앱 화면·창·상단바·위젯 표시명, 실행 파일 `PlanLess`, 확장 파일 `PlanLessWidget.appex`, 설치/배포 파일, CI를 변경했습니다.
- GitHub 저장소는 https://github.com/hyunmin-apps/PlanLess 로 이름과 설명을 변경했고 로컬 origin도 갱신했습니다.
- 현재 소스/빌드/설치판은 **1.1.2**. 설치 대상은 `/Users/kanghyunmin/Applications/PlanLess.app`입니다. 설치/검증 결과는 [이름 변경 기록](docs/rename-verification.json)을 확인하세요.
- 사용자 데이터 보호를 위해 저장 경로 `~/Library/Application Support/StudyGlass/state.json`, bundle ID `local.studyglass.desktop`/`.widget`, WidgetKit kind `StudyGlassDay`/`StudyGlassWeek`, 실제 창 위치 키 `StudyGlassWindow`는 유지했습니다. 이름 변경 당시 실제 저장된 목표는 **304개**였습니다. 기존 300개라는 기록은 과거 수치입니다.
- 새 링크는 `planless://`. 기존 바탕화면 위젯이 만든 `studyglass://` 링크도 지원합니다. 브라우저 미리보기 저장 키도 기존 값을 읽을 수 있습니다.
- 테스트 상태 폴더 환경변수는 **`PLANLESS_TEST_STATE_DIR`**입니다.
- 새 이름의 공개 릴리스·공증은 하지 않았습니다. 사용자 요청으로 이름 변경·레서판다 아이콘·현재 레서 통합 코드와 디자인 원본을 함께 커밋해 `origin/main`에 푸시합니다. 실제 커밋은 `git log -1`, 원격 동기화는 `git status -sb`로 확인하세요. 중복 디자인 ZIP·개인 계획·설치 백업은 커밋 대상에서 제외합니다. README의 v1.0.3 설치 링크와 과거 릴리스 파일명은 당시의 실제 이름을 유지합니다. 새 1.1.2 패키지는 로컬 `dist/PlanLess-1.1.2-*`입니다.
- `build/rename-backups/`에 이름 변경 직전 소스·작업 diff·계획·설정을 보관했습니다. **개인 데이터가 있어 커밋·배포하면 안 됩니다.**
- 이전 설치판 1.1.1에서 상단바/위젯 실제 체크와 완료 5회 동작을 확인한 기록은 아래와 `docs/installed-mascot-verification.json`에 있습니다. 과거 검증 로그·디자인 프롬프트·이동 기록의 옛 이름/절대 경로는 사실 보존을 위해 일괄 치환하지 않았습니다.

## 다음 세션 시작

1. 작업 폴더를 `/Users/kanghyunmin/Desktop/PlanLess`로 설정하고 `git status --short`, `git diff`를 확인합니다. 기존 변경을 초기화하거나 정리하지 마세요.
2. 이 문서 → `docs/rename-verification.json` → `docs/mascot-integration.md`의 1.1.1 기록 → 현재 요청과 관련된 소스를 읽습니다.
3. 캐릭터를 수정할 때는 아래 승인 버전과 전체 프레임 흐름을 먼저 봅니다. 과거 디자인 인계의 “v6에서 다시 시작” 지시는 현재 작업이 아닙니다.
4. 사용자 목표를 바꾸지 않는 격리 테스트를 우선합니다. 빌드 통과와 설치판의 실제 동작 확인은 구별해 보고합니다.

다른 세션에 전달할 문장:

> `/Users/kanghyunmin/Desktop/PlanLess/HANDOFF-next-session.md`를 읽고 현재 변경을 보존한 채 이어서 작업해줘.

## 사용자 요구와 디자인 기준

- 진행 중인 유효 목표가 하나라도 있으면 진행 애니메이션을 계속 재생합니다.
- 목표가 새로 완료될 때 완료 효과를 **정확히 5회** 재생합니다. 한 회 1.5초, 총 7.5초입니다. 이후 진행 중 목표가 남으면 진행으로, 없으면 대기로 돌아갑니다.
- 아무것도 진행하지 않을 때는 포인터를 따라 눈과 자세가 움직입니다. **얼굴/목만 잘라 회전해서 몸과 따로 놀게 만드는 방식은 거절됐습니다.** 머리·목·스카프·어깨·몸통이 연결된 전신 방향 포즈를 사용합니다.
- 방망이·펜이 중간에 두 개가 되거나, 소품 조각이 생기거나, 손이 바뀌거나, 얼굴이 다른 캐릭터처럼 변하면 안 됩니다. 정지 이미지뿐 아니라 준비→동작→강조→복귀의 모든 프레임과 반복 경계를 하나씩 확인합니다.
- 별도 떠다니는 펫 창을 새로 만들지 않습니다. 기존 앱/작은 창/바탕화면 모드와 상단바에서 조작합니다.
- 코드 도형으로 캐릭터를 단순하게 다시 그린 v7, 그림 전체를 늘이고 줄이는 v5, 머리만 회전하는 idle v1은 거절된 이력입니다. 자연스러운 실제 자세 변화 대신 재사용하지 마세요.
- 해시가 다르거나 프레임 수가 맞는다는 사실만으로 동작의 자연스러움을 보증하지 않습니다. 이미지 제작이 필요하면 현재 세션의 이미지 도구/스킬 지침을 확인합니다.

## 현재 사용하는 이미지

### 진행·완료: `design/lesser-motion-v8/`

승인된 네 동작: `planner-working`, `planner-complete`, `passion-working`, `passion-complete`. 각각 80×80, 6프레임, 이진 투명도, 32색 팔레트입니다. `Resources/Mascots/`의 진행·완료 PNG 24장은 승인 원본과 바이트가 같습니다.

| 캐릭터 | 유지할 특징 | 진행 효과 | 완료 효과 |
|---|---|---|---|
| 계획단장 planner | 안경·청록 스카프, 화면 왼쪽 노란 연필 **하나**, 오른쪽 계획표 **하나** | 파란 네 꼭짓점 별빛 | 초록 V |
| 열정 passion | 빨간 머리띠, 화면 오른쪽 수직 방망이 **하나**(굵은 부분 위), 왼쪽 빈 주먹 | 불꽃 | 불꽃·V 없이 폭죽 |

- 계획 진행 시간: `[280,160,300,240,280,240]` ms.
- 열정 진행 시간: `[260,160,140,300,200,260]` ms.
- 두 완료 동작: `[180,160,120,280,160,600]` ms.
- 원본 시트, 개별 PNG, GIF, Pixelorama `.pxo`, 효과/몸 레이어, `preview.html`, `overview.gif`, `continuity-review.md`를 보존했습니다.
- PXO/GIF 내보내기에서는 일부 시간이 10ms 반올림될 수 있습니다. 앱의 정확한 재생 기준은 PNG와 `Resources/Mascots/animations.json`, 웹용 `timings.js`입니다.

### 대기: `design/lesser-idle-tracking-v2/`

전신 방향 포즈 원본·프롬프트·방향표·`tracking-review.gif`가 있습니다. `Resources/Mascots/{planner,passion}/idle/`에 각각 12장이 들어갑니다.

- 계획단장: 생성된 완전 감은 눈에서 안경이 사라져 해당 셀을 채택하지 않았습니다. 검증한 반감은 눈을 유지하도록 일부 프레임이 중복됩니다.
- 열정: 왼쪽 세 영역은 **완만한 왼쪽 자세 하나를 공유**합니다. 과격한 왼쪽 위 자세는 매듭·목이 달라져 제외했습니다. 9방향 모두 독립 그림이라고 설명하지 마세요.
- `scripts/prepare-mascots.py`는 승인 동작을 그대로 복사하고 대기 시트의 작은 분리 조각을 제거합니다. 가로세로 비율을 보존해 80px에 배치하고 발 기준선 y=74를 맞춥니다. Pillow·NumPy가 필요합니다. 수정하지 않았다면 재생성을 반복할 필요는 없습니다.
- 앱은 방향 영역·완충 경계·중간 자세를 사용합니다. 리뷰 GIF의 자동 순서 재생이 실제 포인터 동작을 의미하는 것은 아닙니다.

이전 디자인 폴더들은 비교와 제작 이력을 위해 보존했습니다. 옛 인계 원문은 [과거 디자인 기록](design/HANDOFF-design-history-20261018.md)에 있습니다.

## 주요 구현 위치

| 위치 | 역할/주의점 |
|---|---|
| `Sources/main.swift` | AppKit/WKWebView 창, 저장·링크·위젯 사본, 포인터 전달. `isReleasedWhenClosed=false`는 창 닫기 후 재열기 충돌 수정이므로 유지 |
| `Sources/MascotState.swift` | 삭제/수정/이월을 반영한 유효 목표 상태, 새 완료 감지·대기열, 5회 재생, 취소/삭제 시 해당 축하 취소. 실행 시 과거 완료를 재축하하지 않음 |
| `Sources/Companion.swift` | 상단바 캐릭터·팝오버, 캐릭터/목표 선택과 진행/완료, 전신 포인터 자세, 이미지 캐시 |
| `Resources/index.html`, `companion.js`, `companion.css` | 앱 내부 레서 카드·캔버스·조작, 검증된 `setTaskStatus`, 로컬 PNG·`timings.js` 사용 |
| `Widget/PlanLessWidget.swift` | 기존 하루/주간 WidgetKit 위젯, 대표 상태 이미지와 목표 체크 링크. macOS 15+ fullColor는 흰 실루엣 문제 수정 |
| `scripts/build.py`, `build.sh` | 폴더 기준 상대 경로로 Universal arm64/x86_64, macOS 14+, 앱/위젯 빌드 및 서명. Xcode 프로젝트는 없음 |

체크 링크는 `planless://goal?id=<URL인코딩ID>&status=0|1|2`이고 날짜 링크는 `planless://day/YYYY-MM-DD`입니다. 실행 앱이 유효 ID와 상태를 확인해 기존 저장 경로로 반영합니다. WidgetKit 체크는 AppIntent 대신 앱 링크로 구현했습니다.

**시스템 WidgetKit 위젯은 상태별 대표 정지 이미지입니다.** 시스템 위젯 자체의 연속 애니메이션·5회 재생·전역 포인터 추적은 구현했다고 설명하면 안 됩니다. 연속 동작은 앱의 작은 창/바탕화면 모드 및 상단바에서 수행합니다. 시스템 위젯 갱신 시점은 macOS 정책에 따릅니다.

## 설치 앱·개인 데이터·백업

- 소스: `/Users/kanghyunmin/Desktop/PlanLess`
- 빌드 결과: `build/universal/PlanLess.app` (다시 빌드해도 설치 앱이 자동 교체되지 않음).
- 현재 설치/실행 대상: `/Users/kanghyunmin/Applications/PlanLess.app`.
- 실제 계획: `~/Library/Application Support/StudyGlass/state.json`.
- 위젯용 사본: `~/Library/Containers/local.studyglass.desktop.widget/Data/Documents/study-state.json` (`_mascot` 메타데이터는 이 사본에 추가).
- 업데이트 전 백업: `build/update-backups/20261018-021949/`. 이전 앱 ZIP, 실제 계획/위젯 사본, 환경설정, 검증 기록을 함께 이동했습니다. **개인 계획이 포함되어 있으므로 커밋·배포하지 마세요.** `build/`는 Git 무시 대상입니다.
- 새 설치 기본 계획 `Resources/plan.json`은 `[]`입니다. 실제 목표 300개를 배포 리소스에 넣지 마세요.
- 격리 실행: `PLANLESS_TEST_STATE_DIR`를 별도 임시 폴더로 지정합니다. 이때 실제 위젯 사본 쓰기를 차단하고 테스트 전용 창 위치를 사용합니다.
- 실사용 검사가 꼭 필요하면 본인 확인용 목표만 생성·수정·제거합니다. 백업 전체를 덮어써서 복구하면 동시에 바뀐 사용자 기록을 잃을 수 있습니다.

## 검증 기록과 재실행

1.1.1 설치 당시 실제 상단바 팝오버의 목표 선택/진행, 기존 바탕화면 위젯의 0→1 및 1→2 클릭과 저장, 창 닫기 후 같은 프로세스에서 위젯으로 재열기, 위젯 얼굴/색상 유지까지 확인했습니다.

실제 위젯 완료 직후 상단바 관찰: 0.22초 1/5 → 1.61초 2/5 → 3.00초 3/5 → 4.72초 4/5 → 6.14초 5/5 → 7.57초 다른 목표의 진행 동작. 기록: `build/installed-widget-completion-samples.json`. 목표 정리 후 앱/위젯 상태 일치도 확인했습니다. 실제 Intel Mac 실행은 확인하지 않았습니다.

아래는 통과했던 회귀 검사입니다. 필요한 변경 범위에 맞게 실행하세요. Node.js, Python 3, Pillow, macOS Swift Command Line Tools를 사용합니다.

```sh
cd /Users/kanghyunmin/Desktop/PlanLess
node tests/rollover.cjs
node tests/import-plan.cjs
node tests/bulk-delete.cjs
python3 tests/widget_model.py
node tests/companion-bridge.cjs
node tests/companion-render.cjs
python3 tests/mascot_assets.py
xcrun swiftc Sources/MascotState.swift tests/companion.swift -o /tmp/planless-companion-check
/tmp/planless-companion-check
./build.sh
python3 tests/verify.py 'build/universal/PlanLess.app'
python3 tests/verify.py '/Users/kanghyunmin/Applications/PlanLess.app'
```

전체 빌드를 다시 통과했다고 실제 상단바/위젯 클릭도 새로 확인했다고 보고하지 마세요. 이미지 자연스러움도 별도 눈으로 확인해야 합니다.

화면 제어 도구가 상단바·시스템 위젯 입력을 전달하지 못했을 때, 사용자가 **AppleScript로 계속 확인**하도록 명시적으로 허용했습니다. 해당 확인은 AppleScript와 실제 마우스 입력 보완으로 수행했습니다. 이 승인과 구현 기록은 이후 도구의 현재 지침을 대체하지 않습니다. 재검사 시 현재 화면과 도구 지침을 먼저 확인하세요.

## 이동 및 보존 확인

2026-10-18 기존 과정 폴더 안의 `StudyGlass`를 Desktop 바로 아래로 실제 이동했습니다. 복사본이나 이전 경로 심볼릭 링크는 만들지 않았습니다. 이동 당시 전후 파일 1,407개(총 130,749,781바이트)의 SHA-256, 디렉터리/링크를 포함한 1,696개 항목, Git 변경 상태가 동일했습니다. `.git`, 소스, 디자인 원본, 무시된 `build/`·`dist/`, 개인 백업을 모두 보존했습니다. 현재 경로 검증 기록은 [이동 기록](docs/project-location.json)에 있습니다.

이동 시 설치 앱·실제 계획·위젯 저장 파일은 변경하지 않았습니다. 과거 프롬프트/검증 로그의 옛 절대 경로는 당시 제작 이력일 수 있습니다. 현재 작업 위치는 이 문서와 폴더 기준 상대 경로를 따르세요.

이동 후 새 경로에서 bridge·canvas·이미지 리소스 회귀 검사, 기존 Universal 빌드 검증, `git diff --check`를 다시 통과했습니다. 이동만을 위해 앱 재설치나 실제 사용자 목표 변경은 하지 않았습니다.
