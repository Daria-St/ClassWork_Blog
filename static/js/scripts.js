$('#likeButton').click(function(e) {
    e.preventDefault();
//    alert('Кнопку нажали');

    // перейди потом по ссылке
//    location.href = $(this).attr('href');

    // Меняет текст в кнопке после нажатия
//    $(this).text('Нажали  лайк');
//    $('h1').css({'color': 'red'});

    let baseUrl = 'http://127.0.0.1:8000/';
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
    let baseUrl = 'http://127.0.0.1:8000/';
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