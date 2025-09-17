This folder is for generated ArgoCD reports.
Real JSON reports are ignored by Git (see root .gitignore).

Example output shape (for reference only):
```json
{
  "apps": [
    {
      "name": "manifests-app",
      "project": "personal-lab",
      "namespace": "k8s-minimal",
      "sync": "Synced",
      "health": "Healthy",
      "revision": "main@abcdef1"
    },
    {
      "name": "helm-app",
      "project": "personal-lab",
      "namespace": "k8s-minimal",
      "sync": "Synced",
      "health": "Healthy",
      "revision": "main@abcdef2"
    }
  ],
  "generated_at": "YYYY-MM-DDTHH:MM:SSZ"
}

