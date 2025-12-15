# 🚀 Preview Environment Demo

A demo application showcasing ephemeral preview environments using ArgoCD ApplicationSets with the Pull Request Generator.

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   GitHub PR     │────▶│  GitHub Actions  │────▶│   Docker Hub    │
│  (this repo)    │     │   (build/push)   │     │  (image store)  │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Preview Env   │◀────│     ArgoCD       │◀────│  GitOps Repo    │
│  (Kubernetes)   │     │ (ApplicationSet) │     │ (K8s manifests) │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

## How It Works

1. **Open a PR** → GitHub Actions builds and pushes `shoofio/preview-demo:pr-{number}-{sha}`
2. **ArgoCD detects** → ApplicationSet's PR generator sees the open PR
3. **Deploy preview** → Creates namespace `preview-pr-{number}` with the app
4. **Push more commits** → CI rebuilds, ArgoCD syncs the new image
5. **Close/merge PR** → ArgoCD deletes the preview environment

## Setup

### 1. Create GitHub Repository

Push this folder to a new GitHub repo (e.g., `Shoofio/preview-demo`)

### 2. Configure Secrets

In your GitHub repo settings, add these secrets:
- `DOCKERHUB_USERNAME` - Your Docker Hub username
- `DOCKERHUB_TOKEN` - Docker Hub access token

### 3. Apply ArgoCD ApplicationSet

The ApplicationSet is in the gitops repo at:
```
argocd/applications/child-applications/preview-environments/preview-demo-appset.yaml
```

### 4. Test It!

1. Create a feature branch
2. Make a change
3. Open a PR
4. Watch the magic happen! ✨

## Local Development

```bash
cd app
pip install -r requirements.txt
python main.py
# Visit http://localhost:8080
```

## Image Tags

| Tag Pattern | Description |
|-------------|-------------|
| `pr-{N}-{sha}` | Specific PR commit (e.g., `pr-42-abc1234`) |
| `pr-{N}-latest` | Latest build for PR (e.g., `pr-42-latest`) |

