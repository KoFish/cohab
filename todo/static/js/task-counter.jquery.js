(function($) {
    var methods = {
        init : function(options) {
            var settings = $.extend({
                    'max': 7
                }, options);
            return this.each(function() {
                var $this = $(this),
                    data = $this.data('taskCounter'),
                    counter = $('<div />', { 'id': $this.attr('id')+'-counter', 'class': 'task-counter' });
                if ( ! data ) {
                    var settings = $.extend({
                        'counter-value': 'days-left'
                    }, options),
                        dot = $('<span />').css({height: 10, width: 10, display: "inline-block", margin: 2}),
                        counterValue = $this.data(settings['counter-value']);

                    console.log($this);
                    if (counterValue === undefined) {
                        return;
                    }

                    if (counterValue > settings.max) {
                        $('<span />').css({
                            width: 21,
                            borderBottom: 'dotted #555 3px',
                            display: 'inline-block',
                            margin: 5
                        }).appendTo(counter);
                    }

                    counter.css({
                        position: 'absolute',
                        top: 0,
                        right: 2 
                    }).appendTo($this);
                    for(var i = 0 ; i > counterValue + 1 ; i--) {
                        dot.clone().css({backgroundColor: '#f00'}).appendTo(counter);
                    }
                    for(i = 0 ; i < Math.min(counterValue + 1, settings.max) ; i++) {
                        dot.clone().css({backgroundColor: '#000'}).appendTo(counter);
                    }

                    $(this).data('taskCounter', {
                        'counter-value': settings['counter-value'],
                        'counter': counter
                    });
                }
            });
        },
        destroy : function() {
            return this.each(function() {
                var $this = $(this),
                    data = $this.data('taskCounter');
                if (data) {
                    data.counter.remove();
                    $this.removeData('taskCounter');
                }
            });
        }
    };
    $.fn.taskCounter = function(method) {
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || ! method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Method ' + method + ' does not exist on jQuery.taskCounter');
        }
    };
})(jQuery);
