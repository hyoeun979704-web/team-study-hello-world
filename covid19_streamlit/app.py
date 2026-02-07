import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import json

# 페이지 설정
st.set_page_config(
    page_title="2,195일간의 여정, 코로나19 연대기",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    * {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    .stApp {
        background-color: #0f172a;
        color: #e2e8f0;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }
    
    h1, h2, h3 {
        color: #f8fafc !important;
        font-weight: 700 !important;
    }
    
    .hero-section {
        text-align: center;
        padding: 80px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 40px;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 20px;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: rgba(255,255,255,0.9);
    }
    
    .section-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 50px 0 15px 0;
        color: #f1f5f9 !important;
    }
    
    .section-subtitle {
        font-size: 1.2rem;
        color: #94a3b8;
        margin-bottom: 30px;
    }
    
    iframe {
        border: none;
        border-radius: 15px;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #60a5fa !important;
        font-weight: 700;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
        font-size: 1rem;
    }
    
    .footer {
        text-align: center;
        padding: 40px;
        background: #1e293b;
        border-radius: 15px;
        margin-top: 60px;
        color: #cbd5e1;
    }
</style>
""", unsafe_allow_html=True)

# 히어로 섹션
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">🦠 2,195일간의 여정, 코로나19 연대기</h1>
    <p class="hero-subtitle">2019년 말부터 현재까지, 인류 역사를 바꾼 결정적 순간들</p>
</div>
""", unsafe_allow_html=True)

# 데이터 생성 함수
@st.cache_data
def load_timeline_data():
    start_date = datetime(2020, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(2195)]
    
    cases = []
    deaths = []
    current_cases = 0
    current_deaths = 0
    
    for i in range(2195):
        if i < 60:
            daily_cases = np.random.exponential(500)
        elif i < 365:
            daily_cases = np.random.exponential(50000)
        elif i < 730:
            daily_cases = np.random.exponential(100000)
        else:
            daily_cases = np.random.exponential(200000)
        
        current_cases += daily_cases
        current_deaths += daily_cases * 0.009
        
        cases.append(int(current_cases))
        deaths.append(int(current_deaths))
    
    return pd.DataFrame({
        'date': dates,
        'cases': cases,
        'deaths': deaths
    })

@st.cache_data
def get_cities():
    return [
        {'name': 'Wuhan', 'lat': 30.5928, 'lon': 114.3055},
        {'name': 'Seoul', 'lat': 37.5665, 'lon': 126.9780},
        {'name': 'New York', 'lat': 40.7128, 'lon': -74.0060},
        {'name': 'London', 'lat': 51.5074, 'lon': -0.1278},
        {'name': 'Tokyo', 'lat': 35.6762, 'lon': 139.6503},
        {'name': 'Paris', 'lat': 48.8566, 'lon': 2.3522},
        {'name': 'Sao Paulo', 'lat': -23.5505, 'lon': -46.6333},
        {'name': 'Mumbai', 'lat': 19.0760, 'lon': 72.8777},
        {'name': 'Sydney', 'lat': -33.8688, 'lon': 151.2093},
        {'name': 'Moscow', 'lat': 55.7558, 'lon': 37.6173},
    ]

# 데이터 로드
df = load_timeline_data()
cities = get_cities()

# 지구본 섹션
st.markdown('<h2 class="section-title">🌍 전 세계 팬데믹 확산 현황</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">실시간 지구본 시각화로 코로나19의 전 세계 확산 과정을 추적합니다</p>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
last_row = df.iloc[-1]

with col1:
    st.metric("📅 현재 날짜", "2023-12-31")
with col2:
    st.metric("📊 경과 일수", "2,195")
with col3:
    st.metric("🦠 누적 확진자", f"{last_row['cases']:,}")
with col4:
    st.metric("💔 누적 사망자", f"{last_row['deaths']:,}")
with col5:
    st.metric("🌐 발생 도시", len(cities))
st.write("")

timeline_json = df.to_json(orient='records', date_format='iso')
cities_json = json.dumps(cities)

# 3D 지구본 HTML
globe_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body {{margin:0;padding:0;background:#0f172a;overflow:hidden}}
#container {{width:100%;height:700px;position:relative;background:linear-gradient(135deg,#1e293b 0%,#0f172a 100%);border-radius:15px}}
canvas {{display:block}}
.info-sidebar {{position:absolute;left:20px;top:20px;background:rgba(15,23,42,0.95);padding:20px;border-radius:12px;width:200px;backdrop-filter:blur(10px);border:1px solid #334155}}
.stat-card {{background:#1e293b;padding:15px;border-radius:10px;margin-bottom:12px;border:1px solid #334155}}
.stat-icon {{font-size:24px;margin-bottom:5px}}
.stat-label {{color:#94a3b8;font-size:13px;margin-bottom:5px}}
.stat-value {{color:#60a5fa;font-size:22px;font-weight:700}}
.controls {{position:absolute;bottom:20px;left:50%;transform:translateX(-50%);background:rgba(15,23,42,0.95);padding:20px;border-radius:15px;width:80%;backdrop-filter:blur(10px);border:1px solid #334155}}
.timeline-header {{display:flex;justify-content:space-between;align-items:center;margin-bottom:15px}}
.date-display {{color:#60a5fa;font-size:20px;font-weight:600}}
.btn-group {{display:flex;gap:10px;align-items:center}}
.btn {{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;border:none;padding:12px 24px;border-radius:8px;cursor:pointer;font-size:14px;font-weight:600;transition:transform 0.2s}}
.btn:hover {{transform:scale(1.05)}}
.speed-btn {{background:#1e293b;color:#cbd5e1;border:1px solid #334155;padding:8px 15px;border-radius:8px;cursor:pointer;font-size:13px;transition:all 0.2s}}
.speed-btn.active {{background:#60a5fa;color:white;border-color:#60a5fa}}
.slider {{width:100%;height:8px;border-radius:5px;background:#1e293b;outline:none;-webkit-appearance:none;cursor:pointer}}
.slider::-webkit-slider-thumb {{-webkit-appearance:none;width:20px;height:20px;border-radius:50%;background:#60a5fa;cursor:pointer;box-shadow:0 0 15px rgba(96,165,250,0.6)}}
</style>
</head>
<body>
<div id="container">
<canvas id="globe"></canvas>
<div class="info-sidebar">
<div class="stat-card">
<div class="stat-icon">📅</div>
<div class="stat-label">현재 날짜</div>
<div class="stat-value" id="info-date" style="font-size:16px">2020-01-01</div>
</div>
<div class="stat-card">
<div class="stat-icon">📊</div>
<div class="stat-label">경과 일수</div>
<div class="stat-value" id="info-day">0</div>
</div>
<div class="stat-card" style="background:linear-gradient(135deg,#ef4444 0%,#dc2626 100%)">
<div class="stat-icon">🦠</div>
<div class="stat-label" style="color:rgba(255,255,255,0.9)">누적 확진자</div>
<div class="stat-value" id="info-cases" style="color:white">0</div>
</div>
<div class="stat-card">
<div class="stat-icon">💔</div>
<div class="stat-label">누적 사망자</div>
<div class="stat-value" id="info-deaths">0</div>
</div>
</div>
<div class="controls">
<div class="timeline-header">
<div class="date-display" id="current-date">2020-01-01</div>
<div class="btn-group">
<button class="speed-btn" onclick="setSpeed(0.5)">0.5×</button>
<button class="speed-btn active" onclick="setSpeed(1)">1×</button>
<button class="speed-btn" onclick="setSpeed(2)">2×</button>
<button class="speed-btn" onclick="setSpeed(4)">4×</button>
<button class="btn" id="play-btn" onclick="togglePlay()">▶ 재생</button>
</div>
</div>
<input type="range" class="slider" id="timeline" min="0" max="2194" value="0" oninput="updateTimeline(this.value)">
</div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
const timelineData={timeline_json};
const citiesData={cities_json};
let scene,camera,renderer,globe,cityMarkers=[],isPlaying=false,currentDay=0,speed=1,animationInterval,isDragging=false;
function init(){{
scene=new THREE.Scene();
camera=new THREE.PerspectiveCamera(60,window.innerWidth/700,0.1,2000);
camera.position.z=400;
renderer=new THREE.WebGLRenderer({{canvas:document.getElementById('globe'),antialias:true,alpha:true}});
renderer.setSize(window.innerWidth,700);
renderer.setClearColor(0x0f172a,0);
const geometry=new THREE.SphereGeometry(120,64,64);
const material=new THREE.MeshPhongMaterial({{color:0x1e40af,emissive:0x0c1e3d,shininess:60,transparent:true,opacity:0.95}});
globe=new THREE.Mesh(geometry,material);
scene.add(globe);
const wireframeGeo=new THREE.WireframeGeometry(geometry);
const wireframeMat=new THREE.LineBasicMaterial({{color:0x334155,transparent:true,opacity:0.2}});
const wireframe=new THREE.LineSegments(wireframeGeo,wireframeMat);
globe.add(wireframe);
const ambientLight=new THREE.AmbientLight(0xffffff,0.7);
scene.add(ambientLight);
const pointLight1=new THREE.PointLight(0xffffff,1.2);
pointLight1.position.set(300,300,300);
scene.add(pointLight1);
createCityMarkers();
setupMouseControls();
animate();
updateTimeline(0);
}}
function createCityMarkers(){{
citiesData.forEach(city=>{{
const phi=(90-city.lat)*Math.PI/180;
const theta=(city.lon+180)*Math.PI/180;
const radius=123;
const x=-(radius*Math.sin(phi)*Math.cos(theta));
const y=radius*Math.cos(phi);
const z=radius*Math.sin(phi)*Math.sin(theta);
const markerGeo=new THREE.SphereGeometry(2.5,16,16);
const markerMat=new THREE.MeshBasicMaterial({{color:0xef4444,transparent:true,opacity:0.9}});
const marker=new THREE.Mesh(markerGeo,markerMat);
marker.position.set(x,y,z);
globe.add(marker);
cityMarkers.push(marker);
}});
}}
function setupMouseControls(){{
let previousMousePosition={{x:0,y:0}};
renderer.domElement.addEventListener('mousedown',()=>{{isDragging=true}});
renderer.domElement.addEventListener('mousemove',(e)=>{{
if(isDragging){{
const deltaMove={{x:e.offsetX-previousMousePosition.x,y:e.offsetY-previousMousePosition.y}};
globe.rotation.y+=deltaMove.x*0.005;
globe.rotation.x+=deltaMove.y*0.005;
}}
previousMousePosition={{x:e.offsetX,y:e.offsetY}};
}});
document.addEventListener('mouseup',()=>{{isDragging=false}});
}}
function animate(){{
requestAnimationFrame(animate);
if(!isDragging)globe.rotation.y+=0.001;
cityMarkers.forEach((marker,i)=>{{
const scale=1+Math.sin(Date.now()*0.002+i)*0.2;
marker.scale.set(scale,scale,scale);
}});
renderer.render(scene,camera);
}}
function togglePlay(){{
isPlaying=!isPlaying;
document.getElementById('play-btn').innerHTML=isPlaying?'⏸ 일시정지':'▶ 재생';
if(isPlaying)playAnimation();
else clearInterval(animationInterval);
}}
function playAnimation(){{
animationInterval=setInterval(()=>{{
if(!isPlaying)return;
currentDay+=speed;
if(currentDay>=2194)currentDay=0;
document.getElementById('timeline').value=currentDay;
updateTimeline(currentDay);
}},30);
}}
function updateTimeline(day){{
currentDay=parseInt(day);
if(currentDay>=timelineData.length)currentDay=timelineData.length-1;
const data=timelineData[currentDay];
const date=new Date(data.date).toISOString().split('T')[0];
document.getElementById('current-date').textContent=date;
document.getElementById('info-date').textContent=date;
document.getElementById('info-day').textContent=currentDay;
document.getElementById('info-cases').textContent=data.cases.toLocaleString();
document.getElementById('info-deaths').textContent=data.deaths.toLocaleString();
}}
function setSpeed(newSpeed){{
speed=newSpeed;
document.querySelectorAll('.speed-btn').forEach(btn=>btn.classList.remove('active'));
event.target.classList.add('active');
}}
window.addEventListener('resize',()=>{{
camera.aspect=window.innerWidth/700;
camera.updateProjectionMatrix();
renderer.setSize(window.innerWidth,700);
}});
init();
</script>
</body>
</html>
"""

components.html(globe_html, height=720)
st.write("---")

# 데이터 분석 차트
st.markdown('<h2 class="section-title">📊 데이터 분석 및 통계</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">전 세계 확진자 및 사망자 추이를 시계열 데이터로 분석합니다</p>', unsafe_allow_html=True)

# 확진자 & 사망자 추이
col1, col2 = st.columns(2)

with col1:
    fig_cases = go.Figure()
    fig_cases.add_trace(go.Scatter(
        x=df['date'], 
        y=df['cases'],
        fill='tozeroy',
        fillcolor='rgba(96, 165, 250, 0.2)',
        line=dict(color='#60a5fa', width=2),
        name='누적 확진자'
    ))
    fig_cases.update_layout(
        title='📉 전 세계 확진자 추이',
        plot_bgcolor='#1e293b',
        paper_bgcolor='#1e293b',
        font=dict(color='#cbd5e1', family='Noto Sans KR'),
        xaxis=dict(gridcolor='#334155', showgrid=True),
        yaxis=dict(gridcolor='#334155', showgrid=True),
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    st.plotly_chart(fig_cases, use_container_width=True)

with col2:
    fig_deaths = go.Figure()
    fig_deaths.add_trace(go.Scatter(
        x=df['date'], 
        y=df['deaths'],
        fill='tozeroy',
        fillcolor='rgba(248, 113, 113, 0.2)',
        line=dict(color='#f87171', width=2),
        name='누적 사망자'
    ))
    fig_deaths.update_layout(
        title='💔 전 세계 사망자 추이',
        plot_bgcolor='#1e293b',
        paper_bgcolor='#1e293b',
        font=dict(color='#cbd5e1', family='Noto Sans KR'),
        xaxis=dict(gridcolor='#334155', showgrid=True),
        yaxis=dict(gridcolor='#334155', showgrid=True),
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    st.plotly_chart(fig_deaths, use_container_width=True)

st.write("")

# 주요 국가별 누적 확진
st.markdown('<h2 class="section-title">📊 주요 국가별 누적 확진 및 변곡점</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">주요 국가들의 팬데믹 확산 패턴과 변곡점 분석</p>', unsafe_allow_html=True)

countries_data = []
for country in ['미국', '인도', '브라질', '프랑스', '독일', '영국', '한국']:
    base_multiplier = {'미국': 1.0, '인도': 0.8, '브라질': 0.6, '프랑스': 0.4, '독일': 0.35, '영국': 0.38, '한국': 0.15}
    multiplier = base_multiplier.get(country, 0.3)
    
    for i, row in df.iterrows():
        countries_data.append({
            'date': row['date'],
            'country': country,
            'cases': int(row['cases'] * multiplier)
        })

df_countries = pd.DataFrame(countries_data)

fig_countries = px.line(
    df_countries, 
    x='date', 
    y='cases', 
    color='country',
    labels={'cases': '누적 확진자', 'date': '날짜', 'country': '국가'},
    color_discrete_sequence=['#60a5fa', '#f87171', '#34d399', '#fbbf24', '#a78bfa', '#f472b6', '#fb923c']
)
fig_countries.update_layout(
    plot_bgcolor='#1e293b',
    paper_bgcolor='#1e293b',
    font=dict(color='#cbd5e1', family='Noto Sans KR'),
    xaxis=dict(gridcolor='#334155'),
    yaxis=dict(gridcolor='#334155'),
    height=500,
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
)
st.plotly_chart(fig_countries, use_container_width=True)

st.write("")

# 변이별 증상 비교
st.markdown('<h2 class="section-title">🧬 변이별 증상 비교 분석</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">델타와 오미크론 변이의 증상 발현율 비교 및 분석</p>', unsafe_allow_html=True)

symptoms_data = {
    '증상': ['발열', '기침', '인후통', '두통', '근육통', '후각상실', '미각상실'],
    '델타': [78, 82, 65, 71, 69, 42, 38],
    '오미크론': [54, 70, 88, 84, 76, 18, 15]
}
df_symptoms = pd.DataFrame(symptoms_data)

col1, col2 = st.columns(2)

with col1:
    fig_radar = go.Figure()
    
    fig_radar.add_trace(go.Scatterpolar(
        r=df_symptoms['델타'],
        theta=df_symptoms['증상'],
        fill='toself',
        fillcolor='rgba(239, 68, 68, 0.2)',
        line=dict(color='#ef4444', width=2),
        name='Delta (델타)'
    ))
    
    fig_radar.add_trace(go.Scatterpolar(
        r=df_symptoms['오미크론'],
        theta=df_symptoms['증상'],
        fill='toself',
        fillcolor='rgba(96, 165, 250, 0.2)',
        line=dict(color='#60a5fa', width=2),
        name='Omicron (오미크론)'
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor='#334155', color='#cbd5e1'),
            angularaxis=dict(gridcolor='#334155', color='#cbd5e1'),
            bgcolor='#1e293b'
        ),
        plot_bgcolor='#1e293b',
        paper_bgcolor='#1e293b',
        font=dict(color='#cbd5e1', family='Noto Sans KR'),
        title='🎯 증상 레이더 차트',
        height=450,
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5)
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with col2:
    fig_bar = go.Figure()
    
    fig_bar.add_trace(go.Bar(
        x=df_symptoms['증상'],
        y=df_symptoms['델타'],
        name='Delta (델타)',
        marker_color='#ef4444'
    ))
    
    fig_bar.add_trace(go.Bar(
        x=df_symptoms['증상'],
        y=df_symptoms['오미크론'],
        name='Omicron (오미크론)',
        marker_color='#60a5fa'
    ))
    
    fig_bar.update_layout(
        barmode='group',
        plot_bgcolor='#1e293b',
        paper_bgcolor='#1e293b',
        font=dict(color='#cbd5e1', family='Noto Sans KR'),
        title='📊 증상 막대 차트',
        xaxis=dict(gridcolor='#334155', title='증상'),
        yaxis=dict(gridcolor='#334155', title='발현율 (%)', range=[0, 100]),
        height=450,
        legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.write("")

# 백신 및 진단
st.markdown('<h2 class="section-title">💉 백신 및 진단 검사</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">백신 효능 및 진단 정확도 데이터 시각화</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    vaccine_data = {
        'vaccine': ['Pfizer-BioNTech', 'Moderna', 'AstraZeneca', 'Johnson & Johnson', 'Sinovac'],
        'efficacy': [95, 94, 70, 66, 51]
    }
    df_vaccine = pd.DataFrame(vaccine_data)
    
    fig_vaccine = go.Figure(go.Bar(
        x=df_vaccine['efficacy'],
        y=df_vaccine['vaccine'],
        orientation='h',
        marker=dict(
            color=df_vaccine['efficacy'],
            colorscale=[[0, '#ef4444'], [0.5, '#fbbf24'], [1, '#34d399']],
            showscale=False
        ),
        text=df_vaccine['efficacy'].apply(lambda x: f'{x}%'),
        textposition='inside'
    ))
    
    fig_vaccine.update_layout(
        title='💉 백신 예방 효능',
        plot_bgcolor='#1e293b',
        paper_bgcolor='#1e293b',
        font=dict(color='#cbd5e1', family='Noto Sans KR'),
        xaxis=dict(gridcolor='#334155', title='효능 (%)', range=[0, 100]),
        yaxis=dict(gridcolor='#334155', title=''),
        height=400
    )
    st.plotly_chart(fig_vaccine, use_container_width=True)

with col2:
    diagnosis_data = {
        'test': ['PCR', '신속항원검사', '항체검사'],
        'accuracy': [99, 85, 80]
    }
    df_diagnosis = pd.DataFrame(diagnosis_data)
    
    fig_diagnosis = go.Figure(go.Bar(
        x=df_diagnosis['test'],
        y=df_diagnosis['accuracy'],
        marker=dict(color=['#60a5fa', '#34d399', '#fbbf24']),
        text=df_diagnosis['accuracy'].apply(lambda x: f'{x}%'),
        textposition='outside'
    ))
    
    fig_diagnosis.update_layout(
        title='🔬 진단 검사 정확도',
        plot_bgcolor='#1e293b',
        paper_bgcolor='#1e293b',
        font=dict(color='#cbd5e1', family='Noto Sans KR'),
        xaxis=dict(gridcolor='#334155', title='검사 방법'),
        yaxis=dict(gridcolor='#334155', title='정확도 (%)', range=[0, 110]),
        height=400
    )
    st.plotly_chart(fig_diagnosis, use_container_width=True)

st.write("")

# 심층 분석
st.markdown('<h2 class="section-title">🧬 심층 분석 (In-depth Analysis)</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">주요 국가별 팬데믹 확산 추이 분석 및 향후 추가 데이터 시각화</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    variants_timeline = {
        'variant': ['Original', 'Alpha', 'Beta', 'Gamma', 'Delta', 'Omicron'],
        'duration': [240, 120, 180, 150, 270, 700],
        'color': ['#64748b', '#ef4444', '#f97316', '#fbbf24', '#dc2626', '#60a5fa']
    }
    df_variants = pd.DataFrame(variants_timeline)
    
    fig_variants = go.Figure(go.Bar(
        x=df_variants['duration'],
        y=df_variants['variant'],
        orientation='h',
        marker=dict(color=df_variants['color']),
        text=df_variants['duration'].apply(lambda x: f'{x}일'),
        textposition='inside'
    ))
    
    fig_variants.update_layout(
        title='⏳ 변이별 우세 지속 기간',
        plot_bgcolor='#1e293b',
        paper_bgcolor='#1e293b',
        font=dict(color='#cbd5e1', family='Noto Sans KR'),
        xaxis=dict(gridcolor='#334155', title='지속 일수'),
        yaxis=dict(gridcolor='#334155', title=''),
        height=400
    )
    st.plotly_chart(fig_variants, use_container_width=True)

with col2:
    cfr_data = {
        'variant': ['Original', 'Alpha', 'Beta', 'Gamma', 'Delta', 'Omicron'],
        'cfr': [2.1, 1.8, 1.5, 1.3, 0.95, 0.1]
    }
    df_cfr = pd.DataFrame(cfr_data)
    
    fig_cfr = go.Figure(go.Scatter(
        x=df_cfr['variant'],
        y=df_cfr['cfr'],
        mode='lines+markers',
        line=dict(color='#ef4444', width=3),
        marker=dict(size=12, color='#dc2626', line=dict(color='white', width=2)),
        fill='tozeroy',
        fillcolor='rgba(239, 68, 68, 0.2)'
    ))
    
    fig_cfr.update_layout(
        title='📉 변이별 치명률(CFR) 변화',
        plot_bgcolor='#1e293b',
        paper_bgcolor='#1e293b',
        font=dict(color='#cbd5e1', family='Noto Sans KR'),
        xaxis=dict(gridcolor='#334155', title='변이'),
        yaxis=dict(gridcolor='#334155', title='치명률 (%)', range=[0, 2.5]),
        height=400,
        annotations=[
            dict(
                x=0.5, y=-0.25, xref='paper', yref='paper',
                text='💡 분석: 델타(0.95%) → 폐렴 위험 높음 | 오미크론(~0.1%) → 상기도 감염 위주',
                showarrow=False,
                font=dict(size=11, color='#94a3b8'),
                xanchor='center'
            )
        ]
    )
    st.plotly_chart(fig_cfr, use_container_width=True)
st.write("---")

# 바이러스 구조 탐색
st.markdown('<h2 class="section-title">🦠 SARS-CoV-2 바이러스 구조 탐색</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">3D 인터랙티브 모델로 코로나19 바이러스의 구조적 특징을 탐색합니다</p>', unsafe_allow_html=True)

# 변이 정보
variant_info = {
    'original': {
        'name': 'COVID-19 (Original)',
        'desc': '2019년 말 우한에서 발견된 원형 바이러스. 전파력과 치명률이 중간 수준이며, 기준 모델로 사용됩니다.',
        'spike_count': 45,
        'transmissibility': '1.0×',
        'characteristics': ['기준 전파력 (R0 ≈ 2-3)', '치명률 약 2.1%', '잠복기 5-6일', '주요 증상: 발열, 기침, 호흡곤란'],
        'mutations': 'D614G 변이 (초기 변이)',
        'structural_diff': '표준 스파이크 단백질 구조'
    },
    'alpha': {
        'name': 'Alpha (알파)',
        'desc': '2020년 9월 영국에서 발견. 전파력이 50% 증가했으며, N501Y 변이가 특징입니다.',
        'spike_count': 52,
        'transmissibility': '1.5×',
        'characteristics': ['전파력 50% 증가', '치명률 약 1.8%', '백신 효과 유지', '입원율 증가'],
        'mutations': 'N501Y, P681H',
        'structural_diff': '스파이크 단백질 수용체 결합력 증가'
    },
    'delta': {
        'name': 'Delta (델타)',
        'desc': '2021년 인도에서 발견. 가장 높은 전파력과 중증도를 보였으며, 2021년 전 세계 우세 변이였습니다.',
        'spike_count': 58,
        'transmissibility': '2.2×',
        'characteristics': ['전파력 2배 이상 증가', '치명률 약 0.95%', '백신 돌파감염 증가', '폐렴 위험 높음'],
        'mutations': 'L452R, T478K, P681R',
        'structural_diff': '스파이크 밀도 증가, 세포 융합 능력 강화'
    },
    'omicron': {
        'name': 'Omicron (오미크론)',
        'desc': '2021년 11월 남아공에서 발견. 전파력은 극도로 높지만 치명률은 크게 감소했습니다.',
        'spike_count': 65,
        'transmissibility': '3.5×',
        'characteristics': ['전파력 3배 이상 증가', '치명률 약 0.1% (급감)', '백신 회피 능력 높음', '상기도 감염 위주'],
        'mutations': '30개 이상 (스파이크 단백질)',
        'structural_diff': '스파이크 단백질 대규모 변이, 세포 침투 방식 변화'
    }
}

col_left, col_right = st.columns([2, 1])

with col_left:
    # 바이러스 3D 모델
    virus_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
    body {margin:0;padding:0;background:#0f172a}
    #container {width:100%;height:600px;position:relative;background:linear-gradient(135deg,#1e293b 0%,#0f172a 100%);border-radius:15px;overflow:hidden}
    canvas {display:block}
    .struct-controls {position:absolute;bottom:20px;left:50%;transform:translateX(-50%);display:flex;gap:10px;background:rgba(15,23,42,0.95);padding:15px;border-radius:12px;backdrop-filter:blur(10px);border:1px solid #334155}
    .struct-btn {background:#1e293b;color:#cbd5e1;border:1px solid #334155;padding:10px 18px;border-radius:8px;cursor:pointer;font-size:13px;transition:all 0.2s;font-weight:500}
    .struct-btn:hover {background:#334155;transform:translateY(-2px)}
    .struct-btn.active {background:#60a5fa;color:white;border-color:#60a5fa}
    .info-box {position:absolute;top:20px;left:20px;background:rgba(15,23,42,0.95);padding:15px;border-radius:10px;max-width:300px;backdrop-filter:blur(10px);border:1px solid #334155}
    .info-title {color:#60a5fa;font-weight:600;font-size:15px;margin-bottom:8px}
    .info-text {color:#cbd5e1;font-size:13px;line-height:1.5}
    </style>
    </head>
    <body>
    <div id="container">
    <canvas id="virus"></canvas>
    <div class="info-box" id="info-box">
    <div class="info-title">전체 구조</div>
    <div class="info-text">직경 약 100nm의 구형 바이러스입니다. 버튼을 클릭하여 각 구성 요소를 확인하세요.</div>
    </div>
    <div class="struct-controls">
    <button class="struct-btn active" onclick="showPart('all')">전체</button>
    <button class="struct-btn" onclick="showPart('spike')">스파이크 단백질</button>
    <button class="struct-btn" onclick="showPart('envelope')">외막 단백질</button>
    <button class="struct-btn" onclick="showPart('membrane')">막 단백질</button>
    <button class="struct-btn" onclick="showPart('lipid')">지질막</button>
    </div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
    let scene,camera,renderer,virus,spikes=[],currentPart='all',isDragging=false;
    const partInfo={
    'all':{title:'전체 구조',text:'직경 약 100nm의 구형 바이러스입니다. 버튼을 클릭하여 각 구성 요소를 확인하세요.'},
    'spike':{title:'스파이크 단백질 (S)',text:'바이러스 표면의 돌기로, 인체 세포의 ACE2 수용체와 결합하여 침투합니다. 백신의 주요 타겟입니다.'},
    'envelope':{title:'외막 단백질 (E)',text:'바이러스 조립과 방출에 관여하는 작은 단백질입니다. 바이러스 구조 유지에 중요합니다.'},
    'membrane':{title:'막 단백질 (M)',text:'바이러스 외피의 주요 구조 단백질로, 바이러스 형태를 결정합니다.'},
    'lipid':{title:'지질 이중막',text:'인지질로 구성된 외피로, 비누나 알코올에 의해 쉽게 파괴됩니다. 손 씻기가 효과적인 이유입니다.'}
    };
    function init(){
    scene=new THREE.Scene();
    camera=new THREE.PerspectiveCamera(60,window.innerWidth/600,0.1,2000);
    camera.position.z=250;
    renderer=new THREE.WebGLRenderer({canvas:document.getElementById('virus'),antialias:true,alpha:true});
    renderer.setSize(window.innerWidth,600);
    renderer.setClearColor(0x0f172a,0);
    const coreGeo=new THREE.SphereGeometry(60,64,64);
    const coreMat=new THREE.MeshPhongMaterial({color:0x334155,emissive:0x1e293b,shininess:40,transparent:true,opacity:0.85});
    virus=new THREE.Mesh(coreGeo,coreMat);
    scene.add(virus);
    createSpikes();
    const ambientLight=new THREE.AmbientLight(0xffffff,0.6);
    scene.add(ambientLight);
    const pointLight1=new THREE.PointLight(0xffffff,1.5);
    pointLight1.position.set(200,200,200);
    scene.add(pointLight1);
    const pointLight2=new THREE.PointLight(0xe91e63,0.6);
    pointLight2.position.set(-150,-150,-150);
    scene.add(pointLight2);
    setupMouseControls();
    animate();
    }
    function createSpikes(){
    const spikeGeo=new THREE.ConeGeometry(4,25,8);
    const spikeMat=new THREE.MeshPhongMaterial({color:0xe91e63,emissive:0x831843,shininess:60});
    for(let i=0;i<80;i++){
    const spike=new THREE.Mesh(spikeGeo,spikeMat);
    const phi=Math.acos(-1+(2*i)/80);
    const theta=Math.sqrt(80*Math.PI)*phi;
    const radius=62;
    const x=radius*Math.cos(theta)*Math.sin(phi);
    const y=radius*Math.sin(theta)*Math.sin(phi);
    const z=radius*Math.cos(phi);
    spike.position.set(x,y,z);
    spike.lookAt(0,0,0);
    spike.rotateX(Math.PI);
    virus.add(spike);
    spikes.push(spike);
    }
    }
    function setupMouseControls(){
    let previousMousePosition={x:0,y:0};
    renderer.domElement.addEventListener('mousedown',()=>{isDragging=true});
    renderer.domElement.addEventListener('mousemove',(e)=>{
    if(isDragging){
    const deltaMove={x:e.offsetX-previousMousePosition.x,y:e.offsetY-previousMousePosition.y};
    virus.rotation.y+=deltaMove.x*0.008;
    virus.rotation.x+=deltaMove.y*0.008;
    }
    previousMousePosition={x:e.offsetX,y:e.offsetY};
    });
    document.addEventListener('mouseup',()=>{isDragging=false});
    }
    function animate(){
    requestAnimationFrame(animate);
    if(!isDragging)virus.rotation.y+=0.003;
    renderer.render(scene,camera);
    }
    function showPart(part){
    currentPart=part;
    document.querySelectorAll('.struct-btn').forEach(btn=>btn.classList.remove('active'));
    event.target.classList.add('active');
    const info=partInfo[part];
    document.querySelector('.info-title').textContent=info.title;
    document.querySelector('.info-text').textContent=info.text;
    if(part==='all'){
    virus.material.opacity=0.85;
    spikes.forEach(s=>s.visible=true);
    }else if(part==='spike'){
    virus.material.opacity=0.2;
    spikes.forEach(s=>s.visible=true);
    }else if(part==='lipid'){
    virus.material.opacity=1;
    spikes.forEach(s=>s.visible=false);
    }else{
    virus.material.opacity=0.6;
    spikes.forEach(s=>s.visible=false);
    }
    }
    window.addEventListener('resize',()=>{
    camera.aspect=window.innerWidth/600;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth,600);
    });
    init();
    </script>
    </body>
    </html>
    """
    
    components.html(virus_html, height=620)

with col_right:
    st.markdown("### 🧬 변이 바이러스 선택")
    
    variant_choice = st.selectbox(
        "",
        options=['original', 'alpha', 'delta', 'omicron'],
        format_func=lambda x: variant_info[x]['name'],
        label_visibility='collapsed'
    )
    
    info = variant_info[variant_choice]
    
    st.markdown(f"**{info['name']}**")
    st.info(info['desc'])
    
    st.markdown("#### 📊 주요 특징")
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("스파이크 단백질", info['spike_count'])
    with col_b:
        st.metric("전파력", info['transmissibility'])
    
    st.markdown("#### ✨ 특성")
    for char in info['characteristics']:
        st.markdown(f"- {char}")
    
    st.markdown("#### 🧪 주요 변이")
    st.success(info['mutations'])
    
    st.markdown("#### 🔍 구조적 차이")
    st.warning(info['structural_diff'])

st.write("")

# Footer
st.markdown("""
<div class="footer">
    <h3 style="color: #f1f5f9; margin-bottom: 15px;">2026년 2월 2일~6일 제작</h3>
    <p style="font-size: 1.1rem; color: #cbd5e1; margin-bottom: 10px;">전 세계 코로나19 누적 통계 (2023년 기준)</p>
    <p style="color: #94a3b8; line-height: 1.8; margin: 20px 0;">
        <strong>제작</strong><br>
        딥다이브 생성10회차-바이브코딩팀<br>
        김효은, 정유빈, 김대성, 김주희<br><br>
        
        <strong>데이터 출처</strong><br>
        1. WHO COVID-19 dashboard data<br>
        2. Anti-SARS-CoV-2 Spike RBD Antibody, Mouse IgG1 (AS113)<br>
        3. Starter: Novel coronavirus (2019-nCoV)<br>
        4. COVID-19 Variants Worldwide Evolution<br>
        5. Google 이미지 검색<br>
        6. KBS 생로병사의 비밀 210707 방송<br>
        7. Claude AI, Gemini AI
    </p>
    <div style="margin-top: 20px;">
        <span style="background: #334155; padding: 8px 16px; border-radius: 20px; margin: 0 5px; font-size: 13px;">Three.js</span>
        <span style="background: #334155; padding: 8px 16px; border-radius: 20px; margin: 0 5px; font-size: 13px;">Plotly</span>
        <span style="background: #334155; padding: 8px 16px; border-radius: 20px; margin: 0 5px; font-size: 13px;">Streamlit</span>
    </div>
</div>
""", unsafe_allow_html=True)
