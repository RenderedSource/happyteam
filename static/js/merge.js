(function($) {
    $(function() {
        $('.btn-merge-request').live('click', function(event) {
            event.preventDefault();

            var $button = $(this);
            var $form = $(this).parents('form:first');
            var data = $form.serialize();
            var url = $form.attr('action');

            $.post(url, data, function(response) {
                if (response.success) {
                    $('#mergelist').prepend(response.html);
                } else {
                    console.log(response);
                }
            }, 'json')
            .fail(function() {
                alert('Error');
            });
        });

        $('.btn-merge-action').live('click', function(event) {
            event.preventDefault();

            var $button = $(this);
            var $form = $(this).parents('form:first');
            var data = $form.serialize();
            var url = $form.attr('action');
            var action = $button.data('action');

            data += '&action_code=' + action;

            $.post(url, data, function(response) {
                if (response.success) {
                    $('#action-list-' + response.merge_id).html(response.actions_html);
                    $('#merge-head-' + response.merge_id).html(response.head_html);
                    $('#action-buttons-' + response.merge_id).html(response.buttons_html);
                } else {
                    console.log(response);
                }
            }, 'json').fail(function() {
                alert('Error');
            });
        });
    });
})(jQuery);


