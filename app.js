const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const state=JSON.parse(localStorage.getItem('nucleo-state')||'{"done":[],"bookmarks":[],"theme":"light"}');
state.done ||= []; state.bookmarks ||= []; state.theme ||= 'light'; state.simHistory ||= []; state.seenQuizIds ||= [];
const save=()=>localStorage.setItem('nucleo-state',JSON.stringify(state));

const lessonData={
  geometry:{
    name:'Geometria',color:'blue',weeks:[
      {title:'Vetores: movimento com direção',topic:'Vetores',intro:'Antes de pensar em fórmula, pense em deslocamento. Um vetor conta <strong>quanto</strong> algo andou e <strong>para onde</strong>.'},
      {title:'Distâncias: medir sem régua',topic:'Distâncias',intro:'A distância entre dois pontos nasce de um triângulo invisível. Encontre seus catetos e Pitágoras faz o restante.'},
      {title:'Retas: uma regra para infinitos pontos',topic:'Retas',intro:'Uma reta é uma direção que se repete. Sua equação é uma forma compacta de descrever todos os pontos desse caminho.'},
      {title:'Planos: superfícies no espaço',topic:'Planos',intro:'Se a reta é um caminho, o plano é uma superfície sem bordas. Vamos aprender a descrevê-la com vetores.'},
      {title:'Cônicas: quando um corte vira curva',topic:'Cônicas',intro:'Circunferência, elipse, parábola e hipérbole são parentes: todas nascem de diferentes cortes em um cone.'},
      {title:'Revisão: conectando o mapa',topic:'Revisão',intro:'Agora vamos ligar vetores, distâncias, retas e curvas em um único mapa mental para a avaliação.'}
    ]},
  logic:{
    name:'Lógica',color:'coral',weeks:[
      {title:'Algoritmos: ideias em ordem',topic:'Algoritmos',intro:'Um algoritmo é uma conversa sem ambiguidades com a máquina: dados entram, passos transformam e um resultado sai.'},
      {title:'Dados, operadores e expressões',topic:'Operadores',intro:'Variáveis guardam estados; operadores os transformam. Juntos, eles formam as frases de um programa.'},
      {title:'Decisões: o código escolhe caminhos',topic:'Condicionais',intro:'Condições permitem que o mesmo programa responda de formas diferentes conforme os dados recebidos.'},
      {title:'Repetições: trabalho sem retrabalho',topic:'Laços',intro:'Laços transformam uma tarefa repetitiva em uma regra: enquanto houver trabalho, repita o passo certo.'},
      {title:'Coleções e funções',topic:'Estruturas',intro:'Coleções organizam muitos valores; funções dão nome a comportamentos reutilizáveis.'},
      {title:'Revisão e prova presencial',topic:'Revisão',intro:'Da entrada ao resultado: uma revisão integrada para raciocinar no papel e depois traduzir em código.'}
    ]}
};
// As atividades reais enviadas por print serão acrescentadas aqui, por disciplina e semana.
const weeklyActivities={
  'geometry-1':[], 'geometry-2':[], 'geometry-3':[], 'geometry-4':[], 'geometry-5':[], 'geometry-6':[],
  'logic-1':[], 'logic-2':[], 'logic-3':[], 'logic-4':[], 'logic-5':[], 'logic-6':[]
};
const lenses={
  geometry:{
    everyday:['↗','A explicação do GPS','O endereço não importa; o trajeto, sim.','Imagine que alguém diga: “ande três quarteirões para leste e dois para norte”. Essa instrução funciona partindo da sua casa, da faculdade ou de qualquer outro ponto. O vetor descreve a <em>mudança</em>, não a posição absoluta.','Um ponto diz “onde estou”. Um vetor diz “como saio daqui e chego ali”.'],
    visual:['△','A explicação do triângulo','Enxergue as componentes como dois passos.','Desenhe primeiro o deslocamento horizontal e depois o vertical. Os dois formam os catetos de um triângulo retângulo; o vetor é a seta diagonal que liga o início ao fim. O módulo aparece como a hipotenusa.','As componentes desmontam o movimento; o vetor inteiro remonta o caminho mais direto.'],
    recipe:['½','A receita de dois pontos','Final menos inicial. Sempre nessa ordem.','Para encontrar o vetor de A até B, subtraia as coordenadas: B − A. Faça x de B menos x de A; depois y de B menos y de A. Se A=(1,2) e B=(5,5), então AB=(5−1, 5−2)=(4,3).','Destino menos origem: a resposta diz o que precisa mudar para chegar.'],
    mistake:['!','A armadilha da posição','Vetor não é o ponto final.','Ao ver B=(5,5), é tentador responder que esse é o vetor. Mas (5,5) diz onde B está em relação à origem do plano. O vetor AB precisa dizer como sair de A e chegar a B — por isso calculamos B−A.','Pergunte: estou descrevendo um lugar ou um deslocamento?']
  },
  logic:{
    everyday:['☕','A explicação da receita','Algoritmo é uma sequência que outra pessoa consegue executar.','Pense em preparar café: separar filtro, aquecer água, colocar pó, despejar água. “Faça um café gostoso” é um objetivo, não um algoritmo. O algoritmo elimina lacunas suficientes para que o executor saiba o próximo passo.','Se duas pessoas entendem instruções opostas, ainda falta precisão.'],
    visual:['→','A explicação do fluxo','Dados percorrem uma pequena fábrica.','Imagine caixas entrando numa esteira. Cada etapa lê a caixa, faz uma transformação e a envia adiante. Variáveis são etiquetas; operações são máquinas; a saída é a caixa pronta.','Entrada → transformação → saída. Esse esqueleto aparece em quase todo programa.'],
    recipe:['123','A receita do computador','Quebre o desejo em verbos observáveis.','Troque “calcule a média” por: leia nota 1; leia nota 2; some as notas; divida por 2; mostre o resultado. Cada linha deve provocar uma ação clara e verificável.','Se você consegue testar cada passo separadamente, o algoritmo está ganhando forma.'],
    mistake:['?','A armadilha do óbvio','A máquina não completa o que ficou implícito.','Para nós, “mostre a maior nota” parece claro. Para a máquina, faltam decisões: quantas notas existem? Onde estão? Como comparar? O que fazer em empate? Programar é iluminar esses detalhes.','O computador é literal; a clareza do resultado depende da clareza da instrução.']
  }
};
let currentSubject='geometry',currentWeek=0;

