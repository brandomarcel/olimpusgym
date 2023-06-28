# Copyright (c) 2023, Brando Cevallos and contributors
# For license information, please see license.txt

import frappe
from datetime import date, datetime
from frappe.model.document import Document


@frappe.whitelist(allow_guest=True)
def getClientes():
    sql = "select * from tabCliente"
    return frappe.db.sql(sql, as_dict=True)


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

        # Membresia
        cliente.append("membresia", {"fecha_inicio": datos["fecha_inicio"],
                                "fecha_fin": datos["fecha_fin"],
                                "tipo_membresia": datos["tipo_membresia"],
                                "valor": datos["valor"]
                                })

        # Peso y Altura
        cliente.append("pesos", {"peso": datos["peso"],
                                "altura": datos["fecha_fin"]
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


class Cliente(Document):
    def before_insert(self):
        fecha_actual = date.today()
        self.estado = 'Activo'
        self.nombres_completos = self.nombres + ' ' + self.apellidos
        self.identificador = 'CLI-' + \
            str(fecha_actual.year)+'-' + self.cedula
