# 2026-03-27-grw-05-standard-verification-runtime

- Issue ID: `GRW-05`
- GitHub Issue: `alexization/git-ranker-workflow#26`
- Status: `Completed`
- Repository: `git-ranker-workflow`
- Branch Name: `feat/grw-05-standard-verification-runtime`
- Task Slug: `2026-03-27-grw-05-standard-verification-runtime`

## Problem

`git-ranker`와 `git-ranker-client`는 각 저장소 안에 개별 Docker 자산이 있지만, `git-ranker-workflow`가 소유하는 공통 검증 런타임은 아직 없다. 지금 상태에서는 ranking read harness를 실행할 때마다 개발자마다 다른 compose 파일, 다른 env, 다른 기동 순서를 쓰게 된다.

## Why Now

`GRW-05`는 이후 `GRB-03`, `GRC-04`, `GRW-06`이 같은 검증 환경을 기준으로 seed, Playwright, LogQL, PromQL을 붙일 수 있게 만드는 선행 작업이다. workflow 저장소가 control plane 역할을 하려면 cross-repo 검증 런타임도 여기서 표준화돼 있어야 한다.

## Scope

- workflow가 소유하는 cross-repo verification runtime 디렉터리 추가
- backend, client, db, prometheus, loki 최소 런타임 정의
- `start`, `stop`, `reset`, `seed`, `verify` 인터페이스 정의
- 포트, env, health check 규칙 문서화
- `GRW-05` 실행 기록과 검증 결과 정리

## Non-scope

- Playwright 시나리오 작성
- 배치 harness 구현
- 결정적 seed 데이터 구현
- backend/client 애플리케이션 코드 변경

## Write Scope

- `runtime/`
- `docs/operations/`
- `docs/exec-plans/`
- `.gitignore`

## Outputs

- workflow 소유 compose 파일과 helper script
- runtime env 예시
- workflow verification runtime reference 문서
- `GRW-05` 실행 기록

현재 산출물:

- `runtime/compose.yaml`
- `runtime/grw-runtime`
- `runtime/.env.example`
- `docs/operations/workflow-verification-runtime.md`
- `docs/operations/README.md`
- `.gitignore`
- `docs/exec-plans/completed/2026-03-27-grw-05-standard-verification-runtime.md`

## Verification

- `docker compose --env-file runtime/.env.example -f runtime/compose.yaml config`
- `./runtime/grw-runtime start`
- `./runtime/grw-runtime verify`
- `./runtime/grw-runtime stop`

결과 요약:

- `docker compose --env-file runtime/.env.example -f runtime/compose.yaml config`: 성공
- `./runtime/grw-runtime seed`: placeholder 동작 확인, exit code `3`
- `./runtime/grw-runtime start`: backend/client/db/prometheus/loki/promtail 기동 성공
- `./runtime/grw-runtime verify`: backend actuator, ranking API, client root, Prometheus ready, Loki ready 모두 성공
- `./runtime/grw-runtime stop`: 컨테이너와 network 정상 종료, volume 유지
- `git submodule status`: `git-ranker`, `git-ranker-client` submodule 연결 확인
- client healthcheck는 초기 정의의 `localhost` probe에서 실패했지만, `127.0.0.1` probe로 수정 후 compose 상태와 실제 readiness를 일치시켰다.

## Evidence

- compose config 해석 결과
- backend `/actuator/health`, public ranking endpoint, client root, Prometheus ready, Loki ready 결과
- 변경된 runtime/doc 경로

명령 결과 요약:

- `./runtime/grw-runtime verify`
  - `http://localhost:9090/actuator/health` 준비 완료
  - `http://localhost:8080/api/v1/ranking?page=0` 준비 완료
  - `http://localhost:3000` 준비 완료
  - `http://localhost:9091/-/ready` 준비 완료
  - `http://localhost:3100/ready` 준비 완료
- `docker compose --env-file runtime/.env.example -f runtime/compose.yaml config`
  - 성공, backend observability 설정 재사용을 포함한 compose 해석 확인
- `git submodule status`
  - `git-ranker`, `git-ranker-client` submodule 연결 확인, `start` preflight 추가 근거 확보
- `docker exec runtime-git-ranker-client-1 wget -q --spider http://localhost:3000`
  - 실패, `localhost` probe connection refused
- `docker exec runtime-git-ranker-client-1 wget -q --spider http://127.0.0.1:3000`
  - 성공, client healthcheck 불일치 원인 확인
- `./runtime/grw-runtime stop`
  - runtime containers 제거, `runtime_default` network 제거 확인

## Risks or Blockers

- client의 `NEXT_PUBLIC_API_URL`은 browser와 일부 server-side 코드가 같이 사용하므로, container 내부와 host browser 모두에 완벽한 단일 값은 아직 어렵다. 이번 runtime은 ranking page의 browser fetch 기준을 우선한다.
- backend repo의 observability config를 재사용하므로, workflow runtime과 app repo compose를 동시에 켜면 같은 host port나 `git-ranker-api` container name을 두 번 점유할 수 있다.
- deterministic seed는 `GRB-03` 전까지 제공되지 않으므로 `seed` 인터페이스는 placeholder로 시작한다.
- Loki 수집은 Docker socket 접근 가능 여부에 따라 로컬 환경별 차이가 날 수 있다.

## Next Preconditions

- `GRB-03`: `seed` 인터페이스에 실제 결정적 데이터 적재 연결
- `GRC-04`: workflow runtime 위에서 ranking read Playwright harness 도입
- `GRW-06`: Prometheus/Loki readiness를 실제 evidence query로 확장

## Docs Updated

- `docs/operations/workflow-verification-runtime.md`
- `docs/operations/README.md`
- `docs/exec-plans/completed/2026-03-27-grw-05-standard-verification-runtime.md`

## Skill Consideration

이번 작업은 `issue-to-exec-plan` 흐름을 적용해 roadmap 항목을 active exec plan으로 먼저 고정했다. runtime 실행 절차는 이후 `GRW-S03`에서 ranking harness execution skill이 재사용할 실제 입력이 된다.
