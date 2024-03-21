import os
import subprocess as sp
from datetime import datetime
import argparse

import logging

logger = logging.getLogger(__name__)


def _initialize_dvc(home_dir, data_dir):
    """initialize .dvc stored in 'home_dir' with data in 'data_dir'"""
    logger.info("initializing DVC repository")
    
    with sp.Popen(["git", "init"], cwd=home_dir) as proc:
        proc.wait()

    with sp.Popen(["dvc", "init"], cwd=home_dir) as proc:
        proc.wait()

    with sp.Popen(["dvc", "remote", "add", "-d", "dvc_remote", os.path.join(home_dir, "dvc_remote")], cwd=home_dir) as proc:
        proc.wait()
    
    with sp.Popen(["git", "commit", "-m", "'dvc setup'"], cwd=home_dir) as proc:
        proc.wait()
    
    logger.info("DVC setup committed to Git")

def _check_keys(dict_, required_keys):
    """checks if a dict contains all expected keys"""
    for key in required_keys:
        if key not in dict_:
            raise ValueError(f'input argument "data_files" is missing required key "{key}"')


def track_data(home_dir, data_files, **kwargs):
    """
    Track the raw data stored in data_files['raw_data_file'] with .dvc located in the 'home_dir'

    Args:
        home_dir (str): location of the '.dvc' for data tracking
        data_files (dict): including the key 'raw_data_file', specifying the location of the 
          raw data
    """

    _check_keys(data_files, ['raw_data_file'])

    # os.chdir(home_dir)
    
    if not os.popen("dvc --version").read():
        raise ValueError("DVC is not installed. Please install DVC before running this script") 

    # Check if DVC was already initialized
    if not os.path.exists(os.path.join(home_dir, ".dvc")):
        logger.info("DVC not yet initialized")
        _initialize_dvc(home_dir, data_files['raw_data_file'])
    
    if not os.popen("dvc status").read() == "Data and pipelines are up to date.\n":
        logger.info("Data update detected")
        logger.info(os.popen("dvc status").read())
        
        # TODO: Not fully sure these are working either
        # Track current version of dataset
        current_time = datetime.now()
        timestamp = current_time.strftime("%Y/%m/%d-%H:%M:%S")

        logger.info(f"Current working directory: {os.getcwd()}")

        with sp.Popen(f"dvc add data.csv", cwd=home_dir) as proc:
            proc.wait()

        with sp.Popen(f"git add {data_files['raw_data_file']}.dvc", cwd=home_dir) as proc:
            proc.wait()
        
        commit_msg = ' '.join(["adding dataset version", timestamp])
        with sp.Popen(f"git commit -m '{commit_msg}'", cwd=home_dir) as proc:
            proc.wait()
        
        logger.info(f"Committed new dataset version {timestamp}")
    
        with sp.Popen("dvc push", cwd=home_dir) as proc:
            proc.wait()
        logger.info("Pushed data to remote")
    else:
        logger.info("Dataset did not change. Nothing to track.")
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Track data')
    parser.add_argument('--home_dir', type=str, help='root dir')
    parser.add_argument('--data_files', type=dict, help='dict including the key "raw_data_file"')

    args = parser.parse_args()
    track_data(args.home_dir, args.data_dir)
    