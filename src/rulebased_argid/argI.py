import csv
import re
import json
import argI_data_preprocessor
import os
import argI_train
import argI_test
import argI_evaluate
import argI_Load_KFN

import argparse

description = "Argument Identification by Rule_based method in Korean Framenet. \n It is supported by CoNLL2006 or CoNLL2009 structure. \n [--mode] : [train, test, evaluate]"


def main():
    parser = argparse.ArgumentParser(description = description)
    parser.add_argument('--mode', type=str, default=None,
                        metavar = 'Mode[train/test/evaluate]',
                        help = 'select mode like [train/test/evaluate]')
    parser.add_argument('--train_file', type=str, default=None,
                        metavar='train_file',
                        help = 'to extract the default feature.\n It must be contained in [train] mode !!!tsv format!!!.')
    parser.add_argument('--feature_file', type=str, default=None,
                        metavar = 'feature_file',
                        help = 'Save the feature file or Load the feature file.\n It must be contained in [train/test/evaluate] mode with !!!json format!!!.')
    parser.add_argument('--test_file', type=str, default=None,
                        metavar = 'test_file',
                        help = 'Load the test file you want to predict the result from. \n It must be contained in [test] mode. !!!tsv format!!!')
    parser.add_argument('--prediction_file', type=str, default=None,
                        metavar = 'prediction_file',
                        help = 'Load the prediction file you want to compare the result with golden data. \n It must be contained in [test/evaluate] mode !!!json format!!!.')
    parser.add_argument('--golden_file', type=str, default=None,
                        metavar = 'golden_file',
                        help = 'Load the golden file you want to compare the result with prediction data. \n It must be contained in [evaluate] mode !!!tsv format!!!.')
    parser.add_argument('--CoNLL', type=str, default=None,
                        metavar = 'CoNLL',
                        help = '[2006, 2009] data format')
    parser.add_argument('--covered_output_file', type=str, default=None,
                        metavar = 'covered_output_file',
                        help = 'Save the output file covered the result with training frame. \n It must be contained in [evaluate] mode !!!tsv format!!!.')
    args = parser.parse_args()
    mode = args.mode
    print("Starting with mode: ", mode)
    if mode == 'train':
        print("Training...")
        train_file = args.train_file
        feature_file = args.feature_file
        CoNLL = args.CoNLL
        error = 0
        if train_file == None:
            print("[Error]: Please enter the training file")
            error=1
        if feature_file == None:
            print("[Error]: Please enter the feature file json")
            error=1
        if CoNLL == None:
            if CoNLL == '2009':
                CoNLL = False
            else:
                CoNLL = True
            print("[Error]: Please enter the CoNLL data format")
            error=1
        if error == 0:
            argI_train.train(file_name=train_file, output_file=feature_file, save_mode=True, CoNLL=CoNLL, data_format=True)
                        
    elif mode == 'test':
        test_file = args.test_file
        feature_file = args.feature_file
        prediction_file = args.prediction_file
        CoNLL = args.CoNLL
        error = 0
        if test_file == None:
            print("[Error]: Please enter the test file")
            error=1
        if feature_file == None:
            print("[Error]: Please enter the feature file")
            error=1
        if prediction_file == None:
            print("[Error]: Please enter the prediction file")
            error=1
        if CoNLL == None:
            if CoNLL == '2009':
                CoNLL = False
            else:
                CoNLL = True
            print("[Error]: Please enter the CoNLL data format")
            error=1
        if error == 0:
            argI_test.test(file_name=test_file, feature_name=feature_file, output_file=prediction_file, save_mode=True, CoNLL=CoNLL, data_format = True)        
        
    elif mode == 'evaluate':
        golden_file = args.golden_file
        covered_output_file = args.covered_output_file
        prediction_file = args.prediction_file
        feature_file = args.feature_file
        CoNLL = args.CoNLL
        error = 0
        if golden_file == None:
            print("[Error]: Please enter the test file")
            error=1
        if covered_output_file == None:
            print("[Error]: Please enter the feature file")
            error=1
        if prediction_file == None:
            print("[Error]: Please enter the prediction file")
            error=11
        if feature_file == None:
            print("[Error]: Please enter the feature file")
            error=1
        if CoNLL == None:
            if CoNLL == '2009':
                CoNLL = False
            else:
                CoNLL = True
            print("[Error]: Please enter the CoNLL data format")
            error=1
        if error == 0:
            argI_evaluate.evaluate(prediction_file, golden_file, covered_output_file, feature_file, True, CoNLL)
    else:
        print("[Error]: Mode Error")

if __name__ == "__main__":
    main()