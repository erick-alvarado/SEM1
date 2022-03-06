
from flask import Flask, jsonify,redirect,url_for,request, render_template,Response
import json
import requests
import mysql.connector
import tinys3
import base64


S3_ACCESS_KEY = 'AKIAXUSLBHHVKZ7OMR7L'
S3_SECRET_KEY = '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'
conn = tinys3.Connection(S3_ACCESS_KEY,S3_SECRET_KEY,endpoint='s3-us-east-1.amazonaws.com')


app=Flask(__name__)

@app.route('/login',methods=['POST'])
def login():        
        userToLog={
                'usuario':request.json['usuario'],
                'contrasenia':request.json['contrasenia']
        }
        answer=executequery("SELECT * FROM usuario Where usuario=%(usuario)s AND contrasena=%(contrasenia)s",userToLog)
        if len(answer)==1:
            return  jsonify({'id_user':answer[0][0]})
        return jsonify({'id_user':-1})

@app.route('/crear-album',methods=['POST'])
def crear_album():        
        album={
                'id_user':request.json['id_user'],
                'nombre_album':request.json['nombre_album']
        }
        answer=executequery("INSERT INTO album(nombre,idusuario) VALUES ( %(nombre_album)s,  %(id_user)s ) ",album)
        answer=executequery("SELECT * FROM album WHERE nombre=%(nombre_album)s AND idusuario=%(id_user)s",album)
        albumcreado={
                'id_album':answer[0][0]
        }
        return jsonify(albumcreado)

@app.route('/obtener-albumes',methods=['POST'])
def obtener_albumes():   
        album={
                'id_user':request.json['id_user']
        }
        answer=executequery("SELECT * FROM  album WHERE idusuario=%(id_user)s ",album)
        arregloalbumes=[]
        for (idalbum,nombre,idusuario) in answer:
                arregloalbumes.append({"idalbum":idalbum,"idusuario":idusuario,"nombre":nombre})
        return jsonify(arregloalbumes)

@app.route('/modificar-album',methods=['PUT'])
def modificar_album():        
        albumToUpdate={
                'id_user':request.json['id_user'],
                'id_album':request.json['id_album'],
                'nombre_album':request.json['nombre_album']
        }
        answer=executequery("UPDATE album SET   nombre= %(nombre_album)s WHERE idusuario=%(id_user)s AND idalbum=%(id_album)s ",albumToUpdate)
        return jsonify({'Message':'Album Editado','Code':1})

@app.route('/ver-fotos-album',methods=['POST'])
def ver_fotos_album():   
        iduserfotos={
                'id_user':request.json['id_user']
        }
        answer=executequery("SELECT * FROM  album INNER JOIN foto ON album.idalbum=foto.idalbum WHERE album.idusuario=%(id_user)s ",iduserfotos)
        arregloalbumes=[]
        for (idalbum,nombre,idusuario,idfoto,idalbum,url) in answer:
                arregloalbumes.append({"idalbum":idalbum,"idusuario":idusuario,"nombre":nombre,"url":url})
        return jsonify(arregloalbumes)

@app.route('/eliminar-album',methods=['DELETE'])
def eliminar_album():        
        albumToDelete={
                'id_user':request.json['id_user'],
                'id_album':request.json['id_album']
        }
        answer=executequery("DELETE FROM foto WHERE idalbum= %(id_album)s",albumToDelete)
        answer=executequery("DELETE FROM album WHERE idalbum= %(id_album)s",albumToDelete)
        return jsonify({'Message':'Album eliminado','Code':1})

@app.route('/obtener-perfil',methods=['POST'])
def obtener_perfil():   
        perfil={
                'id_user':request.json['id_user']
        }
        answer=executequery("SELECT * FROM usuario Where idusuario=%(id_user)s",perfil)
        for (idusuario, usuario,contrasena,nombre)  in answer:
                perfil['usuario']=usuario
                perfil['nombre']=nombre
        answer=executequery("SELECT * FROM album WHERE nombre='Foto_Perfil' AND idusuario=%(id_user)s",perfil)
        album={
                'id_album':answer[0][0]
        }
        answer=executequery("SELECT url, MAX(idfoto) as idfoto FROM foto WHERE  idalbum=%(id_album)s GROUP BY url",album)
        for (url, idfoto)  in answer:
                perfil['foto']=url#Obtener la foto de bucket s3

        return jsonify(perfil)

