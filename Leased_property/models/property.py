from attr import field
from odoo import fields, models, api
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
class leased_property(models.Model):
    _name = 'leased.property'
    _inherit = 'estate.properties'

    name=fields.Char()
    partner_id  = fields.Many2one('res.partner')
   

class leased_propertys(models.Model):
    _name = 'leas.propertys'
    _inherits = {'res.partner':'partner_id' , 'property.type':'property_type_id'}
    partner_id  = fields.Many2one('res.partner')
    property_type_id = fields.Many2one('property.type')
    name = fields.Char()
    #property_offer_id =  fields.One2many('estate.offer')
   
    start_Date = fields.Date(default=lambda self: fields.Datetime.now() , copy=False)
    date_deadline = fields.Date()
    lease_duration = fields.Float()


    @api.onchange('start_Date')
    def _onchange_start_date(self):
        for record in self:
            record. date_deadline = record.start_Date + relativedelta(days=30)
