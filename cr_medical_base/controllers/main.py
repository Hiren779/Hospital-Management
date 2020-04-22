# -*- coding: utf-8 -*-

import json
import logging
import werkzeug
from datetime import datetime
from math import ceil

from odoo import fields, http, SUPERUSER_ID
from odoo.http import request
from odoo.tools import ustr
from odoo.http import Controller, request, route
from odoo.addons.http_routing.models.ir_http import slug


class Website(Controller):

    @http.route(['/patient-from-test'], type='http', auth='public', website=True, csrf=False)
    def website_patient_save(self, **post):
        # print("~~~~~post", post)
        patient_info = request.env['res.partner'].sudo().create({
            'name': post.get('patient name'),
            'date_of_birth': post.get('Patient BirthDate'),
            'age': post.get('patient age'),
            'sex': post.get('sex'),
            'blood_group': post.get('blood_group'),
            'marital_status': post.get('marital_status'),
            'mobile': post.get('mobile number'),
            'email': post.get('email'),
            'street': post.get('street_name'),
            'street2': post.get('street2_name'),
            'city': post.get('city_name'),
            'state_id': int(post.get('state_id')),
            'zip': post.get('zip_name'),
            'country_id': int(post.get('country_id')),
            'is_patient': True,
            'state': 'pending'
        })
        # print(">>>>>>>>>>>>>.test>>>>>>>>>>>",patient_info)
        return request.redirect('/thank-you')

    @http.route(['/doctor-form-test'], type='http', auth='public', website=True, csrf=False)
    def doctor_demo_save(self, **post):
        print("===========post=======", post)

        temp = request.httprequest.form.getlist('speciality_name')

        temp2 = request.httprequest.form.getlist('degree_name')

        print("===========\\n\n\n\ntemp2", temp2)
        print("===========\\n\n\n\ntemo", temp)

        doctor_weekavailiblity = request.env["doctor.weeklyavalibility"].sudo().create({
            'available_weekdays': post.get('available_weekdays_name'),
            'from_time': post.get('from_time_name'),
            'to_time': post.get('to_time_name'),
            'totel_appointment': post.get('totel_appointment_name'),
            'name': post.get('total_time_name'),
        })

        doctor_info = request.env['res.partner'].sudo().create({
            'name': post.get('doctor_name'),
            # 'speciality_ids': post.get('speciality_name'),
            'joining_date': post.get('Doctor_Joining_Date'),
            'sex': post.get('sex'),
            'doctor_fees': post.get('doctor_fees'),
            'licence': post.get('licence_id'),
            # 'degree_ids': post.get('degree_name'),
            'working_institute': post.get('working_institute'),
            'mobile': post.get('mobile'),
            'email': post.get('email_name'),
            'work_location': post.get('working_location'),
            'is_doctor': True,
            'state': 'pending',
            'weekly_avalibility_line': [(6, 0, [doctor_weekavailiblity.id])],  # for One2Many Relation
            'speciality_ids': [(6, 0, [speciality1 for speciality1 in temp])],
            'degree_ids': [(6, 0, [degree1 for degree1 in temp2])],

        })
        # print(">>>>>>>>>>>>>.\n\n\n\n\n\n\nspeciality>>>>>>>>>>>", speciality_ids)
        return request.redirect('/thank-you')

    @http.route(['/opd-form-info'], type='http', auth='public', website=True)
    def website_opd(self, **post):
        # print('------self----', self)
        patient_data = request.env['res.partner'].sudo().search([('is_patient', '=', True)])
        doctor_data = request.env['res.partner'].sudo().search([('is_doctor', '=', True)])
        state_name = request.env['res.country.state'].search([])
        country_name = request.env['res.country'].search([])

        time_data = request.env['doctor.weeklyavalibility'].sudo().search([])
        print(">>>>>>>>>>>>>.opd>>>>>>>>>>>", patient_data)
        print(">>>>>>>>>>>>>.opd>>>>>>>>>>>", time_data)
        print(">>>>>>>>>>>>>.Doctor>>>>>>>>", doctor_data)

        return request.render("cr_medical_base.website_opd_form",
                              {'patient_data': patient_data, 'doctor_data': doctor_data, 'time_data': time_data,
                               'res_data_state': state_name,
                               'res_data_country': country_name})

    @http.route(['/test/day_infos/<model("res.partner"):doctor_data>'], type='json', auth="public", methods=['POST'],
                website=True)

    def day_infos(self, doctor_data, **kw):
        print('self-=========',self)
        day_ids = request.env['doctor.weeklyavalibility'].search([('doctor_id', '=', doctor_data.id)])
        # print("\n\n\nAvailabel week days",day_ids.available_weekdays)
        print("===============daysssssss=================", day_ids)

        return dict(
            days=[(str(a.available_weekdays) + ',' + a.from_time + ' to ' + a.to_time + '\n',
                   str(a.available_weekdays) + ',' + a.from_time + ' to ' + a.to_time + '\n',
                   str(a.available_weekdays) + ',' + a.from_time + ' to ' + a.to_time + '\n') for a in day_ids],
        )


    @http.route(['/test/selecttime_infos/<model("res.partner"):doctor_data>'], type='json', auth="public", methods=['POST'],
                website=True)
    def selecttime_infos(self, doctor_data, **kw):
        print('self-=========',self)
        selecttime_ids = request.env['doctor.weeklyavalibility'].search([('doctor_id', '=', doctor_data.id)])
        # print("\n\n\nAvailabel week days",day_ids.available_weekdays)
        print("===============time=================", selecttime_ids)
        return dict(
            selecttime=[(st.id, st.name) for st in selecttime_ids],
        )

    @http.route(['/website-opd-test'], type='http', auth='public', website=True, csrf=False)
    def website_opd_save_existing(self, **post):
        print("~~~~~post", post)
        opd_data = request.env['opd.opd'].sudo().create({
            'patient_id': post.get('patient_name'),
            'doctor_id': post.get('doctor_id'),
            'appointment_date': post.get('appointment_date_name'),
            'available_day': post.get('availabel_days'),
            'weekdays': post.get('weekdays_name'),
            'select_time_id': int(post.get('select_time_id')),
            'existing_patient_name': True
        })
        print(">>>>>>>>>>>>>opd>>>>>>>>>>>", opd_data)
        return request.redirect('/thank-you')


    @http.route(['/website-opd-new-test'], type='http', auth='public', website=True, csrf=False)
    def website_opd_save_new(self, **post):
        print("~~~~~post", post)
        opd_data = request.env['opd.opd'].sudo().create({
            'new_patient_name': post.get('patient_name_name'),
            'date_of_birth': post.get('date_of_birth_name_new'),
            'age': post.get('age_name_new'),
            'sex': post.get('sex'),
            'blood_group': post.get('blood_group'),
            'mobile': post.get('mobile_number'),
            'email': post.get('email'),
            'street': post.get('street_name'),
            'street2': post.get('street2_name'),
            'city': post.get('city_name'),
            'state_id': int(post.get('state_id')),
            # 'zip': post.get('zip_name'),
            'country_id': int(post.get('country_id')),
            'patient_id': post.get('patient_name'),
            'doctor_id': post.get('doctor_id_new'),
            'appointment_date': post.get('appointment_date_name1'),
            'available_day': post.get('available_day_new'),
            'weekdays': post.get('weekdays_name'),
            'select_time_id': post.get('select_time_id_new'),
            'existing_patient_name': False
        })
        # print(">>>>>>>>>>>>>.test>>>>>>>>>>>",opd_data)
        return request.redirect('/thank-you')

    @http.route(['/registration-from-info'], type='http', auth='public', website=True)
    def website_registration_form1(self, **post):
        print('------self----', self)
        res_data = request.env['res.partner'].sudo().search([('is_patient', '=', True)])
        country = request.env['res.country'].search([])
        res_data1 = request.env['res.partner'].sudo().search([('is_doctor', '=', True)])
        speciality_data = request.env["doctor.speciality"].sudo().search([])
        degree_data = request.env["doctor.degree"].sudo().search([])
        print(">>>>>>>>>>>>>.test>>>>>>>>>>>", degree_data)

        print(">>>>>>>>>>>>>.speciality test>>>>>>>>>>>", speciality_data)
        print("=====country1======", res_data)

        print("=====country======", country)
        print(">>>>>>>>>>>>>.test>>>>>>>>>>>", res_data1)
        return request.render("cr_medical_base.website_registration_form",
                              {'res_data': res_data,
                               'countries': country,  # doc
                               'res_data1': res_data1,
                               'degree_data': degree_data,
                               'speciality_data': speciality_data,
                               })

    @http.route(['/country_infos/<model("res.country"):country>'], type='json', auth="public", methods=['POST'],
                website=True)
    def country_infos(self, country, **kw):
        states_ids = request.env['res.country.state'].search([('country_id', '=', country.id)])
        print('\n\n\\n\n\n\n State Ids', states_ids)
        states = [(st.id, st.name, st.code) for st in states_ids]
        print('\n\n\n\nstates=====',states)
        return dict(
            states=[(st.id, st.name, st.code) for st in states_ids],
        )

    @http.route(['/doctor-info'], type='http', auth='public', website=True)
    def doctor_view(self):
        doctor_data = request.env['res.partner'].sudo().search([('is_doctor', '=', True)])
        # print("=================dddddddddddddddddddd========================", doctor_data)
        speciality_data = request.env["doctor.speciality"].sudo().search([])
        return request.render("cr_medical_base.website_doctor_template", {'doctor_data':doctor_data, 'speciality_data':speciality_data})


    # @http.route(['/candidroot_medical/doctor-details-info/'], type='http', auth='public', website=True)
    # def doctor_details_view(self):
    #     doctor_dat = request.env['res.partner'].sudo().search([('is_doctor', '=', True)])
    #     print("=================dddddddddddddddddddd========================", doctor_dat)
    #     return request.render("cr_medical_base.website_doctor_details_template", {'doctor_data': doctor_dat})

    @http.route(['/candidroot_medical/doctor-details-info/<model("res.partner"):doctor>'], type='http', auth="public",website=True)
    def docturinfo(self, doctor, **kwargs):
        return request.render("cr_medical_base.website_doctor_details_template",{'data': doctor})







