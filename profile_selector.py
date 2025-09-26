"""
Simple Profile Selector Node for ComfyUI
"""

class ProfileSelector:
    """
    A simple selector node with predefined profiles and string outputs
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "profile": (["Lovehent", "VioletJoi", "VixMavis"], {
                    "default": "Lovehent"
                }),
            }
        }

    # 5 string outputs
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("output_1", "output_2", "output_3", "output_4", "output_5")

    FUNCTION = "select_profile"
    CATEGORY = "utils"

    def select_profile(self, profile: str):
        """Return profile-specific string values"""

        # Define outputs for each profile (customize these values as needed)
        profiles = {
            "Lovehent": [
                "masterwork,(artist:Shexyo),anime_screenshot, anime_coloring,",  # output_1
                "masterpiece,anime_screenshot, anime_coloring,mdf_an,best quality, good quality, newest, very awa, absurdres, highres",  # output_2
                "/workspace/Randomico/Lovehent/",  # output_3
                "",  # output_4
                "",  # output_5
            ],
            "VioletJoi": [
                "masterwork,",  # output_1
                "masterpiece, best quality, good quality, newest, very awa, absurdres, highres",  # output_2
                "/workspace/Randomico/VioletJoi/",  # output_3
                "",  # output_4
                "",  # output_5
            ],
            "VixMavis": [
                "masterwork,(3dcgi,3d),",  # output_1
                "masterpiece, best quality, good quality, newest, very awa, absurdres, highres,intricate, hyper-detailed, excellent, latest, ((cinematic lighting))",  # output_2
                "/workspace/Randomico/vixmavis/",  # output_3
                "",  # output_4
                "",  # output_5
            ]
        }

        # Get the selected profile outputs
        outputs = profiles.get(profile, [""] * 5)

        return tuple(outputs)


# Node registration
NODE_CLASS_MAPPINGS = {
    "ProfileSelector": ProfileSelector,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ProfileSelector": "Profile Selector",
}