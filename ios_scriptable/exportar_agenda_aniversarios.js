// Exporta aniversários e eventos do calendário para JSON no GitHub.
// Salve um token no Keychain do Scriptable com a chave: totodile_github_token
// Parâmetro opcional do widget/atalho: {"branch":"main"}

const REPO_OWNER = "leosaquetto"
const REPO_NAME = "totodile"
const DEFAULT_BRANCH = "main"
const TOKEN_KEY = "totodile_github_token"

const EVENTOS_PATH = "data/agenda/eventos.json"
const ANIVERSARIOS_PATH = "data/aniversarios/aniversarios.json"

const EXCLUDE_CALENDARS = ["Aniversários", "Birthdays"]
const BIRTHDAY_CALENDARS = ["Aniversários", "Birthdays"]
const DAYS_AHEAD = 365

const params = (() => {
  try {
    return args.widgetParameter ? JSON.parse(args.widgetParameter) : {}
  } catch (error) {
    return {}
  }
})()

const BRANCH = params.branch || DEFAULT_BRANCH

function cleanId(text) {
  return String(text || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-zA-Z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .toLowerCase() || "item"
}

function formatBirthdayName(title) {
  let name = String(title || "").replace(/Aniversário de |Aniversário do |Aniversário da /gi, "")

  const ageMatch = name.match(/faz (\d+) anos|\((\d+) anos\)/i)
  const age = ageMatch ? (ageMatch[1] || ageMatch[2]) : null

  name = name.replace(/faz \d+ anos|\(\d+ anos\)/gi, "").trim()

  const fileName = name.normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^\w\s]/gi, "")
    .toLowerCase()
    .replace(/\s+/g, "")

  const nameParts = name.split(/\s+/).filter((p) => p.trim().length > 0)
  const cleanParts = nameParts.filter((p) => !/[^\w\s]/gi.test(p) || p.length > 2)

  let visualName
  if (cleanParts.length > 1) {
    visualName = `${cleanParts[0]}\n${cleanParts[cleanParts.length - 1]}`
  } else {
    visualName = cleanParts[0] || nameParts[0] || name
  }

  return {
    name: visualName,
    fullName: name,
    age,
    fileName: fileName || cleanId(name)
  }
}

function getDateParts(date) {
  const d = new Date(date)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  d.setHours(0, 0, 0, 0)
  const diffDays = Math.round((d - today) / 86400000)

  return {
    isToday: diffDays === 0,
    diffDays,
    day: String(d.getDate()).padStart(2, "0"),
    month: String(d.getMonth() + 1).padStart(2, "0"),
    year: String(d.getFullYear()).slice(-2),
    weekday: d.toLocaleDateString("pt-BR", { weekday: "long" })
  }
}

function daysLabel(info) {
  if (info.isToday) return "HOJE"
  if (info.diffDays === 1) return "AMANHÃ"
  return `EM ${info.diffDays} DIAS`
}

function toEventPayload(event) {
  const info = getDateParts(event.startDate)
  return {
    id: event.identifier || `${cleanId(event.title)}-${event.startDate.toISOString()}`,
    title: event.title,
    startDate: event.startDate.toISOString(),
    endDate: event.endDate ? event.endDate.toISOString() : null,
    calendar: event.calendar ? event.calendar.title : "",
    isAllDay: Boolean(event.isAllDay),
    diffDays: info.diffDays,
    dayLabel: daysLabel(info),
    dateLine: `${info.day}/${info.month}/${info.year}, ${info.weekday}`
  }
}

function toBirthdayPayload(event) {
  const data = formatBirthdayName(event.title)
  const info = getDateParts(event.startDate)

  return {
    id: event.identifier || data.fileName,
    title: event.title,
    nome: data.fullName,
    nomeWidget: data.name,
    fileName: data.fileName,
    idade: data.age,
    data: event.startDate.toISOString(),
    calendar: event.calendar ? event.calendar.title : "",
    diffDays: info.diffDays,
    dayLabel: daysLabel(info),
    dateLine: `${info.day}/${info.month}/${info.year}, ${info.weekday}`
  }
}


function exportTimezone() {
  try {
    return Intl.DateTimeFormat().resolvedOptions().timeZone || "unknown"
  } catch (error) {
    return "unknown"
  }
}

function buildExportEnvelope(items) {
  return {
    exportedAt: new Date().toISOString(),
    source: "scriptable",
    count: items.length,
    timezone: exportTimezone(),
    branch: BRANCH,
    items
  }
}
async function putGithubJson(path, payload, token) {
  const url = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${path}`

  let sha = null
  const getReq = new Request(`${url}?ref=${BRANCH}`)
  getReq.headers = {
    Authorization: `Bearer ${token}`,
    Accept: "application/vnd.github+json",
    "User-Agent": "Scriptable-Totodile"
  }

  try {
    const current = await getReq.loadJSON()
    sha = current.sha || null
  } catch (error) {}

  const body = {
    message: `🤖 atualizar ${path} via Scriptable`,
    branch: BRANCH,
    content: Data.fromString(JSON.stringify(payload, null, 2)).toBase64String()
  }
  if (sha) body.sha = sha

  const putReq = new Request(url)
  putReq.method = "PUT"
  putReq.headers = {
    Authorization: `Bearer ${token}`,
    Accept: "application/vnd.github+json",
    "Content-Type": "application/json",
    "User-Agent": "Scriptable-Totodile"
  }
  putReq.body = JSON.stringify(body)
  return await putReq.loadJSON()
}

async function main() {
  const token = Keychain.get(TOKEN_KEY)
  if (!token) throw new Error(`Token ausente no Keychain: ${TOKEN_KEY}`)

  const start = new Date()
  const end = new Date(Date.now() + DAYS_AHEAD * 24 * 60 * 60 * 1000)
  const allEvents = await CalendarEvent.between(start, end)

  const aniversarios = allEvents
    .filter((event) => BIRTHDAY_CALENDARS.includes(event.calendar.title))
    .sort((a, b) => a.startDate - b.startDate)
    .map(toBirthdayPayload)

  const eventos = allEvents
    .filter((event) => !EXCLUDE_CALENDARS.includes(event.calendar.title))
    .sort((a, b) => a.startDate - b.startDate)
    .map(toEventPayload)

  const aniversariosPayload = buildExportEnvelope(aniversarios)
  const eventosPayload = buildExportEnvelope(eventos)

  await putGithubJson(ANIVERSARIOS_PATH, aniversariosPayload, token)
  await putGithubJson(EVENTOS_PATH, eventosPayload, token)

  console.log(`Aniversários exportados: ${aniversarios.length}`)
  console.log(`Eventos exportados: ${eventos.length}`)
  console.log(`Branch destino: ${BRANCH}`)
  console.log(`Arquivos atualizados: ${ANIVERSARIOS_PATH}, ${EVENTOS_PATH}`)
}

await main()
Script.complete()
