/** @odoo-module **/

import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc"; // Import rpc directly

export const statisticsService = {
    // Remove "rpc" from dependencies and use the direct import instead
    dependencies: [], 
    start(env) {
        const statistics = reactive({
            isLoaded: false,
            activeCount: 0,
            expectedRevenue: 0,
        });

        async function loadStatistics() {
            // Use the imported rpc function directly
            const [activeCount, revenueData] = await Promise.all([
                rpc("/web/dataset/call_kw/estate.property/search_count", {
                    model: "estate.property",
                    method: "search_count",
                    args: [[["state", "not in", ["cancelled", "sold"]]]],
                    kwargs: {},
                }),
                rpc("/web/dataset/call_kw/estate.property/read_group", {
                    model: "estate.property",
                    method: "read_group",
                    args: [],
                    kwargs: {
                        domain: [["state", "not in", ["cancelled", "sold"]]],
                        fields: ["expected_price"],
                        groupby: [],
                    },
                }),
            ]);

            statistics.activeCount = activeCount;
            statistics.expectedRevenue = revenueData[0]?.expected_price || 0;
            statistics.isLoaded = true;
        }

        return { statistics, loadStatistics };
    },
};

registry.category("services").add("estate.statistics", statisticsService);