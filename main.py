import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Настройка страницы
st.set_page_config(
    page_title="Анализатор CSV файлов", 
    layout="wide",
    page_icon="📊"
)

st.title("📊 Анализатор CSV файлов")
st.markdown("Загрузите CSV файл и проанализируйте его данные")

# ==================== 1. ЗАГРУЗКА ФАЙЛА ====================
st.header("1. Загрузите ваш CSV файл")

uploaded_file = st.file_uploader(
    "Перетащите файл сюда или нажмите для выбора",
    type=["csv"],
    help="Поддерживаются только файлы в формате CSV (таблицы)"
)

if not uploaded_file:
    st.info("📁 Загрузите CSV файл чтобы начать анализ")
    st.stop()

# Загрузка данных
with st.spinner("Загружаем ваши данные..."):
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()  # Убираем лишние пробелы в названиях



# Показываем информацию о файле
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📈 Всего строк", df.shape[0])
with col2:
    st.metric("📊 Всего колонок", df.shape[1])
with col3:
    missing_total = df.isnull().sum().sum()
    st.metric("⚠️ Пропущенных значений", missing_total)

# ==================== 2. БЫСТРЫЙ ПРОСМОТР ДАННЫХ ====================
st.header("2. Как выглядят ваши данные?")

# Показываем первые строки для знакомства
st.subheader("Первые 10 строк таблицы")
st.write("Вот как выглядят ваши данные:")
st.dataframe(df.head(10), use_container_width=True)

# Показываем названия колонок
with st.expander("📋 Показать все колонки и типы данных"):
    st.write("**Список всех колонок в вашем файле:**")
    for i, col in enumerate(df.columns, 1):
        st.write(f"{i}. **{col}** — тип: {df[col].dtype}")

# ==================== 3. ОЧИСТКА ДАННЫХ ====================
st.header("3. Очистка данных")

st.write("Давайте приведём данные в порядок:")

# Копируем данные для очистки
df_clean = df.copy()

# 3.1 Удаление дубликатов
duplicates_count = df_clean.duplicated().sum()

if duplicates_count > 0:
    st.subheader("🔍 Найдены дубликаты")
    st.info(f"Обнаружено **{duplicates_count}** повторяющихся строк")
    
    if st.button(f"🗑️ Удалить {duplicates_count} дубликат(ов)", type="primary"):
        before = len(df_clean)
        df_clean = df_clean.drop_duplicates()
        after = len(df_clean)
        st.success(f"✅ Удалено {duplicates_count} повторяющихся строк")
else:
    st.success("🎉 Отлично! Дубликатов не найдено")

# 3.2 Обработка пропущенных значений
missing_values = df_clean.isnull().sum()
missing_cols = missing_values[missing_values > 0]

if not missing_cols.empty:
    st.subheader("⚠️ Пропущенные значения")
    st.write("В этих колонках есть пустые ячейки:")
    
    for col, count in missing_cols.items():
        percent = (count / len(df_clean)) * 100
        st.write(f"- **{col}**: {count} пропущенных значений ({percent:.1f}% от всех данных)")
        
        # Автоматически заполняем пропуски
        if df_clean[col].dtype == 'object':  # Текстовые данные
            df_clean[col].fillna('Не указано', inplace=True)
            st.info(f"   ↳ Заполнили текстом 'Не указано'")
        elif df_clean[col].dtype in ['int64', 'float64']:  # Числовые данные
            median_val = df_clean[col].median()
            df_clean[col].fillna(median_val, inplace=True)
            st.info(f"   ↳ Заполнили медианным значением: {median_val:.2f}")
    
    st.success("✅ Все пропущенные значения обработаны!")
else:
    st.success("✨ Пропущенных значений нет — отлично!")

# ПОКАЗЫВАЕМ ИСПРАВЛЕННУЮ ТАБЛИЦУ СРАЗУ ЖЕ
st.subheader("📋 Очищенная таблица")
st.write(f"**Теперь у вас {len(df_clean)} строк после очистки:**")
st.dataframe(df_clean.head(20), use_container_width=True)

with st.expander("👀 Показать всю очищенную таблицу"):
    st.dataframe(df_clean, use_container_width=True)

# ==================== 4. СТАТИСТИЧЕСКИЙ АНАЛИЗ ====================
st.header("4. Статистический анализ")

# Находим числовые колонки
numeric_columns = df_clean.select_dtypes(include=['number']).columns.tolist()

if numeric_columns:
    st.write("📈 Вот статистика по числовым данным:")
    
    # Показываем статистику для каждой числовой колонки
    for col in numeric_columns[:5]:  # Ограничиваем 5 колонками для читаемости
        with st.expander(f"📊 Статистика для колонки: **{col}**"):
            col_stats = df_clean[col].describe()
            
            # Красивые метрики
            cols = st.columns(4)
            with cols[0]:
                st.metric("Среднее", f"{col_stats['mean']:.2f}")
            with cols[1]:
                st.metric("Медиана", f"{col_stats['50%']:.2f}")
            with cols[2]:
                st.metric("Минимум", f"{col_stats['min']:.2f}")
            with cols[3]:
                st.metric("Максимум", f"{col_stats['max']:.2f}")
            
            st.write(f"📊 Стандартное отклонение: **{col_stats['std']:.2f}**")
            
            # Полная таблица статистики
            st.dataframe(col_stats.rename('Значение').to_frame())
    
    # Если колонок больше 5, предлагаем выбрать
    if len(numeric_columns) > 5:
        st.info(f"Ещё {len(numeric_columns)-5} числовых колонок. Используйте фильтры ниже для их анализа.")
