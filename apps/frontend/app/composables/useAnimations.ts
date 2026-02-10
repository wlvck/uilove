import gsap from 'gsap'

export function useAnimations() {
  function animateCardHover(el: HTMLElement) {
    gsap.to(el, {
      scale: 1.02,
      boxShadow: '0 20px 40px rgba(0, 0, 0, 0.3)',
      duration: 0.3,
      ease: 'power2.out',
    })
  }

  function animateCardLeave(el: HTMLElement) {
    gsap.to(el, {
      scale: 1,
      boxShadow: '0 0px 0px rgba(0, 0, 0, 0)',
      duration: 0.3,
      ease: 'power2.out',
    })
  }

  function animateGridEntrance(container: HTMLElement, selector = '.website-card') {
    const cards = container.querySelectorAll(selector)
    gsap.fromTo(
      cards,
      { opacity: 0, y: 30 },
      {
        opacity: 1,
        y: 0,
        duration: 0.5,
        stagger: 0.08,
        ease: 'power2.out',
      },
    )
  }

  function animateFadeIn(el: HTMLElement, delay = 0) {
    gsap.fromTo(
      el,
      { opacity: 0, y: 20 },
      { opacity: 1, y: 0, duration: 0.6, delay, ease: 'power2.out' },
    )
  }

  function animatePageEnter(el: HTMLElement) {
    gsap.fromTo(
      el,
      { opacity: 0 },
      { opacity: 1, duration: 0.4, ease: 'power2.out' },
    )
  }

  return {
    animateCardHover,
    animateCardLeave,
    animateGridEntrance,
    animateFadeIn,
    animatePageEnter,
  }
}
