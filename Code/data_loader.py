import ast
import pandas as pd


def load_courses_data(file_path='../CSVs/Courses.csv'):
    try:
        df_courses = pd.read_csv(file_path)

        # Удаляем абсолютно пустые строки
        df_courses.dropna(subset=['Course', 'Description'], how='all', inplace=True)

        # Очищаем текст от случайных пробелов
        df_courses['Course'] = df_courses['Course'].astype(str).str.strip()
        df_courses['Description'] = df_courses['Description'].astype(str).str.strip()

        # Удаляем дубликаты курсов
        df_courses.drop_duplicates(subset=['Course'], keep='first', inplace=True)

        return df_courses.reset_index(drop=True)

    except FileNotFoundError:
        print(f"Error: {file_path}")
        return None


def load_students_data(file_path='../CSVs/Students.csv'):
    try:
        df_students = pd.read_csv(file_path)

        # Удаляем строки, где нет имени студента или поля с оценками
        df_students.dropna(subset=['Student', 'Marks'], how='any', inplace=True)

        # Очищаем имена студентов от случайных пробелов
        df_students['Student'] = df_students['Student'].astype(str).str.strip()

        # Удаляем дубликаты студентов
        df_students.drop_duplicates(subset=['Student'], keep='first', inplace=True)

        df_students['Marks'] = df_students['Marks'].apply(ast.literal_eval)

        return df_students.reset_index(drop=True)

    except FileNotFoundError:
        print(f"Error: {file_path}")
        return None