#import pandas as pd
import mysql.connector

from flask import Flask, json, jsonify, request
#from config import config
#from flask_mysqldb import MySQL

app = Flask(__name__)

#conexion = MySQL(app)

conexion = mysql.connector.connect(host='aws.cd8mxk9c4l84.sa-east-1.rds.amazonaws.com',database='tributacao',user='admin',password='senha123')

"""
con = mysql.connector.connect(host='aws.cd8mxk9c4l84.sa-east-1.rds.amazonaws.com',database='tributacao',user='admin',password='senha123')

cursor = con.cursor()
if con.is_connected():
    print('My SQL conectado')
"""


@app.route('/')
def homepage():
    return 'Essa é a API de Consulta Tributação, seja bem vindo!'


"""
@app.route('/tribut',methods=['GET'])
def tribut():
  query = (f"SELECT id, ncm, cest,segmento, item, descricao, mva, aliquota, fundamentacao FROM tributacao;")
  df = pd.read_sql(query, con)
  tabela = pd.DataFrame(df)
  tabela2 = tabela.to_json(orient = 'columns')
  #return(tabela)
  return tabela2

@app.route('/ncm/<int:buscancm>',methods=['GET'])
def obter_ncm(buscancm):
  query = (f"SELECT id, ncm, cest,segmento, item, descricao, mva, aliquota, fundamentacao FROM tributacao WHERE ncm like '%{buscancm}%';")
  df = pd.read_sql(query, con)
  tabela = pd.DataFrame(df)
  tabela2 = tabela.to_json(orient = 'columns')
  #return(tabela)
  return tabela2

@app.route('/cest/<busca_cest>')
def obter_cest(busca_cest):
  query = (f"SELECT id, ncm, cest,segmento, item, descricao, mva, aliquota, fundamentacao FROM tributacao WHERE cest like '%{busca_cest}%';")
  df2 = pd.read_sql(query, con)
  tabela3 = pd.DataFrame(df2)
  tabela4 = tabela3.to_json(orient = 'columns')
  #return(tabela)
  return tabela4

@app.route('/descr/<buscadescr>')
def obter_descr(buscadescr):
  query = (f"SELECT id, ncm, cest,segmento, item, descricao, mva, aliquota, fundamentacao FROM tributacao WHERE descricao like '%{buscadescr}%';")
  df = pd.read_sql(query, con)
  tabela5 = pd.DataFrame(df)
  tabela6 = tabela5.to_json(orient = 'columns')
  #return(tabela)
  return tabela6
"""

@app.route('/dados', methods=['GET'])
def listar_dados():
    try:
        cursor = conexion.cursor()
        #cursor = conexion.connection.cursor()
        sql = "SELECT id, ncm, cest,segmento, item, descricao, mva, aliquota, fundamentacao FROM tributacao"
        cursor.execute(sql)
        datos = cursor.fetchall()
        dados=[]
        for fila in datos:
            dado={'id': fila[0],'ncm': fila[1], 'cest': fila[2], 'segmento': fila[3], 'item': fila[4], 'descricao': fila[5], 'mva': fila[6], 'aliquota': fila[7], 'fundamentacao': fila[8]}
            dados.append(dado)
        return jsonify({'dados': dados,'menssagem': "Dados Listados"})
    except Exception as ex:
        return jsonify({'menssagem': "Error"})

@app.route('/dados/<busca_ncm>', methods=['GET'])
def filtrar_ncm(busca_ncm):
    try:
        cursor = conexion.cursor()
        #cursor = conexion.connection.cursor()
        sql = f"SELECT id, ncm, cest,segmento, item, descricao, mva, aliquota, fundamentacao FROM tributacao WHERE ncm like '%{busca_ncm}%'"
        cursor.execute(sql)
        datos = cursor.fetchall()
        dados = []
        if datos != None:
            for fila in datos:
                dado = {'id': fila[0], 'ncm': fila[1], 'cest': fila[2], 'segmento': fila[3], 'item': fila[4],
                    'descricao': fila[5], 'mva': fila[6], 'aliquota': fila[7], 'fundamentacao': fila[8]}
                dados.append(dado)
        else:
            return jsonify(({'mensagem': "NCM não encontrado!"}))

        return jsonify({'dados': dados, 'menssagem': "NCMs Listados"})


    except Exception as ex:
        return jsonify({'menssagem': "Error"})


def pagina_nao_encontrada(error):
    return "<h1>A página não existe...</h1>"


if __name__ == '__main__':
    #app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_nao_encontrada)
    app.run(host='0.0.0.0')
