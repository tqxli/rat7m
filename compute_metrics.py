import argparse
import os, time
import numpy as np
import pandas as pd
from metrics import *
import json

metrics = {
    'mpjpe': mpjpe,
    'pa_mpjpe': pa_mpjpe,
    'n_mpjpe': n_mpjpe
}

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prediction_path", type=str, required=True, help="Path to the prediction results.")
    parser.add_argument("--gt_path", type=str, default="mini_rat7m_train_test_annotation.pkl", help="Path to the ground truth.")
    parser.add_argument("--metric", type=str, default="all", help="Error metric about to be computed.")
    parser.add_argument("--save_dir", type=str, default="error_metrics_eval", help="Location to store detailed metric results.")

    args = parser.parse_args()
    return args

def check_args(args):
    assert os.path.isfile(args.prediction_path), "Cannot find the prediction file at the specified location."
    assert os.path.splitext(args.prediction_path)[1] == '.csv', "The prediction needs to be stored in a csv file."

def main(args):
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)

    df = pd.read_csv(args.prediction_path)
    kpts_3d_pred = df.to_numpy().reshape((-1, 20, 3))
    annot_dict = np.load(args.gt_path, allow_pickle=True)
    #start = time.time()
    kpts_3d_gt = annot_dict['table']['3D_keypoints'][annot_dict['table']['subject_idx'] == 5]
    #end = time.time()
    #print(end-start)

    assert kpts_3d_pred.shape == kpts_3d_gt.shape

    eval_results = {}
    if args.metric != "all":
        eval_results[args.metric] = metrics[args.metric](kpts_3d_pred, kpts_3d_gt)
    else:
        for k, metric in metrics.items():
            eval_results[k] = metric(kpts_3d_pred, kpts_3d_gt)
    
    print("Validation results on mini-RAT7M:")
    print("=================================")
    for met, v in eval_results.items():
        print(met, ": {}".format(v.sum()/len(v)))
    print("=================================")

    
    df = pd.DataFrame(eval_results)
    df.to_csv(os.path.join(args.save_dir, 'eval_results.csv'))


if __name__ == '__main__':
    args = parse_args()
    check_args(args)
    main(args)