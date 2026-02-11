import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Input from '~/components/ui/Input.vue'

describe('Input', () => {
  it('renders with modelValue', () => {
    const wrapper = mount(Input, {
      props: { modelValue: 'test value' },
    })
    expect(wrapper.find('input').element.value).toBe('test value')
  })

  it('emits update:modelValue on input', async () => {
    const wrapper = mount(Input, {
      props: { modelValue: '' },
    })
    await wrapper.find('input').setValue('new value')
    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
    expect(wrapper.emitted('update:modelValue')![0]).toEqual(['new value'])
  })

  it('applies text type by default', () => {
    const wrapper = mount(Input, {
      props: { modelValue: '' },
    })
    expect(wrapper.find('input').attributes('type')).toBe('text')
  })

  it('applies email type when specified', () => {
    const wrapper = mount(Input, {
      props: { modelValue: '', type: 'email' },
    })
    expect(wrapper.find('input').attributes('type')).toBe('email')
  })

  it('applies password type when specified', () => {
    const wrapper = mount(Input, {
      props: { modelValue: '', type: 'password' },
    })
    expect(wrapper.find('input').attributes('type')).toBe('password')
  })

  it('renders placeholder', () => {
    const wrapper = mount(Input, {
      props: { modelValue: '', placeholder: 'Enter text...' },
    })
    expect(wrapper.find('input').attributes('placeholder')).toBe('Enter text...')
  })

  it('can be disabled', () => {
    const wrapper = mount(Input, {
      props: { modelValue: '', disabled: true },
    })
    expect(wrapper.find('input').attributes('disabled')).toBeDefined()
  })

  it('applies error styling when error prop is true', () => {
    const wrapper = mount(Input, {
      props: { modelValue: '', error: true },
    })
    expect(wrapper.find('input').classes()).toContain('border-red-500')
  })

  it('applies normal styling when error prop is false', () => {
    const wrapper = mount(Input, {
      props: { modelValue: '', error: false },
    })
    expect(wrapper.find('input').classes()).toContain('border-border')
  })
})
