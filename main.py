import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Настройка страницы
st.set_page_config(page_title="Анализатор CSV", layout="wide")
st.title("📊 Анализатор CSV файлов")

# Загрузка файла
st.header("1. Загрузка данных")
file1 = st.file_uploader("Загрузите CSV файл", type=["csv"])

if file1:
    # Загрузка данных
    df = pd.read_csv(file1)
    df.columns = df.columns.str.strip()
    
    st.success(f"✅ Файл загружен: {df.shape[0]} строк, {df.shape[1]} столбцов")
    
    # Показ ВСЕХ данных
    st.header("2. Просмотр данных")
    st.write(f"**Всего строк:** {len(df)}")
    st.write(f"**Всего столбцов:** {len(df.columns)}")
    
    # Показываем ВСЕ данные
    st.subheader("Все данные:")
    st.dataframe(df)
    
    # Статистика
    st.header("3. Статистика")
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if numeric_cols:
        st.write("**Числовые колонки:**")
        st.dataframe(df[numeric_cols].describe())
    else:
        st.info("Нет числовых колонок для статистики")
    
    # Очистка
    st.header("4. Очистка данных")
    df_clean = df.copy()
    duplicates_count = df_clean.duplicated().sum()
    df_clean = df_clean.drop_duplicates()
    
    # Заполняем пропуски
    for col in df_clean.columns:
        if df_clean[col].dtype == 'object':
            df_clean[col].fillna('Не указано', inplace=True)
        elif df_clean[col].dtype in ['int64', 'float64']:
            df_clean[col].fillna(df_clean[col].median(), inplace=True)
    
    st.write(f"**Удалено дубликатов:** {duplicates_count}")
    st.write(f"**После очистки строк:** {df_clean.shape[0]}")
    
    # Показываем ВСЕ очищенные данные
    st.subheader("Очищенные данные:")
    st.dataframe(df_clean)
    
    # ---------- ШАГ 5: ФИЛЬТРАЦИЯ ДАННЫХ ----------
    st.header("5. Фильтрация данных")
    
    # Получаем все колонки для фильтрации
    all_columns = df_clean.columns.tolist()
    
    # Первый фильтр
    st.subheader("Фильтр 1:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_col1 = st.selectbox(
            "Выберите колонку для фильтрации:",
            options=["Не фильтровать"] + all_columns,
            key="filter_col1"
        )
    
    with col2:
        if filter_col1 != "Не фильтровать":
            # Для числовых колонок
            if df_clean[filter_col1].dtype in ['int64', 'float64']:
                filter_operator1 = st.selectbox(
                    "Оператор:",
                    ["Больше чем (>)", "Меньше чем (<)", "Равно (=)", "Между"],
                    key="filter_op1_num"
                )
            # Для текстовых колонок
            else:
                filter_operator1 = st.selectbox(
                    "Оператор:",
                    ["Равно (=)", "Содержит", "Не содержит"],
                    key="filter_op1_text"
                )
    
    with col3:
        if filter_col1 != "Не фильтровать":
            if df_clean[filter_col1].dtype in ['int64', 'float64']:
                # Числовые значения
                unique_vals = df_clean[filter_col1].dropna().unique()
                if len(unique_vals) > 0:
                    min_val = float(df_clean[filter_col1].min())
                    max_val = float(df_clean[filter_col1].max())
                    
                    if filter_operator1 == "Между":
                        col_range1, col_range2 = st.columns(2)
                        with col_range1:
                            filter_value1_min = st.number_input(
                                "От:", 
                                min_value=min_val, 
                                max_value=max_val,
                                value=min_val,
                                key="filter_val1_min"
                            )
                        with col_range2:
                            filter_value1_max = st.number_input(
                                "До:", 
                                min_value=min_val, 
                                max_value=max_val,
                                value=max_val,
                                key="filter_val1_max"
                            )
                        filter_value1 = (filter_value1_min, filter_value1_max)
                    else:
                        filter_value1 = st.number_input(
                            "Значение:", 
                            min_value=min_val, 
                            max_value=max_val,
                            value=float(df_clean[filter_col1].median()),
                            key="filter_val1"
                        )
            else:
                # Текстовые значения
                unique_vals = df_clean[filter_col1].dropna().unique()
                if len(unique_vals) > 0:
                    filter_value1 = st.selectbox(
                        "Значение:",
                        options=["Введите значение"] + sorted([str(v) for v in unique_vals]),
                        key="filter_val1_text"
                    )
    
    # Второй фильтр (опционально)
    st.subheader("Фильтр 2 (опционально):")
    col4, col5, col6 = st.columns(3)
    
    with col4:
        filter_col2 = st.selectbox(
            "Выберите колонку для фильтрации:",
            options=["Не использовать"] + [c for c in all_columns if c != filter_col1 or filter_col1 == "Не фильтровать"],
            key="filter_col2"
        )
    
    with col5:
        if filter_col2 != "Не использовать":
            if df_clean[filter_col2].dtype in ['int64', 'float64']:
                filter_operator2 = st.selectbox(
                    "Оператор:",
                    ["Больше чем (>)", "Меньше чем (<)", "Равно (=)", "Между"],
                    key="filter_op2_num"
                )
            else:
                filter_operator2 = st.selectbox(
                    "Оператор:",
                    ["Равно (=)", "Содержит", "Не содержит"],
                    key="filter_op2_text"
                )
    
    with col6:
        if filter_col2 != "Не использовать":
            if df_clean[filter_col2].dtype in ['int64', 'float64']:
                unique_vals = df_clean[filter_col2].dropna().unique()
                if len(unique_vals) > 0:
                    min_val = float(df_clean[filter_col2].min())
                    max_val = float(df_clean[filter_col2].max())
                    
                    if filter_operator2 == "Между":
                        col_range1, col_range2 = st.columns(2)
                        with col_range1:
                            filter_value2_min = st.number_input(
                                "От:", 
                                min_value=min_val, 
                                max_value=max_val,
                                value=min_val,
                                key="filter_val2_min"
                            )
                        with col_range2:
                            filter_value2_max = st.number_input(
                                "До:", 
                                min_value=min_val, 
                                max_value=max_val,
                                value=max_val,
                                key="filter_val2_max"
                            )
                        filter_value2 = (filter_value2_min, filter_value2_max)
                    else:
                        filter_value2 = st.number_input(
                            "Значение:", 
                            min_value=min_val, 
                            max_value=max_val,
                            value=float(df_clean[filter_col2].median()),
                            key="filter_val2"
                        )
            else:
                unique_vals = df_clean[filter_col2].dropna().unique()
                if len(unique_vals) > 0:
                    filter_value2 = st.selectbox(
                        "Значение:",
                        options=["Введите значение"] + sorted([str(v) for v in unique_vals]),
                        key="filter_val2_text"
                    )
    
    # Применяем фильтры
    if st.button("Применить фильтры", type="primary"):
        filtered_df = df_clean.copy()
        
        # Применяем первый фильтр
        if filter_col1 != "Не фильтровать":
            if df_clean[filter_col1].dtype in ['int64', 'float64']:
                if filter_operator1 == "Больше чем (>)":
                    filtered_df = filtered_df[filtered_df[filter_col1] > filter_value1]
                elif filter_operator1 == "Меньше чем (<)":
                    filtered_df = filtered_df[filtered_df[filter_col1] < filter_value1]
                elif filter_operator1 == "Равно (=)":
                    filtered_df = filtered_df[filtered_df[filter_col1] == filter_value1]
                elif filter_operator1 == "Между":
                    filtered_df = filtered_df[
                        (filtered_df[filter_col1] >= filter_value1[0]) & 
                        (filtered_df[filter_col1] <= filter_value1[1])
                    ]
            else:
                if filter_operator1 == "Равно (=)":
                    filtered_df = filtered_df[filtered_df[filter_col1] == filter_value1]
                elif filter_operator1 == "Содержит":
                    filtered_df = filtered_df[filtered_df[filter_col1].astype(str).str.contains(str(filter_value1), na=False)]
                elif filter_operator1 == "Не содержит":
                    filtered_df = filtered_df[~filtered_df[filter_col1].astype(str).str.contains(str(filter_value1), na=False)]
        
        # Применяем второй фильтр
        if filter_col2 != "Не использовать":
            if df_clean[filter_col2].dtype in ['int64', 'float64']:
                if filter_operator2 == "Больше чем (>)":
                    filtered_df = filtered_df[filtered_df[filter_col2] > filter_value2]
                elif filter_operator2 == "Меньше чем (<)":
                    filtered_df = filtered_df[filtered_df[filter_col2] < filter_value2]
                elif filter_operator2 == "Равно (=)":
                    filtered_df = filtered_df[filtered_df[filter_col2] == filter_value2]
                elif filter_operator2 == "Между":
                    filtered_df = filtered_df[
                        (filtered_df[filter_col2] >= filter_value2[0]) & 
                        (filtered_df[filter_col2] <= filter_value2[1])
                    ]
            else:
                if filter_operator2 == "Равно (=)":
                    filtered_df = filtered_df[filtered_df[filter_col2] == filter_value2]
                elif filter_operator2 == "Содержит":
                    filtered_df = filtered_df[filtered_df[filter_col2].astype(str).str.contains(str(filter_value2), na=False)]
                elif filter_operator2 == "Не содержит":
                    filtered_df = filtered_df[~filtered_df[filter_col2].astype(str).str.contains(str(filter_value2), na=False)]
        
        st.success(f"✅ Данные отфильтрованы! Осталось {len(filtered_df)} из {len(df_clean)} строк")
        
        # Показываем отфильтрованные данные
        st.subheader("Отфильтрованные данные:")
        st.dataframe(filtered_df)
        
        # Обновляем основную таблицу
        df_clean = filtered_df
    else:
        # Если фильтры не применены, показываем исходные данные
        st.info("Настройте фильтры и нажмите 'Применить фильтры'")
    
    # ---------- ШАГ 6: СОРТИРОВКА ДАННЫХ ----------
    st.header("6. Сортировка данных")
    
    # Выбираем колонку для сортировки
    sort_column = st.selectbox(
        "Выберите колонку для сортировки:",
        options=df_clean.columns.tolist(),
        key="sort_column"
    )
    
    # Выбираем порядок сортировки
    sort_order = st.radio(
        "Порядок сортировки:",
        ["По возрастанию (A-Z, 0-9)", "По убыванию (Z-A, 9-0)"],
        horizontal=True,
        key="sort_order"
    )
    
    # Применяем сортировку
    if sort_column:
        ascending = sort_order == "По возрастанию (A-Z, 0-9)"
        df_sorted = df_clean.sort_values(by=sort_column, ascending=ascending)
        
        st.write(f"**Данные отсортированы по колонке:** {sort_column}")
        st.write(f"**Порядок:** {'По возрастанию' if ascending else 'По убыванию'}")
        
        # Показываем отсортированные данные
        st.dataframe(df_sorted)
        
        # Обновляем основную таблицу на отсортированную
        df_clean = df_sorted
    else:
        st.info("Выберите колонку для сортировки")
    
    # ---------- ГРАФИКИ ----------
    st.header("7. Визуализация")
    
    if numeric_cols:
        # Выбор типа графика
        chart_type = st.selectbox(
            "Выберите тип графика:",
            ["Гистограмма", "Линейный график", "Столбчатая диаграмма", "Точечная диаграмма"],
            key="chart_type"
        )
        
        if chart_type == "Гистограмма":
            col_for_hist = st.selectbox("Выберите колонку:", numeric_cols, key="hist_col")
            fig, ax = plt.subplots(figsize=(10, 6))
            df_clean[col_for_hist].hist(bins=30, ax=ax, color='skyblue', edgecolor='black')
            ax.set_title(f'Распределение {col_for_hist}')
            ax.set_xlabel(col_for_hist)
            ax.set_ylabel('Частота')
            st.pyplot(fig)
            plt.close()
            
        elif chart_type == "Линейный график":
            if len(numeric_cols) >= 2:
                x_col = st.selectbox("Ось X:", numeric_cols, key="line_x")
                y_col = st.selectbox("Ось Y:", [c for c in numeric_cols if c != x_col], key="line_y")
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(df_clean[x_col], df_clean[y_col], 'o-', markersize=4, linewidth=2)
                ax.set_title(f'{y_col} по {x_col}')
                ax.set_xlabel(x_col)
                ax.set_ylabel(y_col)
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
                plt.close()
        
        elif chart_type == "Столбчатая диаграмма":
            # Найдем категориальные колонки
            cat_cols = df_clean.select_dtypes(include=['object']).columns.tolist()
            if cat_cols and numeric_cols:
                cat_col = st.selectbox("Категория:", cat_cols, key="bar_cat")
                num_col = st.selectbox("Значение:", numeric_cols, key="bar_val")
                
                # Группируем и строим график
                grouped = df_clean.groupby(cat_col)[num_col].mean().sort_values(ascending=False)
                fig, ax = plt.subplots(figsize=(12, 6))
                grouped.plot(kind='bar', ax=ax, color='lightgreen', edgecolor='black')
                ax.set_title(f'Среднее {num_col} по {cat_col}')
                ax.set_xlabel(cat_col)
                ax.set_ylabel(f'Среднее {num_col}')
                ax.tick_params(axis='x', rotation=45)
                st.pyplot(fig)
                plt.close()
        
        elif chart_type == "Точечная диаграмма" and len(numeric_cols) >= 2:
            x_col = st.selectbox("Ось X:", numeric_cols, key="scatter_x")
            y_col = st.selectbox("Ось Y:", [c for c in numeric_cols if c != x_col], key="scatter_y")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            scatter = ax.scatter(df_clean[x_col], df_clean[y_col], alpha=0.6, 
                               c=df_clean.index, cmap='viridis', s=50)
            ax.set_title(f'{y_col} vs {x_col}')
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.grid(True, alpha=0.3)
            
            plt.colorbar(scatter, ax=ax, label='Индекс строки')
            st.pyplot(fig)
            plt.close()
    
    # Merge с другой таблицей
    st.header("8. Объединение таблиц")
    file2 = st.file_uploader("Загрузите вторую таблицу (необязательно)", type=["csv"], key="file2")
    
    if file2:
        df2 = pd.read_csv(file2)
        df2.columns = df2.columns.str.strip()
        
        # Показываем ВСЕ данные второй таблицы
        st.write(f"**Вторая таблица: {df2.shape[0]} строк, {df2.shape[1]} столбцов**")
        st.dataframe(df2)
        
        # Ищем общие колонки
        common_cols = list(set(df_clean.columns) & set(df2.columns))
        
        if common_cols:
            st.write(f"**Общие колонки:** {common_cols}")
            
            merge_col = st.selectbox("Выберите колонку для объединения:", common_cols, key="merge_col")
            
            # Все виды merge - показываем ВСЕ данные
            st.subheader("INNER JOIN (только совпадения)")
            inner_merged = pd.merge(df_clean, df2, on=merge_col, how='inner')
            st.write(f"Строк: {len(inner_merged)}")
            st.dataframe(inner_merged)
            
            st.subheader("LEFT JOIN (все из первой + совпадения из второй)")
            left_merged = pd.merge(df_clean, df2, on=merge_col, how='left')
            st.write(f"Строк: {len(left_merged)}")
            st.dataframe(left_merged)
            
            st.subheader("RIGHT JOIN (все из второй + совпадения из первой)")
            right_merged = pd.merge(df_clean, df2, on=merge_col, how='right')
            st.write(f"Строк: {len(right_merged)}")
            st.dataframe(right_merged)
            
            st.subheader("FULL OUTER JOIN (все строки)")
            outer_merged = pd.merge(df_clean, df2, on=merge_col, how='outer')
            st.write(f"Строк: {len(outer_merged)}")
            st.dataframe(outer_merged)
        else:
            st.warning("Нет общих колонок для объединения")
            
            # CONCAT как вариант
            if st.button("Показать CONCAT (соединение таблиц)"):
                concat_df = pd.concat([df_clean, df2], ignore_index=True)
                st.subheader("CONCAT результат:")
                st.write(f"Строк: {len(concat_df)}")
                st.dataframe(concat_df)
    
    # Сохранение
    st.header("9. Сохранение результатов")
    
    csv_data = df_clean.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
    st.download_button(
        label="📥 Скачать обработанные данные",
        data=csv_data,
        file_name="обработанные_данные.csv",
        mime="text/csv"
    )

else:
    st.info("👆 Загрузите CSV файл для начала анализа")