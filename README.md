# Test task for UCar<>TopDoer

## Table of contents

- [Dependencies](#Dependencies)
- [Create virtual environment and installing libraries](#Create-virtual-environment-and-installing-libraries)
- [Run service](#Run-service)
- [Examples with curl](#Examples-with-curl)

## Dependencies
[`uv`](https://github.com/astral-sh/uv)


## Create virtual environment and installing libraries

```bash
uv sync --no-dev
```


## Run service

```bash
uv run --no-dev fastapi run
```


## Try it out
Got to [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs) and make some requests using interactive openapi interface


## Examples with curl

### Create reviews

```bash
# Request
curl -X 'POST' \
  'http://127.0.0.1:8000/reviews' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Супер хороший отзыв"
}'

# Response
# {
#   "id": 1,
#   "text": "Супер хороший отзыв",
#   "sentiment": "positive",
#   "created_at": "2025-07-29T13:02:55.403798+00:00"
# }


# Request
curl -X 'POST' \
  'http://127.0.0.1:8000/reviews' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Самый плохой отзыв"
}'

# Response
# {
#   "id": 2,
#   "text": "Самый плохой отзыв",
#   "sentiment": "negative",
#   "created_at": "2025-07-29T13:05:42.986051+00:00"
# }


# Request
curl -X 'POST' \
  'http://127.0.0.1:8000/reviews' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Просто обычный отзыв"
}'

# Response
# {
#   "id": 3,
#   "text": "Просто обычный отзыв",
#   "sentiment": "neutral",
#   "created_at": "2025-07-29T13:06:47.779132+00:00"
# }
```


### Get created reviews

```bash
# Request
curl -X 'GET' \
  'http://127.0.0.1:8000/reviews' \
  -H 'accept: application/json'

# Response
# [
#   {
#     "id": 1,
#     "text": "Супер хороший отзыв",
#     "sentiment": "positive",
#     "created_at": "2025-07-29T13:02:55.403798+00:00"
#   },
#   {
#     "id": 2,
#     "text": "Самый плохой отзыв",
#     "sentiment": "negative",
#     "created_at": "2025-07-29T13:05:42.986051+00:00"
#   },
#   {
#     "id": 3,
#     "text": "Просто обычный отзыв",
#     "sentiment": "neutral",
#     "created_at": "2025-07-29T13:06:47.779132+00:00"
#   }
# ]


# Request
curl -X 'GET' \
  'http://127.0.0.1:8000/reviews?sentiment=positive' \
  -H 'accept: application/json'

# Response
# [
#   {
#     "id": 1,
#     "text": "Супер хороший отзыв",
#     "sentiment": "positive",
#     "created_at": "2025-07-29T13:02:55.403798+00:00"
#   }
# ]


# Request
curl -X 'GET' \
  'http://127.0.0.1:8000/reviews?sentiment=negative' \
  -H 'accept: application/json'

# Response
# [
#   {
#     "id": 2,
#     "text": "Самый плохой отзыв",
#     "sentiment": "negative",
#     "created_at": "2025-07-29T13:05:42.986051+00:00"
#   }
# ]


# Request
curl -X 'GET' \
  'http://127.0.0.1:8000/reviews?sentiment=neutral' \
  -H 'accept: application/json'

# Response
# [
#   {
#     "id": 3,
#     "text": "Просто обычный отзыв",
#     "sentiment": "neutral",
#     "created_at": "2025-07-29T13:06:47.779132+00:00"
#   }
# ]
```
