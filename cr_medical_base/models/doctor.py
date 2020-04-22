# -*- coding: utf-8 -*-
from odoo import fields,models,api,_
from datetime import date
from odoo.exceptions import UserError,ValidationError

class ResPartner(models.Model):
    _inherit = "res.partner"
    _description = "Doctor Information"

    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        print(">>>>>>>>res>>>>>>>>>>>>",res)
        vals['name'] = self.env['ir.sequence'].next_by_code('Doctor ID')
        res.dr_form_no = vals['name']
        return res

    @api.multi
    def toggle_appointment_active(self):
        form_view_id = self.env.ref('cr_medical_base.cr_opd_form_view').id
        tree_view_id = self.env.ref('cr_medical_base.cr_opd_tree_view').id
        return {
            'name': 'Appointment List',
            'type': 'ir.actions.act_window',
            'res_model': 'opd.opd',
            'view_mode': 'tree,form',
            'views': [(tree_view_id, 'tree'),(form_view_id,'form')],
            'res_id': False,
            'target': 'current',
            'domain': [('doctor_id', '=', self.id)],
        }

    def compute_count(self):
        for appointment in self:
            appointment.appointment_count = self.env["opd.opd"].search_count(
                [('doctor_id', '=', appointment.id)])

    @api.constrains("joining_date")
    def select_valid_date(self):
        today = date.today()
        if self.joining_date:
            print("~~~~~~~~~~~`")
        if self.joining_date:
            today = date.today()
        print("~~~~~~~~~~~`")
        if self.joining_date:
            today = date.today()
            if self.joining_date > today:
                raise ValidationError('Please select valid date')


#Start DeshBoard

    def _get_action(self, action_xmlid):
        # print("\n\n\n\===========self==================",self)
        # print("\n\n\n\===========action_xmlid==================",action_xmlid)
        # TDE TODO check to have one view + custo in methods
        action = self.env.ref(action_xmlid).read()[0]
        print("\n\n\n\===========action==================", action)
        if self:
            action['domain'] = [('doctor_id', '=', self.id)]
        return action

    def get_doctor_detail(self):
        return self._get_action('cr_medical_base.action_appointment_new_listing_details')

    def _get_confirm_action(self,action_xmlid):
        # print("\n\n\n\===========self==================", self)
        # print("\n\n\n\===========action_xmlid==================",action_xmlid)
        action = self.env.ref(action_xmlid).read()[0]
        # print("\n\n\n\===========action==================", action)
        if self:
            action['domain'] = [('doctor_id', '=', self.id),('state','in',['confirm','sent','done'])]
        return action

    @api.one
    def compute_count_confirm(self):
        for i in self:
            a = self.env["opd.opd"].search([('state','in',['confirm','sent','done']),('doctor_id','=', self.id)])
            # print('==========a===============',a.ids)
            i.confirm_count = len(a.ids)
            # print("=====================appppppppppppp========================",i.confirm_count)

    def get_state_confirm_details(self):
        return self._get_confirm_action('cr_medical_base.action_cr_opd_patient_information')



    def _get_pending_action(self,action_xmlid):
        # print("\n\n\n\===========self==================", self)
        # print("\n\n\n\===========action_xmlid==================",action_xmlid)
        action = self.env.ref(action_xmlid).read()[0]
        # print("\n\n\n\===========action==================", action)
        if self:
            action['domain'] = [('doctor_id', '=', self.id),('state','=','pending')]
        return action

    @api.one
    def compute_count_pending(self):
        for i in self:
            a = self.env["opd.opd"].search([('state','=','pending'),('doctor_id','=', self.id)])
            # print('==========a===============',a.ids)
            i.pending_count = len(a.ids)
            # print("=====================appppppppppppp========================",i.pending_count)

    def get_state_pending_details(self):
        return self._get_pending_action('cr_medical_base.action_cr_opd_patient_information')


    def _get_cancel_action(self, action_xmlid):
        # print("\n\n\n\===========self==================", self)
        # print("\n\n\n\===========action_xmlid==================",action_xmlid)
        action = self.env.ref(action_xmlid).read()[0]
        # print("\n\n\n\===========action==================", action)
        if self:
            action['domain'] = [('doctor_id', '=', self.id), ('state', '=', 'cancel')]
        return action

    @api.one
    def compute_count_cancel(self):
        for i in self:
            a = self.env["opd.opd"].search([('state', '=', 'cancel'), ('doctor_id', '=', self.id)])
            # print('==========a===============',a.ids)
            i.cancel_count = len(a.ids)
            # print("=====================appppppppppppp========================",i.pending_count)

    def get_state_cancel_details(self):
        return self._get_cancel_action('cr_medical_base.action_cr_opd_patient_information')

    # def change_colore_on_kanban(self):# NOT WORKING
    #     for record in self:
    #         a = self.env["opd.opd"].search([])
    #         for i in a:
    #             print("===================a.stata===============",i.state)
    #             color = 0
    #             if i.state == 'confirm':
    #                 color = 2
    #             elif i.state == 'pending':
    #                 color = 5
    #
    #             else:
    #                 color = 10
    #     record.color = color

