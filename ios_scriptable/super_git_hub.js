// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
// icon-color: deep-gray; icon-glyph: code-branch;
// scriptable: github workflows hub v7.3 - Colunas & Layout Nativo
// Dashboard nativo, repos, workflows, deploys reais, Vercel e Widgets.

const OWNER = "leosaquetto";
const TOKEN_KEY = "leosaquettoapp_github_token";
const GITHUB_AVATAR_URL = `https://github.com/${OWNER}.png`;

const VERCEL_TEAM_ID = "team_A2ZopFCq3xyFHuJ6wjek1u7q";
const VERCEL_TOKEN_KEY = "leosaquettoapp_vercel_token";
const VERCEL_API_ROOT = "https://api.vercel.com";
const WORKFLOW_DISPATCH_CACHE = {};
const VERCEL_PROJECTS = {
  "codex-usage": "prj_MFf7UyyesYKdZVkiyLMfXa5acrfp",
  "leosaquettoapp": "prj_QBNBVrao0BwJ09eIeMMQRoMmifXU",
  "grabnumber": "prj_BsNTMoUzF8XbA34v59k18YliveFD",
  "music-link-swapper": "prj_9NUF3qN5F1GEXqzA3oZBcnMkBJxK"
};

const CACHE_VERSION = "v7.3";

// 📦 CONFIGURAÇÃO DOS PROJETOS
const REPOS = [
  {
    name: "leosaquettoapp",
    icon: "📱",
    priority: 1,
    hasDeployPanel: true,
    showProductionDeploy: true,
    showPreviewDeploy: true,
    defaultBranch: "main",
    previewBranch: "staging",
    productionBranch: "main",
    productionEnvironment: "production",
    previewEnvironment: "preview",
    stagingEnvironment: "staging",
    previewUrl: "https://leosaquettoapp.vercel.app",
    productionUrl: "https://leosaquetto.com",
    deployKeywords: ["deploy", "vercel", "preview", "production", "prod"],
    usefulKeywords: ["deploy", "vercel", "preview", "production", "prod"]
  },
  {
    name: "grabnumber",
    icon: "🔢",
    priority: 2,
    hasDeployPanel: true,
    showProductionDeploy: true,
    showPreviewDeploy: true,
    defaultBranch: "main",
    previewBranch: "staging",
    productionBranch: "main",
    productionEnvironment: "production",
    previewEnvironment: "preview",
    stagingEnvironment: "staging",
    previewUrl: "https://grabnumber.vercel.app",
    productionUrl: "https://grabnumber.leosaquetto.com",
    deployKeywords: ["deploy", "vercel", "preview", "production", "prod"],
    usefulKeywords: ["deploy", "vercel", "preview", "production", "prod", "instagram", "telegram", "onlyfans", "privacy", "scraper", "stats"]
  },
  {
    name: "codex-usage",
    icon: "🤖",
    priority: 3,
    hasDeployPanel: true,
    showProductionDeploy: true,
    showPreviewDeploy: true,
    defaultBranch: "main",
    previewBranch: "staging",
    productionBranch: "main",
    productionEnvironment: "production",
    previewEnvironment: "preview",
    stagingEnvironment: "staging",
    previewUrl: "https://codex-usage-staging.vercel.app/api/usage",
    productionUrl: "https://codex-usage-nine.vercel.app",
    deployKeywords: ["deploy", "vercel", "preview", "production", "prod"],
    usefulKeywords: ["deploy", "vercel", "preview", "production", "prod", "usage"]
  },
  {
    name: "music-link-swapper",
    icon: "🎵",
    priority: 4,
    hasDeployPanel: true,
    showProductionDeploy: true,
    showPreviewDeploy: true,
    defaultBranch: "main",
    previewBranch: "staging",
    productionBranch: "main",
    productionEnvironment: "production",
    previewEnvironment: "preview",
    stagingEnvironment: "staging",
    previewUrl: "https://music-link-swapper.vercel.app",
    productionUrl: "https://swapper.leosaquetto.com",
    deployKeywords: ["deploy", "vercel", "preview", "production", "prod"],
    usefulKeywords: ["deploy", "vercel", "preview", "production", "prod", "test", "ci"]
  },
  {
    name: "uol-bot",
    icon: "📰",
    priority: 5,
    hasDeployPanel: false,
    defaultBranch: "main",
    previewBranch: "main",
    productionBranch: "main",
    previewUrl: "",
    productionUrl: "",
    deployKeywords: ["deploy", "production", "prod"],
    usefulKeywords: ["scraper", "consumer", "deploy", "run", "bot", "uol", "workflow", "manual"]
  },
  {
    name: "totodile",
    icon: "🐊",
    priority: 6,
    hasDeployPanel: false,
    defaultBranch: "main",
    previewBranch: "main",
    productionBranch: "main",
    previewUrl: "",
    productionUrl: "",
    deployKeywords: ["deploy", "production", "prod"],
    usefulKeywords: ["deploy", "bot", "telegram", "run", "workflow", "manual"]
  },
  {
    name: "statsam",
    icon: "📈",
    priority: 7,
    hasDeployPanel: false,
    defaultBranch: "main",
    previewBranch: "main",
    productionBranch: "main",
    previewUrl: "",
    productionUrl: "",
    deployKeywords: ["deploy", "production", "prod"],
    usefulKeywords: ["deploy", "stats", "scraper", "run", "workflow", "manual"]
  },
  {
    name: "html",
    icon: "🌐",
    priority: 8,
    hasDeployPanel: false,
    defaultBranch: "main",
    previewBranch: "main",
    productionBranch: "main",
    previewUrl: "",
    productionUrl: "",
    deployKeywords: ["deploy"],
    usefulKeywords: ["deploy", "pages", "workflow"]
  }
];

const ORDERED_REPOS = [...REPOS].sort((a, b) => (a.priority || 999) - (b.priority || 999));
const API_ROOT = "https://api.github.com";
const GITHUB_ROOT = "https://github.com";

// ==========================================
// 🛠 CORE / HELPERS / CACHE
// ==========================================

function sleep(seconds) { return new Promise(resolve => Timer.schedule(seconds * 1000, false, resolve)); }

async function getToken() {
  if (!Keychain.contains(TOKEN_KEY)) {
    const alert = new Alert();
    alert.title = "⚠️ Token GitHub Ausente";
    alert.message = `Salve seu token no Keychain:\n${TOKEN_KEY}`;
    alert.addAction("OK");
    await alert.present();
    throw new Error(`Token ausente.`);
  }
  return Keychain.get(TOKEN_KEY);
}

async function getVercelToken() {
  if (!Keychain.contains(VERCEL_TOKEN_KEY)) return null;
  return Keychain.get(VERCEL_TOKEN_KEY);
}

function cachePath(name) {
  const fm = FileManager.local();
  const dir = fm.joinPath(fm.cacheDirectory(), "github-hub");
  if (!fm.fileExists(dir)) fm.createDirectory(dir);
  return fm.joinPath(dir, name);
}

function readJsonCache(name, maxAgeSeconds) {
  const fm = FileManager.local();
  const path = cachePath(name);
  if (!fm.fileExists(path)) return null;
  const ageMs = Date.now() - fm.modificationDate(path).getTime();
  if (ageMs > maxAgeSeconds * 1000) return null;
  try { return JSON.parse(fm.readString(path)); } catch { return null; }
}

function writeJsonCache(name, data) {
  const fm = FileManager.local();
  fm.writeString(cachePath(name), JSON.stringify(data));
}

function cacheUpdatedAgoLabel(name) {
  const fm = FileManager.local();
  const path = cachePath(name);
  if (!fm.fileExists(path)) return "sem cache";
  const updatedAt = fm.modificationDate(path);
  return `atualizado ${formatRelativeDate(updatedAt)}`;
}

function formatProjectsCountLabel(count) {
  const n = Number(count || 0);
  return `${n} ${n === 1 ? "projeto" : "projetos"}`;
}

