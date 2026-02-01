# Лекція 5. Створення та оптимізація Docker образів

## Вступ

Створення ефективних Docker образів є критично важливою навичкою для розробників та DevOps інженерів. Добре спроєктований образ має бути компактним, безпечним, швидко збиратися та легко підтримуватися. У цій лекції ми детально розглянемо Dockerfile та кращі практики написання, багатоетапну збірку для мінімізації розміру образів, Docker Compose для оркестрації багатоконтейнерних застосунків та стратегії роботи з реєстрами контейнерів.

## Dockerfile: кращі практики та багатоетапна збірка

### Основи Dockerfile

Dockerfile є текстовим файлом, що містить послідовність інструкцій для автоматизованої збірки Docker образу. Кожна інструкція створює новий шар у образі, тому ефективна організація Dockerfile безпосередньо впливає на розмір та продуктивність фінального образу.

Базова структура Dockerfile включає кілька ключових інструкцій. FROM визначає базовий образ, на якому будується ваш образ. RUN виконує команди під час збірки образу. COPY та ADD копіюють файли з хост-системи до образу. WORKDIR встановлює робочу директорію для наступних інструкцій. ENV визначає змінні середовища. EXPOSE документує порти, які використовує контейнер. CMD та ENTRYPOINT визначають команду, що виконується при запуску контейнера.

Приклад простого Dockerfile для Node.js застосунку:

```dockerfile
# Базовий образ
FROM node:18-alpine

# Встановлення робочої директорії
WORKDIR /app

# Копіювання файлів залежностей
COPY package*.json ./

# Встановлення залежностей
RUN npm ci --only=production

# Копіювання коду застосунку
COPY . .

# Відкриття порту
EXPOSE 3000

# Команда запуску
CMD ["node", "server.js"]
```

### Кращі практики написання Dockerfile

Мінімізація кількості шарів є важливою практикою. Кожна інструкція RUN, COPY та ADD створює новий шар. Об'єднання команд у одну інструкцію RUN зменшує кількість шарів та розмір образу.

Неефективний підхід з множинними шарами:

```dockerfile
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get clean
```

Ефективний підхід з мінімальною кількістю шарів:

```dockerfile
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

Порядок інструкцій критично важливий для ефективного кешування. Docker кешує шари та повторно використовує їх, якщо інструкції не змінилися. Розміщуйте інструкції, що рідко змінюються, на початку Dockerfile, а ті, що часто змінюються, ближче до кінця.

Оптимізований порядок інструкцій:

```dockerfile
FROM python:3.11-slim

# Системні залежності (змінюються рідко)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Залежності Python (змінюються періодично)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Код застосунку (змінюється часто)
COPY . .

CMD ["python", "app.py"]
```

Використання .dockerignore файлу запобігає копіюванню непотрібних файлів до образу, зменшуючи його розмір та час збірки.

Приклад .dockerignore:

```
# Version control
.git
.gitignore

# Dependencies
node_modules
vendor

# IDE
.vscode
.idea
*.swp

# Documentation
README.md
docs

# Tests
tests
*.test.js

# Environment files
.env
.env.local
```

Використання конкретних тегів базових образів замість latest забезпечує відтворюваність збірок. Тег latest може змінюватися з часом, що призводить до несподіваних проблем.

```dockerfile
# Погано: непередбачувана версія
FROM node:latest

# Добре: конкретна версія
FROM node:18.19.0-alpine3.19
```

Створення непривілейованого користувача підвищує безпеку контейнера. За замовчуванням процеси в контейнері виконуються від імені root, що створює ризики безпеки.

```dockerfile
FROM node:18-alpine

# Створення користувача та групи
RUN addgroup -g 1001 appgroup && \
    adduser -D -u 1001 -G appgroup appuser

WORKDIR /app

# Копіювання файлів як root
COPY package*.json ./
RUN npm ci --only=production

COPY --chown=appuser:appgroup . .

# Перемикання на непривілейованого користувача
USER appuser

CMD ["node", "server.js"]
```

### Багатоетапна збірка

Багатоетапна збірка (multi-stage builds) дозволяє використовувати кілька FROM інструкцій у одному Dockerfile. Кожна FROM інструкція починає новий етап збірки. Ви можете копіювати артефакти з одного етапу до іншого, залишаючи в фінальному образі тільки необхідне.

Основні переваги багатоетапної збірки включають значне зменшення розміру фінального образу, відсутність інструментів збірки у production образі, покращену безпеку через мінімальну attack surface та спрощення Dockerfile без необхідності зовнішніх build scripts.

Приклад багатоетапної збірки для Go застосунку:

```dockerfile
# Етап 1: Збірка
FROM golang:1.21-alpine AS builder

