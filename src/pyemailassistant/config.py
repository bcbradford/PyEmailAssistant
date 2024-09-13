''' Module used to load the app's config.yml file '''

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

    # Set Analytics Paths
    analytics_path = os.path.join(project_path, config["ANALYTICS_PATH"])
    config["ANALYTICS_PATH"] = analytics_path

    # Set Logger Paths
    log_path = config["LOGGER"]["LOG_PATH"]
    info_log_file = config["LOGGER"]["INFO_LOG"]
    info_log_path = os.path.join(project_path, log_path, info_log_file)
    error_log_file = config["LOGGER"]["ERROR_LOG"]
    error_log_path = os.path.join(project_path, log_path, error_log_file)
    config["LOGGER"]["INFO_LOG"] = info_log_path
    config["LOGGER"]["ERROR_LOG"] = error_log_path

    return config
