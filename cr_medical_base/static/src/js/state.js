odoo.define('website_forum.website_forum', function (require) {
    'use strict';

    require('web.dom_ready');
    var ajax = require('web.ajax');
    var core = require('web.core');


    $(document).ready(function () {
        $("select[name=\"country_id\"]").change(function () {
            _onChangeCountry()
        });

        function _onChangeCountry(ev) {
            console.log(">>>>>>>>>test>>>>>>>>>>", ev)
            _changeCountry();
        }

        function _changeCountry() {
            if (!$("#country_id").val()) {
                return;
            }


            ajax.jsonRpc("country_infos/"+ $("#country_id").val(), 'call', {
            }).then(function (data) {
                // placeholder phone_code
                //$("input[name='phone']").attr('placeholder', data.phone_code !== 0 ? '+'+ data.phone_code : '');

                // populate states and display
                console.log(">>>>>>>>>>>Test>>>>>>>>>",data)
                var selectStates = $("select[name='state_id']");
                // dont reload state at first loading (done in qweb)
                if (selectStates.data('init') === 0 || selectStates.find('option').length === 1) {
                    if (data.states.length) {
                        selectStates.html('');
                        _.each(data.states, function (x) {
                            var opt = $('<option>').text(x[1])
                                .attr('value', x[0])
                                .attr('data-code', x[2]);
                            selectStates.append(opt);
                        });
                        selectStates.parent('div').show();
                    } else {
                        selectStates.val('').parent('div').hide();
                    }
                    selectStates.data('init', 0);
                } else {
                    selectStates.data('init', 0);
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