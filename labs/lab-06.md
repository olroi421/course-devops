# Лабораторна робота 06 Автоматизація розгортання застосунку в Kubernetes

## Мета

Навчитися автоматизувати розгортання застосунків у Kubernetes кластері з використанням CD pipeline. Опанувати техніки blue-green розгортання, налаштування health checks та механізми автоматичного відкату при помилках.

## Завдання

### Рівень 1 (обов'язковий мінімум)

Розширити CI pipeline з попередньої лабораторної роботи та додати CD stage для автоматичного розгортання в Kubernetes staging環境.

Необхідно виконати наступне:

- Налаштувати секрет з kubeconfig для доступу до Kubernetes кластера.
- Створити Kubernetes маніфести для staging оточення (deployment та service).
- Додати CD job до GitHub Actions, який розгортає образ у staging namespace при успішному push до main гілки.
- Переконатися, що конвеєр коректно розгортає нову версію застосунку та оновлює pod.

### Рівень 2 (додаткова функціональність)

Реалізувати blue-green розгортання для production оточення з можливістю ручного перемикання трафіку.

Додатково до рівня 1:

- Створити маніфести для production оточення з двома deployment-ами (blue та green).
- Додати CD job для розгортання у green оточення та перевірки health checks.
- Реалізувати ручний workflow_dispatch для переміщення трафіку з blue на green.
- Налаштувати readiness та liveness probes для автоматичного виявлення помилок pod-ів.

### Рівень 3 (творче розширення)

Додати автоматизовану перевірку здоров'я та механізм автоматичного відкату.

Додатково до рівня 2:

- Реалізувати smoke tests після розгортання для перевірки функціональності.
- Налаштувати автоматичний відкат на попередню версію при невдалих health checks.
- Додати моніторинг та логування розгортання в GitHub Actions.
- Реалізувати граціозне завершення pod-ів при відкаті.

## Критерії оцінювання

### Середній рівень (оцінка "задовільно")

Студент створив базовий CD pipeline, який розгортає застосунок у staging Kubernetes namespace. Маніфести налаштовані базово, проте лишаються порушення найкращих практик (відсутні health checks, лімітування ресурсів). Розгортання відбувається, проте немає контролю якості та перевірки здоров'я. Студент розуміє основні концепції Kubernetes розгортання, але недостатньо глибоко знайомий з blue-green стратегією.

### Достатній рівень (оцінка "добре")

Студент успішно реалізував CD pipeline з розгортанням у staging та production оточенням. Blue-green розгортання налаштоване з ручним перемиканням трафіку. Маніфести містять readiness та liveness probes, лімітування ресурсів та labels. Конвеєр коректно виконується, проте відсутні smoke tests або автоматичний відкат. Студент добре розуміє різницю між staging та production, а також переваги blue-green стратегії.

### Високий рівень (оцінка "відмінно")

Студент розробив повнофункціональний CD pipeline з максимальною надійністю та автоматизацією. Blue-green розгортання повністю інтегровано з smoke tests та автоматичним відкатом при помилках. Маніфести оптимізовані з точки зору масштабування та безпеки. Налаштовано детальне логування та моніторинг. Конвеєр демонструє глибоке розуміння Kubernetes операцій та найкращих практик CD. Звіт содит детальні пояснення обраних рішень та скріншоти процесу розгортання.

## Порядок оформлення та здачі лабораторної роботи

Виконання лабораторної роботи відбувається через GitHub Classroom з фінальним підтвердженням здачі в системі Moodle.

