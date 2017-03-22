function main() {
    (function () {
        'use strict';

        /* Smooth Scroll */
        $('a.page-scroll').click(function () {
            if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
                var target = $(this.hash);
                target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
                if (target.length) {
                    $('html,body').animate({
                        scrollTop: target.offset().top - 35
                    }, 900);
                    return false;
                }
            }
        });
            

        /* Show Menu on Book */
        $(window).bind('scroll', function () {
            var navHeight = $(window).height() - 600;
            if ($(window).scrollTop() > navHeight) {
                $('.navbar-default').addClass('on');
            } else {
                $('.navbar-default').removeClass('on');
            }
        });

        /* Collapsing Navigation Bar */
        $('body').scrollspy({
            target: '.navbar-default',
            offset: 80
        })
        
        /* ScrollReveal */
        window.sr = ScrollReveal();
            // sr.reveal('.reveal-sectiontitle', {duration: 700,
            //                       distance: '0px',
            //                       opacity: 0,
            //                       scale: 0.50,
            //                       viewFactor: 0.90,
            //                       reset: true,
            //                       easing: 'linear' });

            sr.reveal('.reveal-title', {duration: 600,
                                  distance: '100px',
                                  origin: 'top',
                                  delay: 200,
                                  opacity: 0,
                                  viewFactor: 0.9,
                                  reset: true,
                                  easing: 'linear' });

            sr.reveal('.reveal-content', {duration: 1000,
                                  distance: '0px',
                                  opacity: 0,
                                  scale: 0.99,
                                  reset: true,
                                  easing: 'linear' });
      
            sr.reveal('.reveal-icons', {duration: 500,
                                  distance: '50px',
                                  origin: 'bottom',
                                  scale: 0,
                                  delay: 400,
                                  reset: true,
                                  easing: 'linear' });

            sr.reveal('.reveal-nav', {duration: 500,
                                  distance: '50px',
                                  origin: 'top',
                                  scale: 0,
                                  delay: 400,
                                  reset: false,
                                  easing: 'linear' });

            sr.reveal('.reveal-lists', {duration: 500,
                                  distance: '50px',
                                  origin: 'bottom',
                                  scale: 0,
                                  delay: 400,
                                  reset: true,
                                  easing: 'linear' });

             sr.reveal('.reveal-contactus', {duration: 500,
                                  distance: '50px',
                                  origin: 'bottom',
                                  scale: 0,
                                  delay: 100,
                                  viewFactor: 0.4,
                                  reset: true,
                                  easing: 'linear' });   

    }());
}

main();