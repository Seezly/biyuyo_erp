import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Pagination from '@/components/ui/Pagination.vue'

describe('Pagination', () => {
  const defaultProps = {
    currentPage: 1,
    lastPage: 5,
    from: 1,
    to: 10,
    total: 50,
  }

  it('renders current page info', () => {
    const wrapper = mount(Pagination, { props: defaultProps })
    expect(wrapper.text()).toContain('Page 1 of 5')
    expect(wrapper.text()).toContain('Showing 1 to 10 of 50')
  })

  it('disables previous button on first page', () => {
    const wrapper = mount(Pagination, { props: defaultProps })
    const prevBtn = wrapper.findAll('button')[0]
    expect(prevBtn!.attributes('disabled')).toBeDefined()
  })

  it('disables next button on last page', () => {
    const wrapper = mount(Pagination, {
      props: { ...defaultProps, currentPage: 5 },
    })
    const nextBtn = wrapper.findAll('button')[1]
    expect(nextBtn!.attributes('disabled')).toBeDefined()
  })

  it('emits update:page on next click', async () => {
    const wrapper = mount(Pagination, { props: defaultProps })
    const nextBtn = wrapper.findAll('button')[1]
    await nextBtn!.trigger('click')
    expect(wrapper.emitted('update:page')).toEqual([[2]])
  })

  it('emits update:page on prev click', async () => {
    const wrapper = mount(Pagination, {
      props: { ...defaultProps, currentPage: 3 },
    })
    const prevBtn = wrapper.findAll('button')[0]
    await prevBtn!.trigger('click')
    expect(wrapper.emitted('update:page')).toEqual([[2]])
  })

  it('does not emit on prev when on first page', async () => {
    const wrapper = mount(Pagination, { props: defaultProps })
    const prevBtn = wrapper.findAll('button')[0]
    await prevBtn!.trigger('click')
    expect(wrapper.emitted('update:page')).toBeUndefined()
  })

  it('does not emit on next when on last page', async () => {
    const wrapper = mount(Pagination, {
      props: { ...defaultProps, currentPage: 5 },
    })
    const nextBtn = wrapper.findAll('button')[1]
    await nextBtn!.trigger('click')
    expect(wrapper.emitted('update:page')).toBeUndefined()
  })

  it('has correct aria-label on nav', () => {
    const wrapper = mount(Pagination, { props: defaultProps })
    const nav = wrapper.find('nav')
    expect(nav.attributes('aria-label')).toBe('Paginación')
  })
})
