from datetime import timedelta
from odoo import api, fields, models, exceptions

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
            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
    #sql Constraints
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            prop = self.env['estate.property'].browse(vals['property_id'])
            if vals.get('price') < prop.best_price:
                raise exceptions.UserError("The offer must be higher than the current best offer!"+ str(prop.best_price))            
            prop.state = 'offer_received'
        return super().create(vals_list)
    
    property_type_id = fields.Many2one(
      "estate.property.type", 
      related="property_id.property_type_id", 
     string="Property Type", 
     store=True
    )
    

