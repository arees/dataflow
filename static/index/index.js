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
      }
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