WORKDIR /build

# Копіювання модулів та завантаження залежностей
COPY go.mod go.sum ./
RUN go mod download

# Копіювання коду та збірка
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .

# Етап 2: Production образ
FROM alpine:3.19

# Встановлення CA сертифікатів для HTTPS
RUN apk --no-cache add ca-certificates

WORKDIR /root/

# Копіювання тільки скомпільованого бінарника
COPY --from=builder /build/app .

# Створення непривілейованого користувача
RUN addgroup -g 1001 appgroup && \
    adduser -D -u 1001 -G appgroup appuser && \
    chown -R appuser:appgroup /root

USER appuser

EXPOSE 8080

CMD ["./app"]
```

У цьому прикладі перший етап використовує повний golang образ для компіляції застосунку. Другий етап починається з мінімального alpine образу та копіює тільки скомпільований бінарник. Фінальний образ містить лише runtime залежності без Go компілятора та інструментів збірки.

Приклад багатоетапної збірки для Node.js застосунку з TypeScript:

```dockerfile
# Етап 1: Встановлення всіх залежностей та збірка
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Етап 2: Встановлення тільки production залежностей
FROM node:18-alpine AS dependencies

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

# Етап 3: Production образ
FROM node:18-alpine

ENV NODE_ENV=production

WORKDIR /app

# Копіювання production залежностей
COPY --from=dependencies /app/node_modules ./node_modules

# Копіювання зібраного коду
COPY --from=builder /app/dist ./dist
COPY package*.json ./

RUN addgroup -g 1001 appgroup && \
    adduser -D -u 1001 -G appgroup appuser && \
    chown -R appuser:appgroup /app

USER appuser

EXPOSE 3000

CMD ["node", "dist/server.js"]
```

Використання іменованих етапів покращує читабельність та дозволяє створювати різні варіанти образу з одного Dockerfile:

```dockerfile
# Development образ
FROM node:18-alpine AS development
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "run", "dev"]

# Test образ
FROM development AS test
RUN npm run test

# Production образ
FROM node:18-alpine AS production
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY --from=development /app/dist ./dist
USER node
CMD ["node", "dist/server.js"]
```

Тепер можна збирати різні образи для різних цілей:

```bash
# Development образ
docker build --target development -t app:dev .

# Test образ з запуском тестів
docker build --target test -t app:test .

# Production образ
docker build --target production -t app:prod .
```

### ARG та ENV інструкції

ARG та ENV інструкції дозволяють параметризувати Dockerfile. ARG використовується для передачі змінних під час збірки, тоді як ENV встановлює змінні середовища для контейнера під час виконання.

```dockerfile
# Build-time аргументи
ARG NODE_VERSION=18
ARG APP_ENV=production

FROM node:${NODE_VERSION}-alpine

# Runtime змінні середовища
ENV NODE_ENV=${APP_ENV} \
    PORT=3000

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE ${PORT}

CMD ["node", "server.js"]
```

Використання з build args:

```bash
# Збірка з конкретною версією Node.js
docker build --build-arg NODE_VERSION=20 -t app:latest .

# Збірка для різних середовищ
docker build --build-arg APP_ENV=development -t app:dev .
```

## Docker Compose для багатоконтейнерних застосунків

### Введення в Docker Compose

Docker Compose є інструментом для визначення та запуску багатоконтейнерних Docker застосунків. Ви використовуєте YAML файл для конфігурації сервісів вашого застосунку, а потім створюєте та запускаєте всі сервіси з єдиної конфігурації однією командою.

Основні переваги Docker Compose включають декларативну конфігурацію всього стеку застосунку, простоту запуску складних середовищ однією командою, автоматичне створення мереж та volumes та підтримку змінних середовища та параметризації.

### Структура docker-compose.yml

Базовий приклад docker-compose.yml файлу:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://db:5432/myapp
    depends_on:
      - db
    networks:
      - app-network

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - app-network

volumes:
  postgres-data:

networks:
  app-network:
    driver: bridge
```

### Детальний розгляд компонентів

Services визначає контейнери, які складають ваш застосунок. Кожний сервіс може мати власну збірку, образ, порти, змінні середовища та інші параметри.

