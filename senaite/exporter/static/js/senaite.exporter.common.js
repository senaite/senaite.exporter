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
    $('select#exporter-selection').change(function() {
        // Gettin bika filter bar values
        var filter_options = {};
        var selected = '';
        // inputs fields
        var input_filters = $(
            '.bika_listing_filter_bar input[name][value!=""]');
        $(input_filters).each(function(e) {
          filter_options[$(this).attr('name')] = $(this).val();
        });
        // select fields
        var select_filters = $('.bika_listing_filter_bar select');
        $(select_filters).each(function(e) {
          selected = $(this).find('option:selected[value!=""]').val();
          filter_options[$(this).attr('name')] = selected;
        });

        if (!jQuery.isEmptyObject(filter_options)) {
          $('#filter-bar-backup').val($.toJSON(filter_options));
        }

        // Get Plone filter value and back it up.
        var filter_val = $('.filter-search-input').val();
        $('#filter-backup').val(filter_val);
        var form = $(this).closest("form");
        // Submit value
        $('input#export-list-submission').val('1');
        $(form).submit();
        // Select the default (empty) option again
        $(this).find("option[value='']").prop('selected', true)
    });
}

