(function($) {
    $.fn.loginModal = function(options) {
        var settings = $.extend({
        }, options);
        return $.when(this.map(function() {
            var $this = $(this),
                url = $this.attr('href');
            $this.click(function(e) {
                e.preventDefault();
                $('<div />', {'id': 'loginModal',
                                    'class': 'modal hide fade',
                                    'role': 'dialog',
                                    'aria-labelledby': 'loginLabel'})
                .append($('<div />', {'class': 'modal-header'})
                    .append($('<button />', {'class': 'close', 'data-dismiss': 'modal'}).text('x')))
                .append($('<div />', {'class': 'modal-body'})
                    .text('Loading'))
                .appendTo('body');
                $('#loginModal').modal({'keyboard': false, 'backdrop': 'static'}).modal('show');
                function setupModal(data) {
                    var $modal = $('#loginModal');
                    $modal
                        .find('.modal-body')
                            .html(data).end()
                        .find('.modal-header')
                            .find('h3').remove().end()
                            .append($('<h3 />', {'id': 'loginLabel'}).text($modal.find('legend').text())).end()
                        .find('legend')
                            .remove().end()
                        .on('hidden', function() { $modal.remove(); })
                        .find('.abort.btn').click(function(e) {
                                    e.preventDefault();
                                    $('#loginModal').modal('hide');
                                }).end()
                        .find('form')
                            .submit(function(e) {
                                var $this = $(this),
                                    data = $this.serialize(),
                                    url = $this.attr('action');
                                e.preventDefault();
                                $.post(url, data)
                                .done(function(data, textStatus, jqXHR) {
                                    if (data instanceof Object) {
                                        if (data.status == "success") {
                                            $modal.on('hidden', function() { location.reload(); }).modal('hide');
                                            return;
                                        }
                                    }
                                    setupModal(data);
                                });

                            });
                }
                $.get(url).done(function(data) {
                    setupModal(data); 
                });
            });
            console.log(url);
        }));
    };
})(jQuery);
