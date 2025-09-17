# kubernetes-argocd-lab

Minimal GitOps lab with **ArgoCD**.

**What’s inside**
- A tiny Flask app (Dockerized)
- Plain Kubernetes manifests
- A simple Helm chart
- ArgoCD `AppProject` and two `Application` examples (one for **manifests**, one for **Helm**)

> Keep this repo separate from your minimal Kubernetes repo to preserve scope.

---

## 0) Prerequisites
- Docker, kubectl, Helm v3
- A running cluster (minikube / k3s / kind / EKS)
- ArgoCD installed in the cluster (see below)

---

## 1) Build & Push the image
```bash
cd app
docker build -t <YOUR_DOCKERHUB_USERNAME>/k8s-argocd-lab:1.0.0 .
docker login
docker push <YOUR_DOCKERHUB_USERNAME>/k8s-argocd-lab:1.0.0


2) Update image in manifests/helm
manifests: edit manifests/deployment.yaml → set the image:

helm: edit helm/demo-chart/values.yaml → set image.repository and image.tag

3) Install ArgoCD (if not installed yet)
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
Access the UI locally
Option A (HTTPS):
kubectl -n argocd port-forward svc/argocd-server 8082:443

# then open https://localhost:8082  (accept the self-signed certificate)
Option B (HTTP, simpler for labs):
kubectl -n argocd port-forward svc/argocd-server 8082:80

# then open http://localhost:8082
Get initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d; echo


4) Create the target namespace
kubectl apply -f manifests/namespace.yaml


5) Create ArgoCD Project & Applications
# Project
kubectl apply -f argocd/project.yaml -n argocd

# Applications (manifests + helm)
# IMPORTANT: edit repoURL in argocd/application-manifests.yaml to your repo before applying!
kubectl apply -f argocd/application-manifests.yaml -n argocd


6) Verify
kubectl -n k8s-minimal get deploy,po,svc
kubectl -n argocd get applications


7) Notes
Use one source at a time per Application (either path: manifests or path: helm/demo-chart).

For quick demos, syncPolicy.automated is enabled; in real projects, add RBAC and consider disabling auto-sync in production.

If port 8080 is already used on your machine (e.g., Jenkins), test via a different local port with port-forward, e.g.:
kubectl -n k8s-minimal port-forward deploy/web 8081:8080
curl http://localhost:8081/


Troubleshooting
App is Synced but Health is Degraded → usually ErrImagePull/ImagePullBackOff.
Make sure the image name/tag in manifests/deployment.yaml or helm/demo-chart/values.yaml matches what you pushed.

Cannot open ArgoCD UI → if you used ... 8082:443, browse to https://localhost:8082;
or use ... 8082:80 and browse to http://localhost:8082.

Multiple ReplicaSets confusing health → re-sync in UI or:
kubectl -n k8s-minimal rollout status deploy/web
kubectl -n k8s-minimal rollout restart deploy/web


Optional: ArgoCD CLI (for reports)
argocd login localhost:8082 --username admin --password '<PASS>' --insecure
argocd app list -o json > reports/report-apps.json   # (ignored by git)
The reports/ folder contains a README with an example JSON shape; real JSON files are ignored by Git.
