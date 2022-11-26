from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import json
from waitress import serve
import datetime
import requests
from flask_jwt_extended import create_access_token,  verify_jwt_in_request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import re

app = Flask(__name__)
cors = CORS(app)
app.config["JWT_SECRET_KEY"]="#M1s10Nt13/"
jwt = JWTManager(app)

@app.route("/",methods=['GET'])
def test():
    json ={}
    json["mensaje"] = "Servidor ejecutándose..."
    return jsonify(json)

@app.route("/login", methods = ['POST'])
def create_token():
    datosUsuario = request.get_json()
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-seguridad"]+'/usuarios/validate'
    respuesta = requests.post(url,json = datosUsuario, headers= headers)
    if respuesta.status_code == 200:
            user = respuesta.json()
            expires = datetime.timedelta(hours = 12)
            access_token = create_access_token(identity=user, expires_delta= expires)
            return jsonify({"token":access_token,"user_id":user["_id"]})
    else:
            return jsonify({"msg":"Correo o contraseña incorrecta"}), 401

@app.before_request
def before_request_callback():
    endpoint = limpiarUrl(request.path)
    rutaExcluida = ["/login"]
    if rutaExcluida.__contains__(request.path):
        print("Ruta excluida "+str(request.path))
        pass
    elif verify_jwt_in_request():
        usuario = get_jwt_identity()
        if usuario['rol'] is not None:
            permiso = validarPermiso(endpoint, request.method, usuario['rol']['_id'])
            if not permiso:
                return jsonify({"mensaje: ":"No tiene permisos para ejecutar esta accion"}),401
        else:
            return jsonify({"mensaje: ":"No tiene permisos para ejecutar esta accion"}),401

def validarPermiso(endpoint, metodo, id_rol):
    url = data['url-ms-seguridad']+'/permisos-rol/validar-permiso/rol/'+id_rol
    tienePermiso = False
    print(url)
    headers = {"content-Type":"application/json; charset = utf-8"}
    body = {
        "url": endpoint,
        "metodo": metodo
    }
    respuesta = requests.get(url, json= body, headers=headers)
    try:
        datos = respuesta.json()
        if("_id" in datos):
            tienePermiso = True
    except:
        pass
    return  tienePermiso

def limpiarUrl(url): #127.0.0.1:8080/permisos-rol/sdfsdfsdf/rol/sdfsdf/permiso/sdfsdf
    partesUrl = url.split('/') #127.0.0.1:8080/candidatos/5a5sd5 -> ['127.0.0.1:8080','candidatos','5a5sd5']
    for parte in partesUrl:
        if re.search('\\d', parte): #\\d -> expresion regular -> contiene string alfanumerico
           url = url.replace(parte,'?')
    return url

@app.route("/candidatos", methods = ['POST'])
def crearcandidato():
    datoscandidato = request.get_json()
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-registraduria"]+'/candidatos'
    respuesta = requests.post(url, json = datoscandidato, headers= headers)
    return jsonify(respuesta.json())

@app.route("/candidatos/<string:id>", methods = ['GET'])
def Obtenercandidato(id):
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-registraduria"]+'/candidatos/'+id
    respuesta = requests.get(url, headers= headers)
    return jsonify(respuesta.json())

@app.route("/candidatos", methods = ['GET'])
def Obtenercandidatos():
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-registraduria"]+'/candidatos'
    respuesta = requests.get(url, headers= headers)
    return jsonify(respuesta.json())

@app.route("/candidatos/<string:id>", methods = ['PUT'])
def actualizarcandidato(id):
    datoscandidato= request.get_json()
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-registraduria"]+'/candidatos/'+id
    respuesta = requests.put(url,json = datoscandidato, headers=headers)
    return jsonify(respuesta.json())

@app.route("/candidatos/<string:id>", methods = ['DELETE'])
def eliminarcandidato(id):
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-registraduria"] + '/candidatos'
    respuesta = requests.delete(url, headers=headers)
    return jsonify(respuesta.json())

#--------------------------------------------------------------
@app.route("/partidos",methods=['POST'])
def crearpartido():
    datospartido = request.get_json()
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-registraduria"] + '/partidos'
    respuesta = requests.post(url, json=datospartido, headers=headers)
    return jsonify(respuesta.json())
###################
@app.route("/partidos",methods=['GET'])
def mostrarpartidos():
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-registraduria"] + '/partidos'
    respuesta = requests.get(url, headers=headers)
    return jsonify(respuesta.json())
################
@app.route("/partidos/<string:id>",methods=['GET'])
def mostrarpartido(id):
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-registraduria"] + '/partidos/'+id
    respuesta = requests.get(url, headers=headers)
    return jsonify(respuesta.json())
