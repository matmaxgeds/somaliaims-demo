$(document).ready(function(){

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);

        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }

    return cookieValue;
  }

  var csrftoken = getCookie('csrftoken');

  // Trigger the event for location dropdowns
  $('#location select[id$=\'location\']').change(function() {
    $.ajax({
      context: this,
      type: 'POST',
      url: '/data-entry/sublocations/',
      data: {
        'location': $(this).find(':selected').val(),
      },
      headers: {'X-CSRFToken': csrftoken},
      success: function(options) {
        // Find the sublocations select
        var subl = $(this).parent().next().find('select');
        subl.multiselect('dataprovider', options);
      },
    });
  });

});