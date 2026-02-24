# 🎯 Лекція 5 Створення та оптимізація Docker образів

---

# 📝 Dockerfile: основи

Dockerfile — текстовий файл з інструкціями для збірки образу

**Ключові інструкції:**
- `FROM` — базовий образ
- `RUN` — виконання команд при збірці
- `COPY` / `ADD` — копіювання файлів
- `WORKDIR` — робоча директорія
- `ENV` — змінні середовища
- `EXPOSE` — документація портів
- `CMD` / `ENTRYPOINT` — команда запуску

---

# 📝 Приклад простого Dockerfile

```dockerfile
# Базовий образ
FROM node:18-alpine

# Робоча директорія
WORKDIR /app

# Копіювання залежностей
COPY package*.json ./
RUN npm ci --only=production

# Копіювання коду
COPY . .

# Порт
EXPOSE 3000

# Команда запуску
CMD ["node", "server.js"]
```

---

# ✨ Кращі практики Dockerfile

**1. Мінімізація шарів**
```dockerfile
# ❌ Погано
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

# ✅ Добре
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*
```

---

# ✨ Кращі практики Dockerfile

**2. Правильний порядок інструкцій**
```dockerfile
FROM python:3.11-slim

# Рідко змінювані залежності
RUN apt-get update && apt-get install -y gcc

WORKDIR /app

# Періодично змінювані залежності
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Часто змінюваний код
COPY . .

CMD ["python", "app.py"]
```

---

# ✨ Кращі практики Dockerfile

**3. Використання .dockerignore**
```
.git
.gitignore
node_modules
vendor
.vscode
.idea
*.md
tests
.env
.env.local
```

---

# ✨ Кращі практики Dockerfile

**4. Конкретні теги базових образів**
```dockerfile
# ❌ Погано: непередбачувана версія
FROM node:latest

# ✅ Добре: конкретна версія
FROM node:18.19.0-alpine3.19
```

---

# ✨ Кращі практики Dockerfile

**5. Непривілейований користувач**
```dockerfile
FROM node:18-alpine

# Створення користувача
RUN addgroup -g 1001 appgroup && \
    adduser -D -u 1001 -G appgroup appuser

WORKDIR /app
COPY --chown=appuser:appgroup . .

# Перемикання на користувача
USER appuser

CMD ["node", "server.js"]
```

---

# 🏗️ Багатоетапна збірка

Дозволяє використовувати кілька `FROM` в одному Dockerfile

**Переваги:**
- Значне зменшення розміру образу
- Відсутність інструментів збірки у production
- Покращена безпека
- Спрощений Dockerfile

---

# 🏗️ Приклад: Go застосунок

```dockerfile
# Етап 1: Збірка
FROM golang:1.21-alpine AS builder
WORKDIR /build
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o app .

# Етап 2: Production
FROM alpine:3.19
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /build/app .
USER nonroot
CMD ["./app"]
```

---

# 🏗️ Приклад: Node.js + TypeScript

```dockerfile
# Етап 1: Збірка
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Етап 2: Production залежності
FROM node:18-alpine AS dependencies
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Етап 3: Production образ
FROM node:18-alpine
WORKDIR /app
COPY --from=dependencies /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
USER node
CMD ["node", "dist/server.js"]
```

---

# 🎯 Іменовані етапи збірки

```dockerfile
# Development
FROM node:18-alpine AS development
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "run", "dev"]

# Production
FROM node:18-alpine AS production
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY --from=development /app/dist ./dist
CMD ["node", "dist/server.js"]
```

```bash
docker build --target development -t app:dev .
docker build --target production -t app:prod .
```

---

# 🐳 Docker Compose

Інструмент для визначення та запуску багатоконтейнерних застосунків

**Переваги:**
- Декларативна конфігурація в YAML
- Запуск всього стеку однією командою
- Автоматичне створення мереж та volumes
- Підтримка змінних середовища

---

# 📄 Структура docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_PASSWORD=secret
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

---

# 🎯 Повний приклад: Web застосунок

```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    depends_on:
      - frontend
      - api
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro

  frontend:
    build:
      context: ./frontend
      target: production
    environment:
      - REACT_APP_API_URL=http://api:3000

  api:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://postgres@db/myapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "--spider", "http://localhost:3000/health"]
      interval: 30s

  db:
    image: postgres:15-alpine
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready"]

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data

  worker:
    build: ./backend
    command: npm run worker
    depends_on:
      - db
      - redis

volumes:
  postgres-data:
  redis-data:
```

---

# 🔧 Основні команди Docker Compose

```bash
# Запуск у фоновому режимі
docker compose up -d

# Запуск з перебудовою
docker compose up -d --build

# Перегляд логів
docker compose logs -f

# Статус сервісів
docker compose ps

# Зупинка
docker compose stop

# Зупинка та видалення
docker compose down
```

---

# 🌍 Змінні середовища

**.env файл:**
```
POSTGRES_DB=myapp
POSTGRES_USER=admin
POSTGRES_PASSWORD=secret
JWT_SECRET=your-key
API_PORT=3000
```

