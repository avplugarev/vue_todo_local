#TODO В качестве базы данных у нас выступает словарик tasks_db с объектами TodoItem? где ключом являются ID этих задач.
# Мы хотим возвращать в соответствующем обработчике JSON, и поэтому надо доопределить метод to_dict ❺,
# который будет преобразовывать наши объекты TodoItem в словари. Мы будем использовать их для генерации
# ответа ❻ обработчику по пути /api/tasks/


import bottle
from truckpad.bottle.cors import CorsPlugin, enable_cors

app = bottle.Bottle()



class TodoItem:
    def __init__(self, description, unique_id):
        self.description = description
        self.is_completed = False
        self.uid = unique_id

    def __str__(self):
        return self.description.lower()

    #Мы хотим возвращать в соответствующем обработчике JSON, и поэтому надо доопределить метод to_dict
    #который будет преобразовывать наши объекты TodoItem в словари.
    def to_dict(self):
        return {
            "description": self.description,
            "is_completed": self.is_completed,
            "uid": self.uid
        }
#В качестве базы данных у нас выступает словарик tasks_db с объектами TodoItem? где ключом являются ID этих задач.
tasks_db = {
    uid: TodoItem(desc, uid)
    for uid, desc in enumerate(
        start=1,
        iterable=[
            "написать код",
            "покормить морскую свинку",
            "постирать кроссовки",
            "поесть еды",
        ])
}
"""
@enable_cors
@app.route("/api/tasks/")
def index():
    tasks = [task.to_dict() for task in tasks_db.values()]
    return {"tasks": tasks}

@enable_cors
@app.route("/api/add-task/", method=["POST"])
def add_task():
    desc = bottle.request.json['description']
    is_completed = bottle.request.json.get('is_completed', False)
    if len(desc) > 0:
        new_uid = max(tasks_db.keys()) + 1
        t = TodoItem(desc, new_uid)
        t.is_completed = is_completed
        tasks_db[new_uid] = t
    return "OK"
"""

@enable_cors
@app.route("/api/tasks/", method=["GET", "POST"])
def add_task():
    if bottle.request.method == "GET":
        tasks = [task.to_dict() for task in tasks_db.values()]
        return {"tasks": tasks}
    elif bottle.request.method == "POST":
        desc = bottle.request.json['description']
        is_completed = bottle.request.json.get('is_completed', False)
        if len(desc) > 0:
            new_uid = max(tasks_db.keys()) + 1
            t = TodoItem(desc, new_uid)
            t.is_completed = is_completed
            tasks_db[new_uid] = t
        return "OK"

#метод получения конкретного товара, изменения и удаления товара
@enable_cors
@app.route("/api/tasks/<uid:int>", method=["GET", "PUT", "DELETE"])
def show_or_modify_task(uid):
    if bottle.request.method == "GET":
        return tasks_db[uid].to_dict()
    elif bottle.request.method == "PUT":
        #В PUT нам могут приходить не все параметры, поэтому мы перестраховываемся в этом месте и проверяем их наличие
        # в приходящем JSON прежде чем править их в нашей "базе"
        if "description" in bottle.request.json:
            tasks_db[uid].description = bottle.request.json['description']
        if "is_completed" in bottle.request.json:
            print(bottle.request.json['is_completed'])
            tasks_db[uid].is_completed = bottle.request.json['is_completed']
        else:
            tasks_db[uid].is_completed = False
        return f"Modified task {uid}"
    elif bottle.request.method == "DELETE":
        tasks_db.pop(uid)
        return f"Deleted task {uid}"

"""
@enable_cors
@app.route("/api/delete/<uid:int>")
def api_delete(uid):
    tasks_db.pop(uid)
    return "Ok"

@enable_cors
@app.route("/api/complete/<uid:int>")
def api_complete(uid):
    tasks_db[uid].is_completed = True
    return "Ok"
"""

app.install(CorsPlugin(origins=['http://localhost:8080']))

###
if __name__ == "__main__":
    bottle.run(app, host="localhost", port=5000)

