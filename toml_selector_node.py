"""
Dynamic TOML Selector Node for ComfyUI
"""

import os
import toml
import json
from typing import Dict, List, Tuple, Any, Optional
from server import PromptServer
from aiohttp import web

class TomlSelectorNode:
    """
    A dynamic node that reads configuration from a TOML file and provides
    selectable outputs based on the sections defined in the file.
    """

    def __init__(self):
        self.config_data = {}
        self.load_config()

    @classmethod
    def INPUT_TYPES(cls):
        # Load config at class level to populate dropdown
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")
        sections = []

        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = toml.load(f)
                    sections = list(config.keys())
            except Exception as e:
                print(f"Error loading config.toml: {e}")
                sections = ["default"]

        if not sections:
            sections = ["default"]

        return {
            "required": {
                "section": (sections, {"default": sections[0] if sections else "default"}),
            }
        }

    # Define maximum possible outputs (we'll use None for unused ones)
    MAX_OUTPUTS = 10

    RETURN_TYPES = tuple(["STRING" for _ in range(MAX_OUTPUTS)])
    RETURN_NAMES = tuple([f"output_{i+1}" for i in range(MAX_OUTPUTS)])

    FUNCTION = "process"
    CATEGORY = "utils/selector"

    def load_config(self):
        """Load configuration from TOML file"""
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")

        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config_data = toml.load(f)
            except Exception as e:
                print(f"Error loading config.toml: {e}")
                self.config_data = {}
        else:
            print(f"Config file not found at {config_path}")
            self.config_data = {}

    def process(self, section: str) -> Tuple:
        """Process the selected section and return its values"""

        # Reload config to get latest changes
        self.load_config()

        # Initialize all outputs with None
        outputs = [None] * self.MAX_OUTPUTS

        # Get the selected section data
        if section in self.config_data:
            section_data = self.config_data[section]

            # Fill outputs with section values (up to MAX_OUTPUTS)
            for i, (key, value) in enumerate(section_data.items()):
                if i < self.MAX_OUTPUTS:
                    # Convert value to string for consistent output type
                    outputs[i] = str(value)
                else:
                    break

        return tuple(outputs)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        """Force the node to update when config file changes"""
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")
        if os.path.exists(config_path):
            return os.path.getmtime(config_path)
        return 0


class TomlSelectorAdvanced:
    """
    Advanced version that shows keys as output names dynamically
    """

    def __init__(self):
        self.config_data = {}
        self.current_section = None
        self.load_config()

    @classmethod
    def INPUT_TYPES(cls):
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")
        sections = []

        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = toml.load(f)
                    sections = list(config.keys())
            except Exception as e:
                print(f"Error loading config.toml: {e}")
                sections = ["default"]

        if not sections:
            sections = ["default"]

        return {
            "required": {
                "section": (sections, {"default": sections[0] if sections else "default"}),
            },
            "optional": {
                "display_info": ("BOOLEAN", {"default": True, "label": "Show Info"}),
            }
        }

    RETURN_TYPES = ("DICT", "ANY", "ANY", "ANY", "ANY", "ANY",
                    "ANY", "ANY", "ANY", "ANY", "ANY")
    RETURN_NAMES = ("full_data", "value_1", "value_2", "value_3", "value_4",
                    "value_5", "value_6", "value_7", "value_8", "value_9", "value_10")

    FUNCTION = "process"
    CATEGORY = "utils/selector"
    OUTPUT_NODE = True

    def load_config(self):
        """Load configuration from TOML file"""
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")

        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config_data = toml.load(f)
            except Exception as e:
                print(f"Error loading config.toml: {e}")
                self.config_data = {}

    def process(self, section: str, display_info: bool = True) -> Tuple:
        """Process the selected section and return its values"""

        # Reload config
        self.load_config()

        # Initialize outputs
        full_data = {}
        outputs = [None] * 10

        if section in self.config_data:
            section_data = self.config_data[section]
            full_data = section_data

            # Fill individual outputs (preserve original types)
            for i, (key, value) in enumerate(section_data.items()):
                if i < 10:
                    outputs[i] = value  # Keep original type instead of converting to string
                    if display_info:
                        print(f"  {key}: {value}")

        if display_info:
            print(f"Selected section: {section}")
            print(f"Number of outputs: {len([o for o in outputs if o is not None])}")

        return (full_data, *outputs)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        """Force the node to update when config file changes"""
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")
        if os.path.exists(config_path):
            return os.path.getmtime(config_path)
        return 0


