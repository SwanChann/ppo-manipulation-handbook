(() => {
  'use strict';
  const $ = (s) => document.querySelector(s);
  const $$ = (s) => Array.from(document.querySelectorAll(s));
  const stages = [
    ['PRESS_VALID','接近目标，形成连续有效按压','只激活当前按压目标的进度项。按钮真实行程达到阈值并连续保持，才完成本阶段。','真实深度 ≥ 5 mm，连续保持 100 ms。','本阶段的有符号进度 + 一次性有效按压事件奖励。'],
    ['RELEASE_CLEAR','释放按钮，沿安全方向撤离','有效按压进度保持锁存，释放不会回到“尚未按过”。按压阶段的接近奖励关闭。','按钮释放，且达到 20 mm 撤离净空。','本阶段的撤离进度 + 一次性释放 / 撤离事件奖励。'],
    ['RETURN_SETTLE','返回完整任务初态，并连续停稳','最终返回预操作初态；碰撞和重复按压由独立验收检查。第三阶段到位不等于已经成功。','TCP 误差 ≤ 2 mm、关节误差 ≤ 0.02 rad；TCP 速度 ≤ 1 mm/s、关节速度 ≤ 0.01 rad/s，连续 150 ms。','本阶段的返回进度；完整物理验收通过后才领取完成奖励。']
  ];
  function selectStage(i) {
    if (!$('#stage-panel')) return;
    $$('[data-stage]').forEach((b, j) => { b.setAttribute('aria-selected', String(j === i)); b.tabIndex = j === i ? 0 : -1; });
    $$('#onehot b').forEach((b, j) => { b.textContent = j === i ? '1' : '0'; b.classList.toggle('active', j === i); });
    ['label','title','body','event','reward'].forEach((key, j) => { $('#stage-' + key).textContent = stages[i][j]; });
    $('#stage-panel').setAttribute('aria-labelledby', 'stage-tab-' + i);
  }
  $$('[data-stage]').forEach(b => {
    b.addEventListener('click', () => selectStage(Number(b.dataset.stage)));
    b.addEventListener('keydown', e => {
      if (!['ArrowLeft','ArrowRight','Home','End'].includes(e.key)) return;
      e.preventDefault();
      const i = e.key === 'Home' ? 0 : e.key === 'End' ? 2 : (Number(b.dataset.stage) + (e.key === 'ArrowRight' ? 1 : 2)) % 3;
      selectStage(i); $('#stage-tab-' + i).focus();
    });
  });
  function filterTasks() {
    if (!$('#task-search')) return;
    const q = $('#task-search').value.trim().toLocaleLowerCase();
    const family = $('#task-family').value;
    let n = 0;
    $$('.task-card').forEach(card => {
      card.hidden = !(card.dataset.search.includes(q) && (family === 'all' || family === card.dataset.family));
      if (!card.hidden) n++;
    });
    $('#task-count').textContent = `显示 ${n} / ${$$('.task-card').length} 条任务与变体`;
    $('#task-empty').hidden = n > 0;
  }
  ['input','change'].forEach(ev => $$('#task-search, #task-family').forEach(e => e.addEventListener(ev, filterTasks)));
  filterTasks();
  $$('.config-toggle').forEach(b => b.addEventListener('click', () => {
    const row = document.getElementById(b.getAttribute('aria-controls'));
    row.hidden = !row.hidden;
    b.setAttribute('aria-expanded', String(!row.hidden)); b.textContent = row.hidden ? '展开' : '收起';
  }));
  function filterConfigs() {
    if (!$('#config-search')) return;
    const q = $('#config-search').value.trim().toLocaleLowerCase(); let n = 0;
    $$('.config-row').forEach(row => {
      row.hidden = !row.dataset.search.includes(q);
      const detail = document.getElementById(row.dataset.detail);
      if (row.hidden) { detail.hidden = true; const b = row.querySelector('button'); b.setAttribute('aria-expanded','false'); b.textContent = '展开'; }
      else n++;
    });
    $('#config-count').textContent = `显示 ${n} / ${$$('.config-row').length} 套配置；命令仅作源码入口参考，未执行上游训练。`;
  }
  $('#config-search')?.addEventListener('input', filterConfigs); filterConfigs();
  function calculate() {
    if (!$('#calc-output')) return;
    const values = ['total','envs','steps'].map(k => Number($('#calc-' + k).value));
    if (!values.every(x => Number.isSafeInteger(x) && x > 0)) { $('#calc-output').textContent = '请输入三个正整数。'; return; }
    const [n, e, t] = values, batch = e * t, rounds = Math.floor(n / batch);
    $('#calc-output').textContent = `每轮 ${batch.toLocaleString('en-US')} 样本 · ${rounds.toLocaleString('en-US')} 个完整采样轮次 · 对齐后 ${(rounds * batch).toLocaleString('en-US')} 步`;
  }
  $$('#calc-total,#calc-envs,#calc-steps').forEach(e => e.addEventListener('input', calculate)); calculate();
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => entries.forEach(e => { if (e.isIntersecting) $$('.sidebar nav a').forEach(a => a.classList.toggle('active', a.hash === '#' + e.target.id)); }), { rootMargin: '-10% 0px -65% 0px' });
    $$('.main>section[id]').forEach(s => observer.observe(s));
  }
  $$('pre').forEach(pre => {
    const b = document.createElement('button'); b.className = 'copy-button'; b.textContent = '复制'; b.type = 'button';
    b.addEventListener('click', async () => {
      const text = (pre.querySelector('code') || pre).textContent;
      try { await navigator.clipboard.writeText(text); b.textContent = '已复制'; }
      catch { const range = document.createRange(); range.selectNodeContents(pre); const sel = getSelection(); sel.removeAllRanges(); sel.addRange(range); b.textContent = '已选中，请复制'; }
      setTimeout(() => { b.textContent = '复制'; }, 2000);
    }); pre.before(b);
  });
  // Browser-only regression checks, enabled by the verification URL.
  if (location.search.includes('verify=1') && $('#task-search')) {
    const results = [];
    function check(name, ok) { results.push({name, passed: Boolean(ok)}); }
    check('initial task count', $$('.task-card').filter(e => !e.hidden).length === 19);
    $('#task-family').value = 'press-switch'; filterTasks();
    check('button task filter', $$('.task-card').filter(e => !e.hidden).length === 3);
    $('#task-search').value = 'NO_MATCH_774'; filterTasks(); check('empty state', !$('#task-empty').hidden);
    $('#task-family').value = 'all'; $('#task-search').value = ''; filterTasks();
    selectStage(2); check('phase onehot', $$('#onehot b').map(b => b.textContent).join('') === '001');
    check('return settle criteria', $('#stage-event').textContent.includes('150 ms')); selectStage(0);
    $('#config-search').value = 'tutorial'; filterConfigs(); check('tutorial configs', $$('.config-row').filter(e => !e.hidden).length === 2);
    $('#config-search').value = ''; filterConfigs();
    const first = $('.config-toggle'); first.click(); check('config expand', first.getAttribute('aria-expanded') === 'true'); first.click();
    check('rollout arithmetic', $('#calc-output').textContent.includes('1,999,872'));
    $('#calc-envs').value = '64'; calculate(); check('parallel arithmetic', $('#calc-output').textContent.includes('244 个')); $('#calc-envs').value = '8'; calculate();
    $('#calc-envs').value = '0'; calculate(); check('invalid budget input', $('#calc-output').textContent === '请输入三个正整数。'); $('#calc-envs').value = '8'; calculate();
    const r = document.createElement('script'); r.type = 'application/json'; r.id = 'verification-results'; r.textContent = JSON.stringify(results); document.body.append(r);
    const images = $$('img'); images.forEach(img => { img.loading = 'eager'; });
    Promise.all(images.map(img => img.decode().then(() => true).catch(() => false))).then(loaded => {
      check('all task images decode offline', images.length > 0 && loaded.every(Boolean));
      check('every guide card has an image', $$('.task-card').every(card => card.querySelector('figure img')));
      r.textContent = JSON.stringify(results);
    });
  }
})();
