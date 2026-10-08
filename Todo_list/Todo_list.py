# class Todolist:
#     def __init__(self):
#         self.tasks=[]
#     def add_task(self,*task_names):
#         for task in task_names:
#             self.tasks.append({
#                 "task":task,
#                 "completed": False
#             })
#         print("Task added successfully.... ")
#     def view_tasks(self):
#         if not self.tasks:
#             print("No task available")
#         else:
#             print("-------------TODO LIST----------------")
#             i=1
#             for task in self.tasks:
#                 if task['completed']== True:
#                     status ="completed"
#                 else:
#                     status="pending"    
#                 print(f"{i}.{task['task']}-{status}")
#                 i=i+1
#     def complete_task(self):
#         self.view_tasks()
#         if self.tasks:
#             try:
#                 task_number=int(input("Enter task number to complete: "))
#                 if 1<=task_number<=len(self.tasks):
#                     self.tasks[task_number-1]["completed"]=True
#                     print("mark task as completed!")
#                 else:
#                     print("Invalid task number!")
#             except ValueError:
#                 print("please enter valid number")
#     def update_task(self):
#             self.view_tasks()
#             if self.tasks:
#                 try:
#                     task_number=int(input("Enter task number to update: "))
#                     if 1<=task_number<=len(self.tasks):
#                         new_task=input("Enter new task name: ")
#                         self.tasks[task_number-1]["task"]=new_task
#                         print("Task updated successfully...")
#                     else:
#                         print("Invalid task number!")
#                 except ValueError:
#                     print("please enter valid number") 
#     def remove_task(self):
#                 self.view_tasks()
#                 if self.tasks:
#                     try:
#                         task_number=int(input("Enter task number to remove: "))
#                         if 1<=task_number<=len(self.tasks):
#                             removed_task=self.tasks.pop(task_number-1)
#                             print(f"{removed_task["task"]} removed successfully.....")
#                         else:
#                             print("Invalid task number!")
#                     except ValueError:
#                         print("please enter valid number")
# todo=Todolist()
# todo.add_task("breakfast","studytime","lunch","snacks","dinner")
# while True:
#     print("\n**********TODO LIST**********")
#     print("1.View task")   
#     print("2.Complete task")  
#     print("3.Update task")  
#     print("4.Remove task")  
#     print("5.Exit task")

#     option=input("Enter your choice: ")  

#     if option=="1":
#         todo.view_tasks()
#     elif option=="2":
#         todo.complete_task() 
#     elif option=="3":
#             todo.update_task()    
#     elif option=="4":
#             todo.remove_task()
#     elif option=="5":
#             print("Thanks for choosing TODO LIST")
#             break
#     else:
#          print("Please enter valid option")        
                               






import csv
import os
import tkinter as tk
from tkinter import messagebox, ttk


# ============================================================
# TODO LIST BACKEND
# ============================================================

