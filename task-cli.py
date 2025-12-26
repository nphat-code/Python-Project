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
        if len(sys.argv) < 3:
            print("Error: Please provide a task description.")
        else:
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
else:
    print("Usage: python script.py add <description>")