function setSubject(subject){
  currentSubject=subject; $$('[data-subject]').forEach(b=>b.classList.toggle('active',b.dataset.subject===subject));
  updateLesson(); document.body.dataset.subject=subject;
}
function setWeek(n){currentWeek=n;$$('[data-week]').forEach(b=>b.classList.toggle('active',+b.dataset.week===n+1));updateLesson();}
function updateLesson(){
  const d=lessonData[currentSubject].weeks[currentWeek];
  $('#lesson-kicker').textContent=`${lessonData[currentSubject].name} · Semana ${String(currentWeek+1).padStart(2,'0')}`;
  $('#lesson-title').textContent=d.title; $('#lesson-intro').innerHTML=d.intro;
  const labels=currentSubject==='geometry'?['Vetores','Distâncias','Retas','Planos','Cônicas','Revisão']:['Algoritmos','Operadores','Decisões','Repetições','Funções','Revisão'];
  $$('[data-week]').forEach((b,i)=>b.querySelector('small').textContent=labels[i]);
  renderLens('everyday'); $$('.lens-tabs button').forEach((b,i)=>b.classList.toggle('active',i===0));
  const detailed=currentWeek===0;
  $$('.concept-card,.explanations,.lab-section,.practice-section').forEach(el=>el.style.display=detailed?'':'none');
  if(!detailed){
    $('#concept-card').style.display='grid';
    $('#concept-card').innerHTML=`<div class="concept-number">${String(currentWeek+1).padStart(2,'0')}</div><div><h3>O material desta semana está sendo preparado</h3><p>O mapa já está no lugar. Quando chegarmos a esta semana, entram aqui explicações em camadas, laboratório e exercícios guiados de <strong>${d.topic.toLowerCase()}</strong>.</p><div class="formula-strip"><span>agora</span><b>→</b><em>semana 01</em><small>um passo de cada vez</small></div></div>`;
  } else {restoreConcept();}
  const isGeo=currentSubject==='geometry';
  $('#geometry-lab').hidden=!isGeo; $('#logic-lab').hidden=isGeo;
  $('#lab-title').textContent=isGeo?'Laboratório de vetores':'Mesa de teste do algoritmo';
  $('#lab-copy').textContent=isGeo?'Altere as componentes. O desenho e os cálculos respondem na hora.':'Troque as notas e acompanhe cada variável ganhar um valor.';
  renderPractice();
  renderActivities();
  updateBookmark();
}
function restoreConcept(){
  const isGeo=currentSubject==='geometry';
  $('#concept-card').innerHTML=isGeo?`<div class="concept-number">01</div><div><h3>A ideia que sustenta tudo</h3><p>O vetor <strong>v = (3, 2)</strong> não é apenas um par de números. É uma instrução: saia de onde está, caminhe 3 unidades para a direita e 2 para cima.</p><div class="formula-strip"><span>v</span><b>=</b><em>( 3 , 2 )</em><small>horizontal&nbsp;&nbsp;&nbsp; vertical</small></div></div><div class="mini-sketch"><span>A</span><i></i><span>B</span><small>mesmo deslocamento,<br>em qualquer ponto</small></div>`:`<div class="concept-number">01</div><div><h3>A ideia que sustenta tudo</h3><p>Um algoritmo transforma uma intenção vaga em passos executáveis. Para calcular a média: <strong>ler → somar → dividir → mostrar</strong>.</p><div class="formula-strip"><span>dados</span><b>→</b><em>processo → saída</em><small>entrada&nbsp;&nbsp;&nbsp; transformação</small></div></div><div class="mini-sketch"><span>A</span><i></i><span>B</span><small>cada passo reduz<br>a ambiguidade</small></div>`;
}
function renderLens(key){const d=lenses[currentSubject][key];$('#lens-panel').innerHTML=`<div class="lens-icon">${d[0]}</div><div><span class="lens-label">${d[1]}</span><h4>${d[2]}</h4><p>${d[3]}</p><blockquote>${d[4]}</blockquote></div>`;}
function renderActivities(){
  const key=`${currentSubject}-${currentWeek+1}`,items=weeklyActivities[key]||[];
  $('#activity-subject').textContent=currentSubject==='geometry'?'Geometria analítica':'Lógica da programação';
  $('#activity-week').textContent=`Semana ${String(currentWeek+1).padStart(2,'0')}`;
  if(!items.length){
    $('#activity-list').innerHTML=`<div class="activity-empty"><div class="activity-empty-icon">⌁</div><div><h4>Pronto para receber o primeiro exercício</h4><p>Envie o print nesta conversa. Depois da resolução conjunta, o exercício aparecerá aqui para você e seus colegas revisarem.</p></div><small>Aguardando atividade</small></div>`;
    return;
  }
  $('#activity-list').innerHTML=items.map((item,i)=>`<details class="resolved-activity"><summary><b>${String(i+1).padStart(2,'0')}</b><span>${item.title}</span></summary><div class="resolved-activity-body">${item.content}</div></details>`).join('');
}

