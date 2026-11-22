/* 구조 먼저 그리기 연구실 02 · 실천편 — 실험 패널 모음 (외부 라이브러리 없음) */
(function(){
'use strict';
var NS='http://www.w3.org/2000/svg';
var C={teal:'#0f8f84',orange:'#e8731a',navy:'#1e2f6e',blue:'#2458d6',green:'#13733a',red:'#c9302c',purple:'#6b4fb0',grid:'#e3e8ee',muted:'#5b6874',ink:'#16212b'};
var KFONT='"IBM Plex Sans KR","Malgun Gothic","Noto Sans KR",sans-serif';
var RM=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var P={};

/* ---------- 공용 도구 ---------- */
function el(tag,a,parent){var e=document.createElementNS(NS,tag);for(var k in a){if(a[k]!=null)e.setAttribute(k,a[k]);}if(parent)parent.appendChild(e);return e;}
function ktxt(p,x,y,s,a){a=a||{};var t=el('text',{x:x,y:y,'font-size':a.size||13,fill:a.fill||C.muted,'font-family':KFONT,'text-anchor':a.anchor||'start','font-weight':a.weight||'normal'},p);t.textContent=s;return t;}
function svgOf(h,W,H,label){h.innerHTML='';return el('svg',{viewBox:'0 0 '+W+' '+H,role:'img','aria-label':'실험 그림: '+(label||noteOf(h))},h);}
function noteOf(h){var n=h.parentNode&&h.parentNode.querySelector('.ph small');return n?n.textContent:'';}
function canvasOf(h,W,H,mw){h.innerHTML='';var c=document.createElement('canvas');c.width=W;c.height=H;c.style.width='100%';c.style.maxWidth=(mw||W*1.2)+'px';c.style.margin='0 auto';c.style.height='auto';c.style.display='block';c.style.borderRadius='10px';c.setAttribute('role','img');c.setAttribute('aria-label','실험 그림: '+noteOf(h));h.appendChild(c);return c;}
function out(h){return h.parentNode.querySelector('.readout');}
function ctl(h){return h.parentNode.querySelector('.ctrl');}
function f2(v,d){d=d==null?2:d;var m=Math.pow(10,d);var s=(Math.round(v*m)/m).toFixed(d);s=s.replace(/\.?0+$/,'');if(s==='-0')s='0';return s;}
function num(v,d){return v<0?'−'+f2(-v,d):f2(v,d);}
function clamp(v,a,b){return Math.max(a,Math.min(b,v));}
function lerp(a,b,t){return a+(b-a)*t;}
function hex(c){c=c.replace('#','');return[parseInt(c.substr(0,2),16),parseInt(c.substr(2,2),16),parseInt(c.substr(4,2),16)];}
function rgb(a){return 'rgb('+a.map(function(v){return Math.round(clamp(v,0,255));}).join(',')+')';}
function mix(c1,c2,t){var a=hex(c1),b=hex(c2);return rgb([lerp(a[0],b[0],t),lerp(a[1],b[1],t),lerp(a[2],b[2],t)]);}
function shade(c,k){var a=hex(c);return rgb([a[0]*k,a[1]*k,a[2]*k]);}
function rad(d){return d*Math.PI/180;}
function seg(h,sel,cb){var bs=ctl(h).querySelectorAll(sel);bs.forEach(function(b){b.addEventListener('click',function(){bs.forEach(function(x){x.classList.remove('on');});b.classList.add('on');cb(b);});});}
function rng(seed){var s=seed>>>0||1;return function(){s=(s*1664525+1013904223)>>>0;return s/4294967296;};}
function onIn(inp,f){inp.addEventListener('input',f);}
function svgPt(s,e){var m=s.getScreenCTM().inverse();var q=s.createSVGPoint();q.x=e.clientX;q.y=e.clientY;return q.matrixTransform(m);}

/* ---------- 캐릭터 얼굴(가슴 위) 그리기 — 캔버스 ---------- */
var CH={
 haru:{hair:'#E9909A',hair2:'#D9707E',streak:'#1E2F5C',buns:true,ahoge:true,eye:'#3D8BE0',skin:'#F6D3B8',outfit:'hoodie',long:true},
 sia:{hair:'#1E1B22',hair2:'#4A4656',eye:'#7A7680',skin:'#F6D9C4',outfit:'maid',long:true,earring:true},
 moa:{hair:'#D8C09A',hair2:'#B89C74',eye:'#B07A3E',skin:'#F8DCC8',outfit:'cardigan',long:true,headband:true,ribbon:'L',wavy:true}
};
function cfg(name,over){var o={};var b=CH[name];for(var k in b)o[k]=b[k];for(var j in over)o[j]=over[j];return o;}
function drawBust(ctx,W,H,o){
  var cx=W/2,s=W/200;ctx.save();ctx.clearRect(0,0,W,H);ctx.fillStyle=o.bg||'#f4f6f9';ctx.fillRect(0,0,W,H);
  var ln=o.line||2.2*s;ctx.lineJoin='round';ctx.lineCap='round';ctx.strokeStyle=o.ink||'#2a2230';ctx.lineWidth=ln;
  function E(x,y,rx,ry,fill,stroke){ctx.beginPath();ctx.ellipse(x,y,rx,ry,0,0,Math.PI*2);if(fill){ctx.fillStyle=fill;ctx.fill();}if(stroke!==false)ctx.stroke();}
  // 뒷머리
  if(o.long){ctx.fillStyle=o.hair;ctx.beginPath();ctx.moveTo(cx-48*s,78*s);ctx.quadraticCurveTo(cx-62*s,150*s,cx-52*s,200*s);ctx.lineTo(cx+52*s,200*s);ctx.quadraticCurveTo(cx+62*s,150*s,cx+48*s,78*s);ctx.closePath();ctx.fill();ctx.stroke();}
  else{ctx.fillStyle=o.hair;ctx.beginPath();ctx.moveTo(cx-46*s,80*s);ctx.quadraticCurveTo(cx-50*s,120*s,cx-36*s,128*s);ctx.lineTo(cx+36*s,128*s);ctx.quadraticCurveTo(cx+50*s,120*s,cx+46*s,80*s);ctx.closePath();ctx.fill();ctx.stroke();}
  // 몸·옷
  var body=o.outfit==='maid'?'#34363F':o.outfit==='cardigan'?'#D4B48A':o.outfit==='generic'?'#8a93a6':'#A99AC8';
  ctx.fillStyle=body;ctx.beginPath();ctx.moveTo(cx-70*s,200*s);ctx.quadraticCurveTo(cx-66*s,150*s,cx-26*s,140*s);ctx.lineTo(cx+26*s,140*s);ctx.quadraticCurveTo(cx+66*s,150*s,cx+70*s,200*s);ctx.closePath();ctx.fill();ctx.stroke();
  if(o.outfit==='hoodie'&&o.coat!==false){ctx.fillStyle='#fbfbfd';ctx.beginPath();ctx.moveTo(cx-70*s,200*s);ctx.quadraticCurveTo(cx-66*s,150*s,cx-30*s,141*s);ctx.lineTo(cx-18*s,200*s);ctx.closePath();ctx.fill();ctx.stroke();ctx.beginPath();ctx.moveTo(cx+70*s,200*s);ctx.quadraticCurveTo(cx+66*s,150*s,cx+30*s,141*s);ctx.lineTo(cx+18*s,200*s);ctx.closePath();ctx.fill();ctx.stroke();
    ctx.strokeStyle='#ffffff';ctx.beginPath();ctx.moveTo(cx-8*s,150*s);ctx.lineTo(cx-10*s,175*s);ctx.moveTo(cx+8*s,150*s);ctx.lineTo(cx+10*s,175*s);ctx.stroke();ctx.strokeStyle=o.ink||'#2a2230';}
  if(o.outfit==='maid'){ctx.fillStyle='#fbfbfd';ctx.fillRect(cx-16*s,136*s,32*s,12*s);ctx.strokeRect(cx-16*s,136*s,32*s,12*s);ctx.fillStyle='#8C8C94';E(cx-12*s,154*s,12*s,8*s,'#8C8C94');E(cx+12*s,154*s,12*s,8*s,'#8C8C94');E(cx,154*s,5*s,5*s,'#77777f');
    ctx.fillStyle='#F4F2EE';ctx.beginPath();ctx.moveTo(cx-30*s,200*s);ctx.lineTo(cx-24*s,172*s);ctx.lineTo(cx+24*s,172*s);ctx.lineTo(cx+30*s,200*s);ctx.closePath();ctx.fill();ctx.stroke();}
  if(o.outfit==='cardigan'){ctx.fillStyle='#ffffff';ctx.beginPath();ctx.moveTo(cx-18*s,142*s);ctx.lineTo(cx,175*s);ctx.lineTo(cx+18*s,142*s);ctx.closePath();ctx.fill();ctx.stroke();ctx.fillStyle='#A8323C';ctx.beginPath();ctx.moveTo(cx,150*s);ctx.lineTo(cx-12*s,144*s);ctx.lineTo(cx-12*s,158*s);ctx.closePath();ctx.moveTo(cx,150*s);ctx.lineTo(cx+12*s,144*s);ctx.lineTo(cx+12*s,158*s);ctx.closePath();ctx.fill();ctx.stroke();
    ctx.fillStyle='#FAF8F4';ctx.beginPath();ctx.moveTo(cx-34*s,200*s);ctx.lineTo(cx-28*s,178*s);ctx.lineTo(cx+28*s,178*s);ctx.lineTo(cx+34*s,200*s);ctx.closePath();ctx.fill();ctx.stroke();}
  // 목·얼굴
  ctx.fillStyle=o.skin;ctx.fillRect(cx-11*s,118*s,22*s,24*s);ctx.beginPath();ctx.moveTo(cx-11*s,118*s);ctx.lineTo(cx-11*s,140*s);ctx.moveTo(cx+11*s,118*s);ctx.lineTo(cx+11*s,140*s);ctx.stroke();
  ctx.beginPath();ctx.moveTo(cx-38*s,70*s);ctx.quadraticCurveTo(cx-40*s,112*s,cx,128*s);ctx.quadraticCurveTo(cx+40*s,112*s,cx+38*s,70*s);ctx.closePath();ctx.fillStyle=o.skin;ctx.fill();ctx.stroke();
  // 눈
  [-1,1].forEach(function(d){var ex=cx+d*17*s,ey=96*s;E(ex,ey,8.5*s,10.5*s,'#ffffff');E(ex,ey+1*s,6.5*s,8.5*s,o.eye,false);E(ex,ey+2*s,3.4*s,4.6*s,shade(o.eye,0.45),false);E(ex-2.4*s,ey-3*s,2.2*s,2.2*s,'#ffffff',false);
    ctx.beginPath();ctx.moveTo(ex-10*s,ey-10*s);ctx.quadraticCurveTo(ex,ey-14*s,ex+10*s,ey-9*s);ctx.lineWidth=ln*1.4;ctx.stroke();ctx.lineWidth=ln;});
  ctx.beginPath();ctx.moveTo(cx-5*s,116*s);ctx.quadraticCurveTo(cx,119*s,cx+5*s,116*s);ctx.stroke();
  if(o.blush!==false){ctx.fillStyle='rgba(240,120,130,.25)';E(cx-26*s,108*s,6*s,3*s,'rgba(240,120,130,.25)',false);E(cx+26*s,108*s,6*s,3*s,'rgba(240,120,130,.25)',false);}
  // 앞머리
  ctx.fillStyle=o.hair;ctx.beginPath();ctx.moveTo(cx-46*s,88*s);ctx.quadraticCurveTo(cx-50*s,34*s,cx,30*s);ctx.quadraticCurveTo(cx+50*s,34*s,cx+46*s,88*s);
  if(o.wavy){ctx.quadraticCurveTo(cx+30*s,76*s,cx+22*s,82*s);ctx.quadraticCurveTo(cx+10*s,72*s,cx,80*s);ctx.quadraticCurveTo(cx-10*s,72*s,cx-22*s,82*s);ctx.quadraticCurveTo(cx-30*s,76*s,cx-46*s,88*s);}
  else{ctx.lineTo(cx+36*s,74*s);ctx.lineTo(cx+24*s,84*s);ctx.lineTo(cx+12*s,72*s);ctx.lineTo(cx,84*s);ctx.lineTo(cx-12*s,72*s);ctx.lineTo(cx-24*s,84*s);ctx.lineTo(cx-36*s,74*s);}
  ctx.closePath();ctx.fill();ctx.stroke();
  ctx.strokeStyle=o.hair2;ctx.beginPath();ctx.moveTo(cx-30*s,44*s);ctx.quadraticCurveTo(cx-20*s,40*s,cx-10*s,46*s);ctx.stroke();ctx.strokeStyle=o.ink||'#2a2230';
  if(o.streak){ctx.fillStyle=o.streak;ctx.beginPath();ctx.moveTo(cx-6*s,31*s);ctx.lineTo(cx+6*s,31*s);ctx.lineTo(cx+5*s,80*s);ctx.lineTo(cx,84*s);ctx.lineTo(cx-5*s,80*s);ctx.closePath();ctx.fill();
    ctx.fillRect(cx-46*s+4*s,100*s,6*s,70*s);ctx.fillRect(cx+46*s-10*s,100*s,6*s,70*s);}
  if(o.buns){E(cx-30*s,30*s,15*s,14*s,o.hair);E(cx+30*s,30*s,15*s,14*s,o.hair);ctx.strokeStyle=o.hair2;ctx.beginPath();ctx.arc(cx-30*s,30*s,8*s,3.6,5.6);ctx.stroke();ctx.beginPath();ctx.arc(cx+30*s,30*s,8*s,3.6,5.6);ctx.stroke();ctx.strokeStyle=o.ink||'#2a2230';}
  if(o.ahoge){ctx.beginPath();ctx.moveTo(cx+2*s,30*s);ctx.quadraticCurveTo(cx+14*s,12*s,cx+4*s,8*s);ctx.lineWidth=ln*1.2;ctx.strokeStyle=o.hair2;ctx.stroke();ctx.lineWidth=ln;ctx.strokeStyle=o.ink||'#2a2230';}
  if(o.headband){ctx.fillStyle='#ffffff';ctx.beginPath();ctx.ellipse(cx,38*s,44*s,12*s,0,Math.PI*1.05,Math.PI*1.95);ctx.lineWidth=7*s;ctx.strokeStyle='#ffffff';ctx.stroke();ctx.lineWidth=ln;ctx.strokeStyle=o.ink||'#2a2230';
    for(var i=-3;i<=3;i++){E(cx+i*11*s,27*s+Math.abs(i)*2.2*s,4.5*s,4*s,'#ffffff');}}
  if(o.ribbon){var side=o.ribbon==='L'?1:-1;var rx=cx+side*44*s,ry=60*s;ctx.fillStyle='#ffffff';ctx.beginPath();ctx.moveTo(rx,ry);ctx.lineTo(rx-10*s,ry-7*s);ctx.lineTo(rx-10*s,ry+7*s);ctx.closePath();ctx.moveTo(rx,ry);ctx.lineTo(rx+10*s,ry-7*s);ctx.lineTo(rx+10*s,ry+7*s);ctx.closePath();ctx.fill();ctx.stroke();}
  if(o.earring){ctx.fillStyle='#c9ccd6';E(cx-39*s,108*s,2.5*s,4*s,'#c9ccd6');E(cx+39*s,108*s,2.5*s,4*s,'#c9ccd6');}
  ctx.restore();
}
function pixelate(src,dst,block){var W=dst.width,H=dst.height,ctx=dst.getContext('2d');if(block<=1){ctx.imageSmoothingEnabled=true;ctx.drawImage(src,0,0,W,H);return;}
  var t=document.createElement('canvas');t.width=Math.max(1,Math.round(W/block));t.height=Math.max(1,Math.round(H/block));var tc=t.getContext('2d');tc.imageSmoothingEnabled=true;tc.drawImage(src,0,0,t.width,t.height);
  ctx.imageSmoothingEnabled=false;ctx.clearRect(0,0,W,H);ctx.drawImage(t,0,0,W,H);ctx.imageSmoothingEnabled=true;}
function offBust(name,over,W){var c=document.createElement('canvas');c.width=W||200;c.height=W||200;drawBust(c.getContext('2d'),c.width,c.height,cfg(name,over||{}));return c;}

/* ---------- 3D 도형 마네킹 ---------- */
function limb(a,b,t,part){var dx=b[0]-a[0],dy=b[1]-a[1];return {c:[(a[0]+b[0])/2,(a[1]+b[1])/2,(a[2]+b[2])/2],s:[t,Math.hypot(dx,dy),t*0.95],rz:Math.atan2(dx,dy)*-1,part:part,ends:[a,b]};}
function mannequin(pose){pose=pose||'hip';
  var B=[];function box(c,s,part){B.push({c:c,s:s,rz:0,part:part});}
  box([0,7.45,0],[0.82,1.0,0.88],'head');box([0,6.78,0],[0.32,0.36,0.32],'neck');box([0,5.95,0],[1.6,1.45,1.0],'chest');box([0,4.62,0],[1.36,1.15,0.85],'pelvis');
  var L=[0.96,6.5,0],R=[-0.96,6.5,0];
  var le=[1.12,5.0,0],lh=[1.18,3.65,0.05];
  var re,rh;if(pose==='up'){re=[-1.15,8.0,0];rh=[-1.2,9.4,0];le=[1.15,8.0,0];lh=[1.2,9.4,0];}else{re=[-1.55,5.35,-0.1];rh=[-0.82,4.75,0.15];}
  B.push(limb(L,le,0.36,'uarm'));B.push(limb(le,lh,0.3,'farm'));B.push(limb(R,re,0.36,'uarm'));B.push(limb(re,rh,0.3,'farm'));
  [0.38,-0.38].forEach(function(x){var hp=[x,4.15,0],kn=[x*1.05,2.2,0.05],an=[x*1.08,0.35,0];B.push(limb(hp,kn,0.5,'thigh'));B.push(limb(kn,an,0.38,'shin'));box([x*1.08,0.14,0.18],[0.34,0.28,0.7],'foot');});
  B.joints={head:[0,7.45,0],neck:[0,6.6,0],ls:L,rs:R,le:le,lh:lh,re:re,rh:rh,lp:[0.38,4.15,0],rp:[-0.38,4.15,0],lk:[0.4,2.2,0.05],rk:[-0.4,2.2,0.05],la:[0.41,0.35,0],ra:[-0.41,0.35,0]};
  return B;}
var FACES=[[0,1,2,3],[4,5,6,7],[0,1,5,4],[2,3,7,6],[1,2,6,5],[0,3,7,4]];
function boxVerts(b){var w=b.s[0]/2,h=b.s[1]/2,d=b.s[2]/2,c=Math.cos(b.rz),s=Math.sin(b.rz);
  var L=[[-w,-h,-d],[w,-h,-d],[w,h,-d],[-w,h,-d],[-w,-h,d],[w,-h,d],[w,h,d],[-w,h,d]];
  return L.map(function(p){var x=p[0]*c-p[1]*s,y=p[0]*s+p[1]*c;return[x+b.c[0],y+b.c[1],p[2]+b.c[2]];});}
function rotY(p,a){var c=Math.cos(a),s=Math.sin(a);return[p[0]*c+p[2]*s,p[1],-p[0]*s+p[2]*c];}
function sub3(a,b){return[a[0]-b[0],a[1]-b[1],a[2]-b[2]];}
function cross(a,b){return[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];}
function norm(a){var l=Math.hypot(a[0],a[1],a[2])||1;return[a[0]/l,a[1]/l,a[2]/l];}
function dot(a,b){return a[0]*b[0]+a[1]*b[1]+a[2]*b[2];}
var PARTCOL={head:'#E9909A',neck:'#F6D3B8',chest:'#A99AC8',pelvis:'#5b7fb8',uarm:'#fbfbfd',farm:'#fbfbfd',thigh:'#5b7fb8',shin:'#5b7fb8',foot:'#A99AC8'};
function renderMan(s,o){/* o: yaw, mode(shade|flat|edge|depth|blocks|sketch|line|color), W,H,scale,ox,oy, light */
  var B=mannequin(o.pose),yaw=rad(o.yaw||0),Lt=norm(o.light||[-0.55,0.65,0.55]);
  var sc=o.scale||40,ox=o.ox||o.W/2,oy=o.oy||o.H-20;var polys=[];var zmin=1e9,zmax=-1e9;
  B.forEach(function(b){var V=boxVerts(b).map(function(p){return rotY(p,yaw);});
    FACES.forEach(function(f){var a=V[f[0]],bb=V[f[1]],c=V[f[2]];var n=norm(cross(sub3(bb,a),sub3(c,a)));
      var cen=[0,0,0];f.forEach(function(i){cen[0]+=V[i][0]/4;cen[1]+=V[i][1]/4;cen[2]+=V[i][2]/4;});
      // 바깥쪽 법선으로 맞춤
      var bc=rotY(b.c,yaw);if(dot(n,sub3(cen,bc))<0)n=[-n[0],-n[1],-n[2]];
      if(n[2]<=0.001)return;zmin=Math.min(zmin,cen[2]);zmax=Math.max(zmax,cen[2]);
      polys.push({pts:f.map(function(i){return[ox+V[i][0]*sc,oy-V[i][1]*sc];}),z:cen[2],n:n,part:b.part});});});
  polys.sort(function(a,b){return a.z-b.z;});var g=el('g',{},s);var R=rng(7);
  polys.forEach(function(p){var d=p.pts.map(function(q){return q[0].toFixed(1)+','+q[1].toFixed(1);}).join(' ');
    var br=0.28+0.72*Math.max(0,dot(p.n,Lt));var m=o.mode;
    if(m==='shade')el('polygon',{points:d,fill:mix('#3b3f4a','#eef1f6',br),stroke:'#2a2e38','stroke-width':0.8},g);
    else if(m==='flat')el('polygon',{points:d,fill:o.flat||'#f2d9c6',stroke:o.flat||'#f2d9c6','stroke-width':0.6},g);
    else if(m==='blocks')el('polygon',{points:d,fill:'none',stroke:C.blue,'stroke-width':1.3},g);
    else if(m==='sketch'){var q=p.pts.map(function(v){return[v[0]+(R()-.5)*3,v[1]+(R()-.5)*3];});el('polygon',{points:q.map(function(v){return v[0].toFixed(1)+','+v[1].toFixed(1);}).join(' '),fill:'none',stroke:'#8a8f99','stroke-width':1,opacity:.85},g);}
    else if(m==='line')el('polygon',{points:d,fill:'#ffffff',stroke:'#1d1a22','stroke-width':1.4},g);
    else if(m==='color'){var A=hex(PARTCOL[p.part]||'#dddddd');el('polygon',{points:d,fill:rgb(A.map(function(v){return v*(0.6+0.4*br);})),stroke:'#1d1a22','stroke-width':1.2},g);}
    else if(m==='edge')el('polygon',{points:d,fill:'#000',stroke:'#fff','stroke-width':1.1},g);
    else if(m==='depth'){var t=(p.z-zmin)/Math.max(1e-6,zmax-zmin);var v=Math.round(70+t*185);el('polygon',{points:d,fill:'rgb('+v+','+v+','+v+')',stroke:'rgb('+v+','+v+','+v+')','stroke-width':0.6},g);}
  });
  var J={};for(var k in B.joints){var r=rotY(B.joints[k],yaw);J[k]=[ox+r[0]*sc,oy-r[1]*sc,r[2]];}
  return {g:g,J:J};}

/* ===================== 1부 ===================== */
/* ===================== 3부: 천 시뮬레이션 ===================== */
function Cloth(nx,ny,sp){this.nx=nx;this.ny=ny;this.sp=sp;this.p=[];this.o=[];this.pin={};var r=rng(3);
  for(var j=0;j<ny;j++)for(var i=0;i<nx;i++){var v=[(i-(nx-1)/2)*sp,-j*sp,(r()-.5)*0.6];this.p.push(v.slice());this.o.push(v.slice());}}
Cloth.prototype.idx=function(i,j){return j*this.nx+i;};
Cloth.prototype.step=function(g,stiff,wind){var n=this.p.length,k,p,o;for(k=0;k<n;k++){if(this.pin[k])continue;p=this.p[k];o=this.o[k];var vx=(p[0]-o[0])*0.985,vy=(p[1]-o[1])*0.985,vz=(p[2]-o[2])*0.985;o[0]=p[0];o[1]=p[1];o[2]=p[2];p[0]+=vx+(wind||0);p[1]+=vy-g;p[2]+=vz;}
  var nx=this.nx,ny=this.ny,sp=this.sp,self=this;
  function sat(a,b,rest,w){var A=self.p[a],B=self.p[b];var dx=B[0]-A[0],dy=B[1]-A[1],dz=B[2]-A[2];var d=Math.sqrt(dx*dx+dy*dy+dz*dz)||1e-6;var df=(d-rest)/d*0.5*w;var pa=self.pin[a]?0:1,pb=self.pin[b]?0:1;if(!pa&&!pb)return;var s2=pa&&pb?1:2;
    if(pa){A[0]+=dx*df*s2;A[1]+=dy*df*s2;A[2]+=dz*df*s2;}if(pb){B[0]-=dx*df*s2;B[1]-=dy*df*s2;B[2]-=dz*df*s2;}}
  for(var it=0;it<6;it++){for(var j=0;j<ny;j++)for(var i=0;i<nx;i++){var a=this.idx(i,j);if(i<nx-1)sat(a,a+1,sp,1);if(j<ny-1)sat(a,a+nx,sp,1);if(i<nx-1&&j<ny-1){sat(a,a+nx+1,sp*1.41421,0.9);sat(a+1,a+nx,sp*1.41421,0.9);}
      if(stiff>0){if(i<nx-2)sat(a,a+2,2*sp,stiff);if(j<ny-2)sat(a,a+2*nx,2*sp,stiff);}}
    for(var key in this.pin){var q=this.pin[key];this.p[key][0]=q[0];this.p[key][1]=q[1];this.p[key][2]=q[2];}}};
Cloth.prototype.draw=function(ctx,W,H,sc,ox,oy){ctx.fillStyle='#fbfcfd';ctx.fillRect(0,0,W,H);var L=norm([-0.5,0.55,0.7]);var nx=this.nx,ny=this.ny,quads=[];
  for(var j=0;j<ny-1;j++)for(var i=0;i<nx-1;i++){var a=this.p[this.idx(i,j)],b=this.p[this.idx(i+1,j)],c=this.p[this.idx(i+1,j+1)],d=this.p[this.idx(i,j+1)];var n=norm(cross(sub3(b,a),sub3(d,a)));if(n[2]<0)n=[-n[0],-n[1],-n[2]];quads.push({q:[a,b,c,d],z:(a[2]+b[2]+c[2]+d[2])/4,n:n});}
  quads.sort(function(a,b){return a.z-b.z;});quads.forEach(function(Q){var br=0.25+0.75*Math.max(0,dot(Q.n,L));ctx.fillStyle=mix('#4a5470','#eef0f8',br);ctx.beginPath();Q.q.forEach(function(v,k){var X=ox+v[0]*sc,Y=oy-v[1]*sc;if(k)ctx.lineTo(X,Y);else ctx.moveTo(X,Y);});ctx.closePath();ctx.fill();ctx.strokeStyle='rgba(40,46,60,.18)';ctx.lineWidth=0.6;ctx.stroke();});
  for(var key in this.pin){var v=this.p[key];ctx.fillStyle='#8c8f9a';ctx.beginPath();ctx.arc(ox+v[0]*sc,oy-v[1]*sc,7,0,7);ctx.fill();ctx.strokeStyle='#2a2e38';ctx.lineWidth=1.5;ctx.stroke();}};
Cloth.prototype.folds=function(){var j=Math.floor(this.ny*0.6),c=0,prev=0;for(var i=1;i<this.nx-1;i++){var dz=this.p[this.idx(i+1,j)][2]-this.p[this.idx(i-1,j)][2];var sgn=dz>0.15?1:dz<-0.15?-1:0;if(sgn&&prev&&sgn!==prev)c++;if(sgn)prev=sgn;}return c;};
Cloth.prototype.sag=function(){var j=0,mid=this.p[this.idx(Math.floor(this.nx/2),0)];var top=Math.max.apply(null,Object.keys(this.pin).map(function(k){return this.p[k][1];},this));return top-mid[1];};
function runCloth(h,setup,opts){var W=520,H=400;var cv=canvasOf(h,W,H),ctx=cv.getContext('2d');var cl,raf=null,frames=0,grab=null;
  function reset(){cl=new Cloth(19,15,1);setup(cl);frames=0;loop();}
  function tick(){var o=opts();for(var k=0;k<2;k++)cl.step(o.g,o.stiff,o.wind||0);if(grab)cl.pin[grab.k]=grab.pos;}
  function render(){cl.draw(ctx,W,H,18,W/2,60);var o=opts();if(o.report)o.report(cl);}
  function loop(){if(raf)cancelAnimationFrame(raf);if(RM){for(var i=0;i<220;i++)tick();render();return;}
    (function f(){tick();frames++;render();if(frames<260||grab)raf=requestAnimationFrame(f);else raf=null;})();}
  function pos(e){var r=cv.getBoundingClientRect();return[((e.clientX-r.left)*W/r.width-W/2)/18,-((e.clientY-r.top)*H/r.height-60)/18];}
  cv.addEventListener('pointerdown',function(e){var q=pos(e),best=-1,bd=4;cl.p.forEach(function(v,k){var d=Math.hypot(v[0]-q[0],v[1]-q[1]);if(d<bd&&!cl.pin[k]){bd=d;best=k;}});if(best>=0){grab={k:best,pos:[q[0],q[1],cl.p[best][2]]};cv.setPointerCapture&&cv.setPointerCapture(e.pointerId);loop();}});
  cv.addEventListener('pointermove',function(e){if(!grab)return;var q=pos(e);grab.pos=[q[0],q[1],grab.pos[2]];});
  cv.addEventListener('pointerup',function(){if(grab){delete cl.pin[grab.k];grab=null;frames=0;loop();}});
  reset();return {reset:reset,get:function(){return cl;}};}
function pinMode(cl,m){var nx=cl.nx,sp=cl.sp,i;cl.pin={};function pin(i,j,pos){var k=cl.idx(i,j);cl.pin[k]=pos||cl.p[k].slice();cl.p[k]=cl.pin[k].slice();cl.o[k]=cl.pin[k].slice();}
  if(m===1)pin(Math.floor(nx/2),0);
  if(m===2){pin(0,0,[-(nx-1)/2*sp*0.7,0,0]);pin(nx-1,0,[(nx-1)/2*sp*0.7,0,0]);}
  if(m===3){pin(0,0,[-(nx-1)/2*sp*0.7,0,0]);pin(nx-1,0,[(nx-1)/2*sp*0.7,-6,0]);}
  if(m===4){for(i=0;i<nx;i++){pin(i,0,[(i-(nx-1)/2)*sp*0.42,0,(i%2?0.35:-0.35)]);}}}

/* ---------- 02 실천편 공용 ---------- */
function fig(s,o){/* 단순 인물(앞모습) — o.pose: hip | up */
  var g=el('g',{},s),SK='#f6d3b8',HD='#a99ac8',PT='#5b6f9a',INK='#2a2230';
  function limb(pts,w,c){el('polyline',{points:pts.map(function(p){return p.join(',');}).join(' '),fill:'none',stroke:INK,'stroke-width':w+3,'stroke-linecap':'round','stroke-linejoin':'round'},g);el('polyline',{points:pts.map(function(p){return p.join(',');}).join(' '),fill:'none',stroke:c,'stroke-width':w,'stroke-linecap':'round','stroke-linejoin':'round'},g);}
  limb([[150,262],[142,370],[140,488]],40,PT);limb([[205,262],[222,375],[205,488]],40,PT);
  el('rect',{x:118,y:480,width:42,height:18,rx:8,fill:'#ddd6ee',stroke:INK},g);el('rect',{x:186,y:480,width:42,height:18,rx:8,fill:'#ddd6ee',stroke:INK},g);
  if(o.pose==='up'){limb([[130,128],[112,72],[118,20]],28,HD);}else limb([[130,128],[112,232],[108,318]],28,HD);
  el('path',{d:'M128 118 Q180 104 232 118 L244 262 Q180 274 116 262 Z',fill:HD,stroke:INK,'stroke-width':2.2},g);
  el('line',{x1:180,y1:116,x2:180,y2:266,stroke:'#fbfbfd','stroke-width':3},g);
  el('rect',{x:116,y:244,width:128,height:22,rx:6,fill:'#9b8cc0',stroke:INK,'stroke-width':1.6},g);
  if(o.pose==='up')limb([[230,128],[262,72],[244,26]],28,HD);else limb([[230,128],[276,200],[238,250]],28,HD);
  el('rect',{x:168,y:88,width:24,height:26,fill:SK,stroke:INK,'stroke-width':1.6},g);
  el('circle',{cx:180,cy:62,r:32,fill:SK,stroke:INK,'stroke-width':2.2},g);
  el('path',{d:'M146 62 Q150 22 180 26 Q212 22 214 62 Q206 40 180 42 Q156 40 146 62Z',fill:'#e9909a',stroke:INK,'stroke-width':1.6},g);
  el('circle',{cx:160,cy:24,r:10,fill:'#e9909a',stroke:INK,'stroke-width':1.4},g);el('circle',{cx:200,cy:24,r:10,fill:'#e9909a',stroke:INK,'stroke-width':1.4},g);
  [166,194].forEach(function(x){el('ellipse',{cx:x,cy:66,rx:5,ry:7,fill:'#3d8be0',stroke:INK,'stroke-width':1.2},g);});el('path',{d:'M172 84 Q180 89 188 84',fill:'none',stroke:INK,'stroke-width':1.6},g);
  return g;}
function wave(x0,x1,y,amp,len,ph){var d='',n=Math.max(8,Math.round(Math.abs(x1-x0)/2));for(var i=0;i<=n;i++){var x=x0+(x1-x0)*i/n;d+=(i?'L':'M')+x.toFixed(1)+','+(y+amp*Math.sin(2*Math.PI*(x-x0)/len+(ph||0))).toFixed(1);}return d;}
function sineAmp(ratio,w){/* 한 물결(폭 w)에 든 천 = ratio·w 가 되는 사인 진폭 */
  if(ratio<=1.0001)return 0;function L(A){var n=200,s=0,k=2*Math.PI/w;for(var i=0;i<n;i++){var x=(i+0.5)*w/n;var d=A*k*Math.cos(k*x);s+=Math.sqrt(1+d*d)*w/n;}return s;}
  var lo=0,hi=w*ratio;for(var it=0;it<50;it++){var m=(lo+hi)/2;if(L(m)<ratio*w)lo=m;else hi=m;}return (lo+hi)/2;}
window.__lab2={sineAmp:sineAmp};
function clothCount(cl,j){var c=0,prev=0;for(var i=1;i<cl.nx-1;i++){var dz=cl.p[cl.idx(i+1,j)][2]-cl.p[cl.idx(i-1,j)][2];var sg=dz>0.12?1:dz<-0.12?-1:0;if(sg&&prev&&sg!==prev)c++;if(sg)prev=sg;}return c;}
function pinAt(cl,i,j,pos){var k=cl.idx(i,j);cl.pin[k]=pos.slice();cl.p[k]=pos.slice();cl.o[k]=pos.slice();}

/* ===================== 1부 · 서 있는 자세 ===================== */
P.p1_contacts=function(h){var W=360,H=520,found={},hint=false,miss=[];
  var SP=[{k:'sh',xy:[[140,116],[222,116]],t:'어깨 꼭대기 — 옷 전체가 여기에 걸려 있다'},{k:'ch',xy:[[180,152]],t:'가슴 위 — 가장 앞으로 나온 곳에 천이 얹힌다'},
          {k:'hd',xy:[[240,250]],t:'허리에 얹은 손 — 손이 천을 누른다'},{k:'el',xy:[[276,200]],t:'굽힌 팔꿈치 — 바깥쪽 천이 당겨진다'},{k:'kn',xy:[[222,374]],t:'앞으로 나온 무릎 — 바지가 걸린다'}];
  function draw(){var s=svgOf(h,W,H);s.style.maxWidth='400px';s.style.display='block';s.style.margin='0 auto';el('rect',{x:0,y:0,width:W,height:H,fill:'#fbfcfd'},s);fig(s,{pose:'hip'});
    SP.forEach(function(p){p.xy.forEach(function(q){if(found[p.k])el('circle',{cx:q[0],cy:q[1],r:16,fill:'rgba(232,115,26,.18)',stroke:C.orange,'stroke-width':3},s);else if(hint)el('circle',{cx:q[0],cy:q[1],r:16,fill:'none',stroke:C.orange,'stroke-width':1.5,'stroke-dasharray':'4 4',opacity:.7},s);});});
    miss.forEach(function(q){el('text',{x:q[0],y:q[1]+5,'text-anchor':'middle','font-size':18,fill:C.red,'font-family':KFONT},s).textContent='×';});
    var n=Object.keys(found).length;ktxt(s,12,22,'찾은 접점 '+n+' / 5',{size:15,fill:C.navy,weight:'bold'});
    s.addEventListener('click',function(e){var q=svgPt(s,e),hit=null;SP.forEach(function(p){p.xy.forEach(function(c){if(Math.hypot(c[0]-q.x,c[1]-q.y)<26)hit=p;});});
      if(hit){found[hit.k]=1;out(h).innerHTML='<b>'+hit.t+'</b>'+(Object.keys(found).length===5?' · 다섯 곳을 모두 찾았습니다. 주름은 모두 이 점들에서 출발합니다.':'');}
      else{miss.push([q.x,q.y]);if(miss.length>6)miss.shift();out(h).innerHTML='여기는 천이 덮여 있을 뿐 걸리거나 붙잡히지 않았습니다. 볼록한 곳·눌린 곳·굽은 곳을 찾아보세요.';}draw();});}
  ctl(h).querySelectorAll('button').forEach(function(b){b.addEventListener('click',function(){if(b.dataset.a==='hint')hint=!hint;else{found={};miss=[];hint=false;out(h).innerHTML='그림을 눌러 접점을 찾아보세요.';}draw();});});
  out(h).innerHTML='그림을 눌러 접점을 찾아보세요. 어깨는 왼쪽·오른쪽 중 하나만 눌러도 됩니다.';draw();};

P.p1_bend=function(h){var ins=ctl(h).querySelectorAll('input'),W=560,H=360;
  function draw(){var a=+ins[0].value,t=+ins[1].value,th=rad(a),px=7;var s=svgOf(h,W,H);el('rect',{x:0,y:0,width:W,height:H,fill:'#fbfcfd'},s);
    var J=[270,230],L1=200,L2=170;/* 위팔은 왼쪽으로, 아래팔은 위로 접힘 */
    var A=[J[0]-L1,J[1]],B=[J[0]+L2*Math.cos(-th),J[1]+L2*Math.sin(-th)];
    var tw=t*px;el('polyline',{points:[A,J,B].map(function(p){return p.join(',');}).join(' '),fill:'none',stroke:'#2a2230','stroke-width':tw+4,'stroke-linejoin':'round','stroke-linecap':'round'},s);
    el('polyline',{points:[A,J,B].map(function(p){return p.join(',');}).join(' '),fill:'none',stroke:'#c9bfe2','stroke-width':tw,'stroke-linejoin':'round','stroke-linecap':'round'},s);
    var diff=t*th;/* 바깥(아래·오른쪽) 당김선, 안쪽(위·왼쪽) 모임 주름 */
    var ro=tw/2-4;if(a>0){el('path',{d:'M'+(J[0]-60)+','+(J[1]+ro)+' L'+J[0]+','+(J[1]+ro),stroke:C.red,'stroke-width':3,fill:'none'},s);
      var bx=J[0]+ro*Math.sin(th),by=J[1]+ro*Math.cos(th);el('line',{x1:J[0],y1:J[1]+ro,x2:bx+60*Math.cos(-th),y2:by+60*Math.sin(-th),stroke:C.red,'stroke-width':3},s);
      var nz=Math.min(9,Math.round(diff/2.5));for(var k=0;k<nz;k++){var ux=Math.cos(Math.PI-th/2+(k-(nz-1)/2)*0.25),uy=-Math.sin(Math.PI-th/2+(k-(nz-1)/2)*0.25);el('line',{x1:J[0]+ux*(tw/2-12),y1:J[1]+uy*(tw/2-12),x2:J[0]+ux*(tw/2+4),y2:J[1]+uy*(tw/2+4),stroke:C.blue,'stroke-width':2.5},s);}}
    ktxt(s,14,24,'빨강 = 바깥 당김 주름 · 파랑 = 안쪽 모임 주름',{size:13,fill:C.navy});
    var bw=Math.min(240,diff*8);el('rect',{x:20,y:H-46,width:bw,height:16,fill:C.orange,rx:3},s);ktxt(s,24+bw,H-33,'바깥 − 안쪽 = '+f2(diff,1)+'cm',{size:13,fill:C.ink});
    out(h).innerHTML='굽힌 각 <b>'+a+'°</b> = '+f2(th,3)+'라디안 · 두께 '+t+'cm → 바깥과 안쪽 길이 차 <b>'+t+' × '+f2(th,3)+' = '+f2(diff,1)+'cm</b>'+(a===0?' · 편 팔이라 남는 천이 없습니다.':diff>10?' · 안쪽에 남는 천이 많아 모임 주름이 겹칩니다.':' · 안쪽에 짧은 모임 주름 몇 개.');}
  ins.forEach(function(i){onIn(i,draw);});draw();};

P.p1_peak=function(h){var W=360,H=380,pk=[175,190],drag=false;var chk=ctl(h).querySelectorAll('input');
  var AN=[[105,52,'왼쪽 어깨'],[250,52,'오른쪽 어깨'],[282,128,'겨드랑이'],[262,330,'허리 손']];
  function draw(){var s=svgOf(h,W,H);s.style.maxWidth='400px';s.style.display='block';s.style.margin='0 auto';el('rect',{x:0,y:0,width:W,height:H,fill:'#fbfcfd'},s);
    el('path',{d:'M90 40 Q180 24 270 40 L300 140 L290 350 Q180 366 70 350 L60 140 Z',fill:'#e4def2',stroke:'#2a2230','stroke-width':2},s);
    var on=[];chk.forEach(function(c,i){if(c.checked)on.push(AN[i]);});var R=rng(5);
    on.forEach(function(a){for(var k=-1;k<=1;k++){var mx=(a[0]+pk[0])/2+k*14,my=(a[1]+pk[1])/2+k*10;var nx=-(pk[1]-a[1]),ny=pk[0]-a[0],l=Math.hypot(nx,ny)||1;
        el('path',{d:'M'+(a[0]+k*8)+','+(a[1]+k*6)+' Q'+(mx+nx/l*k*10)+','+(my+ny/l*k*10)+' '+(pk[0]+k*4)+','+(pk[1]+k*4),fill:'none',stroke:C.red,'stroke-width':2.2,opacity:.85},s);}
      el('circle',{cx:a[0],cy:a[1],r:8,fill:'#8c8f9a',stroke:'#2a2230'},s);});
    for(var k=0;k<4;k++){var x=pk[0]-36+k*24;el('path',{d:'M'+x+','+(pk[1]+40)+' q'+(R()*10-5)+',40 '+(R()*8-4)+',90',fill:'none',stroke:C.blue,'stroke-width':2,'stroke-dasharray':'6 4'},s);}
    el('circle',{cx:pk[0],cy:pk[1],r:12,fill:C.orange,stroke:'#2a2230','stroke-width':2,style:'cursor:grab'},s);ktxt(s,pk[0]+16,pk[1]-10,'꼭대기',{size:13,fill:C.orange,weight:'bold'});
    ktxt(s,10,H-10,'빨강 = 당김 주름 · 파랑 점선 = 처짐 주름',{size:11.5});
    s.addEventListener('pointerdown',function(e){var q=svgPt(s,e);if(Math.hypot(q.x-pk[0],q.y-pk[1])<30){drag=true;s.setPointerCapture&&s.setPointerCapture(e.pointerId);}});
    s.addEventListener('pointermove',function(e){if(!drag)return;var q=svgPt(s,e);pk=[clamp(q.x,80,280),clamp(q.y,70,300)];draw();});
    s.addEventListener('pointerup',function(){drag=false;});
    out(h).innerHTML='켜진 접점 <b>'+on.length+'곳</b> → 당김 주름 '+on.length+'방향이 꼭대기로 모입니다.'+(on.length===0?' 접점이 없으면 천은 그냥 처집니다.':' 꼭대기를 옮기면 주름 방향이 따라 돕니다.');}
  chk.forEach(function(c){c.addEventListener('change',draw);});draw();};

P.p1_forms=function(h){var c=ctl(h),inp=c.querySelector('input'),mode=1,W=520,H=340;var cv=canvasOf(h,W,H),ctx=cv.getContext('2d');
  function draw(){var a=+inp.value,L=norm([Math.cos(rad(a)),Math.sin(rad(a)),0.55]);var img=ctx.createImageData(W,H),d=img.data;
    for(var y=0;y<H;y++)for(var x=0;x<W;x++){var i=(y*W+x)*4,col=[251,252,253];var n=null;
      var dx=(x-160)/90,dy=(y-150)/90;if(dx*dx+dy*dy<=1)n=[dx,-dy,Math.sqrt(1-dx*dx-dy*dy)];
      if(!n&&x>=320&&x<=420&&y>=50&&y<=310){var u=(x-370)/50;n=[u,0,Math.sqrt(Math.max(0,1-u*u))];}
      if(n){var base=[201,191,226];var br=dot(n,L);var k=mode===1?(br>0.12?1:0.62):1;col=base.map(function(v){return v*k;});}
      d[i]=col[0];d[i+1]=col[1];d[i+2]=col[2];d[i+3]=255;}
    ctx.putImageData(img,0,0);ctx.strokeStyle='#2a2230';ctx.lineWidth=2;ctx.beginPath();ctx.arc(160,150,90,0,7);ctx.stroke();ctx.strokeRect(320,50,100,260);
    // 주름 그림자: 짧은 진한 획
    var F=[[120,200,150,214],[150,212,186,220],[188,206,214,196],[330,120,352,140],[392,150,414,128],[330,220,354,236],[388,250,412,232]];
    F.forEach(function(f){var mx=(f[0]+f[2])/2,my=(f[1]+f[3])/2;var n2;var ddx=(mx-160)/90,ddy=(my-150)/90;if(ddx*ddx+ddy*ddy<=1)n2=[ddx,-ddy,Math.sqrt(Math.max(0,1-ddx*ddx-ddy*ddy))];else{var u=(mx-370)/50;n2=[u,0,Math.sqrt(Math.max(0,1-u*u))];}
      var lit=dot(n2,L)>0.12;if(mode===0||lit){ctx.strokeStyle=mode===0?'#6a5f8e':'#7d72a3';ctx.lineWidth=5;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(f[0],f[1]);ctx.quadraticCurveTo(mx,my+6,f[2],f[3]);ctx.stroke();}});
    var lx=270+Math.cos(rad(a))*230,ly=170-Math.sin(rad(a))*150;ctx.fillStyle='#ffd34d';ctx.strokeStyle=C.orange;ctx.lineWidth=2;ctx.beginPath();ctx.arc(clamp(lx,16,W-16),clamp(ly,16,H-16),12,0,7);ctx.fill();ctx.stroke();
    ctx.fillStyle=C.navy;ctx.font='13px '+KFONT;ctx.fillText(mode===1?'큰 형체 그림자 먼저 + 밝은 쪽에만 주름 그림자':'주름 그림자만 — 덩어리가 납작',12,22);
    var side=a<80?'왼쪽':a>100?'오른쪽':'아래쪽';out(h).innerHTML=mode===1?'광원 '+a+'° → 큰 그림자는 구·원기둥의 <b>'+side+'</b> 절반. 주름 그림자는 큰 그림자 안에서 생략하고 밝은 쪽에만 남깁니다.':'주름 그림자만 있으면 빛이 어디서 오는지, 덩어리가 둥근지 알 수 없습니다. <b>큰 형체 먼저</b>를 눌러 비교해 보세요.';}
  onIn(inp,draw);seg(h,'button',function(b){mode=+b.dataset.m;draw();});draw();};

P.p1_step=function(h){var ins=ctl(h).querySelectorAll('input'),W=560,H=340;
  function draw(){var hm=+ins[0].value,al=+ins[1].value,len=al>=90?0:hm/Math.tan(rad(al));var s=svgOf(h,W,H);el('rect',{x:0,y:0,width:W,height:H,fill:'#fbfcfd'},s);
    var X=300,top=40,sc=4,stepY=130,hp=hm*sc;/* 옆에서 본 단면: 옷 면은 세로선, 주머니가 왼쪽(빛 쪽)으로 튀어나옴 */
    el('rect',{x:X,y:top,width:40,height:270,fill:'#e4def2',stroke:'#2a2230'},s);el('rect',{x:X-hp,y:stepY-60,width:hp,height:60,fill:'#c9bfe2',stroke:'#2a2230'},s);
    var sl=Math.min(220,len*sc);el('rect',{x:X-6,y:stepY,width:6,height:sl,fill:'#3d3550'},s);
    var vx=Math.sin(rad(al)),vy=Math.cos(rad(al));/* 빛: 면과 al 각, 위에서 아래로 */
    for(var k=-3;k<=2;k++){var ex=X-hp,ey=stepY;var sx=X-hp-vx*200+k*30*vy,sy=stepY-vy*200-k*30*vx;if(k===0){el('line',{x1:ex-vx*220,y1:ey-vy*220,x2:X,y2:stepY+(al>=90?0:hp/Math.tan(rad(al))),stroke:C.orange,'stroke-width':2.4},s);}
      else el('line',{x1:sx,y1:sy,x2:sx+vx*160,y2:sy+vy*160,stroke:'#f3c07a','stroke-width':1.4},s);}
    ktxt(s,X+48,stepY+sl/2+5,'그림자 '+f2(len/10,2)+'cm',{size:14,fill:C.ink,weight:'bold'});ktxt(s,X-hp-4,stepY-66,'단차 '+f2(hm/10,1)+'cm',{size:12.5,anchor:'end'});
    ktxt(s,12,22,'옆에서 본 단면 — 오른쪽 세로 판이 옷 면, 왼쪽으로 튀어나온 것이 주머니',{size:12.5,fill:C.navy});
    // 앞에서 본 작은 그림
    el('rect',{x:420,y:200,width:120,height:110,fill:'#e4def2',stroke:'#2a2230'},s);el('rect',{x:440,y:212,width:80,height:46,fill:'#c9bfe2',stroke:'#2a2230'},s);el('rect',{x:440,y:258,width:80,height:Math.min(46,len*1.2),fill:'#3d3550',opacity:.75},s);ktxt(s,480,328,'앞에서 본 주머니',{size:11.5,anchor:'middle'});
    out(h).innerHTML='그림자 길이 = 단차 '+f2(hm/10,1)+'cm ÷ tan '+al+'°('+(al>=90?'∞':f2(Math.tan(rad(al)),2))+') = <b>'+f2(len/10,2)+'cm</b>'+(al>=90?' · 빛이 면을 정면으로 비춰 그림자가 없습니다.':al<=30?' · 빛이 면을 스치듯 비춰 띠가 길어집니다.':'');}
  ins.forEach(function(i){onIn(i,draw);});draw();};

/* ===================== 2부 · 주름 많은 옷 ===================== */
P.p2_gather=function(h){var ins=ctl(h).querySelectorAll('input'),W=560,H=320,B=60;
  function draw(){var r=+ins[0].value,w=+ins[1].value,A=sineAmp(r,w),n=B/w,sc=8;var s=svgOf(h,W,H);el('rect',{x:0,y:0,width:W,height:H,fill:'#fbfcfd'},s);
    el('rect',{x:40,y:70,width:B*sc,height:16,fill:'#34363f',rx:3},s);ktxt(s,40,62,'꿰맨 띠 60cm',{size:12.5});
    var y0=150;var d=wave(40,40+B*sc,y0,Math.min(60,A*sc),w*sc,0);el('path',{d:d+' L'+(40+B*sc)+','+(y0+80)+' L40,'+(y0+80)+' Z',fill:'#f4f2ee',stroke:'none'},s);el('path',{d:d,fill:'none',stroke:'#2a2230','stroke-width':2.2},s);
    for(var i=0;i<=Math.floor(n);i++){var x=40+i*w*sc;el('line',{x1:x,y1:86,x2:x,y2:y0-Math.min(60,A*sc)-4,stroke:'#cfd5dd','stroke-dasharray':'3 3'},s);}
    el('rect',{x:40,y:270,width:Math.min(480,B*r*sc/3),height:12,fill:C.orange,rx:3},s);ktxt(s,40,262,'펼친 천 길이 '+Math.round(B*r)+'cm (가로 1/3로 줄여 그림)',{size:12});
    ktxt(s,12,22,'위에서 본 프릴 가장자리 — 물결 하나 = 폭 '+w+'cm',{size:13,fill:C.navy});
    out(h).innerHTML='개더 비율 <b>'+f2(r,1)+'</b> · 천 '+Math.round(B*r)+'cm를 60cm 띠에 꿰맴 → 물결 <b>'+f2(n,1)+'개</b>, 물결 하나에 든 천 '+w+' × '+f2(r,1)+' = <b>'+f2(w*r,1)+'cm</b> · 물결 깊이(위아래) 약 <b>'+f2(2*A,1)+'cm</b>'+(r<1.05?' · 남는 천이 없어 평평합니다.':'');}
  ins.forEach(function(i){onIn(i,draw);});draw();};

P.p2_cinch=function(h){var inp=ctl(h).querySelector('input');var MID=7;
  function setup(cl){var c=+inp.value/100;cl.pin={};var nx=cl.nx;for(var i=0;i<nx;i++){pinAt(cl,i,0,[(i-(nx-1)/2)*0.95,0,0]);pinAt(cl,i,MID,[(i-(nx-1)/2)*0.95*(1-c),-MID*0.95,(i%2?0.3:-0.3)*c*2]);}}
  var sim=runCloth(h,setup,function(){return {g:0.012,stiff:0.15,report:function(cl){var a=clothCount(cl,3)+clothCount(cl,4),b=clothCount(cl,10)+clothCount(cl,11);
    out(h).innerHTML='조임 <b>'+inp.value+'%</b> · 끈 위쪽 굴곡 <b>'+a+'</b> · 끈 아래쪽 굴곡 <b>'+b+'</b>'+(+inp.value===0?' — 조이지 않으면 천이 그냥 걸려 있습니다.':' — 조인 선(가운데 고정점 줄)을 향해 위아래에서 모입니다.');}};});
  onIn(inp,function(){sim.reset();});};

P.p2_detail=function(h){var c=ctl(h),inp=c.querySelector('input'),tilt=0,W=520,H=380;
  function draw(){var lv=+inp.value,s=svgOf(h,W,H);el('rect',{x:0,y:0,width:W,height:H,fill:'#fbfcfd'},s);var g=el('g',{transform:'rotate('+(tilt?8:0)+' 260 80)'},s);
    var hem=function(x){return 300+18*Math.sin((x-60)/400*Math.PI);};var big='M200,70 L320,70 Q400,200 460,'+hem(460)+' Q260,330 60,'+hem(60)+' Q120,200 200,70 Z';
    el('path',{d:big,fill:'#34363f',stroke:'#2a2230','stroke-width':2},g);el('path',{d:'M215,90 L305,90 Q360,190 392,280 Q260,300 128,280 Q160,190 215,90Z',fill:'#f4f2ee',stroke:'#2a2230','stroke-width':1.5},g);
    if(lv>=2){for(var k=0;k<5;k++){var x=150+k*55;el('path',{d:'M'+(230+k*15)+',100 Q'+(x+5)+',200 '+x+','+(hem(x)-8),fill:'none',stroke:'#5b5d68','stroke-width':2},g);}
      el('path',{d:wave(130,390,282,6,52,0),fill:'none',stroke:'#2a2230','stroke-width':2},g);}
    if(lv>=3){var d='';for(var x=60;x<=460;x+=2){var y=hem(x)+8+4*Math.sin((x-60)/12*Math.PI);d+=(x===60?'M':'L')+x+','+y.toFixed(1);}el('path',{d:d+' L460,'+(hem(460)+26)+' L60,'+(hem(60)+26)+'Z',fill:'#fbfbfd',stroke:'#2a2230','stroke-width':1.4},g);}
    if(lv>=4){for(var x2=64;x2<=456;x2+=10){el('circle',{cx:x2,cy:hem(x2)+24,r:3.2,fill:'none',stroke:'#8a8f99','stroke-width':1},g);}}
    el('path',{d:big,fill:'none',stroke:C.red,'stroke-width':3,'stroke-dasharray':lv>1?'8 5':''},g);
    if(tilt)el('line',{x1:60,y1:340,x2:460,y2:340,stroke:C.teal,'stroke-dasharray':'4 4'},s);
    ktxt(s,12,22,['단계 1 · 큰 선(종 모양)','단계 2 · 중간 물결 + 큰 주름','단계 3 · 프릴 잔물결','단계 4 · 레이스'][lv-1]+(tilt?' · 큰 선 8° 기울어짐':''),{size:14,fill:C.navy,weight:'bold'});
    out(h).innerHTML=(tilt?'큰 선이 8° 기울어 있으면 단계 '+lv+'까지 자세함을 올려도 치마는 그대로 기울어 보입니다. <b>고칠 곳은 단계 1</b>입니다.':'단계 '+lv+': '+['치마 전체의 종 모양과 기울기가 여기서 정해집니다.','큰 선을 따라 주름과 물결을 더합니다. 덩어리 모양은 그대로입니다.','밑단에 잔물결 프릴을 얹습니다.','마지막으로 레이스 무늬. 빨간 큰 선은 처음과 같습니다.'][lv-1]);}
  onIn(inp,draw);seg(h,'button',function(b){tilt=+b.dataset.t;draw();});draw();};

P.p2_level=function(h){var c=ctl(h),inp=c.querySelector('input'),fixed=0,W=520,H=380,sc=5;
  function draw(){var t=+inp.value,s=svgOf(h,W,H);el('rect',{x:0,y:0,width:W,height:H,fill:'#fbfcfd'},s);var cx=260,cy=210;
    var g=el('g',{transform:'rotate('+(-t)+' '+cx+' '+cy+')'},s);
    el('path',{d:'M170 90 Q260 70 350 90 L340 330 L180 330 Z',fill:'#34363f',stroke:'#2a2230','stroke-width':2},g);el('path',{d:'M215 110 L305 110 L315 330 L205 330Z',fill:'#f4f2ee',stroke:'#2a2230'},g);
    el('circle',{cx:260,cy:70,r:30,fill:'#f6d9c4',stroke:'#2a2230','stroke-width':2},g);
    var pairs=[[[170,92],[350,92],'어깨 프릴',36],[[240,150],[280,150],'단추',8],[[205,230],[315,230],'앞치마 끈',22]];
    function rot(p){var a=rad(-t),x=p[0]-cx,y=p[1]-cy;return [cx+x*Math.cos(a)-y*Math.sin(a),cy+x*Math.sin(a)+y*Math.cos(a)];}
    pairs.forEach(function(pr,k){var a=rot(pr[0]),b=rot(pr[1]);if(fixed){var my=(a[1]+b[1])/2;a=[a[0],my];b=[b[0],my];}
      var r=k===0?16:k===1?7:9,col=k===0?'#fbfbfd':k===1?'#c9c9cf':'#fbfbfd';[a,b].forEach(function(p){el('circle',{cx:p[0],cy:p[1],r:r,fill:col,stroke:'#2a2230','stroke-width':1.6},s);});
      el('line',{x1:a[0]-30,y1:a[1]+(a[1]-b[1])/(b[0]-a[0]||1)*30,x2:b[0]+30,y2:b[1]-(a[1]-b[1])/(b[0]-a[0]||1)*30,stroke:C.red,'stroke-width':2,'stroke-dasharray':'6 4'},s);});
    ktxt(s,12,22,fixed?'수평 고정 — 몸은 기울었는데 장식만 수평':'몸 따라 — 짝을 잇는 선이 모두 나란히 기움',{size:13.5,fill:C.navy,weight:'bold'});
    var tn=Math.tan(rad(Math.abs(t)));out(h).innerHTML='몸의 기울기 <b>'+t+'°</b> (tan = '+f2(tn,3)+') → 어깨 프릴 높이 차 36 × '+f2(tn,3)+' = <b>'+f2(36*tn,1)+'cm</b> · 단추 8 × '+f2(tn,3)+' = <b>'+f2(8*tn,1)+'cm</b>'+(fixed&&t!==0?' · 지금은 장식이 수평이라 몸과 '+Math.abs(t)+'° 어긋납니다.':'');}
  onIn(inp,draw);seg(h,'button',function(b){fixed=+b.dataset.f;draw();});draw();};

P.p2_mix=function(h){var c=ctl(h),chk=c.querySelectorAll('input[type=checkbox]'),sl=c.querySelectorAll('input[type=range]'),W=520,H=400,sc=6;
  function draw(){var form=chk[0].checked,cast=chk[1].checked,d=+sl[0].value,al=+sl[1].value,len=d/Math.tan(rad(al));var s=svgOf(h,W,H);el('rect',{x:0,y:0,width:W,height:H,fill:'#fbfcfd'},s);
    var L0=190,L1=290,top=140,bot=392;el('rect',{x:L0,y:top-20,width:L1-L0,height:bot-top+20,fill:'#f6d9c4',stroke:'#2a2230','stroke-width':2},s);
    var cid='clipLeg'+Math.round(Math.random()*1e6);var cp=el('clipPath',{id:cid},el('defs',{},s));el('rect',{x:L0,y:top-20,width:L1-L0,height:bot-top+20},cp);var g=el('g',{'clip-path':'url(#'+cid+')'},s);
    if(form)el('rect',{x:L0+(L1-L0)*0.66,y:top-20,width:(L1-L0)*0.34,height:bot-top+20,fill:'#6b5f88',opacity:.45},g);
    var sl2=Math.min(bot-top,len*sc);if(cast){el('path',{d:wave(L0-10,L1+10,top+sl2,7,26,1)+' L'+(L1+10)+','+(top-30)+' L'+(L0-10)+','+(top-30)+'Z',fill:'#3d3550',opacity:.55},g);}
    el('path',{d:'M110,30 L370,30 Q420,100 430,'+top+' '+wave(430,50,top,7,26,1).replace('M','L')+' Q60,100 110,30Z',fill:'#34363f',stroke:'#2a2230','stroke-width':2},s);
    el('path',{d:wave(50,430,top,7,26,1),fill:'none',stroke:'#fbfbfd','stroke-width':4},s);
    ktxt(s,12,22,'빛: 위쪽 왼편에서 · 다리 면과 '+al+'°',{size:13,fill:C.navy});if(cast&&sl2>0)ktxt(s,L1+16,top+sl2,'떨어지는 그림자 끝 — 프릴 물결 모양',{size:12,fill:C.ink});if(form)ktxt(s,L1+16,bot-10,'입체 그림자 — 다리의 둥근 윤곽',{size:12,fill:C.ink});
    out(h).innerHTML='다리 위 그림자 길이 = '+d+'cm ÷ tan '+al+'°('+f2(Math.tan(rad(al)),2)+') = <b>'+f2(len,1)+'cm</b>'+(form&&cast?' · 두 그림자가 겹친 곳은 같은 색이라도 경계 모양으로 주인을 구별합니다.':'');}
  c.querySelectorAll('input').forEach(function(i){i.addEventListener('input',draw);i.addEventListener('change',draw);});draw();};

/* ===================== 3부 · 앉은 자세 ===================== */
P.p3_joints=function(h){var inp=ctl(h).querySelector('input'),W=560,H=360;
  function draw(){var t=+inp.value/100,ha=90*t,ka=150*t,ea=20*t;var s=svgOf(h,W,H);el('rect',{x:0,y:0,width:W,height:H,fill:'#fbfcfd'},s);el('line',{x1:20,y1:330,x2:300,y2:330,stroke:'#8a8f99','stroke-width':2},s);
    var hipY=lerp(170,282,t),hip=[150,hipY],sh=[150,hipY-120],head=[150,hipY-150];
    var th=rad(ha),knee=[hip[0]+Math.sin(th)*90,hip[1]+Math.cos(th)*90];
    var shinAng=th-rad(ka),ank=[knee[0]+Math.sin(shinAng)*85,Math.min(328,knee[1]+Math.cos(shinAng)*85)];
    var elb=[sh[0]-22*t-4,sh[1]+70],hand=[sh[0]-44*t-6,lerp(sh[1]+140,328,t)];
    [[sh,hip,'#c9bfe2',30],[hip,knee,'#5b6f9a',26],[knee,ank,'#5b6f9a',20],[sh,elb,'#c9bfe2',14],[elb,hand,'#c9bfe2',12]].forEach(function(L){el('line',{x1:L[0][0],y1:L[0][1],x2:L[1][0],y2:L[1][1],stroke:'#2a2230','stroke-width':L[3]+3,'stroke-linecap':'round'},s);el('line',{x1:L[0][0],y1:L[0][1],x2:L[1][0],y2:L[1][1],stroke:L[2],'stroke-width':L[3],'stroke-linecap':'round'},s);});
    el('circle',{cx:head[0],cy:head[1],r:22,fill:'#f8dcc8',stroke:'#2a2230','stroke-width':2},s);
    [[hip,'고관절'],[knee,'무릎'],[elb,'팔꿈치']].forEach(function(j){el('circle',{cx:j[0][0],cy:j[0][1],r:6,fill:C.orange},s);});
    var J=[['고관절',14,ha],['무릎',11,ka],['팔꿈치',8,ea]];J.forEach(function(j,k){var v=j[1]*rad(j[2]),y=70+k*70;ktxt(s,330,y-8,j[0]+' — 두께 '+j[1]+'cm × '+f2(rad(j[2]),2)+'라디안('+Math.round(j[2])+'°)',{size:12.5,fill:C.ink});
      el('rect',{x:330,y:y,width:Math.max(2,v*5),height:20,rx:4,fill:k===1?C.orange:C.teal},s);ktxt(s,336+Math.max(2,v*5),y+15,f2(v,1)+'cm',{size:13,fill:C.ink,weight:'bold'});});
    ktxt(s,12,22,'옆에서 본 모습 — 앉는 정도 '+inp.value+'%',{size:13,fill:C.navy});
    out(h).innerHTML='남는 천: 고관절 <b>'+f2(14*rad(ha),1)+'cm</b> · 무릎 <b>'+f2(11*rad(ka),1)+'cm</b> · 팔꿈치 <b>'+f2(8*rad(ea),1)+'cm</b>'+(t>0.5?' → 무릎이 가장 많습니다. 모임 주름은 무릎·고관절부터.':'');}
  onIn(inp,draw);draw();};

P.p3_button=function(h){var c=ctl(h),inp=c.querySelector('input'),lock=1;
  function setup(cl){var p=+inp.value;cl.pin={};pinAt(cl,0,0,[-7.6,0,0]);pinAt(cl,cl.nx-1,0,[7.6,0,0]);pinAt(cl,0,12,[-7.6,-11.4,0]);pinAt(cl,cl.nx-1,12,[7.6,-11.4,0]);
    if(lock)pinAt(cl,9,6,[p*0.55,-5.7-p*0.12,p*0.45]);}
  var sim=runCloth(h,setup,function(){return {g:0.01,stiff:0.25,report:function(cl){var a=clothCount(cl,2)+clothCount(cl,10)+clothCount(cl,6);
    out(h).innerHTML=(lock?'단추 잠금 · 당기는 정도 <b>'+inp.value+'</b> → 단추 둘레 굴곡 <b>'+a+'</b>개. 단추(가운데 회색 점)에서 네 고정점 쪽으로 주름이 퍼집니다.':'단추 풀기 → 붙잡는 점이 없어 천이 처질 뿐입니다(굴곡 '+a+'개).');}};});
  onIn(inp,function(){sim.reset();});seg(h,'button',function(b){lock=+b.dataset.b;sim.reset();});};

P.p3_stiff=function(h){var inp=ctl(h).querySelector('input');
  var sim=runCloth(h,function(cl){pinMode(cl,4);},function(){var st=+inp.value/100;return {g:0.012,stiff:st*0.95,report:function(cl){var f=cl.folds();
    out(h).innerHTML='뻣뻣함 <b>'+inp.value+'</b> → 주름 굴곡 <b>'+f+'</b>개 · '+(st<=0.2?'셔츠·니트처럼 잔주름이 많습니다.':st>=0.7?'블레이저처럼 주름이 적고 크게 꺾입니다.':'중간 두께의 천입니다.');}};});
  onIn(inp,function(){sim.reset();});};

P.p3_pleats=function(h){var ins=ctl(h).querySelectorAll('input'),W=520,H=420,WAIST=66;
  function draw(){var R=+ins[0].value,n=+ins[1].value,rw=WAIST/(2*Math.PI),sc=4.8,cx=W/2,cy=H/2+4;var s=svgOf(h,W,H);el('rect',{x:0,y:0,width:W,height:H,fill:'#fbfcfd'},s);
    for(var k=0;k<n;k++){var a0=2*Math.PI*k/n,a1=2*Math.PI*(k+1)/n;var p=[[rw,a0],[R,a0],[R,a1],[rw,a1]].map(function(q){return (cx+Math.cos(q[1])*q[0]*sc).toFixed(1)+','+(cy+Math.sin(q[1])*q[0]*sc).toFixed(1);}).join(' ');
      el('polygon',{points:p,fill:k%2?'#b7a98c':'#d8c9a8',stroke:'#5a4a30','stroke-width':0.8},s);}
    el('circle',{cx:cx,cy:cy,r:rw*sc,fill:'#f8dcc8',stroke:'#2a2230','stroke-width':2},s);ktxt(s,cx,cy+4,'허리',{size:12,anchor:'middle',fill:C.ink});
    var hemC=2*Math.PI*R,ww=WAIST/n,hw=hemC/n;ktxt(s,12,22,'위에서 본 주름치마 — 허리 둘레 66cm, 주름 '+n+'개',{size:13,fill:C.navy});
    out(h).innerHTML='허리 주름 하나 66 ÷ '+n+' = <b>'+f2(ww,2)+'cm</b> · 밑단 둘레 2 × 3.14 × '+R+' = '+Math.round(hemC)+'cm → 밑단 주름 하나 <b>'+f2(hw,1)+'cm</b> (허리의 '+f2(hw/ww,1)+'배)';}
  ins.forEach(function(i){onIn(i,draw);});draw();};

P.p3_depth=function(h){var W=520,H=330,view='line';var NAMES={hand:'손(소매)',blz:'블레이저 밑단',skt:'치마',leg:'접은 다리'},RIGHT=['hand','blz','skt','leg'];var order=['leg','skt','hand','blz'];
  var wrap=document.createElement('div');wrap.style.cssText='display:grid;grid-template-columns:minmax(0,1fr) 190px;gap:12px;align-items:start';h.innerHTML='';h.appendChild(wrap);var host=document.createElement('div'),list=document.createElement('div');wrap.appendChild(host);wrap.appendChild(list);
  if(window.matchMedia&&window.matchMedia('(max-width:640px)').matches)wrap.style.gridTemplateColumns='1fr';
  var SH={leg:'M40,250 Q120,200 260,230 Q380,250 470,300 L470,320 L40,320 Z',skt:'M150,150 L360,150 Q420,240 440,290 Q300,300 110,285 Q120,220 150,150Z',blz:'M165,70 L345,70 L362,178 Q300,196 255,186 Q210,196 150,178 Z',hand:'M380,60 L410,60 L420,240 Q430,270 405,276 Q378,278 380,250 Z'};
  var COL={leg:'#5b6f9a',skt:'#d8c9a8',blz:'#c79a6a',hand:'#f8dcc8'};
  function draw(){var s=el('svg',{viewBox:'0 0 '+W+' '+H,role:'img','aria-label':'겹침 순서 그림'});host.innerHTML='';host.appendChild(s);el('rect',{x:0,y:0,width:W,height:H,fill:view==='depth'?'#000':'#fbfcfd'},s);
    var back=order.slice().reverse();back.forEach(function(k,idx){var rank=order.indexOf(k);
      if(view==='depth'){var v=Math.round(255-rank*55);el('path',{d:SH[k],fill:'rgb('+v+','+v+','+v+')',stroke:'#000','stroke-width':1},s);return;}
      if(idx>0)el('path',{d:SH[k],fill:'#2a2240',opacity:.28,transform:'translate(-10,12)'},s);
      el('path',{d:SH[k],fill:COL[k],stroke:'#2a2230','stroke-width':2},s);});
    var ok=order.join()===RIGHT.join();ktxt(s,12,22,view==='depth'?'깊이 지도 — 앞일수록 밝게':'선화 + 그림자 — 앞 물체가 뒤 물체에 그림자(왼쪽 아래)',{size:12.5,fill:view==='depth'?'#fff':C.navy});
    list.innerHTML='<b style="font-size:13px">앞 → 뒤 순서</b>'+order.map(function(k,i){return '<div style="display:flex;gap:4px;align-items:center;margin:4px 0"><span style="flex:1;font-size:14px">'+(i+1)+'. '+NAMES[k]+'</span><button type="button" class="btn" data-u="'+i+'" aria-label="'+NAMES[k]+' 앞으로">▲</button><button type="button" class="btn" data-d="'+i+'" aria-label="'+NAMES[k]+' 뒤로">▼</button></div>';}).join('');
    list.querySelectorAll('button').forEach(function(b){b.addEventListener('click',function(){var i=+(b.dataset.u||b.dataset.d),j=b.dataset.u!=null?i-1:i+1;if(j<0||j>3)return;var t=order[i];order[i]=order[j];order[j]=t;draw();});});
    var wrong=order.map(function(k,i){return k===RIGHT[i]?null:NAMES[k];}).filter(Boolean);
    out(h).innerHTML=ok?'<b>맞는 순서입니다.</b> 손이 블레이저 위에, 블레이저가 치마 위에, 치마가 다리 위에 그림자를 드리웁니다.':'아직 어긋난 곳: '+wrong.join(', ')+'. 손은 몸 옆 바닥에서 가장 앞에 있고, 블레이저 밑단은 치마 위에 얹혀 있습니다.';}
  seg(h,'button',function(b){if(b.dataset.v==='shuffle'){var R=Math.random;do{order.sort(function(){return R()-0.5;});}while(order.join()===RIGHT.join());}else view=b.dataset.v;draw();});draw();};

/* ===================== 4부 · 광원 방향 ===================== */
/* 둥근 인물(구·캡슐) 픽셀 음영 — 4부 */
var SFIG=[['cap',[150,262],[142,370],20,'#5b6f9a'],['cap',[142,370],[140,480],18,'#5b6f9a'],['cap',[205,262],[222,375],20,'#5b6f9a'],['cap',[222,375],[205,480],18,'#5b6f9a'],
 ['cap',[130,128],[112,232],14,'#a99ac8'],['cap',[112,232],[108,318],13,'#a99ac8'],['cap',[180,140],[180,236],62,'#a99ac8'],['cap',[180,96],[180,116],12,'#f6d3b8'],
 ['cap',[230,128],[276,200],14,'#a99ac8'],['cap',[276,200],[238,250],13,'#a99ac8'],['sph',[180,62],32,0,'#f6d3b8']];
function smoothFig(ctx,W,H,L,ox){ox=ox||0;var img=ctx.createImageData(W,H),d=img.data,i;for(i=0;i<d.length;i+=4){d[i]=251;d[i+1]=252;d[i+2]=253;d[i+3]=255;}
  SFIG.forEach(function(P_){var col=hex(P_[P_.length-1]);var x0,y0,x1,y1,rr;if(P_[0]==='sph'){x0=P_[1][0]-P_[2];x1=P_[1][0]+P_[2];y0=P_[1][1]-P_[2];y1=P_[1][1]+P_[2];}else{rr=P_[3];x0=Math.min(P_[1][0],P_[2][0])-rr;x1=Math.max(P_[1][0],P_[2][0])+rr;y0=Math.min(P_[1][1],P_[2][1])-rr;y1=Math.max(P_[1][1],P_[2][1])+rr;}
    for(var y=Math.max(0,Math.floor(y0));y<=Math.min(H-1,Math.ceil(y1));y++)for(var x=Math.max(0,Math.floor(x0+ox));x<=Math.min(W-1,Math.ceil(x1+ox));x++){var px=x-ox,n;
      if(P_[0]==='sph'){var dx=(px-P_[1][0])/P_[2],dy=(y-P_[1][1])/P_[2];if(dx*dx+dy*dy>1)continue;n=[dx,-dy,Math.sqrt(1-dx*dx-dy*dy)];}
      else{var ax=P_[1][0],ay=P_[1][1],bx=P_[2][0],by=P_[2][1],vx=bx-ax,vy=by-ay,l2=vx*vx+vy*vy,t=clamp(((px-ax)*vx+(y-ay)*vy)/l2,0,1),cx=ax+vx*t,cy=ay+vy*t,ex=(px-cx)/rr,ey=(y-cy)/rr;if(ex*ex+ey*ey>1)continue;n=[ex,-ey,Math.sqrt(1-ex*ex-ey*ey)];}
      var b=dot(n,L),k=b>0.18?1:0.58;if(n[2]<0.25)k*=0.82;var o=(y*W+x)*4;d[o]=col[0]*k;d[o+1]=col[1]*k;d[o+2]=col[2]*k;}});
  ctx.putImageData(img,0,0);}

var LDIR={up:[-0.15,1,0.35],down:[-0.15,-1,0.35],left:[-1,0.3,0.4],right:[1,0.3,0.4],back:[0.1,0.45,-1]};
var LNAME={up:'위',down:'아래',left:'왼쪽',right:'오른쪽',back:'뒤'};
P.p4_dir=function(h){var lk='up',W=360,H=500;var cv=canvasOf(h,W,H,400),ctx=cv.getContext('2d');
  function draw(){var L=norm(LDIR[lk]);smoothFig(ctx,W,H,L);var cx=305,cy=70,R=36;ctx.strokeStyle='#cfd5dd';ctx.lineWidth=2;ctx.beginPath();ctx.arc(cx,cy,R,0,7);ctx.stroke();var m=Math.hypot(L[0],L[1])||1,lx=cx+L[0]/m*R,ly=cy-L[1]/m*R;
    if(lk==='back'){lx=cx;ly=cy;}ctx.strokeStyle=C.orange;ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(lx,ly);ctx.lineTo(cx+(cx-lx)*0.5,cy+(cy-ly)*0.5);ctx.stroke();ctx.fillStyle='#ffd34d';ctx.beginPath();ctx.arc(lx,ly,10,0,7);ctx.fill();ctx.stroke();
    ctx.fillStyle=C.muted;ctx.font='11.5px '+KFONT;ctx.textAlign='center';ctx.fillText('빛이 오는 쪽',cx,cy+R+16);ctx.textAlign='start';
    ctx.fillStyle=C.navy;ctx.font='bold 15px '+KFONT;ctx.fillText('광원: '+LNAME[lk]+(lk==='back'?' (흐린 원 = 몸 뒤쪽)':''),10,24);
    var tx={up:'윗면(어깨·머리 위)이 밝고, 턱 아래와 몸 아랫면이 어둡습니다.',down:'아랫면(턱 아래·팔 아래)이 밝고, 머리 위와 어깨 위가 어둡습니다. 평소와 반대입니다.',left:'왼쪽 면이 밝고, <b>오른쪽 면</b>이 그림자입니다.',right:'오른쪽 면이 밝고, <b>왼쪽 면</b>이 그림자입니다.',back:'앞면 대부분이 그림자이고, 가장자리만 밝습니다(역광).'}[lk];
    out(h).innerHTML=tx+' 그림자는 늘 광원의 반대쪽 면에 생깁니다.';}
  seg(h,'button',function(b){lk=b.dataset.l;draw();});draw();};

P.p4_below=function(h){var inp=ctl(h).querySelector('input'),W=360,H=500;var cv=canvasOf(h,W,H,400),ctx=cv.getContext('2d');
  function draw(){var e=+inp.value,L=norm([-0.3,Math.sin(rad(e)),Math.cos(rad(e))*0.9]);smoothFig(ctx,W,H,L);var top=Math.max(0,L[1]),bot=Math.max(0,-L[1]);
    ctx.fillStyle='#ffd34d';ctx.strokeStyle=C.orange;ctx.lineWidth=3;ctx.beginPath();ctx.arc(40,clamp(250-e*3.2,40,H-20),13,0,7);ctx.fill();ctx.stroke();
    ctx.fillStyle=C.navy;ctx.font='bold 15px '+KFONT;ctx.fillText('광원 높이 '+e+'°'+(e<0?' — 아래 조명':e>0?' — 위 조명':' — 수평'),10,24);
    [['윗면(어깨 위)',top,52],['아랫면(턱·팔 아래)',bot,78]].forEach(function(r){ctx.fillStyle=C.ink;ctx.font='12.5px '+KFONT;ctx.fillText(r[0],10,r[2]);ctx.fillStyle=r[1]>0.05?'#f2b84b':'#5b6874';ctx.fillRect(130,r[2]-11,Math.max(2,r[1]*80),13);ctx.fillStyle=C.ink;ctx.fillText(Math.round(r[1]*100)+'%',136+Math.max(2,r[1]*80),r[2]);});
    out(h).innerHTML='윗면 밝기 <b>'+Math.round(top*100)+'%</b> · 아랫면 밝기 <b>'+Math.round(bot*100)+'%</b>'+(e<0?' → 아래 조명: 아랫면이 더 밝습니다. 턱 아래 그림자를 지우세요.':e>0?' → 위 조명: 윗면이 더 밝습니다.':' → 둘 다 빛을 스칩니다.');}
  onIn(inp,draw);draw();};

P.p4_side=function(h){var ins=ctl(h).querySelectorAll('input'),W=560,H=360,sc=6;
  function draw(){var d=+ins[0].value,a=+ins[1].value,sh=d*Math.tan(rad(a));var s=svgOf(h,W,H);el('rect',{x:0,y:0,width:W,height:H,fill:'#fbfcfd'},s);
    /* 위에서 본 그림: 아래쪽이 보는 사람. 몸통 앞면은 y=110, 팔은 그 앞(아래)에 d만큼 떠 있음 */
    var fy=110,ax=150,armBack=fy+d*sc,armY=armBack+14;el('rect',{x:30,y:fy-26,width:240,height:26,fill:'#c9bfe2',stroke:'#2a2230'},s);ktxt(s,34,fy-34,'몸통(위에서 본 단면)',{size:11.5});
    var vx=-Math.sin(rad(a)),vy=-Math.cos(rad(a));/* 빛의 진행 방향: 오른쪽 앞 → 왼쪽 뒤 */
    
    el('line',{x1:ax-vx*170,y1:armBack-vy*170,x2:ax-sh*sc,y2:fy,stroke:C.orange,'stroke-width':2.4},s);
    el('rect',{x:ax-14-sh*sc,y:fy-6,width:28,height:6,fill:'#3d3550'},s);el('circle',{cx:ax,cy:armY,r:14,fill:'#d8c9a8',stroke:'#2a2230'},s);ktxt(s,ax+20,armY+4,'팔',{size:12});
    ktxt(s,150,armY+40,'▼ 보는 사람',{size:11.5,anchor:'middle',fill:C.blue});ktxt(s,12,22,'위에서 본 그림 — 빛은 오른쪽 앞에서',{size:12.5,fill:C.navy});
    /* 앞에서 본 그림 */
    var fx=330,fw=200;el('rect',{x:fx,y:60,width:fw,height:270,fill:'#c9bfe2',stroke:'#2a2230'},s);el('rect',{x:fx,y:60,width:fw*0.5,height:270,fill:'#6b5f88',opacity:0.42},s);
    var axf=fx+fw*0.62;el('rect',{x:Math.max(fx,axf-14-sh*sc),y:112,width:28,height:180,fill:'#3d3550',opacity:.55},s);el('rect',{x:axf-14,y:100,width:28,height:180,rx:12,fill:'#d8c9a8',stroke:'#2a2230'},s);
    ktxt(s,fx,52,'앞에서 본 몸통과 팔(왼쪽 절반 = 입체 그림자)',{size:12,fill:C.navy});
    out(h).innerHTML='팔 그림자가 밀리는 거리 = '+d+'cm × tan '+a+'°('+f2(Math.tan(rad(a)),2)+') = <b>'+f2(sh,1)+'cm</b>'+(d===0?' · 팔이 몸에 붙어 있어 그림자도 팔에 딱 붙습니다.':'')+' · 몸통 왼쪽 절반은 입체 그림자입니다.';}
  ins.forEach(function(i){onIn(i,draw);});draw();};

P.p4_angle=function(h){var c=ctl(h),inp=c.querySelector('input'),side=-1,W=560,H=320;
  function draw(){var ph=+inp.value,frac=(1+Math.cos(rad(ph)))/2;var s=svgOf(h,W,H);el('rect',{x:0,y:0,width:W,height:H,fill:'#fbfcfd'},s);
    var cx=140,cy=150,R=80;/* 위에서 본 머리 원: 아래쪽이 보는 사람 */
    el('circle',{cx:cx,cy:cy,r:R,fill:'#5b6874',stroke:'#2a2230','stroke-width':2},s);
    var la=Math.PI/2-side*rad(ph);/* 화면 각: 아래(보는 사람)=90°, 빛이 왼쪽이면 화면 왼쪽 */
    var a0=la-Math.PI/2,a1=la+Math.PI/2;el('path',{d:'M'+(cx+R*Math.cos(a0))+','+(cy+R*Math.sin(a0))+' A'+R+' '+R+' 0 0 1 '+(cx+R*Math.cos(a1))+','+(cy+R*Math.sin(a1))+' Z',fill:'#f6e3c6',stroke:'none'},s);
    el('path',{d:'M'+(cx-R)+','+cy+' A'+R+' '+R+' 0 0 0 '+(cx+R)+','+cy,fill:'none',stroke:C.blue,'stroke-width':5,opacity:.6},s);
    var lx=cx+Math.cos(la)*(R+50),ly=cy+Math.sin(la)*(R+50);el('line',{x1:lx,y1:ly,x2:cx+Math.cos(la)*(R+8),y2:cy+Math.sin(la)*(R+8),stroke:C.orange,'stroke-width':4},s);el('circle',{cx:lx,cy:ly,r:11,fill:'#ffd34d',stroke:C.orange,'stroke-width':2},s);
    ktxt(s,cx,cy+R+40,'▼ 보는 사람',{size:12,anchor:'middle',fill:C.blue});ktxt(s,12,22,'위에서 본 머리 — 파란 테두리 = 보이는 앞쪽 반원',{size:12.5,fill:C.navy});
    // 앞에서 본 원기둥
    var fx=340,fw=180,fy=60,fh=220;el('rect',{x:fx,y:fy,width:fw,height:fh,fill:'#5b6874',stroke:'#2a2230','stroke-width':2},s);
    var litW=fw*frac;el('rect',{x:side<0?fx:fx+fw-litW,y:fy,width:litW,height:fh,fill:'#f6e3c6'},s);el('rect',{x:fx,y:fy,width:fw,height:fh,fill:'none',stroke:'#2a2230','stroke-width':2},s);
    ktxt(s,fx+fw/2,fy+fh+22,'앞에서 본 몸 — 밝은 폭 '+Math.round(frac*100)+'%',{size:13,anchor:'middle',fill:C.ink,weight:'bold'});
    out(h).innerHTML='φ = <b>'+ph+'°</b>, cos φ = '+num(Math.cos(rad(ph)),2)+' → 밝은 폭 (1 + '+num(Math.cos(rad(ph)),2)+') ÷ 2 = <b>'+Math.round(frac*100)+'%</b> · 빛이 '+(side<0?'왼쪽':'오른쪽')+(ph<80?' 앞':ph>100?' 뒤':' 바로 옆')+'에서 옵니다.';}
  onIn(inp,draw);seg(h,'button',function(b){side=+b.dataset.s;draw();});draw();};

P.p4_relight=function(h){var ins=ctl(h).querySelectorAll('input'),W=460,H=270;var cv=canvasOf(h,W,H,560),ctx=cv.getContext('2d');
  function nAt(x,y){var dx=(x-115)/48,dy=(y-75)/48;if(dx*dx+dy*dy<=1)return [dx,-dy,Math.sqrt(1-dx*dx-dy*dy),'#f6d3b8'];if(x>=45&&x<=185&&y>=128&&y<=262){var u=(x-115)/70;return [u*0.95,0.3*(1-(y-128)/134)*0.4,Math.sqrt(Math.max(0,1-u*u*0.9)),'#a99ac8'];}return null;}
  function draw(){var az=+ins[0].value,e=+ins[1].value,L=[Math.sin(rad(az))*Math.cos(rad(e)),Math.sin(rad(e)),Math.cos(rad(az))*Math.cos(rad(e))];var img=ctx.createImageData(W,H),d=img.data;
    for(var y=0;y<H;y++)for(var x=0;x<W;x++){var i=(y*W+x)*4,col=[251,252,253];var half=x>=230?1:0,lx=x-half*230;var n=nAt(lx,y);
      if(n){var nn=norm([n[0],n[1],n[2]]);if(!half)col=[(nn[0]*0.5+0.5)*255,(nn[1]*0.5+0.5)*255,(nn[2]*0.5+0.5)*255];else{var b=Math.max(0,dot(nn,L));var base=hex(n[3]);var k=0.3+0.7*b;col=base.map(function(v){return v*k;});}}
      d[i]=col[0];d[i+1]=col[1];d[i+2]=col[2];d[i+3]=255;}
    ctx.putImageData(img,0,0);ctx.fillStyle=C.navy;ctx.font='13px '+KFONT;ctx.fillText('노멀 지도(그대로)',10,18);ctx.fillText('다시 조명한 결과',240,18);
    var px=230+115+L[0]*90,py=75-L[1]*60;ctx.fillStyle='#ffd34d';ctx.strokeStyle=C.orange;ctx.lineWidth=2;ctx.beginPath();ctx.arc(clamp(px,240,W-12),clamp(py,30,H-12),9,0,7);ctx.fill();ctx.stroke();
    out(h).innerHTML='빛 방향 (lx, ly, lz) = ('+num(L[0],2)+', '+num(L[1],2)+', '+num(L[2],2)+') · 머리 한가운데 면 (0, 0, 1)의 밝기 = max(0, '+num(L[2],2)+') = <b>'+f2(Math.max(0,L[2]),2)+'</b>'+(L[2]<0?' — 빛이 뒤에서 와서 정면은 그림자입니다.':'');}
  ins.forEach(function(i){onIn(i,draw);});draw();};

/* ===================== 5부 · 실전 연습장 ===================== */
function practice(){var root=document.getElementById('practice');if(!root)return;var tabs=root.querySelectorAll('.tabs button'),scenes=root.querySelectorAll('.scene');
  function show(id){tabs.forEach(function(b){b.classList.toggle('on',b.dataset.t===id);});scenes.forEach(function(s){s.classList.toggle('on',s.id===id);});if(history.replaceState)history.replaceState(null,'','#'+id);}
  tabs.forEach(function(b){b.addEventListener('click',function(){show(b.dataset.t);});});var hsh=(location.hash||'').slice(1);show([].some.call(scenes,function(s){return s.id===hsh;})?hsh:'contact');
  contact();frill();lightRoom();homework();}
function mset(S,M,touched){if(!touched)return;S.querySelectorAll('.missions li').forEach(function(li,i){if(M[i])li.classList.add('done');});}

var TRUTH={hip:[0,1,2,3,4],up:[0,5,1],sit:[0,7,4,8,6],walk:[0,4,8,6]};
var PJ={hip:[['팔꿈치',8,90],['무릎',12,15],['고관절',14,5]],up:[['어깨(팔 올림)',10,150],['팔꿈치',8,0],['무릎',12,0]],sit:[['무릎',11,150],['고관절',14,90],['팔꿈치',8,20]],walk:[['고관절',14,30],['무릎',12,40],['팔꿈치',8,15]]};
function contact(){var S=document.getElementById('contact');if(!S)return;var q=function(n){return S.querySelector('[name='+n+']');};var g1=S.querySelector('.g1'),g2=S.querySelector('.g2');var touched=false,passed={};var M=[0,0,0];
  var SPN=['어깨 꼭대기','가슴 위','허리에 얹은 손','굽힌 팔꿈치','앞으로 나온 무릎','겨드랑이','엉덩이','잠근 단추','무릎 뒤','등 한가운데'];
  function upd(){var pose=q('pose').value,T=TRUTH[pose],pick=[];for(var i=0;i<10;i++)if(q('sp'+i).checked)pick.push(i);
    var hit=pick.filter(function(i){return T.indexOf(i)>=0;}).length,wrong=pick.filter(function(i){return T.indexOf(i)<0;}),missed=T.length-hit,perfect=hit===T.length&&wrong.length===0;
    if(perfect&&touched)passed[pose]=1;
    board(S.querySelector('.board'),[['맞힌 접점',hit+' / '+T.length,hit===T.length],['놓친 접점',missed+'곳',missed===0],['틀린 고름',wrong.length+'곳',wrong.length===0],['판정',perfect?'통과':'아직',perfect]]);
    var s=el('svg',{viewBox:'0 0 360 300',role:'img','aria-label':'고른 접점 목록 그림'});g1.innerHTML='';g1.appendChild(s);el('rect',{x:0,y:0,width:360,height:300,fill:'#fbfcfd'},s);
    SPN.forEach(function(nm,i){var y=24+i*27,on=pick.indexOf(i)>=0,ok=T.indexOf(i)>=0;el('circle',{cx:20,cy:y-4,r:8,fill:on?(ok?C.green:C.red):(perfect&&ok?C.green:'#e3e8ee')},s);ktxt(s,36,y,nm+(on&&!ok?' — 여기는 천이 덮여 있을 뿐':''),{size:13,fill:on&&!ok?C.red:C.ink});});
    var s2=el('svg',{viewBox:'0 0 360 300',role:'img','aria-label':'관절마다 남는 천 막대'});g2.innerHTML='';g2.appendChild(s2);el('rect',{x:0,y:0,width:360,height:300,fill:'#fbfcfd'},s2);ktxt(s2,12,22,'이 자세에서 관절마다 남는 천(두께 × 각)',{size:12.5,fill:C.navy});
    PJ[pose].forEach(function(j,k){var v=j[1]*rad(j[2]),y=70+k*70;ktxt(s2,14,y-8,j[0]+' '+j[2]+'°',{size:12.5});el('rect',{x:14,y:y,width:Math.max(2,v*9),height:20,rx:4,fill:C.teal},s2);ktxt(s2,20+Math.max(2,v*9),y+15,f2(v,1)+'cm',{size:12.5,weight:'bold'});});
    M=[!!passed.hip,!!passed.sit,Object.keys(passed).length>=3];mset(S,M,touched);
    say(S.querySelector('.talk'),[['doctor','e10','박사',perfect?'좋다. 이 자세의 접점은 '+T.map(function(i){return SPN[i];}).join(', ')+'.':'자세가 바뀌면 접점도 바뀐다. 어디가 걸리고 눌리고 굽었나?'],['haru','e10','조수','맞힌 '+hit+'곳, 놓친 '+missed+'곳, 틀린 '+wrong.length+'곳이에요.'],['fruitfly','e09','초파리',pose==='sit'?'바닥에 앉으면 단추와 무릎 뒤도 걸리지 않을까?':pose==='up'?'팔을 들면 겨드랑이가 새로 걸리지 않아?':'볼록한 곳, 눌린 곳, 굽은 곳을 차례로 봐.'],['jupanbot','e16','주판봇',wrong.indexOf(9)>=0?'등 한가운데도 넓으니까 접점입니다!':'열 개 다 고르면 하나는 맞겠죠!']]);}
  q('pose').addEventListener('change',function(){for(var i=0;i<10;i++)q('sp'+i).checked=false;touched=true;upd();});
  for(var i=0;i<10;i++)q('sp'+i).addEventListener('change',function(){touched=true;upd();});upd();}

function frill(){var S=document.getElementById('frill');if(!S)return;var q=function(n){return S.querySelector('[name='+n+']');};var g1=S.querySelector('.g1'),g2=S.querySelector('.g2');var touched=false,hist={},M=[0,0,0];
  function upd(){var B=+q('band').value,thick=q('thick').value==='thick',C_=+q('cloth').value,w=+q('wave').value,r=C_/B,n=B/w,A=sineAmp(r,w),depth=2*A,tight=thick&&w<4;
    var key=r.toFixed(2);if(touched){hist[key]=hist[key]||{};hist[key][w]=depth;}
    var dbl=false;Object.keys(hist).forEach(function(k){var H=hist[k];Object.keys(H).forEach(function(ww){if(H[ww*2]!=null&&+k>1.05)dbl=true;});});
    board(S.querySelector('.board'),[['개더 비율',f2(r,2),r>=1.5&&r<=3],['물결 개수',f2(n,2)+'개',Math.abs(n-Math.round(n))<1e-9],['물결 깊이',f2(depth,1)+'cm',depth>=1&&!tight],['천 판정',tight?'너무 촘촘함':'괜찮음',!tight]]);
    var s=el('svg',{viewBox:'0 0 360 220',role:'img','aria-label':'프릴 물결 그림'});g1.innerHTML='';g1.appendChild(s);el('rect',{x:0,y:0,width:360,height:220,fill:'#fbfcfd'},s);var sc=320/B;
    el('rect',{x:20,y:40,width:B*sc,height:10,fill:'#34363f',rx:2},s);var d=wave(20,20+B*sc,120,Math.min(70,A*sc),w*sc,0);el('path',{d:d,fill:'none',stroke:'#2a2230','stroke-width':2},s);
    ktxt(s,20,30,'꿰맨 띠 '+B+'cm · 물결 폭 '+w+'cm',{size:12});ktxt(s,20,210,tight?'두꺼운 천은 물결 폭 4cm 미만으로 접기 어렵습니다':'위에서 본 프릴 가장자리',{size:12,fill:tight?C.red:C.muted});
    var s2=el('svg',{viewBox:'0 0 360 220',role:'img','aria-label':'비율에 따른 물결 깊이 곡선'});g2.innerHTML='';g2.appendChild(s2);el('rect',{x:40,y:20,width:300,height:160,fill:'#fbfcfd',stroke:'#d5dbe2'},s2);
    var maxD=2*sineAmp(3,w),pd='';for(var rr=1;rr<=3.001;rr+=0.1){var dd=2*sineAmp(rr,w);pd+=(rr===1?'M':'L')+(40+(rr-1)/2*300).toFixed(1)+','+(180-dd/maxD*150).toFixed(1);}el('path',{d:pd,fill:'none',stroke:C.teal,'stroke-width':2.5},s2);
    var cxp=40+(clamp(r,1,3)-1)/2*300,cyp=180-Math.min(depth,maxD)/maxD*150;el('circle',{cx:cxp,cy:cyp,r:6,fill:C.orange},s2);ktxt(s2,190,204,'개더 비율 1 ~ 3',{size:12,anchor:'middle'});ktxt(s2,44,16,'물결 깊이(폭 '+w+'cm일 때)',{size:12});
    M=[Math.abs(r-2)<0.005,Math.abs(n-15)<1e-9,dbl];mset(S,M,touched);
    say(S.querySelector('.talk'),[['doctor','e10','박사','비율 '+f2(r,2)+', 물결 '+f2(n,1)+'개. 깊이는 비율이, 개수는 폭이 정한다.'],['sia','e10','시아','물결 하나에 천 '+w+' × '+f2(r,2)+' = '+f2(w*r,1)+'cm가 들어가요.'],['fruitfly','e09','초파리',tight?'두꺼운 천을 이렇게 촘촘히 접을 수 있을까?':'비율은 그대로 두고 폭만 두 배로 해 보면?'],['jupanbot','e16','주판봇',r>2.8?'천은 많을수록 화려합니다! 3배!':'물결은 백 개가 정답입니다!']]);}
  S.querySelectorAll('input,select').forEach(function(i){i.addEventListener('input',function(){touched=true;upd();});i.addEventListener('change',function(){touched=true;upd();});});upd();}

function lightRoom(){var S=document.getElementById('light');if(!S)return;var q=function(n){return S.querySelector('[name='+n+']');};var g1=S.querySelector('.g1'),g2=S.querySelector('.g2');var touched=false,M=[0,0,0],got=[0,0,0];
  function upd(){var ord=q('order').value,ph=+q('phi').value,e=+q('elev').value,side=+q('side').value,lit=(1+Math.cos(rad(ph)))/2*100,top=Math.max(0,Math.sin(rad(e))),bot=Math.max(0,-Math.sin(rad(e)));
    var okOrd=ord==='portrait'?(lit>=70&&lit<=80&&e>0):ord==='stage'?(e<0):(lit<=10);
    board(S.querySelector('.board'),[['밝은 폭',Math.round(lit)+'%',lit>=20],['윗면 / 아랫면',Math.round(top*100)+' / '+Math.round(bot*100),true],['그림자 쪽',(side<0?'오른쪽':'왼쪽')+(ph>100?' 대부분':''),true],['주문 충족',okOrd?'예':'아직',okOrd]]);
    var s=el('svg',{viewBox:'0 0 360 220',role:'img','aria-label':'위에서 본 광원과 앞에서 본 몸'});g1.innerHTML='';g1.appendChild(s);el('rect',{x:0,y:0,width:360,height:220,fill:'#fbfcfd'},s);
    var cx=90,cy=100,R=55,la=Math.PI/2-side*rad(ph);el('circle',{cx:cx,cy:cy,r:R,fill:'#5b6874'},s);el('path',{d:'M'+(cx+R*Math.cos(la-Math.PI/2))+','+(cy+R*Math.sin(la-Math.PI/2))+' A'+R+' '+R+' 0 0 1 '+(cx+R*Math.cos(la+Math.PI/2))+','+(cy+R*Math.sin(la+Math.PI/2))+'Z',fill:'#f6e3c6'},s);
    el('circle',{cx:cx+Math.cos(la)*(R+28),cy:cy+Math.sin(la)*(R+28),r:9,fill:'#ffd34d',stroke:C.orange,'stroke-width':2},s);ktxt(s,cx,cy+R+40,'▼ 보는 사람',{size:11.5,anchor:'middle',fill:C.blue});
    var fx=210,fw=110,litW=fw*lit/100;el('rect',{x:fx,y:30,width:fw,height:160,fill:'#5b6874'},s);el('rect',{x:side<0?fx:fx+fw-litW,y:30,width:litW,height:160,fill:'#f6e3c6'},s);el('rect',{x:fx,y:30,width:fw,height:160,fill:'none',stroke:'#2a2230','stroke-width':2},s);
    el('rect',{x:fx,y:30,width:fw,height:8,fill:top>bot?'#f6e3c6':'#3d3550'},s);el('rect',{x:fx,y:182,width:fw,height:8,fill:bot>top?'#f6e3c6':'#3d3550'},s);ktxt(s,fx+fw/2,212,'앞에서 본 몸',{size:11.5,anchor:'middle'});
    var s2=el('svg',{viewBox:'0 0 360 220',role:'img','aria-label':'광원 각도에 따른 밝은 폭 곡선'});g2.innerHTML='';g2.appendChild(s2);el('rect',{x:40,y:20,width:300,height:160,fill:'#fbfcfd',stroke:'#d5dbe2'},s2);
    var pd='';for(var t=0;t<=180;t+=5){pd+=(t?'L':'M')+(40+t/180*300).toFixed(1)+','+(180-(1+Math.cos(rad(t)))/2*160).toFixed(1);}el('path',{d:pd,fill:'none',stroke:C.teal,'stroke-width':2.5},s2);
    el('circle',{cx:40+ph/180*300,cy:180-lit/100*160,r:6,fill:C.orange},s2);ktxt(s2,190,204,'광원 각도 φ 0° ~ 180°',{size:12,anchor:'middle'});ktxt(s2,44,16,'밝은 폭 = (1 + cos φ) ÷ 2',{size:12});
    if(touched){if(Math.abs(lit-75)<=3)got[0]=1;if(bot>top)got[1]=1;if(lit<=10)got[2]=1;}M=got.slice();mset(S,M,touched);
    say(S.querySelector('.talk'),[['doctor','e10','박사','φ '+ph+'°, 높이 '+e+'°. '+(okOrd?'주문대로다.':'주문을 다시 읽어 봐.')],['haru','e10','조수','밝은 폭 (1 + '+num(Math.cos(rad(ph)),2)+') ÷ 2 = '+Math.round(lit)+'%예요.'],['fruitfly','e09','초파리',e<0?'아래 조명이면 턱 아래가 밝아지겠지.':'같은 왼쪽이라도 앞인지 뒤인지가 중요해.'],['jupanbot','e16','주판봇',ph===90?'옆이면 무조건 절반! 맞죠?':'그림자는 오른쪽 아래면 충분합니다!']]);}
  S.querySelectorAll('input,select').forEach(function(i){i.addEventListener('input',function(){touched=true;upd();});i.addEventListener('change',function(){touched=true;upd();});});upd();}

var PIC={haru_hoodie:['하루(분홍 생머리에 남색 줄, 머리 위 둥근 번 두 개, 파란 눈), 라벤더색 후드 집업과 조거 바지, 한 손을 허리에 얹고 선 자세','어깨 꼭대기·가슴 위·허리에 얹은 손·굽힌 팔꿈치·앞으로 나온 무릎','팔꿈치 안쪽 모임 주름, 가슴 꼭대기를 향한 당김 주름, 주머니·밑단 아래 얇은 그림자 띠'],
 sia_maid:['시아(허리까지 오는 검은 생머리, 회색 눈, 은색 귀걸이), 흰 프릴 앞치마를 두른 검은 메이드복, 양손으로 치마 끝을 살짝 잡은 자세','어깨 꼭대기·허리끈·치마 끝을 잡은 손','앞치마 프릴(개더 비율 약 2), 허리끈 위아래 모임 주름, 어깨 프릴은 어깨선과 나란히'],
 moa_sit:['모아(애쉬 베이지 웨이브 머리, 왼쪽 귀 위 흰 리본, 호박색 눈), 캐멀색 블레이저와 주름치마, 바닥에 앉아 다리를 옆으로 접고 한 손을 짚은 자세','어깨 꼭대기·잠근 단추·무릎·무릎 뒤·엉덩이','무릎·고관절 모임 주름, 단추에서 퍼지는 고정 주름, 빳빳한 블레이저, 부채처럼 퍼진 주름치마'],
 trio_walk:['하루, 흰 반소매 셔츠와 회색 긴 바지, 주머니에 손을 넣고 고개를 숙인 채 걷는 자세','어깨 꼭대기·주머니에 넣은 손·앞으로 나온 무릎·뒤쪽 무릎 뒤','앞다리 무릎 위 당김 주름, 뒷다리 무릎 뒤 모임 주름, 주머니에 넣은 손에서 퍼지는 주름']};
var LTXT={top:'광원은 머리 위. 큰 그림자는 몸 아랫면과 다리 안쪽, 머리가 목에 떨어지는 그림자',left:'광원은 왼쪽 앞 60°(위에서 본 각). 몸 오른쪽 4분의 1이 그림자, 팔 그림자는 몸통 오른쪽으로 밀림',right:'광원은 오른쪽 바로 옆. 몸 왼쪽 절반이 그림자, 팔·가방이 몸통 왼쪽에 그림자를 드리움',below:'광원은 아래. 턱 아래가 밝다. 팔 아래도 밝고, 눈썹 위·어깨 위가 어둡다. 떨어지는 그림자는 뒤쪽 벽 위로 길게'};
function homework(){var S=document.getElementById('homework');if(!S)return;var q=function(n){return S.querySelector('[name='+n+']');};var pre=S.querySelector('.promptbox pre'),btns=S.querySelectorAll('.hw');var touched=false,next=0,miss=0,done={},M=[0,0,0];
  function reset(){next=0;miss=0;btns.forEach(function(b){b.classList.remove('ok','no');b.disabled=false;});pre.textContent='순서를 끝까지 맞히면 요청문이 나타납니다.';upd();}
  function upd(){var P_=PIC[q('pic').value],lt=q('lt').value;
    board(S.querySelector('.board'),[['진행',next+' / 6',next===6],['틀린 횟수',miss+'번',miss===0],['완성한 그림',Object.keys(done).length+'장',Object.keys(done).length>=2],['광원',{top:'위',left:'왼쪽 앞',right:'오른쪽',below:'아래'}[lt],true]]);
    var g1=S.querySelector('.g1');var s=el('svg',{viewBox:'0 0 360 220',role:'img','aria-label':'순서 진행 그림'});var box=g1.querySelector('svg');if(box)box.remove();g1.insertBefore(s,g1.firstChild);el('rect',{x:0,y:0,width:360,height:220,fill:'#fbfcfd'},s);
    ['광원','접점','큰 주름','큰 그림자','작은 그림자','주인 확인'].forEach(function(t,i){var x=30+(i%3)*110,y=40+Math.floor(i/3)*90;el('circle',{cx:x+20,cy:y+20,r:22,fill:i<next?C.teal:'#e3e8ee',stroke:'#2a2230'},s);ktxt(s,x+20,y+26,String(i+1),{size:15,anchor:'middle',fill:i<next?'#fff':C.ink,weight:'bold'});ktxt(s,x+20,y+62,t,{size:12,anchor:'middle'});});
    var g2=S.querySelector('.g2');g2.innerHTML='<div class="box" style="font-size:14px"><b>지금 그림</b><p style="margin:6px 0 0">'+P_[0]+'</p></div>';
    M=[M[0]||(next===6&&miss===0&&touched),Object.keys(done).length>=2,!!done.below];mset(S,M,touched);
    say(S.querySelector('.talk'),[['doctor','e10','박사',next===6?'완성이다. 이 요청문이면 AI도 순서를 따라 그릴 수 있다.':'다음 단계는 무엇일까? 큰 것부터 작은 것 순서다.'],['haru','e10','조수',next+'단계까지 맞혔어요. 틀린 건 '+miss+'번이에요.'],['fruitfly','e09','초파리','광원을 먼저 정하지 않으면 그림자 자리를 모르잖아.'],['jupanbot','e16','주판봇','저는 주름 그림자부터 칠하고 싶습니다!']]);}
  btns.forEach(function(b){b.addEventListener('click',function(){touched=true;var k=+b.dataset.k;if(k===next){b.classList.add('ok');b.disabled=true;next++;if(next===6){var P_=PIC[q('pic').value],lt=q('lt').value;done[q('pic').value]=1;if(lt==='below')done.below=1;
          pre.textContent='그림 요청: '+P_[0]+'.\n① '+LTXT[lt]+'.\n② 접점: '+P_[1]+'.\n③ 큰 주름: '+P_[2]+'.\n④ 큰 형체 그림자를 먼저, ⑤ 주름·단차 그림자는 그 위에 얹고, ⑥ 떨어지는 그림자는 가린 물체의 윤곽을 따라.\n애니풍 셀 채색, 흰 배경, 글자·로고 없음, 연구실의 가상 캐릭터.';}}
      else{miss++;b.classList.add('no');setTimeout(function(){b.classList.remove('no');},500);}upd();});});
  S.querySelector('[data-reset]').addEventListener('click',reset);q('pic').addEventListener('change',function(){touched=true;reset();});q('lt').addEventListener('change',function(){touched=true;reset();});
  var cp=S.querySelector('.copy');if(cp)cp.addEventListener('click',function(){try{navigator.clipboard.writeText(pre.textContent);cp.textContent='복사했습니다';setTimeout(function(){cp.textContent='복사하기';},1200);}catch(e){}});
  upd();}

function board(el_,items){el_.innerHTML=items.map(function(it){return '<div class="'+(it[2]?'good':'bad')+'"><span>'+it[0]+'</span><b>'+it[1]+'</b></div>';}).join('');}
function say(el_,lines){el_.innerHTML=lines.map(function(l){return '<div class="line"><img src="../assets/chars/'+l[0]+'_'+l[1]+'.webp" alt="" width="48" height="48"><div class="bub"><b>'+l[2]+'</b>'+l[3]+'</div></div>';}).join('');}
function missions(el_,state,touched){el_.querySelectorAll('li').forEach(function(li,i){if(touched&&state[i])li.classList.add('done');});}
var DONE={};
/* ===================== 퀴즈·지식 색인·꾸러미 ===================== */
function quiz(q){var ans=+q.getAttribute('data-ans');var fb=q.querySelector('.fb');var OK=q.querySelector('.qok'),NO=q.querySelector('.qno');q.querySelectorAll('.opts button').forEach(function(b,i){b.addEventListener('click',function(){q.querySelectorAll('.opts button').forEach(function(x){x.classList.remove('ok','no');});b.classList.add(i===ans?'ok':'no');fb.innerHTML=i===ans?'⭕ '+OK.innerHTML:'❌ '+NO.innerHTML;});});}
function kg(){var raw=document.getElementById('kg-raw');var mount=document.getElementById('kg-mount');if(!raw||!mount)return;var K=JSON.parse(raw.textContent);
  mount.innerHTML='<input class="kg-search" type="search"><div class="kg-list"></div>';var list=mount.querySelector('.kg-list'),inp=mount.querySelector('input');inp.placeholder='개념 찾기 (예: 그림자, 주름, 강도)';inp.setAttribute('aria-label','지식 색인 검색');
  var TY={Concept:'개념',Method:'방법',Analogy:'비유',Application:'쓰임',OpenQuestion:'열린 질문'};var pre=document.body.getAttribute('data-root')||'';
  function render(){var qv=inp.value.trim().toLowerCase();list.innerHTML=K.nodes.filter(function(n){return !qv||(n.label.ko+' '+n.label.en+' '+n.definition.ko).toLowerCase().indexOf(qv)>=0;}).map(function(n){
    var nb=K.edges.filter(function(e){return e.s===n.id||e.o===n.id;}).map(function(e){var o=e.s===n.id?e.o:e.s;var m=K.nodes.filter(function(x){return x.id===o;})[0];return m?m.label.ko:'';}).filter(Boolean);
    return '<div class="kg-item"><span class="t">'+(TY[n.type]||n.type)+'</span><b>'+n.label.ko+'</b><span class="muted">'+n.label.en+'</span><div>'+n.definition.ko+'</div>'+(nb.length?'<div class="muted" style="font-size:12.5px">이웃: '+nb.join(', ')+'</div>':'')+'<a href="'+pre+n.page+n.anchor+'">설명 보러 가기 →</a></div>';}).join('');}
  inp.addEventListener('input',render);render();var ex=document.getElementById('export-mount');if(!ex)return;
  ex.innerHTML='<div class="exp-btns"><button class="btn" data-x="json">kg.json</button><button class="btn" data-x="ld">JSON-LD</button><button class="btn" data-x="ttl">Turtle (Protégé)</button><button class="btn" data-x="csv">CSV (Neo4j·Gephi)</button><button class="btn" data-x="bib">BibTeX</button><button class="btn" data-x="ris">RIS</button></div>';
  function dl(name,text,type){var b=new Blob([text],{type:type||'text/plain'});var a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=name;document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove();},500);}
  var base=K.page;var refs=JSON.parse((document.getElementById('refs-csl')||{textContent:'[]'}).textContent);
  ex.querySelectorAll('button').forEach(function(b){b.addEventListener('click',function(){var x=b.getAttribute('data-x');
    if(x==='json')dl(base+'.kg.json',JSON.stringify(K,null,2),'application/json');
    if(x==='ld')dl(base+'.jsonld',document.getElementById('kg-ld').textContent,'application/ld+json');
    if(x==='ttl'){var t='@prefix lab: <urn:lab:> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n\n';K.nodes.forEach(function(n){t+='<urn:'+n.id+'> a lab:'+n.type+' ;\n  skos:prefLabel "'+n.label.ko+'"@ko , "'+n.label.en+'"@en ;\n  rdfs:comment "'+n.definition.ko.replace(/"/g,'\\"')+'"@ko .\n\n';});K.edges.forEach(function(e){t+='<urn:'+e.s+'> lab:'+e.p+' <urn:'+e.o+'> .\n';});dl(base+'.ttl',t,'text/turtle');}
    if(x==='csv'){var c='id,type,label_ko,label_en,anchor\n'+K.nodes.map(function(n){return [n.id,n.type,n.label.ko,n.label.en,n.page+n.anchor].map(function(v){return '"'+String(v).replace(/"/g,'""')+'"';}).join(',');}).join('\n');c+='\n\nsource,relation,target\n'+K.edges.map(function(e){return [e.s,e.p,e.o].join(',');}).join('\n');dl(base+'.csv',c,'text/csv');}
    if(x==='bib')dl(base+'.bib',refs.map(function(r){return '@misc{'+r.id+',\n  title = {'+r.title+'},\n  author = {'+r.author+'},\n  note = {'+(r.note||'')+'},\n  year = {'+r.year+'}\n}';}).join('\n\n'));
    if(x==='ris')dl(base+'.ris',refs.map(function(r){return 'TY  - GEN\nTI  - '+r.title+'\nAU  - '+r.author+'\nPY  - '+r.year+'\nN1  - '+(r.note||'')+'\nER  - ';}).join('\n'));});});}

function boot(){document.querySelectorAll('[data-panel]').forEach(function(h){var k=h.getAttribute('data-panel');if(P[k]){try{P[k](h);}catch(e){h.textContent='실험을 불러오지 못했습니다.';if(window.console)console.warn(k,e);}}});
  document.querySelectorAll('.quiz').forEach(quiz);kg();practice();
  var pr=document.getElementById('prog');if(pr)window.addEventListener('scroll',function(){var d=document.documentElement;pr.style.width=(100*d.scrollTop/Math.max(1,d.scrollHeight-d.clientHeight))+'%';},{passive:true});}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
})();