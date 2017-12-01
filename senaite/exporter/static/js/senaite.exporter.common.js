/**
 * Controller class for Senaite Lists Exporter
 */

window.onload = function() {
    export_submit_controller();
};

function export_submit_controller() {
    $('input#export-list-submission-fake').bind('click', function () {
            var form = $(this).closest("form");
            $('input#export-list-submission').val('1');
            $(form).submit();
    });
}

