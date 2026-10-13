"""Chart builder pieces for build_medchart.py: markup, CSS and JS kept as plain
strings so the JS braces don't need f-string escaping."""

BUILDER_HTML = '''
  <section class="ps-sec mc-sec" id="builder" aria-labelledby="b-h">
    <div class="wrap">
      <div class="mc-panel ps-hide-print">
        <h2 class="ps-h2" id="b-h">Build your chart</h2>
        <p class="ps-sub">Choose how many medicines your pet takes on each schedule. The chart below changes as you go.</p>
        <div class="mc-counts" id="mc-counts"></div>
        <details class="mc-more" id="mc-more">
          <summary>Add names and times <span class="mc-opt">(optional)</span><span class="chev" aria-hidden="true">&#9662;</span></summary>
          <div class="mc-top">
            <label class="mc-f"><span>Pet's name</span><input type="text" id="mc-name" placeholder="e.g., Bella" autocomplete="off"></label>
            <label class="mc-f"><span>Week starting</span><input type="date" id="mc-week"></label>
          </div>
          <div id="mc-meds"></div>
          <p class="mc-hint">If you set a first dose time, the rest of the day's Due times are filled in for you. Or leave it blank and write them in.</p>
        </details>
        <div class="mc-tools">
          <button type="button" class="btn btn-primary btn-lg" id="mc-print">Print chart</button>
          <button type="button" class="linkbtn" id="mc-reset">Start over</button>
        </div>
        <p class="mc-hint" id="mc-pages-note">Prints landscape on US letter paper. What you type stays in this browser.</p>
      </div>
      <div class="mc-stage" id="mc-stage" aria-label="Chart preview"></div>
    </div>
  </section>'''