else:
    st.info("ℹ️ В ваших данных нет числовых колонок для статистического анализа")

# ==================== 5. ФИЛЬТРАЦИЯ ДАННЫХ ====================
st.header("5. Фильтрация данных")

st.write("🔍 **Отфильтруйте данные по нужным критериям:**")

# Создаём один фильтр
filter_col = st.selectbox(
    "Выберите колонку для фильтрации:",
    options=["Выберите колонку..."] + df_clean.columns.tolist(),
    help="Выберите колонку, по которой хотите отфильтровать данные"
)

if filter_col != "Выберите колонку...":
    # Определяем тип данных выбранной колонки
    col_type = df_clean[filter_col].dtype
    
    if col_type in ['int64', 'float64']:
        # Фильтр для числовых данных
        st.write(f"🔢 Фильтруем числовую колонку: **{filter_col}**")
        
        min_val = float(df_clean[filter_col].min())
        max_val = float(df_clean[filter_col].max())
        current_val = float(df_clean[filter_col].median())
        
        filter_type = st.radio(
            "Выберите тип фильтра:",
            ["Диапазон значений", "Конкретное значение"],
            horizontal=True
        )
        
        if filter_type == "Диапазон значений":
            col1, col2 = st.columns(2)
            with col1:
                from_val = st.number_input(
                    "От:", 
                    min_value=min_val, 
                    max_value=max_val,
                    value=min_val,
                    key="from_val"
                )
            with col2:
                to_val = st.number_input(
                    "До:", 
                    min_value=min_val, 
                    max_value=max_val,
                    value=max_val,
                    key="to_val"
                )
            
            if st.button("🔍 Применить фильтр", type="primary"):
                filtered_df = df_clean[
                    (df_clean[filter_col] >= from_val) & 
                    (df_clean[filter_col] <= to_val)
                ]
                st.success(f"✅ Найдено {len(filtered_df)} строк")
                st.dataframe(filtered_df, use_container_width=True)
                df_clean = filtered_df.copy()
        
        else:  # Конкретное значение
            value = st.number_input(
                "Значение для поиска:",
                min_value=min_val,
                max_value=max_val,
                value=current_val
            )
            
            if st.button("🔍 Найти точное значение", type="primary"):
                filtered_df = df_clean[df_clean[filter_col] == value]
                st.success(f"✅ Найдено {len(filtered_df)} строк со значением {value}")
                st.dataframe(filtered_df, use_container_width=True)
                df_clean = filtered_df.copy()
    
    else:
        # Фильтр для текстовых данных
        st.write(f"🔤 Фильтруем текстовую колонку: **{filter_col}**")
        
        unique_values = df_clean[filter_col].dropna().unique()
        if len(unique_values) <= 20:
            # Если значений мало, показываем список
            selected_values = st.multiselect(
                "Выберите значения для показа:",
                options=unique_values,
                default=unique_values[:3] if len(unique_values) > 3 else unique_values
            )
            
            if selected_values and st.button("🔍 Применить фильтр", type="primary"):
                filtered_df = df_clean[df_clean[filter_col].isin(selected_values)]
                st.success(f"✅ Найдено {len(filtered_df)} строк")
                st.dataframe(filtered_df, use_container_width=True)
                df_clean = filtered_df.copy()
        else:
            # Если значений много, используем поиск
            search_text = st.text_input(
                "Введите текст для поиска:",
                placeholder="Начните вводить текст..."
            )
            
            if search_text and st.button("🔍 Найти", type="primary"):
                filtered_df = df_clean[
                    df_clean[filter_col].astype(str).str.contains(search_text, case=False, na=False)
                ]
                st.success(f"✅ Найдено {len(filtered_df)} строк, содержащих '{search_text}'")
                st.dataframe(filtered_df.head(50), use_container_width=True)
                df_clean = filtered_df.copy()

# ==================== 6. СОРТИРОВКА ДАННЫХ ====================
st.header("6. Сортировка данных")

st.write("📊 **Отсортируйте данные по важности:**")

sort_col1, sort_col2 = st.columns([2, 1])

with sort_col1:
    sort_column = st.selectbox(
        "Сортировать по колонке:",
        options=["Не сортировать"] + df_clean.columns.tolist(),
        help="Выберите колонку для сортировки"
    )

with sort_col2:
    if sort_column != "Не сортировать":
        sort_order = st.radio(
            "Порядок:",
            ["▲ По возрастанию", "▼ По убыванию"],
            horizontal=True,
            label_visibility="collapsed"
        )

