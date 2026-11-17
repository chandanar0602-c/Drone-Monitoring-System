
let map, marker, homeMarker, pathLine, chart;

const $ = id => document.getElementById(id);

const historyRows = [];

const HOME = [12.9716, 77.5946];


// Safely update dashboard text
function set(id, value) {
    const element = $(id);

    if (element) {
        element.textContent = value ?? '--';
    }
}


// Escape dynamic text before inserting HTML
function escapeHTML(value) {
    return String(value ?? '').replace(/[&<>"']/g, char => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
    })[char]);
}


// Initialize GPS map
function initMap() {
    const mapElement = $('map');

    if (!mapElement || typeof L === 'undefined') {
        console.error('Map container or Leaflet is unavailable.');
        return;
    }

    map = L.map('map').setView(HOME, 14);

    L.tileLayer(
        'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }
    ).addTo(map);

    marker = L.marker(HOME)
        .addTo(map)
        .bindPopup('Simulated Drone Position');

    homeMarker = L.marker(HOME)
        .addTo(map)
        .bindPopup('Simulated Home Location');

    pathLine = L.polyline([], {
        color: '#24c9c3',
        weight: 3
    }).addTo(map);
}


// Initialize flight performance chart
function initChart() {
    const chartElement = $('trendChart');

    if (!chartElement || typeof Chart === 'undefined') {
        console.error('Chart container or Chart.js is unavailable.');
        return;
    }

    chart = new Chart(chartElement, {
        type: 'line',

        data: {
            labels: [],

            datasets: [
                {
                    label: 'Altitude (m)',
                    data: [],
                    borderColor: '#58d4d0',
                    backgroundColor: '#58d4d022',
                    tension: 0.35
                },
                {
                    label: 'Speed (m/s)',
                    data: [],
                    borderColor: '#f2c66d',
                    backgroundColor: '#f2c66d22',
                    tension: 0.35
                }
            ]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            plugins: {
                legend: {
                    labels: {
                        color: '#a9bbca',
                        font: { size: 9 }
                    }
                }
            },

            scales: {
                x: {
                    ticks: {
                        color: '#8196aa',
                        maxTicksLimit: 6
                    },
                    grid: { color: '#26374a' }
                },

                y: {
                    ticks: { color: '#8196aa' },
                    grid: { color: '#26374a' }
                }
            }
        }
    });
}


// Update GPS information and map
function updateGPS(gps) {
    gps = gps || {};

    const validGPS =
        Number.isFinite(gps.latitude) &&
        Number.isFinite(gps.longitude) &&
        gps.latitude >= -90 &&
        gps.latitude <= 90 &&
        gps.longitude >= -180 &&
        gps.longitude <= 180;

    set('lat', validGPS ? gps.latitude : 'Unavailable');
    set('lon', validGPS ? gps.longitude : 'Unavailable');

    set(
        'gpsalt',
        gps.altitude_m != null
            ? gps.altitude_m + ' m'
            : 'Unavailable'
    );

    set('satellites', gps.satellites ?? '--');

    set(
        'gpsfix',
        validGPS
            ? (gps.fix || 'GPS STATUS UNKNOWN')
            : 'GPS SIGNAL UNAVAILABLE'
    );

    if (!validGPS || !map || !marker || !pathLine) {
        return;
    }

    const point = [gps.latitude, gps.longitude];

    marker.setLatLng(point);
    pathLine.addLatLng(point);

    const points = pathLine.getLatLngs();

    if (points.length > 500) {
        pathLine.setLatLngs(points.slice(-500));
    }

    if (!map.getBounds().contains(point)) {
        map.panTo(point);
    }
}


// Update battery monitoring
function updateBattery(battery) {
    battery = battery || {};

    const percent = battery.remaining_percent;

    set('battery', percent ?? '--');

    set(
        'batteryBig',
        percent != null ? percent + '%' : '--'
    );

    const batteryBar = $('batterybar');

    if (batteryBar && Number.isFinite(percent)) {
        batteryBar.style.width =
            Math.max(0, Math.min(100, percent)) + '%';

        batteryBar.style.background =
            percent <= 12
                ? '#f06b70'
                : percent <= 25
                    ? '#f2c66d'
                    : '#65d6a0';
    }

    set('batteryStatus', battery.status || 'Unavailable');

    set('voltage', battery.voltage_v != null
        ? battery.voltage_v + ' V' : '--');

    set('current', battery.current_a != null
        ? battery.current_a + ' A' : '--');

    set('capacity', battery.remaining_capacity_mah != null
        ? battery.remaining_capacity_mah + ' mAh' : '--');

    set('flighttime', battery.estimated_minutes != null
        ? battery.estimated_minutes + ' min' : '--');

    set('batteryTag', battery.source || 'SIMULATED');
}


// Update motor monitoring
function updateMotors(motors) {
    const motorList = $('motorList');

    if (!motorList) return;

    if (!Array.isArray(motors)) {
        motorList.textContent = 'Motor data unavailable';
        return;
    }

    motorList.innerHTML = motors.map(m => `
        <div class="motor">
            <strong>MOTOR ${escapeHTML(m.id)}</strong>
            <span>
                ${escapeHTML(m.output_percent)}% output ·
                ${escapeHTML(m.rpm)} RPM
            </span>
            <small>
                ${escapeHTML(m.temperature_c)} °C ·
                ${escapeHTML(m.status)}
            </small>
        </div>
    `).join('');
}


