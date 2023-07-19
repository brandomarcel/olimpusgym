# Copyright (c) 2023, Brando Cevallos and contributors
# For license information, please see license.txt

import base64
import frappe
import qrcode
from datetime import date, datetime
from frappe.model.document import Document
import pyqrcode

@frappe.whitelist(allow_guest=True)
def updateCliente(datos):
    try:
        sql = """update tabCliente set  cedula='{1}',
                                        nombres='{2}',
                                        apellidos='{3}',
                                        apodo='{4}',
                                        celular='{5}',
                                        correo='{6}',
                                        nombres_completos='{7}',
                                        genero='{8}'
                where name = '{0}'""".format(datos["name"], datos["cedula"], datos["nombres"],
                                             datos["apellidos"], datos["apodo"], datos["celular"], datos["correo"],
                                             (datos["nombres"] + ' ' + datos["apellidos"]),datos["genero"])
        frappe.db.sql(sql, as_dict=True)
        retorno = {
            "estado": 'Exito',
        }
    except Exception as e:
        retorno = {
            "estado": 'Error',
            "mensajeError": e
        }
    return retorno


@frappe.whitelist(allow_guest=True)
def getClientes():
    sql = "select * from tabCliente order by creation DESC"
    return frappe.db.sql(sql, as_dict=True)

@frappe.whitelist(allow_guest=True)
def getAlldetalleClientes(name):
    doc = frappe.get_doc("Cliente", name, load_children=True)
    return doc


@frappe.whitelist(allow_guest=True)
def detalleCliente(name):
    sql = "select * from tabCliente where name = '{0}'".format(name)
    return frappe.db.sql(sql, as_dict=True)


""" @frappe.whitelist(allow_guest=True)
def borrarCliente(name):
    try:
        sql = "delete from tabCliente where name = '{0}'".format(name)
        frappe.db.sql(sql, as_dict=True)
        retorno = {
            "estado": 'Exito',
        }
    except Exception as e:
        retorno = {
            "estado": 'Error',
            "mensajeError": e
        }
    return retorno """

@frappe.whitelist(allow_guest=True)
def borrarCliente(name):
    try:
        frappe.delete_doc('Cliente', name,ignore_permissions=True)
        retorno = {
            "estado": 'Exito',
        }
    except Exception as e:
        retorno = {
            "estado": 'Error',
            "mensajeError": e
        }
    return retorno



@frappe.whitelist(allow_guest=True)
def estadoCliente(name):
    try:
        sql = """update tabCliente set  estado='Inactivo'
                where name = '{0}'""".format(name, )
        frappe.db.sql(sql, as_dict=True)
        retorno = {
            "estado": 'Exito',
        }
    except Exception as e:
        retorno = {
            "estado": 'Error',
            "mensajeError": e
        }
    return retorno


@frappe.whitelist(allow_guest=True)
def crearCliente(datos):
    # Cliente
    try:
        cliente = frappe.new_doc("Cliente")
        cliente.cedula = datos["cedula"]
        cliente.nombres = datos["nombres"]
        cliente.apellidos = datos["apellidos"]
        cliente.apodo = datos["apodo"]
        cliente.celular = datos["celular"]
        cliente.correo = datos["correo"]
        cliente.fecha_registro = datos["fecha_registro"]
        cliente.genero = datos["genero"]

        # Membresia
        cliente.append("membresia", {"fecha_inicio": datos["fecha_inicio"],
                                     "fecha_fin": datos["fecha_fin"],
                                     "tipo_membresia": datos["tipo_membresia"],
                                     "valor": datos["valor"],"tipo_pago": datos["tipo_pago"],
                                     "estado": 1
                                     })

        # Peso y Altura
        cliente.append("pesos", {"peso": datos["peso"],
                                 "altura": datos["altura"],
                                 "fecha": datos["fecha"],
                                 "imc": datos["imc"],
                                 "descripcion": datos["descripcion"],
                                 "sobrepeso": datos["sobrepeso"]
                                 })

        cliente.insert(ignore_permissions=True)
        retorno = {
            "estado": 'Exito',
            "cliente": cliente.name
        }
    except Exception as e:
        retorno = {
            "estado": 'Error',
            "mensajeError": e
        }

    return retorno

