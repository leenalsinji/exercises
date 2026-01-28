/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import { estateDashboardRegistry } from "./dashboard_registry";

export class EstateDashboard extends Component {
    static template = "estate.EstateDashboard";
    static components = { Layout, DashboardItem }; // Chart removed

    setup() {
        this.action = useService("action");
        this.statsService = useService("estate.statistics");
        this.stats = useState(this.statsService.statistics);
        this.items = estateDashboardRegistry.getAll();

        onWillStart(async () => {
            await this.statsService.loadStatistics();
        });

        this.display = { controlPanel: {} };
    }

    async refreshStatistics() {
        await this.statsService.loadStatistics(); 
    }

    openProperties() {
        this.action.doAction("estate.estate_property_action");
    }

    openOffers() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Property Offers",
            res_model: "estate.property.offer",
            views: [[false, "list"], [false, "form"]],
        });
    }
}

// Only ONE registration here
registry.category("actions").add("estate.dashboard", EstateDashboard);