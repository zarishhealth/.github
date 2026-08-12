## What does this PR do?

<!-- One sentence. What is the change? -->

## Why is this change needed?

<!-- Link to the Issue this PR closes: Closes #NNN -->
<!-- If no Issue exists, explain the problem this solves. -->

Closes #

## Type of change

- [ ] Bug fix (fixes something broken — no breaking changes)
- [ ] New feature (adds something new — no breaking changes)
- [ ] Breaking change (changes existing behavior — requires version bump)
- [ ] Documentation only (no code changes)
- [ ] Clinical content (new or updated forms, concepts, terminologies)
- [ ] Infrastructure (IaC, CI/CD, deployment configuration)
- [ ] Refactor (code improvement — no behavior change)
- [ ] Security fix (addresses a vulnerability)

## Checklist

### Before opening this PR, I confirm:

- [ ] I wrote or updated documentation before writing implementation code
- [ ] My commit messages follow [Conventional Commits](https://www.conventionalcommits.org) format
- [ ] All tests pass locally (`go test ./...` or `pnpm test` or `flutter test`)
- [ ] I ran the linter locally (`golangci-lint run` / `pnpm lint` / `flutter analyze`)
- [ ] I updated `CHANGELOG.md` if this is a user-facing change
- [ ] I added or updated tests for the changed code
- [ ] My branch is up to date with `main`

### For clinical content changes, I additionally confirm:

- [ ] The content references a published standard (WHO, ICD-11, LOINC, SNOMED CT, CIEL)
- [ ] A clinical professional has reviewed the content
- [ ] The license for added content is `CC0 1.0` (public domain)

### For security-sensitive changes, I additionally confirm:

- [ ] I have not introduced any new secrets or API keys into the codebase
- [ ] I have reviewed the OWASP Top 10 impact of this change
- [ ] The `@zarishsphere/team-security` team has been requested for review

## Testing Evidence

<!-- Describe how you tested this change. Screenshots for UI changes. -->
<!-- For API changes: paste a sample request and response. -->

## Screenshots (if applicable)

<!-- Delete this section if not applicable -->

## Additional Notes

<!-- Anything a reviewer should know before reviewing this PR -->