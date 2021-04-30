from flask import Flask,jsonify,request

app = Flask(__name__)

from files import files

################################################## CON FICHEROS EXTERNOS ##########################################################

#Editar el contenido de open con la ruta del archivo a abrir, aqui puedes leer el contenido del fichero

@app.route('/agent')
def getConf():
	 f = open ('agent.conf','r')
	 contenido = f.readlines()
	 f.close()
	 return jsonify({"agente":contenido})

#Editar el contenido de data, creara un agente.conf nuevo sobrescribiendo el archivo.	 

@app.route('/agentwrite')
def writeConf():
	data = ["Línea 1", "Línea 2", "Línea 3", "Línea 4", "Línea 5"]
	f = open("agent.conf", "w")
	escritura=f.writelines("%s\n" % s for s in data)
	f.close()
	return jsonify({"archivo sobrescrito"})

#Editar el contenido de new lines, se añadiran esas lineas al final del archivo.

@app.route('/agentaddlines')
def addlineConf():
	newlines = ["", "Línea 2", "Línea 3", "Línea 4", "Línea 5"]
	f = open("agent.conf", "a")
	f.writelines("%s\n" % s for s in newlines)
	f.close()
	return jsonify({"lineas añadidas"})	

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

#para especificar el puerto del server
if __name__== '__main__':
	  app.run(debug=True, port=4000)