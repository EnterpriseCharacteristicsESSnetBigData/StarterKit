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
        dflr1=dflr.groupby(['ID','Name','Suggested URL','Link position','Has Simple Suggested URL','Has equal domain'], as_index=False)['sum'].sum()
        dflr1 = pd.merge(dflr1,dflr[['ID','URL']],on=['ID'],how = 'left',left_index=True)
        dflr=dflr1.drop_duplicates(keep='first').reset_index(drop=True)
        dflr.sort_values(by=['ID','Link position'], ascending=[True,True], inplace=True)
        dflr['Has URL']=dflr['URL'].apply(lambda x: 0 if pd.isna(x) else 1)
        dflr=dflr.reset_index(drop=True)
        return dflr
    def prepareLR(self,dflr,test_size,random_state):
        dflr['predict']=dflr['Has Simple Suggested URL']
        dflr['Score']=dflr['sum']/(dflr['Link position']+1)
        X = dflr[['Score','Has URL','Has equal domain']]
        y = dflr['predict']
        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=test_size,random_state=random_state)
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
    def prepareP(self,dflr,y_test, y_pred,X,logistic_regression):
        y_test['predict'] = y_pred
        df_out = pd.merge(dflr,y_test[['predict']],how = 'left',left_index = True, right_index = True)
        df_new=df_out[['ID','Name','Link position','Score','Suggested URL','URL','predict_x']]
        df_new = pd.merge(df_new,pd.DataFrame(logistic_regression.predict_proba(X)),how = 'left',left_index = True, right_index = True)
        df_new = df_new.drop_duplicates(keep='first')
        return df_new
    def prepareS(self,df_new):
        df_sug = df_new.drop(df_new[df_new.predict_x == 0].index)
        df_sug.sort_values(by=[1], ascending=[False], inplace=True)
        df_sug = df_sug.drop_duplicates(subset=['ID', 'Link position', 'Suggested URL','URL','predict_x'],keep='first')
        return df_sug
    def prepareSS(self,df_sug,level,allURL):
        if not allURL:
            df_sug=df_sug.loc[(df_sug['URL'].isnull())]
        df_sug=df_sug.loc[(df_sug[1]>level)]
        return df_sug
