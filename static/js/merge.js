(function($, undefined) {
    $(function() {

        (function() {
            var regex = /^\/merge\/(\d+)/i;
            var match = regex.exec(document.location.pathname);
            if (match) {
                var mergeId = parseInt(match[1]);
                var offset = $('#merge-head-' + mergeId).offset().top - 40;
                $('html, body').scrollTop(offset);
            }
        })();

        function toggleCollapse(mergeId, animated) {
            var $subrow = $('#merge-actions-' + mergeId);
            if (!$subrow.hasClass('in')) {
                animated ? $('.merge-actions.in').collapse('hide') : $('.merge-actions.in').removeClass('in');
            }
            animated ? $subrow.collapse('toggle') : $subrow.toggleClass('in');
        }

        function toggleActions($link, animated, callback) {
            (animated === undefined) && (animated = true);
            var mergeId = parseInt($link.data('merge-id'));
            var $subrow = $('#merge-actions-' + mergeId);
            if ($subrow.hasClass('in')) {
                history.pushState({}, '', '/merge/');
            } else {
                history.pushState({mergeRequestId: mergeId}, '', '/merge/' + mergeId);
            }
            if ($subrow.children().length == 0) {
                $link.hide();
                $link.after('<div class="ajax-loader"></div>');
                $.get('merge-details/' + mergeId, function(response) {
                    $subrow.html(response);
                    $subrow.find('.btn').button();
                    toggleCollapse(mergeId, animated);
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
                toggleCollapse(mergeId, animated);
            }
        }

        window.addEventListener('popstate', function(e) {
            if (e.state) {
                e.state.mergeRequestId
                    ? toggleCollapse(e.state.mergeRequestId, true)
                    : $('.merge-actions.in').collapse('hide');
            }
        }, false);

        // preload ajax loader image
        $('<img/>')[0].src = '/static/img/nyancat.gif';
      
        // function send filter
        function sendFilter(){
            $.get('', $form.serialize(), function(response) {
                $('#mergelist-container').html(response);
            })
            .fail(function() {
               alert('Error');
            });
        }
        var $form = $('#form-filter');
        // filter by click checkbox
        // BUG: work on by click another checkbox
        $form.find('input[type="checkbox"]').change(function() {
            sendFilter();
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
        // refresh request list
        $('#refresh').on('click', function(){
            sendFilter();
        });
        // clear filters
        $('#clear-filters').on('click', function(){
            $('#form-filter input[type=checkbox]').attr('checked',null);
            sendFilter();
        });
        //git fetch and refresh branch
        var branchList = $('#id_branch');
        var button =  $('#fetch');

        var normal_text = button.html();
        button.on('click', function(){
            button.html('Loading...').attr('disabled','disabled');
            branchList.find('option').remove();

            $.ajax({
                url: '/merge/getbranch/',
                dataType: 'json',
                success: function(data){
                    $.each(data, function(index, value){
                        branchList.append('<option value="' + value + '">' + value + '</option>')
                    });
                    button.html(normal_text).attr('disabled', false);
                }
            })
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