# MEMBRESIAS


@frappe.whitelist(allow_guest=True)
def getMembresias(todos):
    if todos:
        sql="""SELECT tm.name,tm.fecha_inicio,tm.tipo_membresia,tm.valor,tm.estado,tc.nombres_completos,tm.tipo_pago, MAX(tm.fecha_fin) AS fecha_fin
FROM tabMembresia tm inner join tabCliente tc on tm.parent = tc.name 
GROUP BY tm.parent
order by tm.creation DESC """
    else:

        sql = """select tm.name,tm.fecha_fin,tm.fecha_inicio,tm.tipo_membresia,tm.valor,tm.estado,tc.nombres_completos,tm.tipo_pago from tabMembresia tm  
inner join tabCliente tc on tm.parent = tc.name 
order by tm.creation DESC"""
    return frappe.db.sql(sql, as_dict=True)


@frappe.whitelist(allow_guest=True)
def crearMembresia(datos):
    # Cliente
    try:
        membresia = frappe.new_doc("Membresia")
        membresia.parent = datos["cliente"]
        membresia.parentfield = 'membresia'
        membresia.parenttype = 'Cliente'
        membresia.fecha_inicio = datos["fecha_inicio"]
        membresia.fecha_fin = datos["fecha_fin"]
        membresia.tipo_membresia = datos["tipo_membresia"]
        membresia.valor = datos["valor"]
        membresia.tipo_pago = datos["tipo_pago"]
        membresia.estado = 1
       

        membresia.insert(ignore_permissions=True)
        retorno = {
            "estado": 'Exito',
            "cliente": membresia.name
        }
    except Exception as e:
        retorno = {
            "estado": 'Error',
            "mensajeError": e
        }

    return retorno

@frappe.whitelist(allow_guest=True)
def deleteMembresia(name):
    try:
        sql = "delete from tabMembresia where name = '{0}'".format(name)
        frappe.db.sql(sql, as_dict=True)
        retorno = {
            "estado": 'Exito',
        }
    except Exception as e:
        retorno = {
            "estado": 'Error',
            "mensajeError": e
        }
    return retorno

# PESOS

@frappe.whitelist(allow_guest=True)
def createPeso(datos):
    
    try:
        peso = frappe.new_doc("Pesos")
        
        peso.parentfield = 'pesos'
        peso.parenttype = 'Cliente'
        peso.parent = datos["cliente"]
        peso.peso = datos["peso"]
        peso.altura = datos["altura"]
        peso.imc = datos["imc"]
        peso.descripcion = datos["descripcion"]
        peso.sobrepeso = datos["sobrepeso"]
        peso.fecha = datos["fecha"]
        
       

        peso.insert(ignore_permissions=True)
        retorno = {
            "estado": 'Exito',
            "cliente": peso.name
        }
    except Exception as e:
        retorno = {
            "estado": 'Error',
            "mensajeError": e
        }

    return retorno

@frappe.whitelist(allow_guest=True)
def deletePeso(name):
    try:
        sql = "delete from tabPesos where name = '{0}'".format(name)
        frappe.db.sql(sql, as_dict=True)
        retorno = {
            "estado": 'Exito',
        }
    except Exception as e:
        retorno = {
            "estado": 'Error',
            "mensajeError": e
        }
    return retorno


@frappe.whitelist(allow_guest=True)
def generarQR():
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data("CLI-2023-0504424987")
    url = pyqrcode.create("CLI-2023-0504424987", error='H', version=2)
    image_as_str = url.png_as_base64_str(scale=2, background=None, quiet_zone=4)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("CLI-2023-0504424987.png")
    with open("CLI-2023-0504424987.png", "rb") as image_file:
        try:
            formato = base64.b64encode(image_file.read())
            encoded_string =("La imagen está en formato Base64")
        except:
             encoded_string =("La imagen no está en formato Base64")
       
    return {'encoded_string':encoded_string,
            'formato':formato,
            'image_as_str':image_as_str}



class Cliente(Document):
    def before_insert(self):
        fecha_actual = date.today()
        self.estado = 'Activo'
        self.nombres_completos = self.nombres + ' ' + self.apellidos
        self.identificador = 'CLI-' + \
            str(fecha_actual.year)+'-' + self.cedula
