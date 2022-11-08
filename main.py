import re

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
                return jsonify({"mensaje: ":"Se puede ejecutar la accion"}),200

def validarPermiso(endpoint, metodo, id_rol):
    url = data['url-ms-seguridad']+'validar-permiso/rol/'+id_rol
    tienePermiso = False
    headers = {"content-Type":"application/json; charset = utf-8"}
    body = {
        "url": endpoint,
        "metodo": metodo
    }
    respuesta = requests.get(url, json= body, headers=headers)
    try:
        datos = respuesta.json()
        if("_id" in datos):
            tienePermiso
    except:
        pass
    return  tienePermiso

def limpiarUrl(url): #127.0.0.1:8080/permisos-rol/sdfsdfsdf/rol/sdfsdf/permiso/sdfsdf
    partesUrl = url.split('/') #127.0.0.1:8080/estudiantes/5a5sd5 -> ['127.0.0.1:8080','estudiantes','5a5sd5']
    for parte in partesUrl:
        if re.search('\\d', parte): #\\d -> expresion regular -> contiene string alfanumerico
           url = url.replace(parte,'?')
    return url

@app.route("/estudiantes", methods = ['POST'])
def crearEstudiante():
    datosEstudiante = request.get_json()
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-academico"]+'/estudiantes'
    respuesta = request.post(url, json = datosEstudiante, headers= headers)
    return jsonify(respuesta.json())

@app.route("/estudiantes/<string:id>", methods = ['GET'])
def ObtenerEstudiante(id):
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-academico"]+'/estudiantes/'+id
    respuesta = requests.get(url, headers= headers)
    return jsonify(respuesta.json())

@app.route("/estudiantes", methods = ['GET'])
def ObtenerEstudiantes():
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-academico"]+'/estudiantes'
    respuesta = requests.get(url, headers= headers)
    return jsonify(respuesta.json())

@app.route("/estudiantes/<string:id>", methods = ['PUT'])
def actualizarEstudiante(id):
    datosEstudiante= request.get_json()
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-academico"]+'/estudiantes/'+id
    respuesta = requests.put(url,json = datosEstudiante, headers=headers)
    return jsonify(respuesta.json())

@app.route("/estudiantes/<string:id>", methods = ['DELETE'])
def eliminarEstudiante(id):
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-academico"] + '/estudiantes'
    respuesta = requests.delete(url, headers=headers)
    return jsonify(respuesta.json())

#--------------------------------------------------------------
@app.route("/departamentos",methods=['POST'])
def crearDepartamento():
    datosDepartamento = request.get_json()
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-academico"] + '/departamentos'
    respuesta = requests.post(url, json=datosDepartamento, headers=headers)
    return jsonify(respuesta.json())
###################
@app.route("/departamentos",methods=['GET'])
def mostrarDepartamentos():
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-academico"] + '/departamentos'
    respuesta = requests.get(url, headers=headers)
    return jsonify(respuesta.json())
################
@app.route("/departamentos/<string:id>",methods=['GET'])
def mostrarDepartamento(id):
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-academico"] + '/departamentos/'+id
    respuesta = requests.get(url, headers=headers)
    return jsonify(respuesta.json())
##########################
@app.route("/departamentos/<string:id>", methods=['PUT'])
def actualizarDepartamento(id):
    datosDepartamento = request.get_json()
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-academico"] + '/departamentos/' + id
    respuesta = requests.put(url, json= datosDepartamento, headers=headers)
    return jsonify(respuesta.json())
########################
@app.route("/departamentos/<string:id>", methods=['DELETE'])
def eliminarDepartamento(id):
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-academico"] + '/departamentos/' + id
    respuesta = requests.delete(url, headers=headers)
    return jsonify(respuesta.json())
#--------------------------------------------------------------
@app.route("/materias",methods=['POST'])
def crearMateria():
    datosMateria = request.get_json()
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-academico"] + '/materias'
    respuesta = requests.post(url, json=datosMateria, headers=headers)
    return jsonify(respuesta.json())
