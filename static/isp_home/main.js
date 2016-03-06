views = ['main', 'coverage', 'infraestructure', 'compute', 'datacoin']
max_view = views.length
index = -1

$(document).ready(function() {
  $.each(views, function(index, view) {
    console.log('.' + view)
    $('.' + view).hide()
  });
  $(document).on('click', function() {
    target = event.target
    if(target.nodeName == 'HTML' || target.nodeName == 'DIV') {
      $('#welcome').hide();
      console.log(index)
      console.log(views[index])
      $('.' + views[index]).hide();
      index ++;
      $('.' + views[index]).show();
      console.log(views[index])
    }
  });
});
