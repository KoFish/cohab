jQuery.reload = function(obj) {
    var $reloadPoint = obj.closest('.fold-target, .reload-target');
    if ($reloadPoint.length > 0) {
        $reloadPoint = $reloadPoint.first();
        if ($reloadPoint.hasClass('fold-target')) {
            $reloadPoint.folder("update");
        } else if ($reloadPoint.hasClass('reload-target')) {
            var url = $reloadPoint.data('url');
            $.get(url)
                .done(function(data) {
                    $reloadPoint.html(data).bootstrap();
                })
                .fail(function(err) {
                    $.error("Could not reload data: " + err);
                });
        }
    } else {
        _.defer(function() { location.reload(); });
    }
};

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
                    $task.overlay({'startsize': 10, 'endsize': 50, 'fadespeed': 300})
                    .then(function() {
                        $.getJSON(url)
                        .success(function(data) {
                            $.reload($task);
                            $task.overlay("destroy").then(function() { $.reload($task); });
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
    };
})(jQuery);

var Hash = {
    getHashes: function() {
        return _.filter(location.hash.split('#'), function(s) { return s !== ''; });
    },
    addHash: function(hash) {
        location.hash = _.filter(Hash.getHashes(), function(e) { return e !== hash; }).concat([hash]).join('#');
    },
    removeHash: function(hash) {
        location.hash = _.filter(Hash.getHashes(), function(e) { return e !== hash; }).join('#');
    }
};

(function($) {
    var methods = {
        init : function(options) {
            var settings = $.extend({
            }, options);

            return this.each(function() {
                var $this = $(this),
                    $foldee = $($this.data('foldee')),
                    data = $foldee.data('folder');
                if ( ! data ) {
                    $foldee.hide();
                    $foldee.data('folder', {'fold-id': $this.attr('id')});
                    $this.click(function(e) {
                        e.preventDefault();
                        if ($foldee.hasClass('open')) {
                            $foldee.folder('fold');
                        } else {
                            $foldee.folder('unfold');
                        }
                    });
                }
            });
        },
        fold : function() {
            var $foldee = $(this),
                data = $foldee.data('folder');
            if ( data ) {
                var id = data['fold-id'];
                Hash.removeHash(id);
                $foldee.removeClass('open').slideUp("fast");
            }
        },
        unfold : function() {
            var $foldee = $(this),
                data = $foldee.data('folder');
            if ( data ) {
                var id = data['fold-id'];
                $foldee.addClass('open');
                Hash.addHash(id);
                $foldee.folder('update');
            }
        },
        update : function() {
            var $foldee = $(this),
                data = $foldee.data('folder');
            if ( data ) {
                var id = data['fold-id'];
                if ($foldee.hasClass('open')) {
                    $foldee.overlay({fadespeed: $foldee.is(':visible') ? 300 : 0}).then(function() {
                        $.get($foldee.data('url'), function(data) {
                            var overlay = $foldee.find('.overlay').detach();
                            $foldee.html(data).bootstrap().slideDown("fast");
                            $foldee.append(overlay);
                            $foldee.overlay('destroy');
                        });
                    });
                } else {
                    $foldee.folder('unfold');
                }
            }
        }
    };
    $.fn.folder = function(method) {
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || ! method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Method ' + method + ' does not exist on jQuery.folder');
        }
    };
})(jQuery);

(function($) {
    $.fn.bootstrap = function() {
        return this.each(function() {
            var $this = $(this);
            $this.find('.todo-task').setupTask();
            $this.find('.todo-task.active').taskCounter({max: 5});
            $this.find('a.login').loginModal();
            $this.find('.add-task-btn').taskModal();
            $this.find('.url-folder').folder();
            $this.find('.multi-complete').multiComplete();
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
    _.each(Hash.getHashes(), function(e, i) {
        $('#'+e).click();
    });
});
