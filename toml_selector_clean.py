"""
Clean TOML Selector for ComfyUI - Properly Working Version
"""

import os
import toml
import json
from typing import Dict, List, Tuple, Any, Optional

class TomlSelectorClean:
    """
    Clean working version with proper dynamic outputs
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
                "section": (sections, {}),
            }
        }

    # Outputs - first is JSON, then up to 5 values with proper types
    RETURN_TYPES = ("STRING", "INT", "STRING", "STRING", "STRING", "STRING")

    RETURN_NAMES = ("json_data", "output_1", "output_2", "output_3", "output_4", "output_5")

    FUNCTION = "process"
    CATEGORY = "utils/toml"

    def process(self, section: str) -> Tuple:
        """Process the selected section and return only needed outputs"""

        config_path = os.path.join(os.path.dirname(__file__), "config.toml")
        config_data = {}

        # Load config
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = toml.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")

        # Initialize with defaults
        json_output = {}
        outputs = [0, "", "", "", ""]  # Match RETURN_TYPES (minus json)

        if section in config_data:
            section_data = config_data[section]
            json_output = section_data

            print(f"\n=== TOML Section: {section} ===")

            # Process based on section
            if section == "player_1":
                # player_1 has: numero (int), jujuba (string), animal (string)
                outputs[0] = section_data.get("numero", 0)  # INT
                outputs[1] = section_data.get("jujuba", "")  # STRING
                outputs[2] = section_data.get("animal", "")  # STRING
                outputs[3] = ""  # unused
                outputs[4] = ""  # unused

                print(f"  numero: {outputs[0]} (INT)")
                print(f"  jujuba: {outputs[1]} (STRING)")
                print(f"  animal: {outputs[2]} (STRING)")

            elif section == "donald":
                # donald has: leao (string), software (string)
                outputs[0] = 0  # unused INT
                outputs[1] = section_data.get("leao", "")  # STRING
                outputs[2] = section_data.get("software", "")  # STRING
                outputs[3] = ""  # unused
                outputs[4] = ""  # unused

                print(f"  leao: {outputs[1]} (STRING)")
                print(f"  software: {outputs[2]} (STRING)")

            else:
                # Generic handling
                values = list(section_data.values())
                for i in range(min(5, len(values))):
                    if i == 0:  # First output is INT
                        outputs[i] = int(values[i]) if isinstance(values[i], (int, float)) else 0
                    else:  # Rest are STRING
                        outputs[i] = str(values[i])

        # Convert to JSON
        json_str = json.dumps(json_output, indent=2)

        return (json_str, *outputs)

    @classmethod
    def IS_CHANGED(cls, section):
        """Check if config file changed"""
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")
        if os.path.exists(config_path):
            return f"{os.path.getmtime(config_path)}_{section}"
        return "0"


class TomlSelectorProper:
    """
    Proper version with only the outputs that are actually needed
    """

    @classmethod
    def INPUT_TYPES(cls):
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")
        sections = []
        max_keys = 0

        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = toml.load(f)
                    sections = list(config.keys())
                    # Find max number of keys
                    for section_data in config.values():
                        max_keys = max(max_keys, len(section_data))
            except Exception as e:
                print(f"Error: {e}")
                sections = ["default"]

        if not sections:
            sections = ["default"]

        # Store for later use
        cls._max_keys = min(max_keys, 10)  # Limit to 10 outputs

        return {
            "required": {
                "section": (sections, {}),
            }
        }

    # Build RETURN_TYPES dynamically based on config
    @classmethod
    def get_return_types(cls):
        types = ["STRING"]  # json_data
        # Add proper types for known sections
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")

        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = toml.load(f)
                    # Analyze all values to determine types
                    for _ in range(getattr(cls, '_max_keys', 5)):
                        types.append("ANY")
            except:
                for _ in range(5):
                    types.append("ANY")
        else:
            for _ in range(5):
                types.append("ANY")

        return tuple(types)

    RETURN_TYPES = property(lambda self: self.get_return_types())

    @classmethod
    def RETURN_NAMES(cls):
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")
        names = ["json_data"]

        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = toml.load(f)
                    # Get all unique keys
                    all_keys = []
                    for section_data in config.values():
                        for key in section_data.keys():
                            if key not in all_keys:
                                all_keys.append(key)

                    # Use actual key names
                    for i, key in enumerate(all_keys[:10]):
                        names.append(key)
            except:
                pass

        # Fill remaining with generic names
        while len(names) < getattr(cls, '_max_keys', 5) + 1:
            names.append(f"value_{len(names)}")

        return tuple(names)

    FUNCTION = "process"
    CATEGORY = "utils/toml"

    def process(self, section: str) -> Tuple:
        """Process with proper number of outputs"""

        config_path = os.path.join(os.path.dirname(__file__), "config.toml")
        config_data = {}

        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = toml.load(f)
            except Exception as e:
                print(f"Error: {e}")

        # Get section data
        json_output = {}
        outputs = []

        if section in config_data:
            section_data = config_data[section]
            json_output = section_data

            print(f"\n=== Processing: {section} ===")

            # Fill outputs with actual values
            for key, value in section_data.items():
                outputs.append(value)
                print(f"  {key}: {value} ({type(value).__name__})")

        # Pad outputs to match expected count
        max_outputs = getattr(self.__class__, '_max_keys', 5)
        while len(outputs) < max_outputs:
            outputs.append(None)

        # JSON string
        json_str = json.dumps(json_output, indent=2)

        return (json_str, *outputs[:max_outputs])

    @classmethod
    def IS_CHANGED(cls, section):
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")
        if os.path.exists(config_path):
            return f"{os.path.getmtime(config_path)}_{section}"
        return "0"


# Node registration
NODE_CLASS_MAPPINGS = {
    "TomlSelector": TomlSelectorClean,
    "TomlSelectorPro": TomlSelectorProper,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TomlSelector": "TOML Selector",
    "TomlSelectorPro": "TOML Selector Pro",
}