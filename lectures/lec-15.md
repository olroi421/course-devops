# Лекція 15 Автоматизація конфігурування серверів за допомогою Ansible

## 1. Проблема управління конфігурацією та місце Ansible

Уявімо типову ситуацію: команда розгорнула 50 серверів за допомогою Terraform. Сервери запущені, але вони містять лише базову операційну систему — порожні. Тепер на кожен із них потрібно встановити залежності, налаштувати сервіси, розмістити конфігураційні файли, створити системних користувачів, налаштувати правила брандмауера. Ручне виконання цих операцій на кожному сервері через SSH займе години, буде схильним до помилок і не залишить жодних слідів того, що саме і в якому порядку було зроблено.

Це класична задача управління конфігурацією (configuration management), і саме для її вирішення були розроблені такі інструменти, як Ansible, Chef, Puppet і SaltStack.

Ansible — це інструмент автоматизації з відкритим вихідним кодом, розроблений компанією Red Hat, який вирішує задачу управління конфігурацією через простий, зрозумілий синтаксис на основі YAML. На відміну від Chef чи Puppet, Ansible є агентнонезалежним: для його роботи не потрібно встановлювати жодне програмне забезпечення на керовані сервери — достатньо SSH-з'єднання та Python, який присутній у більшості сучасних Linux-систем за замовчуванням.

### Порівняння підходів Terraform і Ansible

Важливо розуміти, що Terraform та Ansible вирішують різні, але взаємодоповнюючі задачі. Ця відмінність часто описується як «провізіонування vs. управління конфігурацією».

```mermaid
graph LR
    subgraph "Terraform"
        T1[Провізіонування\nінфраструктури]
        T2[Створення VM, мереж,\nбаз даних, сховищ]
        T3[Декларативний підхід\nдо стану інфраструктури]
    end

    subgraph "Ansible"
        A1[Управління\nконфігурацією]
        A2[Встановлення ПЗ,\nналаштування сервісів]
        A3[Процедурний підхід\nдо виконання задач]
    end

    T2 --> |Сервери готові| A2
```

Типовий DevOps-конвеєр виглядає так: Terraform створює хмарну інфраструктуру (мережу, сервери, балансувальники навантаження), а Ansible конфігурує створені сервери (встановлює nginx, налаштовує systemd-сервіси, розгортає застосунки).


## 2. Архітектура Ansible

Ansible використовує просту архітектуру «керуючий вузол — керовані вузли» (control node — managed nodes):

```mermaid
graph TD
    subgraph "Control Node"
        Ansible[Ansible Engine]
        Inventory[Inventory\nфайли та плагіни]
        Playbooks[Playbooks\n.yml файли]
        Roles[Roles\nповторно використовувані компоненти]
        Vault[Ansible Vault\nшифрування секретів]
    end

    subgraph "Managed Nodes"
        Web1[Вебсервер 1\nUbuntu 22.04]
        Web2[Вебсервер 2\nUbuntu 22.04]
        DB1[БД-сервер\nRocky Linux 9]
        LB[Балансувальник\nDebian 12]
    end

    Ansible --> |SSH| Web1
    Ansible --> |SSH| Web2
    Ansible --> |SSH| DB1
    Ansible --> |SSH| LB
```

Керуючий вузол — це машина, на якій встановлено Ansible і з якої запускаються плейбуки. Це може бути локальна робоча машина розробника або окремий CI/CD-сервер.

Керовані вузли — це сервери, якими управляє Ansible. Вони можуть бути фізичними машинами, віртуальними машинами у хмарі або контейнерами. Єдина вимога — наявність Python і можливість підключитися через SSH.

Ansible виконує завдання, підключаючись до керованих вузлів через SSH, передаючи невеликі Python-скрипти (модулі), виконуючи їх і отримуючи результат. Усі тимчасові файли видаляються після завершення, залишаючи сервер у чистому стані.