########################
@app.route("/materias",methods=['GET'])
def mostrarMaterias():
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-academico"] + '/materias'
    respuesta = requests.get(url, headers=headers)
    return jsonify(respuesta.json())
###################
@app.route("/materias/<string:id>",methods=['GET'])
def mostrarMateria(id):
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-academico"] + '/materias/'+id
    respuesta = requests.get(url, headers=headers)
    return jsonify(respuesta.json())
####################
@app.route("/materias/<string:id>",methods=['PUT'])
def actualizarMateria(id):
    datosMateria = request.get_json()
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-academico"] + '/materias/' + id
    respuesta = requests.put(url, json= datosMateria, headers=headers)
    return jsonify(respuesta.json())
#####################
@app.route("/materias/<string:id>",methods=['DELETE'])
def eliminarMateria(id):
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-academico"] + '/materias/' + id
    respuesta = requests.delete(url, headers=headers)
    return jsonify(respuesta.json())
###############
@app.route("/materias/<string:id>/departamento/<string:id_departamento>",methods=['PUT'])
def asignarMateria(id, id_departamento):
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-academico"] + '/materias/' + id+'/departamento/'+id_departamento
    respuesta = requests.put(url, headers=headers)
    return jsonify(respuesta.json())
#--------------------------------------------------------------
@app.route("/inscripciones/estudiante/<string:id_estudiante>/materia/<string:id_materia>",methods=['POST'])
def crearInscripcion(id_estudiante, id_materia):
    datosInscripcion = request.get_json()
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-academico"] + '/inscripciones/estudiante/'+id_estudiante+'/materia/'+id_materia
    respuesta = requests.post(url, json=datosInscripcion, headers=headers)
    return jsonify(respuesta.json())
#########################3
@app.route("/inscripciones",methods=['GET'])
def mostrarInscripciones():
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-academico"] + '/inscripciones'
    respuesta = requests.get(url, headers=headers)
    return jsonify(respuesta.json())

#######################
@app.route("/inscripciones/<string:id>",methods = ['GET'])
def mostrarInscripcion(id):
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-academico"] + '/inscripciones/'+id
    respuesta = requests.get(url, headers=headers)
    return jsonify(respuesta.json())
#########################
@app.route("/inscripciones/<string:id>/estudiante/<string:id_estudiante>/materia/<string:id_materia>",methods = ['PUT'])
def actualizarInscripcion(id,id_estudiante,id_materia):
    datosInscripcion = request.get_json()
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-academico"] + '/inscripciones/'+id+'/estudiante/'+id_estudiante+'/materia/'+id_materia
    respuesta = requests.put(url, json=datosInscripcion, headers=headers)
    return jsonify(respuesta.json())
##########################
@app.route("/inscripciones/<string:id>",methods =['DELETE'])
def eliminarInscripcion(id):
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-academico"] + '/inscripciones/' + id
    respuesta = requests.delete(url, headers=headers)
    return jsonify(respuesta.json())
##########################
@app.route("/inscripciones/materia/<string:id_materia>", methods =['GET'])
def inscritosMateria(id_materia):
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-academico"] + '/inscripciones/materia/'+id_materia
    respuesta = requests.get(url, headers=headers)
    return jsonify(respuesta.json())
##########################33
@app.route("/inscripciones/notas_mayores", methods =['GET'])
def notasMayores():
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-academico"] + '/inscripciones/nota_mayores'
    respuesta = requests.get(url, headers=headers)
    return jsonify(respuesta.json())
###########################
@app.route("/inscripciones/promedio/materia/<string:id_materia>", methods = ['GET'])
def promedioMateria(id_materia):
    headers = {"Content-Type": "application/json; charset = utf-8"}
    url = data["url-ms-academico"] + '/inscripciones/promedio/materia/'+id_materia
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