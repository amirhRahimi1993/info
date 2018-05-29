function upload(event) {
        event.preventDefault();
        var data = new FormData($('form').get(0));
        alert($('form').get(0))
        $.ajax({
            url: 'ajax/basic_upload/',
            type: $(this).attr('method'),
            data : data,
            cache: false,
            processData: false,
            contentType: false,
            success: function (data) {
                alert(data.path);
            }
        });
        return false;
    }

    $(function () {
        $('form').submit(upload);
    });