# Демонстрація самовідновлення Kubernetes

Показує як Kubernetes автоматично відновлює Pods та підтримує доступність застосунку.

## Передумови

Docker Desktop із увімкненим Kubernetes: Settings → Kubernetes → Enable Kubernetes → Apply & Restart.

Перевірка готовності кластера:

```bash
kubectl get nodes
```

Вузол `docker-desktop` має мати статус `Ready`.

## Розгортання

**1. ConfigMap з HTML сторінкою:**

```bash
kubectl create configmap webapp-html --from-literal=index.html='<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Kubernetes Demo</title>
<style>
  body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: #1a1a2e; color: white; }
  .card { text-align: center; padding: 40px; border-radius: 12px; background: #16213e; box-shadow: 0 0 30px rgba(0,150,255,0.3); }
  h1 { color: #00d4ff; } .pod { color: #ffa500; font-size: 1.2em; }
</style></head>
<body><div class="card">
  <h1>🚀 Kubernetes Demo</h1>
  <p>Цей застосунок працює в Kubernetes</p>
  <p class="pod">ВоФК НУХТ — DevOps курс</p>
</div></body></html>'
```

**2. Deployment з 3 репліками:**

```bash
kubectl create deployment webapp --image=nginx:alpine --replicas=3
kubectl patch deployment webapp --type=json -p='[
  {"op":"add","path":"/spec/template/spec/volumes","value":[{"name":"html","configMap":{"name":"webapp-html"}}]},
  {"op":"add","path":"/spec/template/spec/containers/0/volumeMounts","value":[{"name":"html","mountPath":"/usr/share/nginx/html"}]}
]'
```

**3. Service:**

```bash
kubectl expose deployment webapp --type=NodePort --port=80
```

**4. Дізнатись порт та відкрити у браузері:**

```bash
kubectl get service webapp
```

У колонці `PORT(S)` знайти число після двокрапки, наприклад `80:31234/TCP` — відкрити `http://localhost:31234`.

## Демонстрація

Відкрити поруч термінал і браузер.

**Термінал — спостереження в реальному часі:**

```bash
kubectl get pods -w
```

**Видаляти Pods по одному** (назви підставити зі списку `kubectl get pods`):

```bash
kubectl delete pod <ім'я-пода>
```

**Або всі одразу:**

```bash
kubectl delete pod -l app=webapp
```

У терміналі видно як Pod переходить у `Terminating` і одразу з'являється новий `Pending → ContainerCreating → Running`. Браузер при оновленні (F5) продовжує показувати сторінку без помилок.

## Прибирання після демонстрації

```bash
kubectl delete deployment webapp
kubectl delete service webapp
kubectl delete configmap webapp-html
```
