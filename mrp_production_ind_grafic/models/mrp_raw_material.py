# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, fields, api,  _
from openerp.exceptions import Warning, ValidationError, except_orm


class RawMaterial(models.Model):
    _name= 'mrp.raw.material'
    _description= 'Dato y caracterisiticas técnicas para producción - Materia Prima'

    @api.onchange('kg','percentage','demasia')
    def onchange_percentaje(self):
        self.total = ((self.kg * (self.percentage / 100)) + self.kg)
        self.demasia = self.kg * (self.percentage/100)

    ord_id = fields.Many2one('mrp.production', 'Orden de Produccion',required=1, ondelete='cascade')
    name= fields.Selection([('Bond', 'Bond'), ('Termico', 'Térmico'), ('Q-CB', 'Q - CB'),('Q-CF','Q-CF'),
        ('Q-CFB', 'Q-CFB')],
        string='Tipo Papel')
    kg = fields.Integer(
        string='KG  ',required=False)
    percentage = fields.Float(
        string='% Demas',digits=(6,2),required=False)
    demasia = fields.Integer(
        string='Demasia',required=False)    
    total = fields.Integer(
        string='Total',required=False)
    paper_processing = fields.Integer(
        string='Papel Procesado',required=False)
    total_load = fields.Integer(
        string='Carga Total',required=False)
    coil_width = fields.Float(
        string='Ancho de Bobina',digits=(6,2),required=False)
    high_form = fields.Float(
        string='Alto Formulario',digits=(6,2),required=False)
    unid_high_form = fields.Selection([('pulg','Pulgadas'),('cm','Cm')], string='Unidad')
    armed = fields.Integer(string='Armado',required=False)