class TomlSelectorDynamic:
    """
    Ultra-dynamic version that detects types and provides proper conversions
    """

    @classmethod
    def INPUT_TYPES(cls):
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")
        sections = []
        section_info = {}

        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = toml.load(f)
                    sections = list(config.keys())

                    # Store info about each section
                    for section_name, section_data in config.items():
                        keys = list(section_data.keys())
                        section_info[section_name] = {
                            "keys": keys,
                            "count": len(keys)
                        }
            except Exception as e:
                print(f"Error loading config.toml: {e}")
                sections = ["default"]

        if not sections:
            sections = ["default"]

        return {
            "required": {
                "section": (sections, {"default": sections[0] if sections else "default"}),
            },
            "optional": {
                "reload": ("BOOLEAN", {"default": False, "label": "Reload Config"}),
                "show_keys": ("BOOLEAN", {"default": True, "label": "Display Keys"}),
            }
        }

    RETURN_TYPES = ("JSON", "ANY", "ANY", "ANY", "ANY", "ANY",
                    "ANY", "ANY", "ANY", "ANY", "ANY")
    RETURN_NAMES = ("json_data", "out_1", "out_2", "out_3", "out_4",
                    "out_5", "out_6", "out_7", "out_8", "out_9", "out_10")

    FUNCTION = "process"
    CATEGORY = "utils/selector"
    OUTPUT_NODE = True

    def process(self, section: str, reload: bool = False, show_keys: bool = True) -> Tuple:
        """Process with type detection and proper conversion"""

        config_path = os.path.join(os.path.dirname(__file__), "config.toml")

        # Load configuration
        config_data = {}
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = toml.load(f)
            except Exception as e:
                print(f"Error loading config.toml: {e}")
                return (None,) * 11

        # Initialize outputs
        json_output = {}
        outputs = [None] * 10

        if section in config_data:
            section_data = config_data[section]
            json_output = section_data

            if show_keys:
                print(f"\n=== Section: {section} ===")

            # Process each key-value pair
            for i, (key, value) in enumerate(section_data.items()):
                if i < 10:
                    # Keep original type for ANY outputs
                    outputs[i] = value

                    if show_keys:
                        value_type = type(value).__name__
                        print(f"  [{i+1}] {key}: {value} (type: {value_type})")

        # Convert to JSON string for first output
        json_str = json.dumps(json_output, indent=2)

        return (json_str, *outputs)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        """Force update when config changes"""
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")
        if os.path.exists(config_path):
            return os.path.getmtime(config_path)
        return 0


# API endpoint for fetching section data
@PromptServer.instance.routes.post("/api/get_toml_section")
async def get_toml_section(request):
    """API endpoint to fetch section data from TOML file"""
    try:
        data = await request.json()
        section = data.get("section")

        config_path = os.path.join(os.path.dirname(__file__), "config.toml")

        if not os.path.exists(config_path):
            return web.json_response({"success": False, "error": "Config file not found"})

        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = toml.load(f)

        if section in config_data:
            section_data = config_data[section]
            return web.json_response({
                "success": True,
                "section_data": section_data,
                "keys": list(section_data.keys())
            })
        else:
            return web.json_response({
                "success": False,
                "error": f"Section '{section}' not found"
            })
    except Exception as e:
        return web.json_response({
            "success": False,
            "error": str(e)
        })


# Node registration
NODE_CLASS_MAPPINGS = {
    "TomlSelector": TomlSelectorNode,
    "TomlSelectorAdvanced": TomlSelectorAdvanced,
    "TomlSelectorDynamic": TomlSelectorDynamic,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TomlSelector": "TOML Selector",
    "TomlSelectorAdvanced": "TOML Selector (Advanced)",
    "TomlSelectorDynamic": "TOML Selector (Dynamic)",
}