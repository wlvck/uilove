import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Badge from '~/components/ui/Badge.vue'

describe('Badge', () => {
  it('renders slot content', () => {
    const wrapper = mount(Badge, {
      slots: {
        default: 'New',
      },
    })
    expect(wrapper.text()).toBe('New')
  })

  it('applies default variant by default', () => {
    const wrapper = mount(Badge)
    expect(wrapper.classes()).toContain('bg-bg-tertiary')
  })

  it('applies accent variant when specified', () => {
    const wrapper = mount(Badge, {
      props: { variant: 'accent' },
    })
    expect(wrapper.classes()).toContain('bg-accent/10')
  })

  it('applies outline variant when specified', () => {
    const wrapper = mount(Badge, {
      props: { variant: 'outline' },
    })
    expect(wrapper.classes()).toContain('border')
    expect(wrapper.classes()).toContain('border-border')
  })

  it('applies sm size by default', () => {
    const wrapper = mount(Badge)
    expect(wrapper.classes()).toContain('px-2')
    expect(wrapper.classes()).toContain('text-xs')
  })

  it('applies md size when specified', () => {
    const wrapper = mount(Badge, {
      props: { size: 'md' },
    })
    expect(wrapper.classes()).toContain('px-3')
    expect(wrapper.classes()).toContain('text-sm')
  })

  it('renders as span element', () => {
    const wrapper = mount(Badge)
    expect(wrapper.element.tagName).toBe('SPAN')
  })

  it('has rounded-full class', () => {
    const wrapper = mount(Badge)
    expect(wrapper.classes()).toContain('rounded-full')
  })
})