// Update LiDAR monitoring
function updateLidar(lidar) {
    lidar = lidar || {};

    set(
        'frontDistance',
        lidar.front_distance_m != null
            ? lidar.front_distance_m + ' m'
            : 'Unavailable'
    );

    const obstacleStatus = $('obstacleStatus');

    if (obstacleStatus) {
        obstacleStatus.textContent =
            lidar.obstacle_detected
                ? 'OBSTACLE DETECTED'
                : 'NO CLOSE OBSTACLE';

        obstacleStatus.style.color =
            lidar.obstacle_detected
                ? '#f2c66d'
                : '#65d6a0';
    }

    const sectorsElement = $('sectors');

    if (sectorsElement) {
        const sectors = lidar.sectors || {};

        sectorsElement.innerHTML =
            Object.entries(sectors).map(([key, value]) => `
                <div>
                    <small>${escapeHTML(key.toUpperCase())}</small>
                    <b>${escapeHTML(value)} m</b>
                </div>
            `).join('');
    }
}


// Update communication monitoring
function updateCommunication(communication) {
    communication = communication || {};

    set('telemetry', communication.telemetry || 'Unavailable');
    set('hm30', communication.hm30 || 'Unavailable');

    set(
        'signal',
        communication.signal_percent != null
            ? communication.signal_percent + '%'
            : '--'
    );

    set(
        'latency',
        communication.latency_ms != null
            ? communication.latency_ms + ' ms'
            : '--'
    );

    set(
        'packetloss',
        communication.packet_loss_percent != null
            ? communication.packet_loss_percent + '%'
            : '--'
    );

    set('lastpacket', communication.last_packet || '--');
}


// Update alerts
function updateAlerts(alerts) {
    const alertList = $('alertList');

    if (!alertList) return;

    if (!Array.isArray(alerts) || alerts.length === 0) {
        alertList.textContent = 'No alert information available';
        return;
    }

    alertList.innerHTML = alerts.map(alert => `
        <div class="alert ${escapeHTML(alert.level)}">
            <b>${escapeHTML(alert.level)}</b> ·
            ${escapeHTML(alert.message)}
            <small>${escapeHTML(alert.time || '--')}</small>
        </div>
    `).join('');
}


// Update performance chart
function updateChart(flight) {
    if (!chart) return;

    chart.data.labels.push(new Date().toLocaleTimeString());

    chart.data.datasets[0].data.push(
        flight.altitude_m ?? null
    );

    chart.data.datasets[1].data.push(
        flight.ground_speed_ms ?? null
    );

    if (chart.data.labels.length > 25) {
        chart.data.labels.shift();

        chart.data.datasets.forEach(dataset => {
            dataset.data.shift();
        });
    }

    chart.update('none');
}


// Update recent flight history
function updateHistory(data, flight, alerts) {
    const history = $('history');

    if (!history) return;

    const battery = data.battery || {};

    historyRows.unshift({
        time: data.timestamp
            ? new Date(data.timestamp).toLocaleTimeString()
            : '--',

        alt: flight.altitude_m ?? '--',
        speed: flight.ground_speed_ms ?? '--',
        gps: data.gps?.fix || 'Unavailable',
        battery: battery.remaining_percent ?? '--',

        alerts: alerts.map(a => a.level).join(', ') || 'None'
    });

    if (historyRows.length > 8) {
        historyRows.pop();
    }

    history.innerHTML = historyRows.map(row => `
        <tr>
            <td>${escapeHTML(row.time)}</td>
            <td>${escapeHTML(row.alt)} m</td>
            <td>${escapeHTML(row.speed)} m/s</td>
            <td>${escapeHTML(row.gps)}</td>
            <td>${escapeHTML(row.battery)}%</td>
            <td>${escapeHTML(row.alerts)}</td>
        </tr>
    `).join('');
}


// Main dashboard update
function update(data) {
    set('clock', new Date().toLocaleTimeString());

    set('connection', data.connection || 'UNKNOWN');

    // Flight data
    const flight = data.flight || {};

    set('altitude', flight.altitude_m ?? '--');
    set('speed', flight.ground_speed_ms ?? '--');

    set('armed', data.armed ? 'ARMED (SIMULATED)' : 'DISARMED (SIMULATED)');

    set('phase', data.vtol_phase || '--');
    set('mode', data.flight_mode || '--');

    set('heading', (flight.heading_deg ?? '--') + '°');
    set('roll', (flight.roll_deg ?? '--') + '°');
    set('pitch', (flight.pitch_deg ?? '--') + '°');
    set('yaw', (flight.yaw_deg ?? '--') + '°');

    set(
        'vertical',
        flight.vertical_speed_ms != null
            ? flight.vertical_speed_ms + ' m/s'
            : '--'
    );

    // Other monitoring modules
    updateGPS(data.gps);
    updateBattery(data.battery);
    updateMotors(data.motors);
    updateLidar(data.lidar);
    updateCommunication(data.communication);

    // Dashboard chart and alerts
    updateChart(flight);

    const alerts = Array.isArray(data.alerts)
        ? data.alerts
        : [];

    updateAlerts(alerts);
    updateHistory(data, flight, alerts);

    set(
        'updated',
        'Updated ' + new Date().toLocaleTimeString()
    );
}


// Request telemetry from Flask
async function poll() {
    try {
        const response = await fetch('/api/telemetry');

        if (!response.ok) {
            throw new Error('Telemetry API error: ' + response.status);
        }

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        update(data);

    } catch (error) {
        set('connection', 'BACKEND DISCONNECTED');
        console.error('Telemetry error:', error);
    }
}


// Start dashboard
window.addEventListener('load', () => {
    initMap();
    initChart();

    poll();

    setInterval(poll, 1500);
});
