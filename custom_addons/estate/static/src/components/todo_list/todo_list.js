/** @odoo-module **/
import { Component, useState, markup } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Counter } from "../counter/counter";
import { DashboardCard } from "../dashboard_card/dashboard_card";
import { TodoItem } from "../todo_item/todo_item";
import { useAutofocus } from "../../utils";
import { useService } from "@web/core/utils/hooks";

export class TodoList extends Component {
    static template = "estate.TodoList";
    static components = { Counter, DashboardCard, TodoItem };

    setup() {
        useAutofocus("todoInput");

        this.state = useState({
            sum: 2,
            todos: [],
        });

        this.nextId = 1;
        this.htmlContent = markup("<span class='text-primary'>HTML from markup</span>");

        // ✅ Use service safely
        this.todoService = useService("todo_service");

        // ✅ Bind methods so child components can call them
        this.toggleTodo = this.toggleTodo.bind(this);
        this.removeTodo = this.removeTodo.bind(this);
    }

    incrementSum() {
        this.state.sum++;
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value.trim() !== "") {
            this.state.todos.push({
                id: this.nextId++,
                description: ev.target.value,
                isCompleted: false,
            });
            ev.target.value = "";
        }
    }

    toggleTodo(todoId) {
        // Optional: call service if it exists
        if (this.todoService?.toggleTodo) {
            this.todoService.toggleTodo(todoId);
        }

        const todo = this.state.todos.find((t) => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(todoId) {
        const index = this.state.todos.findIndex((t) => t.id === todoId);
        if (index >= 0) {
            this.state.todos.splice(index, 1);
        }
    }

    remainingTodos() {
        return this.state.todos.filter((t) => !t.isCompleted).length;
    }
}

// ✅ Register component
registry.category("view_widgets").add("public_todo_list", { component: TodoList });
