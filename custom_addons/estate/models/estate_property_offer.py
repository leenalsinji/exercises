from datetime import timedelta
from xml.dom import ValidationErr
from odoo import api, fields, models, exceptions
from odoo.exceptions import UserError  

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer" 
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float()
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property")
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status",
        copy=False,
        default=False,
    )       
    property_type_id = fields.Many2one(
      "estate.property.type", 
      related="property_id.property_type_id", 
      string="Property Type", 
      store=True
    )
    user_id = fields.Many2one(
    "res.users", 
    string="Offer Creator", 
    default=lambda self: self.env.user,
    required=True
)

    # Computed field with Inverse
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            # Fallback to today if record isn't saved yet
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = base_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            # Updating validity based on the manually picked date
            record.validity = (record.date_deadline - base_date).days

    def action_accept(self):
        for record in self:
            if "accepted" in record.property_id.offer_ids.mapped("status"):
                  raise UserError("An offer has already been accepted for this property!")
            record.status = "accepted"
            if record.user_id:
                 record.property_id.buyer_id = record.user_id.partner_id   
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"
        # Reject others
        other_offers = record.property_id.offer_ids - record
        other_offers.write({'status': 'refused'})
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
    #sql Constraints
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.'),
        ('check_unique_partner_offer', 'UNIQUE(property_id, partner_id)', 
         'This partner has already made an offer for this property!')
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            prop = self.env['estate.property'].browse(vals['property_id'])
            if vals.get('price') < prop.best_price:
                raise exceptions.UserError("The offer must be higher than the current best offer!"+ str(prop.best_price))            
            prop.state = 'offer_received'
        return super().create(vals_list)
    
    @api.constrains('user_id', 'property_id')
    def _check_different_creator(self):
      for record in self:
        other_offers = record.property_id.offer_ids - record
        if other_offers:
            last_creator = other_offers[0].user_id
            if record.user_id == last_creator:
                raise UserError("The person entering this offer must be different from the person who entered the previous offer!")


    

