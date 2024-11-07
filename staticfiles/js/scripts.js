$('#likeButton').click(function(e) {
    e.preventDefault();
//    alert('Кнопку нажали');

    // перейди потом по ссылке
//    location.href = $(this).attr('href');

    // Меняет текст в кнопке после нажатия
//    $(this).text('Нажали  лайк');
//    $('h1').css({'color': 'red'});

    let baseUrl = document.getElementById("host").innerHTML;
    $.ajax({
        type: 'GET',
        url: baseUrl + $(this).attr('href'),
        success: function(response) {
            $('#likesCount').text(response.likes)
            $('#likeButton').hide()
            $('#unlikeButton').show()
            }

    })
})

//$('#unlikeButton').click(function(e) {
//    e.preventDefault();
//    alert('Кнопку отжали');
////    location.href = $(this).attr('href');
//})

$('#unlikeButton').click(function(e) {
    e.preventDefault();
    let baseUrl = document.getElementById("host").innerHTML;

    $.ajax({
        type: 'GET',
        url: baseUrl + $(this).attr('href'),
        success: function(response) {
            $('#likesCount').text(response.likes)
            $('#likeButton').show()
            $('#unlikeButton').hide()
        }
    })
})

//функция, которая отслеживает в js нажатиие на кнопку Добавить

$('#feedbackForm').on('submit',function(e) {
    e.preventDefault();
    let baseUrl = document.getElementById("host").innerHTML;

    $.ajax({
        type: 'POST',
        url: baseUrl + $(this).attr('action'),
        data: {
            name: $('#id_name').val(),
            text: $('#id_text').val(),
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(response) {
            $('.post-card').text('Обратная связь отправлена')
        },
        error: function(response){
            const errors = response.responseJSON.errors
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