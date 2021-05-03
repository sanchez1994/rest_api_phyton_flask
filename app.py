from flask import Flask,jsonify,request
from os import remove,path
import re

app = Flask(__name__)

from files import files

################################################## CON FICHEROS EXTERNOS ##########################################################

#Editar el contenido de open con la ruta del archivo a abrir, aqui puedes leer el contenido del fichero
@app.route('/agent')
def getConf():
	 file = open ('agent.conf','r')
	 contenido = file.readlines()
	 file.close()
	 return jsonify({"agente":contenido})

#Editar el contenido de search para encontrar la palabra busca.
@app.route('/agentsearch')
def searchConf():
	file = open('agent.conf', "r")
	contador = 0
	for line in file:
	  search=re.search(r"snmp_verify",line)
	  contador += 1
	  if search:
	  	print(search, contador)
	  	break
	return jsonify({"busquedarealizada":""})	
 

#Editar el contenido de data, creara un agente.conf nuevo sobrescribiendo el archivo.	 
@app.route('/agentwrite')
def writeConf():
	data = ["Línea 1", "Línea 2", "Línea 3", "Línea 4", "Línea 5"]
	file = open("agent.conf", "w")
	escritura=file.writelines("%s\n" % s for s in data)
	file.close()
	return jsonify({"archivosobrescrito":""})

#Editar el contenido de new lines, se añadiran esas lineas al final del archivo.
@app.route('/agentaddlines')
def addlineConf():
	newlines = ["", "Línea 2", "Línea 3", "Línea 4", "Línea 5"]
	file = open("agent.conf", "a")
	file.writelines("%s\n" % s for s in newlines)
	file.close()
	return jsonify({"lineasañadidas":""})

#Para borrar un fichero, meter la ruta del fichero.
@app.route('/agentdelete')	
def delConf():
	if path.exists("nada.conf"):
		remove('nada.conf')
	return jsonify({"fichero borrado":""})	


#################################################### CON FICHEROS PYTHON ########################################################## 
																																	
#ruta para ver el contenido del archivo
@app.route('/files')
def getFiles():
	 return jsonify({"products":files, "message": "Files list"})	

#ruta para buscar datos del archivo por nombre (GET)
@app.route('/files/<string:agent_name>')
def getFile(agent_name):
	agentFound = [agent for agent in files if agent['agent_name'] == agent_name]
	if (len(agentFound) > 0):
		return jsonify({"agent":agentFound[0]})
	return jsonify({"message":"agente no encontrado"})

#ruta para añadir datos al archivo
@app.route('/files',methods=['POST'])
def addAgent():
	new_agent= {
	"agent_name":request.json['agent_name'],
	"agent_alias":request.json['agent_alias'],
	"address":request.json['address'],
	"group":request.json['group']
	}
	files.append(new_agent)
	return jsonify({"message":"agente añadido satisfactoriamente","files":files})

#ruta para modificar datos del archivo
@app.route('/files/<string:agent_name>', methods=['PUT'])
def editAgent(agent_name):
	agentFound = [agent for agent in files if agent['agent_name'] == agent_name]
	if (len(agentFound) > 0):
		agentFound[0]['agent_name'] = request.json['agent_name']
		agentFound[0]['agent_alias'] = request.json['agent_alias']
		agentFound[0]['address'] = request.json['address']
		agentFound[0]['group'] = request.json['group']
		return jsonify({
			"message":"agente actualizado",
			"agent":agentFound[0]})
	return jsonify({"message":"agente no encontrado"})

#ruta para borrar datos del archivo
@app.route('/files/<string:agent_name>',methods=['DELETE'])
def deleteAgent(agent_name):
	agentFound = [agent for agent in files if agent["agent_name"]== agent_name]
	if len(agentFound) > 0:
		files.remove(agentFound[0])
		return jsonify({
		  "message":"agente eliminado",
		  "agentes":files
			})
	return jsonify({"message":"agente no encontrado"})

#para especificar el puerto del server, activar el modo debug y activar multihilos. 
if __name__== '__main__':
	  app.run(debug=True, port=4000, threaded=True)