export type Paso = { n: string; paso: string; hecho: boolean; evidencia: string }

export type Plan = {
  titulo: string
  rama: string
  archivo: string
  pasos: Paso[]
  espera: string
}

declare module 'claude-code' {
  interface PluginState {
    'avance-del-plan': { plan: Plan | null }
  }
}
