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
    
    # Визуализация
    st.header("5. Визуализация")
    
    if numeric_cols:
        # Выбор типа графика
        chart_type = st.selectbox(
            "Выберите тип графика:",
            ["Гистограмма", "Линейный график", "Столбчатая диаграмма", "Точечная диаграмма"]
        )
        
        if chart_type == "Гистограмма":
            col_for_hist = st.selectbox("Выберите колонку:", numeric_cols)
            fig, ax = plt.subplots(figsize=(10, 6))
            df_clean[col_for_hist].hist(bins=30, ax=ax, color='skyblue', edgecolor='black')
            ax.set_title(f'Распределение {col_for_hist}')
            ax.set_xlabel(col_for_hist)
            ax.set_ylabel('Частота')
            st.pyplot(fig)
            plt.close()
            
        elif chart_type == "Линейный график":
            if len(numeric_cols) >= 2:
                x_col = st.selectbox("Ось X:", numeric_cols)
                y_col = st.selectbox("Ось Y:", [c for c in numeric_cols if c != x_col])
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
                cat_col = st.selectbox("Категория:", cat_cols)
                num_col = st.selectbox("Значение:", numeric_cols)
                
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
    st.header("6. Объединение таблиц")
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
            
            merge_col = st.selectbox("Выберите колонку для объединения:", common_cols)
            
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
    st.header("7. Сохранение результатов")
    
    csv_data = df_clean.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
    st.download_button(
        label="📥 Скачать обработанные данные",
        data=csv_data,
        file_name="обработанные_данные.csv",
        mime="text/csv"
    )

else:
    st.info("👆 Загрузите CSV файл для начала анализа")