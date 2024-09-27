$(document).ready(function () {
    // Animate team member images on scroll
    const teamImages = $('.img-responsive');
    const windowHeight = $(window).height();

    function animateOnScroll() {
        teamImages.each(function () {
            const imageTop = $(this).offset().top;

            if (imageTop < $(window).scrollTop() + windowHeight) {
                $(this).fadeIn(600).css('transform', 'scale(1)');
            } else {
                $(this).css('opacity', '0').css('transform', 'scale(0.8)');
            }
        });
    }

    $(window).on('scroll', function () {
        animateOnScroll();
    });

    // Initial call to animate team images
    animateOnScroll();
});

