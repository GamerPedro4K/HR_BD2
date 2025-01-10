<template>
  <FloatingConfigurator />
  <div class="loading-container">
    <canvas ref="canvas"></canvas>
    <p class="loading-text">Loading...</p>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import gsap from 'gsap';

const canvas = ref(null);

onMounted(() => {
  // Scene, Camera, Renderer
  const scene = new THREE.Scene();
  const renderer = new THREE.WebGLRenderer({
    canvas: canvas.value,
    antialias: true,
    alpha: true,
  });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(window.devicePixelRatio);

  const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );
  camera.position.set(0, 5, 15);
  scene.add(camera);

  // Orbit Controls for interactivity
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;

  // Galaxy Parameters
  const parameters = {
    count: 20000,
    size: 0.02,
    radius: 10,
    branches: 4,
    spin: 1,
    randomness: 1,
    randomnessPower: 3,
    insideColor: new THREE.Color(
      getComputedStyle(document.documentElement)
        .getPropertyValue('--primary-color')
        .trim()
    ),
    outsideColor: new THREE.Color('#000000'),
  };

  let geometry = null;
  let material = null;
  let points = null;

  // Generate Galaxy
  const generateGalaxy = () => {
    if (points !== null) {
      geometry.dispose();
      material.dispose();
      scene.remove(points);
    }

    geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(parameters.count * 3);
    const colors = new Float32Array(parameters.count * 3);

    for (let i = 0; i < parameters.count; i++) {
      const i3 = i * 3;

      // Positions
      const radius = Math.random() * parameters.radius;
      const branchAngle =
        ((i % parameters.branches) / parameters.branches) * Math.PI * 2;
      const spinAngle = radius * parameters.spin;

      const randomX =
        Math.pow(Math.random(), parameters.randomnessPower) *
        (Math.random() < 0.5 ? 1 : -1) *
        parameters.randomness *
        radius;
      const randomY =
        Math.pow(Math.random(), parameters.randomnessPower) *
        (Math.random() < 0.5 ? 1 : -1) *
        parameters.randomness *
        radius;
      const randomZ =
        Math.pow(Math.random(), parameters.randomnessPower) *
        (Math.random() < 0.5 ? 1 : -1) *
        parameters.randomness *
        radius;

      positions[i3] =
        Math.cos(branchAngle + spinAngle) * radius + randomX;
      positions[i3 + 1] = randomY;
      positions[i3 + 2] =
        Math.sin(branchAngle + spinAngle) * radius + randomZ;

      // Colors
      const mixedColor = parameters.insideColor.clone();
      mixedColor.lerp(parameters.outsideColor, radius / parameters.radius);

      colors[i3] = mixedColor.r;
      colors[i3 + 1] = mixedColor.g;
      colors[i3 + 2] = mixedColor.b;
    }

    geometry.setAttribute(
      'position',
      new THREE.BufferAttribute(positions, 3)
    );
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    material = new THREE.PointsMaterial({
      size: parameters.size,
      sizeAttenuation: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
      vertexColors: true,
    });

    points = new THREE.Points(geometry, material);
    scene.add(points);
  };

  generateGalaxy();

  // Animation
  const clock = new THREE.Clock();

  const animate = () => {
    const elapsedTime = clock.getElapsedTime();

    // Rotate galaxy
    points.rotation.y = elapsedTime * 0.1;

    // Update controls
    controls.update();

    // Render
    renderer.render(scene, camera);

    // Request next frame
    requestAnimationFrame(animate);
  };

  animate();

  // GSAP Animation for loading text
  gsap.to('.loading-text', {
    opacity: 0.2,
    duration: 1,
    yoyo: true,
    repeat: -1,
    ease: 'power1.inOut',
  });

  // Handle resize
  window.addEventListener('resize', () => {
    // Update sizes
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    // Update renderer
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
  });
});
</script>

