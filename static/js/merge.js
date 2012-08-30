(function($) {
    $(function() {
        $('.btn-merge-request').click(function(event) {
            event.preventDefault();

            var $button = $(this);
            var $form = $(this).parents('form:first');
            var data = $form.serialize();
            var url = $form.attr('action');

            $.post(url, data, function(response) {
                if (response.success) {
                    window.location.reload();
                } else {
                    console.log(response);
                }
            }, 'json').fail(function() {
                    alert('Error');
                });
        });

        $('.btn-merge-action').click(function(event) {
            event.preventDefault();

            var $button = $(this);
            var $form = $(this).parents('form:first');
            var data = $form.serialize();
            var url = $form.attr('action');
            var action = $button.data('action');

            data += '&status=' + action;

            $.post(url, data, function(response) {
                if (response.success) {
                    window.location.reload();
                } else {
                    console.log(response);
                }
            }, 'json').fail(function() {
                alert('Error');
            });
        });
    });
})(jQuery);


