# ⚡ Быстрый старт деплоя на облако

## 3 шага до живого дашборда

### 1️⃣ Создай репозиторий на GitHub

```bash
# Если ещё нет git
cd /root/frost-ai/users/583297536/dashboard
git init

# Добавь файлы
git add .
git commit -m "Initial: Aidar Dashboard"

# Создай репозиторий на https://github.com/new
# Назови: aidar-dashboard

# Загрузи на GitHub
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/aidar-dashboard.git
git push -u origin main
```

---

### 2️⃣ Развернись на Render за 5 минут

1. Перейди: https://render.com
2. Нажми **"New Web Service"**
3. Выбери свой репозиторий `aidar-dashboard`
4. Заполни:
   - **Name:** `aidar-dashboard`
   - **Build:** `pip install -r requirements.txt`
   - **Start:** `gunicorn --workers 1 --worker-class sync --bind 0.0.0.0:$PORT app:server`
5. Нажми **"Create"**

⏳ Ждёшь 2 минуты... **Готово!** 🎉

Твой дашборд откроется по ссылке вроде:
```
https://aidar-dashboard.onrender.com
```

---

### 3️⃣ Настрой ежедневное обновление (опционально)

1. На Render: **"New Cron Job"**
2. **Schedule:** `0 6 * * *`
3. **Command:** `python data_updater.py`

Готово! Каждый день в 06:00 UTC данные обновляются автоматически.

---

## ✨ Что у тебя теперь есть

✅ Красивый дашборд с 4 вкладками  
✅ Живой в интернете 24/7  
✅ Автообновление данных каждый день  
✅ Бесплатно (план Free)  

---

## 📊 Что внутри дашборда

| Вкладка | Что видно |
|---------|-----------|
| 📈 WB Финансы | Выручка, маржа, топ товары, графики |
| 📦 Остатки | Распределение по 5 складам МойСклад |
| 💼 Оптовая | Целевая модель, прайс, бюджет май |
| 📊 Аналитика | Тренды, прогноз, ключевые метрики |

---

## 🔗 Полная инструкция

Если нужны подробности → читай `DEPLOY.md`

---

**Вопросы? Пиши в Telegram: @darik_ke**
