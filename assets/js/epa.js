/* EPA Bienestar IA — comportamiento compartido del sitio.
   Tema, navegación móvil, reveal on scroll, trazados del hero,
   y widget de estado. Cargar con defer en todas las páginas. */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ── Tema claro / oscuro ────────────────────────────────
     En producción, descomentá las líneas localStorage para
     que la preferencia persista entre visitas.            */
  var theme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  // try { theme = localStorage.getItem("epa-theme") || theme; } catch (e) {}
  document.documentElement.setAttribute("data-theme", theme);

  document.getElementById("tgl").addEventListener("click", function () {
    theme = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", theme);
    // try { localStorage.setItem("epa-theme", theme); } catch (e) {}
    drawTraces();
  });

  /* ── Menú móvil ─────────────────────────────────────── */
  var burger = document.getElementById("burger"), nav = document.getElementById("nav");
  burger.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    burger.setAttribute("aria-expanded", String(open));
  });
  nav.addEventListener("click", function (e) {
    if (e.target.tagName === "A") { nav.classList.remove("open"); burger.setAttribute("aria-expanded", "false"); }
  });

  /* ── SIGNATURE: trazados de presión sistólica ──────────
     Dos series reales de 28 días. Idéntica media (128 mmHg),
     desvío estándar radicalmente distinto. Es la tesis del
     Índice EPA dibujada: LE8 no distingue estas pacientes. */
  var A = [126,133,128,130,124,125,128,126,135,123,139,122,134,123,
           138,129,130,132,124,122,116,135,124,124,128,140,117,129];
  var B = [124,163,125,141,172,122,128,121,116,145,130,136,102,142,
           120, 98,120,104,163,102,139,114,118,110,156,113,122,138];
  /* Verificado: media(A) = media(B) = 128,00 mmHg exactos.
     SD(A) = 6,14 · SD(B) = 19,44 */

  var W = 620, H = 270, PADL = 40, PADR = 16, PADT = 18, PADB = 30;
  var LO = 92, HI = 178;

  function xAt(i, n) { return PADL + (i * (W - PADL - PADR)) / (n - 1); }
  function yAt(v)    { return PADT + ((HI - v) * (H - PADT - PADB)) / (HI - LO); }
  function pathOf(s) {
    return s.map(function (v, i) { return (i ? "L" : "M") + xAt(i, s.length).toFixed(1) + " " + yAt(v).toFixed(1); }).join(" ");
  }

  function drawTraces() {
    var svg = document.getElementById("traces");
    if (!svg) return;
    var g = "", t;

    for (t = 100; t <= 170; t += 20) {
      g += '<line class="grid-l" x1="' + PADL + '" y1="' + yAt(t).toFixed(1) + '" x2="' + (W - PADR) + '" y2="' + yAt(t).toFixed(1) + '"/>';
      g += '<text class="ax-t" x="' + (PADL - 9) + '" y="' + (yAt(t) + 3.5).toFixed(1) + '" text-anchor="end">' + t + "</text>";
    }

    g += '<line class="mean-l" x1="' + PADL + '" y1="' + yAt(128).toFixed(1) + '" x2="' + (W - PADR) + '" y2="' + yAt(128).toFixed(1) + '"/>';

    g += '<text class="ax-t" x="' + PADL + '" y="' + (H - 8) + '">día 1</text>';
    g += '<text class="ax-t" x="' + (W / 2) + '" y="' + (H - 8) + '" text-anchor="middle" style="letter-spacing:.09em">media compartida · 128 mm Hg</text>';
    g += '<text class="ax-t" x="' + (W - PADR) + '" y="' + (H - 8) + '" text-anchor="end">día 28</text>';

    g += '<path id="trB" class="tr-path tr-vary" d="' + pathOf(B) + '"/>';
    g += '<path id="trA" class="tr-path tr-calm" d="' + pathOf(A) + '"/>';

    svg.innerHTML = g;

    if (reduce) return;
    ["trA", "trB"].forEach(function (id, k) {
      var p = document.getElementById(id), len = p.getTotalLength();
      p.style.strokeDasharray = len;
      p.style.strokeDashoffset = len;
      p.style.transition = "stroke-dashoffset 1.7s cubic-bezier(.32,.9,.3,1) " + (k * 0.42 + 0.25) + "s";
      requestAnimationFrame(function () { requestAnimationFrame(function () { p.style.strokeDashoffset = 0; }); });
    });
  }
  drawTraces();

  /* ── Reveal on scroll + barras de determinantes ──────── */
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("in");
        if (en.target.id === "det") {
          en.target.querySelectorAll(".det-fill").forEach(function (f, i) {
            setTimeout(function () { f.style.width = f.dataset.w + "%"; }, reduce ? 0 : i * 110);
          });
        }
        io.unobserve(en.target);
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    document.querySelectorAll(".rv").forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll(".rv").forEach(function (el) { el.classList.add("in"); });
    document.querySelectorAll(".det-fill").forEach(function (f) { f.style.width = f.dataset.w + "%"; });
  }

  /* ── Estado de sistemas (UptimeRobot) ──────────────────
     ATENCIÓN: la API key queda expuesta del lado cliente.
     Es de solo lectura y acotada a un monitor, pero conviene
     moverla a una Lambda que haga de proxy.               */
  (function () {
    var dot = document.getElementById("status-dot"), tx = document.getElementById("status-text");
    if (!dot) return;
    fetch("https://api.uptimerobot.com/v2/getMonitors", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: "api_key=ur3030818-0ff5dfae6f8bb4e68ef8bbb1&format=json"
    })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        var m = d.monitors && d.monitors[0];
        if (m && m.status === 2) {
          dot.style.background = "#22C55E"; dot.style.boxShadow = "0 0 8px #22C55E";
          tx.textContent = "Sistemas operativos";
        } else {
          dot.style.background = "#F59E0B"; dot.style.boxShadow = "0 0 8px #F59E0B";
          tx.textContent = "Mantenimiento en curso";
        }
      })
      .catch(function () { tx.textContent = "Estado no disponible"; });
  })();
})();
