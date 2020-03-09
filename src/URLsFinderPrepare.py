class URLsFinderPrepare:
    def __init__(self,csv_delimiter,csv_encoding,scrapepath,scrapefile):
        self.csv_delimiter=csv_delimiter
        self.csv_encoding=csv_encoding
        self.scrapepath=scrapepath
        self.scrapefile=scrapefile
    def prepareFile(self):
        dflr=pd.read_csv(r'{0}{1}'.format(self.scrapepath,self.scrapefile), delimiter=self.csv_delimiter, encoding = self.csv_encoding, dtype={'ID': object})
        dflr=dflr.loc[(dflr['Status code']==200)]
        dflr['sum']=dflr['Has equal Email and URL Domains']+dflr['Has Email']+dflr['Has Name']+dflr['Has Phone']+dflr['Has Address']+dflr['Has ID']+dflr['Has Populated place']
        dflr1=dflr.groupby(['ID','Name','Suggested URL','Link position','Status code'], as_index=False).agg('sum')
        dflr1['Has Address']=(dflr1['Has Address']>0).astype(int)
        dflr1['Has Email']=(dflr1['Has Email']>0).astype(int)
        dflr1['Has ID']=(dflr1['Has ID']>0).astype(int)
        dflr1['Has Name']=(dflr1['Has Name']>0).astype(int)
        dflr1['Has Phone']=(dflr1['Has Phone']>0).astype(int)
        dflr1['Has Populated place']=(dflr1['Has Populated place']>0).astype(int)
        dflr1['Has Simple Suggested URL']=(dflr1['Has Simple Suggested URL']>0).astype(int)
        dflr1['Has equal Email and URL Domains']=(dflr1['Has equal Email and URL Domains']>0).astype(int)
        dflr1['Has equal domain']=(dflr1['Has equal domain']>0).astype(int)
        dflr1 = pd.merge(dflr1,dflr[['ID','URL']],on=['ID'],how = 'left',left_index=True)
        dflr=dflr1.drop_duplicates(keep='first').reset_index(drop=True)
        dflr.sort_values(by=['ID','Link position'], ascending=[True,True], inplace=True)
        dflr['Has URL']=dflr['URL'].apply(lambda x: 0 if pd.isna(x) else 1)
        dflr=dflr.reset_index(drop=True)
        return dflr
    def prepareLR(self,dflr,test_size,random_state):
        dflr['predict']=dflr[['Has equal domain']]
        dflr['Score']=dflr['sum']-dflr['sum']*dflr['Link position']/100
        idx = dflr.groupby(['ID'])['Score'].transform(max) == dflr['Score']
        dflr=dflr[idx]
        X = dflr[['Has Simple Suggested URL','Has Address','Has Email','Has ID','Has Name','Has Phone','Has Populated place','Has equal Email and URL Domains']]
        y = dflr['predict']
        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=test_size,random_state=random_state)
#        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=test_size) # for production
        logistic_regression= LogisticRegression(solver = 'lbfgs')
        logistic_regression.fit(X_train,y_train)
        y_pred=logistic_regression.predict(X_test)
        return X_train,X_test,y_train,y_test, y_pred, X,logistic_regression
    def prepareCM(self,y_test, y_pred):
        confusion_matrix = pd.crosstab(y_test, y_pred, rownames=['Actual URL'], colnames=['Predicted URL'])
        sn.heatmap(confusion_matrix, annot=True, cmap="YlGnBu" ,fmt='g')
        plt.title('Confusion matrix')
    def prepareA(self,X_train, y_train,y_test, y_pred,logistic_regression):
        print("The training accuracy",logistic_regression.score(X_train, y_train)) #is the training accuracy, while
        print("The testing accuracy:",metrics.accuracy_score(y_test, y_pred)) #is the testing accuracy.
        print("Precision:",metrics.precision_score(y_test, y_pred))
        print("Recall:",metrics.recall_score(y_test, y_pred))
    def prepareC(self,y_test, y_pred):
        print(metrics.classification_report(y_test, y_pred))
    def prepareR(self,X_test,y_test, y_pred,logistic_regression):
        lra = metrics.roc_auc_score(y_test,y_pred)
        fpr, tpr, thresholds = metrics.roc_curve(y_test, logistic_regression.predict_proba(X_test)[:,1])
        plt.figure()
        plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % lra)
        plt.plot([0, 1], [0, 1],'r--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC curve')
        plt.legend(loc="lower right")
        plt.savefig('Log_ROC')
        plt.show()
    def prepareP(self,dflr,y_test, y_pred,X,logistic_regression):
        X = dflr[['Has Simple Suggested URL','Has Address','Has Email','Has ID','Has Name','Has Phone','Has Populated place','Has equal Email and URL Domains']]
        df_new=dflr[['ID','Name','Link position','Score','Suggested URL','URL']]
        df_new = pd.merge(df_new,pd.DataFrame(logistic_regression.predict(X)),how = 'left',left_index = True, right_index = True)
        df_new=df_new.rename({df_new.columns[6]: "predict"}, axis=1)
        df_new = pd.merge(df_new,pd.DataFrame(logistic_regression.predict_proba(X)),how = 'left',left_index = True, right_index = True)
        df_new = df_new.drop_duplicates(keep='first')
        return df_new
    def prepareS(self,df_new):
#        df_sug = df_new.drop(df_new[df_new.predict_x == 0].index)
        df_sug = df_new
#        df_sug.sort_values(by=[1], ascending=[False], inplace=True)
#        df_sug = df_sug.drop_duplicates(subset=['ID', 'Link position', 'Suggested URL','URL','predict_x'],keep='first')
        df_sug = df_sug.drop_duplicates(subset=['ID', 'Link position', 'Suggested URL','URL'],keep='first')
        return df_sug
    def prepareSS(self,df_sug,level,allURL):
        if not allURL:
            df_sug=df_sug.loc[(df_sug['URL'].isnull())]
        df_sug=df_sug.loc[(df_sug[1]>level)]
        df_sug=df_sug.sort_values(by=['Score'], ascending=[False])
        df_sug = df_sug.drop_duplicates(subset=['ID'],keep='first')
        df_sug=df_sug.sort_values(by=['ID'], ascending=[True])
        if not allURL:
            df_sug['This is Logistic Regression Suggested URL'] = [x.split('/')[0]+'//'+x.split('/')[2] for x in df_sug['Suggested URL']]
            df_sug=df_sug.drop(['Link position', 'Suggested URL','URL','Score','predict',0,1], axis=1)
            df_sug = df_sug.reset_index(drop=True)
        return df_sug