if sort_column != "Не сортировать" and st.button("🔄 Отсортировать", type="primary"):
    ascending = sort_order == "▲ По возрастанию"
    df_sorted = df_clean.sort_values(by=sort_column, ascending=ascending)
    
    st.success(f"✅ Данные отсортированы по колонке '{sort_column}'")
    st.write(f"Показаны первые 20 строк после сортировки:")
    st.dataframe(df_sorted.head(20), use_container_width=True)
    
    with st.expander("👀 Показать все отсортированные данные"):
        st.dataframe(df_sorted, use_container_width=True)
    
    df_clean = df_sorted.copy()

# ==================== 7. ВИЗУАЛИЗАЦИЯ ДАННЫХ ====================
st.header("7. Визуализация данных")

if numeric_columns:
    st.write("📈 **Создайте наглядные графики:**")
    
    viz_type = st.selectbox(
        "Выберите тип графика:",
        ["Гистограмма (распределение)", 
         "Столбчатая диаграмма", 
         "Линейный график"]
    )
    
    if viz_type == "Гистограмма (распределение)":
        selected_col = st.selectbox(
            "Выберите колонку для анализа распределения:",
            numeric_columns
        )
        
        fig, ax = plt.subplots(figsize=(10, 6))
        df_clean[selected_col].hist(bins=30, ax=ax, color='#3498db', edgecolor='white', alpha=0.8)
        ax.set_title(f'📊 Распределение значений: {selected_col}', fontsize=16, pad=20)
        ax.set_xlabel(selected_col, fontsize=12)
        ax.set_ylabel('Количество записей', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
        st.caption(f"График показывает, как распределены значения в колонке '{selected_col}'")
    
    elif viz_type == "Столбчатая диаграмма":
        # Ищем категориальные колонки для группировки
        cat_cols = df_clean.select_dtypes(include=['object']).columns.tolist()
        
        if cat_cols and numeric_columns:
            col1, col2 = st.columns(2)
            with col1:
                category_col = st.selectbox("Группировать по:", cat_cols)
            with col2:
                value_col = st.selectbox("Значение для сравнения:", numeric_columns)
            
            # Группируем данные
            grouped_data = df_clean.groupby(category_col)[value_col].mean().sort_values(ascending=False).head(15)
            
            fig, ax = plt.subplots(figsize=(12, 6))
            bars = ax.bar(grouped_data.index, grouped_data.values, color='#2ecc71', edgecolor='white', alpha=0.8)
            ax.set_title(f'📊 Среднее значение {value_col} по {category_col}', fontsize=16, pad=20)
            ax.set_xlabel(category_col, fontsize=12)
            ax.set_ylabel(f'Среднее {value_col}', fontsize=12)
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True, alpha=0.3, axis='y')
            
            # Добавляем значения на столбцы
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}', ha='center', va='bottom')
            
            st.pyplot(fig)
    
    elif viz_type == "Линейный график":
        if len(numeric_columns) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                x_col = st.selectbox("Ось X (горизонтальная):", numeric_columns)
            with col2:
                y_col = st.selectbox("Ось Y (вертикальная):", 
                                   [c for c in numeric_columns if c != x_col])
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(df_clean[x_col], df_clean[y_col], 'o-', markersize=4, 
                   linewidth=2, color='#e74c3c', alpha=0.7)
            ax.set_title(f'📈 {y_col} в зависимости от {x_col}', fontsize=16, pad=20)
            ax.set_xlabel(x_col, fontsize=12)
            ax.set_ylabel(y_col, fontsize=12)
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
else:
    st.info("📊 Для визуализации нужны числовые данные. В вашей таблице их нет.")

# ==================== 8. СОХРАНЕНИЕ РЕЗУЛЬТАТОВ ====================
st.header("8. Сохранение результатов")

st.write("💾 **Ваши данные готовы! Сохраните результат работы:**")

# Информация о финальных данных
final_rows = len(df_clean)
final_cols = len(df_clean.columns)
original_rows = len(df)

st.info(f"""
📊 **Итоги вашего анализа:**
- Изначально было: **{original_rows}** строк
- После очистки и фильтрации: **{final_rows}** строк
- Количество колонок: **{final_cols}**
""")

# Предпросмотр финальных данных
with st.expander("👁️ Предварительный просмотр финальных данных"):
    st.write(f"Показано 15 из {final_rows} строк:")
    st.dataframe(df_clean.head(15), use_container_width=True)

# Кнопка скачивания
csv_data = df_clean.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')

st.download_button(
    label="📥 Скачать обработанные данные (CSV)",
    data=csv_data,
    file_name="очищенные_данные.csv",
    mime="text/csv",
    help="Нажмите чтобы сохранить результат вашей работы",
    type="primary"
)

# ==================== 9. ЗАВЕРШЕНИЕ ====================

st.markdown("""
---
### Что дальше?
1. 📥 **Скачайте** обработанные данные кнопкой выше
2. 📊 **Используйте** эти данные для отчётов или презентаций
3. 🔄 **Загрузите** новый файл для продолжения анализа

**Спасибо за использование анализатора CSV файлов!** ✨
""")