## 3. Інвентар: опис керованої інфраструктури

Інвентар — це файл або набір файлів, у яких описано, якими хостами управляє Ansible і як їх згруповано. Інвентар може бути статичним (простий файл) або динамічним (скрипт або плагін, що запитує API хмарного провайдера в реальному часі).

### Статичний інвентар

Простий текстовий формат INI:

```ini
# inventory/hosts.ini

# Балансувальник навантаження
[loadbalancers]
lb01 ansible_host=10.0.1.10

# Вебсервери
[webservers]
web01 ansible_host=10.0.1.21
web02 ansible_host=10.0.1.22
web03 ansible_host=10.0.1.23

# Сервери баз даних
[databases]
db01 ansible_host=10.0.2.10 ansible_user=dbadmin
db02 ansible_host=10.0.2.11 ansible_user=dbadmin

# Мета-група, що об'єднує всі сервери застосунку
[application:children]
webservers
databases

# Змінні для групи webservers
[webservers:vars]
ansible_user=ubuntu
ansible_python_interpreter=/usr/bin/python3
http_port=80
```

Той самий інвентар у YAML-форматі (рекомендований для складних структур):

```yaml
# inventory/hosts.yml
all:
  children:
    loadbalancers:
      hosts:
        lb01:
          ansible_host: 10.0.1.10
    webservers:
      vars:
        ansible_user: ubuntu
        http_port: 80
      hosts:
        web01:
          ansible_host: 10.0.1.21
        web02:
          ansible_host: 10.0.1.22
        web03:
          ansible_host: 10.0.1.23
    databases:
      vars:
        ansible_user: dbadmin
      hosts:
        db01:
          ansible_host: 10.0.2.10
        db02:
          ansible_host: 10.0.2.11
    application:
      children:
        webservers:
        databases:
```

### Динамічний інвентар

У хмарних середовищах кількість серверів може динамічно змінюватися. Ansible підтримує плагіни динамічного інвентарю, що автоматично отримують список хостів із хмарних API:

```yaml
# inventory/aws_ec2.yml
plugin: amazon.aws.aws_ec2
regions:
  - eu-central-1
filters:
  tag:Environment: production
  instance-state-name: running
keyed_groups:
  - key: tags.Role
    prefix: role
  - key: placement.availability_zone
    prefix: az
hostnames:
  - private-ip-address
```

Цей файл динамічно генерує інвентар на основі тегів EC2-інстансів у хмарі AWS.


## 4. Модулі та ad-hoc команди

Перш ніж перейти до написання плейбуків, корисно розглянути основний будівельний блок Ansible — модуль. Модуль — це ідемпотентна одиниця виконання, що реалізує конкретну дію: встановлення пакету, копіювання файлу, управління сервісом тощо. Ansible поставляється з тисячами вбудованих модулів.

Ad-hoc команди дозволяють виконати один модуль без написання плейбука — зручно для швидких операцій або перевірки стану:

```bash
# Перевірка доступності всіх хостів
ansible all -i inventory/hosts.yml -m ping

# Запуск команди на всіх вебсерверах
ansible webservers -i inventory/hosts.yml -m command -a "uptime"

# Встановлення пакету (модуль apt)
ansible webservers -i inventory/hosts.yml -m apt \
  -a "name=nginx state=present" --become

# Перезапуск сервісу
ansible webservers -i inventory/hosts.yml -m service \
  -a "name=nginx state=restarted" --become

# Збір фактів про хости
ansible db01 -i inventory/hosts.yml -m setup
```

Прапорець `--become` активує підвищення привілеїв (аналог `sudo`) для команд, що вимагають прав адміністратора.


## 5. Плейбуки: основа автоматизації

Плейбук — це YAML-файл, що описує послідовність завдань для виконання на групах хостів. Плейбук складається з одного або кількох «plays», кожен із яких відповідає за конфігурацію певної групи хостів.

