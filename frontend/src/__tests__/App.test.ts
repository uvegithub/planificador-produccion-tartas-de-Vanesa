import { describe, it, expect, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { generarPlan } from '../services/production'
import App from '../App.vue'

// Simulamos la autenticación JWT durante las pruebas.
vi.mock('../services/auth', () => ({
  getToken: vi.fn(() => 'token-de-prueba'),
}))

// Simulamos el servicio del backend para controlar los errores.
vi.mock('../services/production', () => ({
  generarPlan: vi.fn(),
}))

// Simulamos los controles de autenticación.
vi.mock('../components/AuthControls.vue', () => ({
  default: {
    template: '<div data-testid="auth-controls"></div>',
  },
}))

// Comprueba que la aplicación muestra correctamente
// el título principal del Planificador de tartas.
describe('App.vue', () => {
  it('muestra el título principal de la aplicación', () => {
    const wrapper = mount(App)

    expect(wrapper.find('h1').text()).toBe('Planificador de tartas')
  })
  // Comprueba que no se puede generar un plan
  // cuando no hay ningún equipamiento seleccionado.
  it('deshabilita el botón si no hay equipamiento', async () => {
    const wrapper = mount(App)

    const casillasSeleccionadas = wrapper.findAll('input[type="checkbox"]:checked')

    for (const casilla of casillasSeleccionadas) {
      await casilla.setValue(false)
    }   

    expect(wrapper.find('button[type="submit"]').attributes('disabled')).toBeDefined()

    expect(wrapper.text()).toContain('Selecciona al menos un equipo.')
  })
  // Comprueba que el botón está habilitado
  // cuando el formulario tiene datos válidos.
  it('permite generar un plan con los datos iniciales válidos', () => {
    const wrapper = mount(App)

    expect(
      wrapper.find('button[type="submit"]').attributes('disabled')
    ).toBeUndefined()
  })
   // Comprueba los valores iniciales de cantidad y tiempo.
  it('muestra los valores iniciales del formulario', () => {
    const wrapper = mount(App)

    const cantidad = wrapper.find('#cantidad').element as HTMLInputElement
    const tiempo = wrapper.find('#tiempo').element as HTMLInputElement

    expect(cantidad.value).toBe('50')
    expect(tiempo.value).toBe('180')
  })
  // Comprueba que aparecen los cuatro tipos de tarta.
  it('muestra los cuatro tipos de tarta disponibles', () => {
    const wrapper = mount(App)

    const opciones = wrapper.findAll('#tipo-tarta option')

    expect(opciones).toHaveLength(4)
  })
  // Comprueba que aparecen los cuatro equipos disponibles.
  it('muestra los cuatro equipos de producción', () => {
    const wrapper = mount(App)

    const equipos = wrapper.findAll('input[type="checkbox"]')

    expect(equipos).toHaveLength(4)
  })
  // Comprueba que se puede cambiar el tipo de tarta.
  it('permite seleccionar otro tipo de tarta', async () => {
    const wrapper = mount(App)

    await wrapper.find('#tipo-tarta').setValue('queso')

    expect(
      (wrapper.find('#tipo-tarta').element as HTMLSelectElement).value
    ).toBe('queso')
  })
  // Comprueba que se puede modificar la cantidad de tartas.
  it('permite cambiar la cantidad de tartas', async () => {
    const wrapper = mount(App)

    await wrapper.find('#cantidad').setValue(100)

    const cantidad = wrapper.find('#cantidad').element as HTMLInputElement

    expect(cantidad.value).toBe('100')
  })
// Comprueba que se puede modificar el tiempo disponible.
  it('permite cambiar el tiempo disponible', async () => {
    const wrapper = mount(App)

    await wrapper.find('#tiempo').setValue(240)

    const tiempo = wrapper.find('#tiempo').element as HTMLInputElement

    expect(tiempo.value).toBe('240')
  })
  
  // Comprueba que se muestra un error si falla la petición.
  it('muestra un mensaje cuando falla la generación del plan', async () => {
    vi.mocked(generarPlan).mockRejectedValueOnce(
      new Error('Error de conexión')
    )

    const wrapper = mount(App)

    await wrapper.find('form').trigger('submit')
    await flushPromises()

    expect(wrapper.text()).toContain('Error de conexión')
  })
})