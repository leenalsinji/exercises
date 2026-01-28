/** @odoo-module **/
import { Component } from "@odoo/owl";

export class DashboardCard extends Component {
    static template = "estate.DashboardCard";
    static props = {
        title: String,
        value: { type: [Number, String], optional: true },
    };
}