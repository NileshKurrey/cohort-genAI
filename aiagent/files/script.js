document.addEventListener('DOMContentLoaded', function() {
    const todoInput = document.getElementById('todoInput');
    const addTodoBtn = document.getElementById('addTodoBtn');
    const todoList = document.getElementById('todoList');
    const filter = document.getElementById('filter');

    let todos = [];

    // Function to render todos
    function renderTodos(filterValue = 'all') {
        todoList.innerHTML = '';
        let filteredTodos = [...todos]; // Create a copy to avoid modifying the original array

        if (filterValue === 'completed') {
            filteredTodos = filteredTodos.filter(todo => todo.completed);
        } else if (filterValue === 'incomplete') {
            filteredTodos = filteredTodos.filter(todo => !todo.completed);
        }

        filteredTodos.forEach((todo, index) => {
            const li = document.createElement('li');
            li.innerHTML = `
                <span class="${todo.completed ? 'completed' : ''}">${todo.text}</span>
                <div class="actions">
                    <button class="completeBtn" data-index="${index}">${todo.completed ? 'Undo' : 'Complete'}</button>
                    <button class="deleteBtn" data-index="${index}">Delete</button>
                </div>
            `;
            todoList.appendChild(li);
        });
    }

    // Function to add a todo
    function addTodo() {
        const todoText = todoInput.value.trim();
        if (todoText !== '') {
            todos.push({
                text: todoText,
                completed: false
            });
            todoInput.value = '';
            renderTodos(filter.value);
        }
    }

    // Function to toggle complete
    function toggleComplete(index) {
        todos[index].completed = !todos[index].completed;
        renderTodos(filter.value);
    }

    // Function to delete a todo
    function deleteTodo(index) {
        todos.splice(index, 1);
        renderTodos(filter.value);
    }

    // Event listeners
    addTodoBtn.addEventListener('click', addTodo);

    todoInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            addTodo();
        }
    });

    todoList.addEventListener('click', function(event) {
        if (event.target.classList.contains('completeBtn')) {
            const index = event.target.dataset.index;
            toggleComplete(index);
        }
        if (event.target.classList.contains('deleteBtn')) {
            const index = event.target.dataset.index;
            deleteTodo(index);
        }
    });

    filter.addEventListener('change', function() {
        renderTodos(this.value);
    });

    // Initial render
    renderTodos();
});