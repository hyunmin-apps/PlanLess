# 개발 · 테스트 · 배포

[← PlanLess 소개로 돌아가기](../README.md)

## 빌드

macOS, Xcode Command Line Tools 또는 Xcode, Python 3이 필요합니다. 앱 빌드는 Apple 시스템 프레임워크를 사용합니다.

```sh
./build.sh                       # arm64 + x86_64 Universal
./build.sh --arch arm64          # Apple Silicon
./build.sh --arch x86_64         # Intel
python3 tests/verify.py 'build/universal/PlanLess.app'
```

앱과 WidgetKit 확장을 각각 컴파일하고 위젯 → 앱 순서로 서명합니다. `Widget/build-widget.sh`는 같은 빌드를 호출합니다. 빌드는 설치 앱을 자동 교체하지 않습니다.

## 검사

Node.js와 Python 3이 필요하며 이미지 검사는 Pillow를 사용합니다.

```sh
node tests/import-plan.cjs
node tests/bulk-delete.cjs
node tests/rollover.cjs
python3 tests/widget_model.py
node tests/companion-bridge.cjs
node tests/companion-render.cjs
python3 tests/mascot_assets.py
xcrun swiftc Sources/MascotState.swift tests/companion.swift -o /tmp/planless-companion-check
/tmp/planless-companion-check
```

격리 실행은 `PLANLESS_TEST_STATE_DIR`에 임시 상태 폴더를 지정합니다. 실제 위젯 저장 파일은 쓰지 않습니다. 자동 검사와 실제 상단바·시스템 위젯 클릭 검증은 구별합니다.

## 디자인과 문서 리소스

- `python3 scripts/build-icon.py`: 승인된 레서판다 플래너 아이콘 원본에서 PNG·표준 크기·ICNS 내보내기.
- `python3 scripts/build-readme-assets.py`: 승인된 앱 프레임을 그대로 포함한 README의 밝은/어두운 소개 일러스트 생성.
- `python3 scripts/prepare-mascots.py`: 승인 동작을 복사하고 대기 포즈를 정리. Pillow·NumPy가 필요합니다.

README는 GitHub에서 사용할 수 있는 `<details>`, 섹션 링크, 이미지와 GIF로 구성했습니다. 소개 일러스트는 예시 할 일을 보여주며 실제 앱 스크린샷이 아닙니다. SVG의 모션은 `prefers-reduced-motion`을 따릅니다. 캐릭터 GIF는 펼쳐 볼 수 있는 완료/대기 소개에도 사용합니다.

## 배포

1. `VERSION`과 `CHANGELOG.md`를 갱신합니다.
2. Universal 빌드와 검증 후 `python3 scripts/package.py`를 실행합니다.
3. Apple Silicon·Intel CI 결과와 `python3 tests/installer.py dist/*-UNNOTARIZED-preview.zip "$(cat VERSION)"`을 확인합니다.
4. 해당 커밋에 버전 태그를 붙이고 설치 스크립트와 앱 ZIP만 공개 릴리스합니다. DMG·해시·manifest는 로컬 검증용입니다.

현재 공개 배포 워크플로는 수동 실행이며 공증 전 시험판을 만듭니다. README 변경이나 일반 푸시가 새 설치판을 공개하지는 않습니다.

Developer ID 인증서와 Keychain의 notarytool 인증 프로필이 준비된 경우:

```sh
python3 scripts/notarize.py --identity 'Developer ID Application: NAME (TEAMID)' --keychain-profile planless-notary
```

이 경로는 hardened runtime·timestamp 서명, 공증, 티켓 부착, Gatekeeper 검사와 DMG 공증을 수행합니다. 실패하면 패키징을 중단합니다. 실제 Apple 공증 성공은 아직 검증하지 않았습니다.

## 구현 위치

| 위치 | 역할 |
| --- | --- |
| `Sources/main.swift` | macOS 창·저장·위젯 전달·URL 연결 |
| `Sources/Companion.swift` | 상단바 레서·목표 조작·포인터 방향 |
| `Sources/MascotState.swift` | 목표 상태와 완료 축하 대기열 |
| `Resources/index.html`, `companion.js/css` | 날짜별·주간 UI와 앱 내부 레서 |
| `Resources/plan.json` | 빈 기본 계획 |
| `Widget/PlanLessWidget.swift` | 정식 macOS 위젯 |
| `design/planless-icon/` | 승인 아이콘과 제작 기록 |

[검증 기록](verification.md) · [레서 통합](mascot-integration.md) · [로컬 인계](../HANDOFF-next-session.md)

날짜 중심 사용 흐름은 [todo mate](https://www.todomate.net/)와 [Things](https://culturedcode.com/things/features/)를 참고했습니다. 해당 서비스의 리소스는 포함하지 않습니다.
