// 当有文件添加进来的时候
uploader.on('fileQueued', function( file ) {
    var $li = $(
            '<td id="' + file.id + '" class="file-item thumbnail " style="display: inline-block;margin-left: 50px">' +
                '<img  class="thisbannerimg" style="width: 250px;height: 150px">' + '<button type="button" class="btn bg-blue btn-block  waves-effect reonline">启用</button>'+
            '</td>'
            ),
        $img = $li.find('img');

    // $list为容器jQuery实例
    $('.uploader-list  td:first-child').before($li)

    // 创建缩略图
    // 如果为非图片文件，可以不用调用此方法。
    // thumbnailWidth x thumbnailHeight 为 100 x 100
    uploader.makeThumb( file, function( error, src ) {
        if ( error ) {
            $img.replaceWith('<span>不能预览</span>');
            return;
        }

        $img.attr( 'src', src );
    }, 100, 100 );
});

// 文件上传过程中创建进度条实时显示。
uploader.on( 'uploadProgress', function( file, percentage ) {
    var $li = $( '#'+file.id ),
        $percent = $li.find('.progress span');

    // 避免重复创建
    if ( !$percent.length ) {
        $percent = $('<p class="progress"><span></span></p>').appendTo( $li ).find('span');
    }

    $percent.css( 'width', percentage * 100 + '%' );
});

// 文件上传成功，给item添加成功class, 用样式标记上传成功。
uploader.on( 'uploadSuccess', function( file, response ) {
    $( '#'+file.id ).addClass('upload-state-done').find("img").attr('alt',response.file_name);
    $( '#'+file.id ).addClass('upload-state-done').find("img").attr('previewid',response.previewid);
});

// 文件上传失败，显示上传出错。
uploader.on( 'uploadError', function( file ) {
    var $li = $( '#'+file.id ),
        $error = $li.find('div.error');

    // 避免重复创建
    if ( !$error.length ) {
        $error = $('<div class="error"></div>').appendTo( $li );
    }

    $error.text('上传失败');
});

// 完成上传完了，成功或者失败，先删除进度条。
uploader.on( 'uploadComplete', function( file ) {
    $( '#'+file.id ).find('.progress').remove();
});

