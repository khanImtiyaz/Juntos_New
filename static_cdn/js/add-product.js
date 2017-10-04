$(document).ready(function() {
    $("#product_quantity_id").blur(function() {
        var val = $("#product_quantity_id").val();
        if (val > 0) {
            $("#id_in_stock").prop("checked", true)
        } else {
            $("#id_in_stock").prop("checked", false)
        }
    });
    $("#id_category").on("change", function() {
        $.ajax({
            url: "{% url 'Vendor:subcategories'%}",
            type: 'POST',
            dataType: 'json',
            data: {
                category_id: this.value,
                'csrfmiddlewaretoken': '{{ csrf_token }}',
            },
            success: function(e) {
                var str1 = "<option value=''>Select Sub Category</option>";
                var str = "";
                $(e.data).each(function(index, value) {
                    str += "<option value =" + value['id'] + ">" + value['sub_category_name'] + "</option>"
                });
                $("#id_subs_category").empty().append(str1 + str);
            }
        });
    });
    $("#id_subs_category").change(function() {
        subcategory_id = parseInt($("#id_subs_category").val());
        $.ajax({
            url: "{% url 'Vendor:subcategory-tag'%}",
            type: 'POST',
            dataType: 'json',
            data: {
                'subcategory_id': subcategory_id,
                'csrfmiddlewaretoken': '{{ csrf_token }}',
            },
            success: function(e) {
                if (e.data == 'CP') {
                    $("#id_feature").css({
                        'display': 'none'
                    });
                    $("#sub_tag").text(e.data);
                    $(".add_field_button").removeAttr('style');
                } else {
                    $(".input_fields_wrap").empty();
                    $(".add_field_button").css({
                        'display': 'none'
                    });
                    $("#id_feature").removeAttr('style');
                    $("#sub_tag").text(e.data);
                }
            }
        });
    });
    removePhoto = function(index) {
        alert(index)
    }
    multiple_Image_Array = []
    $("#image_upload").on('change', function() {
        var countFiles = $(this)[0].files.length;
        var imgPath = $(this)[0].value;
        var extn = imgPath.substring(imgPath.lastIndexOf('.') + 1).toLowerCase();
        var image_holder = $("#image_preview");
        if (extn == "gif" || extn == "png" || extn == "jpg" || extn == "jpeg") {
            if (typeof(FileReader) != "undefined") {
                for (var i = 0; i < countFiles; i++) {
                    var reader = new FileReader();
                    reader.onload = function(e) {
                        image_holder.empty();
                        $("<img />", {
                            "src": e.target.result,
                            "class": "thumb-image"
                        }).appendTo(image_holder);
                        multiple_Image_Array.push(e.target.result)
                        $("#multiple_image_show").append('<div class="col-sm-2" id="remove_photo_' + multiple_Image_Array.length + '" onClick=removePhoto("remove_photo_"' + multiple_Image_Array.length + ');><div><i class="fa fa-times" aria-hidden="true" style="color:black;float:right"></i><img src="' + e.target.result + '"%}" style="height:40px;width: 100%"></div></div>')
                    }
                    image_holder.show();
                    reader.readAsDataURL($(this)[0].files[i]);
                }
            } else {
                alert("This browser does not support FileReader.");
            }
        } else {
            Lobibox.alert('error', {
                sound: false,
                msg: 'Favor de subir imagen válida.'
            });
            this.value = "";
        }
    });
    var max_fields = 5; //maximum input boxes allowed
    var wrapper = $(".input_fields_wrap"); //Fields wrapper
    var add_button = $(".add_field_button"); //Add button ID
    var x = 1; //initlal text box count
    $(add_button).click(function(e) { //on add input button click
        e.preventDefault();
        if (x < max_fields) {
            x++; //text box increment
            $(wrapper).append('<div><hr>\
   									<div class="form-group"> \
   									    <label class="control-label col-sm-3">Product Color</label> \
   									    <div class="col-sm-9"> \
   									      <input id="id_product_colors-' + (x - 2) + '-color" class="colorfield_field"\
   												 name="product_colors-' + (x - 2) + '-color" value="#FF0000" type="color"> \
   									    <div class="form-group">\
   									    <label class="control-label col-sm-3">Product Color Image</label>\
   											<a href="#" class="add_color_image btn btn-success btn-sm" >Add Image ➕</a>\
   												<ol class="col-sm-9 product_images" >\
   									      </ol>\
   									   </div>\
   									</div></div>\
   									 <a href="#" class="remove_color_field btn btn-danger btn-sm">Remove Color ❌</a>\
   									 </div>'); //add input box
        } else {
            $(".add_field_button").css({
                'display': 'none'
            });
        }
        $("#id_total_color").val(x - 1);
    });

    $(wrapper).on("click", ".remove_color_field", function(e) { //user click on remove text
        e.preventDefault();
        $(this).parent('div').remove();
        x--;
        $(".add_field_button").css({
            'display': 'block'
        });
        $("#id_total_color").val(x - 1);
    })
    var max_fields_img = 17; //maximum input boxes allowed
    var y = 1; //initlal text box count
    $(wrapper).on("click", ".add_color_image", function(e) { //on add input button click
        e.preventDefault();
        if (y < max_fields_img) { //max input box allowed
            y++; //text box increment
            $(this).parent().find('.product_images').append('<div><li>\
   									<input type="file" name="product_colors-' + (x - 2) + '-product_color_images-' + (y - 2) + '-product_images" \
   									 onChange="validate(this)" required="">\
   								 </li> <a href="#" class="remove_color_field1 btn btn-danger btn-xs">Remove ❌</a></div>'); //add input box
        }
        $("#id_total_color_images").val(y - 1);
    });
    $(wrapper).on("click", ".remove_color_field1", function(e) { //user click on remove text
        e.preventDefault();
        $(this).parent('div').remove();
        y--;
        $("#id_total_color_images").val(y - 1);
    });
    $('#product_form').submit(function(e) {
        if ($("#sub_tag").text() == "CP") {
            color_counter = $("#id_total_color").val();
            image_counter = $("#id_total_color_images").val();
            if (color_counter <= 0) {
                e.preventDefault();
                $(".add_field_button").css({
                    'border-color': 'red',
                    'box-shadow': '0 1px 8px 1px red'
                });
                $(".add_field_button").focus();
                Lobibox.alert('warning', {
                    showClass: 'fadeInDown',
                    hideClass: 'fadeUpDown',
                    sound: false,
                    position: 'center',
                    msg: 'Please add atleast one color for this product !'
                });
                return false;
            } else {
                if (image_counter <= 0) {
                    e.preventDefault();
                    $(".add_color_image").css({
                        'border-color': 'red',
                        'box-shadow': '0 1px 8px 1px red'
                    });
                    $(".add_color_image").focus();
                    Lobibox.notify('error', {
                        showClass: 'fadeInDown',
                        hideClass: 'fadeUpDown',
                        sound: false,
                        msg: 'Please add atleast one image for this color !'
                    });
                    return false;
                } else {
                    return true;
                }
            }
        }
    });
    function validate(file) {
        var ext = file.value.split(".");
        ext = ext[ext.length - 1].toLowerCase();
        var arrayExtensions = ["jpg", "jpeg", "png", "bmp", "gif", ];
        if (arrayExtensions.lastIndexOf(ext) == -1) {
            file.value = "";
            Lobibox.alert('error', {
                sound: false,
                msg: 'Favor de subir imagen válida.'
            });
            return false;
        }
    };
    CKEDITOR.replace('description');
    CKEDITOR.replace('feature', {
        height: 100,
        resize_dir: 'both',
        resize_minWidth: 200,
        resize_minHeight: 300,
        resize_maxWidth: 800
    });
    CKEDITOR.replace('services', {
        height: 100,
        resize_dir: 'both',
        resize_minWidth: 200,
        resize_minHeight: 300,
        resize_maxWidth: 800
    });
})