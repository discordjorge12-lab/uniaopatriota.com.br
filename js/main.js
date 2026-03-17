// =====================
// FOCO & ROTINA — main.js
// =====================

// Article index for search
const articles = [
  { title: "Como criar uma rotina matinal produtiva em 7 passos", url: "artigos/rotina-matinal.html", cat: "Produtividade" },
  { title: "Os melhores aplicativos de organização pessoal", url: "artigos/melhores-aplicativos.html", cat: "Ferramentas" },
  { title: "Método Pomodoro: o que é e como usar no dia a dia", url: "artigos/metodo-pomodoro.html", cat: "Produtividade" },
  { title: "Como organizar as finanças pessoais do zero", url: "artigos/financas-pessoais.html", cat: "Organização" },
  { title: "10 hábitos de pessoas altamente organizadas", url: "artigos/habitos-organizadas.html", cat: "Organização" },
  { title: "Como parar de procrastinar: causas e soluções reais", url: "artigos/parar-procrastinar.html", cat: "Produtividade" },
  { title: "Como organizar a casa em um fim de semana", url: "artigos/organizar-casa.html", cat: "Organização" },
  { title: "Como criar um planejamento semanal que você realmente segue", url: "artigos/planejamento-semanal.html", cat: "Produtividade" },
  { title: "Notion para iniciantes: como começar a usar do zero", url: "artigos/notion-iniciantes.html", cat: "Ferramentas" },
  { title: "Como se concentrar melhor no trabalho home office", url: "artigos/concentracao-home-office.html", cat: "Produtividade" },
  { title: "O que é minimalismo e como ele pode transformar sua vida", url: "artigos/minimalismo.html", cat: "Organização" },
  { title: "Como montar uma lista de tarefas que funciona de verdade", url: "artigos/lista-tarefas.html", cat: "Produtividade" },
  { title: "5 livros sobre produtividade que mudaram minha rotina", url: "artigos/livros-produtividade.html", cat: "Livros" },
  { title: "Como organizar e-mails e nunca mais perder tempo", url: "artigos/organizar-emails.html", cat: "Organização" },
  { title: "Como definir metas que você vai alcançar: método SMART", url: "artigos/metas-smart.html", cat: "Produtividade" },
];

// Fix relative URLs for article pages
function fixArticleUrls() {
  const isArticlePage = window.location.pathname.includes('/artigos/');
  if (!isArticlePage) return;
  articles.forEach(a => {
    a.url = '../' + a.url;
  });
}

// Hamburger menu
function initHamburger() {
  const btn = document.querySelector('.hamburger');
  const nav = document.querySelector('.site-nav');
  if (!btn || !nav) return;
  btn.addEventListener('click', () => {
    btn.classList.toggle('open');
    nav.classList.toggle('open');
  });
}

// Search
function initSearch() {
  const input = document.getElementById('search-input');
  const results = document.getElementById('search-results');
  if (!input || !results) return;

  const isArticlePage = window.location.pathname.includes('/artigos/');
  const prefix = isArticlePage ? '../' : '';

  input.addEventListener('input', () => {
    const q = input.value.trim().toLowerCase();
    if (q.length < 2) { results.innerHTML = ''; results.classList.remove('active'); return; }

    const matches = articles.filter(a => a.title.toLowerCase().includes(q));
    if (matches.length === 0) {
      results.innerHTML = '<p class="no-results">Nenhum resultado encontrado.</p>';
    } else {
      results.innerHTML = matches.slice(0, 5).map(a =>
        `<a href="${prefix}${a.url}">${a.title} <small style="color:var(--muted);margin-left:6px;">${a.cat}</small></a>`
      ).join('');
    }
    results.classList.add('active');
  });

  document.addEventListener('click', (e) => {
    if (!input.contains(e.target) && !results.contains(e.target)) {
      results.classList.remove('active');
    }
  });
}

// Cookie banner
function initCookies() {
  const banner = document.getElementById('cookie-banner');
  const btn = document.getElementById('cookie-accept');
  if (!banner || !btn) return;

  if (!localStorage.getItem('cookies-accepted')) {
    setTimeout(() => banner.classList.add('show'), 800);
  }

  btn.addEventListener('click', () => {
    localStorage.setItem('cookies-accepted', '1');
    banner.classList.remove('show');
  });
}

// Contact form
function initContactForm() {
  const form = document.getElementById('contact-form');
  if (!form) return;
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const btn = form.querySelector('.form-submit');
    btn.textContent = 'Mensagem enviada! ✓';
    btn.style.background = '#2E7D32';
    btn.style.color = '#fff';
    btn.disabled = true;
    form.reset();
  });
}

// Init all
document.addEventListener('DOMContentLoaded', () => {
  fixArticleUrls();
  initHamburger();
  initSearch();
  initCookies();
  initContactForm();
});
