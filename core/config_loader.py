import yaml
import os

def load_config(env):
    local_override_path = os.path.join("config", f"{env}.local.yaml")
    default_path = os.path.join("config", f"{env}.yaml")
    path = local_override_path if os.path.exists(local_override_path) else default_path

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Config file not found: {path}. Create {default_path} or add a local override at {local_override_path}."
        )

    with open(path, "r") as f:
        return yaml.safe_load(f)
