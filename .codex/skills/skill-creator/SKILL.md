---
name: skill-creator
description: 이 저장소의 project-local skill을 새로 만들거나 기존 skill을 Claude/Anthropic 모범 사례에 맞게 다시 쓸 때 사용한다. 새 skill의 trigger description, instruction 구조, bundled resource 구성을 설계해야 하거나 기존 skill을 전면 리팩터링해야 할 때 이 skill을 먼저 사용한다.
---

# Skill Creator

새 skill을 만들고 기존 skill을 개선하는 방법을 정리한다.

이 skill의 목적은 문서를 하나 더 추가하는 것이 아니다. 모델이 필요한 순간에 skill을 잘 발견하고, SKILL.md를 과하게 읽지 않고, 실제 사용자 프롬프트에서 더 일관되게 동작하도록 skill bundle을 설계하는 것이다.

## 언제 사용하나

다음 상황에서 이 skill을 사용한다.

- 새 skill을 처음 만들 때
- 기존 skill을 Claude/Anthropic 모범 사례 기준으로 다시 쓸 때
- `description`이 약해서 skill trigger 품질이 낮을 때
- 메모 수준 규칙을 reusable skill로 올릴 때
- bundled resource가 필요한지, 필요 없다면 왜 없는지가 설계 이슈일 때

사소한 오탈자 수정처럼 구조와 trigger 판단이 전혀 바뀌지 않는 경우에는 이 skill이 과하다.

## 좋은 skill의 기준

좋은 skill은 아래 조건을 만족한다.

- 무엇을 하는지와 언제 써야 하는지가 `description`에서 바로 드러난다.
- SKILL.md 본문은 핵심 workflow와 판단 기준만 남기고 불필요하게 길지 않다.
- 상세 문서, 스크립트, 템플릿은 필요할 때만 따로 둔다.
- 실제 사용자 프롬프트와 비슷한 예시로 빠르게 검토할 수 있다.

## 핵심 원칙

### 1. 간결함이 핵심이다

모델은 이미 많은 일반론을 알고 있다. SKILL.md에는 이 skill에서만 필요한 판단 기준과 반복 workflow만 남긴다.

줄여야 하는 것:

- 교과서적인 설명
- canonical doc를 길게 다시 적은 문단
- 결과를 바꾸지 않는 긴 예시

남겨야 하는 것:

- trigger에 직접 영향을 주는 표현
- 실패를 줄이는 workflow
- resource를 언제 읽고 언제 안 읽는지에 대한 기준

### 2. `description`은 trigger surface다

`description`은 단순 요약이 아니라 "이 skill을 언제 써야 하는지"를 모델에게 알려주는 첫 번째 표면이다.

약한 예:

```yaml
description: 문서 작업을 도와준다.
```

강한 예:

```yaml
description: 이 저장소의 project-local skill을 새로 만들거나 기존 skill을 Claude/Anthropic 모범 사례에 맞게 다시 쓸 때 사용한다. 새 skill의 trigger description, instruction 구조, bundled resource 구성을 설계해야 하거나 기존 skill을 전면 리팩터링해야 할 때 이 skill을 먼저 사용한다.
```

좋은 `description`은 아래를 함께 담는다.

1. 무엇을 하는지
2. 언제 트리거되어야 하는지
3. 사용자가 실제로 말할 법한 인접 표현

이 저장소처럼 본문이 한국어인 pack에서는 `description`도 한국어로 맞추는 편이 낫다. 다만 말투는 1인칭 도움말보다 중립적인 동작 설명에 가깝게 쓴다.

### 3. 자유도를 맞게 둔다

모든 skill을 같은 강도로 통제할 필요는 없다.

- 높은 자유도: 여러 접근이 가능하고 heuristic이 중요한 작업
- 중간 자유도: 선호하는 패턴은 있지만 출력이 상황에 따라 달라지는 작업
- 낮은 자유도: 순서가 중요하거나 반복 구현 비용이 큰 작업