$$('[data-subject]').forEach(b=>b.addEventListener('click',()=>setSubject(b.dataset.subject)));
$$('[data-week]').forEach(b=>b.addEventListener('click',()=>setWeek(+b.dataset.week-1)));
$$('.lens-tabs button').forEach(b=>b.addEventListener('click',()=>{$$('.lens-tabs button').forEach(x=>x.classList.remove('active'));b.classList.add('active');renderLens(b.dataset.lens)}));

function drawVector(){
  const canvas=$('#vector-canvas'),ctx=canvas.getContext('2d'),x=+$('#vector-x').value,y=+$('#vector-y').value,w=canvas.width,h=canvas.height,ox=w/2,oy=h/2,s=45;
  ctx.clearRect(0,0,w,h);ctx.strokeStyle=getComputedStyle(document.body).getPropertyValue('--line');ctx.lineWidth=1;
  for(let i=-6;i<=6;i++){ctx.beginPath();ctx.moveTo(ox+i*s,0);ctx.lineTo(ox+i*s,h);ctx.stroke();ctx.beginPath();ctx.moveTo(0,oy+i*s);ctx.lineTo(w,oy+i*s);ctx.stroke()}
  ctx.strokeStyle=getComputedStyle(document.body).getPropertyValue('--ink');ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(0,oy);ctx.lineTo(w,oy);ctx.moveTo(ox,0);ctx.lineTo(ox,h);ctx.stroke();
  const ex=ox+x*s,ey=oy-y*s;ctx.strokeStyle='#e47758';ctx.fillStyle='#e47758';ctx.lineWidth=5;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(ox,oy);ctx.lineTo(ex,ey);ctx.stroke();
  if(x||y){const a=Math.atan2(ey-oy,ex-ox);ctx.beginPath();ctx.moveTo(ex,ey);ctx.lineTo(ex-14*Math.cos(a-.5),ey-14*Math.sin(a-.5));ctx.lineTo(ex-14*Math.cos(a+.5),ey-14*Math.sin(a+.5));ctx.closePath();ctx.fill()}
  ctx.beginPath();ctx.arc(ox,oy,5,0,Math.PI*2);ctx.fill();ctx.font='bold 14px DM Sans';ctx.fillText(`v = (${x}, ${y})`,ex+10,ey-10);
  const sq=x*x+y*y,root=Math.sqrt(sq),pretty=Number.isInteger(root)?String(root):`√${sq} ≈ ${root.toFixed(2).replace('.',',')}`;
  $('#x-output').textContent=x;$('#y-output').textContent=y;$('#vector-pair').textContent=`(${x}, ${y})`;$('#vector-module').textContent=pretty;
  $('#vector-reading').textContent=`${Math.abs(x)} ${x>=0?'→':'←'} e ${Math.abs(y)} ${y>=0?'↑':'↓'}`;
  $('#lab-insight').textContent=(x===0&&y===0)?'Este é o vetor nulo: não há deslocamento, por isso seu módulo é zero.':(x===0||y===0)?'Quando uma componente é zero, todo o movimento acontece sobre um único eixo.':'Perceba: o módulo forma a hipotenusa de um triângulo retângulo. Pitágoras reaparece aqui.';
}
['vector-x','vector-y'].forEach(id=>$('#'+id).addEventListener('input',drawVector));
$('#trace-code').addEventListener('click',()=>{
  const n1=Math.max(0,Math.min(10,+$('#nota-1').value||0)),n2=Math.max(0,Math.min(10,+$('#nota-2').value||0)),sum=n1+n2,avg=sum/2;
  const rows=[['01','nota_1',n1],['02','nota_2',n2],['03','soma',sum],['04','media',avg.toLocaleString('pt-BR')],['05','saída',avg.toLocaleString('pt-BR')]];
  $('#trace-rows').innerHTML=rows.map((r,i)=>`<div class="trace-row" style="animation-delay:${i*.11}s"><span>${r[0]}</span><b>${r[1]}</b><span>${r[2]}</span></div>`).join('');
  $('#trace-output').textContent=avg.toLocaleString('pt-BR');
});

