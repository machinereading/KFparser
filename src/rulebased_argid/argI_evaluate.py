import csv
import re
import json
import argI_data_preprocessor


def evaluate(prediction_file_name, label_file_name, covered_output_file, feature_file, save_mode = True, CoNLL=True):
    with open(prediction_file_name, "r", encoding="utf-8") as make_file:
        predictions = json.load(make_file)    
    
    with open(feature_file, "r", encoding="utf-8") as make_file:
        features = json.load(make_file)
    
    label_datas = argI_data_preprocessor.load_data(label_file_name)
    final_predictions = []
    result_predictions = []
    if CoNLL == True:
        cmpchar = '_'
    else:
        cmpchar = 'O'

    covered_predictions = []
    covered_answers = []
    
    for i in range(0, len(predictions)):
        existance = 0
        for prediction in predictions[i]:
            for token in prediction['tokens']:
                if token[-3] != '_' and label_datas[i]['tokens'][int(token[0])][-3] != '_'\
                and token[-2] == label_datas[i]['tokens'][int(token[0])][-2]:
                    if existance == 1:
                        break
                    
                    
                    covered_FE = []
                    for token in label_datas[i]['tokens']:
                        if token[-1] != cmpchar:
                            if token[-1] not in covered_FE:
                                covered_FE.append(token[-1])
                    existance = 1
                    
                    existance2 = 1
                    for json_data in features:
                        if json_data['lu'] == token[-3] + '.' + token[-2]:
                            for covered in covered_FE:
                                existance3 = 0
                                for pattern in json_data['pattern']:
                                    for set_ in pattern['set']:
                                        if set_['FE'] == covered:
                                            existance3 = 1
                                existance2 *= existance3
                    if existance2 == 1:
                        covered_predictions.append(prediction)
                        covered_answers.append(label_datas[i])
                    
                    
                    
                    final_predictions.append(prediction)
                    result_predictions.append(prediction)
                    existance = 1
        if existance == 0:
            tempdic = {}
            tempdic['sentid'] = label_datas[i]['sentid']
            tempdic['text'] = label_datas[i]['text']
            tempdic['tokens'] = []
            for token in label_datas[i]['tokens']:
                if CoNLL == True:
                    tempdic['tokens'].append(token[0:-3] + ['_', '_', '_'])
                else:
                    tempdic['tokens'].append(token[0:-3] + ['_', '_', 'O'])
            result_predictions.append(tempdic)
            final_predictions.append([])
    
    precision_under = 0
    precision_over = 0
    recall_under = 0
    recall_over = 0
    covered_precision_under = 0
    covered_precision_over = 0
    covered_recall_under = 0
    covered_recall_over = 0
    not_covered_recall_under = 0
    
    for i in range(0, len(final_predictions)):
        if final_predictions[i] == []:
            for token in label_datas[i]['tokens']:
                if token[-1] != cmpchar:
                    not_covered_recall_under += 1
        else:
            for token in final_predictions[i]['tokens']:
                label_datas[i]['tokens'][int(token[0])][-1] = label_datas[i]['tokens'][int(token[0])][-1].replace("B_","")
                label_datas[i]['tokens'][int(token[0])][-1] = label_datas[i]['tokens'][int(token[0])][-1].replace("I_","")
                label_datas[i]['tokens'][int(token[0])][-1] = label_datas[i]['tokens'][int(token[0])][-1].replace("O_","")
                label_datas[i]['tokens'][int(token[0])][-1] = label_datas[i]['tokens'][int(token[0])][-1].replace("S_","")
                
                
                if token[-1] != cmpchar:
                    precision_under += 1
                if token[-1] != cmpchar and token[-1] == label_datas[i]['tokens'][int(token[0])][-1]:
                    precision_over += 1
            for token in label_datas[i]['tokens']:
                final_predictions[i]['tokens'][int(token[0])][-1] = final_predictions[i]['tokens'][int(token[0])][-1].replace("B_","")
                final_predictions[i]['tokens'][int(token[0])][-1] = final_predictions[i]['tokens'][int(token[0])][-1].replace("I_","")
                final_predictions[i]['tokens'][int(token[0])][-1] = final_predictions[i]['tokens'][int(token[0])][-1].replace("O_","")
                final_predictions[i]['tokens'][int(token[0])][-1] = final_predictions[i]['tokens'][int(token[0])][-1].replace("S_","")
                if token[-1] != cmpchar:
                    recall_under += 1
                if token[-1] != cmpchar and token[-1] == final_predictions[i]['tokens'][int(token[0])][-1]:
                    recall_over += 1

    for i in range(0, len(covered_predictions)):
        for token in covered_predictions[i]['tokens']:
            covered_answers[i]['tokens'][int(token[0])][-1] = covered_answers[i]['tokens'][int(token[0])][-1].replace("B_","")
            covered_answers[i]['tokens'][int(token[0])][-1] = covered_answers[i]['tokens'][int(token[0])][-1].replace("I_","")
            covered_answers[i]['tokens'][int(token[0])][-1] = covered_answers[i]['tokens'][int(token[0])][-1].replace("O_","")
            covered_answers[i]['tokens'][int(token[0])][-1] = covered_answers[i]['tokens'][int(token[0])][-1].replace("S_","")

            if token[-1] != cmpchar:
                covered_precision_under += 1
            if token[-1] != cmpchar and token[-1] == covered_answers[i]['tokens'][int(token[0])][-1]:
                covered_precision_over += 1
        for token in covered_answers[i]['tokens']:
            covered_predictions[i]['tokens'][int(token[0])][-1] = covered_predictions[i]['tokens'][int(token[0])][-1].replace("B_","")
            covered_predictions[i]['tokens'][int(token[0])][-1] = covered_predictions[i]['tokens'][int(token[0])][-1].replace("I_","")
            covered_predictions[i]['tokens'][int(token[0])][-1] = covered_predictions[i]['tokens'][int(token[0])][-1].replace("O_","")
            covered_predictions[i]['tokens'][int(token[0])][-1] = covered_predictions[i]['tokens'][int(token[0])][-1].replace("S_","")
            if token[-1] != cmpchar:
                covered_recall_under += 1
            if token[-1] != cmpchar and token[-1] == covered_predictions[i]['tokens'][int(token[0])][-1]:
                covered_recall_over += 1                
                    
                    
        
    
    if precision_under == 0.00000:
        precision = 0.00000
    else:
        precision = float(precision_over)/float(precision_under)
    if not_covered_recall_under + recall_under == 0.00000:
        not_covered_recall = 0.00000
    else:
        not_covered_recall = float(recall_over) / float(recall_under + not_covered_recall_under)
    if precision + not_covered_recall == 0.00000:
        not_covered_f1_score = 0.00000
    else:
        not_covered_f1_score = 2*precision*not_covered_recall / (precision+not_covered_recall)
    if recall_under == 0.00000:
        recall = 0.00000
    else:
        recall = float(recall_over) / float(recall_under)
    if precision + recall == 0.00000:
        f1_score = 0.00000
    else:
        f1_score = 2*precision*recall / (precision+recall)
    print("Evaluating with not covered Test set ...")
    print("#Precision: ",  precision, \
          "#Recall: ", not_covered_recall, \
          "#F1_score: ", not_covered_f1_score)
    print("Evaluating with Frame covered Test set ...")
    print("#Precision: ",  precision, \
          "#Recall: ", recall, \
          "#F1_score: ", f1_score)
    print("Evaluating with both Frame and Argument covered Test set...")
    c_precision = float(covered_precision_over)/float(covered_precision_under)
    c_recall = float(covered_recall_over)/float(covered_recall_under)
    print("#Precision: ",  c_precision, \
          "#Recall: ", c_recall, \
          "#F1_score: ", 2*c_precision*c_recall / (c_precision+c_recall) )
    
    print("##############################################")
    print("Evaluating DataSet Size: ", len(predictions))
    print("Evaluating with coverage of both Frame and Argument DataSet Size: ", len(covered_predictions))
    print("##############################################")
    
    
    print("Saving the Final_prediction tsv file with coverage of Frame...")
    if save_mode == True:
        f = open(covered_output_file, "w", encoding="utf-8", newline ='')
        wr = csv.writer(f, delimiter = '\t')
        for i in range(0, len(result_predictions)):
            wr.writerow(['#sentid:'+ result_predictions[i]['sentid']])
            wr.writerow(['#text:'+ result_predictions[i]['text']])
            for token in result_predictions[i]['tokens']:
                wr.writerow(token)
            wr.writerow('')
                
        f.close()
        
    
    