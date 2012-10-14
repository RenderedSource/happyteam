(function($) {
    $(function() {

        function toggleActions($link, animated, callback) {
            (typeof animated === 'undefined') && (animated = true);
            var mergeId = parseInt($link.data('merge-id'));
            var $subrow = $('#merge-actions-' + mergeId);
            if ($subrow.children().length == 0) {
                $link.hide();
                $link.after('<div class="ajax-loader"></div>');
                $.get('merge-details/' + mergeId, function(response) {
                    $subrow.html(response);
                    $subrow.find('.btn').button();
                    if (animated) {
                        $subrow.collapse('toggle');
                    } else {
                        $subrow.toggleClass('in');
                    }
                    callback && callback();
                })
                .fail(function() {
                    alert('Error');
                })
                .complete(function() {
                    $link.next('.ajax-loader').remove();
                    $link.show();
                });
            } else {
                if (animated) {
                    $subrow.collapse('toggle');
                } else {
                    $subrow.toggleClass('in');
                }
            }
        }

        // preload ajax loader image
        $('<img/>')[0].src = '/static/img/nyancat.gif';

        var $form = $('#form-filter');
        $form.find('input[type="checkbox"]').change(function() {
            $.get('', $form.serialize(), function(response) {
                $('#mergelist-container').html(response);
            })
            .fail(function() {
                alert('Error');
            });
        });

        $('.btn-toggle-actions').live('click', function(event) {
            toggleActions($(this));
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

        (function() {
            var hash = window.location.hash;
            if (hash && hash.length > 1) {
                var mergeId = parseInt(hash.substr(1));
                if (!isNaN(mergeId)) {
                    var $row = $('#merge-head-' + mergeId);
                    var $link = $row.find('.btn-toggle-actions');
                    toggleActions($link, false, function() {
                        var scroll = $row.offset().top;
                        $(window).scrollTop(scroll - 38);
                    });
                }
            }
        })();
    });
})(jQuery);


