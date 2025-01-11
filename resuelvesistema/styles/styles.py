import reflex as rx
from ..state import State

def equation_system_graph():
    return rx.plotly(
        data=State.graph_data,
        layout={
            "width": "100%",
            "height": "100%",
        },
        config={"responsive": True}
    )

button_style = {
    "width": "100%",
    "bg": "#4299E1",
    "color": "white",
    "_hover": {"bg": "#3182CE"},
}

def ondas_effect():
    return rx.html("""
        <!DOCTYPE html>
            <html lang="en">
            <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dots Animation</title>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: #ffffff00;
        }
        canvas {
            display: block;
        }
    </style>
</head>
<body>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        // Crear escena, cámara y renderizador
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // Crear geometría de puntos
        const gridSize = 60; // Reducido de 70 a 60
        const separation = 0.25; // Reducido de 0.3 a 0.25
        const particles = new THREE.BufferGeometry();
        const particleCount = gridSize * gridSize;
        const positions = new Float32Array(particleCount * 3);

        let index = 0;
        for (let i = 0; i < gridSize; i++) {
            for (let j = 0; j < gridSize; j++) {
                positions[index++] = (i - gridSize / 2) * separation;
                positions[index++] = 0;
                positions[index++] = (j - gridSize / 2) * separation;
            }
        }
        
        particles.setAttribute('position', new THREE.BufferAttribute(positions, 3));

        // Crear material para los puntos
        const particleMaterial = new THREE.PointsMaterial({ color: 0xffa500, size: 0.08 }); // Tamaño reducido de 0.1 a 0.08
        const particleSystem = new THREE.Points(particles, particleMaterial);
        scene.add(particleSystem);

        // Posicionar la cámara
        camera.position.y = 5; 
        camera.position.z = 10;
        camera.rotation.x = -Math.PI / 3;

        let count = 0;

        // Animación personalizada
        function animate() {
            requestAnimationFrame(animate);
            
            // Efecto de onda
            const positions = particleSystem.geometry.attributes.position.array;
            for (let i = 0; i < positions.length; i += 3) {
                const x = positions[i];
                const z = positions[i + 2];
                const distance = Math.sqrt(x * x + z * z);
                positions[i + 1] = Math.sin(distance * 2 + count * 0.1) * 0.25;
            }

            particleSystem.geometry.attributes.position.needsUpdate = true;

            count += 0.1;

            renderer.render(scene, camera);
        }

        animate();

        // Ajustar renderizador al tamaño de la ventana
        window.addEventListener('resize', function() {
            const width = window.innerWidth;
            const height = window.innerHeight;
            renderer.setSize(width, height);
            camera.aspect = width / height;
            camera.updateProjectionMatrix();
        });
    </script>
</body>
</html>
                   """)