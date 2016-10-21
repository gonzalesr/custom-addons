# -*- coding: utf-8 -*-

from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from openerp import api, fields, models, _
from openerp.exceptions import  ValidationError, Warning
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF

class ExchangeRate(models.Model):
    """ Clase para tipo de cambio de dolar americano 
    """
    _name = 'account.asset.exchange.rate'
    _description = 'Tipo de cambio para Activos Fijos'
    _order = 'name DESC'

    @api.one
    @api.constrains('name')
    def _check_unique_date_change_type(self):
        if len(self.search([('name', '=', self.name)])) > 1:
            raise ValidationError(_(
                'Advertencia!\n La fecha (%s) ingresada ya está registrada.') % self.name)
    
    name = fields.Date(
        string='Fecha',
        required=True,
        readonly=False,
        index=False,
        default=fields.date.today(),
        help="Fecha de tipo de cambio"
    )
    change_type = fields.Float(
        string='Tipo de cambio',
        required=True,
        readonly=False,
        index=False,
        default=0.0,
        digits=(16, 2),
        help='Este cambio es para ingresar el tipo de cambio correspondiente a esa fecha'
    )