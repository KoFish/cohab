(function($) {
    $.fn.setupTask = function() {
        return this.each(function() {
            var $task = $(this);
            if ( $task.data('task-is-setup') ) return;
            $task.data('task-is-setup', true);
            $task.find('.task-btns .task-btn').each(function() {
                var url = $(this).attr('href'),
                    $btn = $(this);
                $(this).click(function(e) {
                    e.preventDefault();
                    $('.todo-task').overlay("destroy")
                    .then(function() {
                        $task.overlay({'startsize': 10, 'endsize': 50, 'fadespeed': 1000})
                        .then(function() {
                            $.getJSON(url)
                            .success(function(data) {
                                //$task.remove();
                                $task.overlay("destroy")
                                .then(function() {
                                    location.reload();
                                });
                            })
                            .error(function(err) {
                                $task.overlay("destroy");
                                $task.popover({
                                    'placement': 'bottom',
                                    'trigger': 'manual',
                                    'title': 'Failed '+$btn.text(),
                                    'text': err
                                }).popover('show');
                                console.log("Couldn't fetch url:");
                                console.log(err);
                            });
                        });
                    });
                });
            });
        });
    };
})(jQuery);

function getHashes() {
    return _.filter(location.hash.split('#'), function(s) { return s !== ''; });
}

(function($) {
    $.fn.folder = function() {
        return this.each(function() {
            var $this = $(this),
                $foldee = $($this.data('foldee'));
            $foldee.hide();
            $this.click(function(e) {
                var id = $this.attr('id');
                e.preventDefault();
                if ($foldee.hasClass('open')) {
                    $foldee.removeClass('open')
                           .slideUp("fast");
                    location.hash = _.filter(getHashes(), function(e) { return e !== id; }).join('#');
                    return;
                } else {
                    $foldee.addClass('open');
                }
                $.get($this.attr('href'), function(data) {
                    $foldee.html(data).bootstrap().slideDown("fast");
                    location.hash = _.filter(getHashes(), function(e) { return e !== id; }).concat([id]).join('#');
                });
            });
        });
    };
})(jQuery);

(function($) {
    $.fn.bootstrap = function() {
        return this.each(function() {
            var $this = $(this);
            $this.find('.todo-task').setupTask();
            $this.find('.todo-task.active').taskCounter({max: 5});
            $this.find('a.login').loginModal();
            $this.find('.url-folder').folder();
            $this.find('.todo-list-task a.foldout-toggle').each(function() {
                var $this = $(this),
                    foldee = $($this.data('foldee'));
                $this.click(function(e) {
                    e.preventDefault();
                    if (foldee.hasClass('hide')) {
                        foldee.slideDown(100, function() { $(this).removeClass('hide'); });
                    } else {
                        foldee.slideUp(100, function() { $(this).addClass('hide'); });
                    }
                });
            });
            $this.find('time.timeago').timeago();
            $this.find('time[datetime]').each(function() {
                $(this).tooltip({
                    animation: true,
                    html: $(this).attr('datetime'),
                    trigger: 'hover',
                    placement: 'top'
                });
            });
        });
    };
})(jQuery);

$(document).ready(function() {
    $.timeago.settings.allowFuture = true;
    $('body').bootstrap();
    _.each(getHashes(), function(e, i) {
        $('#'+e).click();
    });
});
