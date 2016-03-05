$(document).ready(function() {
  $("#select-isp").hide()
  $('#company-type').on('change', function(){
      console.log("yo lol")
      console.log($("#company-type").val())
      if($('#company-type').val() == 'dev'){
          $('#select-isp').show();
          $('.register-btn').css('height', '540px')
      } else {
        $('#select-isp').hide()
        $('.register-btn').css('height', '470px')
      }
  });
  $('#company-region').on('change', function(){
    console.log("yay change region")
    $.getJSON($SCRIPT_ROOT + '/get_isps_region', {
      region: $('#company-region').val()
    }, function(data) {
      console.log(data)
      $.each(data.isps, function(index, value) {
        console.log(index, value)
        $('#select-isp').append("<option value='" + value.id + "'>" + value.long_name + "</option>")
      });
    });
    return false;

  });

})
$(".user").focusin(function(){
  $(".inputUserIcon").css("color", "#e74c3c");
}).focusout(function(){
  $(".inputUserIcon").css("color", "white");
});

$(".pass").focusin(function(){
  $(".inputPassIcon").css("color", "#e74c3c");
}).focusout(function(){
  $(".inputPassIcon").css("color", "white");
});
