tinymce.init({
            selector: "textarea",
    //relative_urls如果该选项设为true，所有通过MCFileManager返回的URL都会与知道的document_base_url相关。
    // 如果设为false,所有URL会被转化成绝对URL，默认为true。
            relative_urls :false,
    //remove_script_host强制url为绝对路径，不自动转换.该选项允许MCFileManager返回的URL的协议和主机部分被删除，
    // 该选项仅在relative_urls选项设为false时有用，该选项默认为true。
            remove_script_host :false,

            upload_image_url: './myupload/', //配置的上传图片的路由
            height: 400,
            language:'zh_CN',
            plugins: [
                'advlist autolink lists link  charmap print preview hr anchor pagebreak',
                'searchreplace wordcount visualblocks visualchars code fullscreen',
                'insertdatetime media nonbreaking save table contextmenu directionality',
                'emoticons template paste textcolor colorpicker textpattern imagetools codesample toc help  uploadimage'
              ],
              toolbar1: 'undo redo | insert | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image',
              toolbar2: 'print preview media | fullscreen codesample fontsizeselect  forecolor  backcolor  emoticons |  help uploadimage',
    //字体大小
    fontsize_formats: '10pt 12pt 14pt 18pt 24pt 36pt',
    //按tab不换行
    nonbreaking_force_tab: true,
              image_advtab: true,
              templates: [
                { title: 'Test template 1', content: 'Test 1' },
                { title: 'Test template 2', content: 'Test 2' }
              ],
            menubar: false
        });