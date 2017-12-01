/**
 * Controller class for Senaite Lists Exporter
 */

window.onload = function() {
    export_submit_controller();
};

function export_submit_controller() {
    /**
    This function submits the form once the filter button is clicked.
    The function sets the input[name="export-list-submission"]
    value as '1'.
    */
    $('input#export-list-submission-fake').bind('click', function () {
            // Get Plone filter value and back it up.
            var filter_val = $('.filter-search-input').val();
            $('#filter-backup').val(filter_val);
            var form = $(this).closest("form");
            // Submit value
            $('input#export-list-submission').val('1');
            $(form).submit();
    });
}