class TodoList:
    def __init__(self):
        # Store all tasks
        self.tasks = []

        # CSV file name
        self.filename = "tasks.csv"

        # Load existing tasks
        self.load_tasks()

    # --------------------------------------------------------
    # Load tasks from CSV
    # --------------------------------------------------------
    def load_tasks(self):
        """Load tasks from the CSV file."""

        # If the file does not exist, create it
        if not os.path.exists(self.filename):
            with open(
                self.filename,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                # Create CSV headings
                writer.writerow(["Task", "Status"])

            return

        # Read tasks from the CSV file
        try:
            with open(
                self.filename,
                "r",
                newline="",
                encoding="utf-8"
            ) as file:

                reader = csv.DictReader(file)

                for row in reader:

                    # Make sure the required columns exist
                    if "Task" in row and "Status" in row:
                        self.tasks.append({
                            "task": row["Task"],
                            "completed": row["Status"] == "Completed"
                        })

        except Exception as error:
            print("Error loading tasks:", error)

    # --------------------------------------------------------
    # Save tasks to CSV
    # --------------------------------------------------------
    def save_tasks(self):
        """Save all tasks to the CSV file."""

        try:
            with open(
                self.filename,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                # Write headings
                writer.writerow(["Task", "Status"])

                # Write each task
                for task in self.tasks:

                    status = (
                        "Completed"
                        if task["completed"]
                        else "Not Completed"
                    )

                    writer.writerow([
                        task["task"],
                        status
                    ])

        except Exception as error:
            print("Error saving tasks:", error)

    # --------------------------------------------------------
    # Add a task
    # --------------------------------------------------------
    def add_task(self, task):
        """Add a new task."""

        self.tasks.append({
            "task": task,
            "completed": False
        })

        # Save changes
        self.save_tasks()

    # --------------------------------------------------------
    # Remove a task
    # --------------------------------------------------------
    def remove_task(self, index):
        """Remove a task using its index."""

        if 0 <= index < len(self.tasks):

            del self.tasks[index]

            # Save changes
            self.save_tasks()

            return True

        return False

    # --------------------------------------------------------
    # Mark task as completed
    # --------------------------------------------------------
    def mark_completed(self, index):
        """Mark a task as completed."""

        if 0 <= index < len(self.tasks):

            self.tasks[index]["completed"] = True

            # Save changes
            self.save_tasks()

            return True

        return False


# ============================================================
# TODO LIST GUI
# ============================================================

class TodoApp:
    def __init__(self, root):

        # Main window
        self.root = root

        self.root.title("📝 To-Do List Manager")

        # IMPORTANT:
        # No spaces should be used in geometry values.
        self.root.geometry("500x450")

        # Minimum window size
        self.root.minsize(400, 350)

        # Create backend object
        self.todo_list = TodoList()

        # Create GUI
        self.create_widgets()

        # Display existing tasks
        self.refresh_task_list()

    # ========================================================
    # CREATE GUI
    # ========================================================

    def create_widgets(self):

        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        title_label = ttk.Label(
            self.root,
            text="📝 To-Do List Manager",
            font=("Arial", 20, "bold")
        )

        title_label.pack(
            pady=(15, 5)
        )

        subtitle_label = ttk.Label(
            self.root,
            text="Manage your daily tasks easily"
        )

        subtitle_label.pack(
            pady=(0, 10)
        )

        # ----------------------------------------------------
        # Input Frame
        # ----------------------------------------------------

        input_frame = ttk.Frame(
            self.root,
            padding="10"
        )

        input_frame.pack(
            fill=tk.X
        )

        # Task entry box
        self.task_entry = ttk.Entry(
            input_frame,
            font=("Arial", 11)
        )

        self.task_entry.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True,
            padx=(0, 5)
        )

        # Press Enter to add task
        self.task_entry.bind(
            "<Return>",
            lambda event: self.add_task()
        )

        # Add button
        add_btn = ttk.Button(
            input_frame,
            text="➕ Add Task",
            command=self.add_task
        )

        add_btn.pack(
            side=tk.RIGHT
        )

        # ----------------------------------------------------
        # Task List Frame
        # ----------------------------------------------------

        list_frame = ttk.Frame(
            self.root,
            padding="10"
        )

        list_frame.pack(
            fill=tk.BOTH,
            expand=True
        )

        # Listbox
        self.task_listbox = tk.Listbox(
            list_frame,
            selectmode=tk.SINGLE,
            font=("Arial", 11),
            activestyle="none",
            height=12
        )

        self.task_listbox.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            list_frame,
            orient=tk.VERTICAL,
            command=self.task_listbox.yview
        )

        scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        # Connect scrollbar to Listbox
        self.task_listbox.config(
            yscrollcommand=scrollbar.set
        )

        # ----------------------------------------------------
        # Action Buttons
        # ----------------------------------------------------

        button_frame = ttk.Frame(
            self.root,
            padding="10"
        )

        button_frame.pack(
            fill=tk.X
        )

        # Complete button
        complete_btn = ttk.Button(
            button_frame,
            text="✅ Mark Completed",
            command=self.mark_completed
        )

        complete_btn.pack(
            side=tk.LEFT,
            padx=(0, 5)
        )

        # Delete button
        delete_btn = ttk.Button(
            button_frame,
            text="🗑️ Remove Task",
            command=self.remove_task
        )

        delete_btn.pack(
            side=tk.LEFT,
            padx=5
        )

        # Exit button
        exit_btn = ttk.Button(
            button_frame,
            text="❌ Exit",
            command=self.exit_application
        )

        exit_btn.pack(
            side=tk.RIGHT
        )

    # ========================================================
    # REFRESH TASK LIST
    # ========================================================

    def refresh_task_list(self):
        """Refresh the Listbox with current tasks."""

        # Remove old items
        self.task_listbox.delete(
            0,
            tk.END
        )

        # Add current tasks
        for index, task in enumerate(
            self.todo_list.tasks,
            start=1
        ):

            # Check task status
            if task["completed"]:

                status_symbol = "✓"
                status_text = "Completed"

            else:

                status_symbol = "○"
                status_text = "Pending"

            # Text displayed in Listbox
            display_text = (
                f"{index}. "
                f"[{status_symbol}] "
                f"{task['task']} "
                f"— ({status_text})"
            )

            # Insert task
            self.task_listbox.insert(
                tk.END,
                display_text
            )

            # Highlight completed tasks
            if task["completed"]:

                listbox_index = (
                    self.task_listbox.size() - 1
                )

                self.task_listbox.itemconfig(
                    listbox_index,
                    foreground="gray"
                )

    # ========================================================
    # ADD TASK
    # ========================================================

    def add_task(self):
        """Add a new task."""

        # Get text from entry box
        task_text = self.task_entry.get().strip()

        # Validate task
        if not task_text:

            messagebox.showwarning(
                "Warning",
                "Task description cannot be empty!"
            )

            return

        # Add task to backend
        self.todo_list.add_task(task_text)

        # Clear entry box
        self.task_entry.delete(
            0,
            tk.END
        )

        # Refresh Listbox
        self.refresh_task_list()

        # Show success message
        messagebox.showinfo(
            "Success",
            "Task added successfully! ✅"
        )

        # Put cursor back in entry box
        self.task_entry.focus()

    # ========================================================
    # GET SELECTED TASK
    # ========================================================

    def get_selected_index(self):
        """Return the index of the selected task."""

        selected_indices = (
            self.task_listbox.curselection()
        )

        # Check if nothing is selected
        if not selected_indices:

            messagebox.showwarning(
                "Warning",
                "Please select a task from the list first."
            )

            return None

        # Return selected index
        return selected_indices[0]

    # ========================================================
    # MARK COMPLETED
    # ========================================================

    def mark_completed(self):
        """Mark the selected task as completed."""

        # Get selected task index
        index = self.get_selected_index()

        # Stop if no task is selected
        if index is None:
            return

        # Check if already completed
        if self.todo_list.tasks[index]["completed"]:

            messagebox.showinfo(
                "Already Completed",
                "This task is already completed! ✅"
            )

            return

        # Get task name before changing it
        task_name = self.todo_list.tasks[index]["task"]

        # Mark task as completed
        self.todo_list.mark_completed(index)

        # Refresh Listbox
        self.refresh_task_list()

        # Show success message
        messagebox.showinfo(
            "Task Completed",
            f"Task completed successfully!\n\n"
            f"✓ {task_name}"
        )

    # ========================================================
    # REMOVE TASK
    # ========================================================

    def remove_task(self):
        """Remove the selected task."""

        # Get selected task index
        index = self.get_selected_index()

        # Stop if no task is selected
        if index is None:
            return

        # Get task name
        task_name = self.todo_list.tasks[index]["task"]

        # Ask user for confirmation
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete this task?\n\n"
            f"📝 {task_name}"
        )

        # Delete only if user clicks Yes
        if confirm:

            self.todo_list.remove_task(index)

            # Refresh Listbox
            self.refresh_task_list()

            # Show success message
            messagebox.showinfo(
                "Task Deleted",
                "Task deleted successfully! 🗑️"
            )

    # ========================================================
    # EXIT APPLICATION
    # ========================================================

    def exit_application(self):
        """Close the application."""

        confirm = messagebox.askyesno(
            "Exit",
            "Are you sure you want to exit?"
        )

        if confirm:
            self.root.destroy()


# ============================================================
# MAIN FUNCTION
# ============================================================

def main():

    # Create Tkinter window
    root = tk.Tk()

    # Create application
    app = TodoApp(root)

    # Start Tkinter event loop
    root.mainloop()


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()

