import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "TomlSelectorDynamic",

    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name === "TomlSelectorDynamic" || nodeData.name === "TomlSelectorAdvanced") {
            const origOnConnectionsChange = nodeType.prototype.onConnectionsChange;

            // Store original onNodeCreated if it exists
            const origOnNodeCreated = nodeType.prototype.onNodeCreated;

            // Override onNodeCreated to set up the node when it's created
            nodeType.prototype.onNodeCreated = function() {
                // Call original if exists
                origOnNodeCreated?.apply(this, arguments);

                // Add method to update outputs dynamically
                this.updateOutputs = function(sectionData) {
                    if (!sectionData) return;

                    const keys = Object.keys(sectionData);
                    const currentOutputCount = this.outputs ? this.outputs.length : 0;
                    const neededOutputCount = Math.min(keys.length + 1, 11); // +1 for json_data, max 11

                    // Remove excess outputs
                    while (this.outputs && this.outputs.length > neededOutputCount) {
                        this.removeOutput(this.outputs.length - 1);
                    }

                    // Add/update outputs as needed
                    if (!this.outputs || this.outputs.length === 0) {
                        // First output is always JSON data
                        this.addOutput("json_data", "STRING");
                    }

                    // Add outputs for each key
                    for (let i = 0; i < keys.length && i < 10; i++) {
                        const outputName = keys[i];
                        const outputIndex = i + 1; // +1 because json_data is at index 0

                        if (this.outputs.length <= outputIndex) {
                            // Add new output
                            this.addOutput(outputName, "STRING");
                        } else {
                            // Update existing output name
                            this.outputs[outputIndex].name = outputName;
                        }
                    }

                    // Force graph to update
                    this.setDirtyCanvas(true, true);
                };

                // Override widget callback for section dropdown
                const sectionWidget = this.widgets?.find(w => w.name === "section");
                if (sectionWidget) {
                    const originalCallback = sectionWidget.callback;

                    sectionWidget.callback = async () => {
                        // Call original callback if exists
                        originalCallback?.apply(this, arguments);

                        // Fetch current config data
                        try {
                            const response = await fetch("/api/get_toml_section", {
                                method: "POST",
                                headers: { "Content-Type": "application/json" },
                                body: JSON.stringify({
                                    node_id: this.id,
                                    section: sectionWidget.value
                                })
                            });

                            if (response.ok) {
                                const data = await response.json();
                                if (data.success && data.section_data) {
                                    this.updateOutputs(data.section_data);
                                }
                            }
                        } catch (error) {
                            console.error("Error fetching section data:", error);
                        }
                    };

                    // Trigger initial update
                    sectionWidget.callback();
                }
            };

            // Handle connections changes
            nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info, io_slot) {
                // Call original handler
                origOnConnectionsChange?.apply(this, arguments);

                // Additional logic if needed
                if (type === 1) { // Output connection
                    // Could add logic here if needed
                }

                return true;
            };
        }
    },

    async nodeCreated(node) {
        // Additional per-instance setup if needed
        if (node.comfyClass === "TomlSelectorDynamic" || node.comfyClass === "TomlSelectorAdvanced") {
            // Per-instance customization can go here
        }
    }
});