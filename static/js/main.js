$('.page-header .page-menu-handler').on('click', function() {
    $('.page-header .page-menu').addClass('active');
    $('.page-header .overlay').addClass('active');
});

$('.page-header .user-menu-handler').on('click', function() {
    $('.page-header .user-menu').addClass('active');
    $('.page-header .overlay').addClass('active');
});

$('.page-header .overlay').on('click', function() {
    $('.page-header .page-menu').removeClass('active');
    $('.page-header .user-menu').removeClass('active');
    $(this).removeClass('active');
});

$('.form-group input, .form-group textarea').focusin(function() {
   $(this).parent().addClass('active');
}).focusout(function() {
    $(this).parent().removeClass('active');
});