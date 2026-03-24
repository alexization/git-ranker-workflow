# Daily Batch Flow

일일 배치는 모든 사용자의 점수와 랭킹을 다시 계산하는 운영 루프다. 스케줄러, Spring Batch job, GitHub 호출 전략, 실패 저장, 최종 랭킹 재산정이 순서대로 이어진다.

## 스케줄 규칙

- 실행 시각: 매일 `00:00`
- 타임존: `Asia/Seoul`
- 스케줄러: [BatchScheduler.java](../../git-ranker/src/main/java/com/gitranker/api/batch/scheduler/BatchScheduler.java)

스케줄러는 실행 시작 전에 새 `trace_id`를 만들고 `BATCH_STARTED` 이벤트를 남긴다. 예외가 나면 `BATCH_FAILED`를 기록하고 `BATCH_JOB_FAILED`로 래핑한다.

## Job 구성

job 이름:

- Spring Batch job: `dailyScoreRecalculationJob`
- scheduler 로그용 이름: `DailyScoreRecalculation`

step 순서:

1. `scoreRecalculationStep`
2. `rankingRecalculationStep`

구현:

- [DailyScoreRecalculationJobConfig.java](../../git-ranker/src/main/java/com/gitranker/api/batch/job/DailyScoreRecalculationJobConfig.java)

## Step 1. 점수 재계산

### Reader

- 사용자 전체를 `id ASC`로 읽는다.
- page/chunk 크기 기본값은 `100`
- 구현: [UserItemReader.java](../../git-ranker/src/main/java/com/gitranker/api/batch/reader/UserItemReader.java)

### Processor

processor는 사용자별로 아래 순서를 따른다.

1. 가장 최근 activity log를 읽어 이전 누적값을 만든다.
2. 올해 시작 전 baseline log가 있는지 확인한다.
3. baseline log가 있으면 증분 전략, 없으면 전체 전략을 선택한다.
4. GitHub에서 새 활동 통계를 가져와 점수를 다시 계산한다.
5. 오늘 날짜 activity log를 저장하고 diff를 계산한다.

구현:

- [ScoreRecalculationProcessor.java](../../git-ranker/src/main/java/com/gitranker/api/batch/processor/ScoreRecalculationProcessor.java)
- [IncrementalActivityUpdateStrategy.java](../../git-ranker/src/main/java/com/gitranker/api/batch/strategy/IncrementalActivityUpdateStrategy.java)
- [FullActivityUpdateStrategy.java](../../git-ranker/src/main/java/com/gitranker/api/batch/strategy/FullActivityUpdateStrategy.java)

### 증분 전략의 baseline 규칙

- baseline log는 전년도 `12-31` 누적값이다.
- 증분 전략은 올해 활동만 다시 읽고 baseline과 합쳐 전체 누적값을 만든다.
- `merged PR`은 올해 값이 아니라 GitHub search에서 받은 전체 누적값을 사용한다.

이 규칙은 `merged PR`이 contributions collection이 아니라 별도 전체 검색 값이기 때문에 필요하다.

### GitHub username 변경 처리

processor가 `GITHUB_USER_NOT_FOUND`를 받으면 아래 보정 루프를 한 번 수행한다.

1. 기존 `nodeId`로 GitHub user lookup
2. 새 `login`, `avatarUrl`, `email`로 profile update
3. 같은 사용자에 대해 점수 재계산 재시도

lookup 결과에서도 사용자가 없으면 non-retryable failure로 남긴다.

## Step 2. 랭킹 재산정

- `users` 테이블 전체에 대해 bulk ranking/tier update를 수행한다.
- 일반 service 경로와 달리, tasklet은 DB 필드만 갱신하고 ranking cache는 비우지 않는다.
- 따라서 DB 기준 새 랭킹은 즉시 반영되지만, batch 직전 cache hit가 남아 있으면 랭킹 API는 최대 `5분` 동안 이전 page를 반환할 수 있다.

구현:

- [RankingRecalculationTasklet.java](../../git-ranker/src/main/java/com/gitranker/api/batch/tasklet/RankingRecalculationTasklet.java)
- [UserRepository.java](../../git-ranker/src/main/java/com/gitranker/api/domain/user/UserRepository.java)

## Retry / Skip / Failure 저장

`scoreRecalculationStep`의 fault-tolerance 규칙:

- retry 대상: `GitHubApiRetryableException`
- retry 횟수: `3`
- backoff: exponential
- skip 대상: `GitHubApiNonRetryableException`, `GitHubApiRetryableException`
- skip 한도: `100`

skip이 발생하면 [UserScoreCalculationSkipListener.java](../../git-ranker/src/main/java/com/gitranker/api/batch/listener/UserScoreCalculationSkipListener.java)가 아래를 수행한다.

- `BATCH_ITEM_FAILED` 로그 기록
- `phase`, `error_type`, `error_message`, `retryable` 필드 기록
- `batch_failure_logs` 테이블에 실패 이력 저장

## 진행률과 요약

- chunk 진행률은 `10%` 간격으로 debug 로그를 남긴다.
- job 완료 후 summary listener가 `total_count`, `success_count`, `fail_count`, `skip_count`, `duration_ms`를 남긴다.
- 성공/실패 duration과 처리량 metrics도 이 시점에 기록한다.

구현:

- [BatchProgressListener.java](../../git-ranker/src/main/java/com/gitranker/api/batch/listener/BatchProgressListener.java)
- [GitHubCostListener.java](../../git-ranker/src/main/java/com/gitranker/api/batch/listener/GitHubCostListener.java)
- [BatchMetrics.java](../../git-ranker/src/main/java/com/gitranker/api/batch/metrics/BatchMetrics.java)

## 실패 모드

| 위치 | 실패 영향 |
| --- | --- |
| scheduler | job 시작 자체 실패, `BATCH_FAILED` 기록 |
| reader / processor / writer | retry 또는 skip 정책 적용 |
| skip limit 초과 | job 실패 |
| rankingRecalculationStep | 전체 job 실패, 최종 랭킹 일관성 미보장 |
| batch failure log 저장 실패 | 본 실패는 debug/error 로그만 남기고 원래 batch 흐름은 유지 |

## Harness 관점 수용 기준

- 자정 KST 스케줄과 step 순서가 문서와 같아야 한다.
- baseline이 있는 사용자는 증분 전략을, 없는 사용자는 전체 전략을 사용해야 한다.
- retryable GitHub 오류는 최대 3회 재시도 후 skip 대상으로 전환돼야 한다.
- rankingRecalculationStep 완료 후 DB의 `ranking`, `percentile`, `tier`는 새 값이어야 한다.
- ranking API cache stale window가 최대 `5분`이라는 현재 구현 한계를 evidence에 남겨야 한다.

## 참고 경로

- [BatchScheduler.java](../../git-ranker/src/main/java/com/gitranker/api/batch/scheduler/BatchScheduler.java)
- [DailyScoreRecalculationJobConfig.java](../../git-ranker/src/main/java/com/gitranker/api/batch/job/DailyScoreRecalculationJobConfig.java)
- [ScoreRecalculationProcessor.java](../../git-ranker/src/main/java/com/gitranker/api/batch/processor/ScoreRecalculationProcessor.java)
- [BatchFailureLogService.java](../../git-ranker/src/main/java/com/gitranker/api/domain/failure/BatchFailureLogService.java)
- [BatchFailureLog.java](../../git-ranker/src/main/java/com/gitranker/api/domain/failure/BatchFailureLog.java)
