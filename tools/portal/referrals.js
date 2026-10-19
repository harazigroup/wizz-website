// Team admin: Referrals. Loaded on admin.html after admin.js, which signs in and fires 'wizz:admin-ready'.
// Rules: friends get RM 100 off orders of RM 1,000+ (checkout.mjs); referrers earn 10% of the amount paid.
// Paid website orders open a "pending" commission automatically; approve it when the service is completed, then mark it paid.
(function(){
  const $=id=>document.getElementById(id);
  const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const money=(n,c)=>{try{return new Intl.NumberFormat('en-US',{style:'currency',currency:c||'MYR',currencyDisplay:'narrowSymbol'}).format(n)}catch(e){return (c||'')+' '+Number(n).toFixed(2)}};
  const fmtDate=d=>d?new Date(d).toLocaleDateString('en-GB',{day:'numeric',month:'short',year:'numeric'}):'';
  const ST={pending:'Pending (service not completed)',approved:'Approved, to pay',paid:'Paid',void:'Void'};
  const CLS={pending:'s-docs_needed',approved:'s-paid',paid:'s-delivered',void:'s-cancelled'};
  let sb=null,me=null,refs=[],coms=[],leadCount={},orderCount={};
  const flash=(m,bad)=>{const x=$('adMsg');x.hidden=false;x.textContent=m;x.className='ac-msg'+(bad?' bad':'');setTimeout(()=>x.hidden=true,4000);};

  async function load(){
    const [r,c,l,o]=await Promise.all([
      sb.from('referrers').select('*').order('created_at',{ascending:false}),
      sb.from('referral_commissions').select('*').order('created_at',{ascending:false}).limit(1000),
      sb.from('leads').select('ref_code').not('ref_code','is',null),
      sb.from('orders').select('ref_code').not('ref_code','is',null)]);
    if(r.error){$('rfBody').innerHTML='<p class="ac-none">Referrals aren\'t set up in the database yet. Run the referral SQL in Supabase (supabase/migrations/20261019_referral_program.sql), then reload.</p>';return;}
    refs=r.data||[];coms=c.data||[];leadCount={};orderCount={};
    (l.data||[]).forEach(x=>leadCount[x.ref_code]=(leadCount[x.ref_code]||0)+1);
    (o.data||[]).forEach(x=>orderCount[x.ref_code]=(orderCount[x.ref_code]||0)+1);
    render();
  }
  const sum=(list)=>{const t={};list.forEach(x=>t[x.currency]=(t[x.currency]||0)+Number(x.commission));return Object.entries(t).map(([c,v])=>money(v,c)).join(' + ')||'0';};
  function render(){
    const pend=coms.filter(x=>x.status==='pending'),appr=coms.filter(x=>x.status==='approved'),paid=coms.filter(x=>x.status==='paid');
    const f=$('rfF')?$('rfF').value:'open';
    const list=coms.filter(x=>f==='open'?['pending','approved'].includes(x.status):(!f||x.status===f));
    $('rfBody').innerHTML=
      '<div class="ld-stats rf-st"><div class="ld-stat"><b>'+refs.length+'</b><span>Referrers</span></div><div class="ld-stat"><b>'+pend.length+'</b><span>Pending · '+esc(sum(pend))+'</span></div><div class="ld-stat"><b>'+appr.length+'</b><span>To pay · '+esc(sum(appr))+'</span></div><div class="ld-stat"><b>'+paid.length+'</b><span>Paid · '+esc(sum(paid))+'</span></div></div>'+
      '<section class="ad-box"><h3>Commissions</h3><p class="ld-hint" style="margin-top:0">Website orders paid with a code appear here automatically as <b>Pending</b>. Approve when the client\'s service is completed, then mark as paid after you transfer the money. For sales closed on WhatsApp or by invoice, add the commission below.</p>'+
      '<div class="ad-filter"><select id="rfF"><option value="open">Open (pending + to pay)</option><option value="pending">Pending</option><option value="approved">Approved, to pay</option><option value="paid">Paid</option><option value="void">Void</option><option value="">Everything</option></select></div>'+
      (list.length?'<div class="rf-table"><table><thead><tr><th>Date</th><th>Code</th><th>Client / ref</th><th>Sale</th><th>Commission</th><th>Status</th><th></th></tr></thead><tbody>'+list.map(x=>{
        const r=refs.find(y=>y.code===x.code)||{};
        return '<tr><td>'+fmtDate(x.created_at)+'</td><td><b class="ltr">'+esc(x.code)+'</b><br><small>'+esc(r.name||'')+'</small></td><td>'+esc(x.client_name||'')+'<br><small class="ltr">'+esc(x.source_ref)+'</small></td><td class="ltr">'+money(x.sale_amount,x.currency)+'</td><td class="ltr"><b>'+money(x.commission,x.currency)+'</b></td><td><span class="ac-badge '+CLS[x.status]+'">'+ST[x.status]+'</span>'+(x.paid_at?'<br><small>'+fmtDate(x.paid_at)+'</small>':'')+(x.note?'<br><small>'+esc(x.note)+'</small>':'')+'</td><td><div class="rf-acts">'+
          (x.status==='pending'?'<button class="btn solid small" data-st="approved" data-id="'+x.id+'">Approve</button>':'')+
          (x.status==='approved'?'<button class="btn solid small" data-st="paid" data-id="'+x.id+'">Mark paid</button>':'')+
          (['pending','approved'].includes(x.status)?'<button class="ac-link danger" data-st="void" data-id="'+x.id+'">Void</button>':'')+'</div></td></tr>';}).join('')+'</tbody></table></div>':'<p class="ac-none">No commissions here.</p>')+
      '<details class="ad-new"><summary>Add a commission for a sale closed outside the website</summary><form id="rfAdd" class="ad-form"><select name="code" required><option value="">Referral code…</option>'+refs.filter(r=>r.status==='active').map(r=>'<option value="'+esc(r.code)+'">'+esc(r.code)+' · '+esc(r.name)+'</option>').join('')+'</select><input name="client" required placeholder="Client name"><input name="ref" required placeholder="Lead, quote or invoice ref"><input name="amount" type="number" min="0" step="0.01" required placeholder="Amount the client paid"><select name="currency"><option>MYR</option><option>USD</option><option>GBP</option><option>EUR</option><option>AED</option><option>SAR</option><option>OMR</option></select><button class="btn solid small" type="submit">Add (10%)</button></form><p class="ld-hint">Remember the client\'s RM 100 off: enter the amount they actually paid. The commission starts as Pending.</p></details></section>'+
      '<section class="ad-box"><h3>Referrers</h3>'+(refs.length?'<div class="rf-table"><table><thead><tr><th>Code</th><th>Name</th><th>Contact</th><th>Payout</th><th>Leads</th><th>Orders</th><th>To pay</th><th></th></tr></thead><tbody>'+refs.map(r=>{
        const owe=coms.filter(x=>x.code===r.code&&x.status==='approved');
        const wa=r.phone?'https://wa.me/'+String(r.phone).replace(/\D/g,''):'';
        return '<tr class="'+(r.status==='paused'?'rf-paused':'')+'"><td><b class="ltr">'+esc(r.code)+'</b><br><small>'+fmtDate(r.created_at)+'</small></td><td>'+esc(r.name)+'<br><small>'+esc(r.country||'')+'</small></td><td><a href="mailto:'+esc(r.email)+'">'+esc(r.email)+'</a>'+(wa?'<br><a class="ltr" target="_blank" rel="noopener" href="'+wa+'">'+esc(r.phone)+'</a>':'')+'</td><td>'+esc(r.payout_method||'–')+'<br><small>'+esc(r.payout_details||'')+'</small></td><td>'+(leadCount[r.code]||0)+'</td><td>'+(orderCount[r.code]||0)+'</td><td class="ltr">'+(owe.length?'<b>'+esc(sum(owe))+'</b>':'–')+'</td><td><button class="ac-link" data-pause="'+r.id+'">'+(r.status==='active'?'Pause code':'Activate')+'</button></td></tr>';}).join('')+'</tbody></table></div>':'<p class="ac-none">No referrers yet. Share <a href="refer.html" target="_blank">wizz.com.my/refer.html</a> to get the first sign-ups.</p>')+'</section>';
    $('rfF').value=f;
  }
  document.addEventListener('change',e=>{if(e.target.id==='rfF')render();});
  document.addEventListener('click',async e=>{
    const b=e.target.closest('[data-st]');
    if(b&&$('tabReferrals').contains(b)){
      const st=b.dataset.st;let note=null;
      if(st==='void'&&!confirm('Void this commission? Use this for refunds or cancelled services.'))return;
      if(st==='paid'){note=prompt('Payment note (optional), e.g. "Wise transfer 12 Nov":','');if(note===null)return;}
      const upd={status:st};if(note)upd.note=note;
      const {error}=await sb.from('referral_commissions').update(upd).eq('id',b.dataset.id);
      if(error)return flash(error.message,true);flash(st==='approved'?'Approved. It now shows as "To pay".':st==='paid'?'Marked as paid.':'Voided.');load();
    }
    const p=e.target.closest('[data-pause]');
    if(p){const r=refs.find(x=>x.id===p.dataset.pause);const st=r.status==='active'?'paused':'active';
      if(st==='paused'&&!confirm('Pause '+r.code+'? New clients won\'t get the discount and no new commissions open.'))return;
      const {error}=await sb.from('referrers').update({status:st}).eq('id',r.id);if(error)return flash(error.message,true);load();}
  });
  document.addEventListener('submit',async e=>{
    if(e.target.id!=='rfAdd')return;e.preventDefault();
    const d=Object.fromEntries(new FormData(e.target));const amt=Math.round(Number(d.amount)*100)/100;
    if(!(amt>0))return flash('Enter the amount the client paid.',true);
    const {error}=await sb.from('referral_commissions').insert({code:d.code,source:'manual',source_ref:d.ref.trim(),client_name:d.client.trim(),sale_amount:amt,currency:d.currency,rate:0.10,commission:Math.round(amt*10)/100,status:'pending',note:'Added by '+me.email});
    if(error)return flash(error.message.includes('duplicate')?'A commission for that ref already exists.':error.message,true);
    flash('Commission added as Pending.');load();
  });
  function start(d){sb=d.sb;me=d.me;load();}
  if(window.wizzAdmin)start(window.wizzAdmin);else document.addEventListener('wizz:admin-ready',e=>start(e.detail));
})();
