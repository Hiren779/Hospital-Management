odoo.define('website_forum.website_forum', function (require) {
    'use strict';

    require('web.dom_ready');
    var ajax = require('web.ajax');
    var core = require('web.core');


    $(document).ready(function () {
        $("select[name=\"doctor_id_new\"]").change(function () {
            _onChangeDays()
        });

        function _onChangeDays(ev) {
            console.log(">>>>>>>>>test>>>>>>>>>>", ev)
            _changeDays();
        }

        function _changeDays() {
            if (!$("#doctor_id_new").val()) {
                return;
            }


            ajax.jsonRpc("/test/day_infos/"+ $("#doctor_id_new").val(), 'call', {
            }).then(function (data) {
                // placeholder phone_code
                //$("input[name='phone']").attr('placeholder', data.phone_code !== 0 ? '+'+ data.phone_code : '');

                // populate states and display
                console.log(">>>>>>>>>>>Test>>>>>>>>>",data)
                var selectDays = $("select[name='available_day_new']");
                // dont reload state at first loading (done in qweb)
                if (selectDays.data('init') === 0 || selectDays.find('option').length === 1) {
                    if (data.days.length) {
                        selectDays.html('');
                        _.each(data.days, function (x) {
                            var opt = $('<option>').text(x[1])
//                            .attr('value', x[0])
//                            .attr('data-code', x[2]);

                            selectDays.append(opt);
                        });
                        selectDays.parent('div').show();
                    } else {
                        selectDays.val('').parent('div').hide();
                    }
                    selectDays.data('init', 0);
                } else {
                    selectDays.data('init', 0);
                }

                // manage fields order / visibility
                /*if (data.fields) {
                    var all_fields = ["street", "zip", "city", "country_name"]; // "state_code"];
                    _.each(all_fields, function (field) {
                        $(".checkout_autoformat .div_" + field.split('_')[0]).toggle($.inArray(field, data.fields) >= 0);
                    });
                }*/
            });
        }
    });
});