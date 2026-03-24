#!/usr/bin/env python3
"""
Обновление данных дашборда с WB API и МойСклад API
Запускается каждый день в 06:00 UTC
"""

import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import os
from collections import defaultdict

DATA_DIR = "/root/frost-ai/users/583297536/dashboard/data"
os.makedirs(DATA_DIR, exist_ok=True)

# Токены
WB_TOKEN_FILE = "/root/frost-ai/users/583297536/files/secrets/wb_api_token.txt"
MOYSKLAD_TOKEN_FILE = "/root/frost-ai/users/583297536/files/secrets/moysklad_api_token.txt"

def load_token(filepath):
    """Загружает токен из файла"""
    try:
        with open(filepath, 'r') as f:
            return f.read().strip()
    except:
        return None

def fetch_wb_sales():
    """Загружает последние продажи с WB API"""
    print("[WB] Загружаю продажи за последние 30 дней...")
    
    wb_token = load_token(WB_TOKEN_FILE)
    if not wb_token:
        print("❌ WB токен не найден")
        return None
    
    try:
        # Даты для WB API (ISO format YYYY-MM-DD)
        date_to = datetime.utcnow()
        date_from = date_to - timedelta(days=30)
        
        date_from_str = date_from.strftime('%Y-%m-%d')
        date_to_str = date_to.strftime('%Y-%m-%d')
        
        url = "https://statistics-api.wildberries.ru/api/v1/supplier/sales"
        headers = {'Authorization': wb_token}
        params = {
            'dateFrom': date_from_str,
            'dateTo': date_to_str,
            'limit': 10000,
        }
        
        print(f"   Запрос: {date_from.date()} - {date_to.date()}")
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            sales = response.json()
            print(f"   ✅ Получено {len(sales)} записей продаж")
            return sales
        elif response.status_code == 429:
            print(f"   ⚠️  API лимит (429). Пробую через 60 сек...")
            import time
            time.sleep(61)
            response = requests.get(url, headers=headers, params=params, timeout=30)
            if response.status_code == 200:
                sales = response.json()
                print(f"   ✅ Получено {len(sales)} записей продаж")
                return sales
        else:
            print(f"   ❌ WB API ошибка {response.status_code}: {response.text[:200]}")
            return None
    
    except Exception as e:
        print(f"   ❌ WB ошибка: {str(e)}")
        return None

