# -*- coding: utf-8 -*-

from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from openerp import api, fields, models, _
from openerp.exceptions import  ValidationError, Warning
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF


class CostCenter(models.Model):
    """clase para registro de centro de costos, Administración, Comercialización, Producción"""
    _name = 'account.asset.cost.center'
    _description = 'Centro de costo'

    code = fields.Char(string='Código', required= True)
    name = fields.Char(string='Nombre', required= True)

class Office(models.Model):
    """ Clase para representar oficinas o sucursales de la empresa, Santa Cruz, La Paz, Cochabamba
    """
    _name = 'account.asset.office'
    _description = 'Company Office'

    _rec_name = 'name'
    _order = 'name ASC'

    code = fields.Char(string='Código', required=True,select=True)
    name = fields.Char(string='Name',required=True)
    description = fields.Text(string='Descripción')

class Area(models.Model):
    _name = 'account.asset.area'
    _description = "Company Area"

    @api.one
    @api.constrains('code')
    def _check_unique_constrains(self):
        if len(self.search([('code', '=', self.code)])) > 1:
#            raise ValidationError("Code already exists and violates unique field constraint")
            raise ValidationError(_(
                'Advertencia!\n El código (%s) ingresado está duplicado.') % self.code)

    code = fields.Char(required=True, string="Código")
    name = fields.Char(required=True, string="Nombre")
    active = fields.Boolean(string="Activo", default=True)
    note = fields.Text(string="Observacion")
    office_id = fields.Many2one(comodel_name='account.asset.office',string='Oficina', ondelete='restrict')
    cost_center_id = fields.Many2one(comodel_name='account.asset.cost.center',string='Centro de Costo', ondelete='restrict')
    responsable_id = fields.Many2one(comodel_name='asset.responsable',string='Responsable', ondelete='restrict')
    
class Responsable(models.Model):
    _name = 'asset.responsable'
    _description = "Responsable"

    name = fields.Char(required=True, string="Nombre")
    area_id = fields.Many2one(comodel_name='account.asset.area', string='Área', required=True)
    position = fields.Char(string="Cargo")
    ci = fields.Char(string="CI") 
    issued = fields.Selection([('CHQ','CHQ'),('LPZ','LPZ'),('CBB','CBB'),('ORU','ORU'),('PTS','PTS'),
    ('TAR','TAR'),('SCZ','SCZ'),('BEN','BEN'),('PAN','PAN'),('OTR','OTR')],string='Expedido') 
    status = fields.Boolean(string='Activo', default=True) 

class account_asset_category(models.Model):
    _name = 'account.asset.category'
    _description = 'Asset category'
    _inherit = 'account.asset.category'
 
    @api.one
    @api.constrains('code')
    def _check_unique_constrains(self):
        if len(self.search([('code', '=', self.code)])) > 1:
            raise ValidationError(_(
                'Advertencia!\n El código (%s) ingresado está duplicado.') % self.code)

    code = fields.Char(string='Código', required=True)
    abbreviation = fields.Char(string='Abreviación', required=True)
    depreciate = fields.Boolean(string='Deprecia',default=True)
    actualize = fields.Boolean(string='Actualiza',default=True)

class AuxiliaryGroup(models.Model):
    _name = 'account.asset.auxiliary.group'
    _description = 'Auxiliary Group'
    _order = 'code ASC'

    @api.one
    @api.constrains('code')
    def _check_unique_constrains(self):
        if len(self.search([('code', '=', self.code)])) > 1:
            raise ValidationError(_(
                'Advertencia!\n El código (%s) ingresado está duplicado.') % self.code)

    code = fields.Char(string='Código', required=True)
    name = fields.Char(string='Nombre', required=True)
    category_id = fields.Many2one('account.asset.category', 'Grupo Contable', required=False )

class Ufv(models.Model):
    _name = 'account.asset.ufv'   
    _description = 'Indice UFV'
    _order = 'name DESC'

    @api.one
    @api.constrains('name')
    def _check_unique_date_ufv(self):
        if len(self.search([('name', '=', self.name)])) > 1:
            raise ValidationError(_(
                'Advertencia!\n La fecha (%s) ingresado está duplicado.') % self.name)

    ufv = fields.Float(
        string='Indice UFV',digits=(3,5),
        help='Este campo se utiliza para ingresar el índice de Unidad de Fomento a la Vivienda') 
    name = fields.Date(string='Fecha')

