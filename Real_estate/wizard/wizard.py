from odoo import _, api, fields, models

class propertywizard(models.TransientModel):
    _name = 'property.wizard'

    partner_id= fields.Many2one("res.partner", "partner", required=True)
    price = fields.Char()
    status = fields.Selection(
        [('accepted', 'Accepted'), ('rejected', 'Rejected')])

    def partner(self):
        # print("rkgjle")
        self.ensure_one()
        Offer = self.env['estate.offer']
        activeIds = self.env.context.get('active_ids')
        data = {
            'price' : self.price,
            'partner_id' : self.partner_id.id,
            'status' : self.status
        }
        for property in self.env['estate.properties'].browse(activeIds):    
            ## Method 1
            # property.write({'property_offer_id' : [(0 ,0 ,data)]})

            ## Method 2
            data['property_id'] = property.id
            Offer.create(data)
    

