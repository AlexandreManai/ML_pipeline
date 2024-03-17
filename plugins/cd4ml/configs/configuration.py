import sys
import logging
import omegaconf

logger = logging.getLogger(__name__)

def load_config(conf_path):
    # Load the configuration file
    logger.info(f"Configuration path: {conf_path}")
    conf = omegaconf.OmegaConf.load(conf_path)
    logger.info(f"Configuration: {conf}")

    # DictConfig to Dict
    conf = omegaconf.OmegaConf.to_container(conf, resolve=True)

    return conf

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Load configuration file')
    parser.add_argument('--conf_path', type=str, help='Input file')

    args = parser.parse_args()
    load_config(args.conf_path)
