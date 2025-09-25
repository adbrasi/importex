# ComfyUI TOML Selector Node

Dynamic selector node for ComfyUI that reads configuration from TOML files.

## Installation

1. Copy this folder to: `ComfyUI/custom_nodes/comfy_select/`
2. Install requirements: `pip install -r requirements.txt`
3. Restart ComfyUI

## Usage

1. Edit `config.toml` to define your sections and values
2. In ComfyUI, look for nodes under "utils/selector" category
3. Available nodes:
   - **TOML Selector**: Basic selector with string outputs
   - **TOML Selector (Advanced)**: Shows full data + individual outputs
   - **TOML Selector (Dynamic)**: Preserves data types (int, float, bool, string)

## Configuration

Edit `config.toml`:

```toml
[section_name]
key1 = "value1"
key2 = 42
key3 = true
key4 = 3.14

[another_section]
option_a = "text"
option_b = 100
```

## Features

- Dynamic section selection via dropdown
- Automatic reload when config.toml changes
- Support for multiple data types
- Up to 10 outputs per section
- JSON output for complex workflows
- Real-time key display in console

## Example Workflows

1. **Character Selection**: Define characters with attributes (health, speed, power)
2. **Settings Presets**: Switch between different configuration presets
3. **Level Parameters**: Load different level configurations dynamically
4. **Material Properties**: Select between different material settings

## Node Outputs

- **json_data**: Full section data as JSON
- **out_1 to out_10**: Individual values from the section (preserves types)