import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Button from '~/components/ui/Button.vue'

describe('Button', () => {
  it('renders slot content', () => {
    const wrapper = mount(Button, {
      slots: {
        default: 'Click me',
      },
    })
    expect(wrapper.text()).toBe('Click me')
  })

  it('applies primary variant by default', () => {
    const wrapper = mount(Button)
    expect(wrapper.classes()).toContain('bg-accent')
  })

  it('applies secondary variant when specified', () => {
    const wrapper = mount(Button, {
      props: { variant: 'secondary' },
    })
    expect(wrapper.classes()).toContain('bg-bg-tertiary')
  })

  it('applies ghost variant when specified', () => {
    const wrapper = mount(Button, {
      props: { variant: 'ghost' },
    })
    expect(wrapper.classes()).toContain('hover:bg-bg-tertiary')
  })

  it('applies outline variant when specified', () => {
    const wrapper = mount(Button, {
      props: { variant: 'outline' },
    })
    expect(wrapper.classes()).toContain('border')
  })

  it('applies md size by default', () => {
    const wrapper = mount(Button)
    expect(wrapper.classes()).toContain('px-4')
    expect(wrapper.classes()).toContain('py-2')
  })

  it('applies sm size when specified', () => {
    const wrapper = mount(Button, {
      props: { size: 'sm' },
    })
    expect(wrapper.classes()).toContain('px-3')
    expect(wrapper.classes()).toContain('py-1.5')
  })

  it('applies lg size when specified', () => {
    const wrapper = mount(Button, {
      props: { size: 'lg' },
    })
    expect(wrapper.classes()).toContain('px-6')
    expect(wrapper.classes()).toContain('py-3')
  })

  it('can be disabled', () => {
    const wrapper = mount(Button, {
      attrs: { disabled: true },
    })
    expect(wrapper.attributes('disabled')).toBeDefined()
  })

  it('emits click event', async () => {
    const wrapper = mount(Button)
    await wrapper.trigger('click')
    expect(wrapper.emitted('click')).toBeTruthy()
  })
})
