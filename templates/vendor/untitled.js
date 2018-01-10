$("#image").on('change', function() {
    var file = $(this).val();
    var image_holder = $("#image_preview");
    var reader = new FileReader();
    reader.onload = function(e) {
        image_holder.empty();
        $("<img />", {
            "src": e.target.result,
            "class": "thumb-image"
        }).appendTo(image_holder);
        multiple_Image_Array.push(e.target.result)
        $("#product_image").append('<div class="col-sm-2" id="remove_photo_business"><div><i class="fa fa-times" aria-hidden="true" style="color:black;float:right;display:none;"></i><img src="' + e.target.result + '"%}" style="width: 100%;padding-top:20px;"></div></div>')
    }
    image_holder.show();
    reader.readAsDataURL(file);
    $('.file-preview-input').append($('#image').clone({ withDataAndEvents: true}));
});