const lessons = [
  { id: "00-course-roadmap", number: "00", phase: "ภาพรวม", title: "Course Roadmap", short: "เป้าหมายและเส้นทางการเรียน" },
  { id: "01-installation", number: "01", phase: "เริ่มต้น", title: "การติดตั้งสำหรับผู้เริ่มต้น", short: "เตรียม Python และเครื่องมือ" },
  { id: "02-web-basics", number: "02", phase: "พื้นฐาน Web", title: "พื้นฐาน Web, HTML, HTTP และ Developer Tools", short: "อ่านโครงสร้างหน้าเว็บให้เป็น" },
  { id: "03-api-first", number: "03", phase: "API First", title: "API First", short: "เลือกช่องทางข้อมูลที่เหมาะสม" },
  { id: "04-static-scraping", number: "04", phase: "Static", title: "Static Website ด้วย Requests และ BeautifulSoup", short: "ดึงข้อมูลจาก HTML" },
  { id: "05-pagination-downloads", number: "05", phase: "Pagination", title: "Pagination และการดาวน์โหลดไฟล์", short: "วนหน้าและดาวน์โหลดอย่างปลอดภัย" },
  { id: "06-dynamic-playwright", number: "06", phase: "Dynamic", title: "Dynamic Website ด้วย Playwright", short: "จัดการเว็บที่สร้างด้วย JavaScript" },
  { id: "07-selenium", number: "07", phase: "Browser Automation", title: "Selenium", short: "เปรียบเทียบและใช้งาน Selenium" },
  { id: "08-error-resilience", number: "08", phase: "Resilience", title: "ระบบรองรับ Error และ Resilience", short: "Retry, timeout และ validation" },
  { id: "09-ethics-security", number: "09", phase: "Ethics & Security", title: "สิทธิ์ กฎหมาย จริยธรรม และความปลอดภัย", short: "เช็กให้พร้อมก่อนดึงข้อมูลจริง" },
  { id: "10-data-pipeline", number: "10", phase: "Data Pipeline", title: "Export และ Data Pipeline", short: "จัดเก็บและส่งต่อข้อมูล" },
  { id: "11-testing-maintenance", number: "11", phase: "Quality", title: "Testing และ Maintenance", short: "ทำให้ scraper ดูแลต่อได้" },
  { id: "12-use-cases", number: "12", phase: "Use Cases", title: "Use Cases", short: "ต่อยอดเป็นงานจริงหลายรูปแบบ" },
  { id: "13-scheduling-automation", number: "13", phase: "Automation", title: "Scheduling และ Automation", short: "ตั้งเวลาทำงานบน Windows" },
  { id: "14-github-docs-ci", number: "14", phase: "Share & CI", title: "GitHub Documentation และ CI", short: "ตรวจคุณภาพก่อนแชร์" },
  { id: "15-final-review", number: "15", phase: "Final Review", title: "Final Review", short: "สรุปและเตรียม Capstone" }
];

const state = { currentId: null, completed: loadCompleted(), cache: new Map() };
const $ = (selector) => document.querySelector(selector);
const lessonById = (id) => lessons.find((lesson) => lesson.id === id);

function loadCompleted() {
  try { return new Set(JSON.parse(localStorage.getItem("scraping-course-completed") || "[]")); }
  catch { return new Set(); }
}

function saveCompleted() { localStorage.setItem("scraping-course-completed", JSON.stringify([...state.completed])); }

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[character]));
}

function inlineMarkdown(value) {
  let html = escapeHtml(value);
  const codeSpans = [];
  html = html.replace(/`([^`]+)`/g, (_, code) => { codeSpans.push(`<code>${code}</code>`); return `@@CODE${codeSpans.length - 1}@@`; });
  html = html.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, (_, alt, url) => `<img src="${escapeHtml(url)}" alt="${alt}">`);
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, label, url) => `<a href="${normalizeLink(url)}">${label}</a>`);
  html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/__([^_]+)__/g, "<strong>$1</strong>");
  html = html.replace(/\*([^*]+)\*/g, "<em>$1</em>");
  html = html.replace(/_([^_]+)_/g, "<em>$1</em>");
  return html.replace(/@@CODE(\d+)@@/g, (_, index) => codeSpans[Number(index)]);
}

function normalizeLink(url) {
  const cleanUrl = url.replace(/&amp;/g, "&");
  const match = cleanUrl.match(/(?:\.\.\/)?(?:docs\/)?(\d{2}-[a-z0-9-]+)\.md(?:#.*)?$/i);
  if (match && lessonById(match[1])) return `?lesson=${match[1]}`;
  if (cleanUrl.startsWith("#")) return cleanUrl;
  if (/^https?:\/\//i.test(cleanUrl)) return cleanUrl;
  return `https://github.com/itipunsnk-max/8.0.Web-Scraping_API-Static-Dynamic/blob/main/${cleanUrl.replace(/^\.\.\//, "")}`;
}

function isTableDivider(line) { return /^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$/.test(line); }
function tableRow(line) { return line.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((cell) => cell.trim()); }

