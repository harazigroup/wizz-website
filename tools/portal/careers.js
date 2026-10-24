// Team admin: Careers. Job applications from careers.html. CVs arrive at info@ as email attachments; this list tracks status.
(function(){
  const $=id=>document.getElementById(id);
  const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const fmt=d=>d?new Date(d).toLocaleDateString('en-GB',{day:'numeric',month:'short',year:'numeric'}):'';
  const ST={new:'New',shortlisted:'Shortlisted',interview:'Interview',hired:'Hired',rejected:'Not a fit'};
  const CLS={new:'s-docs_needed',shortlisted:'s-paid',interview:'s-paid',hired:'s-delivered',rejected:'s-cancelled'};
  let sb=null,rows=[];
  const flash=(m,bad)=>{const x=$('adMsg');if(!x)return;x.hidden=false;x.textContent=m;x.className='ac-msg'+(bad?' bad':'');setTimeout(()=>x.hidden=true,3500);};
  async function load(){
    const r=await sb.from('job_applications').select('*').order('created_at',{ascending:false}).limit(500);
    if(r.error){$('jbBody').innerHTML='<p class="ac-none">Careers isn\'t set up in the database yet. Run supabase/migrations/20261024_job_applications.sql in Supabase, then reload.</p>';return;}
    rows=r.data||[];render();
  }
  function render(){
    const f=$('jbF')?$('jbF').value:'open';
    const list=rows.filter(x=>f==='open'?['new','shortlisted','interview'].includes(x.status):(!f||x.status===f));
    const count=s=>rows.filter(x=>x.status===s).length;
    $('jbBody').innerHTML='<div class="ld-stats rf-st"><div class="ld-stat"><b>'+count('new')+'</b><span>New</span></div><div class="ld-stat"><b>'+count('shortlisted')+'</b><span>Shortlisted</span></div><div class="ld-stat"><b>'+count('interview')+'</b><span>Interview</span></div><div class="ld-stat"><b>'+count('hired')+'</b><span>Hired</span></div></div>'+
      '<section class="ad-box"><h3>Applications</h3><p class="ld-hint" style="margin-top:0">Each CV is attached to the email sent to info@ (subject "Job application: …"). Change the status here as you go.</p>'+
      '<div class="ad-filter"><select id="jbF"><option value="open">Open (new, shortlisted, interview)</option>'+Object.entries(ST).map(([k,v])=>'<option value="'+k+'">'+v+'</option>').join('')+'<option value="">Everything</option></select></div>'+
      (list.length?'<div class="rf-table"><table><thead><tr><th>Date</th><th>Applicant</th><th>Role</th><th>Details</th><th>Status</th></tr></thead><tbody>'+list.map(x=>{
        const wa=x.phone?'https://wa.me/'+String(x.phone).replace(/\D/g,''):'';
        return '<tr><td>'+fmt(x.created_at)+'<br><small class="ltr">'+esc(x.ref)+'</small></td><td><b>'+esc(x.name)+'</b><br><a href="mailto:'+esc(x.email)+'">'+esc(x.email)+'</a>'+(wa?'<br><a class="ltr" target="_blank" rel="noopener" href="'+wa+'">'+esc(x.phone)+'</a>':'')+'</td><td>'+esc(x.role)+'</td><td><small>'+esc([x.country,x.setup,x.languages].filter(Boolean).join(' · '))+'</small>'+(x.link?'<br><a target="_blank" rel="noopener" href="'+esc(/^https?:/.test(x.link)?x.link:'https://'+x.link)+'">Link</a>':'')+(x.message?'<br><small>'+esc(x.message.slice(0,220))+'</small>':'')+'</td><td><select data-id="'+x.id+'" class="jb-st">'+Object.entries(ST).map(([k,v])=>'<option value="'+k+'"'+(k===x.status?' selected':'')+'>'+v+'</option>').join('')+'</select></td></tr>';}).join('')+'</tbody></table></div>':'<p class="ac-none">No applications here. Share <a href="careers.html" target="_blank">wizz.com.my/careers.html</a>.</p>')+'</section>';
    $('jbF').value=f;
  }
  document.addEventListener('change',async e=>{
    if(e.target.id==='jbF')return render();
    if(e.target.classList.contains('jb-st')){
      const {error}=await sb.from('job_applications').update({status:e.target.value}).eq('id',e.target.dataset.id);
      if(error)return flash(error.message,true);const r=rows.find(x=>x.id===e.target.dataset.id);if(r)r.status=e.target.value;flash('Status updated.');render();
    }
  });
  function start(d){sb=d.sb;load();}
  if(window.wizzAdmin)start(window.wizzAdmin);else document.addEventListener('wizz:admin-ready',e=>start(e.detail));
})();
