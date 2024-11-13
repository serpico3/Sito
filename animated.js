$(window).scroll(function() {
    $('.scroll-animations .animated').each(function() {
    if (isScrolledIntoView(this) === true) {
    $(this).addClass('fadeInLeft');
    }
    });
    });