---
description: 요구사항을 FE/BE 작업으로 분해해 각 서브모듈에 GitHub 이슈를 생성
argument-hint: <요구사항 설명>
---

`workflow-dispatch` 스킬을 먼저 로드해 그 절차를 그대로 따르라.

요구사항: $ARGUMENTS

1. Plan 모드 + AskUserQuestion으로 요구사항을 FE(git-ranker-client) / BE(git-ranker) 작업 범위로 분해한다. 상세 구현 계획은 세우지 않고 범위만 나눈다.
2. 각 이슈 본문 초안과 gh 명령을 미리보기로 제시하고 사용자 승인을 받는다.
3. 승인 후 gh로 루트 추적 이슈 + 해당 서브모듈 이슈를 생성하고 상호 링크한다.
