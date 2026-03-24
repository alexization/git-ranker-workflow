# Harness Roadmap

이 문서는 하네스 엔지니어링 적용 순서와 상위 고정 결정을 정리한 현재 기준 로드맵이다.

## 목표

1. AI Agent가 읽을 수 있는 문서와 계약을 먼저 고정한다.
2. 첫 하네스 대상을 `랭킹 조회`로 고정해 작은 성공 루프를 만든다.
3. 반복될 가능성이 높은 작업은 이후 `SKILL`로 승격 가능한 형태로 남긴다.

## 이번 계획의 고정 결정

- 준비 수준: `균형형`
- 첫 하네스 축: `랭킹 조회`
- source of truth 위치: `workflow 중심`
- 1단계 런타임 방식: `하이브리드`

## 권장 실행 순서

1. `GRW-01` workflow skeleton과 문서 규칙 만들기
2. `GRW-02` 현재 readiness 기준선 문서화
3. `GRW-S01` skill registry와 authoring 규칙 정의
4. `GRW-S05` TDD red-green-refactor skill pack v1
5. `GRB-01` 백엔드 OpenAPI 계약 생성 기반 만들기
6. `GRW-03` 백엔드 도메인/운영 문서 수집
7. `GRC-01` 프런트엔드 계약 타입 단일화
8. `GRW-04` 프런트엔드 구조/데이터 흐름 문서 수집
9. `GRW-S02` core planning/parallel-agent skill pack v1
10. `GRB-02` 백엔드 검증 루프 hardening
11. `GRC-02` 프런트 lint debt 1차 정리
12. `GRC-03` 프런트 build/runtime 하네스 친화화
13. `GRW-05` workflow 표준 검증 런타임 만들기
14. `GRB-03` 랭킹 조회용 결정적 seed 데이터 지원
15. `GRC-04` 랭킹 조회 Playwright 하네스 도입
16. `GRW-06` 랭킹 조회 증거 수집 루프 추가
17. `GRW-S03` ranking harness execution skill pack v1
18. `GRW-07` 문서/계약/플랜 freshness 가드레일 추가
19. `GRW-08` 배지 하네스 계획 문서 작성
20. `GRW-09` 배치 하네스 계획 문서 작성
21. `GRW-S04` reliability/batch skill pack v1

## 바로 다음에 추천하는 작업

1. `GRW-01`
2. `GRW-S01`
3. `GRW-S05`
4. `GRC-01`

`GRW-01`을 먼저 권장하는 이유는 이후 모든 문서, exec plan, skill, evidence를 놓을 자리를 먼저 만들어야 하기 때문이다.

`GRW-S05`를 이어서 권장하는 이유는 이후 backend/client 기능 구현 작업을 TDD turn 기준으로 반복 재사용할 수 있기 때문이다.

## 사용 원칙

- 작업 상세와 write scope는 [work-item-catalog.md](work-item-catalog.md)를 본다.
- 실제 착수 시에는 `docs/exec-plans/active/`에 issue별 실행 문서를 먼저 만든다.
