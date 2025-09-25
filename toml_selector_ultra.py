"""
Ultra Dynamic TOML Selector Node for ComfyUI
"""

import os
import toml
import json
from typing import Dict, List, Tuple, Any, Optional
from server import PromptServer
from aiohttp import web

# Global storage for TOML configurations
TOML_CONFIG_CACHE = {}

def load_toml_config():
    """Load and cache TOML configuration"""
    config_path = os.path.join(os.path.dirname(__file__), "config.toml")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return toml.load(f)
        except Exception as e:
            print(f"Error loading config.toml: {e}")
    return {}

class TomlSelectorUltra:
    """
    Ultra dynamic version with real-time output adjustment
    """

    def __init__(self):
        self.config_data = {}
        self.current_section = None
        self.current_outputs = []

    @classmethod
    def INPUT_TYPES(cls):
        config = load_toml_config()
        sections = list(config.keys()) if config else ["default"]

        return {
            "required": {
                "section": (sections, {"default": sections[0] if sections else "default"}),
            },
            "hidden": {
                "node_id": "UNIQUE_ID"
            }
        }

    # Dynamic output configuration
    @classmethod
    def RETURN_TYPES(cls):
        # Maximum possible outputs
        return tuple(["ANY" for _ in range(16)])

    @classmethod
    def RETURN_NAMES(cls):
        # Will be dynamically updated via JavaScript
        return tuple([f"output_{i}" for i in range(16)])

    FUNCTION = "process_section"
    CATEGORY = "utils/selector/ultra"
    OUTPUT_NODE = True

    def process_section(self, section: str, node_id: str = None) -> Tuple:
        """Process the selected section with dynamic outputs"""

        # Load fresh config
        config = load_toml_config()

        # Initialize all outputs with None
        outputs = [None] * 16

        if section in config:
            section_data = config[section]

            # Store in cache for JavaScript access
            TOML_CONFIG_CACHE[str(node_id)] = {
                "section": section,
                "data": section_data,
                "keys": list(section_data.keys())
            }

            # Fill outputs based on section data
            for i, (key, value) in enumerate(section_data.items()):
                if i < 16:
                    outputs[i] = value

            # Send update to frontend
            if node_id:
                PromptServer.instance.send_sync("toml.selector.update", {
                    "node_id": node_id,
                    "section": section,
                    "keys": list(section_data.keys()),
                    "values": list(section_data.values())
                })

        return tuple(outputs)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        """Force update when config changes"""
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")
        if os.path.exists(config_path):
            return os.path.getmtime(config_path)
        return 0


# API Routes for Ultra Dynamic version
@PromptServer.instance.routes.post("/api/toml/get_config")
async def get_toml_config(request):
    """Get the entire TOML configuration"""
    try:
        config = load_toml_config()
        return web.json_response({
            "success": True,
            "config": config,
            "sections": list(config.keys())
        })
    except Exception as e:
        return web.json_response({
            "success": False,
            "error": str(e)
        })

@PromptServer.instance.routes.post("/api/toml/get_section")
async def get_toml_section_ultra(request):
    """Get specific section data"""
    try:
        data = await request.json()
        section = data.get("section")
        node_id = data.get("node_id")

        config = load_toml_config()

        if section in config:
            section_data = config[section]

            # Cache for node
            if node_id:
                TOML_CONFIG_CACHE[str(node_id)] = {
                    "section": section,
                    "data": section_data,
                    "keys": list(section_data.keys())
                }

            return web.json_response({
                "success": True,
                "section": section,
                "data": section_data,
                "keys": list(section_data.keys()),
                "values": list(section_data.values())
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

@PromptServer.instance.routes.post("/api/toml/reload")
async def reload_toml_config(request):
    """Force reload of TOML configuration"""
    try:
        config = load_toml_config()
        TOML_CONFIG_CACHE.clear()
        return web.json_response({
            "success": True,
            "config": config,
            "message": "Configuration reloaded successfully"
        })
    except Exception as e:
        return web.json_response({
            "success": False,
            "error": str(e)
        })


# Register the Ultra node
NODE_CLASS_MAPPINGS_ULTRA = {
    "TomlSelectorUltra": TomlSelectorUltra,
}

NODE_DISPLAY_NAME_MAPPINGS_ULTRA = {
    "TomlSelectorUltra": "TOML Selector (Ultra Dynamic)",
}