# 🚀 Развертывание дашборда на Render.com

## Шаг 1: Подготовка GitHub репозитория

### 1.1 Создай репозиторий на GitHub

```bash
# В папке dashboard
git init
git add .
git commit -m "Initial commit: Aidar Business Dashboard"
git branch -M main
git remote add origin https://github.com/ТВО_GITHUB/aidar-dashboard.git
git push -u origin main
```

### 1.2 Что должно быть в репозитории:

```
aidar-dashboard/
├── app.py
├── data_updater.py
├── requirements.txt
├── Procfile
├── render.yaml
├── .gitignore
├── README.md
└── DEPLOY.md
```

---

## Шаг 2: Развертывание на Render

### 2.1 Создай аккаунт на [render.com](https://render.com)

1. Перейди на https://render.com
2. Зарегистрируйся через GitHub (это проще)
3. Дай доступ к репозиториям

### 2.2 Создай Web Service

1. Нажми **"New +"** → **"Web Service"**
2. Выбери репозиторий **aidar-dashboard**
3. Заполни поля:

| Поле | Значение |
|------|----------|
| **Name** | aidar-dashboard |
| **Environment** | Python 3.11 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn --workers 1 --worker-class sync --bind 0.0.0.0:$PORT app:server` |
| **Plan** | Free |

4. Нажми **"Create Web Service"**

⏳ Развертывание займет 2-3 минуты. Когда статус **"Live"** — дашборд готов!

### 2.3 Твоя ссылка будет:

```
https://aidar-dashboard.onrender.com
```

---

## Шаг 3: Ежедневное обновление данных

### 3.1 Создай Cron Job на Render

1. В панели Render нажми **"New +"** → **"Cron Job"**
2. Заполни:

| Поле | Значение |
|------|----------|
| **Name** | aidar-data-updater |
| **Schedule** | `0 6 * * *` (каждый день в 06:00 UTC) |
| **Repository** | aidar-dashboard |
| **Branch** | main |
| **Command** | `python data_updater.py` |

3. Нажми **"Create Cron Job"**

### 3.2 Проверь что работает:

1. После создания cron job появится в списке
2. Нажми на него → вкладка **"Logs"**
3. Должны быть логи выполнения

---

## Шаг 4: Мониторинг

### 4.1 Логи приложения:

1. Открой Web Service
2. Вкладка **"Logs"**
3. Видишь все события

### 4.2 Логи обновления данных:

1. Открой Cron Job
2. Вкладка **"Logs"**
3. Видишь время выполнения и результат

---

## Шаг 5: Автообновления

Render автоматически переразвертывает приложение при каждом `git push`:

```bash
# После изменений в коде
git add .
git commit -m "Update dashboard styles"
git push origin main

# Render автоматически redeploy за 1-2 минуты
```

---

## 🎯 Чек-лист перед запуском

- [ ] Репозиторий на GitHub с правильной структурой
- [ ] Токены WB и МойСклад закачаны на сервер Render
- [ ] Web Service создан и статус **"Live"**
- [ ] Cron Job для ежедневного обновления создан
- [ ] Проверил что дашборд открывается по ссылке
- [ ] Логи cron job показывают успешное обновление

---

## 📝 Добавление токенов на Render

### Способ 1: Environment Variables (через UI)

1. Открой Web Service
2. **Settings** → **Environment**
3. Добавь:

```
WB_TOKEN=eyJhbGc...
MOYSKLAD_TOKEN=eyJhbGc...
```

4. Обнови `data_updater.py` чтобы использовал переменные окружения:

```python
import os

wb_token = os.getenv('WB_TOKEN')
moysklad_token = os.getenv('MOYSKLAD_TOKEN')
```

### Способ 2: Через GitHub Secrets (рекомендуется)

1. На GitHub → **Settings** → **Secrets and variables** → **Actions**
2. Добавь секреты: `WB_TOKEN`, `MOYSKLAD_TOKEN`
3. Обнови файл `.github/workflows/deploy.yml` (если используешь)

---

## 💰 Стоимость

**Render Free Plan:**
- ✅ Web Service: бесплатно (с ограничением спящего режима)
- ✅ Cron Jobs: бесплатно (макс 1 бесплатный)
- Если нужно 24/7 без спящего режима: $7/месяц

**Альтернативы:**
- **Railway.app** — $5 в месяц
- **Heroku** — $5-7 в месяц (но дешевле на Railway)
- **Vercel** — бесплатно но только для фронтенда

---

## 🆘 Решение проблем

### Дашборд показывает ошибку 502

1. Проверь логи: Web Service → **Logs**
2. Проверь что все зависимости в `requirements.txt`
3. Перезагрузи: **Redeploy**

### Cron Job не запускается

1. Проверь формат расписания (должен быть `0 6 * * *`)
2. Проверь логи: Cron Job → **Logs**
3. Убедись что `data_updater.py` работает локально

### Токены не работают

1. Проверь что токены в Environment Variables
2. Проверь что скрипт использует `os.getenv()`
3. Перезагрузи Web Service после добавления переменных

---

## 📞 Поддержка Render

- Документация: https://render.com/docs
- Статус сервиса: https://status.render.com
- Support: support@render.com

---

**Готово!** Теперь твой дашборд работает в облаке 24/7 🎉
