import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseModal from '@/components/ui/BaseModal.vue'

describe('BaseModal', () => {
  it('renders title and message when visible', () => {
    const wrapper = mount(BaseModal, {
      props: {
        visible: true,
        title: 'Test Title',
        message: 'Test message content',
      },
      global: {
        stubs: { teleport: true },
      },
    })

    expect(wrapper.text()).toContain('Test Title')
    expect(wrapper.text()).toContain('Test message content')
  })

  it('does not render when not visible', () => {
    const wrapper = mount(BaseModal, {
      props: {
        visible: false,
        title: 'Hidden Title',
      },
      global: {
        stubs: { teleport: true },
      },
    })

    expect(wrapper.find('[role="dialog"]').exists()).toBe(false)
  })

  it('emits close when cancel button clicked', async () => {
    const wrapper = mount(BaseModal, {
      props: {
        visible: true,
        title: 'Close Test',
      },
      global: {
        stubs: { teleport: true },
      },
    })

    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted('close')).toBeTruthy()
  })

  it('emits confirm when confirm button clicked', async () => {
    const wrapper = mount(BaseModal, {
      props: {
        visible: true,
        title: 'Confirm Test',
        confirmText: 'Accept',
      },
      global: {
        stubs: { teleport: true },
      },
    })

    const buttons = wrapper.findAll('button')
    const confirmBtn = buttons.find(b => b.text().includes('Accept'))
    expect(confirmBtn).toBeTruthy()
    await confirmBtn!.trigger('click')
    expect(wrapper.emitted('confirm')).toBeTruthy()
  })

  it('has correct ARIA attributes', () => {
    const wrapper = mount(BaseModal, {
      props: {
        visible: true,
        title: 'Accessible Modal',
        message: 'Description here',
      },
      global: {
        stubs: { teleport: true },
      },
    })

    const dialog = wrapper.find('[role="dialog"]')
    expect(dialog.attributes('aria-modal')).toBe('true')
    expect(dialog.attributes('aria-labelledby')).toBeTruthy()
  })

  it('applies correct size class', () => {
    const wrapper = mount(BaseModal, {
      props: {
        visible: true,
        title: 'Size Test',
        size: 'lg',
      },
      global: {
        stubs: { teleport: true },
      },
    })

    const dialog = wrapper.find('[role="dialog"]')
    expect(dialog.classes()).toContain('max-w-lg')
  })
})
