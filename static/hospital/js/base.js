// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#patientHistoryTable').DataTable({
    'order': [[ $("#patientHistoryTable > thead > tr > th").length - 1, "desc" ]],
    'language': {
      'url': "//cdn.datatables.net/plug-ins/1.10.16/i18n/Russian.json"
    },
    columnDefs: [
        { targets: 'patientHistoryCol_Doctor', width: '160px'},
        { targets: 'patientHistoryCol_Date', width: '140px'}
    ]
  });

  $('[data-toggle="popover"]').each(function() {
    if ($(this).parent().hasClass('bootstrap-select')) {
      $(this).parent().popover({
        placement: 'left',
        trigger: 'hover',
        content: $(this).data('content'),
        title: $(this).attr('title')
      })
    } else if ($(this).parent().parent().hasClass('checkbox')){
      $(this).parent().addClass('col-8')
      $(this).parent().popover({
        placement: 'left',
        trigger: 'hover',
        content: $(this).data('content'),
        title: $(this).attr('title')
      })
    } else {
      $(this).popover({
        placement: 'left',
        trigger: 'hover'
      })
    }
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
