# Лабораторна робота 05 Створення CI конвеєра з автоматизованим тестуванням

## Мета

Навчитися створювати та налаштовувати конвеєри безперервної інтеграції на базі GitHub Actions. Опанувати автоматизацію процесів тестування, лінтингу та побудови Docker образів з інтеграцією в реєстр контейнерів.

## Завдання

### Рівень 1 (обов'язковий мінімум)

Створити базовий CI конвеєр, який автоматично перевіряє якість коду та запускає юніт-тести при кожному push.

Необхідно виконати наступне:

- Підготувати простий вебзастосунок на Node.js або Python з набором юніт-тестів.
- Налаштувати GitHub Actions workflow для запуску лінтера (eslint або flake8).
- Додати крок автоматичного запуску юніт-тестів.
- Переконатися, що конвеєр блокує merge при збоях тестів або лінтингу.

### Рівень 2 (додаткова функціональність)

Розширити конвеєр з можливістю побудови та завантаження Docker образу до GitHub Container Registry.

Додатково до рівня 1:

- Налаштувати секрет для автентифікації в GHCR (GitHub Container Registry).
- Додати крок build-and-push для Docker образу з автоматичним тегуванням.
- Налаштувати кешування залежностей для прискорення збірки.

### Рівень 3 (творче розширення)

Оптимізувати конвеєр із застосуванням паралелізації та безпеки.

Додатково до рівня 2:

- Запустити jobs для лінтингу та тестування паралельно.
- Інтегрувати сканування безпеки Docker образу за допомогою Trivy.
- Налаштувати умовний запуск build-and-push тільки при успішному проходженні всіх перевірок.

## Критерії оцінювання

### Середній рівень (оцінка "задовільно")

Студент створив базовий CI конвеєр на GitHub Actions, в якому налаштовані крок для лінтингу та крок для запуску тестів. Конвеєр запускається при push до репозиторію та правильно визначає помилки коду або невдалі тести. Разом з тим, студент недостатньо глибоко розуміє логіку роботи конвеєра, не налаштував кешування залежностей, і конвеєр потребує значного часу на виконання. Docker образ не збирається або побудова образу залишилася неосвоєною.

### Достатній рівень (оцінка "добре")

Студент успішно створив повнофункціональний CI конвеєр з лінтингом, тестуванням та побудовою Docker образу. Образ завантажується до GHCR з правильним тегуванням. Налаштовано кешування для прискорення збірки. Конвеєр коректно виконується при кожному push, але не налаштовані паралельні jobs або безпекові сканування. Студент добре розуміє логіку роботи конвеєра та елементи YAML-синтаксису.

### Високий рівень (оцінка "відмінно")

Студент розробив оптимізований CI конвеєр з максимальною функціональністю: паралельним виконанням jobs, скануванням безпеки образу за допомогою Trivy, ефективним кешуванням, та коректною обробкою помилок. Конвеєр швидко виконується, надійно блокує merge при виявленні проблем та демонструє глибоке розуміння принципів CI/CD. Звіт містить детальні скріншоти всіх крок та обґрунтовані пояснення обраних рішень.

## Порядок оформлення та здачі лабораторної роботи

Виконання лабораторної роботи відбувається через GitHub Classroom з фінальним підтвердженням здачі в системі Moodle.

