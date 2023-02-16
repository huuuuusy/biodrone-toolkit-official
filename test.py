from __future__ import absolute_import
from biodrone.experiments import *
import os
import json

from tracker.siamfc import TrackerSiamFC
from tracker.siamrpn import TrackerSiamRPN

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--gpu_number', type=str, help='the number of GPU you would like to use', default="1")
parser.add_argument('--tracker_name', type=str, help='the name of selected tracker', default='SiamFC')
parser.add_argument('--subset', type=str, help='the name of selected tracker', default='train')
args = parser.parse_args()

if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_number
    # the path of data folder
    root_dir = "/mnt/second/hushiyu/UAV/BioDrone"

    # the path to save the experiment result
    save_dir = os.path.join(root_dir, 'result')
    repetitions = 1

    # subset = 'val'
    subset = 'test'
    # subset = 'train'
    # subset = args.subset

    """
    I. RUN TRACKER
    Note: 
    method in run function means the evaluation mechanism, you can select the original mode (set 'none') or the restart mode (set 'restart')
    """ 
    tracker_name = args.tracker_name

    if tracker_name == 'SiamFC':
        net_path = os.path.join(os.path.split(os.path.realpath(__file__))[0],'pretrained', 'siamfc','model.pth')
        tracker = TrackerSiamFC(net_path=net_path)
    elif tracker_name == 'SiamRPN':
        net_path = os.path.join(os.path.split(os.path.realpath(__file__))[0],'pretrained', 'siamrpn','model.pth')
        tracker = TrackerSiamRPN(net_path=net_path)

    for repetition in range(repetitions):
        experiment = ExperimentBioDrone(root_dir, save_dir, subset, repetition+1)
        experiment.run(tracker, visualize=False, save_img=False, method='restart')

    """
    II. EVALUATION
    """
    tracker_names = ['SiamFC']

    for repetition in range(repetitions):
        experiment = ExperimentBioDrone(root_dir, save_dir, subset, repetition+1)
        experiment.report(tracker_names)
