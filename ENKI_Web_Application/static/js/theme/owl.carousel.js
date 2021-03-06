'use strict';

import utils from './Utils';

/*-----------------------------------------------
|   Owl Carousel
-----------------------------------------------*/
const $carousel = $('.owl-carousel');

utils.$document.ready(() => {
  if ($carousel.length) {
    const Selector = {
      ALL_TIMELINE: '*[data-zanim-timeline]',
      ACTIVE_ITEM: '.owl-item.active',
    };
    const owlZanim = {
      zanimTimeline($el) {
        return $el.find(Selector.ALL_TIMELINE);
      },
      play($el) {
        if (this.zanimTimeline($el).length === 0) return;
        $el
          .find(`${Selector.ACTIVE_ITEM} > ${Selector.ALL_TIMELINE}`)
          .zanimation((animation) => {
            animation.play();
          });
      },
      kill($el) {
        if (this.zanimTimeline($el).length === 0) return;
        this.zanimTimeline($el).zanimation((animation) => {
          animation.kill();
        });
      },
    };

    $carousel.each((index, value) => {
      const $this = $(value);
      const options = $this.data('options') || {};
      utils.isRTL() && (options.rtl = true);

      options.navText ||
        (options.navText = [
          '<span class="fas fa-angle-left"></span>',
          '<span class="fas fa-angle-right"></span>',
        ]);
      options.touchDrag = true;

      $this.owlCarousel(
        $.extend(options || {}, {
          onInitialized(event) {
            owlZanim.play($(event.target));
          },
          onTranslate(event) {
            owlZanim.kill($(event.target));
          },
          onTranslated(event) {
            owlZanim.play($(event.target));
          },
        })
      );
    });
  }

  const $controllers = $('[data-owl-carousel-controller]');

  if ($controllers.length) {
    $controllers.each((index, value) => {
      const $this = $(value);
      const $thumbs = $($this.data('owl-carousel-controller'));
      $thumbs.find('.owl-item:first-child').addClass('current');

      $thumbs.on('click', '.item', (e) => {
        const thumbIndex = $(e.target).parents('.owl-item').index();
        $('.owl-item').removeClass('current');
        $(e.target).parents('.owl-item').addClass('current');
        $this.trigger('to.owl.carousel', thumbIndex, 500);
      });

      $this.on('changed.owl.carousel', (e) => {
        let itemIndex = e.item.index;
        let item = itemIndex + 1;
        $('.owl-item').removeClass('current');
        $thumbs.find(`.owl-item:nth-child(${item})`).addClass('current');
        $thumbs.trigger('to.owl.carousel', itemIndex, 500);
      });
    });
  }

  // Refresh owlCarousel
  $('.navbar-vertical-toggle').on('navbar.vertical.toggle', () => {
    $carousel.length && $carousel.owlCarousel('refresh');
  });
});
