#!/usr/bin/python3.6

''' Extracts N most frequent classes and splits data set for K-fold cross-validation. '''
import argparse
import pandas as pd

from sklearn.model_selection import StratifiedKFold
from tqdm import tqdm

from debug import dprint

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_folds', help='number of folds', type=int, default=5)
    parser.add_argument('--min_samples', help='minimum number of samples per class',
                        type=int, required=True)
    args = parser.parse_args()

    num_folds = int(args.num_folds)
    min_samples = int(args.min_samples)

    df = pd.read_csv('../data/train.csv')
    df.drop(columns='url', inplace=True)
    counts = df.landmark_id.value_counts()

    selected_classes = counts[counts >= min_samples].index
    num_classes = selected_classes.shape[0]
    print('classes with at least N samples:', num_classes)

    df = df.loc[df.landmark_id.isin(selected_classes)]
    dprint(df.shape)

    skf = StratifiedKFold(n_splits=num_folds, shuffle=True, random_state=7)

    for i, (train_index, val_index) in enumerate(tqdm(skf.split(df.id, df.landmark_id),
                                                      total=num_folds)):
        train = df.iloc[train_index]
        assert train.landmark_id.unique().shape[0] == num_classes
        train.to_csv(f'{min_samples}_samples_{num_classes}_classes_fold_{i}_train.csv', index=False)

        val = df.iloc[val_index]
        assert val.landmark_id.unique().shape[0] == num_classes
        val.to_csv(f'{min_samples}_samples_{num_classes}_classes_fold_{i}_val.csv', index=False)