[**GitHub Classroom assignment лабораторної роботи**](https://classroom.github.com/a/b4HawsVh)

Репозиторій повинен містити наступну структуру:

```
lab-06-username/
├── src/
│   ├── app/
│   │   └── app.js (з попередньої лабораторної роботи)
│   ├── tests/
│   │   └── app.test.js
│   ├── k8s/
│   │   ├── staging/
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   │   └── namespace.yaml
│   │   └── production/
│   │       ├── deployment-blue.yaml
│   │       ├── deployment-green.yaml
│   │       ├── service.yaml
│   │       └── namespace.yaml
│   ├── Dockerfile
│   └── .dockerignore
├── .github/
│   └── workflows/
│       ├── ci.yml (з попередньої лабораторної роботи)
│       └── cd.yml (новий CD pipeline)
├── README.md
└── screenshots/
    ├── staging-deployed.png
    ├── blue-green-switch.png
    ├── health-check.png
    └── rollback-logs.png (для рівня 3)
```

Основні файли звіту розташовуються у коренево репозиторію та папці `screenshots/`. Всі Kubernetes маніфести мають знаходитися у папці `src/k8s/` з розділенням на staging та production. Файл `README.md` повинен містити інструкції для налаштування Kubernetes кластера та розгортання.

Після завершення всіх завдань та оформлення звіту необхідно виконати фінальний коміт:

```bash
git add .
git commit -m "lab-06: CD pipeline з blue-green розгортанням"
git push
```

Після відправлення фінального коміту перейдіть до курсу на платформі Moodle та знайдіть завдання лабораторної роботи. Відкрийте завдання для здачі. У текстовому полі для відповіді напишіть слово **виконано**.

## Політика щодо дедлайнів

При порушенні встановленого терміну здачи лабораторної роботи максимальна можлива оцінка становить "добре", незалежно від якості виконаної роботи. Винятки можливі лише за поважних причин, підтверджених документально.

## Теоретичні відомості

### Continuous Delivery vs Continuous Deployment

Continuous Delivery (CD) та Continuous Deployment часто плутають, проте вони мають важливі відмінності:

**Continuous Delivery** — це практика, при якій код автоматично збирається, тестується та готується для розгортання, проте розгортання у production виконується вручну під керуванням операційної команди. Це забезпечує людський контроль над критичними змінами, що підходить для більшості enterprise систем. На кожному етапі может бути механізм затвердження (approval gate).

**Continuous Deployment** — це крайній випадок, коли кожна версія, яка пройде всі автоматичні тести, автоматично розгортається у production без ручного втручання. Це потребує дуже надійної системи тестування та моніторингу, але дозволяє найшвидше доставляти нові функції кінцевим користувачам.

Для більшості організацій Continuous Delivery є оптимальним балансом між швидкістю та безпекою. Це дозволяє команді контролювати той момент, коли нова версія виходить у production, при цьому автоматизуючи всі технічні аспекти процесу.

### Blue-Green розгортання

Blue-Green розгортання — це стратегія розгортання, яка зменшує ризик та дозволяє швидкий відкат при проблемах. Основна ідея полягає у наявності двох ідентичних production оточень:

- **Blue** — поточна версія застосунку, яка обслуговує реальний трафік.
- **Green** — нова версія застосунку, яка розгортається, але ще не отримує трафік.

Процес розгортання виглядає наступним чином:

1. Нова версія розгортається в Green оточенні.
2. Виконуються smoke tests та перевірки здоров'я Green оточення.
3. Якщо все у порядку, трафік переміщується з Blue на Green (часто за допомогою оновлення Service selector або ingress).
4. Blue оточення залишається у постійній готовності як аварійний запас для відкату.
5. При необхідності відкату, трафік миттєво переміщується назад на Blue.

Основні переваги blue-green розгортання:

- **Нульовий час простою** — трафік переміщується миттєво без значних перерв.
- **Швидкий відкат** — якщо нова версія мала проблеми, просто переміщуємо трафік назад на старе оточення.
- **Тестування у production** — можна виконувати детальне тестування нової версії в реальному оточенні перед переміщенням трафіку.
- **А/В тестування** — можна розділити трафік між blue та green для поступового впровадження.

Недоліки:

- **Подвійні ресурси** — потребує вдвічі більше серверів/pod-ів для запуску одночасно.
- **Складність управління** — потребує більше уваги до синхронізації конфігурацій та даних.

### Rolling vs Blue-Green vs Canary розгортання

Існує кілька популярних стратегій розгортання, кожна з яких має свої переваги та недоліки:

| Характеристика | Rolling | Blue-Green | Canary |
|---|---|---|---|
| **Час простою** | Мінімальний | Нульовий | Нульовий |
| **Ресурси** | Мінімум | Вдвічі більше | Розділені |
| **Складність** | Проста | Середня | Складна |
| **Відкат** | Медленний | Миттєвий | Поступовий |
| **Тестування** | На продакшні | Перед переходом | На фракції трафіку |
| **Ризик** | Середній | Низький | Дуже низький |

**Rolling розгортання** — поступово замінюють старі pod-и на нові. При проблемі можна зупинити процес, проте старі версії вже працюють на деяких pod-ах.

**Canary розгортання** — розгортають нову версію та направляють невелику частину трафіку (2-5%) на новий pod. Якщо помилок немає, поступово збільшують долю трафіку. Дозволяє виявити проблеми на малій фракції користувачів.

### Health Checks у Kubernetes

Health checks забезпечують, що Kubernetes розуміє, коли pod помер або занедужав, та може автоматично його перезавантажити або вилучити з балансування навантаження.

**Liveness Probe** перевіряє, чи контейнер ще живий. Якщо liveness probe невдала, Kubernetes перезавантажує контейнер:

```yaml
livenessProbe:
  httpGet:
    path: /api/health
    port: 3000
  initialDelaySeconds: 10
  periodSeconds: 10
  timeoutSeconds: 3
  failureThreshold: 3
```

**Readiness Probe** перевіряє, чи готовий контейнер приймати трафік. Якщо readiness probe невдала, pod видаляється з Service, але контейнер не перезавантажується:

```yaml
readinessProbe:
  httpGet:
    path: /api/health
    port: 3000
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 2
  failureThreshold: 2
```

Параметри:

- `initialDelaySeconds` — час очікування перед першою перевіркою (дозволяє застосунку стартувати).
- `periodSeconds` — інтервал між перевірками.
- `timeoutSeconds` — максимальний час чекання на відповідь.
- `failureThreshold` — скільки невдалих спроб перш ніж вважати pod небезпечним.

### Механізм відкату в Kubernetes та GitHub Actions

Відкат у Kubernetes можна виконати кількома способами:

**kubectl rollout undo** — повертає deployment до попередньої версії:

```bash
kubectl rollout undo deployment/app -n production
```

**Revision history** — зберігає історію попередніх версій deployment-у:

```bash
kubectl rollout history deployment/app -n production
kubectl rollout undo deployment/app --to-revision=2 -n production
```

У GitHub Actions можна автоматизувати відкат при помилці:

```yaml
- name: Rollback on failure
  if: failure()
  run: |
    kubectl rollout undo deployment/app-green -n production
    kubectl rollout status deployment/app-green -n production
```

### Smoke Tests та поточна перевірка

Smoke tests — це набір коротких функціональних тестів, які перевіряють базову функціональність застосунку після розгортання. На відміну від юніт-тестів, вони запускаються проти справжнього розгорнутого середовища.

Приклад smoke test у GitHub Actions:

```bash
#!/bin/bash
set -e

HEALTH_URL="http://app-service.production:3000/api/health"
TIMEOUT=30

echo "Waiting for service to become healthy..."
for i in $(seq 1 $TIMEOUT); do
  if curl -s "$HEALTH_URL" | grep -q "healthy"; then
    echo "Service is healthy!"
    exit 0
  fi
  echo "Attempt $i/$TIMEOUT..."
  sleep 1
done

echo "Service health check failed!"
exit 1
```

## Хід роботи

### Клонування репозиторію

```bash
git clone git@github.com:organization/lab-06-username.git
cd lab-06-username
```

### Крок 1: Підготовка структури проєкту

Скопіюйте файли з попередньої лабораторної роботи (CI pipeline) та додайте нові директорії для Kubernetes маніфестів:

```bash
mkdir -p src/k8s/staging src/k8s/production screenshots
```

### Крок 2: Налаштування Kubernetes кластера

Якщо у вас немає локального Kubernetes кластера, встановіть minikube або Docker Desktop з вбудованим Kubernetes:

```bash
# Для minikube
minikube start --driver=docker

# Або для Docker Desktop
# Увімкніть Kubernetes у Docker Desktop Settings
```

Перевірте, що кластер запущений:

```bash
kubectl cluster-info
kubectl get nodes
```

### Крок 3: Створення маніфестів для staging оточення

Створіть файл `src/k8s/staging/namespace.yaml`:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: staging
  labels:
    environment: staging
```

Створіть файл `src/k8s/staging/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  namespace: staging
  labels:
    app: app
    environment: staging
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: app
      environment: staging
  template:
    metadata:
      labels:
        app: app
        environment: staging
    spec:
      containers:
      - name: app
        image: ghcr.io/organization/lab-05-username:main
        imagePullPolicy: Always
        ports:
        - name: http
          containerPort: 3000
          protocol: TCP
        env:
        - name: ENVIRONMENT
          value: staging
        - name: LOG_LEVEL
          value: debug
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        readinessProbe:
          httpGet:
            path: /api/health
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 2
          failureThreshold: 2
        livenessProbe:
          httpGet:
            path: /api/health
            port: http
          initialDelaySeconds: 10
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 3
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
```

Створіть файл `src/k8s/staging/service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: app-service
  namespace: staging
  labels:
    app: app
    environment: staging
spec:
  type: ClusterIP
  selector:
    app: app
    environment: staging
  ports:
  - name: http
    protocol: TCP
    port: 80
    targetPort: http
```

### Крок 4: Створення маніфестів для production оточення

Створіть файл `src/k8s/production/namespace.yaml`:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    environment: production
```

Створіть файл `src/k8s/production/deployment-blue.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
  namespace: production
  labels:
    app: app
    environment: production
    version: blue
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: app
      version: blue
  template:
    metadata:
      labels:
        app: app
        environment: production
        version: blue
    spec:
      terminationGracePeriodSeconds: 30
      containers:
      - name: app
        image: ghcr.io/organization/lab-05-username:main
        imagePullPolicy: Always
        ports:
        - name: http
          containerPort: 3000
          protocol: TCP
        env:
        - name: ENVIRONMENT
          value: production
        - name: LOG_LEVEL
          value: info
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "1000m"
        readinessProbe:
          httpGet:
            path: /api/health
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 2
          failureThreshold: 2
        livenessProbe:
          httpGet:
            path: /api/health
            port: http
          initialDelaySeconds: 15
          periodSeconds: 15
          timeoutSeconds: 3
          failureThreshold: 3
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
```

Створіть файл `src/k8s/production/deployment-green.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-green
  namespace: production
  labels:
    app: app
    environment: production
    version: green
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: app
      version: green
  template:
    metadata:
      labels:
        app: app
        environment: production
        version: green
    spec:
      terminationGracePeriodSeconds: 30
      containers:
      - name: app
        image: ghcr.io/organization/lab-05-username:main
        imagePullPolicy: Always
        ports:
        - name: http
          containerPort: 3000
          protocol: TCP
        env:
        - name: ENVIRONMENT
          value: production
        - name: LOG_LEVEL
          value: info
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "1000m"
        readinessProbe:
          httpGet:
            path: /api/health
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 2
          failureThreshold: 2
        livenessProbe:
          httpGet:
            path: /api/health
            port: http
          initialDelaySeconds: 15
          periodSeconds: 15
          timeoutSeconds: 3
          failureThreshold: 3
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
```

Створіть файл `src/k8s/production/service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: app-service
  namespace: production
  labels:
    app: app
    environment: production
spec:
  type: LoadBalancer
  selector:
    app: app
    version: blue
  ports:
  - name: http
    protocol: TCP
    port: 80
    targetPort: http
```

### Крок 5: Налаштування GitHub Actions для доступу до Kubernetes

Отримайте kubeconfig з вашого Kubernetes кластера:

```bash
# Для minikube
minikube update-context

# Отримайте вміст kubeconfig
cat ~/.kube/config | base64
```

Додайте секрет `KUBE_CONFIG` у GitHub репозиторію (Settings → Secrets and variables → Actions):

```
base64-encoded kubeconfig content
```

### Крок 6: Створення CD workflow

Створіть файл `.github/workflows/cd.yml`:

```yaml
name: CD Pipeline

on:
  workflow_run:
    workflows: ["CI Pipeline"]
    types:
      - completed
    branches:
      - main
  workflow_dispatch:

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    if: github.event.workflow_run.conclusion == 'success' || github.event_name == 'workflow_dispatch'
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: latest

      - name: Create kubeconfig
        run: |
          mkdir -p $HOME/.kube
          echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > $HOME/.kube/config
          chmod 600 $HOME/.kube/config

      - name: Create staging namespace
        run: |
          kubectl apply -f src/k8s/staging/namespace.yaml

      - name: Deploy to staging
        run: |
          kubectl apply -f src/k8s/staging/deployment.yaml
          kubectl apply -f src/k8s/staging/service.yaml

      - name: Wait for deployment
        run: |
          kubectl rollout status deployment/app -n staging --timeout=5m

      - name: Check pod health
        run: |
          kubectl get pods -n staging -o wide

  deploy-production:
    name: Deploy to Production (Green)
    runs-on: ubuntu-latest
    needs: deploy-staging
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: latest

      - name: Create kubeconfig
        run: |
          mkdir -p $HOME/.kube
          echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > $HOME/.kube/config
          chmod 600 $HOME/.kube/config

      - name: Create production namespace
        run: |
          kubectl apply -f src/k8s/production/namespace.yaml

      - name: Deploy green environment
        run: |
          kubectl apply -f src/k8s/production/deployment-green.yaml
          kubectl apply -f src/k8s/production/service.yaml

      - name: Wait for green deployment
        run: |
          kubectl rollout status deployment/app-green -n production --timeout=5m

      - name: Run smoke tests
        continue-on-error: true
        run: |
          POD_NAME=$(kubectl get pods -n production -l version=green -o jsonpath='{.items[0].metadata.name}')
          kubectl exec -n production $POD_NAME -- curl -s http://localhost:3000/api/health | grep healthy

      - name: Check green pod health
        run: |
          kubectl get pods -n production -l version=green -o wide

  switch-traffic:
    name: Switch Traffic to Green
    runs-on: ubuntu-latest
    needs: deploy-production
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: latest

      - name: Create kubeconfig
        run: |
          mkdir -p $HOME/.kube
          echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > $HOME/.kube/config
          chmod 600 $HOME/.kube/config

      - name: Switch traffic to green
        run: |
          kubectl patch service app-service -n production -p '{"spec":{"selector":{"version":"green"}}}'
          echo "Traffic switched to green deployment"

      - name: Verify traffic switch
        run: |
          kubectl get service app-service -n production -o jsonpath='{.spec.selector}'
```

### Крок 7: Створення workflow для ручного відкату

Додайте файл `.github/workflows/rollback.yml`:

```yaml
name: Manual Rollback

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to rollback'
        required: true
        default: 'production'
        type: choice
        options:
          - staging
          - production

jobs:
  rollback:
    name: Rollback Deployment
    runs-on: ubuntu-latest
    steps:
      - name: Setup kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: latest

      - name: Create kubeconfig
        run: |
          mkdir -p $HOME/.kube
          echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > $HOME/.kube/config
          chmod 600 $HOME/.kube/config

      - name: Rollback deployment
        run: |
          ENVIRONMENT=${{ github.event.inputs.environment }}
          if [ "$ENVIRONMENT" = "production" ]; then
            echo "Switching traffic back to blue..."
            kubectl patch service app-service -n production -p '{"spec":{"selector":{"version":"blue"}}}'
          else
            echo "Rolling back staging deployment..."
            kubectl rollout undo deployment/app -n staging
          fi

      - name: Verify rollback
        run: |
          ENVIRONMENT=${{ github.event.inputs.environment }}
          if [ "$ENVIRONMENT" = "production" ]; then
            kubectl get service app-service -n production -o jsonpath='{.spec.selector}'
          else
            kubectl rollout status deployment/app -n staging
          fi
```

### Крок 8: Локальне тестування Kubernetes розгортання

Розгорніть маніфести локально:

```bash
# Застосуйте staging
kubectl apply -f src/k8s/staging/

# Перевірте pod-и
kubectl get pods -n staging
kubectl logs -n staging -f deployment/app

# Проксуйте service для локального доступу
kubectl port-forward -n staging svc/app-service 8080:80
curl http://localhost:8080/api/health

# Застосуйте production
kubectl apply -f src/k8s/production/

# Перевірте обидва deployment-и
kubectl get pods -n production
kubectl get deployment -n production
```

Тестуйте health checks:

```bash
# Перевірте готовність pod-ів
kubectl get pods -n staging
kubectl describe pod -n staging <pod-name>

# Отримайте логи
kubectl logs -n staging deployment/app
```

### Крок 9: Оформлення звіту

Скопіюйте скріншоти успішного розгортання до папки `screenshots/`:

- `staging-deployed.png` — скріншот `kubectl get pods -n staging` та успішного розгортання.
- `blue-green-switch.png` — скріншот перемикання трафіку в GitHub Actions.
- `health-check.png` — скріншот виконання health checks та pod status.
- `rollback-logs.png` — скріншот логів при відкаті (для рівня 3).

Створіть або оновіть файл `README.md`:

```markdown
# Lab 06: CD Pipeline з Blue-Green Розгортанням

## Опис

Автоматизований конвеєр для розгортання застосунку в Kubernetes з blue-green стратегією.

## Локальне налаштування

### Встановлення Kubernetes

docker desktop enable kubernetes
# або
minikube start --driver=docker

### Розгортання

kubectl apply -f src/k8s/staging/
kubectl apply -f src/k8s/production/

### Проксування

kubectl port-forward -n staging svc/app-service 8080:80
curl http://localhost:8080/api/health
```

Виконайте фінальний коміт:

```bash
git add .
git commit -m "lab-06: CD pipeline з blue-green розгортанням в Kubernetes"
git push
```

## Шаблон звіту

```markdown
# Лабораторна робота 06: Автоматизація розгортання в Kubernetes

**Виконав:** ПІБ, група

## Хід виконання

### Рівень 1: Базове розгортання у staging

1. Налаштував kubeconfig secret у GitHub Actions.
2. Створив Kubernetes маніфести для staging оточення.
3. Додав CD job для автоматичного розгортання при push до main.
4. Розгортання успішно виконується та pod-и стають готовими.

[Скріншот: staging-deployed.png]

### Рівень 2: Blue-Green розгортання в production

1. Створив два deployment-и (blue та green) для production.
2. Реалізував Service з переключенням версії за допомогою label selector.
3. Додав smoke tests для перевірки здоров'я after deployment.
4. Налаштував health checks (readiness та liveness probes).

[Скріншот: blue-green-switch.png]
[Скріншот: health-check.png]

### Рівень 3: Автоматичний відкат та моніторинг

1. Додав workflow для ручного відкату на blue при проблемах.
2. Налаштував терміни для graceful shutdown pod-ів.
3. Додав детальне логування кожного етапу розгортання.

[Скріншот: rollback-logs.png]

## Висновки

У цій лабораторній роботі я реалізував повнофункціональний CD pipeline з blue-green розгортанням, що дозволяє безпечно розгортати нові версії з можливістю миттєвого відкату. Розуміюю важливість health checks та механізмів відкату для надійної production системи.
```

## Контрольні запитання

1. Поясніть різницю між Continuous Delivery та Continuous Deployment та надайте приклад, коли кожен підхід є більш доречним.
2. Опишіть процес blue-green розгортання та його переваги порівняно з rolling розгортанням.
3. Яка різниця між readiness та liveness probes у Kubernetes та як вони впливають на розгортання?
4. Як налаштувати автоматичний відкат при невдалих health checks у Kubernetes та GitHub Actions?
5. Поясніть, що таке smoke tests та чому вони важливі при CD pipeline.
6. Як налаштувати graceful shutdown pod-ів та чому це критично для уникнення втрати даних?
7. Поясніть, як використовується label selector у Service для перемикання трафіку між blue та green deployment-ами.