@app.route('/register',methods=['POST'])
def register():        
        user={
                'usuario':request.json['usuario'],
                'nombre_completo':request.json['nombre_completo'],
                'contrasenia':request.json['contrasenia'],
                'foto':request.json['foto'],
                'id_usuario':-1
        }
        answer=executequery("SELECT * FROM usuario Where usuario=%(usuario)s",user)
        if len(answer)==1:
            return  jsonify({'Message':'usuario ya existe utilice otro nombre de usuario','Code':-1})

        answer=executequery("INSERT INTO usuario(usuario,contrasena,nombre) VALUES ( %(usuario)s, %(contrasenia)s, %(nombre_completo)s ) ",user)
        answer=executequery("SELECT * FROM usuario Where usuario=%(usuario)s",user)
        user['id_usuario']=answer[0][0]

        answer=executequery("INSERT INTO album(nombre,idusuario) VALUES ( 'Foto_Perfil',  %(id_usuario)s ) ",user)
        answer=executequery("SELECT * FROM album WHERE nombre='Foto_Perfil' AND idusuario=%(id_usuario)s",user)
        album={
                'id_album':answer[0][0],
                'foto':request.json['foto']
        }
        # msg=""
        # try:
        #         msg = base64.b64decode(request.json['foto'])
        # except:
        #         msg=""
        
        answer=executequery("INSERT INTO foto(idalbum,url) VALUES ( %(id_album)s,  %(foto)s ) ",album)
        
        
        return jsonify({'Message':'Usuario Creado Correctamente','Code':1})
        


@app.route('/editar-perfil',methods=['PUT'])
def editar_perfil():        
        userUpdate={
                'id_user':request.json['id_user'],
                'usuario':request.json['usuario'],
                'nombre_completo':request.json['nombre_completo'],
                'contrasenia':request.json['contrasenia'],
                'foto':request.json['foto']
        }
        return jsonify(userUpdate)
        #'INSERT  Usuario SET '


@app.route('/subir-foto',methods=['POST'])
def subir_foto():        
        foto={
                'id_user':request.json['id_user'],
                'id_album':request.json['id_album'],
                'foto':request.json['foto']
        }
        answer=executequery("INSERT INTO foto(idalbum,url) VALUES ( %(id_album)s,  %(foto)s ) ",foto)
        #cargar al bucket y devolver
        return jsonify(foto)


@app.route('/add',methods=['POST'])
def tod():
        item_doc={
                'autor':request.json['autor'],
                'nota':request.json['nota']
        }
        urla='http://34.86.89.112:5000/add'
        urlb='http://34.86.153.141:5000/add'
        urlfinal=urla
        datosa=requests.get('http://34.86.89.112:5000/ramcpu',headers=request.headers)
        datosb=requests.get('http://34.86.153.141:5000/ramcpu',headers=request.headers)
        
        arr=json.loads(datosa.text)
        arr2=json.loads(datosb.text)

        num=getfinalurl(arr,arr2)
        if num==1:
            urlfinal=urlb
        resp = requests.post(urlfinal, json=item_doc,headers=request.headers)
        return  jsonify({"message":resp.text })

def executequery(query,params):
    mydb = mysql.connector.connect(
            host="database-1.ct4jfvgo8r4m.us-east-1.rds.amazonaws.com",
            user="admin",
            password="admin12345",
            database="sys"
    )
    cursor=mydb.cursor()
    cursor.execute((query), params)
    all=""
    try:
        all=cursor.fetchall()
    except:
        all=""
    mydb.commit()
    cursor.close()
    mydb.close()
    return all

def getfinalurl(arr,arr2):
    if arr['cantidad']>arr2['cantidad']:
        return 1
    elif arr['cantidad']<arr2['cantidad']:
        return 0
    if arr['ram']>arr2['ram']:
        return 1
    elif arr['ram']<arr2['ram']:
        return 0
    if arr['cpu']>arr2['cpu']:
        return 1
    elif arr['cpu']<arr2['cpu']:
        return 0
    return 0
if __name__=="__main__":
        app.run(host='0.0.0.0',debug=True,port=3000)
# pip install flask
# pip install requests
# pip install mysql-connector-python |pip install mysql-connector-python-rf
#pip install tinys3

