# EasyExamAI

**EasyExamAI** — мультиагентная система для подготовки к экзаменам.  
Система автоматически маршрутизирует запросы к специализированным агентам:

- **TestAgent** — генерирует тестовые вопросы по теме.  
- **TutorAgent** — объясняет концепции и темы.  
- **DocumentAgent** — обрабатывает и индексирует документы для последующего поиска и анализа.  

Система поддерживает:  
- Семантический поиск по загруженным документам.  
- Энд-ту-энд тестирование и оценки производительности.  
- Мониторинг через Prometheus и Grafana.  
- Docker-окружение для быстрого запуска и деплоя.

---

## Требования

- Docker & Docker Compose  
- Python 3.9+  
- Ollama (можно через Docker образ)

---

## Установка и запуск

1. Клонируем репозиторий:
```bash
git clone https://github.com/AnastasiaDMW/EasyExamAI.git
cd EasyExamAI
```
2. Сборка и запуск контейнеров:
```bash
docker-compose up --build
```
Сервисы запускаются в порядке:
1) "Ollama — сервер LLM"
2) "Indexer — загрузка документов в векторную базу"
3) "App — FastAPI приложение"
4) "Prometheus & Grafana — мониторинг"
3. Доступ
* API: http://localhost:8000
* Prometheus: http://localhost:9090
* Grafana: http://localhost:3000

Примеры использования

Отправка запроса на объяснение темы или на генерацию теста:
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Explain what neural networks are"}'
```
Загрузка документа для анализа и индексирования:
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@example.pdf"
```
Просмотр метрик:
```bash
curl -X GET "http://localhost:8000/metrics"
```
Запуск всех оценочных скриптов:
```bash
python -m run_evals
```
Запуск тестов через pytest (CI/CD):
```bash
pytest -v tests/test_eval_runner.py
```
Автор: <b>*AnastasiaDMW*</b>
