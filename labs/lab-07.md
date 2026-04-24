# Лабораторна робота 07 Створення хмарної інфраструктури за допомогою Terraform та Ansible

## Мета

Освоїти принципи інфраструктури як коду (IaC), навчитися керувати хмарною інфраструктурою за допомогою Terraform та виконувати автоматизовану конфігурацію серверів за допомогою Ansible на локальному симуляторі AWS.

## Завдання

### Рівень 1 (обов'язковий мінімум)

Оволодіння базовими навичками роботи з Terraform та локальним хмарним середовищем.
Необхідно виконати наступне:

- встановити Terraform та локальний хмарний симулятор LocalStack (через Docker Compose);
- написати базову Terraform конфігурацію (main.tf, variables.tf, outputs.tf) для створення ресурсу (S3 bucket або VPC з підмережею);
- виконати terraform init, terraform plan та terraform apply для розгортання інфраструктури;
- встановити Ansible та написати простий playbook для перевірки доступності хостів (ping);
- виконати Ansible playbook та продемонструвати успішне виконання.

### Рівень 2 (додаткова функціональність)

Розширення функціональності IaC за рахунок організації коду та автоматизації конфігурації.
Додатково до рівня 1:

- розбити Terraform конфігурацію на модуль (modules/webserver/) з параметризацією через variables;
- написати Ansible playbook для встановлення nginx та розгортання простого HTML-застосунку;
- використати кілька roles у playbook для розподілу завдань (config, deploy);
- здійснити успішний запуск вебзастосунку та перевірити доступність через curl.

### Рівень 3 (творче розширення)

Інтеграція Terraform та Ansible через динамічний inventory для повного автоматизованого розгортання.
Додатково до рівня 2:

- налаштувати Terraform для експорту інформації про створені інстанси (IP-адреси) через outputs;
- створити Python скрипт або JSON динамічний inventory, що генерує Ansible inventory на основі Terraform outputs;
- автоматизувати повний цикл: terraform apply → генерація inventory → ansible-playbook запуск;
- подати результат з екранними знімками та логами виконання.

## Критерії оцінювання

### Середній рівень (оцінка "задовільно")

Студент виконав завдання рівня 1 в повному обсязі. Базова Terraform конфігурація написана коректно, ініціалізація та застосування закінчилися успішно, відбулося створення принаймні одного облікового ресурсу. Ansible playbook виконувався без критичних помилок та продемонстрував базову функціональність (ping-тест). Репозиторій містить необхідні файли конфігурацій та скріншоти виконання команд. Звіт структурований та містить опис основних кроків.

### Достатній рівень (оцінка "добре")

Студент виконав завдання рівня 2 в повному обсязі. Terraform конфігурація розбита на модулі з коректною параметризацією, модуль успішно використовується в main.tf. Ansible playbook містить кілька roles для розподілу завдань та успішно розгортає вебзастосунок (nginx). Конфігурація протестована, вебзастосунок доступний та функціонує. Звіт містить детальні команди виконання та екранні знімки результатів. Демонструється розуміння концепцій Terraform state та ідемпотентності Ansible.

### Високий рівень (оцінка "відмінно")

Студент виконав завдання рівня 3 в повному обсязі. Реалізована повна інтеграція Terraform та Ansible через динамічний inventory. Terraform outputs коректно експортують інформацію про ресурси, скрипт або механізм динамічного inventory надійно генерує інвентар. Повний цикл розгортання автоматизований та виконується без ручного втручання. Конфігурація розроблена з урахуванням best practices (організація коду, використання змінних, документування). Звіт грунтовний, містить архітектурні діаграми, аналіз виконаної роботи та висновки щодо використання IaC у реальних проєктах.

## Порядок оформлення та здачі лабораторної роботи

Виконання лабораторної роботи відбувається через GitHub Classroom з фінальним підтвердженням здачі в системі Moodle.

