# Лабораторна робота 09 Інтеграція security сканування та управління секретами

## Мета

Усвідомити важливість безпеки на ранніх етапах розробки (shift-left), навчитися інтегрувати автоматичне сканування уразливостей образів та коду у CI pipeline, а також опанувати управління секретами у контейнерному оточенні та Kubernetes кластері.

## Завдання

### Рівень 1 (обов'язковий мінімум)

Реалізовано базову безпеку у DevOps потоці.
Необхідно виконати наступне:

- Додати Trivy сканування Docker образів до GitHub Actions pipeline.
- Налаштувати секретне сховище для credentials та підключити Kubernetes Secret до Deployment.
- Переглянути та інтерпретувати звіти сканування (SARIF формат).
- Переконатися, що secret значення не зберігаються у Git репозиторії та маніфестах.

### Рівень 2 (додаткова функціональність)

Посилена безпека с інтеграцією SAST сканування та Sealed Secrets.
Додатково до рівня 1:

- Інтегрувати Semgrep (або CodeQL) для аналізу коду на безпеку у pipeline.
- Встановити та налаштувати Sealed Secrets (Bitnami) для безпечного зберігання шифрованих секретів у Git.
- Порівняти підходи управління секретами (Kubernetes Secret vs Sealed Secret).

### Рівень 3 (творче розширення)

Повна реалізація розширених механізмів безпеки Kubernetes.
Додатково до рівня 2:

- Налаштувати RBAC (Role-Based Access Control) у Kubernetes: ServiceAccount, Role, RoleBinding.
- Визначити мережеві політики (NetworkPolicy) для обмеження трафіку між подами.
- Проаналізувати та зареєструвати результати всіх сканувань безпеки у звіті.

## Критерії оцінювання

### Середній рівень (оцінка "задовільно")

Студент успішно додав Trivy до pipeline та побачив звіт сканування. Kubernetes Secret налаштований та підключений до Deployment. У звіті описані основні компоненти безпеки та виявлені уразливості. Робота демонструє розуміння базових концепцій shift-left та управління секретами, але може мати неповноту у документуванні та аналізі.

### Достатній рівень (оцінка "добре")

Крім рівня 1, реалізовано SAST сканування (Semgrep або CodeQL) у pipeline та детально документовано результати обох сканувань. Sealed Secrets встановлений та функціональний. Звіт містить чіткий опис процесу внесення Trivy та Sealed Secrets, результати сканування, порівняння підходів до управління секретами. Маніфести чисті від чутливих даних, всі кроки легко відтворюють.

### Високий рівень (оцінка "відмінно")

Повна реалізація всіх трьох рівнів: Trivy, Semgrep, Sealed Secrets функціональні та інтегровані. RBAC та NetworkPolicy налаштовані та протестовані. Звіт глибокий, містить аналіз конкретних уразливостей, вибір мітигації, скрімшоти работающих pipeline та Kubernetes ресурсів. Демонструється розуміння взаємодії компонентів безпеки та їх ролі у DevOps процесі. Код та маніфести відповідають best practices.

## Порядок оформлення та здачі лабораторної роботи

Виконання лабораторної роботи відбувається через GitHub Classroom з фінальним підтвердженням здачі в системі Moodle.

