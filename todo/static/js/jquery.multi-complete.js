(function($) {
    var methods = {
        init : function(options) {
            var settings = $.extend({
            }, options);
            return this.each(function() {
                var $this = $(this),
                    name = $this.attr('id'),
                    url = $this.data('url'),
                    data = $this.data('multiComplete');
                if ( ! data && $this.has('li').length > 0) {
                    $this.wrap('<form id="' + name + '-form" />')
                         .append('<input type="hidden" name="csrfmiddlewaretoken" value="' + getCookie('csrftoken') + '">')
                         .children('li').each(function() {
                             var $child = $(this),
                                 taskId = $child.find('.task').data('id');
                             $child.prepend('<input name="complete" value="' + taskId + '" type="checkbox">')
                             .change(function() {
                                 var $btn = $this.find('#' + name + '-btn');
                                 if ($this.has('input:checked').length > 0) {
                                     $btn.removeAttr('disabled');
                                 } else {
                                     $btn.attr('disabled', 'disabled');
                                 }
                             });
                         }).end()
                         .append('<button type="submit" id="' + name + '-btn" class="btn mini-btn" disabled="disabled">Complete</button>');
                    $this.find('#' + name + '-btn').click(function() {
                             var $form = $(this).parents('form');
                             $.post(url, $form.serialize())
                                .always(function(data) {
                                    $.reload($this);
                                });
                             return false;
                         });
                    $this.data('multiComplete', {});
                }
            });
        }
    };
    $.fn.multiComplete = function(method) {
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || ! method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Method ' + method + ' does not exist on jQuery.multiComplete');
        }
    };
})(jQuery);