BUILDER_CSS = '''
  .mc-panel { max-width: 60rem; margin: 0 auto; background: var(--color-surface);
    border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: clamp(1rem, 4vw, 1.75rem); }
  .mc-panel .ps-h2 { font-size: clamp(1.4rem, 3.5vw, 1.9rem); }
  .mc-counts { display: grid; gap: .6rem; margin-top: 1.1rem; grid-template-columns: 1fr; }
  @media (min-width: 560px) { .mc-counts { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
  @media (min-width: 900px) { .mc-counts { grid-template-columns: repeat(5, minmax(0, 1fr)); } }
  .mc-count { display: flex; align-items: center; justify-content: space-between; gap: .6rem;
    padding: .7rem .8rem; border: 1px solid var(--color-border); border-radius: var(--radius);
    background: var(--color-surface-2); }
  @media (min-width: 900px) { .mc-count { flex-direction: column; align-items: stretch; text-align: center; } }
  .mc-count-l { display: flex; flex-direction: column; line-height: 1.25; }
  .mc-count-l b { font-weight: 600; }
  .mc-count-l small { color: var(--color-text-muted); font-size: .82rem; }
  .mc-step { display: flex; align-items: center; justify-content: center; gap: .35rem; }
  .mc-step button { width: 2.5rem; height: 2.5rem; border-radius: 50%; border: 1px solid var(--color-border-strong);
    background: var(--color-surface); color: var(--color-primary); font: inherit; font-size: 1.3rem; font-weight: 600;
    line-height: 1; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; }
  .mc-step button:hover:not(:disabled) { border-color: var(--color-primary); }
  .mc-step button:disabled { opacity: .35; cursor: default; }
  .mc-step button:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }
  .mc-step output { min-width: 1.6rem; text-align: center; font-weight: 600; font-size: 1.15rem; font-variant-numeric: tabular-nums; }
  .mc-more { margin-top: 1rem; border-top: 1px solid var(--color-border); }
  .mc-more summary { list-style: none; cursor: pointer; padding: .85rem 0 .3rem; font-weight: 600; color: var(--color-primary);
    display: flex; align-items: center; gap: .4rem; }
  .mc-more summary::-webkit-details-marker { display: none; }
  .mc-more .chev { margin-left: auto; transition: transform .2s; }
  .mc-more[open] .chev { transform: rotate(180deg); }
  .mc-opt { font-weight: 400; color: var(--color-text-muted); }
  .mc-top { display: grid; gap: 0 1rem; grid-template-columns: 1fr; margin-top: .5rem; }
  @media (min-width: 560px) { .mc-top { grid-template-columns: 1fr 1fr; } }
  .mc-f { display: block; margin: 0 0 .8rem; min-width: 0; }
  .mc-f span { display: block; font-size: .85rem; font-weight: 600; color: var(--color-text-muted); margin-bottom: .2rem; }
  .mc-f input { width: 100%; box-sizing: border-box; font: inherit; font-size: 1rem; color: var(--color-text);
    background: transparent; border: 0; border-bottom: 1px solid var(--color-border); border-radius: 0; padding: .35rem 0; min-height: 2.2rem; }
  .mc-f input:focus { outline: none; border-bottom-color: var(--color-primary); }
  .mc-f ::placeholder { color: var(--color-text-muted); opacity: .55; }
  .mc-med { display: grid; gap: 0 1rem; grid-template-columns: 1fr; padding-top: .7rem; border-top: 1px dashed var(--color-border); }
  .mc-med h3 { grid-column: 1 / -1; margin: 0 0 .3rem; font-family: inherit; font-size: .92rem; font-weight: 600; color: var(--color-primary); }
  @media (min-width: 560px) { .mc-med { grid-template-columns: minmax(0, 2fr) minmax(0, 1fr); } }
  .mc-hint { margin: .5rem 0 0; font-size: .88rem; color: var(--color-text-muted); }
  .mc-tools { display: flex; flex-wrap: wrap; align-items: center; gap: .6rem 1.4rem; margin-top: 1.2rem; }
  .linkbtn { display: inline-flex; align-items: center; background: none; border: 0; padding: .4rem 0; font: inherit; font-weight: 600;
    color: var(--color-primary); cursor: pointer; text-decoration: underline; text-underline-offset: 3px; }
  .mc-empty { max-width: 60rem; margin: 1.2rem auto 0; padding: 2rem 1rem; text-align: center; color: var(--color-text-muted);
    border: 1px dashed var(--color-border-strong); border-radius: var(--radius-lg); }

  /* The paper: drawn at exactly 11in x 8.5in (1056 x 816 px), scaled down to fit on screen. */
  .mc-stage { max-width: 60rem; margin: 1.4rem auto 0; }
  .mc-fit { position: relative; margin: 0 auto 1.1rem; }
  .mc-paper { position: absolute; top: 0; left: 0; width: 1056px; height: 816px; transform-origin: 0 0;
    box-sizing: border-box; padding: 34px 34px 26px; background: #fff; color: #2b2b2b;
    font-family: Lato, "General Sans", Arial, sans-serif; border: 1px solid var(--color-border);
    border-radius: 6px; box-shadow: 0 6px 24px rgba(0,0,0,.08); display: flex; flex-direction: column; overflow: hidden; }
  .mc-head { display: flex; justify-content: space-between; align-items: flex-start; gap: 24px; }
  .mc-title { margin: 0; font-size: 28px; font-weight: 700; color: #2b2723; letter-spacing: -.01em; line-height: 1.1; font-family: inherit; }
  .mc-subt { margin: 6px 0 0; font-size: 13.5px; color: #666; }
  .mc-who { width: 350px; flex: 0 0 auto; font-size: 15px; color: #666; }
  .mc-who div { display: flex; align-items: flex-end; gap: 8px; height: 29px; }
  .mc-who span.v { flex: 1; border-bottom: 1px solid #bbb; color: #222; font-weight: 600; padding: 0 2px 2px; min-height: 18px;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .mc-tbl { width: 100%; border-collapse: collapse; table-layout: fixed; margin-top: 18px; font-size: 12.5px; }
  .mc-tbl th { background: #2b2723; color: #fff; font-weight: 700; font-size: 14px; letter-spacing: .02em; height: 33px; padding: 0 8px;
    border-bottom: 3px solid #7b9a9e; text-align: center; line-height: 1.05; }
  .mc-tbl th:first-child { text-align: left; padding-left: 12px; }
  .mc-tbl th small { display: block; font-weight: 400; font-size: 10.5px; letter-spacing: 0; opacity: .8; margin-top: 2px; }
  .mc-tbl td { border: 1px solid #cfd3d3; vertical-align: top; height: var(--rh, 72px); padding: 0; position: relative; }
  .mc-tbl tr.s-first td { border-top: 3px solid #7b9a9e; }
  .mc-tbl tbody tr:first-child td { border-top: 0; }
  .mc-tbl tr.s-last td { border-bottom: 3px solid #7b9a9e; }
  .mc-tbl tr.alt td { background: #dcebec; }
  .mc-tbl td.med { vertical-align: middle; padding: 6px 12px; }
  .mc-med-n { border-bottom: 1px solid #aab; min-height: 16px; padding-bottom: 3px; font-size: 13px; font-weight: 600; color: #222;
    line-height: 1.2; overflow-wrap: anywhere; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
  .mc-med-n:empty { margin-top: 20px; }
  .mc-med-s { display: block; margin-top: 6px; color: #12676e; font-size: 13.5px; font-weight: 500; }
  .mc-tbl td.dose { vertical-align: middle; text-align: center; font-size: 13.5px; color: #555; }
  .mc-cell { position: absolute; inset: 0; padding: var(--pt, 14px) 7px 0 18px; }
  .mc-ln { display: flex; align-items: flex-end; gap: 6px; height: 25px; color: #777; }
  .mc-ln i { flex: 1; min-width: 0; font-style: normal; border-bottom: 1px solid #aaa; height: 15px; margin-left: 4px; font-size: 11.5px; color: #222;
    font-weight: 600; text-align: center; line-height: 14px; white-space: nowrap; letter-spacing: -.01em; }
  .mc-ln.d i { margin-left: 11px; }
  .mc-ar { position: absolute; color: #3f8f96; }
  .mc-ar.r { right: 6px; bottom: 3px; width: 34px; height: 8px; }
  .mc-ar.dn { left: 6px; bottom: -12px; width: 8px; height: 22px; z-index: 1; }
  .mc-foot { margin-top: auto; padding-top: 10px; display: flex; justify-content: space-between; align-items: flex-end; gap: 20px; font-size: 11.5px; color: #666; }
  .mc-foot p { margin: 0; line-height: 1.45; }
  .mc-src { margin-top: 4px !important; color: #4a4a4a; font-weight: 600; }
  .mc-plug { flex: 0 0 auto; display: flex; align-items: center; gap: 12px; padding: 8px 14px 8px 8px;
    border: 1.5px solid #7b9a9e; border-radius: 8px; background: #f1f7f7; color: #444; max-width: 560px; }
  .mc-plug img { display: block; width: 66px; height: 66px; background: #fff; border-radius: 3px; }
  .mc-plug-h { font-weight: 700; font-size: 13px; color: #12676e; }
  .mc-plug-u { font-weight: 600; color: #2b2723; }

  @media print {
    @page { size: letter landscape; margin: 0; }
    body { background: #fff !important; }
    body.ps-page { background-image: none !important; }
    .site-head, .site-foot, .ps-hide-print, .skip { display: none !important; }
    .ps-sec.mc-sec { padding: 0 !important; background: none !important; }
    .mc-sec .wrap { max-width: none; padding: 0; margin: 0; }
    .mc-stage { max-width: none; margin: 0; }
    .mc-fit { width: auto !important; height: auto !important; margin: 0; break-after: page; page-break-after: always; }
    .mc-fit:last-child { break-after: auto; page-break-after: auto; }
    .mc-paper { position: relative; transform: none !important; border: 0; border-radius: 0; box-shadow: none;
      -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  }
'''

