# Лабораторна робота 08 Налаштування моніторингу та централізованого журналювання

## Мета

Освоїти практики моніторингу та спостережуваності хмарних застосунків за допомогою Prometheus та Grafana, налаштувати сповіщення через Alertmanager та впровадити централізоване журналювання за допомогою Loki та Promtail.

## Завдання

### Рівень 1 (обов'язковий мінімум)

Оволодіння базовими навичками роботи з системою моніторингу на основі Prometheus та Grafana.
Необхідно виконати наступне:

- розгорнути стек Prometheus + Grafana через Docker Compose;
- розробити простий вебзастосунок (Python Flask або Node.js) з інструментуванням метрик (лічильник запитів, часу відповіді);
- налаштувати prometheus.yml для збирання метрик з вебзастосунку;
- отримати доступ до Grafana та переглядати метрики Prometheus через Web UI;
- написати простий PromQL запит та побудувати графік у Grafana.

### Рівень 2 (додаткова функціональність)

Розширення функціональності моніторингу за рахунок інтерактивних дашбордів та сповіщень.
Додатково до рівня 1:

- розробити кастомний Grafana dashboard для вебзастосунку з кількома панелями (запити за секунду, помилки, латентність);
- налаштувати Alertmanager для виявлення аномалій (наприклад, помилок більше ніж 10% за 5 хвилин);
- налаштувати оповіщення (через webhook або email) при спрацьовуванні алертів;
- продемонструвати спрацьовування алерту через симуляцію помилок.

### Рівень 3 (творче розширення)

Впровадження повного стека спостережуваності з централізованим журналюванням та метриками.
Додатково до рівня 2:

- розгорнути Loki та Promtail для централізованого журналювання;
- налаштувати Promtail для збирання журналів з контейнерів застосунку;
- інтегрувати Loki як datasource у Grafana та створити панелі для перегляду журналів;
- побудувати єдиний dashboard, що комбінує метрики, алерти та журнали для повної спостережуваності.

## Критерії оцінювання

### Середній рівень (оцінка "задовільно")

Студент виконав завдання рівня 1 в повному обсязі. Docker Compose стек розгорнувся успішно та містить Prometheus та Grafana. Простий вебзастосунок розроблено та інструментовано для збирання базових метрик. Prometheus конфігурація налаштована коректно, метрики регулярно збираються. Grafana UI доступна, можна переглядати дані Prometheus. PromQL запити написані та повертають коректні результати. Звіт містить скріншоти інтерфейсів та пояснення конфігурацій.

### Достатній рівень (оцінка "добре")

Студент виконав завдання рівня 2 в повному обсязі. Кастомний Grafana dashboard розроблено та містить кілька інформативних панелей для моніторингу вебзастосунку. Alertmanager налаштовано та інтегровано з Prometheus. Правила для алертів написані коректно та реагують на аномалії. Демонстрація спрацьовування алерту показує, що система спостережуваності функціонує. Звіт детальний, містить пояснення правил та снімки результатів спрацьовування алертів.

### Високий рівень (оцінка "відмінно")

Студент виконав завдання рівня 3 в повному обсязі. Повний стек спостережуваності розгорнувся успішно: Prometheus, Grafana, Alertmanager, Loki та Promtail. Журнали із контейнерів вебзастосунку успішно збираються та доступні у Grafana через Loki datasource. Інтегрований dashboard комбінує метрики, алерти та журнали для цілісного погляду на стан системи. Конфігурація розроблена з урахуванням best practices (організація конфігурацій, документування, правильна настройка PromQL). Звіт комплексний, містить архітектурні діаграми, аналіз трьох стовпів спостережуваності та висновки про практичну цінність інтегрованого моніторингу.

## Порядок оформлення та здачи лабораторної роботи

Виконання лабораторної роботи відбувається через GitHub Classroom з фінальним підтвердженням здачи в системі Moodle.