##########################
@app.route("/partidos/<string:id>", methods=['PUT'])
def actualizarpartido(id):
    datospartido = request.get_json()
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-registraduria"] + '/partidos/' + id
    respuesta = requests.put(url, json= datospartido, headers=headers)
    return jsonify(respuesta.json())
########################
@app.route("/partidos/<string:id>", methods=['DELETE'])
def eliminarpartido(id):
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-registraduria"] + '/partidos/' + id
    respuesta = requests.delete(url, headers=headers)
    return jsonify(respuesta.json())
#--------------------------------------------------------------
@app.route("/mesas",methods=['POST'])
def crearmesa():
    datosmesa = request.get_json()
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-registraduria"] + '/mesas'
    respuesta = requests.post(url, json=datosmesa, headers=headers)
    return jsonify(respuesta.json())
########################
@app.route("/mesas",methods=['GET'])
def mostrarmesas():
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-registraduria"] + '/mesas'
    respuesta = requests.get(url, headers=headers)
    return jsonify(respuesta.json())
###################
@app.route("/mesas/<string:id>",methods=['GET'])
def mostrarmesa(id):
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-registraduria"] + '/mesas/'+id
    respuesta = requests.get(url, headers=headers)
    return jsonify(respuesta.json())
####################
@app.route("/mesas/<string:id>",methods=['PUT'])
def actualizarmesa(id):
    datosmesa = request.get_json()
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-registraduria"] + '/mesas/' + id
    respuesta = requests.put(url, json= datosmesa, headers=headers)
    return jsonify(respuesta.json())
#####################
@app.route("/mesas/<string:id>",methods=['DELETE'])
def eliminarmesa(id):
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-registraduria"] + '/mesas/' + id
    respuesta = requests.delete(url, headers=headers)
    return jsonify(respuesta.json())
###############
@app.route("/candidatos/<string:id>/partido/<string:id_partido>",methods=['PUT'])
def asignacandidatos(id, id_partido):
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-registraduria"] + '/candidatos/' + id+'/partido/'+id_partido
    respuesta = requests.put(url, headers=headers)
    return jsonify(respuesta.json())
#--------------------------------------------------------------
@app.route("/resultados/candidato/<string:id_candidato>/mesa/<string:id_mesa>",methods=['POST'])
def crearInscripcion(id_candidato, id_mesa):
    datosInscripcion = request.get_json()
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-registraduria"] + '/resultados/candidato/'+id_candidato+'/mesa/'+id_mesa
    respuesta = requests.post(url, json=datosInscripcion, headers=headers)
    return jsonify(respuesta.json())
#########################3
@app.route("/resultados",methods=['GET'])
def mostrarresultados():
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-registraduria"] + '/resultados'
    respuesta = requests.get(url, headers=headers)
    return jsonify(respuesta.json())

#######################
@app.route("/resultados/<string:id>",methods = ['GET'])
def mostrarInscripcion(id):
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-registraduria"] + '/resultados/'+id
    respuesta = requests.get(url, headers=headers)
    return jsonify(respuesta.json())
#########################
@app.route("/resultados/<string:id>/candidato/<string:id_candidato>/mesa/<string:id_mesa>",methods = ['PUT'])
def actualizarInscripcion(id,id_candidato,id_mesa):
    datosInscripcion = request.get_json()
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-registraduria"] + '/resultados/'+id+'/candidato/'+id_candidato+'/mesa/'+id_mesa
    respuesta = requests.put(url, json=datosInscripcion, headers=headers)
    return jsonify(respuesta.json())
##########################
@app.route("/resultados/<string:id>",methods =['DELETE'])
def eliminarInscripcion(id):
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-registraduria"] + '/resultados/' + id
    respuesta = requests.delete(url, headers=headers)
    return jsonify(respuesta.json())
##########################
@app.route("/resultados/mesa/<string:id_mesa>", methods =['GET'])
def inscritosmesa(id_mesa):
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-registraduria"] + '/resultados/mesa/'+id_mesa
    respuesta = requests.get(url, headers=headers)
    return jsonify(respuesta.json())
##########################33
@app.route("/resultados/notas_mayores", methods =['GET'])
def notasMayores():
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-registraduria"] + '/resultados/nota_mayores'
    respuesta = requests.get(url, headers=headers)
    return jsonify(respuesta.json())
###########################
@app.route("/resultados/promedio/mesa/<string:id_mesa>", methods = ['GET'])
def promediomesa(id_mesa):
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-registraduria"] + '/resultados/promedio/mesa/'+id_mesa
    respuesta = requests.get(url, headers=headers)
    return jsonify(respuesta.json())
#--------------------------------------------------------------

def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data

if __name__=="__main__":
    data = loadFileConfig()
    print("Servidor corriendo en: "+data["url-api"]+" puerto: "+str(data["port"]))
    serve(app, host =data["url-api"],port=data["port"])