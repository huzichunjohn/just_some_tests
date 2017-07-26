$(function () {
    // $(document).bind('dragover', function (e) {
    //    var dropZone = $("#dropzone"),
    //        timeout = window.dropZoneTimeout;
    //    if (timeout) {
    //        clearTimeout(timeout);
    //    } else {
    //        dropZone.addClass('in');
    //    }
    //    var hoveredDropZone = $(e.target).closest(dropZone);
    //    dropZone.toggleClass('hover', hoveredDropZone.length);
    //    window.dropZoneTimeout = setTimeout(function () {
    //        window.dropZoneTimeout = null;
    //        dropZone.removeClass('in hover');
    //    }, 100);
    // });
    $(document).bind('drop dragover', function (e) {
        e.preventDefault();
    });

    $(".js-upload-photos").click(function () {
        $("#fileupload").click();
    });

    $("#fileupload").fileupload({
        dropZone: $("#dropzone"),
        dataType: 'json',
        sequentialUploads: true,
        start: function (e) {
            $("#modal-progress").modal("show");
        },
        stop: function (e) {
            $("#modal-progress").modal("hide");
        },
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            var strProgress = progress + "%";
            $(".progress-bar").css({"width": strProgress});
            $(".progress-bar").text(strProgress);
        },
        done: function (e, data) {
            if (data.result.is_valid) {
                $("#gallery tbody").prepend(
                    "<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a></td></tr>"
                )
            }
        }
    });
});
