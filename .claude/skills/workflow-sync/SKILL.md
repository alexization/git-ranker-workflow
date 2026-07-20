---
name: workflow-sync
description: 서브모듈 PR 머지 상태를 확인해 루트 gitlink를 갱신하고 요구사항 추적 이슈를 닫을 때 사용한다. destructive 명령 없이 gitlink만 develop 최신으로 반영한다.
---

# Workflow Sync

`/dispatch`가 만든 추적 이슈를 원장으로, 머지된 서브모듈 작업을 루트 gitlink에 반영한다.

## 절차

1. **추적 이슈 선택**: 인자로 번호/URL이 오면 그것을, 없으면 `gh issue list --repo alexization/git-ranker-workflow --label tracking --state open`에서 고른다.
2. **머지 상태 확인**: 추적 이슈 본문의 서브모듈 이슈 번호를 파싱하고, 각 이슈에 연결된 PR의 머지 여부를 확인한다.
   ```bash
   gh issue view <번호> --repo alexization/<repo> --json title,state,body
   gh pr list --repo alexization/<repo> --search "<이슈참조>" --state merged --json number,mergedAt
   ```
3. **gitlink 갱신 (머지된 쪽만)**: destructive 규약 준수.
   ```bash
   git -C <sub> fetch origin develop
   git submodule update --remote <sub>   # 또는: git -C <sub> checkout <merge-sha>
   git add <sub>
   ```
   - 파일 discard용 `git checkout --`가 아닌 브랜치/커밋 checkout만 사용.
   - 서브모듈에 uncommitted 변경이 있으면 중단하고 사용자에게 보고(덮어쓰기 금지).
4. **커밋 초안**: `.gitmessage.ko.txt` 형식으로 gitlink 커밋을 만든다. **push는 사용자 요청 시만.**
   ```bash
   git commit -m "chore: <요구사항> 서브모듈 gitlink 반영"
   ```
5. **추적 이슈 갱신**: 완료 체크박스를 갱신한다. 두 서브모듈 모두 머지·반영되면 사용자 확인 후 닫는다.
   ```bash
   gh issue edit <T> --repo alexization/git-ranker-workflow --body-file <갱신본>
   gh issue close <T> --repo alexization/git-ranker-workflow
   ```

## 부분 진행

- 아직 머지되지 않은 PR은 skip하고 상태만 보고한다.
- 한쪽만 머지되면 그쪽 gitlink만 갱신하고 체크박스도 부분 갱신한다. 나머지는 다음 `/sync`에서 처리.

## 오류 처리

- `gh auth status` 미인증 시 안내 후 중단.
- 연결된 PR을 찾지 못하면(이슈 본문에 `Closes #` 누락 등) 이슈 상태만 보고하고 사용자에게 수동 확인 요청.
