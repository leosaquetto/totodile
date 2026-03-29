// ------------------------------------------------
// TOTODILE MASTER WIDGET
// Parâmetros aceitos: 'agenda', 'niver', 'treino', 'musica'
// ------------------------------------------------

const param = args.widgetParameter ? args.widgetParameter.toLowerCase() : "treino";
const GITHUB_TOKEN = "SEU_TOKEN_GITHUB_AQUI"; // Token secreto (Personal Access Token)
const REPO_OWNER = "leosaquetto";
const REPO_NAME = "totodile";

async function main() {
  let widget = new ListWidget();
  const bg = new LinearGradient();
  bg.colors = [new Color("#2d2d2d"), new Color("#141414")];
  bg.locations = [0, 1];
  widget.backgroundGradient = bg;

  // Roteador de Widgets
  if (param === "agenda") {
    widget = await buildAgenda(widget);
  } else if (param === "niver") {
    widget = await buildAniversarios(widget);
  } else if (param === "treino") {
    widget = await buildTreinos(widget);
    // Sincroniza o arquivo local do iCloud pro GitHub silenciosamente
    await syncToGitHub("Treinos/historico_treinos.txt", "data/treinos.txt");
  } else if (param === "musica") {
    widget = await buildMusica(widget);
  } else {
    widget.addText("Parâmetro inválido. Use: agenda, niver, treino ou musica.");
  }

  if (config.runsInWidget) {
    Script.setWidget(widget);
  } else {
    widget.presentSmall();
  }
  Script.complete();
}

// ==========================================
// FUNÇÕES DE SINCRONIZAÇÃO GITHUB
// ==========================================
async function syncToGitHub(localIcloudPath, githubFilePath) {
  const fm = FileManager.iCloud();
  const path = fm.joinPath(fm.documentsDirectory(), localIcloudPath);
  
  if (!fm.fileExists(path)) return;
  if (fm.isFileStoredIniCloud(path)) await fm.downloadFileFromiCloud(path);
  
  const content = fm.readString(path);
  const base64Content = Data.fromString(content).toBase64String();

  // 1. Busca o SHA do arquivo atual no GitHub (necessário para dar update)
  const url = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${githubFilePath}`;
  const reqGet = new Request(url);
  reqGet.headers = {
    "Authorization": `Bearer ${GITHUB_TOKEN}`,
    "User-Agent": "Scriptable-Totodile"
  };
  
  let sha = null;
  try {
    const resGet = await reqGet.loadJSON();
    if (resGet && resGet.sha) sha = resGet.sha;
  } catch(e) {} // Arquivo pode não existir ainda

  // 2. Envia a atualização
  const reqPut = new Request(url);
  reqPut.method = "PUT";
  reqPut.headers = {
    "Authorization": `Bearer ${GITHUB_TOKEN}`,
    "Content-Type": "application/json",
    "User-Agent": "Scriptable-Totodile"
  };
  
  const body = {
    message: "Sync via Totodile Scriptable",
    content: base64Content
  };
  if (sha) body.sha = sha;
  
  reqPut.body = JSON.stringify(body);
  await reqPut.load();
}

// ==========================================
// MÓDULOS DE UI (Esqueletos adaptados dos seus códigos)
// ==========================================

async function buildTreinos(w) {
  w.setPadding(10, 10, 10, 10);
  let title = w.addText("Últimos Treinos 💪🏼");
  title.font = Font.boldSystemFont(11);
  title.textColor = Color.white();
  w.addSpacer(5);
  // Aqui você cola a sua lógica de leitura do historico_treinos.txt
  // e exibe os últimos treinos.
  let t = w.addText("Sincronização com GitHub ativada nos bastidores.");
  t.font = Font.systemFont(9);
  t.textColor = new Color("#ffcc66");
  return w;
}

async function buildMusica(w) {
    // Lembrete: A separação do nome do artista na UI deve ocorrer após o SEGUNDO espaço
    // Exemplo de helper para usar na sua lógica do Stats.fm:
    /*
    function formatArtistName(name) {
        let parts = name.split(" ");
        if (parts.length > 2) {
            return parts.slice(0, 2).join(" ") + "\n" + parts.slice(2).join(" ");
        }
        return name;
    }
    */
    let title = w.addText("Stats.fm Resumo 🎧");
    title.font = Font.boldSystemFont(11);
    title.textColor = Color.white();
    return w;
}

async function buildAgenda(w) {
    let title = w.addText("Próximos Eventos 🗓️");
    title.font = Font.boldSystemFont(11);
    title.textColor = Color.white();
    return w;
}

async function buildAniversarios(w) {
    let title = w.addText("Aniversários 🎈");
    title.font = Font.boldSystemFont(11);
    title.textColor = Color.white();
    return w;
}

await main();
