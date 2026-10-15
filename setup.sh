#!/usr/bin/env bash
ORG=zarishhealth
# ensure gh is authenticated with admin:org scope
gh auth status || { echo "Authenticate gh with admin privileges"; exit 1; }

# 1. Org hardening
gh api -X PATCH /orgs/${ORG} -f two_factor_requirement_enabled=true
gh api -X PATCH /orgs/${ORG} -f members_can_create_repositories=false

# 2. Actions permissions: allow only local org actions, enable for all repos
gh api -X PUT /orgs/${ORG}/actions/permissions -f allowed_actions=local_only -f enabled_repositories=all
gh api -X PUT /orgs/${ORG}/actions/permissions/workflow -f default_workflow_permissions=read

# 3. Create core repos (public)
for repo in .github zarishhealth.github.io core api fhir mcp app docs deploy content; do
  gh repo create ${ORG}/${repo} --public --description "Auto-created ${repo}" --confirm || echo "repo ${repo} exists or failed"
done

# 4. Create distro-template as private template
gh repo create ${ORG}/distro-template --private --description "distro template (no secrets)" --confirm || echo "distro-template exists or failed"

# 5. Create standard teams
for team in maintainers core-rust app fhir-clinical docs-content security release; do
  gh api -X POST /orgs/${ORG}/teams -f name=${team} -f privacy=closed || echo "team ${team} exists or failed"
done

# 6. Create CODEOWNERS and Dependabot in .github repo (push files)
cat > CODEOWNERS <<'EOF'
* @zarishhealth/maintainers
EOF

cat > dependabot.yml <<'EOF'
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
EOF

git clone https://github.com/${ORG}/.github temp__org_dot_github || true
cd temp__org_dot_github || (echo ".github clone failed"; exit 1)
mkdir -p .github
mv ../CODEOWNERS .
mv ../dependabot.yml .
git add CODEOWNERS dependabot.yml || true
git commit -m "Add CODEOWNERS and global dependabot" || true
git push origin main || true
cd ..
rm -rf temp__org_dot_github

echo "Bootstrap complete. Review each repo for private/public classification and add required files (LICENSE, README, SECURITY.md)."