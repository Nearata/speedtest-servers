$(function() {
    let table = $("#table").DataTable({
        "ajax": {
            "url": "/servers"
        },
        "columns": [
            {"data": "id"},
            {"data": "provider"},
            {"data": "country"},
            {"data": "city"}
        ],
        "order": [[1, "asc"]],
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "ALL"]],
        "autoWidth": true,
        "responsive": true,
        "deferRender": true,
        "columnDefs": [
            {targets: 0, "width": "12%"},
            {targets: [2, 3], width: "20%"}
        ],
        createdRow: function(row, data, index) {
            $("td", row).eq(0).attr("data-label", "id")
            $("td", row).eq(1).attr("data-label", "provider")
            $("td", row).eq(2).attr("data-label", "country")
            $("td", row).eq(3).attr("data-label", "city")
        },
        initComplete: function() {
            this.api().columns().every(function() {
                var column = this;
                var select = $('<select class="select2-filtered" style="width: 100%;"><option value=""></option></select>')
                    .appendTo($(".filters .filter-"+column[0][0]).empty())
                    .on('change', function() {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );
                        column.search(val ? '^'+val+'$' : '', true, false).draw();
                    });
 
                column.data().unique().sort().each(function (d, j) {
                    select.append('<option value="'+d+'">'+d+'</option>')
                });
            });
            $(".select2-filtered").select2({
                placeholder: "Select an option",
                allowClear: true
            });
        }
    });
    $("#update-table").click(function() {
        $.post("/servers/update").fail(function(res) {
            alert(res["responseText"])
        }).done(function() {
            table.ajax.reload();
        })
    })
    $("#admin-tools").submit(function(e) {
        e.preventDefault()
        
        $.post("/admin/servers/update/", {
            "username": $("#username").val(),
            "access_key": $("#access-key").val()
        }).fail(function(res) {
            alert("Invalid credentials.")
        })
    })
});