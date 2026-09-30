const STATUSES = ["NEW", "HOT", "WARM", "COLD", "CONVERTED", "LOST"];
const STAT_LABELS = [
  ["total_customers", "Total Customers"], ["total_leads", "Total Leads"], ["hot_leads", "Hot Leads"],
  ["warm_leads", "Warm Leads"], ["converted_leads", "Converted Leads"],
];
const $ = (id) => document.getElementById(id);
const csrf = () => (document.cookie.match(/csrftoken=([^;]+)/) || [])[1] || "";

function el(tag, text, cls) {
  const e = document.createElement(tag);
  if (text !== undefined) e.textContent = text;
  if (cls) e.className = cls;
  return e;
}

function cell(tr, content) {
  const td = document.createElement("td");
  if (content instanceof Node) td.appendChild(content);
  else td.textContent = content;
  tr.appendChild(td);
  return td;
}

async function api(url, method = "GET", body) {
  const r = await fetch(url, {
    method, credentials: "same-origin",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrf() },
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(data.error || data.detail || JSON.stringify(data));
  return data;
}

async function act(fn) {
  try { await fn(); await load(); } catch (e) { alert(e.message); }
}

function renderStats(s) {
  const box = $("stats");
  box.replaceChildren();
  for (const [key, label] of STAT_LABELS) {
    const c = el("div", undefined, "card");
    c.append(el("div", s[key], "num"), el("div", label, "lbl"));
    box.appendChild(c);
  }
}

function renderLeads(leads) {
  const body = $("leads-body");
  body.replaceChildren();
  for (const l of leads) {
    const tr = document.createElement("tr");
    const who = el("div");
    who.append(el("strong", l.customer.name), el("small", [l.customer.phone, l.customer.email].filter(Boolean).join(" · ")));
    cell(tr, who);
    cell(tr, l.message).dir = "auto";
    cell(tr, l.lead_score);
    cell(tr, el("span", l.status, "badge " + l.status));
    cell(tr, new Date(l.created_at).toLocaleString());

    const sel = el("select");
    for (const s of STATUSES) {
      const o = el("option", s);
      o.value = s;
      o.selected = s === l.status;
      sel.appendChild(o);
    }
    sel.onchange = () => act(() => api(`/api/leads/${l.id}/`, "PUT", { status: sel.value }));
    const note = el("button", "Follow-up", "ghost");
    note.onclick = () => {
      const t = prompt("Follow-up note (scheduled for tomorrow):");
      if (t) act(() => api(`/api/leads/${l.id}/`, "PUT", { note: t }));
    };
    const actions = el("div", undefined, "actions");
    actions.append(sel, note);
    cell(tr, actions);
    body.appendChild(tr);
  }
}

function renderCustomers(customers) {
  const body = $("customers-body");
  body.replaceChildren();
  for (const c of customers) {
    const tr = document.createElement("tr");
    [c.name, c.phone, c.email, c.leads_count, new Date(c.created_at).toLocaleString()].forEach((v) => cell(tr, v));
    body.appendChild(tr);
  }
}

function renderKnowledge(docs) {
  const ul = $("kb-list");
  ul.replaceChildren();
  for (const d of docs) ul.appendChild(el("li", `[${d.category}] ${d.title}`));
}

async function load() {
  try {
    const [stats, leads, customers, docs] = await Promise.all([
      api("/api/stats/"), api("/api/leads/"), api("/api/customers/"), api("/api/knowledge/"),
    ]);
    renderStats(stats); renderLeads(leads); renderCustomers(customers); renderKnowledge(docs);
  } catch (e) { alert(e.message); }
}

$("kb-form").addEventListener("submit", (e) => {
  e.preventDefault();
  act(async () => {
    await api("/api/knowledge/", "POST", {
      title: $("kb-title").value, category: $("kb-category").value, content: $("kb-content").value,
    });
    $("kb-form").reset();
  });
});

load();