from flask import Flask, request, jsonify, render_template
import sheets

sheet_id = "1Jl0OhcH-LhXsI9fIo58pIfEPMrOuBKUHLq_-udr7OjA" # id нашей таблицы
SERVICE_ACCOUNT_FILE = "../gcp_key.json"  # файл с ключом

app = Flask(__name__)

# допустимые названия домашки
hw_names = dict()
hw_names = {"hw-01" : "hw-01-git",
            "hw_01" : "hw-01-git",
            "hw-02" : "hw-02-типы и структуры данных",
            "hw_02" : "hw-02-типы и структуры данных",
            "main-hw-01" : "main-hw-01",
            "big-hw-01" : "main-hw-01",
            "main-hw-02" : "main-hw-02",
            "big-hw-02" : "main-hw-02",
            }

# существующие группы
groups = ["23137", "23144"]


@app.route('/')
def index():
    return 'Главная страница'


@app.route('/names')
def names():

    sheet_read = sheets.get_sheet(SERVICE_ACCOUNT_FILE, sheet_id, 'A2:A27')
    values = sheet_read.get('values', [])

    NAMES = {"names" : [value[0] for value in values]}

    return jsonify(NAMES)


@app.route('/<hw_name>/mean_score')
def mean_score(hw_name):
    if not hw_name in hw_names:
        return "Такой домашки нет:(", 400
    sheet_read = sheets.get_sheet(SERVICE_ACCOUNT_FILE, sheet_id, f'{hw_names[hw_name]}!D2:D27')
    return ("Средний балл всех участников курса за домашку {hw_name}:  \n" + str(
        sheets.mean_score(sheet_read))).format(hw_name=hw_name)


@app.route('/<hw_name>/<group_id>/mean_score')
def mean_score_by_group(hw_name, group_id):
    if not hw_name in hw_names and not group_id in groups:
        return "Выбранные группа и домашка не существуют.", 400
    if not hw_name in hw_names:
        return "Такой домашки нет:(", 400
    if not group_id in groups:
        return "Такой группы не существует:(", 400
    data = sheets.get_sheet(SERVICE_ACCOUNT_FILE, sheet_id, f"{hw_names[hw_name]}!B2:D27")

    return ("Средний балл группы {group_id} за домашку {hw_name}: \n" + str(
        sheets.mean_score_by_group(data, group_id))).format(hw_name=hw_name, group_id=group_id)


@app.route('/mean_score')
def mean_score_by_group1():
    group_id = request.args.get('group_id')
    hw_name = request.args.get('hw_name')

    if group_id and hw_name:
        return mean_score_by_group(hw_name, group_id)
    else:
        return "Нет данных"


@app.route('/mark')
def mark():
    student_id = request.args.get('student_id')
    group_id = request.args.get('group_id')

    # случай, когда указана только группа
    if student_id != None and group_id == None:
        id = int(student_id)

        if id < 1 or id > 23:
            return "Студента с таким id не существует", 400

        data = sheets.get_sheet(SERVICE_ACCOUNT_FILE, sheet_id, "A2:E24")

        values = data.get('values', [])

        values1 = [val[0] for val in values if val[4] == student_id]
        name_of_student = values1[0]

        results = sheets.get_sheet(SERVICE_ACCOUNT_FILE, sheet_id, "Итог!A2:H24")

        res_vals = results.get('values', [])

        res_vals1 = [val[6] for val in res_vals if val[0] == name_of_student]
        score = int(res_vals1[0])

        mark = 0

        if score < 10:
            mark = 2
        elif score >= 10 and score < 30:
            mark = 3
        elif score >= 30 and score < 70:
            mark = 4
        else:
            mark = 5

        return f"{name_of_student}, оценка за зачетную неделю: {mark}"

    # случай, когда указан только id студента
    if student_id == None and group_id != None:

        if not group_id in groups:
            return "Такой группы не существует:(", 400

        data = sheets.get_sheet(SERVICE_ACCOUNT_FILE, sheet_id, "Итог!A2:H24")
        values = data.get('values', [])

        values1 = [int(val[7]) for val in values if val[1] == group_id]

        return f"Группа {group_id}, средняя оценка: " + sheets.count_mean(values1)

    # остальные случаи
    if (student_id != None and group_id != None) or (student_id == None and group_id == None):
        return "Некорректно введены данные", 400


@app.route('/course_table')
def course_table():
    hw_name = request.args.get('hw_name')
    group_id = request.args.get('group_id')

    if not hw_name:
        return "Не указана домашка", 400

    if hw_name not in hw_names:
        return "Такой домашки нет:(", 400

    if group_id != None:
        if group_id not in groups:
            return "Такой группы не существует:(", 400

    sheet_name = hw_names[hw_name]
    data = sheets.get_sheet(SERVICE_ACCOUNT_FILE, sheet_id, f'{sheet_name}!A2:E27')
    values = data.get('values', [])

    # подготавливаем данные для таблицы
    table_data = []
    for val in values:
        # проверяем группу, если она указана
        if not group_id or val[1] == group_id:
            table_data.append({
                'name': val[0],
                'group': val[1],
                'score': val[3] if len(val) > 3 else 'N/A'
            })

    # рендерим таблицу
    return render_template('course_table.html',
                           table_data=table_data,
                           hw_name=hw_name,
                           group_id=group_id if group_id else "Все группы")


if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 1337)
