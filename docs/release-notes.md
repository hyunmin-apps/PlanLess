**Apple 공증 전 시험판입니다. 첫 실행 시 macOS가 차단할 수 있습니다. 0.1.1에서도 공증 경고 자체는 사라지지 않습니다.**

## 설치

1. `StudyGlass-0.1.1-macOS-universal-UNNOTARIZED-preview.dmg`를 다운로드하고 **Finder에서 더블클릭**합니다.
2. `Study Glass.app`을 Applications에 복사하고 실행합니다.
3. “Apple이 악성 코드가 없음을 확인할 수 없음” 경고가 나오면 **완료**를 누릅니다. 공식 파일을 신뢰하고 실행을 원할 때만 **시스템 설정 → 개인정보 보호 및 보안 → 보안 → 그래도 열기**를 선택하고 확인 절차를 진행합니다.
4. 바탕화면 우클릭 → 위젯 편집 → Study Glass에서 위젯을 추가합니다.

ZIP에도 같은 앱과 설치 안내가 들어 있습니다. DMG 파일명은 터미널 명령어가 아닙니다. [Apple 공식 안내](https://support.apple.com/102445).

## 이번 변경

- DMG와 ZIP 모두 첫 실행 안내 포함. 별도 `INSTALL.txt` 제공.
- 파일명에 `UNNOTARIZED-preview` 표시, manifest에 실제 Gatekeeper 평가 기록.
- VERSION과 앱 버전 불일치 시 오래된 앱 패키징 중단.
- Developer ID와 공증 인증 정보가 있을 때 사용할 서명·공증 경로 추가. 미공증 앱은 공증 배포 모드에서 거부.

## 지원과 한계

macOS 14 이상, Apple Silicon 및 Intel 공용. 앱 기능과 기존 데이터 경로는 유지합니다. 업데이트 전 `~/Library/Application Support/StudyGlass/state.json`을 복사해 백업할 수 있습니다.

아키텍처 CI와 실제 다운로드 첫 실행 검증은 다릅니다. Developer ID 서명·공증은 아직 완료하지 못했습니다. 최소 지원 OS와 실제 Intel Mac의 위젯 UI 확인도 별도 필요합니다. [원인 분석](https://github.com/hyunmin-apps/StudyGlass/blob/main/docs/distribution-incident.md).