BUILDER_JS = r'''
<script>
(function () {
  var KEY = 'ct-medchart-v1';
  var SCHED = [
    { h: 24, label: 'Every 24 hours', note: 'Once a day' },
    { h: 12, label: 'Every 12 hours', note: '2 doses a day' },
    { h: 8, label: 'Every 8 hours', note: '3 doses a day' },
    { h: 6, label: 'Every 6 hours', note: '4 doses a day' },
    { h: 4, label: 'Every 4 hours', note: '6 doses a day' }
  ];
  var MAX = 6, ROWS_PER_PAGE = 9;
  var DAYS = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
  var MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  var DEF = { counts: { 24: 2, 12: 2, 8: 0, 6: 0, 4: 0 }, meds: {}, name: '', week: '' };
  var st;
  try { st = JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) { st = null; }
  if (!st || !st.counts) st = JSON.parse(JSON.stringify(DEF));
  st.meds = st.meds || {};
  function save() { try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (e) {} }
  function esc(s) { return String(s || '').replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  var countsEl = document.getElementById('mc-counts');
  var medsEl = document.getElementById('mc-meds');
  var stage = document.getElementById('mc-stage');
  var nameIn = document.getElementById('mc-name');
  var weekIn = document.getElementById('mc-week');
  var printBtn = document.getElementById('mc-print');
  var note = document.getElementById('mc-pages-note');

  function sections() {
    var out = [];
    SCHED.forEach(function (s) {
      for (var i = 0; i < (st.counts[s.h] || 0); i++) out.push({ s: s, k: s.h + '-' + i, n: 24 / s.h });
    });
    return out;
  }

  function renderCounts() {
    countsEl.innerHTML = SCHED.map(function (s) {
      var c = st.counts[s.h] || 0;
      return '<div class="mc-count"><span class="mc-count-l"><b>' + s.label + '</b><small>' + s.note + '</small></span>' +
        '<span class="mc-step" role="group" aria-label="' + s.label + ' medicines">' +
        '<button type="button" data-h="' + s.h + '" data-d="-1" aria-label="One fewer ' + s.label.toLowerCase() + ' medicine"' + (c <= 0 ? ' disabled' : '') + '>&minus;</button>' +
        '<output aria-live="polite">' + c + '</output>' +
        '<button type="button" data-h="' + s.h + '" data-d="1" aria-label="One more ' + s.label.toLowerCase() + ' medicine"' + (c >= MAX ? ' disabled' : '') + '>+</button>' +
        '</span></div>';
    }).join('');
  }
  countsEl.addEventListener('click', function (e) {
    var b = e.target.closest('button[data-h]'); if (!b) return;
    var h = b.dataset.h, c = (st.counts[h] || 0) + (+b.dataset.d);
    st.counts[h] = Math.max(0, Math.min(MAX, c)); save();
    renderCounts(); renderMeds(); renderPages();
    var again = countsEl.querySelector('button[data-h="' + h + '"][data-d="' + b.dataset.d + '"]');
    if (again && !again.disabled) again.focus();
    else { var other = countsEl.querySelector('button[data-h="' + h + '"]:not(:disabled)'); if (other) other.focus(); }
  });

  function renderMeds() {
    var counter = {};
    medsEl.innerHTML = sections().map(function (x) {
      counter[x.s.h] = (counter[x.s.h] || 0) + 1;
      var m = st.meds[x.k] || {};
      return '<div class="mc-med"><h3>' + x.s.label + ' &middot; medicine ' + counter[x.s.h] + '</h3>' +
        '<label class="mc-f"><span>Medicine and dose</span><input type="text" data-k="' + x.k + '" data-f="name" maxlength="60" value="' + esc(m.name) + '" placeholder="e.g., Amoxicillin 250 mg, 1 tablet" autocomplete="off"></label>' +
        '<label class="mc-f"><span>First dose of the day</span><input type="time" data-k="' + x.k + '" data-f="first" value="' + esc(m.first) + '"></label></div>';
    }).join('');
  }
  medsEl.addEventListener('input', function (e) {
    var t = e.target; if (!t.dataset.k) return;
    var m = st.meds[t.dataset.k] = st.meds[t.dataset.k] || {};
    m[t.dataset.f] = t.value; save(); renderPages();
  });
  nameIn.addEventListener('input', function () { st.name = nameIn.value; save(); renderPages(); });
  weekIn.addEventListener('input', function () { st.week = weekIn.value; save(); renderPages(); });

  function fmt(mins) {
    mins = ((mins % 1440) + 1440) % 1440;
    var h = Math.floor(mins / 60), m = mins % 60, ap = h < 12 ? 'AM' : 'PM';
    h = h % 12 || 12;
    return h + ':' + (m < 10 ? '0' : '') + m + ' ' + ap;
  }
  function weekDays() {
    if (!st.week) return DAYS.map(function (d) { return { d: d, sub: '' }; });
    var p = st.week.split('-'), base = new Date(+p[0], +p[1] - 1, +p[2]);
    var out = [];
    for (var i = 0; i < 7; i++) {
      var dt = new Date(base.getFullYear(), base.getMonth(), base.getDate() + i);
      out.push({ d: DAYS[dt.getDay()], sub: MON[dt.getMonth()] + ' ' + dt.getDate() });
    }
    return out;
  }
  function weekLabel() {
    if (!st.week) return '';
    var p = st.week.split('-'), a = new Date(+p[0], +p[1] - 1, +p[2]), b = new Date(a.getFullYear(), a.getMonth(), a.getDate() + 6);
    return MON[a.getMonth()] + ' ' + a.getDate() + ' \u2013 ' + MON[b.getMonth()] + ' ' + b.getDate() + ', ' + b.getFullYear();
  }

  var AR_R = '<svg class="mc-ar r" viewBox="0 0 34 8" aria-hidden="true"><path d="M0 4h31M27 1l4 3-4 3" fill="none" stroke="currentColor" stroke-width="1.2"/></svg>';
  var AR_D = '<svg class="mc-ar dn" viewBox="0 0 8 22" aria-hidden="true"><path d="M4 0v19M1 15l3 4 3-4" fill="none" stroke="currentColor" stroke-width="1.2"/></svg>';

  function sectionRows(x, alt, days) {
    var m = st.meds[x.k] || {}, rows = '';
    var first = null;
    if (m.first) { var t = m.first.split(':'); first = (+t[0]) * 60 + (+t[1]); }
    for (var i = 0; i < x.n; i++) {
      var cls = [alt ? 'alt' : '', i === 0 ? 's-first' : '', i === x.n - 1 ? 's-last' : ''].join(' ').trim();
      rows += '<tr class="' + cls + '">';
      if (i === 0) rows += '<td class="med" rowspan="' + x.n + '"><div class="mc-med-n">' + esc(m.name) + '</div><span class="mc-med-s">' + x.s.label + '</span></td>';
      rows += '<td class="dose">' + (i + 1) + ' of ' + x.n + '</td>';
      var due = first === null ? '' : fmt(first + i * x.s.h * 60);
      for (var d = 0; d < 7; d++) {
        var ar = i < x.n - 1 ? AR_D : (d < 6 ? AR_R : '');
        rows += '<td><div class="mc-cell"><div class="mc-ln d">Due<i>' + due + '</i></div><div class="mc-ln">Taken<i></i></div>' + ar + '</div></td>';
      }
      rows += '</tr>';
    }
    return rows;
  }

  function renderPages() {
    var secs = sections();
    printBtn.disabled = !secs.length;
    if (!secs.length) {
      stage.innerHTML = '<p class="mc-empty">Add at least one medicine above to see your chart.</p>';
      note.textContent = 'Prints landscape on US letter paper. What you type stays in this browser.';
      return;
    }
    var pages = [], cur = [], rows = 0;
    secs.forEach(function (x, idx) {
      x.alt = idx % 2 === 1;
      if (cur.length && rows + x.n > ROWS_PER_PAGE) { pages.push(cur); cur = []; rows = 0; }
      cur.push(x); rows += x.n;
    });
    pages.push(cur);
    var days = weekDays(), wl = weekLabel();
    var head = '<tr><th style="width:150px">MEDICINE</th><th style="width:62px">DOSE</th>' +
      days.map(function (d) { return '<th>' + d.d + (d.sub ? '<small>' + d.sub + '</small>' : '') + '</th>'; }).join('') + '</tr>';
    stage.innerHTML = pages.map(function (pg, pi) {
      return '<div class="mc-fit"><div class="mc-paper">' +
        '<div class="mc-head"><div><p class="mc-title">Weekly Medication Chart</p>' +
        '<p class="mc-subt">Write the medicine name, the time each dose is due, and the time it was actually taken.</p></div>' +
        '<div class="mc-who"><div>Name:<span class="v">' + esc(st.name) + '</span></div><div>Week of:<span class="v">' + esc(wl) + '</span></div></div></div>' +
        '<table class="mc-tbl"><thead>' + head + '</thead><tbody>' +
        pg.map(function (x) { return sectionRows(x, x.alt, days); }).join('') +
        '</tbody></table>' +
        '<div class="mc-foot"><div class="mc-legend"><p>&ldquo;Due&rdquo; = scheduled time. &nbsp; &ldquo;Taken&rdquo; = actual time given.</p>' +
        '<p>Arrows point to the next box to fill: down the day, then across to the next day.</p>' +
        '<p class="mc-src">' + (pages.length > 1 ? 'Page ' + (pi + 1) + ' of ' + pages.length + ' &middot; ' : '') + 'Free chart from cleartrackapps.com/pet-medication-chart</p></div>' +
        '<div class="mc-plug"><img src="qr-pawfolio.svg" width="66" height="66" alt="">' +
        '<div><p class="mc-plug-h">Get free dose reminders on your phone with Pawfolio Free.</p>' +
        '<p>Using a sitter? Pawfolio Complete shares dose times and shows who gave each one.</p>' +
        '<p class="mc-plug-u">Scan the code or visit cleartrackapps.com/pawfolio</p></div></div></div>' +
        '</div></div>';
    }).join('');
    sizeRows();
    note.textContent = (pages.length > 1 ? 'Your chart is ' + pages.length + ' pages. ' : '') +
      'Prints landscape on US letter paper. What you type stays in this browser.';
    fit();
  }

  // Rows fill the space between the table header and the footer, up to 72px each.
  function sizeRows() {
    stage.querySelectorAll('.mc-paper').forEach(function (paper) {
      var tbl = paper.querySelector('.mc-tbl'), foot = paper.querySelector('.mc-foot');
      var n = paper.querySelectorAll('tbody tr').length;
      var head = tbl.offsetTop + paper.querySelector('thead').offsetHeight;
      var avail = paper.clientHeight - 26 - foot.offsetHeight - 14 - head - n * 1.5;
      var rh = Math.max(52, Math.min(72, Math.floor(avail / n)));
      paper.style.setProperty('--rh', rh + 'px');
      paper.style.setProperty('--pt', Math.max(4, Math.round((rh - 50) / 2) + 3) + 'px');
    });
  }

  function fit() {
    var w = stage.clientWidth || 1056, s = Math.min(1, w / 1056);
    stage.querySelectorAll('.mc-fit').forEach(function (f) {
      f.style.width = (1056 * s) + 'px'; f.style.height = (816 * s) + 'px';
      f.firstChild.style.transform = 'scale(' + s + ')';
    });
  }
  window.addEventListener('resize', fit);

  printBtn.addEventListener('click', function () { window.print(); });
  document.getElementById('mc-reset').addEventListener('click', function () {
    if (!confirm('Clear your chart and start over?')) return;
    st = JSON.parse(JSON.stringify(DEF)); try { localStorage.removeItem(KEY); } catch (e) {}
    nameIn.value = ''; weekIn.value = ''; renderCounts(); renderMeds(); renderPages();
  });

  nameIn.value = st.name || ''; weekIn.value = st.week || '';
  if (st.name || st.week || Object.keys(st.meds).some(function (k) { var m = st.meds[k]; return m && (m.name || m.first); }))
    document.getElementById('mc-more').open = true;
  renderCounts(); renderMeds(); renderPages();
})();
</script>'''
