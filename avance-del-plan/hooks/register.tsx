import type { EngineInterface, Register } from 'claude-code'

import type { Paso, Plan } from '../types'

const PANEL = 'avance-del-plan'
const PLAN = { plugin: 'avance-del-plan', key: 'plan' } as const

type Dolar = EngineInterface

async function git($: Dolar, args: string[], cwd?: string): Promise<string | undefined> {
  const r = await $.process.run(['git', ...args], cwd ? { cwd, timeoutMs: 5000 } : { timeoutMs: 5000 })
    .catch(() => undefined)
  return r && r.exitCode === 0 ? r.stdout.trim() : undefined
}

function celdas(linea: string): string[] {
  return linea.trim().replace(/^\||\|$/g, '').split('|').map(c => c.trim())
}

function leerPlan(texto: string, rama: string, archivo: string): Plan {
  const titulo = texto.split('\n').find(l => l.startsWith('# '))?.slice(2).trim() ?? rama
  const espera = /Espera de ti:\s*([^\n]+)/.exec(texto)?.[1]?.trim() ?? ''
  const pasos: Paso[] = []
  const i = texto.indexOf('## Pasos')
  if (i >= 0) {
    const bloque = texto.slice(i).split('\n## ')[0]
    for (const linea of bloque.split('\n')) {
      const c = celdas(linea)
      if (c.length >= 3 && /^\d+$/.test(c[0])) {
        const ultima = c[c.length - 1]
        const hecho = ultima !== '' && !ultima.startsWith('{{')
        pasos.push({ n: c[0], paso: c[1], hecho, evidencia: hecho ? ultima : '' })
      }
    }
  }
  return { titulo, rama, archivo, pasos, espera }
}

async function buscar($: Dolar, desde?: string): Promise<Plan | null> {
  const raiz = await git($, ['rev-parse', '--show-toplevel'], desde)
  const rama = raiz && (await git($, ['branch', '--show-current'], raiz))
  if (!raiz || !rama) return null
  const dir = `${raiz}/tareas/planes`
  if (!(await $.fs.exists(dir))) return null
  const directo = `${dir}/${rama}.md`
  if (await $.fs.exists(directo)) return leerPlan(await $.fs.read(directo), rama, directo)
  const marcador = new RegExp(`<!--[^>]*\\b(rama|slug)\\s+${rama.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`)
  for (const entrada of await $.fs.list(dir)) {
    if (!entrada.name.endsWith('.md')) continue
    const ruta = `${dir}/${entrada.name}`
    const texto = await $.fs.read(ruta).catch(() => '')
    if (marcador.test(texto.split('\n', 1)[0] ?? '')) return leerPlan(texto, rama, ruta)
  }
  return null
}

function linea(p: Plan | null): string | undefined {
  if (!p) return undefined
  if (p.pasos.length === 0) return `Plan · ${p.titulo.slice(0, 40)} (sin tabla de pasos)`
  const hechos = p.pasos.filter(x => x.hecho).length
  const sigue = p.pasos.find(x => !x.hecho)
  return sigue
    ? `Plan ${hechos}/${p.pasos.length} · sigue: ${sigue.paso.slice(0, 48)}`
    : `Plan ${hechos}/${p.pasos.length} · listo para cerrar`
}

async function cargar($: Dolar, desde?: string): Promise<Plan | null> {
  const p = await buscar($, desde).catch(() => null)
  $.ui.status(linea(p))
  return p
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'plan', description: 'Muestra el avance del plan de la rama en curso' })
    const p = await cargar($)
    await $.state.set(PLAN, p)
    return next(e)
  })

  on('command.run', { command: 'plan' }, async $ => {
    const fresco = await cargar($)
    await $.state.set(PLAN, fresco)
    await $.ui.open({ id: PANEL, title: 'Avance del plan' })
    const p = (await $.state.get(PLAN)).value ?? null
    return { text: p ? 'Panel del plan abierto.' : 'No hay plan para la rama en curso.' }
  })

  on('tool.call', { tool: 'Edit' }, async ($, e, next) => {
    const ran = await next(e)
    if (e.file_path.includes('/tareas/planes/')) {
      const p = await cargar($, e.file_path.slice(0, e.file_path.lastIndexOf('/')))
      await $.state.set(PLAN, p)
    }
    return ran
  })

  on('tool.call', { tool: 'Write' }, async ($, e, next) => {
    const ran = await next(e)
    if (e.file_path.includes('/tareas/planes/')) {
      const p = await cargar($, e.file_path.slice(0, e.file_path.lastIndexOf('/')))
      await $.state.set(PLAN, p)
    }
    return ran
  })

  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    const ran = await next(e)
    if (/\bgit\b[^\n]*\b(switch|checkout|merge|commit)\b/.test(e.command)) {
      const p = await cargar($)
      await $.state.set(PLAN, p)
    }
    return ran
  })

  on('ui.render', { component: 'Pane', requestId: PANEL }, async ($, e) => {
    const { Box, Text } = $.ui.resolve(e)
    const p = (await $.state.get(PLAN)).value ?? null
    if (!p) return <Text dimColor>No hay plan para la rama en curso.</Text>
    const actual = p.pasos.find(x => !x.hecho)
    const hechos = p.pasos.filter(x => x.hecho).length
    return (
      <Box flexDirection="column">
        <Text bold>{p.titulo}</Text>
        <Text dimColor>
          rama {p.rama} · {p.pasos.length ? `${hechos} de ${p.pasos.length} pasos` : 'sin tabla de pasos'}
        </Text>
        <Text> </Text>
        {p.pasos.map(x => (
          <Box flexDirection="column">
            <Text dimColor={x.hecho} bold={x === actual}>
              {x.hecho ? '✓' : x === actual ? '▸' : '·'} {x.n}. {x.paso}
            </Text>
            {x.hecho && x.evidencia !== '✓' && <Text dimColor>    {x.evidencia}</Text>}
          </Box>
        ))}
        {p.espera !== '' && <Text> </Text>}
        {p.espera !== '' && <Text color="yellow">Espera de ti: {p.espera}</Text>}
      </Box>
    )
  })
}
