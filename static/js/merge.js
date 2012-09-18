(function($) {
    $(function() {
        // preload ajax loader image
        $('<img/>')[0].src = '/static/img/nyancat.gif';

        $('.btn-toggle-actions').live('click', function(event) {
            var $link = $(this);
            var mergeId = parseInt($link.data('merge-id'));
            var $subrow = $('#merge-actions-' + mergeId);
            if ($subrow.children().length == 0) {
                $link.hide();
                $link.after('<div class="ajax-loader"></div>');
                $.get('merge-details/' + mergeId, function(response) {
                    $subrow.html(response);
                    $subrow.find('.btn').button();
                    $subrow.collapse('toggle');
                })
                .fail(function() {
                    alert('Error');
                })
                .complete(function() {
                    $link.next('.ajax-loader').remove();
                    $link.show();
                });
            } else {
                $subrow.collapse('toggle');
            }
        });

        $('.btn-merge-request').live('click', function(event) {
            event.preventDefault();

            var $button = $(this);
            var $form = $(this).parents('form:first');
            var data = $form.serialize();
            var url = $form.attr('action');

            $.post(url, data, function(response) {
                if (response.success) {
                    var $mergelist = $('#mergelist');
                    $mergelist.find('.row-no-data').remove();
                    $mergelist.prepend(response.html);
                } else {
                    console.log(response);
                }
            }, 'json')
            .fail(function() {
                alert('Error');
            });
        });

        $('.btn-update-merge').live('click', function(event) {
            event.preventDefault();

            var $button = $(this);
            var $form = $(this).parents('form:first');
            var data = $form.serialize();
            var url = $form.attr('action');
            var action = $button.data('action');

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

        $('.btn-post-comment').live('click', function(event) {
            event.preventDefault();

            var $button = $(this);
            var $form = $(this).parents('form:first');
            var data = $form.serialize();
            var url = $form.attr('action');

            $.post(url, data, function(response) {
                if (response.success) {
                    $('#action-comments-' + response.action_id).html(response.comments_html);
                    $('#action-comment-count-' + response.action_id).html(response.comment_count_html);
                } else {
                    console.log(response);
                }
            }, 'json').fail(function() {
                alert('Error');
            });
        });
    });
})(jQuery);