```yaml
# playbooks/configure-webserver.yml
- name: Конфігурація вебсерверів
  hosts: webservers
  become: true         # Виконувати від імені root
  gather_facts: true   # Зібрати інформацію про хости перед виконанням

  vars:
    app_user: webapp
    app_dir: /opt/webapp
    nginx_worker_processes: "{{ ansible_processor_vcpus }}"  # Факт хоста

  pre_tasks:
    - name: Оновлення кешу пакетів
      apt:
        update_cache: true
        cache_valid_time: 3600  # Не оновлювати, якщо кеш свіжіший за 1 годину

  tasks:
    - name: Встановлення необхідних пакетів
      apt:
        name:
          - nginx
          - python3
          - python3-pip
          - git
        state: present

    - name: Створення системного користувача для застосунку
      user:
        name: "{{ app_user }}"
        system: true
        shell: /bin/false
        home: "{{ app_dir }}"
        create_home: true

    - name: Копіювання конфігурації nginx
      template:
        src: templates/nginx.conf.j2  # Шаблон Jinja2
        dest: /etc/nginx/sites-available/webapp
        owner: root
        group: root
        mode: "0644"
      notify: Перезапустити nginx     # Викликати обробник при змінах

    - name: Увімкнення конфігурації сайту
      file:
        src: /etc/nginx/sites-available/webapp
        dest: /etc/nginx/sites-enabled/webapp
        state: link
      notify: Перезапустити nginx

    - name: Видалення стандартної конфігурації nginx
      file:
        path: /etc/nginx/sites-enabled/default
        state: absent
      notify: Перезапустити nginx

    - name: Переконатися, що nginx запущений і увімкнений при старті
      service:
        name: nginx
        state: started
        enabled: true

  handlers:
    - name: Перезапустити nginx
      service:
        name: nginx
        state: restarted
```

### Обробники (Handlers)

Обробники — особливий тип завдань, що виконуються лише один раз наприкінці play, якщо їх було «повідомлено» хоча б одним завданням за допомогою `notify`. Це елегантний механізм для перезапуску сервісів лише тоді, коли їх конфігурація дійсно змінилася.

Наприклад, якщо три завдання у плейбуку мають `notify: Перезапустити nginx`, сервіс буде перезапущений лише один раз наприкінці play, а не після кожного завдання.

### Шаблони Jinja2

Ansible використовує мову шаблонів Jinja2 для генерації конфігураційних файлів із змінними значеннями:

```nginx
# templates/nginx.conf.j2
worker_processes {{ nginx_worker_processes }};

events {
    worker_connections 1024;
}

http {
    upstream app_backend {
{% for host in groups['webservers'] %}
        server {{ hostvars[host]['ansible_host'] }}:8080;
{% endfor %}
    }

    server {
        listen 80;
        server_name {{ ansible_hostname }};

        location / {
            proxy_pass http://app_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Статика обслуговується напряму
        location /static/ {
            alias {{ app_dir }}/static/;
            expires 30d;
        }
    }
}
```


## 6. Змінні та пріоритетність

Ansible надає надзвичайно гнучкий механізм управління змінними. Змінні можна визначити у багатьох місцях, і Ansible дотримується чіткого порядку пріоритетності (від найнижчого до найвищого):

```mermaid
graph TB
    P1[1. Ролі: defaults/main.yml\nНайнижчий пріоритет]
    P2[2. Інвентар: групові змінні\ngroup_vars/]
    P3[3. Інвентар: хостові змінні\nhost_vars/]
    P4[4. Факти хоста\nansible_*]
    P5[5. Змінні play\nvars: у плейбуку]
    P6[6. Ролі: vars/main.yml]
    P7[7. Змінні завдання\nvars: у task]
    P8[8. Передані через командний рядок\n-e або --extra-vars\nНайвищий пріоритет]

    P1 --> P2 --> P3 --> P4 --> P5 --> P6 --> P7 --> P8
```