const practices={geometry:[
  ['c','O vetor que leva A(1, 2) até B(5, 5) é:',['(6, 7)','(−4, −3)','(4, 3)','(5, 5)'],'o vetor AB é destino menos origem: (5−1, 5−2) = (4,3).'],
  ['b','Qual é o módulo do vetor v = (6, 8)?',['14','10','√14','48'],'use Pitágoras: √(6²+8²)=√100=10.'],
  ['d','O que permanece igual quando o mesmo vetor é desenhado a partir de outro ponto?',['A origem','O ponto final','As coordenadas dos pontos','Direção, sentido e módulo'],'ao transladar um vetor, mudam os pontos, mas direção, sentido e módulo permanecem.']
],logic:[
  ['b','Qual opção é um algoritmo claro para calcular o dobro?',['Pensar em um número','Ler o número, multiplicar por 2 e mostrar','Mostrar qualquer valor','Somar sem ler um valor'],'a sequência define entrada, transformação e saída sem deixar lacunas.'],
  ['c','Depois de x ← 4 e x ← x + 3, quanto vale x?',['4','3','7','12'],'a segunda atribuição usa o valor atual de x: 4 + 3 = 7, e guarda o novo resultado.'],
  ['a','Qual instrução representa uma saída?',['mostre media','leia nota','media ← soma / 2','inicio'],'“mostre” envia ao usuário o resultado que o algoritmo produziu.']
]};
function renderPractice(){
  if(currentWeek!==0)return;const letters=['a','b','c','d'];
  $('#exercise-list').innerHTML=practices[currentSubject].map((e,i)=>`<article class="exercise-card" data-answer="${e[0]}"><div class="exercise-meta"><span>0${i+1}</span><small>${i===0?'Aquecimento · 2 min':i===1?'Conexão · 3 min':'Interpretação · 4 min'}</small></div><h4>${e[1]}</h4><div class="answers">${e[2].map((o,j)=>`<button data-option="${letters[j]}">${letters[j].toUpperCase()} <span>${o}</span></button>`).join('')}</div><div class="feedback"><strong></strong><p></p></div></article>`).join('');
  $$('.exercise-card').forEach((card,i)=>{$$('.answers button',card).forEach(btn=>btn.addEventListener('click',()=>{const ok=btn.dataset.option===card.dataset.answer;card.classList.add('answered');btn.classList.add(ok?'correct':'wrong');if(!ok)$(`[data-option="${card.dataset.answer}"]`,card).classList.add('correct');$('.feedback strong',card).textContent=ok?'Boa — raciocínio certo.':'Quase. Repare na lógica:';$('.feedback p',card).textContent=practices[currentSubject][i][3];const key=`${currentSubject}-w1-e${i}`;if(!state.done.includes(key))state.done.push(key);save();updateProgress()}))});
  updateProgress();
}
function updateProgress(){const count=state.done.filter(x=>x.startsWith(`${currentSubject}-w1-e`)).length;$('#practice-done').textContent=Math.min(count,3);const pct=Math.min(100,Math.round(state.done.length/10*100));$('#progress-number').textContent=pct+'%';$('#progress-ring').style.strokeDashoffset=100.5-(100.5*pct/100);}

