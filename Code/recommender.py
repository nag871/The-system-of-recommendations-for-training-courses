import numpy as np

from text_processing import process_text

# Создание матрицы векторов курсов
def build_course_matrix(df_courses):
    # Берем весь текст из таблицы курсов
    df_courses['Full text'] = df_courses['Course'] + ' ' + df_courses['Description']
    courses_text = list(df_courses['Full text'])

    # Фильтруем текст
    filtered_courses = []
    for course in courses_text:
        filtered_courses.append(process_text(course))

    # Собираем все слова
    all_words = []
    for word in filtered_courses:
        all_words.extend(word)

    # Сортируем слова и убираем повторы, чтобы размерность векторов была одинаковая
    vocabulary = sorted(list(set(all_words)))
    vectors_courses = np.zeros((len(filtered_courses), len(vocabulary)))

    # Присваевыем каждому слову в векторе количество таких слов в описании курса
    for i, course_words in enumerate(filtered_courses):
        for j, word in enumerate(vocabulary):
            vectors_courses[i, j] = course_words.count(word)

    return vectors_courses, vocabulary


# Считаем рекомендации
def calculate_recommendations(student_marks, df_courses, vectors_courses, vocabulary):
    student_vector = np.zeros(len(vocabulary)) # Создаем для студента вектор той же длины, что и вектора курсов

    # Проходимся по всем курсам и находим тот курс, который студент закончил, чтобы дать ему веса в этих категориях
    for course_name, mark in student_marks.items():
        course_index = df_courses[df_courses['Course'] == course_name].index # Ищем курс, который студент изучил
        if not course_index.empty:
            idx = course_index[0]
            vector = vectors_courses[idx]
            student_vector += vector * (mark ** 2) # Добавляем вес соответствующий нашей оценки в квадрате (для наглядности)

    # Сами рекомендации
    recommendations = []
    # Проходимся по всем векторам курсов
    for i, course_vector in enumerate(vectors_courses):
        course_name = df_courses.iloc[i]['Course']

        # Если по курсу уже есть оценка, то пропускаем его
        if course_name in student_marks:
            continue

        # Подготавливаем значения для рассчета кос. Расстояния
        dot_product = np.dot(course_vector, student_vector)
        norm_course = np.linalg.norm(course_vector)
        norm_student = np.linalg.norm(student_vector)

        # Проверка на нуль
        if norm_course == 0 or norm_student == 0: similarity = 0.0
        else: similarity = dot_product / (norm_course * norm_student)

        # Если все хорошо добавляем наш курс и его степень схожести
        course_name = df_courses.iloc[i]['Course']
        recommendations.append([course_name, similarity])

    # Сортировка
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations