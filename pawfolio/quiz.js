/* Pawfolio — "Could you answer these 6 questions about your pet?"
 * ---------------------------------------------------------------------------
 * The ad promises "Keep score. One point each." This delivers that promise on
 * the landing page instead of handing the visitor a sales pitch. The static
 * list in index.html (#q-static) stays in the markup as the no-JS fallback and
 * is only hidden once this script has successfully rendered.
 * --------------------------------------------------------------------------- */

(function () {
  'use strict';

  var mount = document.getElementById('q-quiz');
  var staticList = document.getElementById('q-static');
  var sub = document.getElementById('q-sub');
  if (!mount || !staticList) return; // markup missing — leave the page untouched

  var DEMO = 'https://cleartrackapps.com/pet-care-planner-demo/';
  var BUY = 'https://cleartrackapps.com/go/pawfolio/';

  // Kept in step with the six .q-item entries in index.html.
  var QUESTIONS = [
    { ask: 'When was your pet&rsquo;s last vaccination?',
      where: 'Every due date, with the next one already worked out.' },
    { ask: 'Which medication, and what dose?',
      where: 'Current medications and supplements, per pet.' },
    { ask: 'What was the weight at the last visit?',
      where: 'A weight history you can actually see a trend in.' },
    { ask: 'What was the diagnosis last time?',
      where: 'Every visit, reason, diagnosis and what it cost.' },
    { ask: 'When was the last flea and tick dose?',
      where: 'Logged with the rest, not in your head.' },
    { ask: 'What is the microchip number?',
      where: 'On the profile, ready to read out.' }
  ];

  var VERDICTS = [
    { min: 6, title: 'Okay, show-off. \uD83D\uDE02',
      note: 'You genuinely know your pet&rsquo;s records. The real question is whether ' +
            'your pet sitter would &mdash; or whether you&rsquo;d still recall all six at ' +
            '2am in an emergency room with a scared animal on the table.' },
    { min: 5, title: 'That&rsquo;s better than almost everyone.',
      note: 'One gap is one phone call to the vet you shouldn&rsquo;t have to make. ' +
            'Pawfolio keeps all six on your phone so the gap never opens up.' },
    { min: 3, title: 'That&rsquo;s a strong score.',
      note: 'The ones you missed are the ones that live in a folder, a photo roll, ' +
            'or a vet&rsquo;s system you can&rsquo;t get into on a Sunday.' },
    { min: 1, title: 'Most people land right about here.',
      note: 'Two out of six is the normal result. It isn&rsquo;t a memory problem &mdash; ' +
            'this information was never kept anywhere you could reach it.' },
    { min: 0, title: 'You&rsquo;re in very good company.',
      note: 'Almost nobody has these to hand. That gap is the entire reason ' +
            'Pawfolio exists.' }
  ];

  var answers = [];
  var started = false;

  function track(name, params) {
    if (typeof window.ctTrack === 'function') window.ctTrack(name, params);
  }

  function dots(current) {
    var out = '';
    for (var i = 0; i < QUESTIONS.length; i++) {
      var cls = 'qz-dot';
      if (i < current) cls += ' is-done';
      else if (i === current) cls += ' is-now';
      out += '<span class="' + cls + '"></span>';
    }
    return '<div class="qz-prog" aria-hidden="true">' + out + '</div>';
  }

  function renderQuestion(i) {
    var q = QUESTIONS[i];
    mount.innerHTML =
      '<div class="qz-card qz-fade">' +
        dots(i) +
        '<p class="qz-step">Question ' + (i + 1) + ' of ' + QUESTIONS.length + '</p>' +
        '<h3 class="qz-q" id="qz-current" tabindex="-1">' + q.ask + '</h3>' +
        '<div class="qz-btns">' +
          '<button type="button" class="btn btn-primary btn-lg" data-yes="1">I know it</button>' +
          '<button type="button" class="btn btn-ghost btn-lg" data-yes="0">No idea</button>' +
        '</div>' +
        (i === 0
          ? '<button type="button" class="qz-skip" data-skip="1">Skip the quiz &mdash; just show me the app</button>'
          : '') +
      '</div>';

    // Move focus to the new question so keyboard and screen-reader users follow along.
    var h = document.getElementById('qz-current');
    if (h && started) h.focus({ preventScroll: true });
  }

  function verdictFor(score) {
    for (var i = 0; i < VERDICTS.length; i++) {
      if (score >= VERDICTS[i].min) return VERDICTS[i];
    }
    return VERDICTS[VERDICTS.length - 1];
  }

  function renderResult() {
    var score = answers.reduce(function (a, b) { return a + b; }, 0);
    var v = verdictFor(score);

    var rows = QUESTIONS.map(function (q, i) {
      var got = answers[i] === 1;
      return '<li>' +
        '<span class="qz-mark" aria-hidden="true">' + (got ? '\u2713' : '\u2014') + '</span>' +
        '<span><b>' + q.ask + '</b><br>' +
        '<span class="qz-where">' + q.where + '</span></span>' +
      '</li>';
    }).join('');

    mount.innerHTML =
      '<div class="qz-card qz-fade">' +
        '<p class="qz-score" id="qz-current" tabindex="-1">' + score + '/' + QUESTIONS.length +
          '<small>' + (score === 1 ? 'one point' : score + ' points') + ' out of six</small></p>' +
        '<p class="qz-verdict">' + v.title + '</p>' +
        '<p class="qz-note">' + v.note + '</p>' +
        '<ul class="qz-rev">' + rows + '</ul>' +
        '<div class="qz-cta">' +
          '<div class="pf-actions">' +
            '<a class="btn btn-primary btn-lg" href="' + DEMO + '" data-qz-cta="demo">Try the free demo</a>' +
            '<a class="btn btn-ghost btn-lg" href="' + BUY + '" data-qz-cta="buy">Buy now &mdash; $14.99</a>' +
          '</div>' +
          '<p class="pf-micro">The demo is the full app with a sample pet loaded &mdash; but it ' +
            'forgets when you close it. The paid version remembers forever.</p>' +
        '</div>' +
        '<button type="button" class="qz-again" data-again="1">Start over</button>' +
      '</div>';

    var h = document.getElementById('qz-current');
    if (h) h.focus({ preventScroll: true });

    track('QuizComplete', {
      score: score,
      content_name: 'Pawfolio 6 questions',
      value: score,
      currency: 'USD'
    });
  }

  // Single delegated handler — the card is re-rendered on every step.
  mount.addEventListener('click', function (e) {
    var t = e.target && e.target.closest ? e.target.closest('button, a') : null;
    if (!t) return;

    if (t.hasAttribute('data-skip')) {
      track('QuizSkipped', {});
      var buy = document.getElementById('buy-h');
      if (buy) buy.scrollIntoView({ behavior: 'smooth', block: 'start' });
      return;
    }
    if (t.hasAttribute('data-again')) {
      answers = [];
      renderQuestion(0);
      return;
    }
    if (t.hasAttribute('data-qz-cta')) {
      track('QuizCtaClick', { cta: t.getAttribute('data-qz-cta') });
      return; // let the link navigate
    }
    if (t.hasAttribute('data-yes')) {
      if (answers.length >= QUESTIONS.length) return; // guard against double taps
      if (!started) { started = true; track('QuizStart', {}); }
      answers.push(t.getAttribute('data-yes') === '1' ? 1 : 0);
      if (answers.length >= QUESTIONS.length) renderResult();
      else renderQuestion(answers.length);
    }
  });

  // Boot: swap the static list for the quiz.
  renderQuestion(0);
  mount.hidden = false;
  staticList.hidden = true;
  if (sub) {
    sub.innerHTML = 'Six questions, one point each. Answer honestly &mdash; ' +
                    'then we&rsquo;ll show you where each one lives.';
  }
})();