[**GitHub Classroom assignment лабораторної роботи**](https://classroom.github.com/a/SVfQY1j7)

Структура репозиторію повинна містити папку src/ з двома підпапками: terraform/ та ansible/. У папці terraform/ розмістіть файли main.tf, variables.tf, outputs.tf та папку modules/ з модулями. У папці ansible/ розмістіть inventory.ini, playbook.yml та папку roles/ з необхідними rolями. Кореневий файл README.md повинен містити інструкції запуску (встановлення залежностей, docker-compose up для LocalStack, terraform init/plan/apply, ansible-playbook запуск). Папка screenshots/ повинна містити екранні знімки виконання всіх основних команд та результатів.

Після завершення всіх завдань та оформлення звіту необхідно виконати фінальний коміт, який зафіксує остаточний стан вашої роботи. Після відправлення фінального коміту перейдіть до курсу на платформі Moodle та знайдіть завдання лабораторної роботи. Відкрайте завдання для здачі. У текстовому полі для відповіді напишіть слово **виконано**.

## Політика щодо дедлайнів

При порушенні встановленого терміну здачи лабораторної роботи максимальна можлива оцінка становить "добре", незалежно від якості виконаної роботи. Винятки можливі лише за поважних причин, підтверджених документально.

## Теоретичні відомості

### Концепція інфраструктури як коду

Інфраструктура як код (Infrastructure as Code, IaC) — це практика управління та налаштування хмарної інфраструктури за допомогою декларативних або імперативних конфігураційних файлів замість ручного втручання. Декларативний підхід (як у Terraform) передбачає опис бажаного стану інфраструктури, а система сама визначає, які кроки необхідні для досягнення цього стану. Імперії́ativний підхід (як у більшості скриптів) описує послідовність команд для виконання. Переваги IaC включають відтворюваність (розгортання в різних середовищах стає однаковим), версіонування (можливість отримати історію змін інфраструктури через Git), масштабованість (легко дублювати конфігурації для кількох клієнтів) та надійність (уникнення помилок, які виникають при ручних діях).

### Архітектура та компоненти Terraform

Terraform — це інструмент IaC з відкритим вихідним кодом для керування ресурсами в різних хмарних провайдерах (AWS, Azure, Google Cloud та ін.). Архітектура Terraform складається з трьох основних компонентів: Terraform Core (головна частина, що інтерпретує конфігурації), Providers (модулі, які спілкуються з API хмарних сервісів) та State Backend (сховище стану інфраструктури). Workflow Terraform складається з чотирьох основних кроків: init (ініціалізація робочої директорії, завантаження потрібних провайдерів), plan (планування змін, показ того, що буде створено чи змінено), apply (застосування плану та створення ресурсів) та destroy (видалення ресурсів). Файл terraform.tfstate зберігає поточний стан інфраструктури, що дозволяє Terraform порівнювати бажаний та реальний стан.

### HCL синтаксис та основні блоки

HashiCorp Configuration Language (HCL) — це декларативна мова, розроблена для Terraform. Основні блоки в HCL: resource (визначення облікового ресурсу, наприклад resource "aws_s3_bucket" "my_bucket" { bucket = "my-bucket-name" }), variable (параметри конфігурацій для переиспользования та гнучкості), output (експорт значень, які можуть бути використані іншими системами або інструментами), data source (отримання інформації про існуючі ресурси) та module (переважне групування та переиспользования частин конфігурацій). Примітка: змінні оголошуються через variable, використовуються через var.name, outputs експортуються через output та доступні після apply через terraform output.

### LocalStack та локальне тестування

LocalStack — це проєкт з відкритим кодом, який симулює AWS сервіси локально за допомогою контейнерів Docker. Це дозволяє розробникам та DevOps-фахівцям тестувати Terraform конфігурації без витрат на реальну хмару та без ризику помилок на production. LocalStack підтримує більшість популярних AWS сервісів (S3, EC2, RDS, Lambda та ін.) та дозволяє налаштування Terraform провайдера для роботи з локальним API за допомогою змінної endpoint_override. Docker Compose дозволяє легко запустити LocalStack та інші сервіси в одній команді.

### Ansible: архітектура та управління конфігурацією

Ansible — це інструмент для управління конфігурацією та автоматизації завдань на множині серверів без необхідності встановлення агентів. Архітектура Ansible складається з control node (комп'ютер, з якого запускаються команди) та managed nodes (сервери, на яких виконуються завдання); спілкування відбувається через SSH. Основні концепції: inventory (файл або скрипт, що описує хости для управління), playbook (YAML файл з набором завдань для виконання), task (окремий модуль на виконання), role (організована структура задач, змінних та файлів для переиспользування). На відміну від Terraform (який керує інфраструктурою), Ansible керує конфігурацією та розгортанням застосунків на вже створену інфраструктуру.

### Ідемпотентність та best practices

Ідемпотентність — це властивість, коли повторне виконання однієї й тієї ж операції не змінює результат (операція безпечна для повторного запуску). Ansible модулі розроблені так, щоб бути ідемпотентними: якщо пакет вже встановлений, модуль apt не переустановлює його; якщо файл вже має правильні дозволи, модуль file не змінює їх. Це критично для надійної автоматизації. Best practices для IaC та Ansible включають: зберігання конфігурацій у системі контролю версій (Git), використання змінних замість жорсткого кодування значень, розділення конфігурацій для різних середовищ (dev, staging, prod), документування конфігурацій, регулярне тестування розгортання в тестових середовищах та моніторинг результатів.

## Хід роботи

### Клонування репозиторію

Скопіюйте URL репозиторію з GitHub Classroom та клонуйте його на локальну машину:

```bash
git clone https://github.com/your-username/lab-07-iac.git
cd lab-07-iac
```

### Встановлення Terraform та LocalStack

Встановіть Terraform, слідуючи офіційній документації (https://www.terraform.io/downloads). Для macOS через Homebrew:

```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

Для Linux:

```bash
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/
```

Переконайтеся, що Terraform встановлено:

```bash
terraform version
```

Встановіть Docker та Docker Compose (якщо не встановлені). Створіть файл docker-compose.yml для LocalStack:

```yaml
version: '3.8'
services:
  localstack:
    image: localstack/localstack:latest
    ports:
      - "4566:4566"
    environment:
      - SERVICES=s3,ec2,iam
      - DEBUG=1
      - DATA_DIR=/tmp/localstack/data
    volumes:
      - "${TMPDIR:-.}:/tmp/localstack"
      - "/var/run/docker.sock:/var/run/docker.sock"
```

Запустіть LocalStack:

```bash
docker-compose up -d
```

### Створення базової Terraform конфігурацією

У папці src/terraform/ створіть файл main.tf для визначення провайдера та ресурсів:

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  # Налаштування для LocalStack
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    s3  = "http://localhost:4566"
    ec2 = "http://localhost:4566"
  }
}

resource "aws_s3_bucket" "app_bucket" {
  bucket = var.bucket_name

  tags = {
    Name        = var.bucket_name
    Environment = var.environment
  }
}

resource "aws_s3_bucket_versioning" "app_bucket_versioning" {
  bucket = aws_s3_bucket.app_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}
```

Створіть файл variables.tf:

```hcl
variable "aws_region" {
  type        = string
  description = "AWS регіон для розгортання"
  default     = "us-east-1"
}

variable "bucket_name" {
  type        = string
  description = "Назва S3 bucket"
  default     = "my-app-bucket-dev"
}

variable "environment" {
  type        = string
  description = "Середовище розгортання"
  default     = "development"
}
```

Створіть файл outputs.tf:

```hcl
output "bucket_id" {
  value       = aws_s3_bucket.app_bucket.id
  description = "ID створеного S3 bucket"
}

output "bucket_arn" {
  value       = aws_s3_bucket.app_bucket.arn
  description = "ARN створеного S3 bucket"
}
```

### Ініціалізація та запуск Terraform

Інеціалізуйте Terraform робочу директорію (завантаження провайдерів):

```bash
cd src/terraform
terraform init
```

Перевірте план змін (без фактичного створення ресурсів):

```bash
terraform plan
```

Застосуйте конфігурацію для створення ресурсів:

```bash
terraform apply
```

Переконайтеся, що S3 bucket успішно створено. Переглядайте outputs:

```bash
terraform output
```

### Розширення Terraform конфігурацією з модулями (рівень 2)

Створіть директорію modules/webserver та файл modules/webserver/main.tf:

```hcl
resource "aws_instance" "webserver" {
  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Name = var.instance_name
  }
}

resource "aws_security_group" "webserver_sg" {
  name = "${var.instance_name}-sg"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

Створіть modules/webserver/variables.tf:

```hcl
variable "ami_id" {
  type        = string
  description = "AMI ID для EC2 інстансу"
}

variable "instance_type" {
  type        = string
  description = "Тип EC2 інстансу"
  default     = "t2.micro"
}

variable "instance_name" {
  type        = string
  description = "Назва EC2 інстансу"
}
```

Оновіть src/terraform/main.tf для використання модуля:

```hcl
module "webserver" {
  source = "./modules/webserver"

  ami_id         = "ami-12345678"
  instance_type  = "t2.micro"
  instance_name  = "my-webserver"
}
```

### Встановлення та налаштування Ansible

Встановіть Ansible:

```bash
pip install ansible
```

Створіть src/ansible/inventory.ini:

```ini
[webservers]
localhost ansible_connection=local

[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

Створіть базовий playbook src/ansible/playbook.yml:

```yaml
---
- name: Налаштування вебсервера
  hosts: webservers
  become: yes
  tasks:
    - name: Перевірка доступності хоста
      ping:

    - name: Оновлення пакетів
      apt:
        update_cache: yes
      when: ansible_os_family == "Debian"

    - name: Встановлення nginx
      package:
        name: nginx
        state: present

    - name: Запуск nginx
      service:
        name: nginx
        state: started
        enabled: yes
```

Запустіть playbook:

```bash
cd src/ansible
ansible-playbook -i inventory.ini playbook.yml
```

### Розширення Ansible з ролями (рівень 2)

Створіть структуру ролей:

```bash
mkdir -p roles/webserver/tasks
mkdir -p roles/nginx/tasks
mkdir -p roles/app/tasks
```

Створіть roles/nginx/tasks/main.yml:

```yaml
---
- name: Встановлення nginx
  package:
    name: nginx
    state: present

- name: Запуск nginx
  service:
    name: nginx
    state: started
    enabled: yes
```

Оновіть playbook.yml для використання ролей:

```yaml
---
- name: Розгортання вебзастосунку
  hosts: webservers
  become: yes
  roles:
    - nginx
    - app
```

Розгорніть просту HTML сторінку через roles/app/tasks/main.yml:

```yaml
---
- name: Створення директорії застосунку
  file:
    path: /var/www/html
    state: directory
    mode: '0755'

- name: Розгортання HTML застосунку
  copy:
    content: |
      <!DOCTYPE html>
      <html>
      <head><title>DevOps Lab 07</title></head>
      <body>
        <h1>Інфраструктура як код</h1>
        <p>Terraform + Ansible = Потужна автоматизація</p>
      </body>
      </html>
    dest: /var/www/html/index.html
    mode: '0644'
```

Запустіть оновлений playbook:

```bash
ansible-playbook -i inventory.ini playbook.yml
```

Перевірте результат:

```bash
curl http://localhost
```

### Динамічний inventory та повна інтеграція (рівень 3)

Створіть Python скрипт src/ansible/generate_inventory.py для генерації inventory з Terraform outputs:

```python
#!/usr/bin/env python3
import json
import subprocess
import sys

# Отримайте Terraform outputs у JSON форматі
result = subprocess.run(
    ["terraform", "output", "-json"],
    cwd="../terraform",
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print("Помилка отримання Terraform outputs", file=sys.stderr)
    sys.exit(1)

outputs = json.loads(result.stdout)

# Генеруйте Ansible inventory структуру
inventory = {
    "webservers": {
        "hosts": {},
    },
    "_meta": {
        "hostvars": {}
    }
}

# Припущення: у Terraform outputs є instance_ips або подібне
if "instance_ips" in outputs:
    for idx, ip in enumerate(outputs["instance_ips"]["value"]):
        hostname = f"webserver-{idx}"
        inventory["webservers"]["hosts"][hostname] = {
            "ansible_host": ip,
            "ansible_user": "ec2-user"
        }
        inventory["_meta"]["hostvars"][hostname] = {}

print(json.dumps(inventory, indent=2))
```

Зробіть скрипт виконуваним:

```bash
chmod +x src/ansible/generate_inventory.py
```

Запустіть Ansible playbook з динамічним inventory:

```bash
ansible-playbook -i generate_inventory.py playbook.yml
```

### Оформлення звіту

Створіть звіт у форматі Markdown, що містить описи всіх виконаних кроків, скріншоти команд та результатів, та аналіз роботи Terraform та Ansible. Помістіть звіт у файл REPORT.md у корені репозиторію.

## Шаблон звіту

```markdown
# Лабораторна робота 07: Створення хмарної інфраструктури за допомогою Terraform та Ansible

**Виконав:** ПІБ, група

## Хід виконання

### Завдання рівня 1

[Опис виконання завдання 1.1 ...]

**Скріншоти:**
- Результат terraform init
- Результат terraform plan
- Результат terraform apply

### Завдання рівня 2

[Опис виконання завдання 2.1 ...]
[Опис Ansible playbook виконання ...]

**Скріншоти:**
- Структура модулів
- Результат ansible-playbook
- Перевірка nginx на localhost

### Завдання рівня 3

[Опис динамічного inventory ...]
[Опис інтеграції ...]

**Скріншоти:**
- Вихід generate_inventory.py
- Остаточний результат

## Аналіз та висновки

[Обговорення переваг IaC, дизайну конфігурацій, складностей та рішень ...]

[Висновки щодо використання Terraform та Ansible у реальних проєктах DevOps ...]
```

## Контрольні запитання

1. Які основні переваги використання інфраструктури як коду (IaC) порівняно з ручним управлінням серверами?

2. Поясніть різницю між decelerative та imperative підходами до управління інфраструктурою та наведіть приклади інструментів для кожного.

3. Як Terraform керує станом інфраструктури? Чому файл terraform.tfstate є критичним для роботи Terraform?

4. Що таке Terraform модуль та як його використання сприяє переиспользуванню коду та організації конфігурацій?

5. Яка архітектурна різниця між Terraform (керування інфраструктурою) та Ansible (управління конфігурацією)?

6. Поясніть концепцію ідемпотентності та як вона реалізується в Ansible модулях.

7. Як можна інтегрувати Terraform та Ansible для повністю автоматизованого розгортання (infrastructure + configuration + application)?

---
