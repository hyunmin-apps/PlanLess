# 설치와 내 기록 관리

[← PlanLess 소개로 돌아가기](../README.md)

## 먼저 버전 확인

- **현재 소스·로컬 설치판: PlanLess 1.1.2.** 새 이름과 레서판다 플래너 아이콘을 사용합니다.
- **현재 공개 설치판: Study Glass 1.0.3.** 이름 변경 전 버전입니다. 새 이름의 설치 파일은 아직 공개 릴리스하지 않았습니다.

이미 최신 로컬 설치판을 쓰고 있다면 이전 공개 설치기로 덮어쓰지 마세요. 최신 소스는 [빌드 안내](development.md)로 실행할 수 있습니다.

## 기존 공개 설치판 받기

공식 [v1.0.3 릴리스](https://github.com/hyunmin-apps/PlanLess/releases/tag/v1.0.3)에서 `StudyGlass-1.0.3-Install.command` 하나를 받습니다. ZIP은 설치 스크립트가 자동으로 내려받습니다. GitHub의 `Source code`는 개발용 소스입니다.

받은 파일을 다운로드 폴더에 두고 아래 한 줄 전체를 실행하세요.

```bash
/bin/bash "$HOME/Downloads/StudyGlass-1.0.3-Install.command"
```

`$HOME`은 현재 사용자 폴더를 가리킵니다. 파일이 다른 폴더에 있거나 파일명 뒤에 `(1)`이 붙었다면 실제 경로에 맞춰야 합니다. `/bin/bash`만 따로 실행하지 말고 파일 경로까지 한 줄로 실행하세요.

안내를 읽고 `y`를 입력하면 공식 ZIP의 고정 SHA-256과 앱 서명 구조를 확인한 뒤 `~/Applications`에 설치합니다. 해당 앱에만 다운로드 격리 해제를 적용하며 Mac 전체 보안 설정은 변경하지 않습니다. 관리자 암호는 필요하지 않습니다.

**Apple 공증 전 시험판**입니다. 이 절차는 공증을 대신하지 않습니다. `/Applications`에 수동 설치한 다른 앱은 자동 삭제하지 않습니다.

## 업데이트 전

실행 중인 같은 앱은 자동 종료하며, 응답하지 않으면 강제 종료할 수 있습니다. 편집 중인 내용은 먼저 저장하세요. 설치기는 이전 앱을 ZIP으로 백업하고 실패 시 복구합니다. 직접 추가·가져온 기록은 유지합니다.

현재 소스의 PlanLess 설치기는 이전 Study Glass 설치 이름을 확인해 `PlanLess.app`으로 교체합니다. 앱과 위젯의 영구 식별자를 유지해 기존 설정과 위젯 배치를 이어갑니다. 같은 식별자의 두 설치가 함께 있는 경우 먼저 정리하도록 중단합니다.

## 위젯 추가

바탕화면 우클릭 → **위젯 편집 → 앱 이름**에서 하루 목표 또는 주간 목표를 고릅니다. 새 이름 설치판은 PlanLess, 이전 공개판은 Study Glass로 표시됩니다.

시스템 위젯은 대표 정지 이미지를 표시하며 갱신 시점은 macOS가 정합니다. 1.1.2 소스의 위젯 체크는 앱을 열어 목표 상태를 변경합니다. 연속 애니메이션과 포인터 추적은 앱·작은 창·상단바에서 동작합니다.

<a name="data"></a>

## 저장 위치와 백업

- 목표·체크·메모: `~/Library/Application Support/StudyGlass/state.json`
- 위젯용 사본: `~/Library/Containers/local.studyglass.desktop.widget/Data/Documents/study-state.json`

앱을 종료하고 `state.json`을 다른 위치에 복사하면 백업할 수 있습니다. 실제 사용자 기록을 저장소나 설치 파일에 넣지 마세요. 배포용 `Resources/plan.json`은 빈 배열입니다.

이름 변경 후에도 기록과 환경설정·배치된 위젯을 유지하기 위해 기존 저장 경로, `local.studyglass.desktop`/`.widget`, WidgetKit kind를 유지합니다. 새 `planless://`와 기존 `studyglass://` 링크를 모두 지원합니다.

앱을 삭제하려면 바탕화면 위젯을 제거하고 앱을 휴지통으로 옮기세요. 사용자 기록은 자동으로 삭제하지 않습니다.