```yaml
services:
  api:
    build:
      context: ./api
      dockerfile: Dockerfile
      args:
        - NODE_VERSION=18
    image: myapp/api:latest
    container_name: myapp-api
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      NODE_ENV: production
      DATABASE_URL: postgresql://postgres:5432/myapp
    env_file:
      - .env
    volumes:
      - ./api:/app
      - /app/node_modules
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

Volumes забезпечують постійне зберігання даних. Docker Compose автоматично створює іменовані volumes та керує їх життєвим циклом.

```yaml
volumes:
  postgres-data:
    driver: local
  redis-data:
    driver: local
  uploads:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /mnt/uploads
```

Networks визначають мережі для ізоляції та комунікації між сервісами.

```yaml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # Внутрішня мережа без доступу до зовнішнього світу
```

### Практичний приклад: Повний стек застосунку

Розглянемо комплексний приклад застосунку з frontend, backend, базою даних, кешем та reverse proxy:

```yaml
version: '3.8'

services:
  # Reverse proxy
  nginx:
    image: nginx:alpine
    container_name: nginx-proxy
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - frontend
      - api
    networks:
      - frontend
    restart: unless-stopped

  # Frontend React застосунок
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      target: production
    container_name: myapp-frontend
    environment:
      - REACT_APP_API_URL=http://api:3000
    networks:
      - frontend
    restart: unless-stopped

  # Backend API
  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: myapp-api
    environment:
      - NODE_ENV=production
      - PORT=3000
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/myapp
      - REDIS_URL=redis://redis:6379
      - JWT_SECRET=${JWT_SECRET}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - frontend
      - backend
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # PostgreSQL база даних
  postgres:
    image: postgres:15-alpine
    container_name: myapp-postgres
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./postgres/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    networks:
      - backend
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis кеш
  redis:
    image: redis:7-alpine
    container_name: myapp-redis
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    networks:
      - backend
    restart: unless-stopped

  # Worker для фонових завдань
  worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: myapp-worker
    command: npm run worker
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/myapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
    networks:
      - backend
    restart: unless-stopped

volumes:
  postgres-data:
  redis-data:

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
```

### Основні команди Docker Compose

```bash
# Запуск всіх сервісів у фоновому режимі
docker compose up -d

# Запуск з перебудовою образів
docker compose up -d --build

# Перегляд логів усіх сервісів
docker compose logs -f

# Перегляд логів конкретного сервісу
docker compose logs -f api

# Перегляд статусу сервісів
docker compose ps

# Зупинка всіх сервісів
docker compose stop

# Зупинка та видалення контейнерів
docker compose down

# Зупинка з видаленням volumes
docker compose down -v

# Виконання команди в сервісі
docker compose exec api npm run migrate

# Масштабування сервісу
docker compose up -d --scale worker=3
```

### Змінні середовища та .env файли

Docker Compose підтримує автоматичне завантаження змінних з .env файлу:

.env файл:

```
# Database
POSTGRES_DB=myapp
POSTGRES_USER=admin
POSTGRES_PASSWORD=secretpassword

# API
JWT_SECRET=your-secret-key
API_PORT=3000

# Redis
REDIS_PASSWORD=redis-secret
```

Використання в docker-compose.yml:

```yaml
services:
  api:
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
      - JWT_SECRET=${JWT_SECRET}
    ports:
      - "${API_PORT}:3000"

  postgres:
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
```

### Profiles для різних середовищ

Docker Compose підтримує profiles для вибіркового запуску сервісів:

```yaml
services:
  api:
    build: ./api
    # Завжди запускається

  postgres:
    image: postgres:15
    # Завжди запускається

  pgadmin:
    image: dpage/pgadmin4
    profiles:
      - debug
    # Запускається тільки з --profile debug

  monitoring:
    image: prom/prometheus
    profiles:
      - monitoring
    # Запускається тільки з --profile monitoring
```

Використання:

```bash
# Стандартний запуск без debug сервісів
docker compose up -d

# Запуск з debug інструментами
docker compose --profile debug up -d

# Запуск з моніторингом
docker compose --profile monitoring up -d

# Запуск з кількома profiles
docker compose --profile debug --profile monitoring up -d
```

## Оптимізація розміру образів

### Вибір базового образу

Вибір правильного базового образу критично впливає на розмір фінального образу. Alpine Linux образи є найкомпактнішими, slim варіанти надають баланс між розміром та функціональністю, а повні образи містять усі інструменти але займають більше місця.

Порівняння розмірів базових образів для Node.js:

```dockerfile
# node:18 - ~900 MB
FROM node:18

# node:18-slim - ~200 MB
FROM node:18-slim

# node:18-alpine - ~110 MB (рекомендовано для production)
FROM node:18-alpine
```

Для Python застосунків:

```dockerfile
# python:3.11 - ~1 GB
FROM python:3.11

