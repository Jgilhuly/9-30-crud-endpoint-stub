const storageKey = 'theme';

function getStoredTheme() {
  try {
    return localStorage.getItem(storageKey);
  } catch (_) {
    return null;
  }
}

function getSystemTheme() {
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
}

function updateToggle(theme) {
  const button = document.getElementById('theme-toggle');
  if (!button) return;
  const isDark = theme === 'dark';
  button.setAttribute('aria-pressed', isDark ? 'true' : 'false');
  button.textContent = isDark ? 'Light mode' : 'Dark mode';
}

function setTheme(theme, persist = true) {
  applyTheme(theme);
  if (persist) {
    try {
      localStorage.setItem(storageKey, theme);
    } catch (_) {}
  }
  updateToggle(theme);
}

function initTheme() {
  const stored = getStoredTheme();
  const initial = stored === 'dark' || stored === 'light' ? stored : getSystemTheme();
  applyTheme(initial);
  updateToggle(initial);

  const button = document.getElementById('theme-toggle');
  if (button) {
    button.addEventListener('click', function () {
      const current = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
      const next = current === 'dark' ? 'light' : 'dark';
      setTheme(next);
    });
  }

  const mql = window.matchMedia('(prefers-color-scheme: dark)');
  const handleChange = function () {
    const pref = getStoredTheme();
    if (pref !== 'dark' && pref !== 'light') {
      const sys = getSystemTheme();
      applyTheme(sys);
      updateToggle(sys);
    }
  };
  if (mql.addEventListener) mql.addEventListener('change', handleChange);
  else if (mql.addListener) mql.addListener(handleChange);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initTheme);
} else {
  initTheme();
}