[**GitHub Classroom assignment лабораторної роботи**](https://classroom.github.com/a/PLACEHOLDER_LAB_09)

Репозиторій містить структуру:

```
src/
├── Dockerfile
├── .github/workflows/
│   └── security-scan.yml
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── secret.yaml          (для локального тестування, НЕ комітити реальні секрети!)
│   ├── sealed-secret.yaml   (безпечна версія, комітити безпечно)
│   └── rbac/
│       ├── serviceaccount.yaml
│       ├── role.yaml
│       └── rolebinding.yaml
└── README.md
k8s/
└── network-policy.yaml
```

Після завершення всіх завдань та оформлення звіту необхідно виконати фінальний коміт, який зафіксує остаточний стан вашої роботи. Після відправлення фінального коміту перейдіть до курсу на платформі Moodle та знайдіть завдання лабораторної роботи. Відкрийте завдання для здачі. У текстовому полі для відповіді напишіть слово **виконано**.

## Політика щодо дедлайнів

При порушенні встановленого терміну здачі лабораторної роботи максимальна можлива оцінка становить "добре", незалежно від якості виконаної роботи. Винятки можливі лише за поважних причин, підтверджених документально.

## Теоретичні відомості

### Концепція shift-left безпеки

Shift-left безпеки — це методологія, яка переміщує перевірки безпеки на ранні етапи розробки замість того, щоб залишати їх на завершальні стадії тестування або впровадження. У традиційному підході (shift-right) уразливості виявляються пізно, коли виправлення обходиться дорого. Shift-left включає сканування коду розробниками під час написання, контроль залежностей, сканування образів перед розгортанням та автоматизацію вразливості у CI/CD pipeline.

Переваги shift-left: розробники отримують швидкий зворотний зв'язок про проблеми безпеки, вартість виправлення значно менша на ранніх стадіях, зменшується кількість уразливостей у production, команда розвивається у правильних практиках. DevOps інженери можуть вбудовувати контроль якості та безпеки в автоматизовані pipeline без ручного втручання. Культура безпеки стає частиною розробки, а не окремим процесом в кінці.

### SAST, DAST та SCA: відмінності та інструменти

SAST (Static Application Security Testing) аналізує вихідний код без його виконання, шукаючи типові вразливості кодування (SQL injection, XSS, buffer overflow тощо). Інструменти включають Semgrep, SonarQube, Checkmarx. SAST швидкий, не вимагає запуску приложення, але може генерувати false positives.

DAST (Dynamic Application Security Testing) тестує вебзастосунок під час його роботи, імітуючи напади реальних зловмисників (скан портів, fuzz testing, exploitation). Інструменти включають OWASP ZAP, Burp Suite. DAST знаходить реальні вразливості в runtime, але повільний та вимагає запущеного сервісу.

SCA (Software Composition Analysis) сканує залежності проєкту (npm пакети, pip модулі, Maven артефакти) на наявність відомих уразливостей у базах CVE. Інструменти включають Snyk, OWASP Dependency-Check, GitHub Dependabot. SCA критично важливий, оскільки більшість проєктів залежать від третьосторонніх бібліотек.

Для DevOps потоку часто поєднуються всі три підходи: розробник запускає SAST локально, CI/CD запускає SCA при push, DAST та Trivy (образи) запускаються перед розгортанням.

### Управління секретами: принципи та best practices

Секрети (passwords, API ключі, tokens, certificates) — найкритичніший актив у сучасних системах. Основні принципи управління:

**Ніколи не зберігайте секрети в Git.** Зберігайте приватні keys, passwords у спеціальних сховищах (GitHub Secrets, HashiCorp Vault, AWS Secrets Manager), не в кодоумовах. Git історія永遠 залишається, видалення файлу не забезпечує безпеку.

**Rotation.** Секрети повинні регулярно змінюватися. Якщо виникне компрометація, вплив обмежується часом після ротації.

**Least Privilege.** Процес, контейнер або користувач повинні мати мінімально необхідні дозволи для роботи. Якщо додаток тільки читає базу, він не повинен мати права видалення.

**Шифрування.** Секрети повинні зберігатися та передаватися в зашифрованому вигляді. TLS для транспорту, шифрування at-rest у сховищі.

**Аудит.** Логуйте доступ до секретів, хто та коли їх прочитав, для виявлення аномалій.

### Kubernetes Secrets та обмеження

Kubernetes Secrets — це ресурси для зберігання чутливих даних (passwords, tokens, configs) у кластері. Вони зберігаються у базі etcd, але за замовчуванням **не шифруються** — лише кодуються base64, що є рівнем безпеки тільки від випадкового перегляду. Доступ контролюється RBAC, але адміністратор може прочитати raw etcd.

Типи Secrets:

- **Opaque** (default): довільні дані, кодовані base64.
- **docker-registry**: credentials для приватних Docker реєстрів.
- **tls**: сертифікати та ключі для TLS.
- **basic-auth**: username та password.

Приклад Kubernetes Secret:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  DB_PASSWORD: cGFzc3dvcmQxMjM=  # base64 закодований пароль
  API_KEY: YWJjZGVmZ2hpams=
```

Pod підключається до Secret через environment variables або volume:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  containers:
  - name: app
    image: myapp:latest
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: app-secrets
          key: DB_PASSWORD
```

Обмеження: base64 кодування не є шифруванням, Secrets зберігаються без шифрування у etcd, розроблювачі можуть побачити декодовані значення у pod описах. Для більшої безпеки використовуйте Sealed Secrets або зовнішні сховища ключів.

### Sealed Secrets: схема роботи та інтеграція

Sealed Secrets (Bitnami) — це розширення Kubernetes, яке дозволяє шифрувати Secret значення так, щоб лише конкретний Kubernetes кластер міг їх розшифрувати. Це дозволяє безпечно зберігати зашифровані Secrets у Git репозиторії.

Архітектура:

```
┌─────────────┐
│ Developer   │
└──────┬──────┘
       │ kubeseal (public key)
       ▼
┌─────────────────┐
│ SealedSecret    │  ← зберігаємо в Git, безпечно
└─────────────────┘
       │ Sealed Secret Controller (private key in cluster)
       ▼
┌─────────────────┐
│ Secret (etcd)   │  ← розшифрований лише в cluster
└─────────────────┘
```

Процес:

1. Встановити Sealed Secrets controller у Kubernetes.
2. Отримати public key з кластера за допомогою kubeseal.
3. Закодувати Secret с kubeseal, отримати SealedSecret YAML.
4. Комітити SealedSecret безпечно у Git.
5. Pod звертається до Secret як звичайно, controller розшифровує SealedSecret та створює Secret.

Приклад:

```bash
# Створити звичайний Secret
echo -n "mypassword" | kubectl create secret generic app-secret --from-file=password=/dev/stdin --dry-run=client -o yaml > secret.yaml

# Запечатати його
kubeseal < secret.yaml > sealed-secret.yaml

# Комітити лишь sealed-secret.yaml
git add sealed-secret.yaml
git commit -m "Add sealed secrets"
```

Sealed Secrets дає більше безпеки ніж базові Secrets, але потребує встановлення додаткового контролера та управління ключами.

### RBAC у Kubernetes: ServiceAccount, Role, RoleBinding

RBAC (Role-Based Access Control) — це механізм контролю доступу в Kubernetes, який визначає, хто (Subject) може робити що (Verb) з якими ресурсами (Resource). Основні компоненти:

**Subject**: користувач, група або ServiceAccount (для processes у cluster).

**Role** або **ClusterRole**: набір дозволів (rules). Role обмежений простором імен (namespace), ClusterRole глобальний.

**RoleBinding** або **ClusterRoleBinding**: зв'язує Subject до Role.

Приклад Role:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: default
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
```

RoleBinding:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: default
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: pod-reader
subjects:
- kind: ServiceAccount
  name: app-sa
  namespace: default
```

ServiceAccount для контейнера:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
  namespace: default
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  template:
    spec:
      serviceAccountName: app-sa
      containers:
      - name: app
        image: myapp:latest
```

RBAC дозволяє реалізувати Least Privilege: контейнер Deployment-a отримує лишь потрібні дозволи для API сервера.

### NetworkPolicy та мережева безпека

NetworkPolicy — це Kubernetes ресурс для визначення мережевих правил трафіку між podами. За замовчуванням, всі pod-и можуть спілкуватися один з одним. NetworkPolicy обмежує трафік на базі label selector.

Приклад NetworkPolicy, яка дозволяє лишь frontened pod-ам спілкуватися з backend:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
```

Цей поліс дозволяє:

- Ingress: frontend (app: frontend) до backend на порту 8080.
- Egress: backend до database на порту 5432.

NetworkPolicy потребує мережевого плагіну (CNI), який її підтримує (Calico, Cilium, Flannel не підтримує). У Minikube використовуйте `minikube start --network-plugin=cni`.

Mermaid схема DevSecOps pipeline:

```mermaid
graph TD
    A["Developer Push Code"] -->|GitHub Actions| B["SAST Scan<br/>Semgrep/CodeQL"]
    B -->|Vulnerabilities Found| C["Report & Block if Critical"]
    C -->|Pass| D["Build Docker Image"]
    D -->|Trivy Scan| E["Image Vulnerability Check"]
    E -->|Pass| F["Push to Registry"]
    F -->|ArgoCD/Manual Deploy| G["Kubernetes Cluster"]
    G -->|Pod with Secret| H["Secret/SealedSecret Mount"]
    H -->|RBAC Check| I["ServiceAccount Permissions"]
    I -->|NetworkPolicy| J["Network Isolation"]
    J -->|Secure Pod Running| K["Logs & Audit"]
    style B fill:#ff9999
    style E fill:#ff9999
    style H fill:#99ccff
    style I fill:#99ccff
    style J fill:#99ccff
```

## Хід роботи

### Клонування репозиторію

```bash
git clone <GitHub Classroom URL>
cd <repository-name>
```

### Крок 1. Підготовка Docker образу з вразливостями

Переконайтесь, що у папці `src/` є `Dockerfile`. Для демонстрації, скажімо, використовуємо Node.js образ з деякими залежностями:

```dockerfile
FROM node:16

WORKDIR /app

COPY package.json .
RUN npm install

COPY . .

EXPOSE 3000
CMD ["node", "server.js"]
```

`package.json` може містити залежності, які мають відомі уразливості (для демонстрації):

```json
{
  "name": "vulnerable-app",
  "version": "1.0.0",
  "dependencies": {
    "express": "4.17.1",
    "lodash": "4.17.15"
  }
}
```

### Крок 2. Налаштування Trivy у GitHub Actions

Створіть файл `.github/workflows/security-scan.yml`:

```yaml
name: Security Scanning

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  trivy-scan:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Build Docker image
      run: |
        docker build -t myapp:latest .
    
    - name: Run Trivy vulnerability scan
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: myapp:latest
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy results to GitHub
      uses: github/codeql-action/upload-sarif@v2
      if: always()
      with:
        sarif_file: 'trivy-results.sarif'
    
    - name: Display Trivy results
      run: |
        docker run --rm -v $PWD:/root aquasec/trivy image --format table myapp:latest
```

Поштовхніть цей файл до Git:

```bash
git add .github/workflows/security-scan.yml
git commit -m "Add Trivy vulnerability scanning to pipeline"
git push
```

Перейдіть на GitHub у закладку "Actions" та переглядайте результати сканування. GitHub автоматично покаже знайдені уразливості.

### Крок 3. Розгляд Trivy звіту

GitHub Security tab показує всі виявлені уразливості, їх severity (Critical, High, Medium, Low), та рекомендації щодо обновлення залежностей. SARIF файл містить структурований звіт, який можна аналізувати програмно.

Интерпретуйте результати:

- **Critical**: одразу обновити залежність.
- **High**: обновити у найближчий sprint.
- **Medium/Low**: планувати обновлення, не критично.

### Крок 4. Налаштування Kubernetes Secret

Створіть файл `src/k8s/secret.yaml` для локального тестування (НЕ комітити реальні секрети!):

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-credentials
  namespace: default
type: Opaque
stringData:
  DATABASE_URL: "postgres://user:pass@localhost:5432/mydb"
  API_KEY: "secret-api-key-12345"
  JWT_SECRET: "jwt-secret-key"
```

Застосуйте Secret у Minikube:

```bash
kubectl apply -f src/k8s/secret.yaml
kubectl get secrets
kubectl describe secret app-credentials
```

### Крок 5. Налаштування Deployment для використання Secret

Модифікуйте або створіть `src/k8s/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 3000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-credentials
              key: DATABASE_URL
        - name: API_KEY
          valueFrom:
            secretKeyRef:
              name: app-credentials
              key: API_KEY
        - name: JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: app-credentials
              key: JWT_SECRET
```

Розгорніть:

```bash
kubectl apply -f src/k8s/deployment.yaml
kubectl get pods
kubectl logs <pod-name>
```

Перевірте, що pod правильно отримує Secret значення:

```bash
kubectl exec <pod-name> -- env | grep API_KEY
```

### Крок 6 (Рівень 2). Інтеграція Semgrep у pipeline

Додайте SAST сканування до `.github/workflows/security-scan.yml`:

```yaml
  semgrep-scan:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Run Semgrep SAST scan
      uses: returntocorp/semgrep-action@v1
      with:
        generateSarif: true
    
    - name: Upload Semgrep SARIF
      uses: github/codeql-action/upload-sarif@v2
      if: always()
      with:
        sarif_file: 'semgrep.sarif'
```

Поштовхніть та розгляньте результати SAST сканування на GitHub Security tab.

### Крок 7 (Рівень 2). Встановлення Sealed Secrets

Встановіть Sealed Secrets controller у Minikube:

```bash
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/controller.yaml

# Перевірте встановлення
kubectl get deployment -n kube-system sealed-secrets-controller
```

Завантажте kubeseal CLI:

```bash
wget https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/kubeseal-0.24.0-linux-amd64.tar.gz
tar xfz kubeseal-0.24.0-linux-amd64.tar.gz
sudo mv kubeseal /usr/local/bin/
```

### Крок 8 (Рівень 2). Створення SealedSecret

Створіть звичайний Secret YAML:

```bash
cat > secret.yaml << EOF
apiVersion: v1
kind: Secret
metadata:
  name: app-credentials
  namespace: default
type: Opaque
stringData:
  DATABASE_URL: "postgres://user:pass@localhost:5432/mydb"
  API_KEY: "secret-api-key-12345"
EOF
```

Запечатайте його:

```bash
kubeseal -f secret.yaml -w sealed-secret.yaml
```

Переглядайте вміст `sealed-secret.yaml` — тепер значення зашифровані. Комітьте лише `sealed-secret.yaml`:

```bash
git add src/k8s/sealed-secret.yaml
git commit -m "Add sealed secrets (encrypted)"
git push
```

Не комітьте звичайний `secret.yaml`! Додайте до `.gitignore`:

```bash
echo "src/k8s/secret.yaml" >> .gitignore
git add .gitignore
git commit -m "Ignore raw secrets"
git push
```

Застосуйте SealedSecret у Minikube:

```bash
kubectl apply -f src/k8s/sealed-secret.yaml
kubectl get sealedsecrets
kubectl get secrets
```

Controller автоматично розшифрує та створить Secret.

### Крок 9 (Рівень 3). Налаштування RBAC

Створіть ServiceAccount:

```yaml
# src/k8s/rbac/serviceaccount.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
  namespace: default
```

Role для читання configmaps та secrets:

```yaml
# src/k8s/rbac/role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-role
  namespace: default
rules:
- apiGroups: [""]
  resources: ["secrets", "configmaps"]
  verbs: ["get", "list"]
- apiGroups: [""]
  resources: ["pods", "pods/logs"]
  verbs: ["get", "list"]
```

RoleBinding:

```yaml
# src/k8s/rbac/rolebinding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-rolebinding
  namespace: default
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: app-role
subjects:
- kind: ServiceAccount
  name: app-sa
  namespace: default
```

Застосуйте:

```bash
kubectl apply -f src/k8s/rbac/
```

Модифікуйте Deployment для використання ServiceAccount:

```yaml
spec:
  template:
    spec:
      serviceAccountName: app-sa
      containers:
      - name: app
        image: myapp:latest
```

Протестуйте доступ:

```bash
kubectl exec <pod-name> -- kubectl get secrets
kubectl exec <pod-name> -- kubectl delete secrets app-credentials  # Має бути заблоковано
```

### Крок 10 (Рівень 3). NetworkPolicy

Створіть `src/k8s/network-policy.yaml`:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: app-network-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 3000
  egress:
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 443
    - protocol: TCP
      port: 5432
```

Застосуйте:

```bash
kubectl apply -f src/k8s/network-policy.yaml
kubectl get networkpolicies
```

Перевірте залежи від мережевого плагіну. Якщо використовуєте Minikube без CNI, NetworkPolicy не матимуть ефекту.

### Крок 11. Оформлення звіту

У репозиторії створіть файл `REPORT.md` за шаблоном нижче. Перевірте що:

- Усі команди виконуються без помилок.
- Скрімшоти показують результати Trivy, Semgrep, Secret та SealedSecret.
- Описано, як вони інтегруються разом.

## Шаблон звіту

```markdown
# Лабораторна робота 09: Інтеграція security сканування та управління секретами

**Виконав:** ПІБ, група

## Хід виконання

### Рівень 1

1. Додав Trivy до GitHub Actions pipeline. Результати сканування показують:
   - (скрімшот GitHub Security tab)
   - Список виявлених уразливостей та їх severity.

2. Налаштував Kubernetes Secret:
   - Secret створений з комендою `kubectl apply -f src/k8s/secret.yaml`.
   - Deployment модифіковано для підключення Secret через environment variables.
   - (скрімшот `kubectl get secrets` та `kubectl exec ... env`)

### Рівень 2

3. Додав Semgrep SAST сканування до pipeline:
   - (скрімшот результатів Semgrep у GitHub)
   - Порівняння Trivy (SCA) та Semgrep (SAST).

4. Встановив та налаштував Sealed Secrets:
   - kubeseal встановлено.
   - SealedSecret YAML закодований та закомічений.
   - Secret автоматично розшифрований у кластері.
   - (скрімшот `kubectl get sealedsecrets`)

### Рівень 3

5. Налаштував RBAC:
   - ServiceAccount, Role, RoleBinding створені.
   - Pod запущений з правильними дозволами.
   - (скрімшот `kubectl exec ... kubectl get secrets`)

6. Налаштував NetworkPolicy:
   - NetworkPolicy застосована, обмежено трафік.
   - (скрімшот `kubectl get networkpolicies`)

## Висновки

Лабораторна робота продемонструвала важливість shift-left безпеки та управління секретами у Kubernetes. Trivy та Semgrep дозволяють виявляти вразливості на ранніх етапах. Sealed Secrets та RBAC забезпечують безпеку на runtime. Всі компоненти разом формують комплексну стратегію DevSecOps.

Ключові засвоєні навички:
- Інтеграція сканування образів та коду у CI pipeline.
- Управління секретами: базові Kubernetes Secrets та Sealed Secrets.
- RBAC для контролю доступу.
- NetworkPolicy для мережевої безпеки.
```

## Контрольні запитання

1. Що таке shift-left безпеки та які переваги вона надає для DevOps процесу?

2. Поясніть різницю між SAST, DAST та SCA. Який інструмент найкраще підходить для кожного типу аналізу?

3. Чому небезпечно зберігати Kubernetes Secrets за замовчуванням, і як Sealed Secrets вирішує цю проблему?

4. Як налаштувати Kubernetes Secret у Deployment так, щоб контейнер отримував значення як environment variables?

5. Поясніть архітектуру RBAC у Kubernetes: чим відрізняються Role, ClusterRole, RoleBinding та ClusterRoleBinding?

6. Для чого потрібна NetworkPolicy, і як вона обмежує трафік між podами?

7. Опишіть процес роботи Sealed Secrets: як розробник запечатує Secret, як він зберігається в Git, та як controller його розшифровує у кластері?
```

---