def fetch_wb_orders():
    """Загружает заказы с WB API"""
    print("[WB] Загружаю заказы за последние 30 дней...")
    
    wb_token = load_token(WB_TOKEN_FILE)
    if not wb_token:
        print("❌ WB токен не найден")
        return None
    
    try:
        date_to = datetime.utcnow()
        date_from = date_to - timedelta(days=30)
        
        date_from_str = date_from.strftime('%Y-%m-%d')
        date_to_str = date_to.strftime('%Y-%m-%d')
        
        url = "https://statistics-api.wildberries.ru/api/v1/supplier/orders"
        headers = {'Authorization': wb_token}
        params = {
            'dateFrom': date_from_str,
            'dateTo': date_to_str,
            'limit': 10000,
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            orders = response.json()
            print(f"   ✅ Получено {len(orders)} заказов")
            return orders
        else:
            print(f"   ⚠️  WB orders API ошибка {response.status_code}")
            return None
    
    except Exception as e:
        print(f"   ❌ WB orders ошибка: {str(e)}")
        return None

def fetch_moysklad_stock():
    """Загружает остатки с МойСклад API"""
    print("[МойСклад] Загружаю остатки...")
    
    moysklad_token = load_token(MOYSKLAD_TOKEN_FILE)
    if not moysklad_token:
        print("❌ МойСклад токен не найден")
        return None
    
    try:
        url = "https://api.moysklad.ru/api/remap/1.2/entity/product"
        headers = {
            'Authorization': f'Bearer {moysklad_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('rows', [])
            print(f"   ✅ Получено {len(products)} товаров")
            return products
        else:
            print(f"   ❌ МойСклад API ошибка {response.status_code}")
            return None
    
    except Exception as e:
        print(f"   ❌ МойСклад ошибка: {str(e)}")
        return None

def process_wb_data(sales, orders):
    """Обрабатывает данные WB и создает финансовый отчет"""
    print("[PROCESS] Обработка данных WB...")
    
    if not sales:
        print("   ❌ Нет данных продаж")
        return None
    
    try:
        # Конвертируем в DataFrame для удобства
        sales_df = pd.DataFrame(sales)
        
        # Основные метрики
        total_revenue = sales_df['salePrice'].sum() if 'salePrice' in sales_df else 0
        total_quantity = len(sales_df)
        
        # Группируем по товарам (nmId)
        by_product = sales_df.groupby('nmId').agg({
            'salePrice': ['sum', 'count'],
            'saleCost': 'sum',
        }).reset_index() if 'nmId' in sales_df else None
        
        # Финансовые метрики
        report = {
            'updated': datetime.utcnow().isoformat(),
            'period_start': (datetime.utcnow() - timedelta(days=30)).isoformat(),
            'period_end': datetime.utcnow().isoformat(),
            'metrics': {
                'total_revenue': float(total_revenue),
                'total_quantity': int(total_quantity),
                'average_check': float(total_revenue / total_quantity) if total_quantity > 0 else 0,
                'unique_products': len(sales_df['nmId'].unique()) if 'nmId' in sales_df else 0,
            },
            'daily_data': [],
            'status': 'success'
        }
        
        # Подготавливаем дневные данные (если есть дата продажи)
        if 'saleDt' in sales_df:
            sales_df['date'] = pd.to_datetime(sales_df['saleDt'])
            daily = sales_df.groupby(sales_df['date'].dt.date).agg({
                'salePrice': 'sum',
                'nmId': 'count'
            }).reset_index()
            
            for _, row in daily.iterrows():
                report['daily_data'].append({
                    'date': row['date'].isoformat(),
                    'revenue': float(row['salePrice']),
                    'orders': int(row['nmId'])
                })
        
        print(f"   ✅ Обработано: выручка {total_revenue:,.0f}₽, заказов {total_quantity}")
        return report
    
    except Exception as e:
        print(f"   ❌ Ошибка обработки: {str(e)}")
        return None

def save_data(filename, data):
    """Сохраняет JSON данные"""
    try:
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"   ✅ Сохранено: {filename}")
        return True
    except Exception as e:
        print(f"   ❌ Ошибка сохранения: {str(e)}")
        return False

def main():
    """Основной скрипт обновления"""
    print("\n" + "="*70)
    print("🔄 ОБНОВЛЕНИЕ ДАННЫХ ДАШБОРДА")
    print(f"⏰ Время: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("="*70 + "\n")
    
    # Загружаем данные с API
    sales = fetch_wb_sales()
    orders = fetch_wb_orders()
    moysklad = fetch_moysklad_stock()
    
    # Обрабатываем данные
    if sales:
        wb_report = process_wb_data(sales, orders)
        if wb_report:
            save_data('wb_report.json', wb_report)
    
    # Сохраняем МойСклад данные
    if moysklad:
        moysklad_data = {
            'updated': datetime.utcnow().isoformat(),
            'count': len(moysklad),
            'status': 'success'
        }
        save_data('moysklad_stock.json', moysklad_data)
    
    # Создаем статус файл
    status = {
        'updated': datetime.utcnow().isoformat(),
        'wb_status': 'success' if sales else 'error',
        'moysklad_status': 'success' if moysklad else 'error',
        'last_update': datetime.utcnow().isoformat(),
    }
    save_data('status.json', status)
    
    print("\n" + "="*70)
    print("✅ ОБНОВЛЕНИЕ ЗАВЕРШЕНО")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
