# kubernetes-argocd-lab

Minimal GitOps lab with **ArgoCD**. Includes:
- A tiny Flask app (Dockerized)
- Plain Kubernetes manifests
- A simple Helm chart
- ArgoCD `AppProject` and two `Application` examples (one for manifests, one for Helm)

> Keep this repo separate from your minimal Kubernetes repo to preserve scope.

## 0) Prerequisites
- Docker, kubectl, Helm v3
- A running cluster (minikube/k3s/kind/EKS)
- ArgoCD installed in the cluster (see below)

## 1) Build & Push the image
```bash
cd app
docker build -t <YOUR_DOCKERHUB_USERNAME>/k8s-argocd-lab:1.0.0 .
docker login
docker push <YOUR_DOCKERHUB_USERNAME>/k8s-argocd-lab:1.0.0
```

## 2) Update image in manifests/helm
- `manifests/deployment.yaml` → set `image:`
- `helm/demo-chart/values.yaml` → set `image.repository` and `tag`

## 3) Install ArgoCD (if not installed yet)
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Access UI locally
kubectl -n argocd port-forward svc/argocd-server 8082:443

# Get initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```

## 4) Create the target namespace
```bash
kubectl apply -f manifests/namespace.yaml
```

## 5) Create ArgoCD Project & Applications
```bash
# Create project
kubectl apply -f argocd/project.yaml -n argocd

# Create applications (manifests + helm)
# Edit repoURL to point to your repo before applying!
kubectl apply -f argocd/application-manifests.yaml -n argocd
```

## 6) Verify
```bash
kubectl -n k8s-minimal get deploy,po,svc
kubectl -n argocd get applications
```

## 7) Notes
- Use **one source at a time** per application (either `path: manifests` or `path: helm/demo-chart`).
- Prefer enabling `automated` sync for quick demos; for real projects, add RBAC and disable auto-sync in production.
- If port 8080 is already used on your machine (e.g., Jenkins), use `kubectl port-forward ... 8081:8080` when testing locally.
