odoo.define('website_forum.website_forum', function (require) {
    'use strict';

    require('web.dom_ready');
    var ajax = require('web.ajax');
    var core = require('web.core');


    $(document).ready(function () {
        $("select[name=\"doctor_id\"]").change(function () {
            _onChangeDays()
        });

        function _onChangeDays(ev) {
            console.log(">>>>>>>>>ev>>>>>>>>>>", ev)
            _changeDays();
        }

        function _changeDays() {
            if (!$("#doctor_id").val()) {
                return;
            }


            ajax.jsonRpc("/test/selecttime_infos/"+ $("#doctor_id").val(), 'call', {
            }).then(function (data) {
                // placeholder phone_code
                //$("input[name='phone']").attr('placeholder', data.phone_code !== 0 ? '+'+ data.phone_code : '');

                // populate states and display
                console.log(">>>>>>>>>>>Test>>>>>>>>>",data)
                var selecttimeid = $("select[name='select_time_id']");
                // dont reload state at first loading (done in qweb)
                if (selecttimeid.data('init') === 0 || selecttimeid.find('option').length === 1) {
                    if (data.selecttime.length) {
                        selecttimeid.html('');
                        _.each(data.selecttime, function (x) {
                            var opt = $('<option>').text(x[1])
//                            .attr('value', x[0])
//                            .attr('data-code', x[2]);

                            selecttimeid.append(opt);
                        });
                        selecttimeid.parent('div').show();
                    } else {
                        selecttimeid.val('').parent('div').hide();
                    }
                    selecttimeid.data('init', 0);
                } else {
                    selecttimeid.data('init', 0);
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