[**GitHub Classroom assignment лабораторної роботи**](https://classroom.github.com/a/p8aj11TZ)

Репозиторій повинен містити наступну структуру:

```
lab-05-username/
├── src/
│   ├── app/
│   │   ├── app.js (або app.py)
│   │   ├── package.json (для Node.js)
│   │   └── index.html (опційно для фронтенду)
│   ├── tests/
│   │   └── app.test.js (або test_app.py)
│   ├── Dockerfile
│   └── .dockerignore
├── .github/
│   └── workflows/
│       └── ci.yml
├── .eslintrc.json (для Node.js) або setup.cfg (для Python)
├── README.md
└── screenshots/
    ├── ci-passed.png
    ├── docker-push.png
    └── trivy-scan.png (для рівня 3)
```

Основні файли звіту мають лежати у коренево репозиторію та папці `screenshots/`. Файл `README.md` повинен містити опис проєкту та інструкції для локального запуску. У папці `src/` розміщуються всі вихідні коди застосунку та конфігурацій.

Після завершення всіх завдань та оформлення звіту необхідно виконати фінальний коміт, який зафіксує остаточний стан вашої роботи:

```bash
git add .
git commit -m "lab-05: CI pipeline завершений"
git push
```

Після відправлення фінального коміту перейдіть до курсу на платформі Moodle та знайдіть завдання лабораторної роботи. Відкрийте завдання для здачі. У текстовому полі для відповіді напишіть слово **виконано**.

## Політика щодо дедлайнів

При порушенні встановленого терміну здачі лабораторної роботи максимальна можлива оцінка становить "добре", незалежно від якості виконаної роботи. Винятки можливі лише за поважних причин, підтверджених документально.

## Теоретичні відомості

### Принципи безперервної інтеграції

Безперервна інтеграція (Continuous Integration, CI) — це практика розробки, при якій членам команди необхідно інтегрувати свої зміни коду в єдиний репозиторій декілька разів на день. Кожна інтеграція автоматично перевіряється за допомогою виконання автоматичного набору тестів та статичного аналізу коду. Основні принципи CI полягають у наступному:

- **Fail Fast** — помилки мають бути виявлені якомога раніше в процесі розробки. Це дозволяє розробникам швидко реагувати на проблеми та вносити виправлення.
- **Ранній зворотний зв'язок** — розробник отримує миттєве повідомлення про результати запусків тестів та перевірок якості коду після push до репозиторію.
- **Автоматизація** — всі перевірки мають виконуватися автоматично без участі людини, що зменшує ймовірність людської помилки.
- **Стабільність репозиторію** — тільки код, який пройшов всі перевірки, має можливість бути об'єднаним у основну гілку.

Впровадження CI дозволяє командам швидше виявляти та виправляти баги, поліпшувати якість коду та скорочувати час доставки нових функцій у продакшн.

### Архітектура GitHub Actions

GitHub Actions — це вбудована система автоматизації GitHub для запуску конвеєрів. Основні компоненти архітектури:

- **Workflow** — це файл у форматі YAML, який визначає послідовність дій, що мають бути виконані. Workflow розташовується у папці `.github/workflows/`.
- **Тригери (Events)** — це подія, яка спускає запуск workflow. Найчастіше використовуються `push`, `pull_request` та `workflow_dispatch`.
- **Job** — це набір кроків, які виконуються на одному runner-і. Workflow може містити декілька jobs, які можуть виконуватися послідовно або паралельно.
- **Step** — це окремий крок у job, який може бути як shell-командою, так і публічною action.
- **Action** — це переналагоджена утиліта, яка виконує загальну задачу (наприклад, checkout коду, налаштування Node.js, або запуск тестів).
- **Runner** — це сервер, на якому виконуються jobs. GitHub надає безкоштовні Linux, Windows та macOS runners.

Мінімальна структура workflow-файлу:

```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run a one-line script
        run: echo Hello, world!
```

### Піраміда тестування та типи тестів у CI

Піраміда тестування описує розподіл різних типів тестів у проєкті. На найнижчому рівні розташовуються юніт-тести (найбільше за кількістю, найшвидші), на середньому — інтеграційні тести, а на верхівці — наскрізні функціональні тести (найменше, найповільніші).

Для CI конвеєру найбільш важливими є:

- **Юніт-тести** — перевіряють окремі функції або методи ізольовано від решти коду. В Node.js найпопулярніший фреймворк — Jest або Mocha. Для Python — pytest або unittest.
- **Лінтинг** — статичний аналіз коду, який виявляє стилістичні помилки та потенційні баги. Для JavaScript це eslint, для Python — flake8 або pylint.
- **Перевірка типів** — для мов зі слабою типізацією (JavaScript) використовуються TypeScript або Flow. Для Python — mypy.

### Кешування та артефакти в GitHub Actions

Кешування залежностей значно прискорює виконання конвеєра. GitHub Actions надає дію `actions/cache@v3` для зберігання та відновлення файлів між запусками:

```yaml
- name: Cache npm dependencies
  uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-npm-
```

Артефакти — це файли, які генеруються під час виконання job і можуть бути завантажені після завершення workflow. Це корисно для збереження логів, звітів про тестування або побудованих образів:

```yaml
- name: Upload test results
  uses: actions/upload-artifact@v3
  if: always()
  with:
    name: test-results
    path: coverage/
```

### Docker та GitHub Container Registry

Docker дозволяє упакувати застосунок разом з усіма залежностями у контейнер, який гарантує однакову поведінку на будь-якій системі. GitHub Container Registry (GHCR) — це вбудований реєстр образів GitHub, який дозволяє зберігати та розповсюджувати Docker образи.

Для push до GHCR у GitHub Actions використовується дія `docker/build-push-action@v4`:

```yaml
- name: Build and push Docker image
  uses: docker/build-push-action@v4
  with:
    context: .
    push: true
    tags: ghcr.io/${{ github.repository_owner }}/app:latest
    registry: ghcr.io
```

Секрет `GITHUB_TOKEN` автоматично доступний у GitHub Actions і дозволяє push до GHCR без додаткової конфігурації.

### Сканування безпеки образів з Trivy

Trivy — це потужний інструмент для сканування контейнерних образів на уразливості. Він перевіряє образ на наявність відомих CVE (Common Vulnerabilities and Exposures) та дає рекомендації щодо оновлення базових образів.

Інтеграція Trivy у GitHub Actions:

```yaml
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ghcr.io/${{ github.repository_owner }}/app:latest
    format: 'sarif'
    output: 'trivy-results.sarif'

- name: Upload Trivy results to GitHub Security tab
  uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: 'trivy-results.sarif'
```

## Хід роботи

### Клонування репозиторію

```bash
git clone git@github.com:organization/lab-05-username.git
cd lab-05-username
```

### Крок 1: Підготовка структури проєкту

Створіть необхідні директорії:

```bash
mkdir -p src/app src/tests .github/workflows screenshots
```

### Крок 2: Розробка вебзастосунку на Node.js

Створіть файл `src/app/package.json`:

```json
{
  "name": "lab-05-app",
  "version": "1.0.0",
  "description": "Simple web application for CI/CD lab",
  "main": "app.js",
  "scripts": {
    "start": "node app.js",
    "test": "jest --coverage",
    "lint": "eslint ."
  },
  "dependencies": {
    "express": "^4.18.2"
  },
  "devDependencies": {
    "eslint": "^8.40.0",
    "jest": "^29.5.0",
    "supertest": "^6.3.3"
  }
}
```

Створіть файл `src/app/app.js`:

```javascript
const express = require('express');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.json({ message: 'Welcome to Lab 05 CI/CD App' });
});

app.get('/api/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date() });
});

app.post('/api/add', (req, res) => {
  const { a, b } = req.body;
  if (typeof a !== 'number' || typeof b !== 'number') {
    return res.status(400).json({ error: 'Invalid input' });
  }
  res.json({ result: a + b });
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

module.exports = app;
```

Створіть файл `src/app/.eslintrc.json`:

```json
{
  "env": {
    "node": true,
    "es2021": true,
    "jest": true
  },
  "extends": "eslint:recommended",
  "parserOptions": {
    "ecmaVersion": "latest"
  },
  "rules": {
    "indent": ["error", 2],
    "linebreak-style": ["error", "unix"],
    "quotes": ["error", "single"],
    "semi": ["error", "always"],
    "no-unused-vars": ["error", { "argsIgnorePattern": "^_" }]
  }
}
```

### Крок 3: Створення юніт-тестів

Створіть файл `src/tests/app.test.js`:

```javascript
const request = require('supertest');
const app = require('../app/app');

describe('API Endpoints', () => {
  describe('GET /', () => {
    it('should return welcome message', async () => {
      const response = await request(app)
        .get('/')
        .expect('Content-Type', /json/)
        .expect(200);

      expect(response.body).toHaveProperty('message');
      expect(response.body.message).toBe('Welcome to Lab 05 CI/CD App');
    });
  });

  describe('GET /api/health', () => {
    it('should return health status', async () => {
      const response = await request(app)
        .get('/api/health')
        .expect(200);

      expect(response.body).toHaveProperty('status');
      expect(response.body.status).toBe('healthy');
    });
  });

  describe('POST /api/add', () => {
    it('should add two numbers correctly', async () => {
      const response = await request(app)
        .post('/api/add')
        .send({ a: 5, b: 3 })
        .expect(200);

      expect(response.body).toHaveProperty('result');
      expect(response.body.result).toBe(8);
    });

    it('should return error for invalid input', async () => {
      const response = await request(app)
        .post('/api/add')
        .send({ a: 'five', b: 3 })
        .expect(400);

      expect(response.body).toHaveProperty('error');
    });
  });
});
```

### Крок 4: Створення Dockerfile

Створіть файл `src/Dockerfile`:

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY app/package*.json ./

RUN npm ci --only=production

COPY app/ .

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/api/health', (r) => {if (r.statusCode !== 200) throw new Error(r.statusCode)})"

CMD ["node", "app.js"]
```

Створіть файл `src/.dockerignore`:

```
node_modules
npm-debug.log
.git
.gitignore
README.md
tests
```

### Крок 5: Налаштування GitHub Actions CI workflow

Створіть файл `.github/workflows/ci.yml`:

```yaml
name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  lint:
    name: Linting
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: 'src/app/package-lock.json'

      - name: Install dependencies
        run: cd src/app && npm ci

      - name: Run ESLint
        run: cd src/app && npm run lint

  test:
    name: Unit Tests
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: 'src/app/package-lock.json'

      - name: Install dependencies
        run: cd src/app && npm ci

      - name: Run tests
        run: cd src/app && npm test

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./src/app/coverage/lcov.info
          flags: unittests
          name: codecov-umbrella

  build-and-push:
    name: Build and Push Docker Image
    needs: [ lint, test ]
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=sha,prefix={{branch}}-

      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: ./src
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

Для рівня 3 додайте сканування Trivy до workflow. Розширте файл `.github/workflows/ci.yml` додавши наступний job після `build-and-push`:

```yaml
  security-scan:
    name: Security Scan with Trivy
    needs: build-and-push
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write
    steps:
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:main
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

### Крок 6: Налаштування локального тестування

Встановіть залежності локально:

```bash
cd src/app
npm install
npm run lint
npm test
```

Побудуйте Docker образ локально:

```bash
cd src
docker build -t lab-05-app:latest .
docker run -p 3000:3000 lab-05-app:latest
```

Перевірте здоров'я контейнера:

```bash
curl http://localhost:3000/api/health
```

### Крок 7: Оформлення звіту

Скопіюйте скріншоти успішного виконання CI конвеєра до папки `screenshots/`:

- `ci-passed.png` — скріншот успішного запуску всіх jobs у GitHub Actions.
- `docker-push.png` — скріншот push до GHCR в консолі або GitHub Actions.
- `trivy-scan.png` — скріншот результатів сканування Trivy (для рівня 3).

Створіть або оновіть файл `README.md` з описом проєкту та інструкціями:

```markdown
# Lab 05: CI Pipeline

## Опис

Простий вебзастосунок Node.js з автоматичним тестуванням та CI/CD pipeline.

## Локальний запуск

npm install
npm test
npm start

## Docker

docker build -t lab-05-app .
docker run -p 3000:3000 lab-05-app
```

Виконайте фінальний коміт:

```bash
git add .
git commit -m "lab-05: CI pipeline з лінтингом, тестами та Docker"
git push
```

## Шаблон звіту

```markdown
# Лабораторна робота 05: Створення CI конвеєра

**Виконав:** ПІБ, група

## Хід виконання

### Рівень 1: Базовий CI pipeline

1. Підготував вебзастосунок на Node.js з юніт-тестами.
2. Налаштував GitHub Actions workflow з jobs для лінтингу (eslint) та тестування (jest).
3. Конвеєр успішно блокує merge при помилках коду.

[Скріншот: ci-passed.png]

### Рівень 2: Docker образ та GHCR

1. Додав Dockerfile для упакування застосунку.
2. Налаштував build-and-push job з автоматичним тегуванням та кешуванням.
3. Образ успішно завантажується до ghcr.io.

[Скріншот: docker-push.png]

### Рівень 3: Паралелізація та безпека

1. Налаштував паралельне виконання lint та test jobs.
2. Додав Trivy для сканування образу на уразливості.
3. Результати сканування завантажуються до Security tab GitHub.

[Скріштот: trivy-scan.png]

## Висновки

У цій лабораторній роботі я створив повнофункціональний CI конвеєр, який автоматично перевіряє якість коду, запускає тести та збирає Docker образи. Розумію важливість ранньої автоматизації для виявлення проблем та забезпечення стабільності проєкту.
```

## Контрольні запитання

1. Поясніть принцип "fail fast" у контексті CI та його значення для командної розробки.
2. Яка різниця між GitHub Actions job та step, та як вони пов'язані?
3. Як налаштувати кешування залежностей у GitHub Actions та чому це важливо для швидкості конвеєра?
4. Опишіть процес push Docker образу до GHCR та які переваги надає GitHub Container Registry.
5. Що таке artifact у GitHub Actions і як його використовувати для збереження результатів тестування?
6. Поясніть, як встановити умови для виконання job (наприклад, залежність від іншого job) за допомогою `needs`.
7. Яку роль відіграє Trivy при сканюванні Docker образів та які типи уразливостей він виявляє?

---