function bookmarkKey(){return `${currentSubject}-${currentWeek}`};function updateBookmark(){$('#bookmark').classList.toggle('saved',state.bookmarks.includes(bookmarkKey()))}$('#bookmark').addEventListener('click',()=>{const k=bookmarkKey(),i=state.bookmarks.indexOf(k);i>=0?state.bookmarks.splice(i,1):state.bookmarks.push(k);save();updateBookmark()});
$('#theme-toggle').addEventListener('click',()=>{state.theme=state.theme==='dark'?'light':'dark';document.body.classList.toggle('dark',state.theme==='dark');save();drawVector()});document.body.classList.toggle('dark',state.theme==='dark');
$$('[data-open-planner]').forEach(b=>b.addEventListener('click',()=>$('#planner-dialog').showModal()));$$('[data-close-dialog]').forEach(b=>b.addEventListener('click',()=>b.closest('dialog').close()));$$('dialog').forEach(d=>d.addEventListener('click',e=>{if(e.target===d)d.close()}));
$$('.topnav a').forEach(a=>a.addEventListener('click',()=>{$$('.topnav a').forEach(x=>x.classList.remove('active'));a.classList.add('active')}));
$$('[data-week-jump]').forEach(b=>b.addEventListener('click',()=>{setWeek(+b.dataset.weekJump-1);$('#estudo').scrollIntoView()}));

