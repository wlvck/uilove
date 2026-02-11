import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import LoadingSpinner from '~/components/ui/LoadingSpinner.vue'

describe('LoadingSpinner', () => {
  it('renders spinner element', () => {
    const wrapper = mount(LoadingSpinner)
    expect(wrapper.find('.animate-spin').exists()).toBe(true)
  })

  it('applies md size by default', () => {
    const wrapper = mount(LoadingSpinner)
    const spinner = wrapper.find('.animate-spin')
    expect(spinner.classes()).toContain('h-8')
    expect(spinner.classes()).toContain('w-8')
  })

  it('applies sm size when specified', () => {
    const wrapper = mount(LoadingSpinner, {
      props: { size: 'sm' },
    })
    const spinner = wrapper.find('.animate-spin')
    expect(spinner.classes()).toContain('h-5')
    expect(spinner.classes()).toContain('w-5')
  })

  it('applies lg size when specified', () => {
    const wrapper = mount(LoadingSpinner, {
      props: { size: 'lg' },
    })
    const spinner = wrapper.find('.animate-spin')
    expect(spinner.classes()).toContain('h-12')
    expect(spinner.classes()).toContain('w-12')
  })

  it('applies default container class', () => {
    const wrapper = mount(LoadingSpinner)
    expect(wrapper.classes()).toContain('py-12')
  })

  it('applies custom container class', () => {
    const wrapper = mount(LoadingSpinner, {
      props: { containerClass: 'py-4' },
    })
    expect(wrapper.classes()).toContain('py-4')
  })

  it('has rounded-full class for circular shape', () => {
    const wrapper = mount(LoadingSpinner)
    const spinner = wrapper.find('.animate-spin')
    expect(spinner.classes()).toContain('rounded-full')
  })
})
