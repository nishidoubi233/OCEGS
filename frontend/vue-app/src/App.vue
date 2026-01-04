<template>
  <a-config-provider :theme="themeConfig">
    <a-layout class="app-layout">
      <!-- Header -->
      <a-layout-header class="app-header">
        <div class="header-content">
          <div class="logo-section">
            <span class="logo-icon">🩺</span>
            <span class="logo-text">OCEGS</span>
          </div>
          <nav class="nav-links">
            <router-link to="/" class="nav-link">Home</router-link>
            <router-link to="/consultation" class="nav-link">Consultation</router-link>
            <!-- Step 2: Auth links -->
            <!-- <router-link to="/login" class="nav-link">Login</router-link> -->
          </nav>
        </div>
      </a-layout-header>

      <!-- Main Content -->
      <a-layout-content class="app-content">
        <router-view />
      </a-layout-content>

      <!-- Footer -->
      <a-layout-footer class="app-footer">
        <p>OCEGS © 2026 - AI-Powered Medical Consultation</p>
        <p class="disclaimer">⚠️ For informational purposes only. Seek professional medical advice for health concerns.</p>
      </a-layout-footer>
    </a-layout>
  </a-config-provider>
</template>

<script setup>
import { theme } from 'ant-design-vue'

// Custom theme matching the user's design (cyan/teal primary color)
const themeConfig = {
  algorithm: theme.defaultAlgorithm,
  token: {
    colorPrimary: '#12c6c6',
    borderRadius: 10,
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
  },
}
</script>

<style>
/* Global Styles */
:root {
  --bg: #f3f6fb;
  --card: #ffffff;
  --text: #1b2a3b;
  --muted: #6b7785;
  --primary: #12c6c6;
  --primary-weak: #e6f8f8;
  --line: #e9eef5;
}

* {
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
  margin: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  color: var(--text);
  background: var(--bg);
}

.app-layout {
  min-height: 100vh;
}

.app-header {
  background: var(--card) !important;
  border-bottom: 1px solid var(--line);
  padding: 0 24px !important;
  height: 64px !important;
  line-height: 64px !important;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  font-size: 24px;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  color: var(--primary);
}

.nav-links {
  display: flex;
  gap: 24px;
}

.nav-link {
  color: var(--text);
  text-decoration: none;
  transition: color 0.2s;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: var(--primary);
}

.app-content {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.app-footer {
  text-align: center;
  background: var(--card) !important;
  border-top: 1px solid var(--line);
  padding: 16px 24px !important;
}

.app-footer p {
  margin: 0;
}

.disclaimer {
  font-size: 12px;
  color: var(--muted);
  margin-top: 4px !important;
}
</style>
