import sys
import json
from datetime import datetime

def load_data(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"next_id": 1, "tasks": []}
    
def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

filename = "task_list.json"
data = load_data(filename)
if len(sys.argv) > 1:
    if sys.argv[1] == "add":
        if len(sys.argv) == 3:
            new_task = {
                "id": data["next_id"],
                "description": sys.argv[2],
                "status": "todo",
                "createdAt": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "updatedAt": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
            data["tasks"].append(new_task)
            data["next_id"] += 1
            save_data(filename, data)
            print(f"Task added successfully (ID: {new_task["id"]})")
    elif sys.argv[1] == "list":
        if len(sys.argv) == 2:
            print(f"{"ID":5} {"Description":15} {"Status":10} {"Created At":25} {"Updated At":25}")
            for task in data["tasks"]:
                print(f"{str(task["id"]):5} {task["description"]:15} {task["status"]:10} {task["createdAt"]:25} {task["updatedAt"]:25}")
        elif len(sys.argv) == 3:
            print(f"{"ID":5} {"Description":15} {"Status":10} {"Created At":25} {"Updated At":25}")
            for task in data["tasks"]:
                if task["status"] == sys.argv[2]:
                    print(f"{str(task["id"]):5} {task["description"]:15} {task["status"]:10} {task["createdAt"]:25} {task["updatedAt"]:25}")
    elif sys.argv[1] == "update":
        if len(sys.argv) == 4:
            for task in data["tasks"]:
                if str(task["id"]) == sys.argv[2]:
                    task["description"] = sys.argv[3]
                    save_data(filename, data)
                    print(f"Task updated successfully (ID: {task["id"]})")
                    break
    elif sys.argv[1] == "delete":
        if len(sys.argv) == 3:
            for task in data["tasks"]:
                if str(task["id"]) == sys.argv[2]:
                    data["tasks"].remove(task)
                    save_data(filename, data)
                    print(f"Task deleted successfully (ID: {task["id"]})")
                    break
else:
    print("Usage: python script.py add <description>")

