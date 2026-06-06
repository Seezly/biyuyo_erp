import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseAlert from '@/components/ui/BaseAlert.vue'

describe('BaseAlert', () => {
  it('renders title and description when visible', () => {
    const wrapper = mount(BaseAlert, {
      props: {
        visible: true,
        title: 'Alert Title',
        description: 'Alert description here',
        variant: 'info',
      },
      global: {
        stubs: { teleport: true },
      },
    })

    expect(wrapper.text()).toContain('Alert Title')
    expect(wrapper.text()).toContain('Alert description here')
  })

  it('does not render when not visible', () => {
    const wrapper = mount(BaseAlert, {
      props: {
        visible: false,
        title: 'Hidden',
        description: 'Hidden desc',
        variant: 'info',
      },
      global: {
        stubs: { teleport: true },
      },
    })

    expect(wrapper.find('[role="alertdialog"]').exists()).toBe(false)
  })

  it('renders subtitle when provided', () => {
    const wrapper = mount(BaseAlert, {
      props: {
        visible: true,
        title: 'Title',
        subtitle: 'Subtitle text',
        description: 'Description',
        variant: 'edit',
      },
      global: {
        stubs: { teleport: true },
      },
    })

    expect(wrapper.text()).toContain('Subtitle text')
  })

  it('shows cancel button when cancel prop is true', () => {
    const wrapper = mount(BaseAlert, {
      props: {
        visible: true,
        title: 'Title',
        description: 'Desc',
        variant: 'delete',
        cancel: true,
      },
      global: {
        stubs: { teleport: true },
      },
    })

    expect(wrapper.text()).toContain('Cancelar')
  })

  it('hides cancel button when cancel prop is false', () => {
    const wrapper = mount(BaseAlert, {
      props: {
        visible: true,
        title: 'Title',
        description: 'Desc',
        variant: 'delete',
        cancel: false,
      },
      global: {
        stubs: { teleport: true },
      },
    })

    expect(wrapper.text()).not.toContain('Cancelar')
  })

  it('has correct ARIA attributes', () => {
    const wrapper = mount(BaseAlert, {
      props: {
        visible: true,
        title: 'Accessible Alert',
        description: 'Accessible desc',
        variant: 'info',
      },
      global: {
        stubs: { teleport: true },
      },
    })

    const dialog = wrapper.find('[role="alertdialog"]')
    expect(dialog.attributes('aria-modal')).toBe('true')
    expect(dialog.attributes('aria-labelledby')).toBeTruthy()
    expect(dialog.attributes('aria-describedby')).toBeTruthy()
  })

  it('uses custom cta text', () => {
    const wrapper = mount(BaseAlert, {
      props: {
        visible: true,
        title: 'Title',
        description: 'Desc',
        variant: 'info',
        cta: 'Got it',
      },
      global: {
        stubs: { teleport: true },
      },
    })

    expect(wrapper.text()).toContain('Got it')
  })
})
