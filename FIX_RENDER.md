# 🔧 Исправление ошибки на Render

## Проблема
```
ModuleNotFoundError: No module named 'pkg_resources'
ERROR: Failed to build wheel for 'pandas'
```

## Решение

### Вариант 1: Пересоздай Web Service на Render (рекомендуется)

1. На Render удали старый Web Service:
   - Открой Web Service
   - **Settings** → **Delete Service**
   - Подтверди

2. Создай новый Web Service:
   - **New Web Service**
   - Выбери `aidar-dashboard` репозиторий
   - **Build Command:** 
     ```
     pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
     ```
   - **Start Command:**
     ```
     gunicorn --workers 1 --worker-class sync --bind 0.0.0.0:$PORT app:server
     ```
   - **Create**

⏳ Жди 5-10 минут → должно работать!

---

### Вариант 2: Обнови код в GitHub (если изменил локально)

1. Скачай обновленный ZIP (я пересоздал)
2. Распакуй и замени файлы
3. В терминале:
   ```bash
   git add .
   git commit -m "Fix Render build: add setuptools and wheel"
   git push origin main
   ```
4. Render автоматически переразвернёт за 3-5 минут

---

### Вариант 3: Быстрый фикс в render.yaml

Если Render уже создан и не переразворачивается:

1. Обнови `render.yaml` в GitHub:
   ```yaml
   buildCommand: |
     pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
   ```

2. Push на GitHub

3. На Render нажми **"Redeploy"** (правый верхний угол)

---

## ✅ Как проверить что работает

После развертывания:
1. Открой URL дашборда: `https://aidar-dashboard.onrender.com`
2. Должна быть синяя страница с логотипом и вкладками
3. Если видишь — ✅ готово!

---

## 📝 Что изменилось в коде

- ✅ Обновлён `requirements.txt` с явным указанием `setuptools` и `wheel`
- ✅ Исправлен `app.py` для работы без pandas (если не установлен)
- ✅ Обновлён `build.sh` для явной установки инструментов сборки
- ✅ Улучшена команда сборки в `render.yaml`

---

## 🆘 Если всё ещё не работает

1. Проверь логи Render:
   - Web Service → **Logs** → ищи ошибки
   
2. Попробуй пересоздать Web Service вручную с нуля

3. Или развернись на **Railway.app** (иногда работает лучше):
   - https://railway.app
   - Проще с Python + автоматический cron

---

**Версия:** 2.1 (Render build fix)  
**Дата:** 24.03.2026