Рекомендована структура директорій для змінних:

```
inventory/
├── group_vars/
│   ├── all.yml          # Змінні для всіх хостів
│   ├── webservers.yml   # Змінні для групи webservers
│   └── databases.yml    # Змінні для групи databases
└── host_vars/
    ├── web01.yml        # Змінні для конкретного хоста
    └── db01.yml
```

Приклад `group_vars/webservers.yml`:

```yaml
# Налаштування nginx
nginx_worker_processes: auto
nginx_keepalive_timeout: 65
http_port: 80
https_port: 443

# Параметри застосунку
app_version: "{{ lookup('env', 'APP_VERSION') | default('latest') }}"
app_port: 8080
```


## 7. Ролі: організація коду Ansible

Ролі (roles) — це основний механізм організації та повторного використання коду Ansible. Роль інкапсулює завдання, обробники, змінні, шаблони та файли, необхідні для конфігурації певного компонента системи.

### Структура ролі

```
roles/
└── nginx/
    ├── defaults/
    │   └── main.yml     # Значення змінних за замовчуванням (мінімальний пріоритет)
    ├── vars/
    │   └── main.yml     # Незмінні змінні ролі (вищий пріоритет)
    ├── tasks/
    │   ├── main.yml     # Основний список завдань
    │   ├── install.yml  # Можна виділити підзавдання у окремі файли
    │   └── configure.yml
    ├── handlers/
    │   └── main.yml     # Обробники
    ├── templates/
    │   └── nginx.conf.j2  # Шаблони Jinja2
    ├── files/
    │   └── ssl/           # Статичні файли
    ├── meta/
    │   └── main.yml     # Метадані ролі, залежності
    └── README.md        # Документація ролі
```

Приклад ролі для встановлення nginx:

`roles/nginx/defaults/main.yml`:

```yaml
nginx_worker_processes: auto
nginx_worker_connections: 1024
nginx_keepalive_timeout: 65
nginx_server_name: "{{ inventory_hostname }}"
nginx_document_root: /var/www/html
nginx_enable_ssl: false
```

`roles/nginx/tasks/main.yml`:

```yaml
- name: Встановлення nginx
  include_tasks: install.yml

- name: Конфігурація nginx
  include_tasks: configure.yml
```

`roles/nginx/tasks/install.yml`:

```yaml
- name: Встановлення nginx
  apt:
    name: nginx
    state: present
    update_cache: true

- name: Запуск та увімкнення nginx
  service:
    name: nginx
    state: started
    enabled: true
```

`roles/nginx/tasks/configure.yml`:

```yaml
- name: Копіювання основної конфігурації nginx
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    validate: nginx -t -c %s
  notify: Перезавантажити nginx

- name: Перевірка коректності конфігурації
  command: nginx -t
  changed_when: false
```

`roles/nginx/handlers/main.yml`:

```yaml
- name: Перезавантажити nginx
  service:
    name: nginx
    state: reloaded

- name: Перезапустити nginx
  service:
    name: nginx
    state: restarted
```

### Виклик ролей у плейбуку

```yaml
# site.yml — головний плейбук
- name: Конфігурація балансувальників навантаження
  hosts: loadbalancers
  become: true
  roles:
    - role: nginx
      vars:
        nginx_worker_processes: 4

- name: Конфігурація вебсерверів
  hosts: webservers
  become: true
  roles:
    - common        # Базові налаштування для всіх серверів
    - nginx
    - role: app
      vars:
        app_version: "{{ lookup('env', 'DEPLOY_VERSION') }}"

- name: Конфігурація серверів баз даних
  hosts: databases
  become: true
  roles:
    - common
    - postgresql
```


## 8. Ідемпотентність та коли вона порушується

