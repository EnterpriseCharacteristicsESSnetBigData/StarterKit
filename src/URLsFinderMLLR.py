# -*- coding: utf-8 -*-

"""
Source code for the OBEC Stater Kit URLs Finder Machine Learning 
with Logistic Regression class.
TODO: 
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import seaborn as sn
import glob
import numpy as np
import math
from IPython.display import Markdown, display
from urllib.parse import urlparse
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (5, 3) # (w, h)
plt.rcParams["figure.dpi"] = 100

# Class URLsFinderMLLR contains functions responsible to find OBECs of
# Enterprises with Machine Learning Logistic Regression method.
# These are the variables that this class uses:
#    version - identification of the scraped files by date, id or other.
#    start_path - directory where a csv file with Enterprises 
#                 information is located.
#    machin_learning_path - directory where the csv files with 
#                           machine learning information are saved.
#    scrape_path - directory where a csv files with scraped 
#                  Enterprises information are saved.
#    scrape_file - name of a csv file with scraped information from 
#                  websites.
#    obec_file - name of the csv files with infomation from machine 
#                learning execution.
#    obec_words_file - Words to be serched in the contents of the 
#                      pages, eg.: e-mail, address, phone, etc. in 
#                      case of finding urls or key words in case of 
#                      OBEC.
#    obec_known_characteristics - name of a csv file known enterprises 
#                                 characteristics.
#    csv_delimiter - delimiter of the csv file, eg.: ";".
#    csv_encoding - encoding of the csv file, eg.: "utf-8".
#    csv_ext - files extension, eg.: ".csv".
#from datetime import datetime
#variables = {
#    'version': datetime.now().strftime('%Y-%m-%d'),
#    'version': 'v.2020.2',
#    'start_path': '.\\sbr_data\\',
#    'machin_learning_path': '.\\machin_learning\\',
#    'scrape_path': '.\\scrape_data\\',
#    'scrape_file': 'OBEC_Starter_Kit_Scrape_Data',
#    'obec_file': 'OBEC_Starter_Kit_URLs',
#    'obec_words_file': 'URLs_words.txt',
#    'obec_known_characteristics': 'OBEC_known_urls.csv',
#    'csv_delimiter': ';',
#    'csv_encoding': 'utf-8',
#    'csv_ext': '.csv',
#}

class URLsFinderMLLR:

    def __init__(self, iterable=(), **kwargs):
        self.__dict__.update(iterable, **kwargs)
        print(" ".join('URLs Finder machine learning logistic \
                       regression module is ready to work for vesion \
                       {0}'.format(self.version).split()))


    def prepare_file_form_scraped_data(self):
        all_files = []
        path = r'{0}{1}_{2}*{3}'.format(self.scrape_path,
                                        self.scrape_file,
									    self.version,
									    self.csv_ext)
        all_files += glob.glob(path, recursive=True)
        li = []
        for filename in all_files:
            df = pd.read_csv(filename,
                     delimiter = self.csv_delimiter, 
                     encoding = self.csv_encoding, 
                     dtype = {'ID': object})
            li.append(df)
        try:
            frame = pd.concat(li, axis=0, ignore_index=True)
        except Exception as e:
            frame = pd.DataFrame()
            print('No sach files to concatenate {0}'.format(path))
            print(str(e))
        else:
            self.save_results(frame, '_final')
            scrape = frame
            self.df_scrape = scrape
            try:
                df = pd.read_csv(r'{0}{1}'.format(
                                                self.start_path, 
				                                self.obec_words_file),
                                 delimiter = self.csv_delimiter, 
                                 encoding = self.csv_encoding)
            except Exception as e:
                df = pd.DataFrame()
                print(
				    'Something went wrong on reading ' \
					'{0}{1}'.format(self.start_path, 
				                   self.obec_words_file)
				)
                print(str(e))
            else:
                self.df_words = df			
                try:
                    dfc = pd.read_csv(
                                r'{0}{1}'.format(
					                self.start_path, 
				                    self.obec_known_characteristics),
                                delimiter = self.csv_delimiter, 
                                encoding = self.csv_encoding, 
                                dtype = {'ID': object})
                except Exception as e:
                    dfc = pd.DataFrame()
                    print(
					    'Something went wrong on reading ' \
					    '{0}{1}'.format(self.start_path, 
				                       self.obec_known_characteristics)
			        )
                    print(str(e))
                else:
                    self.df_obec = dfc				
                    if not 'Link position' in frame.columns:
                        frame = frame[
	     			        ['ID', 'Suggested URL', 'URL to scrape'] 
		    			    + df['Word'].unique().tolist()
			    		]
                        frame = frame.groupby(['ID', 'URL'])[
                            df['Word'].unique().tolist()
                        ].sum().reset_index()
                    else:
                        frame = frame[
	     			        [
                                'ID', 'Name', 'Suggested URL', 
                                'URL to scrape', 'Link position', 
                                'Has equal domain', 
                                'Has Simple Suggested URL'
                            ] 
		    			    + df['Word'].unique().tolist()
			    		]
                        frame = frame.groupby([
                            'ID', 
                            'Name', 
                            'Suggested URL', 
                            'Link position'
                        ])[df['Word'].unique().tolist() \
                            + [
                                'Has equal domain', 
                                'Has Simple Suggested URL'
                              ]].sum().reset_index()
                        frame[[
                            'Has equal domain', 
                            'Has Simple Suggested URL'
                        ]] = frame[[
                                'Has equal domain', 
                                'Has Simple Suggested URL'
                            ]].where(~(frame[[
                                    'Has equal domain', 
                                    'Has Simple Suggested URL'
                                ]]>0), other=1)	# count to 1
                    frame[
                        df['Word'].unique().tolist()
                    ] = frame[
                            df['Word'].unique().tolist()
                        ].where(~(frame[
                                        df['Word'].unique().tolist()
                                    ]>0),other=1)	# word count to 1
                    try:
                        frame = frame.join(dfc.set_index('ID'), on='ID')
                    except Exception as e:
                        frame = pd.DataFrame()
                        print(
					        'Something went wrong on joining ' \
                            '{0}{1}_{2}{3} and {4}{5}'.format(
							    self.machin_learning_path,
                                self.scrape_file,
								self.version,
                                self.csv_ext,								
							    self.start_path,
				                self.obec_known_characteristics)
			            )
                        print(str(e))
                    else:
                        frame['Known OBEC'] = frame['OBEC'].apply(\
						    lambda x: 0 if pd.isna(x) else 1)
                        if not 'Link position' in frame.columns:
                            frame[
                                'Link position'
                            ] = frame.apply(
                                lambda row: 1 if '.'.join(
                                    urlparse(
                                        row['URL'].lower()
                                        ).netloc.split('.')[-2:]
                                    ) == '.'.join(
                                        urlparse(
                                            str(row['OBEC']
                                                ).lower()
                                            ).netloc.split('.')[-2:]
                                        ) else 2, 
                                axis = 1)
                        frame['sum'] = 0
                        for x in df['Word'].unique().tolist():
                            frame['sum'] = frame['sum'] + frame[x]
                        if 'Has equal domain' in frame.columns:
                            frame['sum'] = frame['sum'] \
                                           + frame['Has equal domain']
                        if 'Has Simple Suggested URL' in frame.columns:
                            frame['sum'] = frame['sum'] \
                                           + frame['Has Simple Suggested URL']
                        frame['Score'] = frame['sum'] \
                                         - frame['sum'] \
                                           * frame['Link position'] / 100
#                        frame['Score'] = frame['sum'] - frame['sum']/100
                        self.df_ml = frame						
        self.save_results(frame, '_ml_ready')
        return [frame, df ,dfc, scrape]
		

    def fit(self, *args, **kwargs):
        test_size = kwargs.get('test_size', 0.7)
        random_state = kwargs.get('random_state', 0)
        solver = kwargs.get('solver', 'lbfgs')
        max_iter = kwargs.get('max_iter', 1000)
        dflr = self.df_ml
        idx = dflr.groupby(['ID'])['Score'].transform(max) == dflr['Score']
        dflr = dflr[idx]
        display(Markdown('**Dataframe Object for Training and Test:**'))
        print(dflr.info(verbose=False))
        X = dflr[self.df_words['Word'].unique().tolist()]
        X = dflr[['Score']]
        y = dflr['Known OBEC']
        if 'Has equal domain' in dflr.columns:		
            y = dflr['Has equal domain']
        if random_state < 1 :
            X_train, X_test, y_train, y_test = train_test_split(
                                                X, y, 
                                                test_size=test_size)
        else:
            X_train, X_test, y_train, y_test = train_test_split(
                                                X, y, 
                                                test_size=test_size, 
                                                random_state=random_state)
        logistic_regression = LogisticRegression(solver=solver, 
                                                 max_iter=max_iter)
        try:
            logistic_regression.fit(X_train, y_train)
        except:
            print("Could not fit the model")
            return X_train, X_test, y_train, y_test, y, X, \
                   logistic_regression, False
        else:
            y_pred = logistic_regression.predict(X_test)
            display(Markdown('**Logistic Regression Model \
                             Information:**'))
            print("The training accuracy", 
                  '{0:.2}'.format(
                        logistic_regression.score(X_train, y_train)))
            print("The testing accuracy:",
                  '{0:.2}'.format(
                        metrics.accuracy_score(y_test, y_pred)))
            print("Precision:", '{0:.2}'.format(
                    metrics.precision_score(y_test, y_pred)))
            print("Recall:", '{0:.2}'.format(
                    metrics.recall_score(y_test, y_pred)))
            print("Average precision-recall score:", '{0:.2}'.format(
                    metrics.average_precision_score(y_test, y_pred)))
            return X_train, X_test, y_train, y_test, y_pred, X, \
                   logistic_regression, True


    def predict(self, logistic_regression):
        dflr = self.df_ml
        X = dflr[self.df_words['Word'].unique().tolist()]
        X = dflr[['Score']]
        df_new = dflr.drop(self.df_words['Word'].unique().tolist(), axis=1)
        df_new = pd.merge(df_new, 
                          pd.DataFrame(logistic_regression.predict(X)), 
                          how = 'left', 
                          left_index=True, 
                          right_index=True)
        df_new = df_new.rename({0: "predict"}, axis=1)
        df_new = pd.merge(df_new,
                          pd.DataFrame(logistic_regression.predict_proba(X)),
                          how = 'left',
                          left_index=True, 
                          right_index=True)
        df_new = df_new.drop_duplicates(keep = 'first')
        self.save_results(df_new, '_ml_lr_predict')
        return df_new


    def drop_duplicates(self, df_new):
        df_sug = df_new
        df_sug.sort_values(by=[1], ascending=[False], inplace=True)
        if 'Suggested URL' in df_sug.columns:
            df_sug = df_sug.drop_duplicates(
                subset = [
                    'ID', 'Link position', 'OBEC', 
                    'Suggested URL', 'predict'
                ],
                keep='first'
            )
        if 'URL' in df_sug.columns:
            df_sug = df_sug.drop_duplicates(
                subset = ['ID', 'Link position', 'OBEC', 'URL', 'predict'],
                keep='first'
            )
        return df_sug
		

    def results(self, df):
        df = df.loc[(df['predict'] == 1) | (df['Known OBEC'] == 1)]
        df = df.sort_values(by=['ID', 'Link position', 1], 
                            ascending=[True, True, False])
        df0 = df.drop_duplicates(subset=['ID'], keep='first')
        self.save_results(df0, '_ml_lr_result')
        df1 = df.loc[(df['predict'] == 1) & (df['Known OBEC'] == 1)]
        self.save_results(df1, '_ml_lr_result_known')
        df2 = df.loc[(df['predict'] == 0) & (df['Known OBEC'] == 1)]
        self.save_results(df2, '_ml_lr_result_revise')
        df3 = df.loc[(df['predict'] == 1) & (df['Known OBEC'] == 0)]
        self.save_results(df3, '_ml_lr_result_new')
        df11 = df1.drop_duplicates(
            subset=['ID', 'Known OBEC', 'predict'], 
            keep='first')
        self.save_results(df11, '_ml_lr_result_known_first')
        df12 = df1.drop_duplicates(
            subset=['ID', 'Known OBEC', 'predict', 'Link position'], 
            keep='first')
        self.save_results(df12, '_ml_lr_result_known_multiple')
        df21 = df2.drop_duplicates(
            subset=['ID', 'Known OBEC', 'predict'], 
            keep='first')
        self.save_results(df21, '_ml_lr_result_revise_first')
        df22 = df2.drop_duplicates(
            subset=['ID', 'Known OBEC', 'predict', 'Link position'], 
            keep='first')
        self.save_results(df22, '_ml_lr_result_revise_multiple')
        df32 = df3.drop_duplicates(
            subset=['ID', 'Known OBEC', 'predict', 'Link position'], 
            keep='first')
        self.save_results(df32, '_ml_lr_result_new_multiple')
        return [df0, df1, df2, df3, df11, df12, df21, df22, df32]
		

    def save_results(self, frame, str):
        frame.to_csv(r'{0}{1}_{2}{3}{4}'.format(
                                      self.machin_learning_path,
		                              self.obec_file,
									  self.version,
									  str,
									  self.csv_ext), 
                     sep = self.csv_delimiter, 
                     encoding = self.csv_encoding, 
                     index = None, 
                     header=True)


    def multiple(self, *args, **kwargs):
        test_size = kwargs.get('test_size', 0.7)
        solver = kwargs.get('solver', 'lbfgs')
        max_iter = kwargs.get('max_iter', 1000)
        multiple = kwargs.get('multiple', 1)
        random = kwargs.get('random', True)
        mcc = kwargs.get('mcc', 0.5)
        frames=[]
        for x in range(0, multiple):
            display(Markdown('### Logistic Regression Model Fitting \
                              for Random State {0}'.format(x)))
            if random :
                lr = self.fit(test_size=test_size,
                              solver=solver,
                              max_iter=max_iter)
            else:
                lr = self.fit(test_size=test_size,
                              random_state=x,
                              solver=solver,
                              max_iter=max_iter)
            if self.check_mcc(lr[3], lr[4], mcc) and lr[7]:
                self.confusion_matrix(lr[3], lr[4])
                self.confusion_matrix_information(lr[3], lr[4])
                self.classification_report(lr[3], lr[4])
                self.roc_curve(lr[1], lr[3], lr[4], lr[6])
                df_new = self.predict(lr[6])
                frames.append(df_new)
        result = pd.concat(frames)
        result = result.sort_values(by=['ID'], ascending=[True])
        result.drop_duplicates(subset=None, keep='first', inplace=True)
        result = result.reset_index(drop=True)
        return result			


    def check_mcc(self, y_test, y_pred, mcc):
        tf = False
        cm = pd.crosstab(y_test, 
                         y_pred, 
                         rownames=['Known OBEC URLs'], 
                         colnames=['Predicted OBEC URLs'])
        try:
            TP = cm.iloc[1][1]
            TN = cm.iloc[0][0]
            FP = cm.iloc[0][1]
            FN = cm.iloc[1][0]
        except:
            tf = False
        else:
            if (TP*TN-FP*FN)/math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN)) > mcc :
                tf = True
        return tf


    def confusion_matrix(self, y_test, y_pred):
        cm = pd.crosstab(y_test, 
                         y_pred, 
                         rownames=['Known OBEC URLs'], 
                         colnames=['Predicted OBEC URLs'])
        sn.heatmap(cm, annot=True, cmap = 'YlGnBu', fmt = 'g')
        plt.title('Confusion matrix')


    def confusion_matrix_information(self, y_test, y_pred):
        cm = pd.crosstab(y_test, 
                         y_pred, 
                         rownames=['Known OBEC URLs'], 
                         colnames=['Predicted OBEC URLs'])
        TP = cm.iloc[1][1]
        TN = cm.iloc[0][0]
        FP = cm.iloc[0][1]
        FN = cm.iloc[1][0]
        display(Markdown('**Confusion Matrix Information:**'))
        print('OBEC URLs that are predicted as False and we do not ' \
               'know (True Negatives):', TN)
        print('OBEC URLs that are predicted as False and we do know ' \
              '(False Negatives):', FN)
        print('OBEC URLs that are predicted as True and we do not ' \
              'know (False Positives):', FP)
        print('OBEC URLs that are predicted as True and we do know ' \
              '(True Positives):', TP)
        print('Accuracy = (TP+TN)/(TP+TN+FP+FN):', 
              '{0:.2}'.format((TP+TN)/(TP+TN+FP+FN)))
        print('Precision = TP/(TP+FP):', '{0:.2}'.format(TP/(TP+FP)))
        print('Recall = TP/(TP+FN):', '{0:.2}'.format(TP/(TP+FN)))
        print('Specificity = TN/(TN+FP):', '{0:.2}'.format(TN/(TN+FP)))
        print('F1 Score = 2*TP/(2*TP+FP+FN):', 
              '{0:.2}'.format(2*TP/(2*TP+FP+FN)))
        print(
            'MCC = (TP*TN-FP*FN)/math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN)):', 
            '{0:.2}'.format(
                (TP*TN-FP*FN)/math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))))
        display(Markdown('**Confusion Matrix Explanations:**'))
        print('Accuracy - This is simply equal to the proportion ' \
              'of predictions that the model classified correctly.')
        print('Precision - Precision is also known as positive ' \
              'predictive value and is the proportion of relevant ' \
              'instances among the retrieved instances. In other ' \
              'words, it answers the question "What proportion of ' \
              'positive identifications was actually correct?".')
        print('Recall - Recall, also known as the sensitivity, hit ' \
              'rate, or the true positive rate (TPR), is the ' \
              'proportion of the total amount of relevant instances ' \
              'that were actually retrieved. It answers the question ' \
              '"What proportion of actual positives was identified ' \
              'correctly?".')
        print('Specificity - Specificity, also known as the true ' \
              'negative rate (TNR), measures the proportion of actual ' \
              'negatives that are correctly identified as such. It is ' \
              'the opposite of recall.')
        print('F1 Score - The F1 score is a measure of a test\'s ' \
              'accuracy — it is the harmonic mean of precision and ' \
              'recall. It can have a maximum score of 1 (perfect ' \
              'precision and recall) and a minimum of 0. Overall, ' \
              'it is a measure of the preciseness and robustness ' \
              'of your model.')
        print('Matthews correlation coefficient (MCC) - The MCC is ' \
              'in essence a correlation coefficient between the ' \
              'observed and predicted binary classifications; it ' \
              'returns a value between -1 and +1. A coefficient ' \
              'of +1 represents a perfect prediction, 0 no better ' \
              'than random prediction and -1 indicates total ' \
              'disagreement between prediction and observation. ' \
              'The statistic is also known as the phi coefficient. ' \
              'MCC is related to the chi-square statistic for a 2x2 ' \
              'contingency table.')


    def classification_report(self, y_test, y_pred):
        display(Markdown('**Classification Report:**'))
        print(metrics.classification_report(y_test, y_pred))


    def roc_curve(self, X_test, y_test, y_pred, logistic_regression):
        lra = metrics.roc_auc_score(y_test, y_pred)
        fpr, tpr, thresholds = metrics.roc_curve(
            y_test, logistic_regression.predict_proba(X_test)[:,1])
        plt.figure()
        plt.plot(
            fpr, tpr, 
            label = 'Logistic Regression (area = %0.2f)' % lra)
        plt.plot([0, 1], [0, 1], 'r--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC curve')
        plt.legend(loc = "lower right")
        plt.savefig('Log_ROC')
        plt.show()