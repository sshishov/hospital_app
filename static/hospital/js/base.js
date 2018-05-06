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
});