Ідемпотентність — одна з ключових властивостей, якої прагне Ansible: плейбук можна запустити будь-яку кількість разів, і результат завжди буде однаковим — система досягне описаного стану без непотрібних змін.

Більшість вбудованих модулів Ansible ідемпотентні за визначенням: модуль `apt` з `state: present` перевірить, чи встановлений пакет, і нічого не зробить, якщо він вже є. Модуль `file` перевірить, чи існує файл з потрібними атрибутами.

Однак при використанні модулів `command` та `shell` ідемпотентність не гарантується автоматично, оскільки Ansible не може передбачити ефект довільної команди:

```yaml
# Неідемпотентно — команда виконається при кожному запуску
- name: Ініціалізація бази даних
  command: /opt/app/scripts/init-db.sh

# Ідемпотентно — перевіряємо наявність маркерного файлу
- name: Ініціалізація бази даних
  command: /opt/app/scripts/init-db.sh
  args:
    creates: /opt/app/.db-initialized  # Пропустити, якщо файл існує

# Ідемпотентно через реєстрацію результату
- name: Перевірка ініціалізації бази даних
  stat:
    path: /opt/app/.db-initialized
  register: db_initialized

- name: Ініціалізація бази даних
  command: /opt/app/scripts/init-db.sh
  when: not db_initialized.stat.exists

- name: Позначити базу даних як ініціалізовану
  file:
    path: /opt/app/.db-initialized
    state: touch
  when: not db_initialized.stat.exists
```


## 9. Умови, цикли та реєстрація результатів

Ansible надає потужні механізми управління потоком виконання.

### Умови (when)

```yaml
- name: Встановлення пакетів для Debian/Ubuntu
  apt:
    name: "{{ item }}"
    state: present
  loop:
    - nginx
    - python3
    - git
  when: ansible_os_family == "Debian"

- name: Встановлення пакетів для RedHat/CentOS
  dnf:
    name: "{{ item }}"
    state: present
  loop:
    - nginx
    - python3
    - git
  when: ansible_os_family == "RedHat"

# Умови можна комбінувати
- name: Налаштування файлу конфігурації
  template:
    src: app.conf.j2
    dest: /etc/app/config.conf
  when:
    - ansible_distribution == "Ubuntu"
    - ansible_distribution_version is version('20.04', '>=')
    - app_config_enabled | bool
```

### Цикли (loop)

```yaml
# Простий цикл
- name: Створення системних користувачів
  user:
    name: "{{ item.name }}"
    uid: "{{ item.uid }}"
    groups: "{{ item.groups }}"
    shell: /bin/bash
  loop:
    - { name: deploy, uid: 1001, groups: "sudo,docker" }
    - { name: monitor, uid: 1002, groups: "adm" }
    - { name: backup, uid: 1003, groups: "" }

# Цикл по списку із змінної
- name: Розгортання конфігурацій сайтів
  template:
    src: "vhost.conf.j2"
    dest: "/etc/nginx/sites-available/{{ item.name }}.conf"
  loop: "{{ nginx_virtual_hosts }}"
  notify: Перезавантажити nginx
```

### Реєстрація результатів (register)

```yaml
- name: Перевірка статусу сервісу
  systemd:
    name: nginx
  register: nginx_status

- name: Виведення статусу
  debug:
    msg: "Nginx активний: {{ nginx_status.status.ActiveState == 'active' }}"

- name: Запуск nginx якщо не запущений
  service:
    name: nginx
    state: started
  when: nginx_status.status.ActiveState != "active"

# Реєстрація результату виконання команди
- name: Отримання поточної версії застосунку
  command: cat /opt/app/VERSION
  register: current_version
  ignore_errors: true
  changed_when: false  # Команда читання не змінює стан системи

- name: Розгортання нової версії
  # ... завдання розгортання
  when: >
    current_version.rc != 0 or
    current_version.stdout != desired_version
```


## 10. Ansible Vault: захист секретів

