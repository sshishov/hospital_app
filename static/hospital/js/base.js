// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#patientHistoryTable').DataTable({
    'language': {
      'url': "//cdn.datatables.net/plug-ins/1.10.16/i18n/Russian.json"
    },
    'columns': [
      null,
      { "width": "140px" },
      { "width": "80px" }
    ]
  });

  $('[data-toggle="popover"]').popover({
    placement: 'left',
    trigger: 'focus'
  });

  $.datetimepicker.setLocale('ru');

  $('[data-provide="datepicker"]').datetimepicker({
    timepicker:false,
    onShow: function(){
      this.setOptions({mask: true});
    },
    format: "d.m.Y"
  });

  $('[data-provide="datetimepicker"]').datetimepicker({
    onShow: function(){
      this.setOptions({mask: true});
    },
    format: "d.m.Y H:i:s"
  });
});
