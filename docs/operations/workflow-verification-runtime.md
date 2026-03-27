# Workflow Verification Runtime

이 문서는 `git-ranker-workflow`가 소유하는 표준 검증 런타임을 설명한다. 목적은 운영 환경을 완전히 복제하는 것이 아니라, ranking read harness를 같은 기준으로 반복 실행할 수 있는 cross-repo runtime을 고정하는 것이다.

## 목적과 범위

- 대상 작업: `GRW-05`
- 첫 대상 흐름: public ranking read
- 포함 서비스: backend, client, db, prometheus, loki
- 보조 서비스: promtail

현재 runtime은 아래를 보장한다.

- workflow 루트에서 같은 compose 파일과 helper script로 기동
- backend/client/public ranking endpoint/observability endpoint의 기본 health 확인
- 후속 `GRB-03`, `GRC-04`, `GRW-06`이 붙을 interface와 포트 규칙 고정

현재 runtime은 아래를 아직 보장하지 않는다.

- 결정적 seed 데이터 적재
- Playwright 시나리오 실행
- 배지/배치 harness

## 디렉터리 구조

| 경로 | 역할 |
| --- | --- |
| `runtime/compose.yaml` | workflow가 소유하는 cross-repo compose 정의 |
| `runtime/grw-runtime` | `start`, `stop`, `reset`, `seed`, `verify` wrapper |
| `runtime/.env.example` | 안전한 기본 env 예시 |
| sibling `git-ranker` repo의 `prometheus.yml` | workflow runtime이 재사용하는 metrics scrape 설정 |
| sibling `git-ranker` repo의 `loki-config.yml` | workflow runtime이 재사용하는 loki 설정 |
| sibling `git-ranker` repo의 `promtail-config.yml` | workflow runtime이 재사용하는 backend log shipping 설정 |

## 인터페이스

기본 명령:

- `./runtime/grw-runtime start`
- `./runtime/grw-runtime stop`
- `./runtime/grw-runtime reset`
- `./runtime/grw-runtime seed`
- `./runtime/grw-runtime verify`

동작 규칙:

- helper는 `runtime/.env`가 있으면 우선 사용하고, 없으면 `runtime/.env.example`을 사용한다.
- `start`는 compose build/up만 수행한다.
- `stop`은 컨테이너만 내리고 volume은 유지한다.
- `reset`은 volume까지 제거해 db/metrics/log positions를 초기화한다.
- `seed`는 현재 placeholder다. 실제 결정적 데이터 적재는 `GRB-03`에서 연결한다.
- `verify`는 host 기준 endpoint에 대해 wait + health 확인을 수행한다.

재사용 원칙:

- workflow는 orchestration과 env 정책만 소유한다.
- Prometheus/Loki/Promtail 본문 설정은 모두 `git-ranker`를 source of truth로 재사용한다.
- workflow에는 runtime wiring과 host/env 정책만 남긴다.
- 따라서 observability 규칙 자체를 두 군데에서 병렬 수정하지 않는다.

## 서비스와 포트

| 서비스 | compose service | host port | 내부 포트 | 용도 |
| --- | --- | --- | --- | --- |
| client | `git-ranker-client` | `3000` | `3000` | ranking UI |
| backend api | `git-ranker-api` | `8080` | `8080` | public API, OAuth start endpoint |
| backend management | `git-ranker-api` | `9090` | `9090` | actuator health, prometheus |
| mysql | `git-ranker-db` | `3307` | `3306` | runtime DB |
| prometheus | `prometheus` | `9091` | `9090` | metrics scrape/readiness |
| loki | `loki` | `3100` | `3100` | log storage/readiness |
| promtail | `promtail` | 없음 | `9080` | backend container log shipper |

## Environment Rules

helper는 `runtime/.env.example`의 값을 기본값으로 사용한다. 대표 변수:

| 이름 | 기본값 | 의미 |
| --- | --- | --- |
| `BACKEND_HTTP_PORT` | `8080` | backend public API host port |
| `BACKEND_MANAGEMENT_PORT` | `9090` | backend actuator host port |
| `CLIENT_PORT` | `3000` | frontend host port |
| `MYSQL_PORT` | `3307` | mysql host port |
| `PROMETHEUS_PORT` | `9091` | prometheus host port |
| `LOKI_PORT` | `3100` | loki host port |
| `NEXT_PUBLIC_BASE_URL` | `http://localhost:3000` | client public site origin |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8080` | browser 기준 backend origin |
| `APP_CORS_ALLOWED_ORIGINS` | `http://localhost:3000,http://127.0.0.1:3000` | runtime용 backend CORS override |
| `APP_OAUTH2_AUTHORIZED_REDIRECT_URI` | `http://localhost:3000/auth/callback` | runtime용 frontend redirect |
| `APP_COOKIE_DOMAIN` | `localhost` | runtime cookie domain |
| `APP_COOKIE_SECURE` | `false` | local cookie secure flag |
| `SPRING_JPA_HIBERNATE_DDL_AUTO` | `update` | fresh mysql에서도 schema를 만들 수 있게 하는 runtime-only override |

주의:

- backend는 `prod` profile을 유지해 JSON 로그와 production-like actuator exposure를 재사용한다.
- 대신 localhost 검증 환경에 맞게 CORS/cookie/oauth redirect와 JPA ddl-auto만 runtime에서 override한다.
- client의 `NEXT_PUBLIC_API_URL`은 browser와 일부 server-side 코드가 같이 사용되므로, 이번 runtime은 ranking page browser fetch 기준을 우선한다.
- runtime은 backend promtail config를 그대로 재사용하기 위해 backend container name을 `git-ranker-api`로 유지한다.
- Next.js 컨테이너 healthcheck는 `localhost`가 아닌 `127.0.0.1`을 사용한다. 이 이미지는 `localhost` 해석 시 IPv6 loopback을 먼저 타면서 connection refused가 날 수 있다.
- 따라서 기존 app repo compose stack과 동시에 켜지 않는 것을 전제로 한다.

## Verify 기준

`./runtime/grw-runtime verify`는 아래 순서로 확인한다.

1. backend actuator health: `http://localhost:9090/actuator/health`
2. backend public ranking API: `http://localhost:8080/api/v1/ranking?page=0`
3. client root: `http://localhost:3000`
4. prometheus ready: `http://localhost:9091/-/ready`
5. loki ready: `http://localhost:3100/ready`

## Known Gaps

- `seed`는 아직 실제 데이터를 넣지 않는다. 첫 기동 시 ranking API와 UI는 empty state를 반환할 수 있다.
- client의 sitemap/opengraph 같은 server-side fetch 경로는 `NEXT_PUBLIC_API_URL=http://localhost:8080`일 때 container 내부에서 동일하게 동작하지 않을 수 있다.
- promtail은 Docker socket 기반으로 backend stdout JSON 로그를 수집한다. Docker 엔진 접근 제약이 있는 환경에서는 loki signal이 비어 있을 수 있다.

## 다음 작업 연결

- `GRB-03`: `seed` 명령에 결정적 fixture 연결
- `GRC-04`: ranking UI smoke와 pagination/tier filter를 runtime 위에서 실행
- `GRW-06`: LogQL/PromQL query와 evidence summary 추가
