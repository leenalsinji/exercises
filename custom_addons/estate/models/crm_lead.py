from odoo import models, api

class CrmLead(models.Model):
    _inherit = "crm.lead"


    @api.model
    def get_stats(self):
    # We use the 'estate.property' model which you already created
        Property = self.env['estate.property']
    
        return {
            "total_properties": Property.search_count([]),
            "available_properties": Property.search_count([('state', 'in', ['new', 'offer_received'])]),
            "average_price": sum(Property.mapped('expected_price')) / (Property.search_count([]) or 1),
    }