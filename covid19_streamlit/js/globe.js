// js/globe.js

import { cities } from './data.js';

export function initGlobe(timelineData) {
    const container = document.getElementById('globe-container');
    const canvas = document.getElementById('globe-canvas');

    if (!container || !canvas) {
        console.warn("⚠️ 지구본 컨테이너가 없습니다.");
        return;
    }

    // 1. 씬 설정
    const width = container.clientWidth;
    const height = container.clientHeight;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 4000);
    camera.position.z = 280;

    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio);

    // 2. 조명 & 배경
    scene.add(new THREE.AmbientLight(0xffffff, 0.6));
    const sunLight = new THREE.DirectionalLight(0xfff8e1, 1.2);
    sunLight.position.set(1000, 500, 1000);
    scene.add(sunLight);

    // 별 배경
    const starGeo = new THREE.BufferGeometry();
    const posArray = new Float32Array(3000 * 3);
    for (let i = 0; i < 3000 * 3; i++) posArray[i] = (Math.random() - 0.5) * 2500;
    starGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    const stars = new THREE.Points(
        starGeo,
        new THREE.PointsMaterial({ color: 0xffffff, size: 0.7, transparent: true, opacity: 0.6 })
    );
    scene.add(stars);

    // 3. 지구 그룹
    const earthGroup = new THREE.Group();
    scene.add(earthGroup);
    const texLoader = new THREE.TextureLoader();

    // 지구 본체
    const earth = new THREE.Mesh(
        new THREE.SphereGeometry(80, 64, 64),
        new THREE.MeshPhongMaterial({
            map: texLoader.load('https://raw.githubusercontent.com/mrdoob/three.js/master/examples/textures/planets/earth_atmos_2048.jpg'),
            specular: new THREE.Color(0x111111),
            shininess: 10
        })
    );
    earthGroup.add(earth);

    // 구름 (조금 더 입체감 있게 회전 속도 차별화 예정)
    const clouds = new THREE.Mesh(
        new THREE.SphereGeometry(81, 64, 64),
        new THREE.MeshLambertMaterial({
            map: texLoader.load('https://raw.githubusercontent.com/mrdoob/three.js/master/examples/textures/planets/earth_clouds_1024.png'),
            transparent: true,
            opacity: 0.3,
            blending: THREE.AdditiveBlending
        })
    );
    earthGroup.add(clouds);

    // 대기 효과 (Glow)
    const atmosphere = new THREE.Mesh(
        new THREE.SphereGeometry(82, 64, 64),
        new THREE.MeshBasicMaterial({
            color: 0x3b82f6,
            transparent: true,
            opacity: 0.1,
            side: THREE.BackSide,
            blending: THREE.AdditiveBlending
        })
    );
    earthGroup.add(atmosphere);

    // 4. 도시 마커 및 전파 시뮬레이션 설정
    const markersGroup = new THREE.Group();
    earthGroup.add(markersGroup);

    // 우한 좌표 (기준점)
    const originLat = 30.5928;
    const originLng = 114.3055;

    // 두 좌표 간 거리 계산 (단순화된 구면 거리)
    function getDistance(lat1, lng1, lat2, lng2) {
        const R = 6371;
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLon = (lng2 - lng1) * Math.PI / 180;
        const a =
            Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c;
    }

    const cityMeshes = [];

    if (cities) {
        cities.forEach(city => {
            // 위경도 -> 3D 좌표 변환
            const phi = (90 - city.lat) * (Math.PI / 180);
            const theta = (city.lng + 180) * (Math.PI / 180);
            const r = 80;
            const x = -(r * Math.sin(phi) * Math.cos(theta));
            const y = (r * Math.cos(phi));
            const z = (r * Math.sin(phi) * Math.sin(theta));

            // 마커 메쉬 생성
            const geometry = new THREE.SphereGeometry(1.0, 16, 16);
            const material = new THREE.MeshBasicMaterial({
                color: 0xff3366,
                transparent: true,
                opacity: 0.8
            });
            const mesh = new THREE.Mesh(geometry, material);
            mesh.position.set(x, y, z);

            // 도시 이름에 따른 전파 지연(Onset Delay) 계산
            // 우한(0일) -> 가까운 곳/허브(빠름) -> 먼 곳(느림)
            let dist = getDistance(originLat, originLng, city.lat, city.lng);
            let delayDay = Math.floor(dist / 150); // 거리에 따라 지연
            if (city.isOrigin) delayDay = 0;
            if (city.hub) delayDay = Math.max(10, delayDay * 0.5); // 허브는 더 빨리 도달

            // 랜덤성 추가 (자연스러움을 위해)
            delayDay += Math.floor(Math.random() * 15);

            markersGroup.add(mesh);

            cityMeshes.push({
                mesh,
                delay: delayDay,
                baseScale: city.isOrigin ? 2.5 : (city.hub ? 2.0 : 1.5)
            });
        });
    }

    // 5. 보간(Lerp) 함수: 부드러운 데이터 표현
    function lerp(start, end, t) {
        return start * (1 - t) + end * t;
    }

    function getDataAtDay(floatDay) {
        const index = Math.floor(floatDay);
        const nextIndex = Math.min(index + 1, timelineData.length - 1);
        const progress = floatDay - index;

        if (!timelineData[index]) return { date: '', cases: 0, deaths: 0 };

        const current = timelineData[index];
        const next = timelineData[nextIndex];

        return {
            date: current.date, // 날짜는 문자열이라 보간 안 함
            cases: lerp(current.cases, next.cases, progress),
            deaths: lerp(current.deaths, next.deaths, progress)
        };
    }

    // 6. 업데이트 및 렌더링
    let currentDayFloat = 0; // 실수형 날짜 (0.0 ~ )
    let playing = false;
    let speed = 0.1; // 기본 재생 속도

    // UI 요소
    const elDate = document.getElementById('current-date');
    const elMainDate = document.getElementById('current-date-main');
    const elCases = document.getElementById('total-cases');
    const elDay = document.getElementById('current-day');
    const elDeaths = document.getElementById('new-cases'); // 라벨은 신규확진이지만 데이터는 사망자로 매핑 중 (유지)
    const elCities = document.getElementById('affected-cities');
    const slider = document.getElementById('timeline-slider');
    const playBtn = document.getElementById('play-btn');

    function updateVisualization() {
        if (!timelineData || timelineData.length === 0) return;

        // 범위 제한
        if (currentDayFloat >= timelineData.length - 1) {
            currentDayFloat = timelineData.length - 1;
            if (playing) togglePlay(); // 끝까지 가면 정지
        }

        const data = getDataAtDay(currentDayFloat);

        // 텍스트 업데이트
        if (elDate) elDate.innerText = data.date;
        if (elMainDate) elMainDate.innerText = data.date;
        if (elDay) elDay.innerText = Math.floor(currentDayFloat);
        if (elCases) elCases.innerText = Math.floor(data.cases).toLocaleString();
        if (elDeaths) elDeaths.innerText = Math.floor(data.deaths).toLocaleString();

        // 도시 마커 애니메이션
        let activeCities = 0;
        const time = Date.now() * 0.003; // 펄스용 시간

        cityMeshes.forEach((item, i) => {
            // 시뮬레이션: 현재 날짜가 이 도시의 감염 시작일(delay)을 지났는가?
            if (currentDayFloat > item.delay) {
                activeCities++;

                // 감염 진행도 (0 ~ 1)
                // 시작일로부터 100일 동안 서서히 커짐
                const infectionProgress = Math.min((currentDayFloat - item.delay) / 100, 1);

                // 펄스 효과 (확진자가 많을수록 빨라짐)
                const pulseSpeed = 1 + infectionProgress * 3;
                const pulse = Math.sin(time * pulseSpeed + i) * 0.3 + 1; // 0.7 ~ 1.3

                // 최종 크기 = 기본크기 * 진행도 * 펄스
                const scale = item.baseScale * (0.2 + 0.8 * infectionProgress) * pulse;

                item.mesh.visible = true;
                item.mesh.scale.set(scale, scale, scale);

                // 색상 변화: 초기(노랑) -> 심각(빨강)
                const colorLerp = Math.min(infectionProgress * 1.5, 1);
                item.mesh.material.color.setHSL(0.95 - (colorLerp * 0.4), 1.0, 0.5); // 핑크 -> 레드
                item.mesh.material.opacity = 0.6 + (infectionProgress * 0.4);

            } else {
                item.mesh.visible = false;
                item.mesh.scale.set(0.1, 0.1, 0.1);
            }
        });

        if (elCities) elCities.innerText = activeCities;
        if (slider) slider.value = currentDayFloat;
    }

    // 제어 로직
    function togglePlay() {
        playing = !playing;
        if (playBtn) {
            playBtn.innerHTML = playing ? '<span>⏸</span> 정지' : '<span>▶</span> 재생';
            playBtn.classList.toggle('playing', playing);
        }
    }

    if (playBtn) playBtn.onclick = togglePlay;

    if (slider) {
        slider.max = timelineData.length - 1;
        slider.addEventListener('input', (e) => {
            playing = false; // 슬라이더 조작 시 재생 멈춤
            if (playBtn) {
                playBtn.innerHTML = '<span>▶</span> 재생';
                playBtn.classList.remove('playing');
            }
            currentDayFloat = parseFloat(e.target.value);
            updateVisualization();
        });
    }

    // 속도 버튼
    document.querySelectorAll('.speed-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            // [수정] 배속 계수 조정 (기본 0.1 기준)
            const multiplier = parseFloat(btn.dataset.speed);
            speed = 0.1 * multiplier;
        });
    });

    // 마우스 회전 제어
    let isDragging = false;
    let prevX = 0, prevY = 0;

    // 이벤트 타겟을 window가 아닌 캔버스나 컨테이너로 한정해도 됨
    if (canvas) {
        canvas.addEventListener('mousedown', e => {
            isDragging = true;
            prevX = e.clientX;
            prevY = e.clientY;
            canvas.style.cursor = 'grabbing';
        });

        window.addEventListener('mouseup', () => {
            isDragging = false;
            canvas.style.cursor = 'grab';
        });

        window.addEventListener('mousemove', e => {
            if (isDragging) {
                const deltaX = e.clientX - prevX;
                const deltaY = e.clientY - prevY;

                earthGroup.rotation.y += deltaX * 0.005;
                earthGroup.rotation.x += deltaY * 0.005;

                prevX = e.clientX;
                prevY = e.clientY;
            }
        });
    }

    // 애니메이션 루프
    function animate() {
        requestAnimationFrame(animate);

        // 자동 회전 (드래그 안 할 때만, 천천히)
        if (!isDragging) {
            earthGroup.rotation.y += 0.0005;
            clouds.rotation.y += 0.0007; // 구름을 조금 더 빠르게
        }

        if (playing) {
            currentDayFloat += speed;
            updateVisualization();
        } else {
            // 정지 상태에서도 펄스 효과는 계속되도록
            updateVisualization();
        }

        renderer.render(scene, camera);
    }

    animate();

    // 반응형
    window.addEventListener('resize', () => {
        if (!container) return;
        const w = container.clientWidth;
        const h = container.clientHeight;
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
    });
}