async function loadCachedImage(url, filename, maxAgeMinutes = 1440) {
  const fm = FileManager.local();
  const path = cachePath(filename);
  if (fm.fileExists(path)) {
    const ageMs = Date.now() - fm.modificationDate(path).getTime();
    if (ageMs < maxAgeMinutes * 60 * 1000) return fm.readImage(path);
  }
  try {
    const req = new Request(url);
    const img = await req.loadImage();
    fm.writeImage(path, img);
    return img;
  } catch(e) { return null; }
}

function parseJsonSafe(value) { try { return JSON.parse(value); } catch { return null; } }

async function githubRequest(url, method = "GET", body = null) {
  const token = await getToken();
  const req = new Request(url);
  req.method = method;
  req.headers = {
    "Authorization": `Bearer ${token}`,
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "Content-Type": "application/json",
    "User-Agent": "Scriptable-GitHub-Hub"
  };
  if (body) req.body = JSON.stringify(body);
  const response = await req.loadString();
  const status = req.response.statusCode;
  if (status >= 300 && status !== 304) {
    const detail = response ? `\nDetalhe: ${String(response).slice(0, 400)}` : "";
    throw new Error(`API Erro ${status}\nMétodo: ${method}\nURL: ${url}${detail}`);
  }
  return response ? parseJsonSafe(response) : null;
}

async function vercelRequest(path) {
  const token = await getVercelToken();
  if (!token) throw new Error(`Token Vercel ausente: ${VERCEL_TOKEN_KEY}`);
  const separator = path.includes("?") ? "&" : "?";
  const url = `${VERCEL_API_ROOT}${path}${separator}teamId=${encodeURIComponent(VERCEL_TEAM_ID)}`;
  const req = new Request(url);
  req.method = "GET";
  req.headers = {
    "Authorization": `Bearer ${token}`,
    "Content-Type": "application/json",
    "User-Agent": "Scriptable-Vercel-Hub"
  };
  const response = await req.loadString();
  const status = req.response.statusCode;
  if (status >= 300) throw new Error(`Vercel API Erro ${status}\n${url}`);
  return response ? parseJsonSafe(response) : null;
}

const repoApi = (repo) => `${API_ROOT}/repos/${OWNER}/${repo.name}`;
const repoWeb = (repo) => `${GITHUB_ROOT}/${OWNER}/${repo.name}`;
const runWeb = (repo, run) => run?.html_url || `${repoWeb(repo)}/actions/runs/${run.id}`;

const normalizeText = (val) => String(val || "").toLowerCase();
const workflowHaystack = (w) => normalizeText([w.name, w.path, w.state, w.id].join(" "));
const includesAny = (txt, keys) => (keys || []).some(k => normalizeText(txt).includes(normalizeText(k)));

const isPreviewWorkflow = (w) => includesAny(workflowHaystack(w), ["preview", "staging", "vercel_preview", "deploy preview"]);
const isProductionWorkflow = (w) => includesAny(workflowHaystack(w), ["production", "prod", "vercel_production", "deploy production"]);
const isDeployWorkflow = (repo, w) => includesAny(workflowHaystack(w), repo.deployKeywords || []);
const isUsefulWorkflow = (repo, w) => includesAny(workflowHaystack(w), repo.usefulKeywords || []);
const workflowLabel = (w) => `⚙️ ${w.name || w.path.split("/").pop()}`;
const formatDate = (v) => v ? new Date(v).toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" }) : "N/A";

// ==========================================
// 🛠 UI HELPERS & FORMATTERS
// ==========================================

function shortSha(run) {
  return run?.head_sha ? run.head_sha.slice(0, 7) : "sem sha";
}

function createCircularImage(image, size) {
  if(!image) return null;
  try {
    const ctx = new DrawContext();
    ctx.size = new Size(size, size);
    ctx.opaque = false;
    ctx.respectScreenScale = true;
    const path = new Path();
    path.addEllipse(new Rect(0, 0, size, size));
    ctx.addPath(path);
    ctx.clip();
    ctx.drawImageInRect(image, new Rect(0, 0, size, size));
    return ctx.getImage();
  } catch (e) { return image; }
}

function conclusionIcon(run) {
  if (!run) return "⚪";
  if (run.status === "queued" || run.status === "in_progress" || run.status === "requested") return "🟡";
  const c = run.conclusion;
  if (c === "success") return "🟢";
  if (c === "failure") return "🔴";
  if (c === "cancelled") return "🚫";
  if (c === "skipped") return "⏭️";
  return "⚪";
}

function deploymentIcon(deploy) {
  if (!deploy) return "⚪";
  const state = String(deploy.state || deploy.status?.state || "").toLowerCase();
  if (["success", "ready"].includes(state)) return "🟢";
  if (["failure", "error", "failed"].includes(state)) return "🔴";
  if (["inactive", "canceled", "cancelled"].includes(state)) return "⚫";
  if (["pending", "queued", "in_progress", "building"].includes(state)) return "🟡";
  return "⚪";
}

function formatRelativeDate(value) {
  if (!value) return "N/A";
  const date = new Date(value);
  const diffMs = Date.now() - date.getTime();
  const min = Math.floor(diffMs / 60000);
  const hour = Math.floor(min / 60);
  const day = Math.floor(hour / 24);

  if (min < 1) return "agora";
  if (min < 60) return `${min}m`;
  if (hour < 24) return `${hour}h`;
  if (day < 7) return `${day}d`;
  return formatDate(value).split(" ")[0];
}

function deploymentDate(deploy) {
  if (!deploy) return "—";
  return formatRelativeDate(deploy.updated_at || deploy.created_at);
}

function getPrimaryVercelUrl(item) {
  if (!item?.urls?.length) return "";
  const customDomain = item.urls.find(url => !url.includes("vercel.app"));
  return customDomain || item.urls[0];
}

function shortUrlLabel(url) {
  return String(url || "").replace("https://", "").replace("http://", "").replace(/\/$/, "");
}

function addSectionTitle(table, title) {
  const row = new UITableRow();
  row.height = 25;
  const cell = row.addText(title);
  cell.titleFont = Font.boldSystemFont(12);
  cell.titleColor = Color.dynamic(new Color("#8E8E93"), new Color("#98989D"));
  table.addRow(row);
}

function addSimpleActionRow(table, title, subtitle, onSelectCallback) {
  const row = new UITableRow();
  row.height = 48;
  row.dismissOnTap = Boolean(onSelectCallback);
  const cell = row.addText(title, subtitle || "");
  cell.titleFont = Font.semiboldSystemFont(14);
  cell.subtitleFont = Font.systemFont(11);
  cell.subtitleColor = Color.gray();
  if (onSelectCallback) row.onSelect = onSelectCallback;
  table.addRow(row);
}

function addRunRow(table, item, compact = false, onSelectCallback) {
  const row = new UITableRow();
  row.height = compact ? 44 : 50;
  row.dismissOnTap = true;
  
  const { repo, run } = item;
  const icon = conclusionIcon(run);

  const c1 = row.addText(`${repo.icon || "📦"} ${repo.name}`);
  c1.titleFont = Font.boldSystemFont(13);
  c1.widthWeight = 40;

  const actor = run?.actor?.login || "github";
  const runInfo = `${run.head_branch || "N/A"} • ${formatRelativeDate(run.updated_at || run.created_at)} • ${actor}`;
  const c2 = row.addText(`${icon} ${run.name || "workflow"}`, runInfo);
  c2.titleFont = Font.semiboldSystemFont(12);
  c2.subtitleFont = new Font("Menlo-Regular", 10);
  c2.subtitleColor = Color.gray();
  c2.widthWeight = 60;

  if (onSelectCallback) row.onSelect = onSelectCallback;
  table.addRow(row);
}