절벽 사이의 좁은 다리라면 가드레일을 강하게 두고, 열린 들판이라면 모델이 판단할 여지를 남긴다.

### 4. Progressive disclosure를 사용한다

SKILL.md는 entrypoint다. 모든 세부사항을 한 파일에 몰아넣지 않는다.

- `SKILL.md`: trigger, 핵심 workflow, 판단 기준
- `references/`: 길고 상세한 참고 문서
- `scripts/`: 반복되는 결정론적 작업
- `assets/`: 템플릿, boilerplate, 재사용 파일

추가 자산은 "있으면 좋아 보인다"가 아니라 "반복 사용에서 실제로 이득이 있다"는 근거가 있을 때만 만든다.

### 5. 실제 프롬프트로 검토한다

초안만으로 끝내지 않는다. 실제 사용자 요청과 비슷한 2~3개의 프롬프트를 떠올려 아래를 확인한다.

- 이 `description`이 실제로 trigger될 것 같은가
- 본문이 너무 막연하거나 너무 빡빡하지 않은가
- bundled resource가 진짜 필요한가

### 6. 레거시 resource를 재분류한다

기존 skill pack을 리팩터링할 때는 예전 디렉터리 이름을 그대로 유지하지 않는다. 먼저 "이 파일이 실제로 무엇을 위해 존재하는가"를 보고 다시 분류한다.

- 최종 출력에 복사하거나 수정해서 쓰는 템플릿이면 `assets/`
- 작업 중 읽어야 하는 checklist, schema, 긴 참고 문서면 `references/`
- 반복해서 실행하는 deterministic helper면 `scripts/`
- 실제 반복 가치가 없다면 별도 파일로 두지 말고 SKILL.md에 흡수한다

## 작성 순서

명확한 이유가 없다면 아래 순서를 따른다.

### 1. 의도와 사용 예시를 고정한다

먼저 아래 질문에 답한다.

1. 이 skill이 모델에게 무엇을 가능하게 해야 하는가
2. 사용자는 어떤 말로 이 skill을 필요로 할까
3. 기대 결과물은 무엇인가
4. 성공 기준은 무엇인가
5. 무엇을 비범위로 둘 것인가

가능하면 현재 대화와 기존 문서에서 먼저 답을 추출하고, 정말 구조가 달라질 질문만 추가로 묻는다.

### 2. 관련 자료를 읽는다

초안을 쓰기 전에 아래를 확인한다.

- 이 공간의 canonical source
- 비슷한 로컬 skill 1~2개
- 사용자가 준 외부 reference

어떤 정보가 skill 안에 들어가야 하고, 어떤 정보가 바깥 canonical doc에 남아야 하는지 이 단계에서 먼저 정리한다.

이 저장소 안 문서와 skill 파일에서 링크를 남길 때는 저장소 기준 상대경로를 사용한다. 로컬 도구 응답에서 쓰는 절대경로를 본문에 그대로 넣지 않는다.

### 3. skill shape를 결정한다

가장 작은 유효 bundle을 선택한다.

질문은 단순하다.

- SKILL.md 하나로 충분한가
- 길고 상세한 참고 문서가 필요해서 `references/`가 필요한가
- 같은 코드를 반복해서 쓸 가능성이 높아 `scripts/`가 필요한가
- 템플릿이나 boilerplate가 핵심이라 `assets/`가 필요한가

지원 자산은 반복 사용에서 비용을 줄일 때만 추가한다.

### 4. frontmatter를 먼저 쓴다

`name`과 `description`부터 쓴다.

- `name`: 짧고 구체적인 `kebab-case`
- `description`: 무엇을 하는지 + 언제 쓰는지

이 단계에서 애매하면 skill 전체가 흐려진다. clever한 이름보다 잘 발견되는 이름을 고른다.

### 5. SKILL.md 본문을 쓴다

