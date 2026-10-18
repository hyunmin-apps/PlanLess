# 레서 · 24프레임 모션 시안

대기는 기존 디자인을 유지하고 진행 중·완료를 각각 24프레임으로 확장한 편집용 픽셀 애니메이션입니다. 앱·위젯에 적용된 릴리스는 아닙니다.

`preview.html`은 파일 하나만 열어도 동작합니다. 상태 선택, 정지, 프레임 탐색, 처음부터 재생을 지원합니다. 진행 중은 반복하고 완료는 한 번 재생한 뒤 멈춥니다. GIF는 비교 확인을 위해 반복 재생합니다.

## 구성
- `planner-idle`, `passion-idle`: 기존 대기 디자인, 4프레임
- `planner-working`: 파란 네 꼭짓점 별 눈빛과 계획표 체크
- `passion-working`: 불꽃과 주먹 응원
- `planner-complete`: 체크 동작과 회전하는 체크 효과
- `passion-complete`: 불꽃 없는 폭죽과 점프

각 폴더의 `.pxo`를 Pixelorama로 열면 모든 프레임을 편집할 수 있습니다. 프레임마다 캐릭터와 효과가 합쳐진 단일 래스터 레이어입니다. PNG 시트·JSON·개별 PNG·GIF·확대 GIF도 포함했습니다.

실사용 PNG는 64×64px, 애니메이션별 최대 48색, 투명/불투명 알파입니다. 진행 중·완료는 12fps 기준 약 2초입니다. GIF의 시간 단위 제한으로 재생 길이에 미세한 차이가 있습니다. 상세 검증은 manifest.json을 확인하세요.

## 제작 및 참고
내장 이미지 생성 도구로 연속 포즈를 제작하고 FFmpeg로 저해상도·팔레트·알파를 정리했습니다. Pixelorama 1.2.3에서 실제 PXO를 읽어 GIF와 시트를 내보냈습니다. AI 보조 2D 애니메이션 시안으로, 리깅된 3D 모델이나 전 프레임 수작업 그림이 아닙니다. 픽셀 단위 위치와 소품 형태는 앱 적용 전에 추가 정리할 수 있습니다.

행동 참고: Pixar in a Box — Squash and stretch (도약 전 준비 동작, 눌림·늘어남)
https://www.khanacademy.org/computing/pixar/animate/ball/v/animate-4

편집기: https://pixelorama.org/
프롬프트: prompts.json
