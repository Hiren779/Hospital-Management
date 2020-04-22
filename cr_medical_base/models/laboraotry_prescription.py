from odoo import fields, models,api
from datetime import date

class laboratoryPrescription(models.Model):
    _name = "laboratory.prescription"
    _description = "laboratory prescription Details"

    @api.model  # seq
    def create(self, vals):
        res = super(laboratoryPrescription, self).create(vals)
        vals['name'] = self.env['ir.sequence'].next_by_code('LaboratoryPrescription')
        res.name = vals['name']
        return res

    name = fields.Char(string="seq")
    patient_id = fields.Many2one("res.partner", string="Patient Name")
    doctor_id = fields.Many2one("res.partner", string="Doctor Name")
    test = fields.Many2one("patient.lab.test",string="Lab Test Name")
    prescriptionDate = fields.Date(string="Prescription Date")
    opd_id = fields.Many2one('opd.opd')
    state = fields.Selection([('draft', 'Draft'), ('laboratory', 'Send To Laboratory')],default='draft')
