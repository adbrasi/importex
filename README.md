# ComfyUI TOML Selector Nodes

Dynamic selector nodes for ComfyUI that read configuration from TOML files.

## Installation

1. Copy this folder to: `ComfyUI/custom_nodes/comfy_select/`
2. Install requirements: `pip install toml`
3. Restart ComfyUI

## Available Nodes

### 1. TOML Selector (Static)
- Fixed 10 outputs + JSON data
- **Reload button** to refresh configuration
- Preserves data types (int, float, bool, string)
- Shows output info in console

### 2. TOML Selector Dynamic
- **Dynamic output labels** that change based on selected section
- Output names update to match TOML keys
- Reload button for configuration refresh
- Up to 15 outputs + JSON data
- Real-time visual updates

## Configuration

Edit `config.toml`:

```toml
[player_1]
numero = 5
jujuba = "doce"
animal = "macaco"

[donald]
leao = "animal"
software = "antivirus"
```

## Features

- **Type Preservation**: Numbers stay as numbers, not converted to strings
- **Dynamic Labels**: Output names match your TOML keys (in Dynamic version)
- **Reload Button**: Both nodes have a reload button to refresh config
- **JSON Output**: First output always contains full section data as JSON
- **Console Info**: Shows key names and types when processing

## Usage

1. Place your `config.toml` in the node folder
2. Add node to ComfyUI workspace
3. Select section from dropdown
4. For Dynamic version: outputs automatically rename to match keys
5. Click reload button when you edit the TOML file

## Output Types

All outputs use `ANY` type, preserving original data types:
- `5` remains an integer
- `"text"` remains a string
- `true/false` remain booleans
- `3.14` remains a float