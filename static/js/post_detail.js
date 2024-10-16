function loadComments(){
    let baseUrl = 'http://localhost:8001/';
    let postId = $('.container-post').data('post-id')

    $.ajax({
        type: 'GET',
        url: baseUrl + `/api/posts/${postId}/comments`,
        success: function(response) {
            let comments = ''
            $.each(response.comments, function(index, comment) {
                comments += '<div class="comment">'
                comments += '<p class="comment-author">' + comment.profile + '</p>'
                comments += '<p class="comment-text">' + comment.text + '</p>'
                comments += '</div>'
            })

            $('.comments-section').html(comments);
        }
    })
}

$(document).ready(function(){
    loadComments();
})