function addDeployPanelRow(table, repo, deployInfo, onSelectCallback) {
  const prodRun = deployInfo?.production || null;
  const previewRun = deployInfo?.preview || null;

  const row = new UITableRow();
  row.height = 50;
  row.dismissOnTap = true;

  const c1 = row.addText(`${repo.icon || "📦"} ${repo.name}`);
  c1.titleFont = Font.boldSystemFont(13);
  c1.widthWeight = 40;

  if (repo.showProductionDeploy !== false) {
    const c2 = row.addText("Produção", `${deploymentIcon(prodRun)} ${deploymentDate(prodRun)}`);
    c2.titleFont = Font.systemFont(9); c2.titleColor = Color.gray();
    c2.subtitleFont = Font.semiboldSystemFont(11);
    c2.widthWeight = 30;
  } else {
    const c2 = row.addText(""); c2.widthWeight = 30;
  }

  if (repo.showPreviewDeploy !== false) {
    const c3 = row.addText("Staging", `${deploymentIcon(previewRun)} ${deploymentDate(previewRun)}`);
    c3.titleFont = Font.systemFont(9); c3.titleColor = Color.gray();
    c3.subtitleFont = Font.semiboldSystemFont(11);
    c3.widthWeight = 30;
  } else {
    const c3 = row.addText(""); c3.widthWeight = 30;
  }

  if (onSelectCallback) row.onSelect = onSelectCallback;
  table.addRow(row);
}

function addVercelLinkRow(table, repo, item, deployInfo, onSelectCallback) {
  const row = new UITableRow();
  row.height = 56;
  row.dismissOnTap = true;

  const c1 = row.addText(`${repo.icon || "▲"} ${repo.name}`);
  c1.titleFont = Font.boldSystemFont(13);
  c1.widthWeight = 40;

  const primaryUrl = getPrimaryVercelUrl(item);
  const prod = deployInfo?.production || null;
  const prev = deployInfo?.preview || null;
  const deployLine = [
    repo.showProductionDeploy !== false ? `prod ${deploymentIcon(prod)} ${deploymentDate(prod)}` : "",
    repo.showPreviewDeploy !== false ? `stg ${deploymentIcon(prev)} ${deploymentDate(prev)}` : ""
  ].filter(Boolean).join("  ");
  const c2 = row.addText(
    primaryUrl ? shortUrlLabel(primaryUrl) : "sem link",
    deployLine || "sem deploy"
  );
  c2.titleFont = new Font("Menlo-Regular", 10);
  c2.subtitleFont = Font.systemFont(10);
  c2.subtitleColor = Color.gray();
  c2.widthWeight = 60;

  if (onSelectCallback) row.onSelect = onSelectCallback;
  table.addRow(row);
}

// ==========================================
// 📡 FETCHERS GITHUB & VERCEL
// ==========================================

async function fetchWorkflows(repo) {
  const data = await githubRequest(`${repoApi(repo)}/actions/workflows?per_page=100`);
  return data?.workflows || [];
}

async function fetchWorkflowRuns(repo, workflow, options = {}) {
  const params = [`per_page=${options.perPage || 10}`];
  if (options.branch) params.push(`branch=${encodeURIComponent(options.branch)}`);
  const wId = workflow.id ? encodeURIComponent(workflow.id) : workflow; 
  const url = workflow.id 
    ? `${repoApi(repo)}/actions/workflows/${wId}/runs?${params.join("&")}`
    : `${repoApi(repo)}/actions/runs?${params.join("&")}`; 
  const data = await githubRequest(url);
  return data?.workflow_runs || [];
}

async function triggerWorkflow(repo, workflow, ref) {
  const wId = encodeURIComponent(workflow.id || workflow.path);
  await githubRequest(`${repoApi(repo)}/actions/workflows/${wId}/dispatches`, "POST", { ref });
}

async function workflowHasManualDispatch(repo, workflow, ref) {
  if (!workflow?.path) return true;
  const cacheKey = `${repo.owner || OWNER}/${repo.name}:${workflow.path}@${ref}`;
  if (cacheKey in WORKFLOW_DISPATCH_CACHE) return WORKFLOW_DISPATCH_CACHE[cacheKey];
  try {
    const data = await githubRequest(`${repoApi(repo)}/contents/${encodeURIComponent(workflow.path)}?ref=${encodeURIComponent(ref)}`);
    const content = typeof data?.content === "string" ? data.content : "";
    if (!content) {
      WORKFLOW_DISPATCH_CACHE[cacheKey] = true;
      return true;
    }
    const normalizedContent = content.replace(/\n/g, "").replace(/-/g, "+").replace(/_/g, "/");
    const decodedData = Data.fromBase64String(normalizedContent);
    if (!decodedData) {
      WORKFLOW_DISPATCH_CACHE[cacheKey] = true;
      return true;
    }
    const decoded = decodedData.toRawString();
    const hasDispatch = /(^|\n)\s*workflow_dispatch\s*:/m.test(decoded) ||
      /\bon\s*:\s*\[[^\]]*\bworkflow_dispatch\b[^\]]*\]/m.test(decoded) ||
      /\bon\s*:\s*\n(?:\s*-\s*[\w"'-]+\s*\n)*\s*-\s*["']?workflow_dispatch["']?\s*$/m.test(decoded);
    WORKFLOW_DISPATCH_CACHE[cacheKey] = hasDispatch;
    return hasDispatch;
  } catch (e) {
    WORKFLOW_DISPATCH_CACHE[cacheKey] = true;
    return true;
  }
}

async function fetchDeployments(repo, environment, perPage = 3) {
  if (!environment) return [];
  const url = `${repoApi(repo)}/deployments?environment=${encodeURIComponent(environment)}&per_page=${perPage}`;
  const data = await githubRequest(url);
  return Array.isArray(data) ? data : [];
}

async function fetchDeploymentStatuses(repo, deployment, perPage = 5) {
  if (!deployment?.id) return [];
  const url = `${repoApi(repo)}/deployments/${deployment.id}/statuses?per_page=${perPage}`;
  const data = await githubRequest(url);
  return Array.isArray(data) ? data : [];
}

async function fetchLatestDeploymentWithStatus(repo, environments = []) {
  for (const env of environments.filter(Boolean)) {
    try {
      const deployments = await fetchDeployments(repo, env, 3);
      if (!deployments.length) continue;
      for (const deployment of deployments) {
        const statuses = await fetchDeploymentStatuses(repo, deployment, 5);
        const latestStatus = statuses[0] || null;
        if (!latestStatus) {
          return {
            environment: env, deployment, status: null, state: "unknown",
            created_at: deployment.created_at, updated_at: deployment.updated_at,
            url: deployment.payload?.web_url || deployment.environment_url || ""
          };
        }
        return {
          environment: env, deployment, status: latestStatus, state: latestStatus.state || "unknown",
          created_at: latestStatus.created_at || deployment.created_at,
          updated_at: latestStatus.updated_at || deployment.updated_at,
          url: latestStatus.environment_url || deployment.environment_url || deployment.payload?.web_url || ""
        };
      }
    } catch (e) {}
  }
  return null;
}

// --- VERCEL SPECIFIC FETCHERS ---

async function fetchVercelDeployments(repo, limit = 10) {
  const projectId = VERCEL_PROJECTS[repo.name];
  if (!projectId) return [];
  const path = `/v6/deployments?projectId=${encodeURIComponent(projectId)}&limit=${limit}`;
  const data = await vercelRequest(path);
  if (Array.isArray(data?.deployments)) return data.deployments;
  if (Array.isArray(data)) return data;
  return [];
}

function normalizeVercelDeployment(repo, d) {
  if (!d) return null;
  const state = d.readyState === "READY"
    ? "success"
    : String(d.readyState || d.state || "unknown").toLowerCase();
  const created = d.createdAt || d.created || d.buildingAt || d.ready;
  return {
    source: "vercel",
    environment: d.target || "preview",
    state,
    created_at: created,
    updated_at: d.ready || created,
    url: d.url ? `https://${d.url}` : "",
    deployment: {
      id: d.uid || d.id || "",
      ref: d.meta?.githubCommitRef || d.gitSource?.ref || d.target || "",
      sha: d.meta?.githubCommitSha || ""
    },
    status: {
      state
    },
    raw: d
  };
}