class AccountAssetAsset(models.Model):
    _name = 'account.asset.asset'
    _description = 'Asset/Revenue Recognition/Fixeds Asset'
    _inherit = 'account.asset.asset'
    
    '''obtiene el porcentaje de depreciación según los años de vida del activo fijo'''
    @api.onchange('year_life')
    def _on_change_year_life(self):
        if self.year_life == 0 :
            return
        self.rate_depreciate = 100 / self.year_life 
    
    '''calcula el factor actual'''
    @api.onchange('ufv','ufv_actual')
    def _on_change_factor_actual(self):
        if self.ufv != 0:
            self.actual_factor = self.ufv_actual / self.ufv 
        else:
            self.actual_factor = 0

    '''calcula el valor actual'''
    @api.onchange('actual_factor','purchase_value')
    def _on_change_valor_actual(self):
        self.actual_value = self.purchase_value * self.actual_factor
     #   print self.purchase_value
      #  print self.actual_factor

    '''obtiene la ufv desde bd correspondiente a la fecha de incorporación'''
    @api.onchange('purchase_date')
    def _on_change_ufv(self):
      #  print self.env['account.asset.ufv']
        ufv_obj = self.env['account.asset.ufv'].search([['name', '=', self.purchase_date]])
        self.ufv = ufv_obj.ufv
    
    '''obtiene la ufv desde bd de la fecha actual'''
    @api.onchange('date_actual')
    def _on_change_ufv_actual(self):
        ufv_obj = self.env['account.asset.ufv'].search([['name', '=', self.date_actual]])
        self.ufv_actual = ufv_obj.ufv

    '''obtiene la depreciación de gestión en funcion del (valor actual/total meses) * meses en años'''
    @api.onchange('actual_value')
    def _on_change_dep_gestion(self):
        formato_fecha = "%Y-%m-%d"
        fecha_inicial = datetime.strptime(self.purchase_date, formato_fecha)
        fecha_final = datetime.strptime(self.date_actual, formato_fecha)
      #  print("Diferencia: ", diferencia.days, " días")
        if fecha_inicial.year != fecha_final.year:
            fecha_inicial = datetime.strptime(str(date.today().year) + '-01-01', formato_fecha)
        diferencia = (fecha_final - fecha_inicial).days
        print diferencia
        print self.year_life
        if self.year_life != 0:
            self.dep_gestion = (self.actual_value / self.year_life) * (float(diferencia) / 365)
            print 'VALOR ACTUAL : ' + str(self.actual_value / self.year_life)
            print 'DIFERENCIA ENTRE 365 : ' + str(float(diferencia) / 365)
        else:
            self.dep_gestion = 10201
            print self.dep_gestion
            print 'adiosssss'

    @api.onchange('purchase_value','exchange_type')
    def _on_change_actualize_cost_usd(self):
        self.initial_cost_usd = self.purchase_value * self.exchange_type

    #This function automatically sets the currency to EUR.
    def _get_default_ufv(self, cr, uid, context=None):
        res = self.pool.get('account.asset.ufv').search(cr, uid, [('name','=',self.purchase_date)], context=context)
        return res and res[0] or False

    @api.model
    def _default_type_exchange(self):
        tipo_cambio_obj = self.env['account.asset.exchange.rate'].search([], limit=1)
        print tipo_cambio_obj
        return tipo_cambio_obj

    @api.onchange('category_id','area_id','auxiliary_group_id','year_life')
    def _on_change_generate_code(self):
        '''Genera el codigo de activo fijo en funcion a la siguiente nomenclarua
            MU–01-02-003-001  donde:
            MU  Abreviatura Cuenta contable
            01  codigo centro de costo
            02  codigo ubicacion fisica
            003 codigo del activo CODIGO DEL GRUPO AUXILIAR
            001 numero correlativo del activo 
        '''
        accounting_account = 'CC'
        cost_center = '99'
        physical_location = '88'
        id_auxiliary_group = '777'
        correlative_number_asset = '666'
        if self.category_id and self.area_id and AuxiliaryGroup:
            ac_obj = self.env['account.asset.category'].search([['id', '=', int(self.category_id)]])
            accounting_account = ac_obj.abbreviation
            cc_obj = self.env['account.asset.cost.center'].search([['id','=',int(self.area_id.cost_center_id)]])
            cost_center = cc_obj.code
            uf_obj = self.env['account.asset.area'].search([['id','=',int(self.area_id)]])
            physical_location = uf_obj.code
            id_auxiliary_group = str(self.auxiliary_group_id.code).zfill(3)
           
            #search_ids = self.search([])
            #self.env.cr.execute('SELECT ID FROM Account_asset_asset ORDER BY ID DESC LIMIT 1')
            #code_assets = str(self.env.cr.fetchone()[0] + 1).zfill(3)
            code_auxiliary_group = int(self.auxiliary_group_id)
            self.env.cr.execute('SELECT code_correlative_asset,name FROM Account_asset_asset '
                                'WHERE auxiliary_group_id = %s '
                                'ORDER BY code_correlative_asset DESC LIMIT 1', (code_auxiliary_group,))
            res = self.env.cr.fetchone()
            if res:
                self.code_correlative_asset = int(res[0]) + 1
            else:
                 self.code_correlative_asset = 1
            
            correlative_number_asset = str(self.code_correlative_asset).zfill(3)

                        
            #correlative_number_asset = self.env['account.asset.auxiliary.group'].search([['id','=',int(self.auxiliary_group_id)]]).code
            self.code = accounting_account + cost_center + physical_location +  id_auxiliary_group + correlative_number_asset

       # print accounting_account + '-' + cost_center + '-' + physical_location + '-' + code_assets + '-' + correlative_number

    code =fields.Char('Codigo', size=32, readonly=True, states={'draft':[('readonly',False)]}, default='MU-01-01-003-001') 
    code_correlative_asset = fields.Char('Código correlativo') 
    code_sai = fields.Char(string = 'Código SAI')
    description = fields.Char(string= 'Descripción')
    brand = fields.Char(string='Marca')
    model = fields.Char(string='Modelo')
    color = fields.Char(string='Color')
    serial_number = fields.Char(string='Nro. Serial')
    '''Este campo es representado por purchase_date, field nativo de odoo,
    incorporation = fields.Date(string = 'fecha de incorporacion') '''
    state_asset = fields.Selection(
        [('bueno', 'Bueno'), ('regular', 'Regular'), ('malo', 'Malo')],
        string='Estado activo',
        help='Este campo se utiliza para asignar el estado/condiciones fìsicas del Activo Fijo.',
        default='bueno'
        )
    
    fecha_usd = fields.Many2one(comodel_name='account.asset.exchange.rate', 
        string='Grupo Auxiliar', ondelete='restrict',default=_default_type_exchange)
    exchange_type = fields.Float(string='Tipo de cambio',related='fecha_usd.change_type', store=True, readonly=True)
    initial_cost_usd = fields.Float(string='Costo en $us')
    init_acum_depre = fields.Float(string='Dep Acum Inicial')
    actual_factor = fields.Float(string='Factor Actual',digits=(4, 6),readonly=True)
    actual_value = fields.Float(string='Valor Actual')
    warranty= fields.Integer(string='Garantía (mes)')
    year_life = fields.Integer(string='Vida Útil en años',related='category_id.method_number', store=True)
    day_life = fields.Integer(string='Días')
    depreciate = fields.Boolean(string='Depreciar')
    actualize = fields.Boolean(string='Actualizar')
    rate_depreciate = fields.Float(string='% Depreciación')
    dep_gestion = fields.Float(string='Dep. Gestion')
    dep_acumulada = fields.Float(string='Dep. Acumulada')
    valor_neto = fields.Float(string='Valor neto')
    
    '''datos de compra'''
    number_invoice = fields.Char(string='Número de Factura')
    purchase_date_invoice = fields.Date(string='Fecha de compra', default=fields.date.today(),
            help="Este campo es para introducir la fecha de compra")
    # change_type_id = fields.Many2one(
    #     string='Tipo de Cambio',
    #     required=True,
    #     readonly=False,
    #     comodel_name='account.asset.exchange.rate',
    #     ondelete='restrict')
    ufv = fields.Float(string='UFV', digits=(8, 5),readonly=True,
        help='Este campo visualiza el indice correspondiente a la fecha de incorporación')
    ufv_actual = fields.Float(string='UFV actual', digits=(8,5), help='Indice UFV actual',readonly=True)
    date_actual= fields.Date(string='Calculados a fecha',default=fields.date.today())
    auxiliary_group_id = fields.Many2one(comodel_name='account.asset.auxiliary.group', string='Grupo Auxiliar', ondelete='restrict')
    area_id = fields.Many2one(comodel_name='account.asset.area', string='Área', ondelete='restrict')    
    responsable_id = fields.Many2one(comodel_name='asset.responsable',string='Responsable', ondelete='restrict')
    position = fields.Char(string='Cargo', related='responsable_id.position')
