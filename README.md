# Проект

## Цель

Систематизировать и применить на практике знания полученные на курсе

## Тема

Тема: "_**Frontend-тестирование на основе веб-приложения Opencart и Backend-тестирование на основе API Reqres.in**_"

# Frontend-тестирование на основе веб-приложения Opencart

## Инструкции

### - Локальный запуск:
Запустить приложение OpenCart

- Необходим запуск с параметром --db_host localhost

- По-умолчанию установлен headless режим

Для отключения --headless false(False)

Браузеры:

--browser: chrome(ch), firefox(ff), edge(ed)

Кол-во параллельных потоков можно установить -n:

-n 2

### - Для запуска в Selenoid
Запустить приложение OpenCart

Запустить Selenoid

- Необходимо запускать с параметром --remote
- Необходимо запускать с параметром --db_host localhost

Браузеры:

--browser chrome(ch) --bw 128.0 (127.0), если не указываем, запуститься с последней версией

--browser firefox(ff) --bw 125.0 (124.0), если не указываем, запуститься с последней версией

--browser edge(ed) --bw 124.0

Кол-во параллельных потоков:
-n 2


### - Для запуска в контейнере Docker:

Запустить приложение OpenCart

Запустить Selenoid

```
docker build -t tests_opencart .

docker run -it --rm tests_opencart
```

Кол-во параллельных потоков:
-n 2

### - Для запуска через docker compose:

Запустить Selenoid

Запустить Selenoid UI

```
docker build -t opencart-tests-compose -f Dockerfile_for_compose .

$env:PHPADMIN_PORT=8888; $env:OPENCART_PORT=8085; $env:LOCAL_IP="192.168.100.9"; docker compose -f docker-compose.yml up

```

Кол-во параллельных потоков:

Передать переменную - $env:THREADS=4;  либо поменять в docker-compose.yml в environment

### - Для запуска в Jenkins:
Создать параметры:

OPENCART_HOST

BROWSER

BROWSER_VERSION

EXECUTOR_URL

THREADS - Number of parallel test threads

#### Pipeline job:
 - Используйте  Jenkinsfile

#### Freestyle job:

```
# Очистка предыдущих Allure-результатов
rm -rf allure-results

# Запуск инфраструктуры
PHPADMIN_PORT=8888 OPENCART_PORT=8085 LOCAL_IP=192.168.100.9 docker compose up -d mariadb opencart

until docker ps | grep mariadb; do sleep 3; done
until docker ps | grep opencart; do sleep 3; done

sleep 10

# Запуск тестов
docker build -t tests_opencart .
docker run --name testing \
  -e OPENCART_HOST="$OPENCART_HOST" \
  -e BROWSER="$BROWSER" \
  -e BROWSER_VERSION="$BROWSER_VERSION" \
  -e EXECUTOR_URL="$EXECUTOR_URL" \
  -e THREADS="$THREADS" \
  tests_opencart \
  --url "$OPENCART_HOST" --browser "$BROWSER" --bv "$BROWSER_VERSION" --executor "$EXECUTOR_URL" -n "$THREADS"
  
docker cp testing:/app/allure-results . 
docker rm testing

# Остановка контейнеров
docker compose down --remove-orphans --timeout 2
```