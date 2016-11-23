# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, fields, api,  _
from openerp.exceptions import Warning, ValidationError, except_orm

class res_country(models.Model):
    _inherit = 'res.partner'
    '''
        Sobreescribe el metodo para obtener nombres de los contactos solamente.
    '''
    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            name = record.name
            if record.parent_id and not record.is_company:
                name = "%s" % (name)
            if context.get('show_address_only'):
                name = self._display_address(cr, uid, record, without_company=True, context=context)
            if context.get('show_address'):
                name = name + "\n" + self._display_address(cr, uid, record, without_company=True, context=context)
            name = name.replace('\n\n','\n')
            name = name.replace('\n\n','\n')
            if context.get('show_email') and record.email:
                name = "%s <%s>" % (name, record.email)
            res.append((record.id, name))
        return res

class HorizontalCut(models.Model):
    _name = 'horizontal.cut'
    _description='Troquelado Horizontal'

    name = fields.Char(string="Troquelado horizontal",
        help='Este campo se utiliza para establecer el troquelado horizontal')
    height_id = fields.Float(digits=(3,2),string='ID Alto')

class PaperType(models.Model):
    _name = 'mrp.type.paper'
    _description = 'Tipo de papel'
    name = fields.Char(string='Tipo de papel')

class Gramaje(models.Model):
    _name = 'mrp.gramaje'
    _description='Gramaje'

    name = fields.Char(string="Gramaje",
        help='Este campo se utiliza para establecer el gramaje')
    paper_type_id = fields.Many2one(comodel_name='mrp.type.paper',
        string='Tipo de papel', )
    
class OriginalCopy(models.Model):
    _name= 'original.copy'
    _description= 'Especificaciones de Original y copias'


    Order_id = fields.Many2one('mrp.production', 'Orden de Produccion',required=1, ondelete='cascade')
    name= fields.Selection([('Original', 'Original'), ('Copia 1', 'Copia 1'), ('Copia 2', 'Copia 2'),('Copia 3','Copia 3'),
        ('Copia 4', 'Copia 4'),('Copia 5', 'Copia 5'),('Copia 6', 'Copia 6')],
        string='Vias')
    color_print = fields.Char(string='Anverso')
    color_paper = fields.Char(string='Color papel')
    purpose = fields.Char(string='Destino')
    reverse = fields.Char(string='Reverso')
    # reverse_point = fields.Char(related='mrp.production.preimp_ids')

class Preimpreso(models.Model):
    _name = 'mrp.preimpreso'
    _description = 'Preimpreso'
    
    name = fields.Char(string='Preimpreso')
     # Many2many inverse relation
    form_id = fields.Many2many('mrp.production',string='Preimpreso')
       
