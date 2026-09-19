import pandas as pd

file_path = r"C:\Users\user\Desktop\med.xlsx"

print("Загрузка данных...")

df = pd.read_excel(file_path, engine="openpyxl")

print(f"Файл загружен. Всего строк: {len(df)}")

print("\nДоступные столбцы в файле:")
print(df.columns.tolist())

print("=" * 60)

selected_columns = [
    "Systolic Blood Pressure",
    "Diastolic Blood Pressure",
    "Risk Score CVRM",
    "BMI",
    "Glucose Fasting",
    "Total Cholesterol",
    "MDRD",
    "Hypertension"
]

available_columns = [
    col for col in selected_columns
    if col in df.columns
]

print("Выбранные столбцы:")
print(available_columns)

if len(available_columns) != len(selected_columns):
    print("\nНекоторые столбцы не найдены.")

    missing_columns = [
        col for col in selected_columns
        if col not in df.columns
    ]

    print("Отсутствуют:")
    print(missing_columns)

    exit()

data = df[selected_columns].copy()

print("\nРазмер нового датафрейма:")
print(data.shape)

print("\nПервые 5 строк:")
print(data.head())

print("\n" + "=" * 60)
print("Удаление пустых ячеек")

print("Количество пустых значений:")
print(data.isnull().sum())

data = data.dropna().copy()

print(f"\nПосле удаления пустых строк: {len(data)}")

print("\n" + "=" * 60)
print("Удаление некорректных значений")

numeric_columns = [
    "Systolic Blood Pressure",
    "Diastolic Blood Pressure",
    "Risk Score CVRM",
    "BMI",
    "Glucose Fasting",
    "Total Cholesterol",
    "MDRD"
]

for column in numeric_columns:
    data[column] = pd.to_numeric(
        data[column],
        errors="coerce"
    )

data = data.dropna().copy()

valid_data = (
    data["Systolic Blood Pressure"].between(90, 230)
    & data["Diastolic Blood Pressure"].between(40, 120)
    & data["Risk Score CVRM"].between(0, 50)
    & data["BMI"].between(15, 45)
    & data["Glucose Fasting"].between(3, 25)
    & data["Total Cholesterol"].between(2, 15)
    & data["MDRD"].between(15, 140)
)

data = data[valid_data].copy()

print("Коридоры значений проверены.")
print(f"После удаления некорректных значений: {len(data)}")

print("\n" + "=" * 60)
print("Преобразование нечисловых значений")

categorical_columns = data.select_dtypes(
    include=["object", "category", "bool"]
).columns.tolist()

print("Нечисловые столбцы:")
print(categorical_columns)

if categorical_columns:
    data = pd.get_dummies(
        data,
        columns=categorical_columns,
        dtype=int
    )

print("\nПреобразование завершено.")

print("\n" + "=" * 60)
print("Итоговый ДАТАФРЕЙМ")

print(f"Количество строк: {len(data)}")
print(f"Количество столбцов: {len(data.columns)}")

print("\nСтолбцы:")
print(data.columns.tolist())

print("\nПервые 5 строк:")
print(data.head())

if len(data) >= 20000:
    print("\nУсловие выполнено: строк больше 20 000.")
else:
    print("\nОшибка строк меньше 20 000.")

output_file = r"C:\Users\user\Desktop\med_hypertension_prepared.xlsx"

data.to_excel(
    output_file,
    index=False
)

print(f"\nГотовый датасет сохранён:")
print(output_file)