**docker-compose.yml:**
```yaml
services:
  api:
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db
      - JWT_SECRET=${JWT_SECRET}
    ports:
      - "${API_PORT}:3000"
```

---

# 🎭 Profiles для різних середовищ

```yaml
services:
  api:
    build: ./api
    # Завжди запускається

  pgadmin:
    image: dpage/pgadmin4
    profiles:
      - debug
    # docker compose --profile debug up -d

  monitoring:
    image: prom/prometheus
    profiles:
      - monitoring
    # docker compose --profile monitoring up -d
```

---

# 📦 Оптимізація розміру образів

**1. Вибір базового образу**

| Образ | Розмір |
|-------|---------|
| `node:18` | ~900 MB |
| `node:18-slim` | ~200 MB |
| `node:18-alpine` | ~110 MB ✅ |

| Образ | Розмір |
|-------|---------|
| `python:3.11` | ~1 GB |
| `python:3.11-slim` | ~120 MB |
| `python:3.11-alpine` | ~50 MB ✅ |

---

# 📦 Оптимізація розміру образів

**2. Очищення кешів**
```dockerfile
# Debian/Ubuntu
RUN apt-get update && \
    apt-get install -y package && \
    rm -rf /var/lib/apt/lists/*

# Alpine
RUN apk add --no-cache package

# Python
RUN pip install --no-cache-dir -r requirements.txt

# Node.js
RUN npm ci --only=production && \
    npm cache clean --force
```

---

# 🔒 Distroless образи

Google Distroless — мінімальні образи без shell та package managers

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

**Переваги:** мінімальна attack surface, найменший розмір

---

# 🗄️ Реєстри контейнерів

**Docker Hub** 🐳
- Публічний реєстр
- Офіційні образи
- Автоматизована збірка

**Приватні реєстри:**
- Harbor
- GitLab Container Registry
- GitHub Container Registry (GHCR)
- Amazon ECR / Google GCR / Azure ACR

---

# 🗄️ Робота з Docker Hub

```bash
# Вхід
docker login

# Тегування
docker tag myapp:latest username/myapp:latest
docker tag myapp:latest username/myapp:1.0.0

# Публікація
docker push username/myapp:latest
docker push username/myapp:1.0.0

# Завантаження
docker pull username/myapp:latest
```

---

# 🏷️ Стратегії тегування

```bash
# Semantic versioning
docker tag app myregistry.com/app:1.2.3
docker tag app myregistry.com/app:1.2
docker tag app myregistry.com/app:1
docker tag app myregistry.com/app:latest

# Git commit SHA
docker tag app myregistry.com/app:${GITHUB_SHA}

# Branch name
docker tag app myregistry.com/app:main

# Environment
docker tag app myregistry.com/app:production
```

---

# 🤖 GitHub Container Registry

**.github/workflows/docker-publish.yml:**
```yaml
name: Docker Build and Push

on:
  push:
    tags: [ 'v*' ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Login to GHCR
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
```

---

# 🤖 GitHub Container Registry

```yaml
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:latest
            ghcr.io/${{ github.repository }}:${{ github.ref_name }}
```

---

# 📊 Checklist оптимізації образів

✅ Використовувати Alpine або slim базові образи
✅ Застосовувати багатоетапну збірку
✅ Мінімізувати кількість шарів
✅ Правильний порядок інструкцій для кешування
✅ Використовувати .dockerignore
✅ Очищати кеші package managers
✅ Створювати непривілейованого користувача
✅ Використовувати конкретні теги версій
✅ Налаштовувати health checks
✅ Обмежувати ресурси контейнерів

---

# 🎓 Підсумки: Лекція 4

**Ключові концепції:**
- Контейнеризація ефективніша за віртуалізацію
- Docker використовує клієнт-серверну архітектуру
- Образи складаються з незмінних шарів
- Контейнери — запущені екземпляри образів
- Томи забезпечують персистентність даних
- Мережі дозволяють комунікацію між контейнерами

---

# 🎓 Підсумки: Лекція 5

**Ключові концепції:**
- Dockerfile — інструкції для збірки образів
- Багатоетапна збірка зменшує розмір образів
- Docker Compose для багатоконтейнерних застосунків
- Оптимізація через вибір базових образів
- Реєстри для зберігання та розповсюдження образів
- Правильне тегування для версіонування

---

# 💡 Практичні рекомендації

**Для розробки:**
- Використовуйте Docker Compose для локального розгортання
- Налаштуйте volume mounting для hot reload
- Створюйте окремі development та production образи

**Для production:**
- Завжди використовуйте багатоетапну збірку
- Встановлюйте health checks
- Обмежуйте ресурси контейнерів
- Використовуйте конкретні версії образів
- Налаштуйте централізоване логування

---

# 📚 Корисні ресурси

**Документація:**
- https://docs.docker.com/
- https://docs.docker.com/compose/

**Кращі практики:**
- https://docs.docker.com/develop/dev-best-practices/
- https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

**Образи:**
- https://hub.docker.com/ (Docker Hub)
- https://github.com/GoogleContainerTools/distroless
