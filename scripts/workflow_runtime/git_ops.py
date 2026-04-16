from __future__ import annotations

import subprocess
from pathlib import Path

from workflow_runtime.models import normalize_repo_path


def git_command(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)


def git_paths(root: Path, staged: bool = False) -> list[str]:
    result = git_command(
        root,
        ["diff", "--name-only", "--diff-filter=ACMRTUXB", *(["--cached"] if staged else [])],
    )
    if result.returncode != 0:
        return []

    tracked = [normalize_repo_path(line) for line in result.stdout.splitlines() if line.strip()]
    if staged:
        return sorted(set(tracked))

    untracked_result = git_command(root, ["ls-files", "--others", "--exclude-standard"])
    if untracked_result.returncode != 0:
        return sorted(set(tracked))
    untracked = [normalize_repo_path(line) for line in untracked_result.stdout.splitlines() if line.strip()]
    return sorted(set(tracked + untracked))


def unpushed_git_paths(root: Path) -> list[str]:
    upstream = git_command(root, ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"])
    if upstream.returncode == 0:
        ref = upstream.stdout.strip()
        if ref:
            diff_result = git_command(root, ["diff", "--name-only", "--diff-filter=ACMRTUXB", f"{ref}...HEAD"])
            if diff_result.returncode == 0:
                return sorted(
                    {
                        normalize_repo_path(line)
                        for line in diff_result.stdout.splitlines()
                        if line.strip()
                    }
                )

    parent = git_command(root, ["rev-parse", "HEAD~1"])
    if parent.returncode == 0:
        diff_result = git_command(root, ["diff", "--name-only", "--diff-filter=ACMRTUXB", "HEAD~1..HEAD"])
        if diff_result.returncode == 0:
            return sorted(
                {
                    normalize_repo_path(line)
                    for line in diff_result.stdout.splitlines()
                    if line.strip()
                }
            )

    show_result = git_command(root, ["show", "--name-only", "--pretty=format:", "HEAD"])
    if show_result.returncode != 0:
        return []
    return sorted({normalize_repo_path(line) for line in show_result.stdout.splitlines() if line.strip()})
