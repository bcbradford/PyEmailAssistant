''' Load's the config.yml file into the app's config dictionary. '''

import os
import yaml

def init_config() -> dict:
    package_path = os.path.dirname(os.path.dirname(__file__)) # src
    project_path = os.path.dirname(package_path) # PyEmailAssistant
    config_path = os.path.join(project_path, "config.yml")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Path: '{project_path}' not found.")

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    if not config:
        raise ValueError(f"Failed to load configuration file: {config_path}")

    _set_paths(config, project_path)

    return config

def _set_paths(config, project_path):
    # Set Model File Paths
    model_path = config["MODEL"]["MODEL_PATH"]
    model_file_path = os.path.join(project_path, model_path)

    for key, file in config["MODEL"]["FILES"].items():
        config["MODEL"]["FILES"][key] = os.path.join(model_file_path, file)

    log_path = config["LOGGER"]["LOG_PATH"]
    info_file = config["LOGGER"]["INFO_LOG"]
    info_path = os.path.join(project_path, log_path, info_file)
    error_file = config["LOGGER"]["ERROR_LOG"]
    error_path = os.path.join(project_path, log_path, error_file);

    config["LOGGER"]["INFO_LOG"] = info_path
    config["LOGGER"]["ERROR_LOG"] = error_path

