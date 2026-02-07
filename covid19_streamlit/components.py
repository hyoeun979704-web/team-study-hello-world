# components.py 3D 지구본/바이러스 JS 래퍼

import streamlit.components.v1 as components

def render_globe_component(timeline_df, cities_list, height=600):
    # 디버깅용: 무조건 빨간 큐브만 렌더링
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <style>
            /* 1. 배경을 분홍색으로 강제 지정해서 영역이 잡히는지 확인 */
            body {{ margin: 0; overflow: hidden; background-color: #ffccd5; }}
            #debug-container {{ width: 100%; height: {height}px; }}
        </style>
    </head>
    <body>
        <div id="debug-container"></div>
        
        <div style="position:absolute; top:10px; left:10px; color:black; font-weight:bold; z-index:999;">
            ✅ 3D 영역이 잡혔습니다. (Three.js 로딩 중...)
        </div>

        <script>
            try {{
                const container = document.getElementById('debug-container');
                
                // 씬 & 카메라
                const scene = new THREE.Scene();
                const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
                camera.position.z = 5;

                // 렌더러
                const renderer = new THREE.WebGLRenderer({{ alpha: true }});
                renderer.setSize(window.innerWidth, {height}); // 높이 강제 지정
                container.appendChild(renderer.domElement);

                // 큐브 (빨간색)
                const geometry = new THREE.BoxGeometry();
                const material = new THREE.MeshBasicMaterial({{ color: 0xff0000, wireframe: true }});
                const cube = new THREE.Mesh(geometry, material);
                scene.add(cube);

                // 애니메이션
                function animate() {{
                    requestAnimationFrame(animate);
                    cube.rotation.x += 0.01;
                    cube.rotation.y += 0.01;
                    renderer.render(scene, camera);
                }}
                animate();
                
            }} catch (e) {{
                // 에러 발생 시 화면에 빨간 글씨로 출력
                document.body.innerHTML += '<div style="color:red; font-size:20px;">JS 에러: ' + e.message + '</div>';
            }}
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=height)

# 바이러스도 동일하게 테스트
def render_virus_component(height=500):
    render_globe_component(None, None, height)