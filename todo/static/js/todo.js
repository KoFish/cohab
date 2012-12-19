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
                    console.log($task);
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

$(document).ready(function() {
    $('.todo-task').setupTask();
    $('.todo-task.active').taskCounter({max: 5});
    $('a.login').loginModal();
});
