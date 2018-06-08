// Call the dataTables jQuery plugin
$(document).ready(function() {
  table = $('#patientHistoryTable').DataTable({
    'language': {
      'url': "//cdn.datatables.net/plug-ins/1.10.16/i18n/Russian.json"
    },
    columnDefs: [
        { targets: 'patientHistoryCol_Doctor', width: '160px'},
        { targets: 'patientHistoryCol_Date', width: '140px'}
    ]
  });

  $('[data-toggle="popover"]').popover({
    placement: 'left',
    trigger: 'hover'
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
