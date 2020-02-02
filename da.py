
from flask import Flask,render_template,request
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from sklearn.datasets import load_iris
import numpy as np
import io
import seaborn as sns
from scipy.stats import norm



iris = load_iris()

df = pd.DataFrame(data= np.c_[iris['data'], iris['target']],
                     columns= iris['feature_names'] + ['target'])


#good=df[df['target']==1]['sepal width (cm)']
#bad=df[df['target']==0]['sepal width (cm)']


def build_graph(good,bad):
    img = io.BytesIO()
    sns.distplot(good,fit=norm,kde=False)
    sns.distplot(bad,fit=norm,kde=False)
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)


#graph1=build_graph(good,bad)

app = Flask(__name__)

@app.route('/',methods = ['POST', 'GET'])
def index():

   select =  request.form.get('comp_select')

   if select:
       select=select
   else:
       select=df.columns[0]

   variables=df.columns
   variables=variables.to_list()
   variables.remove('target')

   good=df[df['target']==1][select]
   bad=df[df['target']==0][select]
   values=[]
   values.append(df[select].quantile(0.25))
   values.append(df[select].quantile(0.50))
   values.append(df[select].quantile(0.75))

   labels = [
    '0.25', '0.50', '0.75']
   max=df[select].max()+1

   graph1=build_graph(good,bad)
   return render_template('index.html',graph1=graph1,variables=variables,\
       select=select,labels=labels,max=max,values=values)
    

if __name__ == "__main__":
 #app.run()
 app.run(debug = False)
 #app.run(host='0.0.0.0',port=5000)
 #serve(app, host='0.0.0.0', port=5000)

