// Exporta aniversários e eventos do calendário para JSON no GitHub.
// Salve um token no Keychain do Scriptable com a chave: totodile_github_token

const REPO_OWNER = "leosaquetto"
const REPO_NAME = "totodile"
const BRANCH = "main"
const TOKEN_KEY = "totodile_github_token"

const EVENTOS_PATH = "data/agenda/eventos.json"
const ANIVERSARIOS_PATH = "data/aniversarios/aniversarios.json"

const EXCLUDE_CALENDARS = ["Aniversários", "Birthdays"]
const BIRTHDAY_CALENDARS = ["Aniversários", "Birthdays"]
const DAYS_AHEAD = 365

function cleanId(text) {
  return String(text || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-zA-Z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .toLowerCase() || "item"
}

function cleanBirthdayName(title) {
  return String(title || "")
    .replace(/Aniversário de |Aniversário do |Aniversário da /gi, "")
    .trim()
}

function toEventPayload(event) {
  return {
    id: event.identifier || `${cleanId(event.title)}-${event.startDate.toISOString()}`,
    title: event.title,
    startDate: event.startDate.toISOString(),
    endDate: event.endDate ? event.endDate.toISOString() : null,
    calendar: event.calendar ? event.calendar.title : "",
    isAllDay: Boolean(event.isAllDay)
  }
}

function toBirthdayPayload(event) {
  return {
    id: event.identifier || cleanId(event.title),
    nome: cleanBirthdayName(event.title),
    data: event.startDate.toISOString(),
    title: event.title,
    calendar: event.calendar ? event.calendar.title : ""
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
    .map(toBirthdayPayload)

  const eventos = allEvents
    .filter((event) => !EXCLUDE_CALENDARS.includes(event.calendar.title))
    .map(toEventPayload)

  await putGithubJson(ANIVERSARIOS_PATH, aniversarios, token)
  await putGithubJson(EVENTOS_PATH, eventos, token)

  console.log(`Exportados ${aniversarios.length} aniversários e ${eventos.length} eventos.`)
}

await main()
Script.complete()
