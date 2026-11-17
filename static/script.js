let map, marker, pathLine, chart;
const $ = id => document.getElementById(id);
const historyRows = [];
function initMap(){
  map = L.map('map').setView([12.9716,77.5946],14);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    {attribution:'© OpenStreetMap contributors',maxZoom:19}).addTo(map);
  marker = L.marker([12.9716,77.5946]).addTo(map).bindPopup('Simulated drone position');
  pathLine = L.polyline([], {color:'#24c9c3',weight:3}).addTo(map);
}
function initChart(){
  chart = new Chart($('trendChart'),{type:'line',data:{labels:[],datasets:[
    {label:'Altitude (m)',data:[],borderColor:'#58d4d0',backgroundColor:'#58d4d022',tension:.35},
    {label:'Speed (m/s)',data:[],borderColor:'#f2c66d',backgroundColor:'#f2c66d22',tension:.35}
  ]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:'#a9bbca',font:{size:9}}}},
  scales:{x:{ticks:{color:'#8196aa',maxTicksLimit:6},grid:{color:'#26374a'}},
  y:{ticks:{color:'#8196aa'},grid:{color:'#26374a'}}}}});
}
function set(id,value){$(id).textContent=value}
function update(data){
  set('clock',new Date().toLocaleTimeString());set('connection',data.connection);
  set('altitude',data.flight.altitude_m);set('speed',data.flight.ground_speed_ms);
  set('battery',data.battery.remaining_percent);set('batteryBig',data.battery.remaining_percent+'%');
  $('batterybar').style.width=data.battery.remaining_percent+'%';
  $('batterybar').style.background=data.battery.remaining_percent<=25?'#f2c66d':'#65d6a0';
  set('batteryStatus',data.battery.status);set('satellites',data.gps.satellites);set('gpsfix',data.gps.fix);
  set('armed',data.armed?'ARMED':'DISARMED');set('phase',data.vtol_phase);set('mode',data.flight_mode);
  set('heading',data.flight.heading_deg+'°');set('roll',data.flight.roll_deg+'°');set('pitch',data.flight.pitch_deg+'°');
  set('yaw',data.flight.yaw_deg+'°');set('vertical',data.flight.vertical_speed_ms+' m/s');
  set('lat',data.gps.latitude);set('lon',data.gps.longitude);set('gpsalt',data.gps.altitude_m+' m');
  set('voltage',data.battery.voltage_v+' V');set('current',data.battery.current_a+' A');
  set('capacity',data.battery.remaining_capacity_mah+' mAh');set('flighttime',data.battery.estimated_minutes+' min');
  set('telemetry',data.communication.telemetry);set('hm30',data.communication.hm30);
  set('signal',data.communication.signal_percent+'%');set('latency',data.communication.latency_ms+' ms');
  set('packetloss',data.communication.packet_loss_percent+'%');set('lastpacket',data.communication.last_packet);
  set('frontDistance',data.lidar.front_distance_m+' m');
  set('obstacleStatus',data.lidar.obstacle_detected?'OBSTACLE DETECTED':'NO CLOSE OBSTACLE');
  $('obstacleStatus').style.color=data.lidar.obstacle_detected?'#f2c66d':'#65d6a0';
  $('motorList').innerHTML=data.motors.map(m=>`<div class="motor"><strong>MOTOR ${m.id}</strong><span>${m.output_percent}% output · ${m.rpm} RPM</span><small>${m.temperature_c} °C · ${m.status}</small></div>`).join('');
  $('sectors').innerHTML=Object.entries(data.lidar.sectors).map(([k,v])=>`<div><small>${k.toUpperCase()}</small><b>${v} m</b></div>`).join('');
  const point=[data.gps.latitude,data.gps.longitude];marker.setLatLng(point);pathLine.addLatLng(point);
  if(pathLine.getLatLngs().length===1)map.setView(point,14);
  chart.data.labels.push(new Date().toLocaleTimeString());chart.data.datasets[0].data.push(data.flight.altitude_m);
  chart.data.datasets[1].data.push(data.flight.ground_speed_ms);
  if(chart.data.labels.length>25){chart.data.labels.shift();chart.data.datasets.forEach(d=>d.data.shift())}chart.update('none');
  $('alertList').innerHTML=data.alerts.map(a=>`<div class="alert ${a.level}"><b>${a.level}</b> · ${a.message}<small>${new Date(a.time).toLocaleTimeString()}</small></div>`).join('');
  historyRows.unshift({time:new Date(data.timestamp).toLocaleTimeString(),alt:data.flight.altitude_m,speed:data.flight.ground_speed_ms,gps:data.gps.fix,battery:data.battery.remaining_percent,alerts:data.alerts.map(a=>a.level).join(', ')});
  if(historyRows.length>8)historyRows.pop();
  $('history').innerHTML=historyRows.map(r=>`<tr><td>${r.time}</td><td>${r.alt} m</td><td>${r.speed} m/s</td><td>${r.gps}</td><td>${r.battery}%</td><td>${r.alerts}</td></tr>`).join('');
  set('updated','Updated '+new Date().toLocaleTimeString());
}
async function poll(){
  try{const response=await fetch('/api/telemetry');if(!response.ok)throw new Error('API error');update(await response.json())}
  catch(e){set('connection','BACKEND DISCONNECTED');console.error(e)}
}
window.addEventListener('load',()=>{initMap();initChart();poll();setInterval(poll,1500)});