Playbooks часто містять чутливі дані: паролі, API-ключі, приватні сертифікати. Ansible Vault дозволяє шифрувати ці дані, зберігаючи їх безпосередньо у репозиторії у зашифрованому вигляді.

```bash
# Створення зашифрованого файлу
ansible-vault create group_vars/all/vault.yml

# Редагування зашифрованого файлу
ansible-vault edit group_vars/all/vault.yml

# Шифрування існуючого файлу
ansible-vault encrypt group_vars/all/secrets.yml

# Розшифрування (тільки для перегляду, не рекомендується зберігати розшифрованим)
ansible-vault decrypt group_vars/all/secrets.yml

# Перешифрування з новим паролем
ansible-vault rekey group_vars/all/vault.yml
```

Рекомендована практика: зберігати зашифровані змінні у файлі `vault.yml`, а у звичайних файлах змінних посилатися на них:

`group_vars/all/vault.yml` (зашифрований):

```yaml
vault_db_password: "super-secret-password"
vault_api_key: "sk-abc123xyz"
vault_ssl_private_key: |
  -----BEGIN RSA PRIVATE KEY-----
  ...
  -----END RSA PRIVATE KEY-----
```

`group_vars/all/vars.yml` (відкритий, у Git):

```yaml
# Посилання на зашифровані змінні — сам файл не містить секретів
db_password: "{{ vault_db_password }}"
api_key: "{{ vault_api_key }}"
ssl_private_key: "{{ vault_ssl_private_key }}"
```

Запуск плейбука з vault:

```bash
# Інтерактивне введення пароля
ansible-playbook site.yml --ask-vault-pass

# Зчитування пароля з файлу (для CI/CD)
ansible-playbook site.yml --vault-password-file ~/.vault_pass.txt

# Або через змінну оточення
export ANSIBLE_VAULT_PASSWORD_FILE=~/.vault_pass.txt
ansible-playbook site.yml
```


## 11. Структура повноцінного Ansible-проєкту

Повноцінний Ansible-проєкт для управління хмарною інфраструктурою матиме таку структуру:

```
ansible/
├── ansible.cfg              # Конфігурація Ansible
├── site.yml                 # Головний плейбук
├── inventory/
│   ├── production/
│   │   ├── hosts.yml        # Статичний інвентар
│   │   ├── aws_ec2.yml      # Динамічний інвентар (AWS)
│   │   ├── group_vars/
│   │   │   ├── all/
│   │   │   │   ├── vars.yml    # Спільні змінні
│   │   │   │   └── vault.yml   # Зашифровані секрети
│   │   │   ├── webservers.yml
│   │   │   └── databases.yml
│   │   └── host_vars/
│   │       └── db-primary.yml
│   └── staging/
│       └── ... (аналогічна структура)
├── roles/
│   ├── common/              # Базові налаштування для всіх серверів
│   ├── nginx/               # Вебсервер nginx
│   ├── postgresql/          # СУБД PostgreSQL
│   ├── app/                 # Застосунок
│   └── monitoring/          # Агенти моніторингу
└── playbooks/
    ├── deploy.yml           # Розгортання застосунку
    ├── upgrade.yml          # Оновлення ОС та пакетів
    └── maintenance.yml      # Обслуговування
```

Файл `ansible.cfg`:

```ini
[defaults]
inventory           = inventory/production
roles_path          = roles
host_key_checking   = False     # Вимкнути у тестових середовищах
retry_files_enabled = False
stdout_callback     = yaml      # Більш читабельний вивід

[privilege_escalation]
become      = True
become_method = sudo

[ssh_connection]
pipelining  = True              # Підвищує продуктивність
ssh_args    = -o ControlMaster=auto -o ControlPersist=30m  # Перевикористання з'єднань
```


## 12. Інтеграція Ansible із Terraform та CI/CD

