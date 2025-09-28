"""
Simple Profile Selector Node for ComfyUI
"""

class ProfileSelector:
    """
    A simple selector node with predefined profiles and string/int outputs.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "profile": (
                    ["Lovehent", "VioletJoi", "VixMavis"],
                    {"default": "Lovehent"}
                ),
            }
        }

    # 4 strings + 1 int (NUMBER não é tipo válido no ComfyUI)
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "INT")
    RETURN_NAMES = ("output_1", "output_2", "output_3", "output_4", "output_5")

    FUNCTION = "select_profile"
    CATEGORY = "utils"

    def select_profile(self, profile: str):
        """Return profile-specific values"""

        # Define outputs for each profile
        # outputs: [str, str, str, str, int]
        profiles = {
            "Lovehent": [
                "masterwork,(artist:Shexyo),anime_screenshot, anime_coloring,",
                "masterpiece,anime_screenshot, anime_coloring,mdf_an,best quality, good quality, newest, very awa, absurdres, highres",
                "/workspace/Randomico/Lovehent/",
                "",
                0,
            ],
            "VioletJoi": [
                "masterwork,(3dcgi,3d),",
                "masterpiece, best quality, good quality, newest, very awa, absurdres, highres, hyper-detailed, excellent, latest",
                "/workspace/Randomico/VioletJoi/",
                "",
                1,
            ],
            "VixMavis": [
                "masterwork,(artist:Shexyo),curvy",
                "masterpiece, best quality, good quality, newest, very awa, absurdres, highres, hyper-detailed, excellent, latest,curvy_figure",
                "/workspace/Randomico/vixmavis/",
                "",
                0,
            ],
        }

        # Fallback com tipos consistentes (4 strings + 1 int)
        outputs = profiles.get(profile, ["", "", "", "", 0])

        return tuple(outputs)


# Node registration
NODE_CLASS_MAPPINGS = {
    "ProfileSelector": ProfileSelector,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ProfileSelector": "Profile Selector",
}
