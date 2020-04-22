# -*- coding: utf-8 -*-
from odoo import fields, models,api
from odoo.exceptions import ValidationError
# from odoo import exceptions
from datetime import date


class opdopd(models.Model):
    _name = "opd.opd"
    _description = "patient can book their appointment"

    @api.onchange('appointment_date')
    def findDay(self):
        if self.appointment_date:
            day1 = self.appointment_date.strftime("%A")
            self.weekdays = day1
            print("\n\n\n!~~~~~!!dayy",day1)
            day_dict = {}
            for value in self.doctor_id.weekly_avalibility_line:

                if value.available_weekdays in day_dict:
                    day_dict[str(value.available_weekdays)].append(str(value.from_time) + ' to ' + str(value.to_time))
                if value.available_weekdays not in day_dict:
                    day_dict.update({str(value.available_weekdays):[str(value.from_time)+' to '+ str(value.to_time)]})
            for key,val in day_dict.items():
                x = ''
                for i in val:
                    x = x + ' '+ i

            self.select_time = x


    def confirm_appointment(self):
        self.state = "confirm"


    def pending_appointment(self):
        self.state = "pending"

    def reject_appointment(self):
        self.state = "cancel"

    def send_appointment(self):
        self.state = 'sent'
        print("context----------", self, self._context.get('active_id'), self._context)
        self.prescription_line_ids.write({'opd_id': self.id,
                    'patient_id': self.patient_id.id,
                    'doctor_id': self.doctor_id.id,
                    'prescriptionDate':self.appointment_date})
        for p_line in self.prescription_line_ids:
            if p_line.prescription_type == 'ipd':
                vals = {'patient_id': self.patient_id.id, 'doctor_id': self.doctor_id.id,  'disease':p_line.indication_id.name, 'opd_id' : self.id}
                print("========================a======bvals=================", vals)
                ipd_creation_id = self.env['ipd.registration'].create(vals)

        for i in self:
            for j in i.prescription_line_ids:
                print("==============j==================",j.prescription_type)
                if j.prescription_type in 'pharmacy':
                     j.state = 'pharmacy'
                elif j.prescription_type in 'laboratory':
                    j.state = 'laboratory'
                elif j.prescription_type in 'ipd':
                    j.state = 'ipd'


    @api.onchange('doctor_id')
    def show_date(self):
        q = []

        for i in self:
            for a in i.doctor_id.weekly_avalibility_line:
                k = str(a.available_weekdays)+','+a.from_time+' to '+a.to_time+'\n'
                q.append(k)
                day = "".join(str(x) for x in q)
                i.available_day = day


    @api.constrains("weekdays")
    def match_day_with_doctor(self):
        for i in self:
            day_val = []
            print("\n\n\n~~~~~day_val",day_val)
            for day in i.doctor_id.weekly_avalibility_line:
                day_val.append(day.available_weekdays)
            print("\n\n\n~~~~~day_val", day_val)
        for rec in self:
            if rec.weekdays not in day_val:
                raise ValidationError("Sorry,Doctor is not Available")

    @api.constrains("appointment_date")
    def select_valid_date(self):
        today = date.today()
        if self.appointment_date < today:
            raise ValidationError('Please select valid date')


    @api.model
    def create(self,values):
        result = super(opdopd,self).create(values)
        # print ('--------------',self.env['ir.sequence'].next_by_code('Appointment_seq'))
        values['name'] = self.env['ir.sequence'].next_by_code('Appointment_seq')
        # print("==================vals===========",values['name'])
        result.name = values['name']
        for val in result:
            my_dict = {}
            for line in val.doctor_id.weekly_avalibility_line:
                days = line.available_weekdays
                time = line.name
                appointment = line.totel_appointment
                if str(days) in my_dict:
                    my_dict[str(days)].append({str(time): str(appointment)})
                if str(days) not in my_dict:
                    my_dict.update({str(days): [{str(time): str(appointment)}]})
            weekdays = my_dict.get(str(val.weekdays))
            if weekdays:
                tot_time = self.env["doctor.weeklyavalibility"].search(
                    [("available_weekdays", "=", val.weekdays),("name", "=", val.select_time_id.name),("doctor_id","=",val.doctor_id.id)])
                print(tot_time,"\n\n\n\nval.weekdaysssssss----",type(val.weekdays))
                print("\n\n\n val.select_time_id.nameeeeeeeeee===",type(val.select_time_id.name))
                slot_dict = {}  # if doctor come twice in a day
                opd_record = self.env['opd.opd'].search_count(
                    [('weekdays', '=', str(val.weekdays)), ('doctor_id', '=', val.doctor_id.id),
                     ('select_time_id', '=', tot_time.name), ('appointment_date', '=', val.appointment_date)
                     ,('state','=','confirm')])

                for val in my_dict.get(val.weekdays):
                    for vals in val:
                        if vals == tot_time.name:
                            slot_ = val.get(tot_time.name)
                            slot_dict.update({'slot':slot_})
                if str(opd_record) > str(slot_dict.get('slot')):
                        raise ValidationError("Appoint is Full")
        return result




    name = fields.Char("seq")
    patient_id = fields.Many2one('res.partner',string='Patient', domain=[('is_patient','=',True)])
    existing_patient_name = fields.Boolean(string="Existing Patient")
    new_patient_name = fields.Char(string="Patient Name")
    doctor_id = fields.Many2one('res.partner',string='Doctor', domain=[('is_doctor','=',True)])
    appointment_date = fields.Date("Appointment Date")
    available_day = fields.Text()
    urgent_level = fields.Selection([('normal','Normal'),('urgent','Urgent'),('medical_emergency','Medical Emergency')],string='Urgent Level')
    state = fields.Selection([('draft', 'Draft'), ('pending', 'Pending'),('confirm', 'Confirm'),('sent', 'Sent Pharmacy/Laboratory/IPD'), ('cancel', 'Cancel')], default='draft')
    weekdays = fields.Char("WeekDay", readonly=True)
    available_appointment_slot = fields.Char("Available Appointment Slot")
    select_time_id = fields.Many2one('doctor.weeklyavalibility',string='Select Time')
    prescription_line_ids = fields.One2many("pharmacy.prescription",'opd_id')

    sex = fields.Selection([('male', 'Male'), ('female', 'Female')], 'Sex')
    date_of_birth = fields.Date('Date of Birth', help='Date Of Birth')
    age = fields.Integer('Age')
    blood_group = fields.Selection(
        [('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'),
         ('O-', 'O-')], 'Blood Group')
    email = fields.Char("Email_id",help='abc@gmail.com')
    mobile = fields.Char("Mobile_no" ,help='1234567890')
    street = fields.Char("Street")
    street2 = fields.Char("Street2")
    city = fields.Char("City")
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')







class AvailableApppointment(models.Model):
    _name="available.appointment"
    _description="Show available slot of appointment"
    _rec_name = 'available_appointment_slot'

    weekdays = fields.Selection([('Monday', 'Monday'), ('Tuesday','Tuesday'), ('Wednesday','Wednesday'),('Thursday','Thursday'), ('Friday','Friday'), ('Saturday','Saturday'), ('Sunday','Sunday')], string='Available Weekdays')
    available_appointment_slot= fields.Char("Available Appointment Slot")
    doctor_id = fields.Many2one("res.partner",String="Doctor Name")
    state = fields.Selection([('draft', 'Draft'), ('booked', 'Booked')], default='draft')







