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

def print_usage():
    """Displays instructions on how to use the CLI"""
    print("\n--- TASK TRACKER CLI USAGE ---")
    print("1. Add a task:         python script.py add \"task description\"")
    print("2. List all tasks:     python script.py list")
    print("3. Filter by status:   python script.py list todo/done/in-progress")
    print("4. Update description: python script.py update [ID] \"new description\"")
    print("5. Delete a task:      python script.py delete [ID]")
    print("6. Mark in progress:   python script.py mark-in-progress [ID]")
    print("7. Mark as done:       python script.py mark-done [ID]")
    print("------------------------------\n")

filename = "task_list.json"
data = load_data(filename)

if len(sys.argv) < 2:
    print("Error: No command provided.")
    print_usage()
    sys.exit()

if len(sys.argv) > 1:
    if sys.argv[1] == "add":
        if len(sys.argv) < 3:
            print("Error: Missing task description. Example: python script.py add \"Buy groceries\"")
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
    elif sys.argv[1] == "list":
        tasks_to_show = data["tasks"]
        if len(sys.argv) == 3:
            status_filter = sys.argv[2]
            tasks_to_show = [t for t in data["tasks"] if t["status"] == status_filter]
            if not tasks_to_show:
                print(f"Notice: No tasks found with status '{status_filter}'")

        if tasks_to_show:
            print(f"\n{'ID':<5} {'Description':<25} {'Status':<15} {'Created At':<20} {'Updated At':<20}")
            print("-" * 100)
            for task in tasks_to_show:
                print(f"{task['id']:<5} {task['description']:<25} {task['status']:<15} {task['createdAt']:<20} {task['updatedAt']:<20}")
        else:
            print("Your task list is currently empty.")
    elif sys.argv[1] == "update":
        if len(sys.argv) < 4:
            print("Error: Missing ID or new description. Example: python script.py update 1 \"Updated task\"")
        else:
            task_id = sys.argv[2]
            found = False
            for task in data["tasks"]:
                if str(task["id"]) == task_id:
                    task["description"] = sys.argv[3]
                    task["updatedAt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    save_data(filename, data)
                    print(f"Task updated successfully (ID: {task["id"]})")
                    found = True
                    break
            if not found: print(f"Error: Task with ID {task_id} not found.")
    elif sys.argv[1] == "delete":
        if len(sys.argv) < 3:
            print("Error: Missing ID. Example: python script.py delete 1")
        else:
            task_id = sys.argv[2]
            original_length = len(data["tasks"])
            data["tasks"] = [t for t in data["tasks"] if str(t["id"]) != task_id]
            if len(data["tasks"]) < original_length:
                save_data(filename, data)
                print(f"Success: Task {task_id} deleted.")
            else:
                print(f"Error: Task with ID {task_id} not found.")
    elif sys.argv[1] in ["mark-in-progress", "mark-done"]:
        if len(sys.argv) < 3:
            print(f"Error: Missing ID. Example: python script.py {sys.argv} 1")
        else:
            task_id = sys.argv[2]
            new_status = "in-progress" if sys.argv[1] == "mark-in-progress" else "done"
            found = False
            for task in data["tasks"]:
                if str(task["id"]) == task_id:
                    task["status"] = new_status
                    task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    save_data(filename, data)
                    print(f"Success: Task {task_id} is now {new_status}.")
                    found = True
                    break
            if not found: print(f"Error: Task with ID {task_id} not found.")


