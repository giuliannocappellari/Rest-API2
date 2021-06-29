from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
#import pandas as pd
#from sklearn.model_selection import train_test_split
import pickle
from sklearn.linear_model import LinearRegression
import os

#esta comentado pois o modelo já foi testado e salvo em modelo.sav
#não é preciso deixar pois o custo do treinamento é alto

'''df = pd.read_csv("notebook\Data\casas.csv")
colunas = ['tamanho','ano','garagem']


#Variavel explicativa
X = df.drop('preco', axis=1)
#Variavel resposta
y = df['preco']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
modelo = LinearRegression()
modelo.fit(X_train, y_train)
'''

#configura a ordem das colunas, caso receba o json
colunas = ['tamanho','ano','garagem']

#lê o arquivo de modelo salvo
modelo = pickle.load(open('..\..\models\modelo.sav','rb'))

app = Flask(__name__)

#configura o usuário
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

#objeto de autenticação básica
basic_auth = BasicAuth(app)

#metodo get que retorna uma string
@app.route('/')
def home():
    return "Minha primeira API."

#metodo get -> retorna se a frase é boa ou ruim
@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(to='en')
    polaridade = tb_en.sentiment.polarity
    return f"polaridade: {polaridade}"

#metodo post -> recebe um json
'''@app.route('/cotacao/', methods=['POST'])
@basic_auth.required
def cotacao():
    dados = request.get_json()
    dados_input = [dados[col] for col in colunas]
    preco = modelo.predict([dados_input])
    return jsonify(preco=preco[0])'''

#metodo get -> retorna o preço estimado
@app.route('/cotacao/<tamanho>/<ano>/<garagem>')
@basic_auth.required
def cotacao(tamanho, ano, garagem):
    dados_input = [int(tamanho), int(ano), int(garagem)]
    preco = modelo.predict([dados_input])
    return f'preço estimado foi {preco}'

#reinicia a API quando o código for alterado
app.run(debug=True, host='0.0.0.0')
