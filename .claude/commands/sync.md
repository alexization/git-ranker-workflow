---
description: 서브모듈 PR 머지 상태를 확인해 gitlink를 갱신하고 추적 이슈를 닫는다
argument-hint: <추적 이슈 번호 또는 URL (선택)>
---

`workflow-sync` 스킬을 먼저 로드해 그 절차를 그대로 따르라.

대상 추적 이슈: $ARGUMENTS (없으면 열린 `tracking` 라벨 이슈를 조회해 선택)

1. 추적 이슈를 읽어 연결된 서브모듈 이슈/PR 머지 상태를 gh로 확인한다.
2. 머지된 서브모듈만 gitlink를 갱신한다(destructive 금지 규약 준수).
3. `.gitmessage.ko.txt` 형식으로 gitlink 커밋 초안을 만든다. push는 사용자 요청 시만.
4. 추적 이슈 체크박스를 갱신하고, 모두 완료되면 사용자 확인 후 닫는다.
