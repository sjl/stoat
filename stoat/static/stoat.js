grappelli.initTableElements = function() {;};

(function($) {
    $(function() {
        var orig_template = $('#id_template').val();

        $('.changing-page #id_template').change(function() {
            var resp = confirm('Are you sure you want to change the template?' +
                               '\n\n' +
                               'The page will be saved and any content sections not present in the ' +
                               'new template will be lost!');

            if (resp === true) {
                $('input[name=_continue]').click();
            } else {
                $('#id_template').val(orig_template);
            }
        });

        $('.changelist-results tbody tr th a').wrap('<div class="stoat-row" />');
        $('.changelist-results tbody tr th .stoat-row').each(function() {
            $(this).append('<div class="drag-handle">Move</div>');

            var indent = $(this).find('.indent').html();
            var has_child = $(this).find('.has-child').text();
            var first_child = $(this).find('.first-child').text();

            var above_class = first_child === '1' ? ' first-child ' : '';
            $(this).prepend('<div class="drop drop-above ' + above_class + '"><div class="indent">' + indent + '</div><div class="border">&nbsp;</div></div>');

            if (has_child === '0') {
                $(this).prepend('<div class="drop drop-below"><div class="indent">' + indent + '</div><div class="border">&nbsp;</div></div>');
            };

            $(this).prepend('<div class="drop drop-inside"><div class="indent">' + indent + '</div><div class="child">↳</div></div>');
        });
        $('.drag-handle').draggable({
            containment: 'table',
            revert: 'invalid',
        });

        var droppable_options = {
            hoverClass: "drop-hover",
            activeClass: "drop-active",
            accept: function(el) {
                var drop_id = "" + $(this).closest('tr').find('.action-select').val();
                var drag_id = "" + $(el).closest('tr').find('.action-select').val();

                var descendants = $(el).closest('tr').find('.descendants').text().split(',');

                if (drop_id === drag_id) {
                    return false;
                }
                if ($.inArray(drop_id, descendants) !== -1) {
                    return false;
                }

                return true;
            },
            greedy: true,
        };

        var update_drop_form = function(dragging, drop_onto, method) {
            var drop_id = drop_onto.closest('tr').find('.action-select').val();
            var drag_id = dragging.closest('tr').find('.action-select').val();

            $('form#move-page .page').val(drag_id);
            $('form#move-page .target').val(drop_id);
            $('form#move-page .position').val(method);

            $('form#move-page').submit();
        };

        var drop_above_options = {
            drop: function(event, ui) {
                update_drop_form($(ui.draggable), $(this), 'above');
            }
        };
        var drop_below_options = {
            drop: function(event, ui) {
                update_drop_form($(ui.draggable), $(this), 'below');
            }
        };
        var drop_inside_options = {
            drop: function(event, ui) {
                update_drop_form($(ui.draggable), $(this), 'inside');
            }
        };

        $.extend(drop_above_options, droppable_options);
        $.extend(drop_below_options, droppable_options);
        $.extend(drop_inside_options, droppable_options);

        $('.drop-above').droppable(drop_above_options);
        $('.drop-below').droppable(drop_below_options);
        $('.drop-inside').droppable(drop_inside_options);

    });
})(django.jQuery);
