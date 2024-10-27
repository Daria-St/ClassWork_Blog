function loadComments(){
    let baseUrl = 'http://localhost:8001/';
    let postId = $('.container-post').data('post-id')

    $.ajax({
        type: 'GET',
        url: baseUrl + `/api/rest/posts/${postId}/comments`,
        success: function(response) {
            let comments = ''
            $.each(response.comments, function(index, comment) {
                comments += '<div class="comment">'
                comments += '<p class="comment-author">' + comment.profile + '</p>'
                comments += '<p class="comment-text">' + comment.text + '</p>'
//                comments += '<p class="comment-text">' + comment.my_field + '</p>' # проверка, что подключились к нужной вьюхе, везде появилось кастомное поле
                comments += '</div>'
            })

            $('.comments-section').html(comments);
        }
    })
}

// Обработака клика по кнопке отправки коммента
$('#CommentForm').on('submit',function(e) {
    e.preventDefault();
    let baseUrl = 'http://localhost:8001/';

    $.ajax({
        type: 'POST',
        url: baseUrl + $(this).attr('action'),
        data: {
            text: $('#id_text').val(),
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(response) {
            loadComments()
            $('#CommentForm')[0].reset() // очистка поля после ввода коммента
            $('.formErrors').html('') // очистка поля ошибки  после ее исправления
        },
        error: function(response){
            const errors = response.responseJSON
            let err = ''

            for (let field in errors) {
                for (let error of errors[field]) {
                    err += '<p>' + error + '</p>'
                }
            }
            $('.formErrors').html(err)

        }
    })
})


//$(document).ready(function(){
//    loadComments();
//})