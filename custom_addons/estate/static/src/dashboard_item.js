/** @odoo-module **/

import { Component } from "@odoo/owl";
import { estateDashboardRegistry } from "./dashboard_registry";

// 1. Define the Component first
export class DashboardItem extends Component {
    static template = "estate.DashboardItem";
    static props = {
        size: { type: Number, optional: true },
        slots: { type: Object, optional: true },
    };
    static defaultProps = {
        size: 1,
    };
}

// 2. Register the items OUTSIDE the class
estateDashboardRegistry.add("active_properties", {
    description: "Active Properties",
    size: 1,
    props: (stats) => ({
        title: "Active Properties",
        value: stats.activeCount,
        color: "text-primary",
    }),
});

estateDashboardRegistry.add("expected_revenue", {
    description: "Expected Revenue",
    size: 2,
    props: (stats) => ({
        title: "Expected Revenue",
        value: `$${stats.expectedRevenue.toLocaleString()}`,
        color: "text-success",
    }),
});