function markdownToHtml(markdown) {
  const lines = markdown.replace(/\r\n?/g, "\n").split("\n");
  const output = [];
  let paragraph = [];
  let listType = null;
  let listItems = [];
  let codeLines = null;
  let codeLanguage = "";

  const flushParagraph = () => { if (paragraph.length) { output.push(`<p>${inlineMarkdown(paragraph.join(" "))}</p>`); paragraph = []; } };
  const flushList = () => { if (listItems.length) { output.push(`<${listType}>${listItems.map((item) => `<li>${inlineMarkdown(item)}</li>`).join("")}</${listType}>`); listItems = []; listType = null; } };
  const flushCode = () => { if (codeLines !== null) { output.push(`<pre><code class="language-${escapeHtml(codeLanguage)}">${escapeHtml(codeLines.join("\n"))}</code></pre>`); codeLines = null; codeLanguage = ""; } };

  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];
    const fence = line.match(/^\s*```\s*([\w+-]*)\s*$/);
    if (fence) { if (codeLines === null) { flushParagraph(); flushList(); codeLines = []; codeLanguage = fence[1]; } else flushCode(); continue; }
    if (codeLines !== null) { codeLines.push(line); continue; }
    if (!line.trim()) { flushParagraph(); flushList(); continue; }
    if (/^\s*---+\s*$/.test(line)) { flushParagraph(); flushList(); output.push("<hr>"); continue; }
    const heading = line.match(/^\s*(#{1,4})\s+(.+?)\s*#*\s*$/);
    if (heading) { flushParagraph(); flushList(); const level = Math.min(heading[1].length, 3); output.push(`<h${level}>${inlineMarkdown(heading[2])}</h${level}>`); continue; }
    if (/^\s*>/.test(line)) { flushParagraph(); flushList(); output.push(`<blockquote>${inlineMarkdown(line.replace(/^\s*>\s?/, ""))}</blockquote>`); continue; }
    const unordered = line.match(/^\s*[-*+]\s+(?:\[([ xX])\]\s+)?(.+)$/);
    const ordered = line.match(/^\s*\d+[.)]\s+(.+)$/);
    if (unordered || ordered) { const nextType = unordered ? "ul" : "ol"; if (listType && listType !== nextType) flushList(); listType = nextType; listItems.push(unordered ? `${unordered[1] ? `<input type="checkbox" disabled ${unordered[1].toLowerCase() === "x" ? "checked" : ""}> ` : ""}${unordered[2]}` : ordered[1]); continue; }
    if (line.includes("|") && index + 1 < lines.length && isTableDivider(lines[index + 1])) { flushParagraph(); flushList(); const headers = tableRow(line); index += 1; const rows = []; while (index + 1 < lines.length && lines[index + 1].includes("|")) { index += 1; rows.push(tableRow(lines[index])); } output.push(`<div class="table-wrap"><table><thead><tr>${headers.map((cell) => `<th>${inlineMarkdown(cell)}</th>`).join("")}</tr></thead><tbody>${rows.map((row) => `<tr>${row.map((cell) => `<td>${inlineMarkdown(cell)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`); continue; }
    paragraph.push(line.trim());
  }
  flushCode(); flushParagraph(); flushList();
  return output.join("\n");
}

function renderLessonList(filter = "") {
  const query = filter.trim().toLowerCase();
  const visible = lessons.filter((lesson) => `${lesson.title} ${lesson.short} ${lesson.phase}`.toLowerCase().includes(query));
  $("#lesson-list").innerHTML = visible.length ? visible.map((lesson) => `<button class="lesson-item ${lesson.id === state.currentId ? "active" : ""} ${state.completed.has(lesson.id) ? "completed" : ""}" type="button" data-lesson="${lesson.id}"><span class="lesson-number">${lesson.number}</span><span class="lesson-name">${escapeHtml(lesson.title)}</span><span class="lesson-check" aria-label="อ่านแล้ว">✓</span></button>`).join("") : `<p class="sidebar-note">ไม่พบบทเรียนที่ค้นหา</p>`;
  $("#lesson-list").querySelectorAll("[data-lesson]").forEach((button) => button.addEventListener("click", () => openLesson(button.dataset.lesson)));
}

function updateProgress() {
  const percentage = Math.round((state.completed.size / lessons.length) * 100);
  $("#progress-bar").style.width = `${percentage}%`;
  $("#progress-label").textContent = `${percentage}%`;
  $("#progress-detail").textContent = percentage ? `อ่านแล้ว ${state.completed.size} จาก ${lessons.length} บท` : "เริ่มบทแรกได้เลย";
  $("#continue-learning").hidden = !localStorage.getItem("scraping-course-last");
}

async function getLesson(lesson) {
  if (state.cache.has(lesson.id)) return state.cache.get(lesson.id);
  const response = await fetch(`lessons/${lesson.id}.md`);
  if (!response.ok) throw new Error(`Lesson ${lesson.id} not found`);
  const markdown = await response.text();
  state.cache.set(lesson.id, markdown);
  return markdown;
}

function updateNavigation(index) {
  const previous = lessons[index - 1]; const next = lessons[index + 1];
  const previousButton = $("#previous-lesson"); const nextButton = $("#next-lesson");
  previousButton.disabled = !previous; nextButton.disabled = !next;
  $("#previous-title").textContent = previous ? previous.title : "ต้นทางของหลักสูตร";
  $("#next-title").textContent = next ? next.title : "จบหลักสูตร";
  previousButton.onclick = () => previous && openLesson(previous.id);
  nextButton.onclick = () => next && openLesson(next.id);
}

async function openLesson(id, updateUrl = true) {
  const lesson = lessonById(id) || lessons[0]; const index = lessons.indexOf(lesson);
  state.currentId = lesson.id;
  $("#main-content").classList.add("is-reading");
  localStorage.setItem("scraping-course-last", lesson.id);
  renderLessonList($("#lesson-search").value);
  $("#welcome-view").hidden = true; $("#error-view").hidden = true; $("#reader-view").hidden = false;
  $("#lesson-phase").textContent = `PHASE ${lesson.number} · ${lesson.phase.toUpperCase()}`;
  $("#lesson-position").textContent = `บทที่ ${index + 1} จาก ${lessons.length}`;
  $("#lesson-cover-number").textContent = lesson.number;
  $("#lesson-content").innerHTML = `<div class="loading-block"><span></span><span></span><span></span></div>`;
  $("#complete-label").textContent = state.completed.has(lesson.id) ? "อ่านแล้ว" : "ทำเครื่องหมายว่าอ่านแล้ว";
  $("#mark-complete").classList.toggle("completed", state.completed.has(lesson.id));
  updateNavigation(index); closeSidebar();
  if (updateUrl) history.pushState({}, "", `?lesson=${lesson.id}`);
  window.scrollTo({ top: 0, behavior: "smooth" });
  try { $("#lesson-content").innerHTML = markdownToHtml(await getLesson(lesson)); }
  catch { $("#reader-view").hidden = true; $("#error-view").hidden = false; }
}

function toggleComplete() {
  if (!state.currentId) return;
  if (state.completed.has(state.currentId)) state.completed.delete(state.currentId); else state.completed.add(state.currentId);
  saveCompleted(); updateProgress(); renderLessonList($("#lesson-search").value);
  const isComplete = state.completed.has(state.currentId);
  $("#complete-label").textContent = isComplete ? "อ่านแล้ว" : "ทำเครื่องหมายว่าอ่านแล้ว";
  $("#mark-complete").classList.toggle("completed", isComplete);
}

function closeSidebar() { $("#sidebar").classList.remove("open"); $("#mobile-overlay").hidden = true; $("#menu-toggle").setAttribute("aria-expanded", "false"); }
function toggleSidebar() { const open = $("#sidebar").classList.toggle("open"); $("#mobile-overlay").hidden = !open; $("#menu-toggle").setAttribute("aria-expanded", String(open)); }

function initTheme() {
  const saved = localStorage.getItem("scraping-course-theme"); const theme = saved || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  document.documentElement.dataset.theme = theme; $("#theme-toggle").innerHTML = `<span aria-hidden="true">${theme === "dark" ? "☀" : "☾"}</span>`; $("#theme-toggle").setAttribute("aria-label", theme === "dark" ? "เปิดโหมดสว่าง" : "เปิดโหมดกลางคืน");
}
function toggleTheme() { const theme = document.documentElement.dataset.theme === "dark" ? "light" : "dark"; localStorage.setItem("scraping-course-theme", theme); initTheme(); }

document.addEventListener("DOMContentLoaded", () => {
  renderLessonList(); updateProgress(); initTheme();
  const queryLesson = new URLSearchParams(location.search).get("lesson");
  if (queryLesson && lessonById(queryLesson)) openLesson(queryLesson, false);
  $("#start-learning").addEventListener("click", () => openLesson("00-course-roadmap"));
  $("#continue-learning").addEventListener("click", () => openLesson(localStorage.getItem("scraping-course-last") || "00-course-roadmap"));
  $("#mark-complete").addEventListener("click", toggleComplete); $("#theme-toggle").addEventListener("click", toggleTheme); $("#menu-toggle").addEventListener("click", toggleSidebar); $("#mobile-overlay").addEventListener("click", closeSidebar); $("#back-home").addEventListener("click", () => { history.pushState({}, "", "/"); $("#main-content").classList.remove("is-reading"); $("#error-view").hidden = true; $("#reader-view").hidden = true; $("#welcome-view").hidden = false; });
  $("#lesson-search").addEventListener("input", (event) => renderLessonList(event.target.value));
  document.addEventListener("keydown", (event) => { if (event.key === "/" && document.activeElement.tagName !== "INPUT") { event.preventDefault(); $("#lesson-search").focus(); } if (event.key === "Escape") closeSidebar(); });
  document.querySelectorAll("[data-lesson]").forEach((button) => button.addEventListener("click", () => openLesson(button.dataset.lesson)));
  window.addEventListener("popstate", () => { const id = new URLSearchParams(location.search).get("lesson"); if (id && lessonById(id)) openLesson(id, false); else { $("#main-content").classList.remove("is-reading"); $("#reader-view").hidden = true; $("#welcome-view").hidden = false; } });
});
