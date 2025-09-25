import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "TomlSelectorUltra",

    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name === "TomlSelectorUltra") {
            // Store original methods
            const origOnNodeCreated = nodeType.prototype.onNodeCreated;
            const origOnConfigure = nodeType.prototype.onConfigure;

            // Override onNodeCreated for initial setup
            nodeType.prototype.onNodeCreated = function() {
                origOnNodeCreated?.apply(this, arguments);

                // Store node reference for API callbacks
                this.tomlData = {};

                // Method to dynamically update outputs based on TOML section
                this.updateDynamicOutputs = async function(sectionName) {
                    try {
                        // Fetch section data from backend
                        const response = await fetch("/api/toml/get_section", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({
                                node_id: this.id,
                                section: sectionName
                            })
                        });

                        if (!response.ok) return;

                        const result = await response.json();
                        if (!result.success) return;

                        const keys = result.keys || [];
                        const values = result.values || [];

                        // Store data
                        this.tomlData = result.data || {};

                        // Clear existing outputs (except first few we want to keep)
                        while (this.outputs && this.outputs.length > 0) {
                            this.removeOutput(this.outputs.length - 1);
                        }

                        // Add outputs based on TOML keys
                        for (let i = 0; i < keys.length && i < 16; i++) {
                            const key = keys[i];
                            const value = values[i];

                            // Determine type based on value
                            let outputType = "STRING";
                            if (typeof value === "number") {
                                outputType = Number.isInteger(value) ? "INT" : "FLOAT";
                            } else if (typeof value === "boolean") {
                                outputType = "BOOLEAN";
                            }

                            // Add output with key name
                            this.addOutput(key, outputType);
                        }

                        // Update node size to fit new outputs
                        this.size = this.computeSize();

                        // Force redraw
                        this.setDirtyCanvas(true, true);
                        app.graph.setDirtyCanvas(true, true);

                    } catch (error) {
                        console.error("Error updating dynamic outputs:", error);
                    }
                };

                // Find section widget and add callback
                const sectionWidget = this.widgets?.find(w => w.name === "section");
                if (sectionWidget) {
                    const origCallback = sectionWidget.callback;

                    sectionWidget.callback = async (value) => {
                        // Call original callback
                        origCallback?.apply(this, arguments);

                        // Update outputs based on new section
                        await this.updateDynamicOutputs(value);
                    };

                    // Initial load
                    setTimeout(() => {
                        this.updateDynamicOutputs(sectionWidget.value);
                    }, 100);
                }
            };

            // Override onConfigure for loading from saved workflow
            nodeType.prototype.onConfigure = function(config) {
                origOnConfigure?.apply(this, arguments);

                // When loading a saved workflow, restore outputs
                const sectionWidget = this.widgets?.find(w => w.name === "section");
                if (sectionWidget && sectionWidget.value) {
                    setTimeout(() => {
                        this.updateDynamicOutputs(sectionWidget.value);
                    }, 200);
                }
            };

            // Override onSerialize to save output configuration
            const origOnSerialize = nodeType.prototype.onSerialize;
            nodeType.prototype.onSerialize = function(data) {
                if (origOnSerialize) {
                    origOnSerialize.apply(this, arguments);
                }

                // Save current TOML data
                data.tomlData = this.tomlData;
                data.outputConfig = this.outputs?.map(o => ({
                    name: o.name,
                    type: o.type
                }));
            };
        }
    },

    // Setup message listener for backend updates
    async setup() {
        // Listen for TOML updates from backend
        app.api.addEventListener("toml.selector.update", (event) => {
            const data = event.detail;
            const node = app.graph.getNodeById(data.node_id);

            if (node && node.updateDynamicOutputs) {
                // Node will update itself based on the event
                console.log("TOML update received for node", data.node_id);
            }
        });
    },

    // Handle node creation
    async nodeCreated(node) {
        if (node.comfyClass === "TomlSelectorUltra") {
            // Add context menu for reload
            const origGetExtraMenuOptions = node.getExtraMenuOptions;
            node.getExtraMenuOptions = function(_, options) {
                origGetExtraMenuOptions?.apply(this, arguments);

                options.push({
                    content: "🔄 Reload TOML Config",
                    callback: async () => {
                        try {
                            const response = await fetch("/api/toml/reload", {
                                method: "POST",
                                headers: { "Content-Type": "application/json" }
                            });

                            if (response.ok) {
                                const sectionWidget = this.widgets?.find(w => w.name === "section");
                                if (sectionWidget) {
                                    await this.updateDynamicOutputs(sectionWidget.value);
                                }
                                console.log("TOML configuration reloaded");
                            }
                        } catch (error) {
                            console.error("Error reloading config:", error);
                        }
                    }
                });

                options.push({
                    content: "📋 Show Current Values",
                    callback: () => {
                        console.log("Current TOML Data:", this.tomlData);
                        const message = Object.entries(this.tomlData)
                            .map(([k, v]) => `${k}: ${v}`)
                            .join("\n");
                        alert(`Current section values:\n\n${message}`);
                    }
                });
            };
        }
    }
});