const questionBank=[
  {id:'g01',s:'g',topic:'Geometria · Vetores',q:'De P(−1, 2) até Q(3, 5), qual é o vetor PQ?',opts:['(2, 7)','(4, 3)','(−4, −3)','(3, 5)'],a:1,why:'Destino menos origem: (3−(−1), 5−2) = (4,3).'},
  {id:'g02',s:'g',topic:'Geometria · Vetores',q:'Qual é o módulo do vetor (3, 4)?',opts:['7','12','5','√7'],a:2,why:'√(3²+4²)=√25=5.'},
  {id:'g03',s:'g',topic:'Geometria · Vetores',q:'Dois vetores são iguais quando possuem:',opts:['A mesma origem','O mesmo ponto final','As mesmas componentes','O mesmo nome'],a:2,why:'As componentes determinam direção, sentido e módulo do vetor.'},
  {id:'g04',s:'g',topic:'Geometria · Vetores',q:'A soma de u=(2,−1) e v=(3,4) é:',opts:['(5,3)','(1,5)','(6,−4)','(5,−5)'],a:0,why:'Somamos componente a componente: (2+3, −1+4)=(5,3).'},
  {id:'g05',s:'g',topic:'Geometria · Vetores',q:'O vetor oposto de v=(4,−2) é:',opts:['(4,2)','(−4,−2)','(−4,2)','(2,−4)'],a:2,why:'O vetor oposto troca o sinal de cada componente.'},
  {id:'g06',s:'g',topic:'Geometria · Vetores',q:'Multiplicar (2,3) por 3 resulta em:',opts:['(5,6)','(6,9)','(6,3)','(2,9)'],a:1,why:'A multiplicação escalar atua em cada componente: (3·2,3·3).'},
  {id:'g07',s:'g',topic:'Geometria · Vetores',q:'Qual vetor é nulo?',opts:['(0,1)','(1,0)','(0,0)','(−1,1)'],a:2,why:'Sem deslocamento horizontal nem vertical, o módulo é zero.'},
  {id:'g08',s:'g',topic:'Geometria · Vetores',q:'O vetor (−3,2) indica deslocamento:',opts:['3 à direita e 2 abaixo','3 à esquerda e 2 acima','3 acima e 2 à esquerda','Somente vertical'],a:1,why:'x negativo aponta para a esquerda; y positivo, para cima.'},
  {id:'g09',s:'g',topic:'Geometria · Vetores',q:'Se |v|=0, então:',opts:['v é vertical','v é horizontal','v é o vetor nulo','v tem duas direções'],a:2,why:'Somente o vetor com todas as componentes zero possui módulo zero.'},
  {id:'g10',s:'g',topic:'Geometria · Vetores',q:'O produto escalar de (1,2) e (3,4) é:',opts:['(3,8)','11','10','14'],a:1,why:'1·3 + 2·4 = 3+8 = 11.'},
  {id:'g11',s:'g',topic:'Geometria · Distâncias',q:'A distância entre (0,0) e (6,8) é:',opts:['14','10','48','√14'],a:1,why:'√(6²+8²)=√100=10.'},
  {id:'g12',s:'g',topic:'Geometria · Ponto médio',q:'O ponto médio entre A(2,4) e B(6,8) é:',opts:['(8,12)','(3,4)','(4,6)','(2,2)'],a:2,why:'Fazemos a média de cada coordenada: ((2+6)/2,(4+8)/2)=(4,6).'},
  {id:'g13',s:'g',topic:'Geometria · Distâncias',q:'A distância entre (2,3) e (2,9) é:',opts:['6','11','4','12'],a:0,why:'Os pontos têm o mesmo x; a distância vertical é |9−3|=6.'},
  {id:'g14',s:'g',topic:'Geometria · Ponto médio',q:'Se M(3,2) é o ponto médio de A(1,1) e B(x,y), então B é:',opts:['(2,1)','(5,3)','(4,2)','(6,4)'],a:1,why:'(1+x)/2=3 dá x=5; (1+y)/2=2 dá y=3.'},
  {id:'g15',s:'g',topic:'Geometria · Retas',q:'Na equação y=2x+1, o coeficiente angular é:',opts:['1','−1','2','3'],a:2,why:'Na forma y=mx+b, m é o coeficiente angular.'},
  {id:'g16',s:'g',topic:'Geometria · Retas',q:'Uma reta horizontal possui coeficiente angular:',opts:['Zero','Um','Indefinido','Negativo'],a:0,why:'Não há variação vertical; por isso Δy/Δx=0.'},
  {id:'g17',s:'g',topic:'Geometria · Retas',q:'Qual ponto pertence à reta y=x+2?',opts:['(0,0)','(1,2)','(2,4)','(3,2)'],a:2,why:'Substituindo x=2, obtemos y=4.'},
  {id:'g18',s:'g',topic:'Geometria · Retas',q:'Retas com o mesmo coeficiente angular e interceptos diferentes são:',opts:['Perpendiculares','Paralelas','Coincidentes','Verticais'],a:1,why:'Mesma inclinação e alturas diferentes produzem retas paralelas.'},
  {id:'l01',s:'l',topic:'Lógica · Algoritmos',q:'Qual sequência descreve melhor um algoritmo para calcular desconto?',opts:['Mostrar preço e terminar','Ler preço, aplicar percentual e mostrar novo preço','Escolher qualquer valor','Somar preço ao percentual'],a:1,why:'Há entrada, transformação definida e saída verificável.'},
  {id:'l02',s:'l',topic:'Lógica · Algoritmos',q:'A principal característica de um bom algoritmo é:',opts:['Ambiguidade','Quantidade de linhas','Clareza dos passos','Uso obrigatório de código'],a:2,why:'Os passos precisam ser claros, finitos e executáveis.'},
  {id:'l03',s:'l',topic:'Lógica · Entrada e saída',q:'Qual instrução representa entrada de dados?',opts:['mostre resultado','leia idade','total ← 10','fim'],a:1,why:'“leia” recebe um valor externo e o armazena.'},
  {id:'l04',s:'l',topic:'Lógica · Entrada e saída',q:'Qual instrução representa uma saída?',opts:['leia nome','idade ← 20','mostre media','inicio'],a:2,why:'“mostre” apresenta ao usuário o resultado produzido.'},
  {id:'l05',s:'l',topic:'Lógica · Algoritmos',q:'Um algoritmo precisa necessariamente:',opts:['Ser escrito em Python','Ter passos finitos','Usar banco de dados','Possuir interface gráfica'],a:1,why:'Um algoritmo deve terminar após um número finito de passos.'},
  {id:'l06',s:'l',topic:'Lógica · Algoritmos',q:'Em entrada → processamento → saída, calcular a média pertence a:',opts:['Entrada','Processamento','Saída','Comentário'],a:1,why:'A média transforma os dados recebidos em um novo valor.'},
  {id:'l07',s:'l',topic:'Lógica · Variáveis',q:'Uma variável representa principalmente:',opts:['Um valor armazenado que pode mudar','Um erro inevitável','Somente texto','Uma linha decorativa'],a:0,why:'Variáveis nomeiam espaços de memória usados durante a execução.'},
  {id:'l08',s:'l',topic:'Lógica · Atribuição',q:'Após x ← 4 e x ← x+3, quanto vale x?',opts:['4','3','7','12'],a:2,why:'A segunda atribuição calcula 4+3 e substitui o valor anterior por 7.'},
  {id:'l09',s:'l',topic:'Lógica · Operadores',q:'Qual é o resultado de 17 MOD 5?',opts:['2','3','5','12'],a:0,why:'MOD retorna o resto da divisão inteira; 17 dividido por 5 deixa resto 2.'},
  {id:'l10',s:'l',topic:'Lógica · Operadores',q:'Qual expressão calcula corretamente a média de a e b?',opts:['a+b/2','(a+b)/2','a+(b/2)','a*b/2'],a:1,why:'Os parênteses garantem que a soma aconteça antes da divisão.'},
  {id:'l11',s:'l',topic:'Lógica · Tipos de dados',q:'Qual valor é do tipo lógico?',opts:['"Maria"','42','3,14','verdadeiro'],a:3,why:'Valores lógicos assumem verdadeiro ou falso.'},
  {id:'l12',s:'l',topic:'Lógica · Operadores',q:'Se a=5 e b=2, a*b+1 resulta em:',opts:['11','15','8','7'],a:0,why:'A multiplicação ocorre primeiro: 5·2+1=11.'},
  {id:'l13',s:'l',topic:'Lógica · Condicionais',q:'Uma estrutura “se...senão” serve para:',opts:['Repetir para sempre','Escolher entre caminhos','Guardar vários itens','Encerrar o computador'],a:1,why:'A condição determina qual bloco de instruções será executado.'},
  {id:'l14',s:'l',topic:'Lógica · Condicionais',q:'Se idade=17, a condição idade >= 18 é:',opts:['Verdadeira','Falsa','Indefinida','Uma repetição'],a:1,why:'17 não é maior nem igual a 18.'},
  {id:'l15',s:'l',topic:'Lógica · Repetições',q:'Qual estrutura é adequada quando sabemos quantas vezes repetir?',opts:['para','se','senão','leia'],a:0,why:'O laço “para” é natural quando há uma contagem definida.'},
  {id:'l16',s:'l',topic:'Lógica · Repetições',q:'Em um laço, uma condição que nunca se torna falsa pode causar:',opts:['Uma média','Um laço infinito','Uma variável constante','Uma entrada'],a:1,why:'Sem condição de parada alcançável, a repetição não termina.'},
  {id:'l17',s:'l',topic:'Lógica · Condicionais',q:'O operador lógico E resulta verdadeiro quando:',opts:['Ao menos uma condição é verdadeira','Todas as condições são verdadeiras','Todas são falsas','Os valores são números'],a:1,why:'O operador E exige que todas as condições ligadas sejam verdadeiras.'},
  {id:'l18',s:'l',topic:'Lógica · Condicionais',q:'O operador lógico OU resulta falso quando:',opts:['Uma condição é verdadeira','Todas são verdadeiras','Todas são falsas','Há duas condições'],a:2,why:'OU só é falso quando nenhuma das condições é verdadeira.'}
];
const shuffle=items=>{const a=[...items];for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
let activeQuiz=[],qi=0,answers=[];
function pickQuestions(subject,count){let available=questionBank.filter(q=>q.s===subject&&!state.seenQuizIds.includes(q.id));if(available.length<count){state.seenQuizIds=state.seenQuizIds.filter(id=>!questionBank.some(q=>q.s===subject&&q.id===id));available=questionBank.filter(q=>q.s===subject)}const picked=shuffle(available).slice(0,count);state.seenQuizIds.push(...picked.map(q=>q.id));return picked}
function prepareQuiz(){activeQuiz=shuffle([...pickQuestions('g',6),...pickQuestions('l',6)]).map(q=>{const correct=q.opts[q.a],opts=shuffle(q.opts);return{...q,opts,a:opts.indexOf(correct)}});qi=0;answers=[];save()}
function renderHistory(){const latest=state.simHistory[0];$('#last-score').textContent=latest?.score??'—';$('#last-score-line').style.width=latest?`${latest.score/12*100}%`:'0';$('#last-score-copy').textContent=latest?`Realizado em ${latest.date}. Você pode gerar outro conjunto quando quiser.`:'Ainda não realizado. Comece quando quiser — não há cronômetro obrigatório.';$('#sim-history').innerHTML=state.simHistory.length?state.simHistory.slice(0,3).map((h,i)=>`<div class="history-item"><span>${i===0?'Último':'Anterior'} · ${h.date}</span><strong>${h.score}/12</strong></div>`).join(''):'<div class="history-item"><span>Histórico</span><strong>Nenhuma tentativa</strong></div>';$('#clear-history').style.display=state.simHistory.length?'block':'none'}
function startQuiz(){prepareQuiz();$('#sim-setup').hidden=true;$('#quiz-result').hidden=true;$('#quiz-area').hidden=false;renderQuestion()}
$('#start-sim').addEventListener('click',()=>{renderHistory();$('#sim-dialog').showModal();$('#sim-setup').hidden=false;$('#quiz-area').hidden=true;$('#quiz-result').hidden=true});
$('#begin-quiz').addEventListener('click',startQuiz);$('#new-sim').addEventListener('click',startQuiz);
$('#clear-history').addEventListener('click',()=>{state.simHistory=[];state.seenQuizIds=[];save();renderHistory()});
function renderQuestion(){const q=activeQuiz[qi];$('#quiz-label').textContent=`Questão ${qi+1} de ${activeQuiz.length}`;$('#quiz-bar').style.width=`${(qi+1)/activeQuiz.length*100}%`;$('#quiz-topic').textContent=q.topic;$('#quiz-question').textContent=q.q;$('#quiz-options').innerHTML=q.opts.map((o,i)=>`<button data-i="${i}"><b>${String.fromCharCode(65+i)}</b>&nbsp;&nbsp;${o}</button>`).join('');$('#next-question').disabled=true;$$('#quiz-options button').forEach(b=>b.addEventListener('click',()=>{$$('#quiz-options button').forEach(x=>x.classList.remove('selected'));b.classList.add('selected');answers[qi]=+b.dataset.i;$('#next-question').disabled=false}));$('#next-question').innerHTML=qi===activeQuiz.length-1?'Ver resultado <span>→</span>':'Próxima <span>→</span>'}
$('#next-question').addEventListener('click',()=>{if(qi<activeQuiz.length-1){qi++;renderQuestion()}else showResult()});
function showResult(){const score=activeQuiz.reduce((n,q,i)=>n+(answers[i]===q.a),0);$('#quiz-area').hidden=true;$('#quiz-result').hidden=false;$('#quiz-score').textContent=score;$('#quiz-message').textContent=score>=10?'Excelente: os fundamentos estão firmes. Avance mantendo a prática.':score>=7?'Boa base. Leia os comentários e revise as questões que errou.':'Este resultado é um mapa, não um rótulo. Volte às explicações e tente um novo conjunto depois.';$('#quiz-review').innerHTML=activeQuiz.map((q,i)=>`<div class="review-item"><b>${answers[i]===q.a?'✓':'↺'} ${q.topic}</b><p>${q.why}</p></div>`).join('');state.simHistory.unshift({score,date:new Date().toLocaleDateString('pt-BR',{day:'2-digit',month:'2-digit',year:'2-digit'})});state.simHistory=state.simHistory.slice(0,10);state.done.push(`quiz-${Date.now()}`);save();renderHistory();updateProgress()}

setSubject('geometry');setWeek(0);drawVector();renderHistory();updateProgress();
