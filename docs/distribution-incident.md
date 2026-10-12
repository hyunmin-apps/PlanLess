# 2026-10-12 첫 설치 차단 분석

공개 v0.1.0 ZIP을 다시 다운로드해 검사했습니다.

- 앱과 위젯의 Universal 아키텍처 포함 여부와 코드 서명 구조 검사는 별개입니다.
- 실제 앱 서명은 `Signature=adhoc`, `TeamIdentifier=not set`입니다.
- `spctl --assess --type execute`는 `rejected`를 반환했습니다.
- `stapler validate`는 공증 티켓이 없다고 보고했습니다.
- 따라서 제출된 스크린샷의 “Apple이 악성 코드가 없음을 확인할 수 없음” 경고는 Developer ID 및 공증 부재와 일치합니다.
- 터미널의 `command not found`는 DMG 이름을 명령어로 입력한 별도 오류입니다.

기존 CI는 바이너리를 직접 실행하고 8초 생존을 확인했습니다. 이는 다운로드한 앱이 Finder/Gatekeeper를 통해 열리는지를 검증하지 않습니다. 이 구분이 설치 안내에 충분히 반영되지 않았습니다.

0.1.1은 공증을 완료한 수정판이 아니라 설치 안내와 배포 검사를 보완한 시험판입니다. DMG/ZIP 양쪽에 설치 안내를 넣고 파일명에도 미공증 상태를 표시했습니다. manifest에 Gatekeeper의 실제 평가를 기록하며, 공증 배포 모드는 Developer ID 서명·공증 티켓·Gatekeeper 허용을 모두 요구합니다. 시스템 보안 설정을 자동으로 해제하거나 격리 속성을 제거하지 않습니다.

경고 없이 설치되는 정식 배포는 Developer ID 인증서와 Apple 공증 인증 정보가 준비된 뒤 진행해야 합니다. 현재 Mac에서 유효한 코드 서명 인증서는 0개이며 저장소 Actions의 배포 비밀 정보도 등록되어 있지 않았습니다.

참고: [Apple 앱 열기 안내](https://support.apple.com/102445), [Apple 공증 과정](https://developer.apple.com/documentation/security/customizing-the-notarization-workflow).