# python:3.11-slim - ~120 MB
FROM python:3.11-slim

# python:3.11-alpine - ~50 MB
FROM python:3.11-alpine
```

### Distroless образи

Google Distroless образи містять тільки ваш застосунок та його runtime залежності, без package managers, shells чи будь-яких інших програм. Це мінімізує attack surface та розмір образу.

```dockerfile
# Збірка
FROM golang:1.21 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 go build -o app .

# Production з distroless
FROM gcr.io/distroless/static-debian11
COPY --from=builder /app/app /
USER nonroot:nonroot
CMD ["/app"]
```

### Очищення кешів та тимчасових файлів

Завжди видаляйте package manager кеші та тимчасові файли в тій самій RUN інструкції, де вони створюються:

```dockerfile
# Debian/Ubuntu
RUN apt-get update && \
    apt-get install -y package && \
    rm -rf /var/lib/apt/lists/*

# Alpine
RUN apk add --no-cache package

# Python pip
RUN pip install --no-cache-dir -r requirements.txt

# Node.js npm
RUN npm ci --only=production && \
    npm cache clean --force
```

### Використання .dockerignore

Ефективний .dockerignore файл значно зменшує контекст збірки:

```
# Git
.git
.gitignore
.gitattributes

# CI/CD
.github
.gitlab-ci.yml
Jenkinsfile

# Documentation
*.md
docs/
LICENSE

# Development
.vscode/
.idea/
*.swp
.DS_Store

# Dependencies
node_modules/
vendor/
__pycache__/
*.pyc

# Test files
test/
tests/
*.test.js
*.spec.js
coverage/

# Build artifacts
dist/
build/
target/

# Logs
*.log
logs/

# Environment
.env*
!.env.example

# Docker
Dockerfile*
docker-compose*
.dockerignore
```

## Реєстри контейнерів

### Docker Hub

Docker Hub є публічним реєстром Docker образів. Він підтримує автоматизовану збірку з GitHub та GitLab, приватні репозиторії та офіційні образи від виробників програмного забезпечення.

Робота з Docker Hub:

```bash
# Вхід до Docker Hub
docker login

# Тегування образу для push
docker tag myapp:latest username/myapp:latest
docker tag myapp:latest username/myapp:1.0.0

# Публікація образу
docker push username/myapp:latest
docker push username/myapp:1.0.0

# Завантаження образу
docker pull username/myapp:latest
```

### Приватні реєстри

Організації часто використовують приватні реєстри для зберігання власних образів. Популярні рішення включають Harbor, GitLab Container Registry, GitHub Container Registry, Amazon ECR, Google Container Registry та Azure Container Registry.

Приклад використання Harbor:

```bash
# Вхід до приватного реєстру
docker login harbor.company.com

# Тегування та публікація
docker tag myapp:latest harbor.company.com/project/myapp:latest
docker push harbor.company.com/project/myapp:latest
```

### GitHub Container Registry

GitHub Container Registry інтегрується з GitHub Actions для автоматизованої публікації:

```yaml
# .github/workflows/docker-publish.yml
name: Docker Build and Push

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v3

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

### Стратегії тегування

Ефективне тегування образів критично важливе для версіонування та відтворюваності:

```bash
# Semantic versioning
docker tag app:latest myregistry.com/app:1.2.3
docker tag app:latest myregistry.com/app:1.2
docker tag app:latest myregistry.com/app:1
docker tag app:latest myregistry.com/app:latest

# Git commit SHA
docker tag app:latest myregistry.com/app:${GITHUB_SHA}

# Branch name
docker tag app:latest myregistry.com/app:main
docker tag app:latest myregistry.com/app:develop

# Environment specific
docker tag app:latest myregistry.com/app:production
docker tag app:latest myregistry.com/app:staging
```

## Висновки

Створення оптимізованих Docker образів вимагає ретельного планування та дотримання кращих практик. Використання багатоетапної збірки, правильний вибір базових образів, ефективне кешування шарів та очищення непотрібних файлів дозволяють створювати компактні та безпечні образи.

Docker Compose спрощує управління багатоконтейнерними застосунками, забезпечуючи декларативний підхід до конфігурації та оркестрації сервісів. Розуміння роботи з реєстрами контейнерів та стратегій тегування є необхідним для ефективного управління життєвим циклом образів у production середовищах.

Ці навички формують фундамент для подальшого вивчення більш складних тем DevOps, включаючи оркестрацію з Kubernetes, безперервну інтеграцію та доставку.