Типовий сценарій: Terraform створює інфраструктуру і передає дані (IP-адреси, ідентифікатори) до Ansible для подальшого конфігурування.

```mermaid
sequenceDiagram
    participant TF as Terraform
    participant INV as Інвентар Ansible
    participant ANS as Ansible Playbook
    participant Srv as Сервери

    TF->>Srv: Створення EC2-інстансів
    TF->>INV: Збереження IP-адрес у outputs
    Note over INV: Динамічний інвентар\nзчитує теги з AWS
    ANS->>INV: Отримання списку хостів
    ANS->>Srv: SSH підключення
    ANS->>Srv: Встановлення ПЗ
    ANS->>Srv: Розгортання конфігурацій
    ANS->>Srv: Запуск сервісів
```

Приклад GitHub Actions workflow для спільного використання Terraform та Ansible:

```yaml
name: Deploy Infrastructure and Configure

on:
  push:
    branches: [main]

jobs:
  provision:
    name: Провізіонування інфраструктури
    runs-on: ubuntu-latest
    outputs:
      instance_ips: ${{ steps.tf-output.outputs.instance_ips }}

    steps:
      - uses: actions/checkout@v4

      - name: Terraform Apply
        working-directory: terraform/
        run: |
          terraform init
          terraform apply -auto-approve
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

      - name: Отримання виводів Terraform
        id: tf-output
        working-directory: terraform/
        run: |
          echo "instance_ips=$(terraform output -json instance_ips)" >> $GITHUB_OUTPUT

  configure:
    name: Конфігурація серверів
    runs-on: ubuntu-latest
    needs: provision

    steps:
      - uses: actions/checkout@v4

      - name: Встановлення Ansible
        run: pip install ansible boto3

      - name: Налаштування SSH-ключа
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa

      - name: Очікування готовності серверів
        run: sleep 60  # Дати час на ініціалізацію ОС

      - name: Запуск Ansible Playbook
        working-directory: ansible/
        run: |
          ansible-playbook site.yml \
            --vault-password-file <(echo "${{ secrets.VAULT_PASSWORD }}")
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```


## Висновки

Ansible суттєво спрощує управління конфігурацією серверів, пропонуючи баланс між простотою та потужністю. Ключові ідеї:

Агентнонезалежність означає відсутність необхідності встановлювати агенти на керовані сервери. Це суттєво спрощує інтеграцію у наявну інфраструктуру і знижує операційне навантаження.

Декларативний опис у YAML-форматі разом із принципом ідемпотентності дозволяє безпечно запускати плейбуки повторно — система завжди досягатиме описаного стану без непотрібних змін.

Ролі забезпечують перевикористання коду та чітке розділення відповідальності. Добре спроєктована роль може бути використана у десятках різних проєктів без модифікації.

Ansible Vault дозволяє безпечно зберігати секрети разом із конфігурацією у Git-репозиторії, не ризикуючи їх розкриттям.

Інтеграція Terraform + Ansible утворює повноцінний стек IaC: Terraform відповідає за провізіонування хмарної інфраструктури, Ansible — за конфігурацію розгорнутих систем.


## Питання для самоперевірки

1. У чому полягає відмінність між провізіонуванням інфраструктури (Terraform) та управлінням конфігурацією (Ansible)? Як ці інструменти доповнюють один одного?
2. Що таке агентнонезалежна архітектура Ansible? Які вимоги вона висуває до керованих вузлів?
3. Поясніть концепцію ідемпотентності в контексті Ansible. Чому вона важлива і коли може порушуватися?
4. Яка структура Ansible-ролі? Для чого призначений кожен каталог?
5. Поясніть різницю між `defaults/main.yml` та `vars/main.yml` у ролі з точки зору пріоритетності змінних.
6. Для чого використовуються обробники (handlers) і чим вони відрізняються від звичайних завдань?
7. Як Ansible Vault допомагає вирішити проблему зберігання секретів у Git-репозиторії?
