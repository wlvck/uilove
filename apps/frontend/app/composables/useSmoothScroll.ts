import Lenis from 'lenis'

export function useSmoothScroll() {
  const lenis = ref<Lenis | null>(null)

  function init() {
    if (import.meta.server) return

    lenis.value = new Lenis({
      duration: 1.2,
      easing: (t: number) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true,
    })

    function raf(time: number) {
      lenis.value?.raf(time)
      requestAnimationFrame(raf)
    }
    requestAnimationFrame(raf)
  }

  function destroy() {
    lenis.value?.destroy()
    lenis.value = null
  }

  function scrollTo(target: string | number | HTMLElement, options?: { offset?: number; duration?: number }) {
    lenis.value?.scrollTo(target, options)
  }

  return { lenis, init, destroy, scrollTo }
}
