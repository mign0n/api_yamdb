# API YaMDb

[![CI](https://github.com/mign0n/api_yamdb/actions/workflows/python-app.yml/badge.svg?branch=master)](https://github.com/mign0n/api_yamdb/actions/workflows/python-app.yml)
[![CI](https://github.com/mign0n/api_yamdb/actions/workflows/python-app.yml/badge.svg?branch=develop)](https://github.com/mign0n/api_yamdb/actions/workflows/python-app.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://github.com/python/mypy)
[![isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

## Описание

Проект YaMDb собирает отзывы пользователей на различные произведения.

## Технологии

- Python v3.9
- Django v3.2
- Django Rest Framework v3.12

## Запуск проекта в dev-режиме

- Склонируйте репозиторий и перейдите в директорию проекта

```shell
git clone https://github.com/mign0n/api_yamdb.git && cd api_yamdb
```

- Установите виртуальное окружение, установите зависимости, выполните миграции
с помощью команды:

```shell
make install
```

- Запустите тесты:

```shell
make test
```

- Запустите сервер:

```shell
make run
```

- Перейдите по адресу `127.0.0.1:8000/api/v1/doc`. Эта страница содержит
интерактивную документацию по API.

## Примеры запросов

Для регистрации пользователя отправьте POST-запрос по адресу
`127.0.0.1:8000/api/v1/auth/signup/`:

```shell
curl --header "content-type:application/json" \
--data '{"username":"<ИМЯ-ПОЛЬЗОВАТЕЛЯ>","email":"<ВАШ-EMAIL>"}' \
--request POST http://127.0.0.1:8000/api/v1/auth/signup/
```

Примерный ответ:

```text
{"username":"<ИМЯ-ПОЛЬЗОВАТЕЛЯ>","email":"<ВАШ-EMAIL>"}
```

На адрес <ВАШ-EMAIL> придет письмо с кодом подтверждения <ВАШ-КОД>.
Чтобы получить токен отправьте POST-запрос по адресу
`127.0.0.1:8000/api/v1/auth/token/`:

```shell
curl --header "content-type:application/json" \
--data '{"username":"<ИМЯ-ПОЛЬЗОВАТЕЛЯ>","confirmation_code":"<ВАШ-КОД>"}' \
--request POST http://127.0.0.1:8000/api/v1/auth/token/
```

Примерный ответ:

```text
{"token":"<ВАШ-ТОКЕН-ДОСТУПА>"}
```

HTTP-запросы можно отправлять прямо со страницы документации
`127.0.0.1:8000/api/v1/doc/`.
 Для авторизации используйте полученный ранее токен.
