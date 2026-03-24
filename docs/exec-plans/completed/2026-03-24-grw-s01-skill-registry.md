# 2026-03-24-grw-s01-skill-registry

- Issue ID: `GRW-S01`
- GitHub Issue: `#6`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-s01-skill-registry`
- Task Slug: `2026-03-24-grw-s01-skill-registry`

## Problem

workflow 저장소에는 project skill의 저장 위치, naming 규칙, 지원 파일 규칙이 아직 없다. 이 상태에서는 이후 skill을 추가할 때마다 형식과 증거 기준이 흔들리고, 병렬 에이전트 운영에서도 같은 작업을 반복 설명해야 한다.

## Why Now

`GRW-S02`, `GRW-S03`, `GRW-S04`는 모두 `skills/` 아래에 새 skill을 추가하는 작업이다. 먼저 registry와 authoring 규칙을 고정해야 후속 skill을 같은 기준으로 검토하고 확장할 수 있다.

## Scope

- `skills/` 디렉터리 추가
- `skills/README.md`에 registry 구조, naming 규칙, 지원 디렉터리 규칙 정리
- `skills/authoring-rules.md`에 최소 authoring 규칙 정리
- `_template/` 없이 진행한다는 현재 결정을 source of truth 문서에 반영
- `GRW-S01` 실행/완료 기록 남기기

## Non-scope

- 실제 ranking, batch, reliability skill 본문 작성
- Playwright, PromQL, LogQL 쿼리 추가
- skill용 스크립트나 자동화 도구 추가

## Write Scope

- `skills/`
- `docs/product/`
- `docs/exec-plans/`

## Outputs

- `skills/README.md`
- `skills/authoring-rules.md`
- `docs/product/harness-roadmap.md`
- `docs/product/work-item-catalog.md`
- `GRW-S01` 실행/완료 기록

## Verification

- `find skills -maxdepth 2 -type f | sort`
  - 결과: `skills/README.md`, `skills/authoring-rules.md` 두 문서만 생성된 것을 확인했다.
- `cat skills/README.md`
  - 결과: 기본 구조를 `skills/<skill-name>/SKILL.md`로 고정하고, 지원 디렉터리는 각 skill 폴더 아래 선택 사항으로 두는 규칙을 확인했다.
- `cat skills/authoring-rules.md`
  - 결과: 고정 템플릿 없이도 각 skill이 다뤄야 할 최소 항목과 review checklist를 확인했다.
- `rg -n "GRW-S01|authoring 규칙|skills/authoring-rules.md" docs/product skills docs/exec-plans/completed/2026-03-24-grw-s01-skill-registry.md`
  - 결과: `GRW-S01` 명칭과 산출물이 roadmap, catalog, skill 문서, 완료 기록에 일관되게 반영된 것을 확인했다.
- `rg -n "_template" docs/product skills`
  - 결과: `docs/product/`와 `skills/` 아래 source of truth 기준 문서에는 `_template` 언급이 남지 않았다.

## Evidence

문서 전용 Issue라 브라우저, 로그, 메트릭 artifact는 필수는 아니다. 대신 검증 명령 결과와 갱신된 source of truth 문서 경로를 exec plan에 남긴다.

## Risks or Blockers

- 기존 역사 문서인 `docs/plans/git-ranker-harness-issue-pr-roadmap.md`에는 `_template/` 언급이 남아 있다. 이 문서는 참고용 이관 전 문서이므로 이번 Issue 범위에서는 유지했다.
- skill 구조를 과하게 고정하지 않기 위해 샘플 템플릿 대신 coverage 기준만 남겼다. 후속 작업에서 이 기준이 너무 느슨하다고 판단되면 별도 Issue로 보완해야 한다.

## Next Preconditions

- `GRW-S02`: coordination skill 3종 작성
- `GRW-S03`: ranking harness execution skill 작성
- `GRW-S04`: reliability/batch skill 작성

## Docs Updated

- `skills/README.md`
- `skills/authoring-rules.md`
- `docs/product/harness-roadmap.md`
- `docs/product/work-item-catalog.md`
- `docs/exec-plans/completed/2026-03-24-grw-s01-skill-registry.md`

## Skill Consideration

이번 Issue는 개별 skill을 추가하는 작업이 아니라 skill authoring 기준을 정하는 작업이다. 따라서 새 project skill 본문은 만들지 않고, 후속 skill들이 같은 기준으로 추가될 수 있는 규칙만 남긴다.