function getVercelDeploymentBranch(d) {
  return String(
    d?.meta?.githubCommitRef ||
    d?.meta?.githubCommitBranch ||
    d?.gitSource?.ref ||
    d?.gitSource?.branch ||
    d?.source?.ref ||
    d?.source?.branch ||
    d?.branch ||
    ""
  ).replace(/^refs\/heads\//, "");
}
function getVercelDeploymentTarget(d) {
  return String(
    d?.target ||
    d?.environment ||
    d?.meta?.vercelTarget ||
    ""
  ).toLowerCase();
}
function getVercelDeploymentUrl(d) {
  return String(d?.url || d?.alias?.[0] || "");
}
function isVercelProductionDeployment(repo, d) {
  const target = getVercelDeploymentTarget(d);
  const branch = getVercelDeploymentBranch(d);
  return (
    target === "production" ||
    branch === repo.productionBranch
  );
}
function isVercelPreviewDeployment(repo, d) {
  const target = getVercelDeploymentTarget(d);
  const branch = getVercelDeploymentBranch(d);
  const url = getVercelDeploymentUrl(d).toLowerCase();
  return (
    target === "preview" ||
    target === "staging" ||
    branch === repo.previewBranch ||
    url.includes("staging") ||
    url.includes("preview")
  );
}

async function fetchVercelDeploymentsByTarget(repo) {
  const limit = repo.name === "codex-usage" ? 50 : 20;
  const deployments = await fetchVercelDeployments(repo, limit);
  const readyDeployments = deployments.filter(d => {
    const state = String(d.readyState || d.state || "").toUpperCase();
    return !state || ["READY", "BUILDING", "ERROR", "QUEUED"].includes(state);
  });
  const productionRaw = readyDeployments.find(d => {
    return isVercelProductionDeployment(repo, d);
  });
  const previewRaw = readyDeployments.find(d => {
    return isVercelPreviewDeployment(repo, d);
  });
  return {
    production: normalizeVercelDeployment(repo, productionRaw),
    preview: normalizeVercelDeployment(repo, previewRaw)
  };
}

async function fetchLatestRunForBranch(repo, branch) {
  if (!branch) return null;
  const runs = await fetchWorkflowRuns(repo, "general", {
    perPage: 1,
    branch
  });
  return runs?.[0] || null;
}
function normalizeRunAsDeployment(repo, run, environment, url) {
  if (!run) return null;
  const state = run.status === "completed"
    ? (run.conclusion === "success" ? "success" : run.conclusion || "unknown")
    : run.status;
  return {
    source: "github-run",
    environment,
    state,
    created_at: run.created_at,
    updated_at: run.updated_at,
    url: url || "",
    deployment: {
      id: run.id,
      ref: run.head_branch,
      sha: run.head_sha || ""
    },
    status: {
      state
    },
    raw: run
  };
}

async function fetchDashboardData(options = {}) {
  const perRepoRuns = options.perRepoRuns || 3;
  const promises = ORDERED_REPOS.map(async (repo) => {
    try {
      const runsPromise = fetchWorkflowRuns(repo, "general", { perPage: perRepoRuns });
      const productionDeployPromise = repo.hasDeployPanel && repo.showProductionDeploy !== false
        ? fetchLatestDeploymentWithStatus(repo, [repo.productionEnvironment, "production", "Production"])
        : Promise.resolve(null);
      const previewDeployPromise = repo.hasDeployPanel && repo.showPreviewDeploy !== false
        ? fetchLatestDeploymentWithStatus(repo, [repo.previewEnvironment, repo.stagingEnvironment, "preview", "staging", "Preview", "Staging"])
        : Promise.resolve(null);

      const [runs, rawProductionDeploy, rawPreviewDeploy] = await Promise.all([
        runsPromise, 
        productionDeployPromise, 
        previewDeployPromise
      ]);

      let productionDeploy = rawProductionDeploy;
      let previewDeploy = rawPreviewDeploy;

      if (repo.hasDeployPanel && VERCEL_PROJECTS[repo.name]) {
        try {
          const vercelDeploys = await fetchVercelDeploymentsByTarget(repo);
          if (!productionDeploy && repo.showProductionDeploy !== false && vercelDeploys.production) {
            productionDeploy = vercelDeploys.production;
          }
          if (!previewDeploy && repo.showPreviewDeploy !== false && vercelDeploys.preview) {
            previewDeploy = vercelDeploys.preview;
          }
        } catch (e) {}
      }
      if (!previewDeploy && repo.showPreviewDeploy !== false && repo.previewBranch && repo.previewBranch !== repo.productionBranch) {
        try {
          const branchRun = await fetchLatestRunForBranch(repo, repo.previewBranch);
          previewDeploy = normalizeRunAsDeployment(
            repo,
            branchRun,
            repo.stagingEnvironment || repo.previewEnvironment || "staging",
            repo.previewUrl
          );
        } catch (e) {}
      }
      
      const normalizedRuns = runs.map(run => ({ repo, run, updatedAt: new Date(run.updated_at || run.created_at || 0).getTime() }));
      const sortedRuns = normalizedRuns.sort((a, b) => b.updatedAt - a.updatedAt);
      
      return {
        repo, runs: sortedRuns, latest: sortedRuns[0] || null,
        deploys: { production: productionDeploy, preview: previewDeploy }
      };
    } catch (e) {
      return { repo, runs: [], latest: null, deploys: { production: null, preview: null }, error: String(e.message || e) };
    }
  });

  const repoGroups = await Promise.all(promises);
  const globalRuns = repoGroups.flatMap(group => group.runs).sort((a, b) => b.updatedAt - a.updatedAt);
  const groupsByRepo = repoGroups.filter(group => group.runs.length).sort((a, b) => (b.latest?.updatedAt || 0) - (a.latest?.updatedAt || 0));
  const deployGroups = repoGroups.filter(group => group.repo.hasDeployPanel).sort((a, b) => (a.repo.priority || 999) - (b.repo.priority || 999));
  
  return { globalRuns, groupsByRepo, deployGroups, errors: repoGroups.filter(g => g.error) };
}

function hydrateDashboardData(cached) {
  const hydrateRunItem = (item) => ({ ...item, repo: REPOS.find(r => r.name === item.repo.name) || item.repo });
  return {
    globalRuns: cached.globalRuns.map(hydrateRunItem),
    groupsByRepo: cached.groupsByRepo.map(group => ({
      ...group,
      repo: REPOS.find(r => r.name === group.repo.name) || group.repo,
      runs: group.runs.map(hydrateRunItem),
      latest: group.latest ? hydrateRunItem(group.latest) : null
    })),
    deployGroups: cached.deployGroups.map(group => ({
      ...group,
      repo: REPOS.find(r => r.name === group.repo.name) || group.repo,
      runs: group.runs.map(hydrateRunItem),
      latest: group.latest ? hydrateRunItem(group.latest) : null,
      deploys: { production: group.deploys?.production || null, preview: group.deploys?.preview || null }
    })),
    errors: cached.errors
  };
}

async function fetchDashboardDataCached(force = false) {
  const cacheName = `dashboard-data-${CACHE_VERSION}.json`;
  if (!force) {
    const cached = readJsonCache(cacheName, 90); 
    if (cached) return hydrateDashboardData(cached);
  }
  const fresh = await fetchDashboardData({ perRepoRuns: 5 }); 
  writeJsonCache(cacheName, fresh);
  return fresh;
}

async function fetchWidgetDataCached(force = false) {
  const cacheName = `widget-dashboard-data-${CACHE_VERSION}.json`;
  if (!force) {
    const cached = readJsonCache(cacheName, 900); 
    if (cached) return hydrateDashboardData(cached);
  }
  const fresh = await fetchDashboardData({ perRepoRuns: 3 });
  writeJsonCache(cacheName, fresh);
  return fresh;
}

async function fetchVercelProjectByRepo(repo) {
  const projectId = VERCEL_PROJECTS[repo.name];
  if (!projectId) return null;
  return await vercelRequest(`/v9/projects/${encodeURIComponent(projectId)}`);
}

async function fetchVercelOfficialLinks(repo) {
  const project = await fetchVercelProjectByRepo(repo);
  if (!project) return null;
  const rawDomains = [];
  if (Array.isArray(project.domains)) rawDomains.push(...project.domains);
  if (Array.isArray(project.alias)) rawDomains.push(...project.alias);
  if (project.targets?.production?.alias) {
    const alias = project.targets.production.alias;
    if (Array.isArray(alias)) rawDomains.push(...alias);
    else rawDomains.push(alias);
  }
  if (project.latestDeployment?.url) {
    rawDomains.push(project.latestDeployment.url);
  }
  const cleanedDomains = rawDomains
    .map(item => {
      if (!item) return "";
      if (typeof item === "string") return item;
      return item.domain || item.name || item.url || "";
    })
    .filter(Boolean)
    .map(domain => domain.replace(/^https?:\/\//, "").replace(/\/$/, ""));
  const uniqueDomains = [...new Set(cleanedDomains)];
  const officialUrls = uniqueDomains.map(domain => `https://${domain}`);
  return {
    repoName: repo.name,
    projectId: project.id,
    projectName: project.name || repo.name,
    updatedAt: project.updatedAt,
    latestDeployment: project.latestDeployment || null,
    domains: uniqueDomains,
    urls: officialUrls
  };
}

async function fetchVercelLinksCached(force = false) {
  const cacheName = `vercel-official-links-${CACHE_VERSION}.json`;
  if (!force) {
    const cached = readJsonCache(cacheName, 3600);
    if (cached) return cached;
  }
  const repos = ORDERED_REPOS.filter(repo => VERCEL_PROJECTS[repo.name]);
  const results = await Promise.all(
    repos.map(async repo => {
      try { return await fetchVercelOfficialLinks(repo); } 
      catch (e) { return { repoName: repo.name, error: String(e.message || e), urls: [], domains: [] }; }
    })
  );
  const clean = results.filter(Boolean);
  writeJsonCache(cacheName, clean);
  return clean;
}

// ==========================================
// 🎨 VIEWS DO DASHBOARD & REPO HOME
// ==========================================

async function showDashboard() {
  let dashboardResult = { action: "EXIT" };
  const table = new UITable();
  table.showSeparators = true;
  
  const imgRow = new UITableRow();
  imgRow.height = 90;
  const rawImg = await loadCachedImage(GITHUB_AVATAR_URL, "avatar.png", 1440);
  if(rawImg) {
    const finalImg = createCircularImage(rawImg, 64);
    const imgCell = imgRow.addImage(finalImg || rawImg);
    imgCell.centerAligned();
  }
  table.addRow(imgRow);

  const headerRow = new UITableRow();
  headerRow.height = 40;
  const titleCell = headerRow.addText("LEO SAQUETTO", "deploys • workflows • repos");
  titleCell.titleFont = Font.blackSystemFont(20);
  titleCell.subtitleFont = Font.mediumSystemFont(11);
  titleCell.subtitleColor = Color.gray();
  titleCell.centerAligned();
  table.addRow(headerRow);

  const spacer1 = new UITableRow(); spacer1.height = 16; table.addRow(spacer1);

  const dashboardData = await fetchDashboardDataCached(false);

  addSectionTitle(table, "STATUS");
  const failed = dashboardData.globalRuns.filter(item => item.run.status === "completed" && item.run.conclusion === "failure");
  const running = dashboardData.globalRuns.filter(item => ["queued", "in_progress", "requested"].includes(item.run.status));

  const statusRow = new UITableRow();
  statusRow.height = 54;
  statusRow.dismissOnTap = true;
  
  const cFail = statusRow.addText(`🔴 ${failed.length}`, "Falhas");
  cFail.titleFont = Font.boldSystemFont(15); cFail.subtitleFont = Font.systemFont(11); cFail.centerAligned();
  
  const cRun = statusRow.addText(`🟡 ${running.length}`, "Rodando");
  cRun.titleFont = Font.boldSystemFont(15); cRun.subtitleFont = Font.systemFont(11); cRun.centerAligned();
  
  const cRef = statusRow.addText(`☰`, "Menu");
  cRef.titleFont = Font.boldSystemFont(15); cRef.subtitleFont = Font.systemFont(11); cRef.centerAligned();
  
  statusRow.onSelect = () => { dashboardResult = { action: "STATUS_MENU", failed, running }; };
  table.addRow(statusRow);

  const spacer2 = new UITableRow(); spacer2.height = 16; table.addRow(spacer2);

  addSectionTitle(table, "DEPLOYS");
  if (!dashboardData.deployGroups.length) {
    const emptyRow = new UITableRow(); emptyRow.height = 40;
    emptyRow.addText("Nenhum deploy configurado.").titleColor = Color.gray();
    table.addRow(emptyRow);
  } else {
    dashboardData.deployGroups.forEach(group => {
      addDeployPanelRow(table, group.repo, group.deploys, () => {
        dashboardResult = { action: "REPO_HOME", repo: group.repo };
      });
    });
  }

  const spacer3 = new UITableRow(); spacer3.height = 16; table.addRow(spacer3);

  addSectionTitle(table, "LINKS OFICIAIS VERCEL");
  const vCacheName = `vercel-official-links-${CACHE_VERSION}.json`;
  const cachedVercelLinks = readJsonCache(vCacheName, 3600);
  const cacheMeta = `${cacheUpdatedAgoLabel(vCacheName)} • ${formatProjectsCountLabel(cachedVercelLinks?.length || 0)}`;
  addSimpleActionRow(table, "🕒 Cache dos links Vercel", cacheMeta, null);
  addSimpleActionRow(table, "🔄 Atualizar links oficiais Vercel", "Buscar domínios oficiais dos projetos", () => {
    dashboardResult = { action: "REFRESH_VERCEL_LINKS" };
  });
  if (!cachedVercelLinks) {
    addSimpleActionRow(table, "▲ Nenhum link em cache", "Use atualizar para carregar os links", null);
  } else {
    addSimpleActionRow(table, "📋 Copiar links Vercel (cache)", "Copiar todos os domínios oficiais", () => {
      const urls = [...new Set(cachedVercelLinks.flatMap(item => item.urls || []))];
      if (urls.length) Pasteboard.copy(urls.join("\n"));
    });
    cachedVercelLinks.forEach(item => {
      const repo = REPOS.find(r => r.name === item.repoName);
      if (!repo) return;
      const deployGroup = dashboardData.deployGroups.find(g => g.repo.name === repo.name);
      addVercelLinkRow(table, repo, item, deployGroup?.deploys || null, () => {
        dashboardResult = { action: "VERCEL_LINKS_PANEL", repo, item };
      });
    });
  }

  const spacer4 = new UITableRow(); spacer4.height = 16; table.addRow(spacer4);

  addSectionTitle(table, "AUTOMAÇÕES CRÍTICAS");
  const automacoes = ORDERED_REPOS.filter(r => !r.hasDeployPanel);
  automacoes.forEach(repo => {
    addSimpleActionRow(table, `${repo.icon} ${repo.name}`, "Acessar atalhos e workflows", () => {
      dashboardResult = { action: "REPO_HOME", repo };
    });
  });

  const spacer5 = new UITableRow(); spacer5.height = 16; table.addRow(spacer5);

  addSectionTitle(table, "ATIVIDADE RECENTE");
  if (!dashboardData.globalRuns.length) {
    const emptyRow = new UITableRow(); emptyRow.height = 40;
    emptyRow.addText("Nenhuma atividade recente.").titleColor = Color.gray();
    table.addRow(emptyRow);
  } else {
    const activityPriority = (item) => {
      const status = item?.run?.status;
      const conclusion = item?.run?.conclusion;
      if (status === "completed" && conclusion === "failure") return 0;
      if (["queued", "in_progress", "requested", "waiting"].includes(status)) return 1;
      return 2;
    };
    const prioritizedRuns = [...dashboardData.globalRuns].sort((a, b) => {
      const p = activityPriority(a) - activityPriority(b);
      if (p !== 0) return p;
      return (b.updatedAt || 0) - (a.updatedAt || 0);
    });
    prioritizedRuns.slice(0, 6).forEach(item => {
      addRunRow(table, item, false, () => {
        dashboardResult = { action: "RUN_DETAILS", repo: item.repo, run: item.run };
      });
    });
  }

  await table.present();
  return dashboardResult;
}

async function showRepoHome(repo) {
  let result = { action: "BACK" };
  const table = new UITable();
  table.showSeparators = true;

  const titleRow = new UITableRow();
  titleRow.height = 60;
  const titleCell = titleRow.addText(repo.icon, repo.name.toUpperCase());
  titleCell.titleFont = Font.blackSystemFont(30);
  titleCell.subtitleFont = Font.boldSystemFont(18);
  titleCell.centerAligned();
  table.addRow(titleRow);

  let dashboardData = readJsonCache(`dashboard-data-${CACHE_VERSION}.json`, 90);
  if(!dashboardData) {
     dashboardData = await fetchDashboardData({ perRepoRuns: 5 }); 
     writeJsonCache(`dashboard-data-${CACHE_VERSION}.json`, dashboardData);
  } else {
     dashboardData = hydrateDashboardData(dashboardData);
  }
  
  const repoGroup = dashboardData.deployGroups.find(g => g.repo.name === repo.name) || 
                    dashboardData.groupsByRepo.find(g => g.repo.name === repo.name);
  
  const deploys = repoGroup?.deploys || { production: null, preview: null };
  const recentRuns = repoGroup?.runs || [];

  if (repo.hasDeployPanel) {
    addSectionTitle(table, "DEPLOYS (ENVIRONMENT)");
    addDeployPanelRow(table, repo, deploys, () => {}); 
  }

  addSectionTitle(table, "AÇÕES RÁPIDAS");
  if (repo.showProductionDeploy !== false) {
    addSimpleActionRow(table, "🌍 Acionar Produção", "Fazer deploy no environment principal", () => { result = { action: "QUICK_DEPLOY", repo, mode: "production" }; });
    if(repo.productionUrl) addSimpleActionRow(table, "🔗 Abrir site Produção", repo.productionUrl, () => { Safari.open(repo.productionUrl); });
  }
  if (repo.showPreviewDeploy !== false) {
    addSimpleActionRow(table, "👀 Acionar Staging/Preview", "Fazer deploy no environment secundário", () => { result = { action: "QUICK_DEPLOY", repo, mode: "preview" }; });
    if(repo.previewUrl) addSimpleActionRow(table, "🔗 Abrir site Preview", repo.previewUrl, () => { Safari.open(repo.previewUrl); });
  }

  addSectionTitle(table, "ATIVIDADE (WORKFLOWS)");
  if(!recentRuns.length) {
    const empty = new UITableRow(); empty.addText("Sem workflows rodados."); table.addRow(empty);
  } else {
    recentRuns.slice(0, 5).forEach(item => {
      addRunRow(table, item, true, () => { result = { action: "RUN_DETAILS", repo, run: item.run }; });
    });
  }

  addSectionTitle(table, "LINKS GITHUB & VERCEL");
  const links = [
    { label: "📁 Código Fonte", val: repoWeb(repo) },
    { label: "⚙️ GitHub Actions", val: `${repoWeb(repo)}/actions` },
    { label: "🔀 Pull Requests", val: `${repoWeb(repo)}/pulls` },
    { label: "🐛 Issues", val: `${repoWeb(repo)}/issues` },
    { label: "🔐 Secrets Actions", val: `${repoWeb(repo)}/settings/secrets/actions` }
  ];
  if(VERCEL_PROJECTS[repo.name]) links.push({ label: "▲ Projeto na Vercel", val: `https://vercel.com/leosaquettos-projects/${repo.name}` });

  links.forEach(l => {
    const r = new UITableRow(); r.height = 44; r.dismissOnTap = true;
    const c = r.addText(l.label); c.titleFont = Font.systemFont(14); c.titleColor = Color.dynamic(new Color("#333333"), new Color("#CCCCCC"));
    r.onSelect = () => { Safari.open(l.val); };
    table.addRow(r);
  });

  await table.present();
  return result;
}

// ==========================================
// 🧭 DETALHES & ACTIONS
// ==========================================

async function showFilteredRuns(title, runsList) {
  let result = { action: "BACK" };
  const table = new UITable(); table.showSeparators = true;
  const titleRow = new UITableRow(); titleRow.height = 60;
  const titleCell = titleRow.addText(title, `${runsList.length} workflows encontrados`);
  titleCell.titleFont = Font.blackSystemFont(20); titleCell.subtitleColor = Color.gray();
  table.addRow(titleRow);

  if (!runsList.length) {
    const empty = new UITableRow(); empty.height = 50; empty.addText("Vazio."); table.addRow(empty);
  } else {
    runsList.forEach(item => {
      addRunRow(table, item, false, () => { result = { action: "RUN_DETAILS", repo: item.repo, run: item.run }; });
    });
  }
  await table.present();
  return result;
}

async function showVercelLinksPanel(repo, item) {
  const urls = item?.urls || [];
  if (!urls.length) {
    await showInfo("Links Vercel", "Nenhum link oficial encontrado para esse projeto.");
    return;
  }
  const options = urls.map(url => ({ label: `🔗 ${shortUrlLabel(url)}`, value: url }));
  options.push({ label: "📋 Copiar todos", value: "COPY_ALL" });
  options.push({ label: "▲ Abrir projeto na Vercel", value: "OPEN_PROJECT" });
  
  const msg = [
    `Projeto: ${item.projectName || repo.name}`,
    `Domínios: ${item.domains?.length || 0}`,
    item.latestDeployment?.createdAt ? `Último deploy: ${formatDate(item.latestDeployment.createdAt)}` : null
  ].filter(Boolean).join("\n");
  
  const choice = await presentMenu(`▲ ${repo.name}`, msg, options);
  if (choice === "BACK") return;
  if (choice === "COPY_ALL") {
    Pasteboard.copy(urls.join("\n"));
    await showInfo("Copiado", "Links oficiais copiados.");
    return;
  }
  if (choice === "OPEN_PROJECT") { Safari.open(`https://vercel.com/leosaquettos-projects/${repo.name}`); return; }
  Safari.open(choice);
}

async function presentMenu(title, message, options, showBack = true) {
  const alert = new Alert();
  alert.title = title;
  if (message) alert.message = message;
  options.forEach(opt => alert.addAction(opt.label));
  alert.addCancelAction(showBack ? "🔙 Voltar" : "❌ Fechar");
  const index = await alert.presentSheet();
  if (index === -1) return "BACK";
  return options[index].value;
}

async function showInfo(title, message, actions = []) {
  const alert = new Alert();
  alert.title = title;
  alert.message = message;
  actions.forEach(action => alert.addAction(action.label));
  alert.addCancelAction("🔙 Fechar");
  const choice = await alert.presentAlert();
  if (choice >= 0 && actions[choice]?.handler) await actions[choice].handler();
  return choice;
}

async function quickDeploy(repo, mode) {
  const workflows = await fetchWorkflows(repo);
  const activeWfs = workflows.filter(w => w.state === "active");
  const isTarget = mode === "preview" ? isPreviewWorkflow : isProductionWorkflow;
  const ref = mode === "preview" ? repo.previewBranch || repo.defaultBranch || "main" : repo.productionBranch || repo.defaultBranch || "main";

  let candidates = activeWfs.filter(w => isDeployWorkflow(repo, w) && isTarget(w));
  if (!candidates.length) candidates = activeWfs.filter(w => isDeployWorkflow(repo, w));
  if (candidates.length) {
    const filtered = [];
    for (const wf of candidates) {
      if (await workflowHasManualDispatch(repo, wf, ref)) {
        filtered.push(wf);
      }
    }
    if (filtered.length) candidates = filtered;
  }
  
  if (!candidates.length) {
    await showInfo("⚠️ Nenhum deploy", `Não encontrei workflow de deploy em ${repo.name}.`);
    return;
  }

  const workflow = candidates[0];

  const confirm = await presentMenu(
    mode === "preview" ? "👀 Deploy Preview" : "🌍 Deploy Produção",
    `Repo: ${repo.name}\nWorkflow: ${workflow.name}\nBranch/ref: ${ref}`,
    [{ label: "🚀 Acionar agora", value: "RUN" }, { label: "⚙️ Escolher outro workflow", value: "CHOOSE" }]
  );

  if (confirm === "BACK") return;
  if (confirm === "CHOOSE") {
    const wfOptions = candidates.map(w => ({ label: workflowLabel(w), value: w }));
    const chosen = await presentMenu("Escolher Workflow", repo.name, wfOptions);
    if (chosen === "BACK") return;
    try {
      await triggerWorkflow(repo, chosen, ref);
      await showInfo("✅ Acionado", `${chosen.name} iniciou em ${ref}.`);
    } catch (e) {
      const errMsg = String(e.message || e);
      await showInfo("❌ Falha ao acionar", errMsg, [
        { label: "📋 Copiar erro", handler: async () => Pasteboard.copy(errMsg) },
        { label: "🌐 Abrir Actions", handler: async () => Safari.open(`${repoWeb(repo)}/actions`) }
      ]);
    }
    return;
  }
  let triggered = null;
  let lastError = null;
  for (const wf of candidates) {
    try {
      await triggerWorkflow(repo, wf, ref);
      triggered = wf;
      break;
    } catch (e) {
      lastError = e;
      const msg = String(e.message || e);
      if (!msg.includes("API Erro 422")) break;
    }
  }
  if (!triggered) {
    const errMsg = String(lastError?.message || "Nenhum workflow aceitou workflow_dispatch para esse ref.");
    await showInfo("❌ Falha ao acionar", errMsg, [
      { label: "📋 Copiar erro", handler: async () => Pasteboard.copy(errMsg) },
      { label: "🌐 Abrir Actions", handler: async () => Safari.open(`${repoWeb(repo)}/actions`) }
    ]);
    return;
  }
  await showInfo("✅ Acionado", `${triggered.name} iniciou em ${ref}.`);
}

async function handleRunDetails(repo, run, targetUrl = null) {
  let currentRun = run;
  while (true) {
    const icon = conclusionIcon(currentRun);
    const msg = [
      `Repo: ${repo.name}`,
      `Nome: ${currentRun.name || "Workflow"}`,
      `Status: ${currentRun.status || "desconhecido"}`,
      `Conclusão: ${currentRun.conclusion || "em andamento"}`,
      `Branch: ${currentRun.head_branch || "N/A"}`,
      `Evento: ${currentRun.event || "N/A"}`,
      `Autor: ${currentRun?.actor?.login || "github"}`,
      `SHA: ${shortSha(currentRun)}`,
      `Atualizado: ${formatDate(currentRun.updated_at)}`
    ].join("\n");

    const isRunning = ["in_progress", "queued", "requested", "waiting"].includes(currentRun.status);
    const options = [{ label: "🔄 Recarregar Status", value: "RELOAD" }];

    if (isRunning) {
      options.push({ label: "🛑 Cancelar Workflow", value: "CANCEL" });
    } else {
      options.push({ label: "🔁 Re-executar Run", value: "RERUN" });
    }

    if (targetUrl) options.push({ label: `🔗 Abrir URL`, value: "TARGET" });
    options.push({ label: "📋 Copiar URL do Run", value: "COPY_RUN_URL" });
    options.push({ label: "🌿 Abrir Branch", value: "BRANCH" });
    options.push({ label: "🌐 Abrir Actions no Safari", value: "WEB" });

    const choice = await presentMenu(`${icon} Detalhes do Run`, msg, options);

    if (choice === "BACK") break;
    if (choice === "COPY_RUN_URL") { Pasteboard.copy(runWeb(repo, currentRun)); await showInfo("Copiado", "URL copiada."); }
    if (choice === "BRANCH" && currentRun.head_branch) Safari.open(`${repoWeb(repo)}/tree/${encodeURIComponent(currentRun.head_branch)}`);
    if (choice === "WEB") Safari.open(runWeb(repo, currentRun));
    if (choice === "TARGET") Safari.open(targetUrl);
    
    if (choice === "RELOAD") {
      const fresh = await githubRequest(`${repoApi(repo)}/actions/runs/${currentRun.id}`);
      if (fresh) currentRun = fresh;
    }
    if (choice === "CANCEL") {
      try {
        await githubRequest(`${repoApi(repo)}/actions/runs/${currentRun.id}/cancel`, "POST");
        currentRun.status = "completed"; currentRun.conclusion = "cancelled";
      } catch (e) {}
    }
    if (choice === "RERUN") {
      try {
        await githubRequest(`${repoApi(repo)}/actions/runs/${currentRun.id}/rerun`, "POST");
        const fresh = await githubRequest(`${repoApi(repo)}/actions/runs/${currentRun.id}`);
        if (fresh) currentRun = fresh;
      } catch (e) {}
    }
  }
}

// ==========================================
// 🚀 STATE MACHINE / NAVEGAÇÃO APP
// ==========================================

async function runApp() {
  let state = "DASHBOARD";
  let activeRepo = null;

  while (state !== "EXIT") {
    try {
      if (state === "DASHBOARD") {
        const result = await showDashboard();
        
        if (result.action === "EXIT") state = "EXIT";
        
        if (result.action === "STATUS_MENU") {
          const opt = await presentMenu("Status Rápido", "Escolha a visão:", [
            { label: `🔴 Falhas Recentes (${result.failed.length})`, value: "FAILURES" },
            { label: `🟡 Em Andamento (${result.running.length})`, value: "RUNNING" },
            { label: `🔄 Recarregar Dados da API`, value: "REFRESH" },
            { label: `▲ Atualizar links Vercel`, value: "REFRESH_VERCEL" }
          ]);
          if (opt === "FAILURES") { const r = await showFilteredRuns("Falhas Recentes", result.failed); if(r.action === "RUN_DETAILS") await handleRunDetails(r.repo, r.run); state = "DASHBOARD"; }
          else if (opt === "RUNNING") { const r = await showFilteredRuns("Em Andamento", result.running); if(r.action === "RUN_DETAILS") await handleRunDetails(r.repo, r.run); state = "DASHBOARD"; }
          else if (opt === "REFRESH") { await fetchDashboardDataCached(true); state = "DASHBOARD"; }
          else if (opt === "REFRESH_VERCEL") { await fetchVercelLinksCached(true); state = "DASHBOARD"; }
          else state = "DASHBOARD";
        }

        if (result.action === "REFRESH_DASHBOARD") { await fetchDashboardDataCached(true); state = "DASHBOARD"; }
        if (result.action === "REFRESH_VERCEL_LINKS") { await fetchVercelLinksCached(true); state = "DASHBOARD"; }
        if (result.action === "VERCEL_LINKS_PANEL") { await showVercelLinksPanel(result.repo, result.item); state = "DASHBOARD"; }
        
        if (result.action === "LIST_RUNS") {
          const r = await showFilteredRuns(result.title, result.runs);
          if (r.action === "RUN_DETAILS") await handleRunDetails(r.repo, r.run);
          state = "DASHBOARD";
        }
        if (result.action === "RUN_DETAILS") { await handleRunDetails(result.repo, result.run); state = "DASHBOARD"; }
        if (result.action === "REPO_HOME") { activeRepo = result.repo; state = "REPO_HOME"; }
      }

      else if (state === "REPO_HOME") {
        const r = await showRepoHome(activeRepo);
        if (r.action === "BACK") state = "DASHBOARD";
        if (r.action === "QUICK_DEPLOY") { 
            await quickDeploy(r.repo, r.mode); 
            await fetchDashboardDataCached(true);
            state = "REPO_HOME"; 
        }
        if (r.action === "RUN_DETAILS") { await handleRunDetails(r.repo, r.run); state = "REPO_HOME"; }
      }
    } catch (e) {
      await showInfo("❌ Erro Crítico", String(e.message || e));
      state = "DASHBOARD";
    }
  }
}

// ==========================================
// 📱 WIDGET MODULE & ENGINE
// ==========================================

function parseWidgetParameter(parameter) {
  const raw = String(parameter || "overview").trim();
  if (raw.includes(":")) {
    const [mode, value] = raw.split(":").map(x => x.trim());
    return { mode, value };
  }
  return { mode: raw || "overview", value: "" };
}

function widgetLimit(small, medium, large) {
  if (config.widgetFamily === "small") return small;
  if (config.widgetFamily === "medium") return medium;
  return large;
}

function applyWidgetBackground(widget) {
  const gradient = new LinearGradient();
  gradient.colors = [new Color("#242424"), new Color("#111111")];
  gradient.locations = [0, 1];
  widget.backgroundGradient = gradient;
}

function addWidgetHeader(widget, title, subtitle = "") {
  const row = widget.addStack();
  row.centerAlignContent();
  const titleText = row.addText(title);
  titleText.font = Font.boldSystemFont(12);
  titleText.textColor = Color.white();
  titleText.lineLimit = 1;
  if (subtitle) {
    widget.addSpacer(4);
    const sub = widget.addText(subtitle);
    sub.font = Font.systemFont(9);
    sub.textColor = new Color("#AAAAAA");
    sub.lineLimit = 1;
  }
  widget.addSpacer(8);
}

function addWidgetLine(widget, left, right, subtitle = "") {
  const row = widget.addStack();
  row.centerAlignContent();
  const leftText = row.addText(left);
  leftText.font = Font.semiboldSystemFont(10);
  leftText.textColor = Color.white();
  leftText.lineLimit = 1;
  row.addSpacer();
  const rightText = row.addText(right);
  rightText.font = Font.mediumSystemFont(10);
  rightText.textColor = new Color("#CCCCCC");
  rightText.lineLimit = 1;
  if (subtitle) {
    widget.addSpacer(3);
    const sub = widget.addText(subtitle);
    sub.font = Font.systemFont(8);
    sub.textColor = new Color("#8E8E93");
    sub.lineLimit = 1;
  }
  widget.addSpacer(4);
}

function buildWidgetError(widget, err) {
  addWidgetHeader(widget, "github hub", "erro");
  const text = widget.addText(String(err.message || err));
  text.font = Font.systemFont(10);
  text.textColor = new Color("#FF453A");
  text.lineLimit = 4;
}

async function buildOverviewWidget(widget) {
  const data = await fetchWidgetDataCached(false);
  const failed = data.globalRuns.filter(item => item.run.status === "completed" && item.run.conclusion === "failure");
  const running = data.globalRuns.filter(item => ["queued", "in_progress", "requested"].includes(item.run.status));
  
  addWidgetHeader(widget, "github hub", `falhas ${failed.length} • rodando ${running.length}`);
  const limit = widgetLimit(2, 4, 8);

  data.deployGroups.slice(0, limit).forEach(group => {
    const repo = group.repo;
    const prod = group.deploys?.production;
    const prev = group.deploys?.preview;
    const prodText = prod ? `${deploymentIcon(prod)} ${deploymentDate(prod)}` : "—";
    const prevText = prev ? `${deploymentIcon(prev)} ${deploymentDate(prev)}` : "—";
    addWidgetLine(widget, `${repo.icon} ${repo.name}`, `p ${prodText}   s ${prevText}`);
  });
}

async function buildDeploysWidget(widget) {
  const data = await fetchWidgetDataCached(false);
  addWidgetHeader(widget, "deploys reais", "production • staging");
  const limit = widgetLimit(2, 4, 8);

  data.deployGroups.slice(0, limit).forEach(group => {
    const repo = group.repo;
    const prod = group.deploys?.production;
    const prev = group.deploys?.preview;
    const prodLabel = repo.showProductionDeploy === false ? "" : `prod ${deploymentIcon(prod)} ${deploymentDate(prod)}`;
    const prevLabel = repo.showPreviewDeploy === false ? "" : `stg ${deploymentIcon(prev)} ${deploymentDate(prev)}`;
    addWidgetLine(widget, `${repo.icon} ${repo.name}`, [prodLabel, prevLabel].filter(Boolean).join("  "));
  });
}

async function buildRepoWidget(widget, repoName) {
  const repo = ORDERED_REPOS.find(r => r.name.toLowerCase() === String(repoName).toLowerCase()) || ORDERED_REPOS[0];
  const data = await fetchWidgetDataCached(false);
  const group = data.deployGroups.find(g => g.repo.name === repo.name) || data.groupsByRepo.find(g => g.repo.name === repo.name);

  addWidgetHeader(widget, `${repo.icon} ${repo.name}`, repo.hasDeployPanel ? "deploys • actions" : "actions");

  if (repo.hasDeployPanel && group?.deploys) {
    const prod = group.deploys.production;
    const prev = group.deploys.preview;
    if (repo.showProductionDeploy !== false) addWidgetLine(widget, "produção", `${deploymentIcon(prod)} ${deploymentDate(prod)}`);
    if (repo.showPreviewDeploy !== false) addWidgetLine(widget, "staging", `${deploymentIcon(prev)} ${deploymentDate(prev)}`);
    widget.addSpacer(4);
  }

  const runs = group?.runs || [];
  const limit = widgetLimit(2, 4, 8);
  runs.slice(0, limit).forEach(item => {
    addWidgetLine(
      widget,
      conclusionIcon(item.run) + " " + (item.run.name || "workflow"),
      formatRelativeDate(item.run.updated_at || item.run.created_at),
      item.run.head_branch || ""
    );
  });
}

async function buildFailuresWidget(widget) {
  const data = await fetchWidgetDataCached(false);
  const failed = data.globalRuns.filter(item => item.run.status === "completed" && item.run.conclusion === "failure");
  addWidgetHeader(widget, "falhas recentes", `${failed.length} encontradas`);

  if (!failed.length) {
    const ok = widget.addText("sem falhas recentes");
    ok.font = Font.semiboldSystemFont(13);
    ok.textColor = new Color("#34C759");
    return;
  }
  const limit = widgetLimit(2, 5, 8);
  failed.slice(0, limit).forEach(item => {
    addWidgetLine(widget, `🔴 ${item.repo.name}`, formatRelativeDate(item.run.updated_at || item.run.created_at), item.run.name || "workflow");
  });
}

async function buildRunningWidget(widget) {
  const data = await fetchWidgetDataCached(false);
  const running = data.globalRuns.filter(item => ["queued", "in_progress", "requested"].includes(item.run.status));
  addWidgetHeader(widget, "rodando agora", `${running.length} ativos`);

  if (!running.length) {
    const idle = widget.addText("nada em andamento");
    idle.font = Font.semiboldSystemFont(13);
    idle.textColor = new Color("#8E8E93");
    return;
  }
  const limit = widgetLimit(2, 5, 8);
  running.slice(0, limit).forEach(item => {
    addWidgetLine(widget, `🟡 ${item.repo.name}`, formatRelativeDate(item.run.updated_at || item.run.created_at), item.run.name || "workflow");
  });
}

async function buildVercelWidget(widget) {
  const vCacheName = `vercel-official-links-${CACHE_VERSION}.json`;
  const cached = readJsonCache(vCacheName, 3600);
  addWidgetHeader(widget, "vercel links", cached ? "domínios oficiais" : "cache vazio");

  if (!cached) {
    const text = widget.addText("abra o app para carregar");
    text.font = Font.systemFont(12);
    text.textColor = new Color("#AAAAAA");
    return;
  }
  const limit = widgetLimit(2, 4, 8);
  cached.slice(0, limit).forEach(item => {
    const repo = REPOS.find(r => r.name === item.repoName);
    const url = getPrimaryVercelUrl(item);
    addWidgetLine(widget, `${repo?.icon || "▲"} ${item.repoName}`, shortUrlLabel(url));
  });
}

async function createWidget(parameter) {
  const parsed = parseWidgetParameter(parameter);
  const mode = parsed.mode;
  const value = parsed.value;

  const widget = new ListWidget();
  applyWidgetBackground(widget);
  widget.setPadding(12, 12, 12, 12);
  widget.refreshAfterDate = new Date(Date.now() + 15 * 60 * 1000);

  try {
    if (mode === "deploys") await buildDeploysWidget(widget);
    else if (mode === "failures") await buildFailuresWidget(widget);
    else if (mode === "running") await buildRunningWidget(widget);
    else if (mode === "repo") await buildRepoWidget(widget, value);
    else if (mode === "vercel") await buildVercelWidget(widget);
    else await buildOverviewWidget(widget);
  } catch (e) {
    buildWidgetError(widget, e);
  }

  widget.url = `scriptable:///run/${encodeURIComponent(Script.name())}?widget=${encodeURIComponent(parameter || "overview")}`;
  return widget;
}

if (config.runsInWidget) {
  const widget = await createWidget(args.widgetParameter);
  Script.setWidget(widget);
  Script.complete();
} else {
  await runApp();
  Script.complete();
}