<style scoped>
.loading-container {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

canvas {
  display: block;
  width: 100%;
  height: 100vh;
}

.loading-text {
  position: absolute;
  bottom: 30px;
  width: 100%;
  text-align: center;
  font-size: 2rem;
  color: var(--primary-color);
}
</style>


<!--  <template>
  <FloatingConfigurator />
  <div class="loading-container">
    <canvas ref="canvas"></canvas>
    <p class="loading-text">Loading...</p>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import * as THREE from 'three';
import gsap from 'gsap';

const canvas = ref(null);

onMounted(() => {
  // Scene, Camera, Renderer
  const scene = new THREE.Scene();
  const renderer = new THREE.WebGLRenderer({
    canvas: canvas.value,
    antialias: true,
    alpha: true,
  });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(window.devicePixelRatio);

  const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );
  camera.position.set(0, 0, 50);
  scene.add(camera);

  // Resize handler
  window.addEventListener('resize', () => {
    // Update camera
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    // Update renderer
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
  });

  // Wormhole Parameters
  const particleCount = 5000;
  const particles = new THREE.BufferGeometry();
  const positions = new Float32Array(particleCount * 3);
  const colors = new Float32Array(particleCount * 3);

  const primaryColor = new THREE.Color(
    getComputedStyle(document.documentElement)
      .getPropertyValue('--primary-color')
      .trim()
  );

  for (let i = 0; i < particleCount; i++) {
    const theta = Math.random() * 2 * Math.PI; // Angle around Y-axis
    const radius = Math.random() * 20; // Distance from center
    const y = (Math.random() - 0.5) * 40; // Height along Y-axis

    const x = radius * Math.sin(theta);
    const z = radius * Math.cos(theta);

    positions[i * 3] = x;
    positions[i * 3 + 1] = y;
    positions[i * 3 + 2] = z;

    const color = primaryColor.clone().lerp(new THREE.Color(0x000000), radius / 20);
    colors[i * 3] = color.r;
    colors[i * 3 + 1] = color.g;
    colors[i * 3 + 2] = color.b;
  }

  particles.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  particles.setAttribute('color', new THREE.BufferAttribute(colors, 3));

  const particleMaterial = new THREE.PointsMaterial({
    size: 0.2,
    vertexColors: true,
    transparent: true,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
  });

  const particleSystem = new THREE.Points(particles, particleMaterial);
  scene.add(particleSystem);

  // Animation
  const clock = new THREE.Clock();

  const animate = () => {
    const elapsedTime = clock.getElapsedTime();

    // Rotate particles to create swirling effect
    particleSystem.rotation.y = elapsedTime * 0.2;

    // Animate particles moving towards the center
    const positions = particleSystem.geometry.attributes.position.array;
    for (let i = 0; i < particleCount; i++) {
      const y = positions[i * 3 + 1];
      positions[i * 3 + 1] = y + Math.sin(elapsedTime + i) * 0.05;

      const x = positions[i * 3];
      const z = positions[i * 3 + 2];
      const distance = Math.sqrt(x * x + z * z);

      // Move particles inward
      positions[i * 3] *= 0.99;
      positions[i * 3 + 2] *= 0.99;

      // Reset particles that reach the center
      if (distance < 0.1) {
        const theta = Math.random() * 2 * Math.PI;
        const radius = 20;
        positions[i * 3] = radius * Math.sin(theta);
        positions[i * 3 + 2] = radius * Math.cos(theta);
      }
    }
    particleSystem.geometry.attributes.position.needsUpdate = true;

    // Render
    renderer.render(scene, camera);

    requestAnimationFrame(animate);
  };

  animate();

  // GSAP Animation for loading text
  gsap.to('.loading-text', {
    opacity: 0.2,
    duration: 1,
    yoyo: true,
    repeat: -1,
    ease: 'power1.inOut',
  });

  // Mouse movement interaction
  document.addEventListener('mousemove', (event) => {
    const mouseX = (event.clientX / window.innerWidth - 0.5) * 2;
    const mouseY = (event.clientY / window.innerHeight - 0.5) * 2;

    gsap.to(particleSystem.rotation, {
      x: mouseY * 0.5,
      y: mouseX * 0.5,
      duration: 1,
      ease: 'power1.out',
    });
  });
});
</script>

<style scoped>
.loading-container {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  background-color: #000;
}

canvas {
  display: block;
  width: 100%;
  height: 100vh;
}

.loading-text {
  position: absolute;
  bottom: 30px;
  width: 100%;
  text-align: center;
  font-size: 2rem;
  color: var(--primary-color);
}
</style>
 -->

 