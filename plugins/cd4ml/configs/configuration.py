import sys
import logging
import omegaconf
import subprocess as sp

logger = logging.getLogger(__name__)

def load_config(conf_path):
    # Load the configuration file
    logger.info(f"Configuration path: {conf_path}")
    conf = omegaconf.OmegaConf.load(conf_path)
    logger.info(f"Configuration: {conf}")

    # DictConfig to Dict
    conf = omegaconf.OmegaConf.to_container(conf, resolve=True)

    # Set up git configuration Email
    with sp.Popen(["git", "config", "--global", "user.email", conf["general_config"]["git_email"]], stdout=sp.PIPE, stderr=sp.PIPE) as proc:
        print(proc.stdout.read())
        print(proc.stderr.read())

    # Set up git configuration Name
    with sp.Popen(["git", "config", "--global", "user.name", conf["general_config"]["git_name"]], stdout=sp.PIPE, stderr=sp.PIPE) as proc:
        print(proc.stdout.read())
        print(proc.stderr.read())

    return conf

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Load configuration file')
    parser.add_argument('--conf_path', type=str, help='Input file')

    args = parser.parse_args()
    load_config(args.conf_path)
