import data_loader
import recommender
import graphics


# Загружаем наши таблицы
df_courses = data_loader.load_courses_data()
df_students = data_loader.load_students_data()

if df_courses is None or df_students is None:
        print("The program cannot be started due to an I/O error.")
        exit()

# Создаем матрицу из векторов курсов
vectors_courses, vocabulary = recommender.build_course_matrix(df_courses)
all_recommendations = {}

# Вычисляем рекомендации для определенного студента и добавляем в словарь вида {ФИО: [список рекомендаций]}
for index, row in df_students.iterrows():
    student_recommendations = recommender.calculate_recommendations(row['Marks'], df_courses, vectors_courses, vocabulary)
    all_recommendations[row['Student']] = student_recommendations

# Вывод студентов в консоль
for student_name, recommendations_list in all_recommendations.items():
    print("-" * 50)
    print(f"Recommendations for student: {student_name} \n")

    for course_name, similarity in recommendations_list[:5]:
        print(f"{course_name} similarity: {similarity:.4f}")

# Подготовка к созданию тепловой карты
# Листы с именами\названиями для осей графика
student_list = list(all_recommendations.keys())
course_list = list(df_courses['Course'].unique())

graphics.make_heatmap(student_list, course_list, all_recommendations)