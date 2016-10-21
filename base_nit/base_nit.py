#-*- coding: utf-8 -*-
from openerp import models, fields, api

class res_partner(models.Model):
    """agrega campos a cliente"""
    _inherit = 'res.partner'

    nit = fields.Char('NIT/CI', size=15, help="NIT Número de Identificación Tributaria", required=True)
    codigo = fields.Char('Código', size=20, help="Código de Sistema SAI", required=True)
   
