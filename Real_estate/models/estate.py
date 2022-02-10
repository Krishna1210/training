from attr import field
from odoo import fields, models, api
from odoo.exceptions import UserError


class Buyer_partner(models.Model):
    _inherit = 'res.partner'

    is_buyer = fields.Boolean(domain="[('is_buyer', '=', ['True'])]")


class estate_property(models.Model):
    _name = "estate.properties"
    _description = "estate property"
    _inherit = [
        'mail.thread',
        'mail.activity.mixin', ]

    def get_description(self):
        if self.env.context.get('is_my_property'):
            return self.env.user.name + '\'s property'

    name = fields.Char(default="Unknown")

    selling_price = fields.Float()
    bedrom = fields.Integer(default=2)
    postcode = fields.Char()
    image = fields.Image()
    date_availability = fields.Date(copy=False)
    expected_price = fields.Float(help="help")
    living_area = fields.Integer()
    garden_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    active = fields.Boolean(default=True)
    description = fields.Char(default=get_description)
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
    state = fields.Selection(
        [('new', 'New'), ('sold', 'Sold'), ('cancel', 'Cancel')], default="new")
    property_type_id = fields.Many2one('property.type')
    property_tag_id = fields.Many2many('estate.tag')
    property_offer_id = fields.One2many('estate.offer', 'property_id')
    offer_ids = fields.One2many(
        'estate.offer', 'property_id', 'property.type"')
    total_area = fields.Integer(
        compute="_total_area", inverse="_inverse_area", search="_search_area")
    best_offer = fields.Float(compute="_best_prize")
    buyer = fields.Many2one('res.partner')
    #date_availability = fields.Date()
    date_deadline = fields.Date()
    current_user = fields.Many2one(
        'res.users', 'Current User', default=lambda self: self.env.user, readonly=True)
    salesman_id = fields.Many2one('res.users')
    #p_name = fields.Char(related='offer_ids.partner_id.name', string="OFFER NAME")
   # partner = fields.Char(related='partner_ids.partner_id.name', string="partner")

    def _search_area(self, operator, value):
        self.env.cr.execute(
            "SELECT id from estate.properties where total_area::%s %s" % (operator, value))
        ids = self.env.cr.fetchall()
        return [('id', 'in', [id[0] for id in ids])]

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'west'
            else:
                record.garden_area = 0
                record.garden_orientation = None

    @api.depends('offer_ids.price')
    def _best_prize(self):
        for record in self:
            max_price = 0
            for offer in record.offer_ids:
                if offer.price > max_price:
                    max_price = offer.price
            record.best_offer = max_price

    @api.depends('garden_area', 'living_area')
    def _total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    def _inverse_area(self):
        for record in self:
            record.living_area = record.garden_area = record.total_area / 2

    # @api.constrains('garden_area', 'living_area')
    # def _check_garden_area(self):
    #     for record in self:
    #         if record.living_area >= record.garden_area:
    #             raise UserError("garden area must be bigger than living area")

    @api.constrains('expected_price')
    def _expectedprize(self):
        for record in self:
            if record.expected_price == 0:
                raise UserError("expected prize is not null")

    def action_sold(self):
        for record in self:
            if record.state == "cancel":
                raise UserError("Cancel property can not be sold")
            record.state = 'sold'

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold property can not be cancel")
            record.state = 'cancel'


class estate_property_type(models.Model):
    _name = "property.type"
    _description = "estate property type"

    name = fields.Char()
    property_ids = fields.One2many('estate.properties', 'property_type_id')
    offers = fields.One2many('estate.offer', 'property_type_id')


class estate_tag(models.Model):
    _name = 'estate.tag'
    _description = 'estate property tag'

    name = fields.Char()
    color = fields.Integer()

class estate_offer(models.Model):
    _name = 'estate.offer'
    _description = 'estate offer'

    name = fields.Char()
    price = fields.Float()
    status = fields.Selection(
        [('accepted', 'Accepted'), ('rejected', 'Rejected')])
    partner_id = fields.Many2one('res.partner')
    property_id = fields.Many2one('estate.properties')
    property_type_id = fields.Many2one(related='property_id.property_type_id')

    def action_accepted(self):
        for record in self:
            record.status = "accepted"

    def action_rejected(self):
        for record in self:
            record.status = "rejected"