####END DeshBoard

    def create_user(self):
        self.state = 'approve'
        for user in self:
            # print('-----self---', i)
            values = {'partner_id': user.id,
                      'name': user.name,
                      'login': user.email,
                      'state': 'active',
                      'groups_id': [(6, 0, self.env.ref('cr_medical_base.group_doctor').ids)]}
            # print('-----values---', values)
            result = self.env['res.users'].create(values)
            return result

    def cancel(self):
        self.state = 'reject'


    sex = fields.Selection([('male', 'Male'), ('female', 'Female')], 'Sex')
    speciality_ids = fields.Many2many('doctor.speciality', string='Speciality',required=True)
    # speciality = fields.Char("Speciality")
    # age = fields.Integer('Age')
    degree_ids = fields.Many2many('doctor.degree', string='Degree',required=True)
    doctor_fees = fields.Char('Fees')
    licence = fields.Char('Licence ID')
    working_institute = fields.Char('Working Institute')
    work_location = fields.Char('Work Location')
    weekly_avalibility_line = fields.One2many("doctor.weeklyavalibility", "doctor_id", 'Doctor Availablity', required="1")
    dr_form_no = fields.Char("Doctor Form Number")
    bool_field = fields.Boolean("Confirm", default=False)
    appointment_count = fields.Integer(compute="compute_count")
    joining_date = fields.Date(string="Doctor Joining Date")
    is_doctor = fields.Boolean('Is Doctor')
    patient_id = fields.Many2one("opd.opd",string="Patient Name")
    user_id = fields.Many2one('res.users',string='User Id')
    confirm_count = fields.Char(compute="compute_count_confirm")
    pending_count = fields.Char(compute="compute_count_pending")
    cancel_count = fields.Char(compute="compute_count_cancel")
    # color = fields.Integer('Color Index', compute="change_colore_on_kanban")
    state = fields.Selection(
        [('draft', 'Draft'), ("pending", "Pending"), ("approve", "Approved"), ("reject", "Rejected")],
        string="State", default="draft")


class weeklyavalibility(models.Model):
    _name ="doctor.weeklyavalibility"
    _description = "Doctor Weekly Schedule"


    @api.onchange('from_time', 'to_time')
    def totall_time(self):
        if self.from_time and self.to_time:
            for i in self:
                self.name = i.from_time + ' To ' +i.to_time


    available_weekdays = fields.Selection([('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')],string='Available Weekdays',required=True)
    from_time = fields.Char("From Time")
    to_time = fields.Char("To Time")
    totel_appointment = fields.Integer("Total Appointment")
    name = fields.Char(string ='Total Time')
    doctor_id = fields.Many2one("res.partner")

class speciality(models.Model):
    _name = "doctor.speciality"
    _description = "Doctor Speciality"
    _rec_name = "speciality"

    speciality = fields.Char("Speciality")


class degree(models.Model):
    _name = "doctor.degree"
    _description = "Doctor Degree"
    _rec_name = "degree"

    degree = fields.Char("Degree")






