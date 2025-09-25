"""
Fixed TOML Selector Node with Dynamic Names
"""

import os
import toml
import json
from typing import Dict, List, Tuple, Any, Optional

class TomlSelectorFixed:
    """
    Fixed version with proper output names and types
    """

    def __init__(self):
        self.config_data = {}
        self.section_keys = {}
        self.load_config()

    def load_config(self):
        """Load configuration from TOML file"""
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")

        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config_data = toml.load(f)
                    # Store keys for each section
                    for section, data in self.config_data.items():
                        self.section_keys[section] = list(data.keys())
            except Exception as e:
                print(f"Error loading config.toml: {e}")

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
                    # Store section info for display
                    for section, data in config.items():
                        section_info[section] = {
                            "keys": list(data.keys()),
                            "types": [type(v).__name__ for v in data.values()]
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
                "show_info": ("BOOLEAN", {"default": True, "label": "Show Info"}),
            }
        }

    # Return generic types that can hold any value
    RETURN_TYPES = ("JSON", "ANY", "ANY", "ANY", "ANY", "ANY",
                    "ANY", "ANY", "ANY", "ANY", "ANY")

    # Dynamic names based on loaded config
    @classmethod
    def RETURN_NAMES(cls):
        """Generate return names dynamically"""
        # Load config to get first section keys
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")

        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = toml.load(f)
                    if config:
                        # Get first section's keys for default names
                        first_section = list(config.values())[0]
                        keys = list(first_section.keys())

                        names = ["json_data"]
                        for i in range(10):
                            if i < len(keys):
                                names.append(keys[i])
                            else:
                                names.append(f"output_{i+1}")
                        return tuple(names)
            except:
                pass

        return ("json_data", "output_1", "output_2", "output_3", "output_4",
                "output_5", "output_6", "output_7", "output_8", "output_9", "output_10")

    FUNCTION = "process"
    CATEGORY = "utils/selector/fixed"
    OUTPUT_NODE = True

    def process(self, section: str, show_info: bool = True) -> Tuple:
        """Process with proper type preservation"""

        # Reload config
        self.load_config()

        # Initialize outputs
        json_output = {}
        outputs = [None] * 10

        if section in self.config_data:
            section_data = self.config_data[section]
            json_output = section_data

            if show_info:
                print(f"\n=== Section: {section} ===")

            # Process each key-value pair
            for i, (key, value) in enumerate(section_data.items()):
                if i < 10:
                    # Keep original type
                    outputs[i] = value

                    if show_info:
                        value_type = type(value).__name__
                        print(f"  [{i+1}] {key}: {value} (type: {value_type})")

        # Convert dict to JSON string for first output
        json_str = json.dumps(json_output, indent=2)

        return (json_str, *outputs)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        """Force update when config changes"""
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")
        if os.path.exists(config_path):
            return os.path.getmtime(config_path)
        return 0


class TomlSelectorNamed:
    """
    Version with properly named outputs for each section
    """

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
            }
        }

    # Maximum 10 outputs + JSON
    RETURN_TYPES = ("JSON", "ANY", "ANY", "ANY", "ANY", "ANY",
                    "ANY", "ANY", "ANY", "ANY", "ANY")

    FUNCTION = "process"
    CATEGORY = "utils/selector/named"
    OUTPUT_NODE = True

    @classmethod
    def RETURN_NAMES(cls):
        """Try to use actual key names from config"""
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")

        base_names = ["json_data"]

        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = toml.load(f)

                    # Collect all unique keys from all sections
                    all_keys = []
                    for section_data in config.values():
                        for key in section_data.keys():
                            if key not in all_keys:
                                all_keys.append(key)

                    # Use the first 10 unique keys
                    for i in range(10):
                        if i < len(all_keys):
                            base_names.append(all_keys[i])
                        else:
                            base_names.append(f"unused_{i+1}")

                    return tuple(base_names)
            except:
                pass

        # Fallback names
        for i in range(10):
            base_names.append(f"value_{i+1}")

        return tuple(base_names)

    def process(self, section: str) -> Tuple:
        """Process and return values with proper types"""

        config_path = os.path.join(os.path.dirname(__file__), "config.toml")

        # Load config
        config_data = {}
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = toml.load(f)
            except Exception as e:
                print(f"Error loading config.toml: {e}")

        # Initialize outputs
        json_output = {}
        outputs = [None] * 10

        if section in config_data:
            section_data = config_data[section]
            json_output = section_data

            print(f"\n=== Loading section: {section} ===")

            # Fill outputs preserving types
            for i, (key, value) in enumerate(section_data.items()):
                if i < 10:
                    outputs[i] = value
                    print(f"  Output {i+1} ({key}): {value} [{type(value).__name__}]")

        # JSON string for first output
        json_str = json.dumps(json_output, indent=2)

        return (json_str, *outputs)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        """Force update when config changes"""
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")
        if os.path.exists(config_path):
            return os.path.getmtime(config_path)
        return 0


# Node registration
NODE_CLASS_MAPPINGS_FIXED = {
    "TomlSelectorFixed": TomlSelectorFixed,
    "TomlSelectorNamed": TomlSelectorNamed,
}

NODE_DISPLAY_NAME_MAPPINGS_FIXED = {
    "TomlSelectorFixed": "TOML Selector (Fixed Types)",
    "TomlSelectorNamed": "TOML Selector (Named Outputs)",
}