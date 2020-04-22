from odoo import fields, models,api,_
from datetime import date

class pharmacyPrescription(models.Model):
    _name = "pharmacy.prescription"
    _description = "pharmacy prescription Details"

    @api.model  # seq
    def create(self, vals):
        res = super(pharmacyPrescription, self).create(vals)
        vals['name'] = self.env['ir.sequence'].next_by_code('PharmacyPrescription')
        res.name = vals['name']
        return res

    @api.onchange('opd_id')
    def onchange_name(self):
        for i in self:
            i.patient_id = i.opd_id.patient_id.id
            i.prescriptionDate = i.opd_id.appointment_date
            i.doctor_id = i.opd_id.doctor_id.id


    def confirm_prescription(self):
        return {
            'name': _('Update quantity on hand'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': self.env.ref('cr_medical_base.view_update_pharmacy_stock').id,
            'res_model': 'update.pharmacy.stock',
            'target': 'new',
            'context': {'medicine_ids': self.env.context.get('medicine_id', self.medicine_id).ids}
        }

        # self.state = 'done'


    def cancel_prescription(self):
        self.state = 'cancel'

    # def create_prescription_record(self):
    #     print("context----------", self, self._context.get('active_id'), self._context)
    #     record_ids = self.env['opd.opd'].browse(self._context.get('active_id'))
    #     for record in record_ids:
    #         record.write({
    #             'opd_id': self.id,
    #             'patient_id': self.patient_id.id,
    #             'doctor_id': self.doctor_id.id
    #         })


    name = fields.Char(string="seq")
    pharmacy_id = fields.Many2one("pharmacy.pharmacy",string="Pharmacy Name", required=False)
    patient_id = fields.Many2one("res.partner",string="Patient Name")
    doctor_id = fields.Many2one("res.partner",string="Doctor Name")
    # pharmacyPrescription_line_id = fields.One2many("pharmacy.medicine","prescription_id",string="prescription Lines")
    prescriptionDate = fields.Date(string="Prescription Date")
    opd_id = fields.Many2one('opd.opd')
    medicine_id = fields.Many2many("product.product", string="Medicine Name", domain="[('is_medicine','=',True)]", required=True)
    indication_id = fields.Many2one("disease.description", string="Indication")
    form_id = fields.Many2one("medicine.from", string="Form")
    dose = fields.Char(string="Dose")
    treatment_period = fields.Char(string="Treatment Period")
    prescription_type = fields.Selection([("pharmacy","Pharmacy"),("laboratory","Laboratory"),("ipd","IPD")])
    lab_id = fields.Many2one("res.partner",string="Lab Name")
    state = fields.Selection([('draft', 'Draft'),('done','Done'),('cancel','Not Available'),('pharmacy', 'Send To Pharmacy'), ('laboratory', 'Send To Laboratory')
                              ,("ipd","Send T0 IPD")],default='draft')


class patientDisease(models.Model):
    _name = "disease.description"
    _description = "About patient Disease"

    name = fields.Char("Indication")

class medicineForm(models.Model):
    _name = "medicine.from"
    _description = "About medicine From Description(Capsule...etc)"

    name = fields.Char(string="Form")





