$(function () {                                                                     //multiselection
  $('select').each(function () {
    $(this).select2({
      theme: 'bootstrap4',
      width: 'style',
      placeholder: $(this).attr('placeholder'),
      allowClear: Boolean($(this).data('allow-clear')),
    });
  });
});


$(function () {                                                                      //fromtotime(doctor)
    $("#from_time,#to_time").on("input", function () {
        if ($("#from_time").val() != "") {
            terms = $("#from_time").val() + ' to ' + $("#to_time").val();
        } else terms = terms = "No time entered";

        $("#total_time_name").val(terms);
    });
});


function validation1() {                                                                  //dateofjoining
    var UserDate = document.getElementById("date_of_joining").value;
    var ToDate = new Date();

    if (new Date(UserDate).getTime() >= ToDate.getTime()) {
          document.getElementById("username1").innerHTML = "Please enter valid date"

          return false;
     }
    return true;
}

function validation() {                                                                     //dateofbirth
var UserDate = document.getElementById("date_of_birth").value;
var ToDate = new Date();

if (new Date(UserDate).getTime() >= ToDate.getTime()) {
      document.getElementById("username").innerHTML = "Please enter valid date"

      return false;
 }
return true;
}

function comp(){
   var bday = document.getElementById('date_of_birth').value;
    var today = new Date();
    var birthDate = new Date(bday);
    var age = today.getFullYear() - birthDate.getFullYear();
    var m = today.getMonth() - birthDate.getMonth();
    if (today.getMonth() <= birthDate.getMonth() || (today.getMonth() == birthDate.getMonth() && today.getDate() < birthDate.getDate())) {
        age--;
         }
    document.getElementById('age').value=age;

}

function myFunction() {                                                                   //datetoday and compare(exist)
    var a = document.getElementById("appointment_date").value;
    var availabel_day_time = document.getElementById("availabel_days").value;
    var availabel_day = availabel_day_time.split(',');
    var ToDate = new Date();
     var d = new Date(a);

      var weekday = new Array(7);
      weekday[0] = "Sunday";
      weekday[1] = "Monday";
      weekday[2] = "Tuesday";
      weekday[3] = "Wednesday";
      weekday[4] = "Thursday";
      weekday[5] = "Friday";
      weekday[6] = "Saturday";

      var weekdays = weekday[d.getDay()];
      document.getElementById("weekdays").value = weekdays;

      if (weekdays != availabel_day[0] || d.getTime() <= ToDate.getTime() ) {
            alert('Choose Correct weekday as per availabel day or date must greter today date');

      return false;
 }

return true;

}

function myFunction_new() {                                                             //datetoday and compare(new)
    var a = document.getElementById("appointment_date1").value;
    var availabel_day_time = document.getElementById("available_day_new").value;
    var availabel_day = availabel_day_time.split(',');
    var ToDate = new Date();
     var d = new Date(a);
      var weekday = new Array(7);
      weekday[0] = "Sunday";
      weekday[1] = "Monday";
      weekday[2] = "Tuesday";
      weekday[3] = "Wednesday";
      weekday[4] = "Thursday";
      weekday[5] = "Friday";
      weekday[6] = "Saturday";

      var weekdays = weekday[d.getDay()];
      document.getElementById("weekdays1").value = weekdays;

      if (weekdays != availabel_day[0] || d.getTime() <= ToDate.getTime()) {
     alert('Choose Correct weekday as per availabel day or date must greter today date');

      return false;
 }

return true;

}


$(document).ready(function(){                                                    //menucolour
    if (window.location.pathname == '/'){
    $('.nav-link').addClass('home-menu')
    }
});


type="text/javascript">                                                              //radiobutton
    $(document).ready(function() {
        $('input[type="radio"]').click(function() {
            var inputValue = $(this).attr("value");
            var targetBox = $("." + inputValue);
            $(".selectt").not(targetBox).hide();
            $(targetBox).show();
        });
    });


function timeselectop(){
//    var a = document.getElementById("select_time_id").value;
    var availabel_day_time = document.getElementById("availabel_days").value;
    var availabel_day = availabel_day_time.split(',');

    console.log(">>>>>>>>>>>Test>>>>>>>>>",(typeof availabel_day[1]))
    console.log(">>>>>>>>>>>Test>>>>>>>>>",(typeof a))
    console.log(">>>>>>>>>>>Test>>>>>>>>>",(result))

//    var result = availabel_day[1];
//     console.log(">>>>>>>>>>>Test>>>>>>>>>",result)
//    document.getElementById("select_time_id").value = result;
//}

    if (a != availabel_day[1]) {
        alert('Choose Correct time as per availabel day od doctor');
        return false;
   }
return true;
}

//function comp_new() {
//    var UserDate = document.getElementById("date_of_birth_new").value;
//    var ToDate = new Date();
//
//
//    if (new Date(UserDate).getTime() >= ToDate.getTime()) {
//    alert('Enter Correct BirthDate');
//
//    return false;
//    }
//
//    return true;
//}

//$('#abc').click(function () {
//
//    console.log("===========================abc================,")
//    var WRProdId = "<t t-esc="data.name"/>";
//    console.log("=================================",WRProdId)
//    addComment();
//});
//
//$(abc).ready(function(){
//    console.log("dgufyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyei")
//     var WRProdId = "<t t-esc="data.name"/>";
//     $(abc).attr('href','/abc.info');
//
//});

//$(document).ready(function()
//{
//
//var input = $("abc").html();
//console.log("wefwwwwwwwwwwwww",input);
//
//$('#contents').attr('href','/registration-from-info');
//})