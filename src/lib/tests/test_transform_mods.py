from src.lib.transform_mods import flatten_mods


def test_flatten_mods_normal_case():
    data = {
        "gameplay": {
            "tweaks": ["Restricted Portals", "End Remastered"],
            "new": ["Moonlight", "Exposure"],
        },
        "optimization": ["Sodium", "Lithium"],
        "utils": ["Mod Menu", "Catalogue"],
    }
    expected = [
        "Catalogue",
        "End Remastered",
        "Exposure",
        "Lithium",
        "Mod Menu",
        "Moonlight",
        "Restricted Portals",
        "Sodium",
    ]
    result = flatten_mods(data)
    assert result == expected


def test_flatten_mods_empty_case():
    result = flatten_mods({})
    assert result == []


def test_flatten_mods_nested_case():
    data = {
        "category1": {"sub1": ["Mod2", "Mod1"], "sub2": ["Mod4"]},
        "category2": [["Mod3"], ["Mod5"]],  # Nested lists
    }
    expected = ["Mod1", "Mod2", "Mod3", "Mod4", "Mod5"]
    result = flatten_mods(data)
    assert result == expected