[**GitHub Classroom assignment лабораторної роботи**](https://classroom.github.com/a/EnZPkxr-)

Структура репозиторію повинна містити папку src/ з такими підпапками: app/ (вебзастосунок з інструментуванням метрик), monitoring/ (Docker Compose та конфігурації Prometheus, Grafana dashboards, Alertmanager), logging/ (конфігурації Loki та Promtail). Кореневий файл README.md повинен описувати архітектуру, інструкції запуску (docker-compose up), доступ до Grafana та інші компоненти. Папка screenshots/ повинна містити екранні знімки Grafana дашбордів, перегляду метрик, спрацьовування алертів та журналів. Конфігураційні файли повинні містити коментарі для пояснення кожного блоку.

Після завершення всіх завдань та оформлення звіту необхідно виконати фінальний коміт, який зафіксує остаточний стан вашої роботи. Після відправлення фінального коміту перейдіть до курсу на платформі Moodle та знайдіть завдання лабораторної роботи. Відкрайте завдання для здачи. У текстовому полі для відповіді напишіть слово **виконано**.

## Політика щодо дедлайнів

При порушенні встановленого терміну здачи лабораторної роботи максимальна можлива оцінка становить "добре", незалежно від якості виконаної роботи. Винятки можливі лише за поважних причин, підтверджених документально.

## Теоретичні відомості

### Три стовпи спостережуваності

Спостережуваність (observability) у контексті DevOps та виробництва складається з трьох ключових компонентів: метрики, журнали та трейси. Метрики — це числові вимірювання, які показують стан системи в конкретний момент часу (наприклад, кількість запитів за секунду, використання пам'яті або латентність запитів). Журнали — це текстові записи подій, які відбуваються в системі (помилки, попередження, інформаційні повідомлення), часто з часовими мітками та контекстом. Трейси — це детальні записи про виконання окремих операцій через різні компоненти системи, які показують шлях запиту через мікросервіси та взаємодію компонентів. Кожен компонент надає різні переваги: метрики дозволяють агрегувати дані та виявляти тренди, журнали надають деталі для відлагодження, трейси допомагають розуміти взаємозв'язки. Комбінація всіх трьох забезпечує комплексне розуміння здоров'я та поведінки системи.

### Prometheus: архітектура та концепції

Prometheus — це система моніторингу з відкритим кодом, спеціально розроблена для контейнеризованих та хмарних середовищ. На відміну від традиційних систем моніторингу (наприклад, Graphite), які використовують push модель (агент надсилає дані на сервер), Prometheus використовує pull модель (сервер Prometheus періодично запитує метрики у цільових послуг через HTTP). Це робить архітектуру простішою та надійнішою. Prometheus зберігає метрики у своїй часовій базі даних та надає мову запитів PromQL для аналізу даних. Основні компоненти Prometheus: Prometheus Server (основний сервіс), Exporter (додатки, які експортують метрики у форматі Prometheus), Alertmanager (керує сповіщеннями), та клієнтські бібліотеки (дозволяють застосункам експортувати свої метрики). Prometheus конфігурація визначає, які цілі (targets) моніторити, як часто запитувати метрики та які правила для алертів застосовувати.

### Типи метрик та PromQL

Prometheus підтримує чотири основні типи метрик: Counter (лічильник, тільки зростає, наприклад кількість запитів), Gauge (показник, може зростати та спадати, наприклад температура або обсяг пам'яті), Histogram (розподіл значень у бакетах, наприклад розподіл латентностей запитів) та Summary (подібно histogram, але з розрахунком квантилів). PromQL (Prometheus Query Language) — це мова для запитів до метрик. Простий запит може мати вигляд http_requests_total (отримати всі значення метрики), http_requests_total{job="myapp"} (фільтр за label'ом), rate(http_requests_total[5m]) (темп зростання за 5 хвилин). Складні запити можна будувати з використанням функцій, агрегацій та операцій.

### Grafana: візуалізація та дашборди

Grafana — це платформа для візуалізації та аналізу часових рядів з підтримкою множини джерел даних (datasources), включаючи Prometheus, Loki, Elasticsearch та інші. Основні поняття: datasource (конфігурація підключення до джерела даних), dashboard (сторінка з панелями моніторингу), panel (окремий елемент візуалізації, наприклад графік або таблиця), alert (правило для сповіщення про аномалії). Grafana дозволяє створювати складні дашборди з перекиданням змінних, повторенням панелей для різних користувачів та інших гібких конфігурацій. Дашборди можна експортувати як JSON для переиспользування та зберігання версійного контролю.

### Alertmanager та управління сповіщеннями

Alertmanager — це компонент Prometheus, який отримує алерти від Prometheus сервера та управляє їх маршрутизацією, дедублікацією та відправленням. Alertmanager конфігурація визначає групування алертів (наприклад, групувати все від одного сервісу), часи утримання перед відправленням (щоб уникнути шуму від тимчасових проблем), та способи доставки (email, Slack, webhook). При спрацьовуванні правила для алерту у Prometheus, система відправляє інформацію до Alertmanager, який приймає рішення про те, чи відправляти сповіщення (враховуючи існуючі активні алерти того ж типу). Це дозволяє уникнути навали сповіщень та зосередити увагу на істинних проблемах.

### Loki та централізоване журналювання

Loki — це система для централізованого збирання та аналізу журналів, розроблена компанією Grafana та оптимізована для використання в Kubernetes та контейнеризованих середовищах. На відміну від Elasticsearch (яка індексує весь вміст журналів), Loki індексує тільки labels (мітки, як у Prometheus), що робить систему більш ефективною за пам'яттю та дешевою в операції. Promtail — це агент для збирання журналів з різних джерел (файлів, системи логування контейнерів, systemd) та відправлення їх до Loki. Конфігурація Promtail дозволяє визначати джерела, парсинг журналів, додавання labels та фільтрування. LogQL — це мова запитів до Loki, подібна PromQL, яка дозволяє шукати та аналізувати журнали.

### SLI, SLO та спостережуваність у production

SLI (Service Level Indicator) — це конкретне вимірюване значення, яке вказує на якість сервісу (наприклад, відсоток успішних запитів або латентність p99). SLO (Service Level Objective) — це ціль для SLI, встановлена командою (наприклад, 99.9% доступність). Моніторинг та спостережуваність критичні для отримання SLI, а слідкування за SLO допомагає командам приймати рішення про розподіл ресурсів та пріоритизацію роботи. У production-середовищі спостережуваність дозволяє швидко виявляти причини порушення SLO та відповідати на них. Best practices включають визначення ключових метрик для вашого сервісу, встановлення реалістичних SLO на основі користувацького досвіду та регулярний перегляд та коригування на основі даних.

## Хід роботи

### Клонування репозиторію

Скопіюйте URL репозиторію з GitHub Classroom та клонуйте його:

```bash
git clone https://github.com/your-username/lab-08-monitoring.git
cd lab-08-monitoring
```

### Розгортання стеку Prometheus та Grafana

Створіть структуру папок:

```bash
mkdir -p src/{app,monitoring/{prometheus,alertmanager,grafana/dashboards},logging/{loki,promtail}}
```

Створіть src/monitoring/docker-compose.yml:

```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./alertmanager/alert-rules.yml:/etc/prometheus/alert-rules.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - monitoring

  alertmanager:
    image: prom/alertmanager:latest
    container_name: alertmanager
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager/alertmanager.yml:/etc/alertmanager/alertmanager.yml
    command:
      - '--config.file=/etc/alertmanager/alertmanager.yml'
    networks:
      - monitoring

volumes:
  prometheus_data:
  grafana_data:

networks:
  monitoring:
    driver: bridge
```

Запустіть стек:

```bash
cd src/monitoring
docker-compose up -d
```

Переконайтеся, що всі контейнери запущені:

```bash
docker-compose ps
```

### Розробка вебзастосунку з інструментуванням метрик

Створіть src/app/app.py з Flask та інструментуванням Prometheus:

```python
from flask import Flask
from prometheus_client import Counter, Histogram, generate_latest
import time

app = Flask(__name__)

# Визначення метрик
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

@app.route('/metrics')
def metrics():
    return generate_latest()

@app.route('/')
def hello():
    with request_duration.labels(method='GET', endpoint='/').time():
        time.sleep(0.1)
    request_count.labels(method='GET', endpoint='/', status=200).inc()
    return 'Hello, DevOps Lab 08!'

@app.route('/api/data')
def data():
    with request_duration.labels(method='GET', endpoint='/api/data').time():
        time.sleep(0.05)
    request_count.labels(method='GET', endpoint='/api/data', status=200).inc()
    return {'message': 'Data endpoint', 'status': 'ok'}

@app.route('/error')
def error_endpoint():
    request_count.labels(method='GET', endpoint='/error', status=500).inc()
    return {'error': 'Internal Server Error'}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

Створіть src/app/Dockerfile:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

Створіть src/app/requirements.txt:

```
Flask==2.3.0
prometheus_client==0.17.0
```

### Налаштування Prometheus для збирання метрик

Створіть src/monitoring/prometheus/prometheus.yml:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - localhost:9093

rule_files:
  - '/etc/prometheus/alert-rules.yml'

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'flask_app'
    static_configs:
      - targets: ['host.docker.internal:5000']
    metrics_path: '/metrics'
    scrape_interval: 5s
```

### Налаштування Alertmanager

Створіть src/monitoring/alertmanager/alert-rules.yml:

```yaml
groups:
  - name: app_rules
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: 'rate(http_requests_total{status=~"5.."}[5m]) > 0.05'
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }}"

      - alert: ServiceDown
        expr: 'up{job="flask_app"} == 0'
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.job }} is down"
```

Створіть src/monitoring/alertmanager/alertmanager.yml:

```yaml
global:
  resolve_timeout: 5m

route:
  receiver: 'default'
  group_by: ['alertname', 'cluster']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h

receivers:
  - name: 'default'
    webhook_configs:
      - url: 'http://localhost:5001/alert'
        send_resolved: true
```

### Запуск вебзастосунку

Запустіть вебзастосунок у Docker або локально:

```bash
cd src/app
pip install -r requirements.txt
python app.py
```

Перевірте метрики:

```bash
curl http://localhost:5000/metrics
```

### Налаштування Grafana та перегляд метрик

Відкрийте Grafana у браузері (http://localhost:3000) з логіном admin/admin.

Додайте Prometheus як datasource:
- Configuration → Data Sources → Add data source
- Виберіть Prometheus
- URL: http://prometheus:9090

Створіть простий dashboard:
- Create → Dashboard
- Add Panel
- Query: rate(http_requests_total[1m])
- Зберегти

### Розширення: Кастомний Grafana Dashboard (рівень 2)

Створіть src/monitoring/grafana/dashboards/app-dashboard.json:

```json
{
  "dashboard": {
    "title": "Flask Application Monitoring",
    "panels": [
      {
        "id": 1,
        "title": "Requests per second",
        "targets": [
          {
            "expr": "rate(http_requests_total[1m])"
          }
        ],
        "type": "graph"
      },
      {
        "id": 2,
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])"
          }
        ],
        "type": "stat"
      },
      {
        "id": 3,
        "title": "Request Duration (p99)",
        "targets": [
          {
            "expr": "histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))"
          }
        ],
        "type": "graph"
      }
    ]
  }
}
```

Завантажте dashboard у Grafana через Dashboard → Import.

### Розширення: Симуляція помилок та спрацьовування алертів

Створіть скрипт для генерування помилок src/app/load_test.sh:

```bash
#!/bin/bash

# Генеруйте запити з помилками
for i in {1..100}; do
  curl http://localhost:5000/error
  sleep 1
done
```

Запустіть скрипт:

```bash
chmod +x src/app/load_test.sh
./src/app/load_test.sh
```

Спостерігайте за алертами у Prometheus (http://localhost:9090/alerts) та Alertmanager (http://localhost:9093).

### Розширення: Loki та централізоване журналювання (рівень 3)

Оновіть src/monitoring/docker-compose.yml для додавання Loki та Promtail:

```yaml
  loki:
    image: grafana/loki:latest
    container_name: loki
    ports:
      - "3100:3100"
    volumes:
      - ./loki/loki-config.yml:/etc/loki/local-config.yml
      - loki_data:/loki
    command: -config.file=/etc/loki/local-config.yml
    networks:
      - monitoring

  promtail:
    image: grafana/promtail:latest
    container_name: promtail
    volumes:
      - /var/log:/var/log
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock
      - ./promtail/promtail-config.yml:/etc/promtail/config.yml
    command: -config.file=/etc/promtail/config.yml
    networks:
      - monitoring
```

Додайте volume:

```yaml
volumes:
  loki_data:
```

Створіть src/logging/loki/loki-config.yml:

```yaml
auth_enabled: false

ingester:
  chunk_idle_period: 3m
  max_chunk_age: 1h
  max_streams_limit_errors: false

limits_config:
  enforce_metric_name: false
  reject_old_samples: true
  reject_old_samples_max_age: 168h

schema_config:
  configs:
    - from: 2020-10-24
      store: boltdb-shipper
      object_store: filesystem
      schema:
        version: v11
        index:
          prefix: index_
          period: 24h

storage_config:
  boltdb_shipper:
    active_index_directory: /loki/boltdb-shipper-active
    cache_location: /loki/boltdb-shipper-cache

server:
  http_listen_port: 3100
```

Створіть src/logging/promtail/promtail-config.yml:

```yaml
clients:
  - url: http://loki:3100/loki/api/v1/push

positions:
  filename: /tmp/positions.yaml

scrape_configs:
  - job_name: docker
    docker: {}
    relabel_configs:
      - source_labels: ['__meta_docker_container_name']
        target_label: 'container'
      - source_labels: ['__meta_docker_container_log_stream']
        target_label: 'stream'
```

Додайте Loki як datasource у Grafana та створіть панель для перегляду журналів з LogQL запитом {container="flask_app"}.

### Оформлення звіту

Створіть детальний звіт у форматі Markdown, що містить опис всіх компонентів стека моніторингу, скріншоти дашбордів та алертів, результати тестування та аналіз трьох стовпів спостережуваності.

## Шаблон звіту

```markdown
# Лабораторна робота 08: Налаштування моніторингу та централізованого журналювання

**Виконав:** ПІБ, група

## Архітектура стека моніторингу

[Опис компонентів: Prometheus, Grafana, Alertmanager, Loki, Promtail ...]

## Рівень 1: Prometheus та Grafana

[Опис розгортання, конфігурацій, перегляду метрик ...]

**Скріншоти:**
- Prometheus targets та scrape результати
- Grafana dashboard з PromQL запитами

## Рівень 2: Alertmanager та дашборди

[Опис alert rules, дашборда, симуляції помилок ...]

**Скріншоти:**
- Grafana dashboard з панелями для запитів, помилок, латентності
- Активні алерти у Prometheus
- Сповіщення в Alertmanager

## Рівень 3: Loki та централізоване журналювання

[Опис Loki та Promtail, інтеграції з Grafana ...]

**Скріншоти:**
- Журнали у Grafana через Loki datasource
- Комбінований dashboard з метриками та журналами

## Аналіз та висновки

[Обговорення трьох стовпів спостережуваності, SLI/SLO, практичної цінності ...]
```

## Контрольні запитання

1. Поясніть три стовпи спостережуваності (метрики, журнали, трейси) та наведіть практичні приклади використання кожного у розробці та підтримці вебзастосунків.

2. Яка архітектурна різниця між pull-моделлю Prometheus та push-моделлю традиційних систем моніторингу? Які переваги має pull-модель?

3. Назвіть чотири типи метрик у Prometheus та наведіть приклад метрики кожного типу для вебзастосунку.

4. Як написати PromQL запит для отримання темпу зростання помилок за останні 5 хвилин? Як використовувати цей запит у Grafana dashboard?

5. Які основні функції Alertmanager та як вона запобігає навалі сповіщень при множинних активних алертах?

6. Яка різниця між Loki та Elasticsearch у контексті централізованого журналювання? Які переваги має Loki?

7. Як інтегрувати метрики Prometheus та журнали Loki в єдиному Grafana dashboard для повної спостережуваності системи?