좋은 SKILL.md는 보통 아래를 설명한다.

- 이 skill이 해결하는 일
- 언제 사용해야 하는지
- 어떻게 생각해야 하는지
- 핵심 workflow 또는 iteration loop
- 더 읽을 자료가 있다면 어디를 볼지
- 어떻게 빠르게 검토할지

모든 skill에 동일한 section template를 강제할 필요는 없다. skill의 workflow를 가장 잘 드러내는 구조를 선택한다.

### 6. 기존 skill을 리팩터링한다

기존 skill을 고칠 때는 형식만 다듬지 말고 아래를 본다.

- `description`이 너무 모호해서 under-trigger되는가
- canonical doc를 본문에서 과하게 복제하고 있는가
- 한 파일이 너무 커서 reference로 쪼개는 편이 나은가
- 이유 설명 없이 MUST만 반복하는가
- 반복되는 예시나 boilerplate가 asset이나 script로 분리되는 편이 나은가

리팩터링의 목표는 더 잘 발견되고, 더 lean하며, 실제 프롬프트에서 더 잘 쓰이게 만드는 것이다.

pack 전체를 리팩터링할 때는 아래 순서를 권장한다.

1. 모든 skill의 현재 `description`과 줄 수를 빠르게 훑는다
2. weak trigger, 과도한 boilerplate, 레거시 resource 경로를 먼저 표시한다
3. 공통 문제가 보이면 `skill-creator`를 먼저 보완한다
4. 그 다음 개별 skill을 다시 쓴다
5. refactor 중 새 패턴이 반복되면 `skill-creator`에 다시 반영한다

### 7. 가볍게 검토한다

초안 뒤에는 최소한 아래를 다시 본다.

1. frontmatter를 다시 읽고 `description`을 다듬는다
2. SKILL.md가 여전히 lean한지 확인한다
3. representative prompt 2~3개를 기준으로 시뮬레이션한다
4. 추가한 resource가 정말 필요한지 확인한다
5. registry가 바뀌었다면 `.codex/skills/README.md`를 갱신한다

초안이 아직 raw note처럼 보인다면 끝난 것이 아니다.

## 언제 SKILL.md 하나로 충분한가

아래 조건이 맞으면 SKILL.md 하나로 시작해도 된다.

- 핵심 가치가 workflow와 판단 기준 자체에 있다
- 상세 reference 없이도 skill을 실행할 수 있다
- 반복 실행마다 같은 코드를 다시 쓰게 될 가능성이 낮다
- 템플릿 파일 없이도 결과 품질이 크게 흔들리지 않는다

반대로 아래가 보이면 지원 자산 추가를 검토한다.

- 긴 참고 문서가 없으면 본문이 비대해진다
- 같은 스크립트를 반복해서 작성하게 된다
- 템플릿이나 boilerplate가 결과 품질에 직접 영향을 준다

## 안티패턴

아래는 피한다.

- 모호한 `description`을 두고 본문이 보완해주길 기대하는 것
- 외부 문서를 길게 복사해 넣는 것
- 모델이 이미 아는 일반론을 장황하게 적는 것
- 근거 없이 `references/`, `scripts/`, `assets/`를 미리 만드는 것
- `templates/`, `checklists/`, `queries/` 같은 레거시 디렉터리를 목적 재검토 없이 그대로 유지하는 것
- 모든 skill을 같은 section 구조에 억지로 맞추는 것
- 기존 skill을 리팩터링하면서 trigger 품질은 건드리지 않는 것

## 산출물

이 skill을 제대로 사용했다면 결과는 보통 아래를 포함한다.

- 새로 만든 또는 개정한 `.codex/skills/<skill-name>/SKILL.md`
- 정말 필요한 경우에만 추가한 bundled resource
- registry나 진입점이 바뀌었다면 갱신된 `.codex/skills/README.md`
- 어떤 프롬프트나 점검으로 검토했는지에 대한 짧은 메모