class MrpProduction(models.Model):
    # _name = 'mrp.production'
    _inherit = 'mrp.production'

    @api.onchange('partner')
    def _on_change_partner(self):
        self.partner_child_ids = False

    @api.onchange('via')
    def _on_change_name(self): 

        if self.via == 0:
            lines =[]
            self.update({'vias_lines':lines})
        elif self.via == 1:
            self.vias_lines = self.vias_lines.new({'name': 'Original','color_paper': 'Blanco'})
        elif self.via == 2:
            self.vias_lines = self.vias_lines.new({'name': 'Original' })
            self.vias_lines += self.vias_lines.new({'name': 'Copia 1' })
        elif self.via == 3:
            self.vias_lines = self.vias_lines.new({'name': 'Original' })
            self.vias_lines += self.vias_lines.new({'name': 'Copia 1' })
            self.vias_lines += self.vias_lines.new({'name': 'Copia 2' })
        elif self.via == 4:
            self.vias_lines = self.vias_lines.new({'name': 'Original' })
            self.vias_lines += self.vias_lines.new({'name': 'Copia 1' })
            self.vias_lines += self.vias_lines.new({'name': 'Copia 2' })
            self.vias_lines += self.vias_lines.new({'name': 'Copia 3' })
        elif self.via == 5:
            self.vias_lines = self.vias_lines.new({'name': 'Original' })
            self.vias_lines += self.vias_lines.new({'name': 'Copia 1' })
            self.vias_lines += self.vias_lines.new({'name': 'Copia 2' })
            self.vias_lines += self.vias_lines.new({'name': 'Copia 3' })
            self.vias_lines += self.vias_lines.new({'name': 'Copia 4' })
        elif self.via == 6:
            self.vias_lines = self.vias_lines.new({'name': 'Original' })
            self.vias_lines += self.vias_lines.new({'name': 'Copia 1' })
            self.vias_lines += self.vias_lines.new({'name': 'Copia 2' })
            self.vias_lines += self.vias_lines.new({'name': 'Copia 3' })
            self.vias_lines += self.vias_lines.new({'name': 'Copia 4' })
            self.vias_lines += self.vias_lines.new({'name': 'Copia 5' })
        elif self.via == 6:
            self.vias_lines = self.vias_lines.new({'name': 'Original' })
            self.vias_lines += self.vias_lines.new({'name': 'Copia 1' })
            self.vias_lines += self.vias_lines.new({'name': 'Copia 2' })
            self.vias_lines += self.vias_lines.new({'name': 'Copia 3' })
            self.vias_lines += self.vias_lines.new({'name': 'Copia 4' })
            self.vias_lines += self.vias_lines.new({'name': 'Copia 5' })
            self.vias_lines += self.vias_lines.new({'name': 'Copia 6' })
        else:
            lines =[]
            self.update({'vias_lines':lines})

    @api.onchange('type_work')
    def onchange_unid(self):
        if self.type_work == 'continuo':
            self.unid_width = 'pulg'
            self.unid_high = 'pulg'
        elif self.type_work == 'pliego':
            self.unid_width = 'cms'
            self.unid_high = 'cms'
        elif self.type_work == 'rollo':
            self.unid_width = 'mm'
            self.unid_high = 'mts'
        elif self.type_work == 'sobre':
            self.unid_width = 'cms'
            self.unid_high = 'cms'
        else:
            self.unid_width = ''
            self.unid_high = '' 
    
    @api.onchange('price_for','product_qty','box_cant','block_cant','unit_price')
    def onchange_unit_price(self):
        if self.price_for == 'millar':
            self.total_price = self.unit_price * (self.product_qty/1000)
        elif self.price_for == 'caja':
            self.total_price = self.unit_price * self.box_cant
        elif self.price_for == 'block':
            self.total_price = self.unit_price * self.block_cant
        elif self.price_for == 'unidad':
            self.total_price = self.unit_price * self.product_qty 

    @api.onchange('type_work')
    def onchange_type_work(self):
        if self.type_work == False:
          return {
            'warning': {
                'title': 'Advertencia!',
                'message': 'Debe seleccionar el tipo de trabajo'}
                }
    @api.one
    @api.constrains('type_work','width','height','cod_partner_product','nit_ci','street','phone')
    def _check_type_work_size(self):
        cad = ''
        if self.type_work == False:
            cad = 'Debe seleccionar el tipo de trabajo\n'
        if self.width == 0:
            cad += 'Debe ingresar el ancho del formulario\n'
        if self.height == 0:
            cad += 'Debe ingresar el alto del formulario'
        print str(len(self.cod_partner_product)) + 'holaaaaaaaaaaaa'
        if len(self.cod_partner_product) == 0:
            cad += 'Debe ingresar el código en el dato maestro del cliente\n'
        if len(self.nit_ci) == 0:
            cad += 'Debe ingresar el NIT en el dato maestro del cliente\n'
        if len(self.street) == 0:
            cad += 'Debe ingresar la dirección en el dato maestro del cliente\n'
        if len(self.phone) == 0:
            cad += 'Debe ingresar el teléfono en el dato maestro del cliente\n'


        if len(cad) >0:
            raise ValidationError(cad)

    def action_ok_customer(self):
        """ Approves customer production order.
        @return: Newly generated Shipment Id.
        """
        self.write({'state': 'approved_customer'})  
        return 0

    type_work = fields.Selection(
        [('continuo', 'Continuo'), ('pliego', 'Pliego o Plana'), ('rollo', 'Rollos'),('sobre','Sobres')],
        string='Tipo de trabajo',
        readonly=True, states={'draft': [('readonly', False)]},
        help='Este campo se utiliza para distinguir los tipos de trabajo.',
        default='continuo',
        required=True
        )
    # paper_type = fields.Selection(
    #     [('bond', 'Bond'), ('quimico', 'Quimico'), ('termico', 'Termico'),
    #     ('adhesivo','Adhesivo'),('cartulina','Cartulina'),('couche','Couche'),('copia','Copia'),('kraft','Kraft')],
    #     string='Tipo de papel',
    #     readonly=True, states={'draft': [('readonly', False)]},
    #     help='Este campo se utiliza para seleccionar el tipo de papel',
    #     required=True
    #     )
       
    paper_type= fields.Many2one(
        comodel_name='mrp.type.paper',string='Tipo de papel',
        required=True)

    # gramaje= fields.Char(string='Gramaje',related='mrp.gramaje.name',store=True,
    #     required=True)

    gramaje = fields.Many2one(
        comodel_name='mrp.gramaje',
        string='Gramaje')

    specification = fields.Char(string='Especificaciones')
    partner = fields.Many2one(
        comodel_name='res.partner', string='Empresa', store=True,
        required=True)

    cod_partner_product = fields.Char(string='Código',related='partner.codigo',store=True)
    nit_ci = fields.Char(string='NIT/CI', related='partner.nit',store=True)

    partner_child_ids = fields.Many2one(
        comodel_name='res.partner', string='Responsable Pedido',
        required=True)

    street = fields.Char(string='Dirección', related='partner.street',store=True)
    phone = fields.Char(string='Teléfono', related= 'partner.phone',store=True)
    date_order = fields.Date('Fecha pedido', default= fields.date.today())
    date_design = fields.Date('Fecha aprobado por cliente')  
    date_commit = fields.Date('Fecha estimada entrega')
    width = fields.Float(
        string='Ancho',digits=(3,2),
        help='Este campo se utiliza para ingresar el ancho del formulario',
        required=True)

    unid_width = fields.Selection(
         [('pulg', 'Pulgadas'),('cms', 'Centímetros'), ('mm', 'Milímetros')],
        string='Ancho Unidad de Medida', required=True,
        help='Este campo se utiliza para distinguir los tipos de trabajo.'
        )
    height = fields.Float(
        string='Alto',digits=(3,2),required=True,
        help='Este campo se utiliza para ingresar el alto del formulario')
    unid_high = fields.Selection(
         [('pulg', 'Pulgadas'),('cms', 'Centímetros'), ('mts', 'Metros')],
        string='Alto Unidad de Medida', required=True,
        help='Este campo se utiliza para distinguir los tipos de trabajo.'
        )
    via = fields.Integer(
        string='Vías',required=True,
        help='Este campo se utiliza para ingresar las vías del formulario')
    preimp_ids = fields.Many2many(
        'mrp.preimpreso',       # related= (model name)
        'mrp_preimpreso_rel',   # relation= (table name)
        'form_id',              # column1= ("this" field)
        'preimp_id',            # column2= ("other" field)
        string='Preimpreso',

        # Relational field attributes:
        auto_join=False,
        context="{}",
        domain="[]",
        ondelete='cascade',
        )
    troquel = fields.Boolean('Troquelado')
    separation = fields.Float(
        string='Separación (cm)',digits=(3,2),required=True,
        help='Este campo se utiliza para ingresar la separación')
    horizontal_cut = fields.Many2one(
        comodel_name= 'horizontal.cut', string="Troquelado horizontal")
    vertical_cut = fields.Boolean('Troquelado Vertical?')
    vertical_cut_type = fields.Selection(
        [('cruz','Cruz'),('especial','Especial')], 
        string='Tipo')
    numeration = fields.Boolean('Numeración')
    initial_number = fields.Integer(string='Numeración inicial', 
        help='Este campo se utiliza para ingresar la numeración inicial del formulario')
    end_number = fields.Integer(string='Numeración final',
        help='Este campo se utiliza para ingresar la numeración final del formulario')
    color_number= fields.Char(string='Color de numeración',
        help='Este campo se utiliza para ingresar el color de la numeración')
    binding = fields.Selection(
        [('engomado', 'Engomado'),('engrapado','Engrapado')],
        string="Encuadernación", help='Este campo se utiliza para ingresar el tipo de Encuadernación del formulario')
    engotam = fields.Boolean('Engomado Tamara')
    
    reel = fields.Selection(
        [('6','6 Dx'),('8','8 Dx"'),('72','72 Dx"')],
        string='Carretillas')
    catch = fields.Selection(
        [('6','6 Dx"'),('8','8 Dx"'),('72','72 Dx"')],
        string='Plecas')
    # paper_type= fields.Many2one(
    #     comodel_name='type.paper', string='Tipo de Papel')
   
    
    box_cant = fields.Integer(string='Cantidad cajas')

    block_cant_sel =fields.Selection(
         [('blocks', 'Blocks'),('talonarios','Talonarios'),('paquete','Paquete')],
        string="Cantidad blocks/talonarios/paquete")
    block_cant = fields.Integer(string='Cantidad blocks/talonarios/paquete')

    # block_set = fields.Integer(string='Juegos por block/talonario/paquete')
    block_set_sel =fields.Selection(
         [('blocks', 'Blocks'),('talonarios','Talonarios'),('paquete','Paquete')],
        string="Cantidad juegos por blocks/talonarios/paquete")
    block_set = fields.Integer(string='Juegos por')

    sheet_set_sel =fields.Selection(
         [('blocks', 'Blocks'),('talonarios','Talonarios'),('paquete','Paquete')],
        string="Cantidad hojas por blocks/talonarios/paquete")
    sheet_set = fields.Integer(string='Hojas por')   
    note = fields.Text(string='Observaciones')
    costing = fields.Char(string='Costeo No.')
    price_for= fields.Selection(
        [('millar', 'Millar'),('caja','Caja'),('block','Block'),('unidad','Unidad')],
        string="Precio por",
        required=True)
    unit_price= fields.Float('Precio Unitario', (3, 2))
    total_price= fields.Float('Precio Total',(3,2))
    metho_pay= fields.Char(string='Forma de pago',
        required=True)
    
    # DIAGRAMACIÓN
    date_entry = fields.Datetime('Fecha y hora ingreso') 
    date_entry_s = fields.Datetime('Fecha y hora ingreso')
    date_delivery = fields.Datetime('Fecha y hora entrega')
    date_delivery_s = fields.Datetime('Fecha y hora entrega')
    note_diagram = fields.Text('Otros')
    
    # Caracteristicas tecnicas para produccion
    plaque = fields.Char(string='Placa')
    box = fields.Char(string='Cajas')
    cone = fields.Char(string='Conos')
    other = fields.Char(string='Otros')
    
    inst_esp = fields.Text(string='Instrucciones especiales')

    vias_lines = fields.One2many(comodel_name='original.copy',inverse_name='Order_id',string='lineas vias')
    state = fields.Selection(
            [('draft', 'New'), ('cancel', 'Cancelled'),
            ('diagramming', 'Diagramming'),
            ('approved_customer', 'Ok Customer'),
            ('confirmed', 'Planning'),
            ('ready', 'Ready to Produce'), 
            ('in_production', 'Production Started'), 
            ('done', 'Done')],
            string='Status', readonly=True,
            track_visibility='onchange', copy=False,
            help="When the production order is created the status is set to 'Draft'.\n\
                If the order is confirmed the status is set to 'Waiting Goods'.\n\
                If any exceptions are there, the status is set to 'Picking Exception'.\n\
                If the stock is available then the status is set to 'Ready to Produce'.\n\
                When the production gets started then the status is set to 'In Production'.\n\
                When the production is over, the status is set to 'Done'.")

    raw_material_lines = fields.One2many(comodel_name='mrp.raw.material',inverse_name='ord_id',string='Materia Prima')
