# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from odoo import fields, models,api, _
from datetime import date

class ResPartner(models.Model):
    _inherit = "res.partner"
    _description = 'About Patient'

    @api.onchange('date_of_birth')
    def _compute_age(self):
        for record in self:
            print("............")
            if record.date_of_birth and record.is_patient:
                if str(record.date_of_birth) > str(date.today()):
                    print("............if",str(date.today()))
                    warning_mess = {
                            'title':('Warning!'),
                            'message': ('Pleace Select Valid Date!!'),
                        }
                    return {'warning': warning_mess}
                else:
                    if record.date_of_birth and record.date_of_birth <= fields.Date.today():
                        print("----------------else")
                        record.age = relativedelta(
                        fields.Date.from_string(fields.Date.today()),
                        fields.Date.from_string(record.date_of_birth)).years
                        print("======================sge-------------------",record.age)

            if record.date_of_birth and record.date_of_birth <= fields.Date.today() and record.is_pharmacist:
                record.age = relativedelta(
                    fields.Date.from_string(fields.Date.today()),
                    fields.Date.from_string(record.date_of_birth)).years
                if record.age < str(21):
                    warning_mess = {
                        'title': _('Warning!'),
                        'message': _(
                            'Age Must Be Grater Then 21!!'),
                    }
                    return {'warning': warning_mess}

    def create_user(self):
        self.state = 'approve'
        for user in self:
            # print('-----self---', user)
            values = {'partner_id': user.id,
                      'name': user.name,
                      'login': user.email,
                      'groups_id': [(6, 0, self.env.ref('cr_medical_base.group_patient').ids)]}
            # print('-----values---', values)
            res = self.env['res.users'].create(values)
            return res

    def cancel(self):
        self.state = 'reject'


    sex = fields.Selection([('male','Male'),('female','Female')], 'Sex')
    age = fields.Integer('Age')
    blood_group = fields.Selection([('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),('AB+','AB+'),('AB-','AB-'),('O+','O+'),('O-','O-')], 'Blood Group')
    date_of_birth = fields.Date('Date of Birth', help = 'Date Of Birth')
    marital_status = fields.Selection([('single','Single'),('married','Married'),('widow','Widow'),('divorced','Divorced')], 'Marital Status')
    is_patient = fields.Boolean('Is Patient')
    user_id = fields.Many2one('res.users',string='User Id')
    pharmacy_history_line_ids = fields.One2many('pharmacy.prescription','patient_id')
    laboratory_history_line_ids = fields.One2many('pharmacy.prescription', 'patient_id')
    state = fields.Selection(
        [('draft', 'Draft'), ("pending", "Pending"), ("approve", "Approved"), ("reject", "Rejected")],
        string="State", default="draft")

