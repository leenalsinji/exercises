/** @odoo-module **/
import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const todoService = {
    // List any dependencies your service needs (like 'rpc' or 'orm')
    dependencies: [], 
    start(env) {
        // Create a reactive object to hold your data and functions
        const state = reactive({
            todos: [],
            addTodo(description) {
                const id = Math.max(0, ...state.todos.map(t => t.id)) + 1;
                state.todos.push({ id, description, isCompleted: false });
            },
            toggleTodo(id) {
                const todo = state.todos.find(t => t.id === id);
                if (todo) {
                    todo.isCompleted = !todo.isCompleted;
                }
            },
        });
        
        // CRITICAL: You must return the state so components can use it
        return state; 
    },
};

// Register the service so Odoo's web client loads it
registry.category("services").add("todo_service", todoService);