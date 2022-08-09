(() => {
  const previousBtnEl = document.querySelector('.js-previous-btn');
  const nextBtnEl = document.querySelector('.js-next-btn');
  const carouselCardsEl = document.querySelectorAll('.js-carousel-card');

  const maxSlideIndex = carouselCardsEl.length - 1;

  const activeClassesName = {
    active: 'carousel__card--active',
    fromLeft: 'carousel__card--appear-from-left',
    fromRight: 'carousel__card--appear-from-right',
  };

  let currentSlideIndex = 0;

  const carouselCardClasses = (index) => carouselCardsEl[index].classList;

  function cleanActiveClasses(slideIndex) {
    carouselCardClasses(slideIndex).remove(
      activeClassesName.active,
      activeClassesName.fromLeft,
      activeClassesName.fromRight
    );
  }

  function previousSlide() {
    cleanActiveClasses(currentSlideIndex);
    currentSlideIndex =
      currentSlideIndex === 0 ? maxSlideIndex : currentSlideIndex - 1;
    carouselCardClasses(currentSlideIndex).add(
      activeClassesName.active,
      activeClassesName.fromRight
    );
  }

  function nextSlide() {
    cleanActiveClasses(currentSlideIndex);
    currentSlideIndex =
      currentSlideIndex === maxSlideIndex ? 0 : currentSlideIndex + 1;
    carouselCardClasses(currentSlideIndex).add(
      activeClassesName.active,
      activeClassesName.fromLeft
    );
  }

  carouselCardClasses(currentSlideIndex).add(activeClassesName.active);
  previousBtnEl.addEventListener('click', previousSlide);
  nextBtnEl.addEventListener('click', nextSlide);

  setInterval(nextSlide, 6000);
})();
