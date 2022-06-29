# importing Flask and other modules
from flask import Flask, request, render_template
import flask
import csv
from flask import Flask, render_template, request
import difflib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

app = flask.Flask(__name__, template_folder='templates')

df= pd.read_excel('OnlineRetail.xlsx')
df['CustomerID'].isna().sum()
df = df.dropna(subset=['CustomerID'])

customer_item_matrix = df.pivot_table(
    index='CustomerID',
    columns='StockCode',
    values='Quantity',
    aggfunc='sum'
)

customer_item_matrix = customer_item_matrix.applymap(lambda x: 1 if x > 0 else 0)

user_user_sim_matrix = pd.DataFrame(cosine_similarity(customer_item_matrix))
user_user_sim_matrix.columns = customer_item_matrix.index
user_user_sim_matrix['CustomerID'] = customer_item_matrix.index

user_user_sim_matrix = user_user_sim_matrix.set_index('CustomerID')




# custID = 17935.0
def getRecommend(custID):
    for i in user_user_sim_matrix:
        temp = user_user_sim_matrix.loc[i].sort_values(ascending=False).head(2).index[1]
        if (temp==custID):
            print(i)
            break
    return product(i,temp)

def product(A,B):
    user_user_sim_matrix.loc[A].sort_values(ascending=False)
    items_bought_by_A = customer_item_matrix.loc[A][customer_item_matrix.loc[A]>0]
    
    items_bought_by_B = customer_item_matrix.loc[B][customer_item_matrix.loc[B]>0]
    
    items_to_recommend_to_B = set(items_bought_by_A.index) - set(items_bought_by_B.index)
   
    res=df.loc[df['StockCode'].isin(items_to_recommend_to_B),['StockCode', 'Description']].drop_duplicates().set_index('StockCode')
    
    
    resdf = pd.DataFrame(columns=['s','d'])
    resdf['s']=res.index
    resdf['d']=res.values
    return resdf

# Flask constructor
app = Flask(__name__)  
 
# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])
def printid():
    d = dict()
    if request.method == "POST":
       # getting input with name = fname in HTML form
        uid = request.form.get("userid")
        result=getRecommend(float(uid))
        print('result type : ',type(result))
        print(result)
        if (len(result)<10):
            for i in range(len(result)):
                d[str(result.iloc[i][0])] = result.iloc[i][1]
        else:
            for i in range(10):
                d[str(result.iloc[i][0])] = result.iloc[i][1]

            
        #return d
    return render_template("index.html",result=d)
 
if __name__=='__main__':
   app.run()