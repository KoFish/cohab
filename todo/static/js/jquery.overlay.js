(function($) {
    var methods = {
        init : function(options) {
            var settings = $.extend({
                                'startsize': 10,
                                'endsize': 20,
                                'fadespeed': 300},
                                options);
            return $.when.apply(null, this.map(function() {
                var $obj = $(this),
                    promise = new $.Deferred(),
                    pos = $.extend({
                        width: $obj.outerWidth(),
                        height: $obj.outerHeight()
                    }, $obj.position()),
                    sz = settings.startsize,
                    $pre = $('<div />', {'class': 'pre-overlay'})
                                .css({
                                    position: 'absolute',
                                    top: pos.top,
                                    left: pos.left,
                                    width: pos.width,
                                    height: pos.height,
                                    backgroundColor: '#000',
                                    opacity: 0.0})
                                .appendTo($obj);
                $('<div />', {
                    'class': 'overlay',
                    'data-fadespeed': settings.fadespeed,
                    'data-endsize': settings.endsize})
                    .css({
                        position: 'absolute',
                        top: pos.top - sz,
                        left: pos.left - sz,
                        width: pos.width + sz*2,
                        height: pos.height + sz*2,
                        backgroundColor: '#000',
                        opacity: 0.0
                    }).animate({
                        opacity: 0.5,
                        top: pos.top,
                        left: pos.left,
                        width: pos.width,
                        height: pos.height
                    }, settings.fadespeed, function() {
                        $pre.remove();
                        promise.resolve();
                    }).appendTo($obj);
                return promise;
            }).get());
        },
        destroy : function() {
            if ($(this).children('.overlay').length === 0) {
                return $.when();
            }
            return $.when.apply(null, this.map(function() {
                var $obj = $(this),
                    promise = new $.Deferred();
                    pos = $.extend({
                        width: $obj.outerWidth(),
                        height: $obj.outerHeight()
                    }, $obj.position()),
                    $overlay = $obj.children('.overlay'),
                    speed = $overlay.data('fadespeed'),
                    endsize = $overlay.data('endsize');
                $overlay.animate({
                    opacity: 0.0,
                    top: pos.top - endsize,
                    left: pos.left - endsize,
                    width: pos.width + 2*endsize,
                    height: pos.height + 2*endsize
                }, speed, function() {
                    $(this).remove();
                    promise.resolve();
                });
                return promise;
            }).get());
        }
    };
    $.fn.overlay = function(method, callback) {
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || ! method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Method ' + method + ' does not exist on jQuery.overlay');
        }
    };
})(jQuery);
