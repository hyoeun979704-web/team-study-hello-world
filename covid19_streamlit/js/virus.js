// js/virus.js

export function initVirus() {
    const container = document.getElementById('virus-canvas-container');
    if (!container) return;

    // 1. 씬 & 카메라 설정
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.z = 16;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);

    // 캔버스 초기화 (중복 방지)
    while (container.firstChild) container.removeChild(container.firstChild);
    container.appendChild(renderer.domElement);

    // 2. 조명
    scene.add(new THREE.AmbientLight(0xffffff, 0.6));
    const mainLight = new THREE.DirectionalLight(0xffffff, 1.0);
    mainLight.position.set(10, 10, 10);
    scene.add(mainLight);

    const rimLight = new THREE.SpotLight(0x3b82f6, 3.0);
    rimLight.position.set(-10, 5, 10);
    scene.add(rimLight);

    // 3. 그룹 및 파츠 저장소
    let virusGroup = new THREE.Group();
    scene.add(virusGroup);
    let parts = { spike: [], envelope: [], membrane: [], lipid: [] };

    // 4. [검증됨] 6종 변이 풀 데이터
    const variantData = {
        original: {
            name: "초기형 (Wild Type)",
            color: 0xe91e63,
            spikeCount: 45,
            transmissibility: "1.0 (기준)",
            description: "2019년 12월 우한에서 처음 발견된 바이러스 원형입니다.<br>모든 변이 비교의 기준점이 됩니다.",
            characteristics: ["ACE2 수용체 결합", "비말 전파", "폐렴 유발 가능성"],
            mutations: "없음 (Reference)",
            differences: "기본 구형 구조"
        },
        alpha: {
            name: "알파 변이 (Alpha)",
            color: 0x4caf50,
            spikeCount: 52,
            transmissibility: "약 1.5배",
            description: "2020년 9월 영국 발견.<br>N501Y 변이로 수용체 결합력이 강해져 초기형보다 빠르게 확산되었습니다.",
            characteristics: ["전파력 50% 증가", "입원 위험 소폭 증가", "PCR S유전자 누락"],
            mutations: "N501Y, P681H",
            differences: "스파이크 결합 각도 변경"
        },
        beta: {
            name: "베타 변이 (Beta)",
            color: 0x9c27b0,
            spikeCount: 50,
            transmissibility: "약 1.5배",
            description: "2020년 5월 남아공 발견.<br>초기 백신과 항체 치료제에 대한 회피 능력을 보여주었습니다.",
            characteristics: ["백신 효능 감소", "항체 저항성", "재감염 위험"],
            mutations: "E484K, K417N",
            differences: "RBD(결합부위) 구조 변형"
        },
        gamma: {
            name: "감마 변이 (Gamma)",
            color: 0xff9800,
            spikeCount: 51,
            transmissibility: "약 1.7배",
            description: "2020년 11월 브라질 확산.<br>남미 지역에서 높은 재감염률을 기록하며 팬데믹의 장기화를 경고했습니다.",
            characteristics: ["높은 재감염률", "남미 지역 중심 확산", "면역 회피"],
            mutations: "K417T, E484K",
            differences: "결합력과 안정성 동시 강화"
        },
        delta: {
            name: "델타 변이 (Delta)",
            color: 0x2196f3,
            spikeCount: 65,
            transmissibility: "약 2.5배",
            description: "2020년 10월 인도 발견.<br>가장 강력한 독성과 전파력으로 팬데믹의 '암흑기'를 주도했습니다.",
            characteristics: ["잠복기 단축(4일)", "높은 입원율", "백신 돌파 감염"],
            mutations: "L452R, P681R",
            differences: "스파이크 밀도 대폭 증가"
        },
        omicron: {
            name: "오미크론 (Omicron)",
            color: 0x06b6d4,
            spikeCount: 90,
            transmissibility: "약 4.0배 이상",
            description: "2021년 11월 남아공.<br>폭발적 전파와 낮은 치명률로 엔데믹(Endemic)으로의 전환점을 만들었습니다.",
            characteristics: ["상기도 감염(인후통)", "폭발적 전파력", "빠른 회복"],
            mutations: "30개 이상 다중 변이",
            differences: "스파이크 단백질 과밀집"
        }
    };

    // 5. 구조 설명 데이터
    const structureInfo = {
        all: { title: "전체 구조", desc: "직경 약 100nm의 구형 바이러스입니다.<br>지질막 표면에 스파이크 단백질이 돋아나 왕관(Corona) 모양을 형성합니다." },
        spike: { title: "스파이크 단백질 (S)", desc: "바이러스 표면의 돌기입니다.<br>인체 세포의 ACE2 수용체와 결합하여 침투를 주도하는 핵심 부위입니다." },
        envelope: { title: "외막 단백질 (E)", desc: "바이러스의 조립과 방출을 돕는 소수 단백질입니다." },
        membrane: { title: "막 단백질 (M)", desc: "바이러스 외피에 가장 많이 존재하며 구조적 안정성을 제공합니다." },
        lipid: { title: "지질 이중막 (Lipid)", desc: "바이러스를 감싸 보호하는 기름막입니다.<br>비누나 알코올에 쉽게 파괴됩니다." }
    };

    // 6. 바이러스 생성 함수 (Cylinder + Sphere 스파이크 / 지질막 투명도 적용됨)
    function buildVirus(variantKey) {
        scene.remove(virusGroup);
        virusGroup = new THREE.Group();
        scene.add(virusGroup);
        parts = { spike: [], envelope: [], membrane: [], lipid: [] };

        const data = variantData[variantKey];
        const R_BODY = 4.5;
        const R_SPIKE = 4.8;

        // (1) Lipid (지질막)
        const lipidGeo = new THREE.SphereGeometry(R_BODY, 64, 64);
        const lipidMat = new THREE.MeshPhongMaterial({
            color: 0x334155,
            transparent: true,
            opacity: 0.95,
            shininess: 30
        });
        const lipid = new THREE.Mesh(lipidGeo, lipidMat);
        lipid.userData = { type: 'lipid' };
        virusGroup.add(lipid);
        parts.lipid.push(lipid);

        // (2) Spikes (스파이크)
        const spikeMat = new THREE.MeshPhongMaterial({ color: data.color });
        for (let i = 0; i < data.spikeCount; i++) {
            const phi = Math.acos(1 - 2 * (i + 0.5) / data.spikeCount);
            const theta = Math.PI * (1 + Math.sqrt(5)) * (i + 0.5);
            const x = R_SPIKE * Math.sin(phi) * Math.cos(theta);
            const y = R_SPIKE * Math.sin(phi) * Math.sin(theta);
            const z = R_SPIKE * Math.cos(phi);

            // 줄기(Cylinder)
            const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.1, 1.2, 8), spikeMat);
            stem.position.set(0, 0.6, 0);

            // 머리(Sphere)
            const head = new THREE.Mesh(new THREE.SphereGeometry(0.25, 10, 10), spikeMat);
            head.position.set(0, 1.2, 0);

            const spikeObj = new THREE.Group();
            spikeObj.add(stem);
            spikeObj.add(head);
            spikeObj.position.set(x, y, z);
            spikeObj.lookAt(0, 0, 0);

            spikeObj.rotateX(Math.PI / 2);
            spikeObj.rotateZ(Math.PI);

            stem.userData = head.userData = { type: 'spike' };
            parts.spike.push(stem, head);
            virusGroup.add(spikeObj);
        }

        // (3) Envelope (외막)
        const envMat = new THREE.MeshPhongMaterial({ color: 0xf97316 });
        for (let i = 0; i < 20; i++) {
            const phi = Math.acos(1 - 2 * (i + 0.5) / 20);
            const theta = Math.PI * (1 + Math.sqrt(5)) * (i + 0.5) + 2;
            const x = (R_BODY + 0.1) * Math.sin(phi) * Math.cos(theta);
            const y = (R_BODY + 0.1) * Math.sin(phi) * Math.sin(theta);
            const z = (R_BODY + 0.1) * Math.cos(phi);

            const env = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.4, 0.4), envMat);
            env.position.set(x, y, z);
            env.lookAt(0, 0, 0);
            env.userData = { type: 'envelope' };
            virusGroup.add(env);
            parts.envelope.push(env);
        }

        // (4) Membrane (막)
        const memMat = new THREE.MeshPhongMaterial({ color: 0x8b5cf6 });
        for (let i = 0; i < 80; i++) {
            const phi = Math.random() * Math.PI;
            const theta = Math.random() * Math.PI * 2;
            const x = (R_BODY + 0.1) * Math.sin(phi) * Math.cos(theta);
            const y = (R_BODY + 0.1) * Math.sin(phi) * Math.sin(theta);
            const z = (R_BODY + 0.1) * Math.cos(phi);

            const mem = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 0.3, 6), memMat);
            mem.position.set(x, y, z);
            mem.lookAt(0, 0, 0);
            mem.rotateX(Math.PI / 2);
            mem.userData = { type: 'membrane' };
            virusGroup.add(mem);
            parts.membrane.push(mem);
        }
    }

    // 7. 하이라이트 함수 (지질막 투명도 예외처리 적용)
    function highlight(target) {
        Object.values(parts).flat().forEach(m => {
            if (target === 'reset' || target === 'all') {
                if (m.userData.type === 'lipid') {
                    m.material.transparent = true;
                    m.material.opacity = 0.95;
                } else {
                    m.material.transparent = false;
                    m.material.opacity = 1.0;
                }
            } else {
                m.material.transparent = true;
                m.material.opacity = 0.1;
            }
        });

        if (target !== 'reset' && target !== 'all' && parts[target]) {
            parts[target].forEach(m => {
                m.material.transparent = false;
                m.material.opacity = 1.0;
                if (m.material.emissive) {
                    m.material.emissive.setHex(0x555555);
                    setTimeout(() => { if (m.material) m.material.emissive.setHex(0x000000); }, 300);
                }
            });
        }
    }

    // 8. [핵심 수정] UI 업데이트 (누락 방지: 요소 존재 여부 체크 후 삽입)
    function updateVariantUI(variantKey) {
        const data = variantData[variantKey];
        if (!data) return;

        const nameEl = document.getElementById('v-name');
        if (nameEl) nameEl.innerText = data.name;

        // [수정 포인트] innerHTML로 변경하여 <br> 적용
        const descEl = document.getElementById('v-desc');
        if (descEl) descEl.innerHTML = data.description;

        const spikeEl = document.getElementById('v-spike-count');
        if (spikeEl) spikeEl.innerText = data.spikeCount;

        const transEl = document.getElementById('v-trans');
        if (transEl) transEl.innerText = data.transmissibility;

        const charList = document.getElementById('v-char-list');
        if (charList) {
            charList.innerHTML = data.characteristics.map(c => `<li>${c}</li>`).join('');
        }

        const mutBox = document.getElementById('v-mutations');
        if (mutBox) {
            mutBox.innerHTML = `<span style="border: 1px solid #${data.color.toString(16)}; padding: 4px 8px; border-radius: 12px; color: #${data.color.toString(16)}; display: inline-block;">${data.mutations}</span>`;
        }

        const diffBox = document.getElementById('v-diff');
        if (diffBox) {
            diffBox.innerText = data.differences;
        }
    }

    // [핵심 수정] UI 업데이트 (innerText -> innerHTML)
    function updateStructureDesc(part) {
        const info = structureInfo[part];
        const titleEl = document.getElementById('structure-title');
        const textEl = document.getElementById('structure-text');

        if (titleEl && textEl && info) {
            titleEl.innerText = info.title;
            // [수정 포인트] innerHTML로 변경하여 <br> 적용
            textEl.innerHTML = info.desc;

            if (part === 'all') titleEl.style.color = '#cbd5e1';
            else if (part === 'lipid') titleEl.style.color = '#94a3b8';
            else titleEl.style.color = '#BF5AF2';
        }
    }

    // 9. 이벤트 리스너
    document.querySelectorAll('.struct-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.struct-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const part = btn.dataset.part;
            highlight(part);
            updateStructureDesc(part);
        });
    });

    document.querySelectorAll('.variant-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.variant-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const variant = btn.dataset.variant;
            buildVirus(variant);
            updateVariantUI(variant);

            document.querySelectorAll('.struct-btn').forEach(b => b.classList.remove('active'));
            document.querySelector('.struct-btn[data-part="all"]').classList.add('active');
            highlight('reset');
            updateStructureDesc('all');
        });
    });

    // 10. 초기 실행
    buildVirus('original');
    updateVariantUI('original');
    updateStructureDesc('all');

    function animate() {
        requestAnimationFrame(animate);
        if (virusGroup) {
            virusGroup.rotation.y += 0.002;
            virusGroup.rotation.x += 0.001;
        }
        renderer.render(scene, camera);
    }
    animate();

    window.addEventListener('resize', () => {
        if (!container) return;
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    });
}