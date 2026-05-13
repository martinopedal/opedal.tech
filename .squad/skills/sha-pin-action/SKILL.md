# Skill: SHA-pin GitHub Actions

## Purpose

SHA-pin a GitHub Action by resolving its latest release tag to a commit SHA, enabling secure workflow automation while maintaining human-readable version comments.

## Context

opedal.tech repository policy requires all GitHub Actions to use SHA-pinned versions (not tags) with inline `# vX.Y.Z` comments for human readability. Example:
```yaml
uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
```

This prevents tag-rewriting attacks while keeping workflows maintainable.

## Prerequisites

- `gh` CLI authenticated
- Target action has a GitHub release with tagged version

## Steps

### 1. Fetch latest release metadata

```pwsh
gh api repos/{owner}/{repo}/releases/latest --jq '{tag_name, target_commitish}'
```

Example output:
```json
{
  "tag_name": "v2.4.3",
  "target_commitish": "main"
}
```

### 2. Resolve tag to commit SHA

```pwsh
gh api repos/{owner}/{repo}/git/refs/tags/{tag} --jq '.object.sha'
```

Example:
```pwsh
gh api repos/ossf/scorecard-action/git/refs/tags/v2.4.3 --jq '.object.sha'
# Output: 99c09fe975337306107572b4fdf4db224cf8e2f2
```

### 3. Use SHA in workflow with inline comment

```yaml
- name: Run OSSF Scorecard
  uses: ossf/scorecard-action@99c09fe975337306107572b4fdf4db224cf8e2f2 # v2.4.3
  with:
    results_file: results.sarif
```

## Batch example (multiple actions)

```pwsh
$actions = @(
  @{owner="ossf"; repo="scorecard-action"},
  @{owner="reviewdog"; repo="action-actionlint"},
  @{owner="actions"; repo="dependency-review-action"},
  @{owner="step-security"; repo="harden-runner"},
  @{owner="actions"; repo="attest-build-provenance"}
)

foreach ($action in $actions) {
  $release = gh api "repos/$($action.owner)/$($action.repo)/releases/latest" --jq '{tag_name, target_commitish}'
  $tag = ($release | ConvertFrom-Json).tag_name
  $sha = gh api "repos/$($action.owner)/$($action.repo)/git/refs/tags/$tag" --jq '.object.sha'
  Write-Host "$($action.owner)/$($action.repo)@$sha # $tag"
}
```

## Verification

After pinning, verify the workflow parses:
```pwsh
python -c "import yaml; yaml.safe_load(open('.github/workflows/scorecard.yml'))"
```

## Applied in

- PR C (feat/garman-hardening): scorecard.yml, actionlint.yml, dependency-review.yml, pages.yml (harden-runner + attest-build-provenance), cv.yml (harden-runner)

## References

- GitHub Security Best Practices: [Using third-party actions](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions#using-third-party-actions)
- OpenSSF Scorecard: [Pinned-Dependencies check](https://github.com/ossf/scorecard/blob/main/docs/checks.md#pinned-dependencies)
