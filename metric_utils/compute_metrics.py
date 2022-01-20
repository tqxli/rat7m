import argparse
import os, time, datetime
import numpy as np
import pandas as pd
from metrics import *

metrics = {
    'mpjpe': mpjpe,
    'pa_mpjpe': pa_mpjpe,
    'n_mpjpe': n_mpjpe
}

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pred_path", type=str, 
        required=True, 
        help="Path to the prediction results.")
    parser.add_argument("--gt_path", type=str, default="../mini_rat7m_train_test_annotation.pkl", 
        help="Path to the ground truth annotation file.")
    parser.add_argument("--metric", type=str, default="all", 
        help="Error metric about to be computed. Defaults are mpjpe, pa_mpjpe, n_mpjpe.")
    parser.add_argument("--save_dir", type=str, default="../metrics_eval", 
        help="Location to store the detailed metric evaluation results.")

    args = parser.parse_args()
    return args

def check_args(args):
    assert os.path.isfile(args.pred_path), "Cannot find the prediction file at the specified location."
    assert os.path.splitext(args.pred_path)[1] == '.csv', "The prediction needs to be stored in a csv file."

def main(args):
    # make directory for saving the eval results
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)

    # read ground truth from annotations
    annot_dict = np.load(args.gt_path, allow_pickle=True)
    kpts_3d_gt = annot_dict['table']['3D_keypoints'][annot_dict['table']['subject_idx'] == 5]

    # read the predictions from the specified csv file
    df = pd.read_csv(args.pred_path)
    # read 3d keypoints 
    kpts_3d_pred = df.to_numpy().reshape((-1, 20, 3))
    assert kpts_3d_pred.shape == kpts_3d_gt.shape, \
        "Expect keypoint predictions for  {} samples, but only got {} from the csv file." 

    print("Evaluating over {} samples...".format(kpts_3d_pred.shape[0]))

    start = time.time()
    eval_results = {}
    if args.metric != "all":
        eval_results[args.metric] = metrics[args.metric](kpts_3d_pred, kpts_3d_gt)
    else:
        for k, metric in metrics.items():
            eval_results[k] = metric(kpts_3d_pred, kpts_3d_gt)
    end = time.time()
    print("Mean validation results on mini-RAT7M:")
    print("=================================")
    for met, v in eval_results.items():
        print(met, ": {}".format(v.sum()/len(v)))
    print("=================================")
    print("Time: {}".format(end - start))

    print("Saving results to {}".format(args.save_dir))
    df = pd.DataFrame(eval_results)
    df.to_csv(os.path.join(args.save_dir, '{}_eval.csv'.format(time.strftime("%Y-%m-%d-%H-%M"))))


if __name__ == '__main__':
    args = parse_args()
    check_args(args)
    main(args)