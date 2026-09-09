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

  /* Funnel measurement without a tag manager.
   * Cloudflare's beacon patches history.pushState and reports the route the
   * visitor is leaving, so pushing a real path on each step makes quiz
   * drop-off readable straight from the Paths report in Web Analytics:
   *   /pawfolio/        arrivals
   *   /pawfolio/q2..q6/ answered question 1..5
   *   /pawfolio/score/  answered all six
   * Query strings are stripped in that report, so the utm tags are carried
   * along purely for other tools and never split the counts.
   * Matching stub pages exist on disk (built by build_pawfolio.py) so a
   * refresh or a shared link still resolves instead of 404ing. */
  var BASE = '/pawfolio/';

  function mark(seg) {
    try {
      history.pushState({ qz: seg }, '', BASE + (seg ? seg + '/' : '') + location.search);
    } catch (e) { /* history unavailable — measurement is not worth breaking the quiz over */ }
  }

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

  /* Visitors who arrive from the paid reel have already been asked all six
   * questions by the video itself, so opening on "Question 1 of 6" makes the
   * click feel like a repeat and is the most likely reason paid traffic reaches
   * the page and stops. They get the answers view instead, with the quiz still
   * one tap away. Organic and direct visitors are unaffected. */
  /* The Daisy reel tells a story instead of asking the six questions, so a
   * visitor arriving from it must not be told they "just answered those six in
   * their head". ?from=daisy gets the timeline it promised, with Buy on the
   * same card. The quiz is one tap below and everyone else is unaffected. */
  function daisyArrival() {
    return /(^|[?&])from=daisy(&|$)/.test(location.search);
  }

  function paidArrival() {
    return /(^|[?&])utm_medium=paid(&|$)/.test(location.search) ||
           /(^|[?&])where=1(&|$)/.test(location.search);
  }

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
            '<a class="btn btn-primary btn-lg" href="' + BUY + '" data-qz-cta="buy">Buy now &mdash; $14.99</a>' +
            '<a class="btn btn-ghost btn-lg" href="' + DEMO + '" data-qz-cta="demo">Try the free demo</a>' +
          '</div>' +
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

  /* The result card without a score: the six questions and where each answer
   * lives. Shares .qz-rev styling with renderResult so nothing new is needed
   * in the stylesheet. */
  function renderWhere() {
    var rows = QUESTIONS.map(function (q) {
      return '<li>' +
        '<span class="qz-mark" aria-hidden="true">\u2192</span>' +
        '<span><b>' + q.ask + '</b><br>' +
        '<span class="qz-where">' + q.where + '</span></span>' +
      '</li>';
    }).join('');

    mount.innerHTML =
      '<div class="qz-card qz-fade">' +
        '<p class="qz-step">You just answered those six in your head.</p>' +
        '<h3 class="qz-q" id="qz-current" tabindex="-1">Here&rsquo;s where each answer lives.</h3>' +
        '<ul class="qz-rev">' + rows + '</ul>' +
        '<div class="qz-cta">' +
          '<div class="pf-actions">' +
            '<a class="btn btn-primary btn-lg" href="' + BUY + '" data-qz-cta="buy">Buy now &mdash; $14.99</a>' +
            '<a class="btn btn-ghost btn-lg" href="' + DEMO + '" data-qz-cta="demo">Try the free demo</a>' +
          '</div>' +
        '</div>' +
        '<button type="button" class="qz-again" data-quiz="1">Score yourself out of six &mdash; it takes a minute</button>' +
      '</div>';

    var h = document.getElementById('qz-current');
    if (h && started) h.focus({ preventScroll: true });
  }

  /* Arrival panel for the Daisy reel. Reuses .qz-card / .qz-cta / .pf-actions
   * so it needs nothing new in the stylesheet; the screenshot is the real
   * Timeline screen with the clinic names removed. */
  function renderDaisy() {
    var shot = 'display:block;width:100%;max-width:330px;margin:0 auto 0.85rem;' +
               'border-radius:14px;border:1px solid rgba(28,32,51,0.12);' +
               'box-shadow:0 10px 26px rgba(28,32,51,0.14);';

    mount.innerHTML =
      '<div class="qz-card qz-fade">' +
        '<p class="qz-step">08/16 &middot; 4:15 AM</p>' +
        '<h3 class="qz-q" id="qz-current" tabindex="-1">The night it stopped being a funny story.</h3>' +
        '<img src="/assets/daisy-timeline.png" alt="A Pawfolio timeline card: Daisy, Emergency, 08/16/2026 at 4:15 AM at a 24-hour emergency vet. The vet tried to lance the abscess and found that it is instead a mast cell tumor." style="' + shot + '" width="780" height="660" loading="eager">' +
        '<p class="qz-note">On 08/09 the skunk spray was a funny story I typed in and forgot. ' +
          'On 08/18 my vet read that note back and worked out that all the bathing afterwards ' +
          'had irritated a tumor &mdash; which is what started the whole thing.</p>' +
        '<p class="qz-note">That is the entire point. The small note is still there on the night ' +
          'it turns out to matter, along with every visit, dose and weight.</p>' +
        '<div class="qz-cta">' +
          '<div class="pf-actions">' +
            '<a class="btn btn-primary btn-lg" href="' + BUY + '" data-qz-cta="buy">Buy now &mdash; $14.99</a>' +
            '<a class="btn btn-ghost btn-lg" href="' + DEMO + '" data-qz-cta="demo">Try the free demo</a>' +
          '</div>' +
        '</div>' +
        '<button type="button" class="qz-again" data-quiz="1">Or answer six questions about your own pet</button>' +
      '</div>';

    var h = document.getElementById('qz-current');
    if (h && started) h.focus({ preventScroll: true });
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
    if (t.hasAttribute('data-quiz')) {
      answers = [];
      mark('');
      started = true;
      renderQuestion(0);
      return;
    }
    if (t.hasAttribute('data-again')) {
      answers = [];
      mark('');
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
      if (answers.length >= QUESTIONS.length) { mark('score'); renderResult(); }
      else { mark('q' + (answers.length + 1)); renderQuestion(answers.length); }
    }
  });

  /* Because each step is a real history entry, Back now means "undo my last
   * answer" rather than "leave the page", which is what people expect.
   * Re-rendering here never calls mark(), so replaying history cannot loop. */
  window.addEventListener('popstate', function (e) {
    var seg = (e.state && e.state.qz) || '';
    if (seg === 'score') {
      if (answers.length === QUESTIONS.length) renderResult();
      return;
    }
    if (seg === 'where') { renderWhere(); return; }
    var m = /^q([2-6])$/.exec(seg);
    var idx = m ? parseInt(m[1], 10) - 1 : 0;
    answers = answers.slice(0, idx);
    renderQuestion(idx);
  });

  // Boot: swap the static list for the quiz.
  var fromDaisy = daisyArrival();
  var fromAd = !fromDaisy && paidArrival();
  if (fromDaisy) {
    mark('daisy');
    track('DaisyLanding', {});
    renderDaisy();
  } else if (fromAd) {
    mark('where');
    track('PaidLanding', {});
    renderWhere();
  } else {
    renderQuestion(0);
  }
  mount.hidden = false;
  staticList.hidden = true;
  if (fromDaisy) {
    var h1 = document.getElementById('q-h');
    if (h1) h1.textContent = 'The skunk was nine days earlier.';
    if (sub) {
      sub.innerHTML = 'Daisy is my own dog. Everything below is her real record, ' +
                      'with the clinic names taken out.';
    }
  } else if (sub) {
    sub.innerHTML = fromAd
      ? 'You have already been asked all six. Here is where each answer lives &mdash; ' +
        'and you can still score yourself if you want to.'
      : 'Six questions, one point each. Answer honestly &mdash; ' +
        'then we&rsquo;ll show you where each one lives.';
  }
})();
