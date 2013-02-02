(function($) {
    $.fn.taskModal = function(options) {
        var settings = $.extend({
        }, options);
        return $.when(this.map(function() {
            var $this = $(this),
                url = $this.attr('href');
            $this.click(function(e) {
                e.preventDefault();
                $('<div />', {'id': 'taskModal',
                                    'class': 'modal hide fade',
                                    'role': 'dialog',
                                    'aria-labelledby': 'taskLabel'})
                .append($('<div />', {'class': 'modal-header'})
                    .append($('<button />', {'class': 'close', 'data-dismiss': 'modal'}).text('x')))
                .append($('<div />', {'class': 'modal-body'})
                    .text('Loading'))
                .insertAfter($this.closest('.fold-target, body').first());
                $('#taskModal').modal({'keyboard': false, 'backdrop': 'static'}).modal('show');

                function updateForm() {
                    var $modal = this;
                    function doUpdate() {
                        var $this = $(this),
                            has_area = $this.data('has-area'),
                            has_object = $this.data('has-object');
                        $modal.find('#area-group')
                                .each(function() {
                                    if (has_area) {
                                        $(this).show();
                                    } else {
                                        $(this).hide();
                                    }
                                }).end()
                              .find('#object-group')
                                .each(function() {
                                    if (has_object) {
                                        $(this).show();
                                    } else {
                                        $(this).hide();
                                    }
                                }).end();
                    }
                    $modal.find('#action option:selected').each(function() {
                        doUpdate.call($(this));
                    }).end()
                    .find('#action[type=hidden]').each(function() {
                        doUpdate.call($(this));
                    });
                }

                function setupModal(data) {
                    var $modal = $('#taskModal'),
                        $parent = $modal.prev();
                    $modal
                        .on('hidden', function() { $modal.remove(); })
                        .find('.modal-body')
                            .html(data).end()
                        .find('.modal-header')
                            .find('h3').remove().end()
                            .append($('<h3 />', {'id': 'taskLabel'}).text($modal.find('legend').text())).end()
                        .find('legend')
                            .remove().end()
                        .find('#action')
                            .change(function() {
                                updateForm.call($modal);
                            }).end()
                        .find('.abort.btn').click(function(e) {
                                    e.preventDefault();
                                    $('#taskModal').modal('hide');
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
                                            $.reload($parent);
                                            $modal.modal('hide');
                                            return;
                                        }
                                    }
                                    setupModal(data);
                                });

                            }).end()
                        .find('.jdpicker').jdPicker();
                    updateForm.call($modal);
                }
                $.get(url).done(function(data) {
                    setupModal(data); 
                });
            });
        }));
    };
})(jQuery);
