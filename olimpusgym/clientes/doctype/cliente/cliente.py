# Copyright (c) 2023, Brando Cevallos and contributors
# For license information, please see license.txt

import frappe
from datetime import date, datetime
from frappe.model.document import Document

class Cliente(Document):
    def before_insert(self):
        fecha_actual = date.today()
        self.estado = 'Activo'
        self.nombres_completos = self.nombres+' '+self.apellidos
        self.identificador = 'CLI-' + \
        str(fecha_actual.year)+'-'+ self.cedula
