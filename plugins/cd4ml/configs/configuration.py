# prepare_config.py
import hydra
from omegaconf import OmegaConf

@hydra.main(config_path="conf_files", config_name="config")
def load_config(cfg: DictConfig) -> None:
    # Process and save your configuration as needed
    # For example, save to a file or print to stdout
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    load_config()
