import streamlit as st

class ToDoList:
    def __init__(self):
        if 'tasks' not in st.session_state:
            st.session_state.tasks = []

    def add_task(self, task):
        st.session_state.tasks.append(task)

    def delete_task(self, task_number):
        try:
            del st.session_state.tasks[task_number]
        except IndexError:
            st.error("Invalid task number.")

    def mark_complete(self, task_number):
        try:
            task = st.session_state.tasks[task_number]
            if "(completed)" not in task:
                st.session_state.tasks[task_number] = f"{task} (completed)"
        except IndexError:
            st.error("Invalid task number.")

    def get_tasks(self):
        return st.session_state.tasks

# Main Streamlit App
st.title("📝 To-Do List App")

todo = ToDoList()

# Add task
new_task = st.text_input("Enter a new task:")
if st.button("Add Task"):
    if new_task.strip() != "":
        todo.add_task(new_task)
    else:
        st.warning("Task cannot be empty.")

# Display tasks
st.subheader("Your Tasks:")
tasks = todo.get_tasks()
if tasks:
    for i, task in enumerate(tasks):
        col1, col2, col3 = st.columns([6, 1, 1])
        col1.write(f"{i+1}. {task}")
        if col2.button("✅", key=f"complete_{i}"):
            todo.mark_complete(i)
        if col3.button("❌", key=f"delete_{i}"):
            todo.delete_task(i)
else:
    st.info("No tasks yet. Add one above!")

