/*
 * signDataLoader.js
 * Lightweight runtime loader & cache for sign language preset assets (handshapes & NMF rules).
 * Sources:
 *   Authoritative (domain):   panini/data/sign/*.json  (not fetched at runtime)
 *   Runtime (normalized):     tech/data/presets/*.json (served statically by demo)
 *
 * Responsibilities:
 *  - Fetch and cache JSON presets exactly once
 *  - Provide accessor APIs: getHandshapes(), getHandshape(code), getNmfRules(), validate()
 *  - Basic structural validation with compact error reporting (non-throwing unless fatal)
 *  - Version exposure for telemetry / console logging
 *
 * NOTE: This module intentionally avoids build tooling; plain ES module.
 */

const RUNTIME_PATHS = {
  handshapes: '../../data/presets/handshapes_preset.v0.1.json',
  nmfRules: '../../data/presets/nmf_rules.v0.1.json'
};

const _cache = {
  handshapes: null,      // { version, handshapes: [...] }
  nmfRules: null         // { version, rules: [...] }
};

function _fetchJSON(path) {
  return fetch(path, { cache: 'no-store' })
    .then(r => {
      if (!r.ok) throw new Error(`Failed to fetch ${path}: ${r.status}`);
      return r.json();
    });
}

function _validateHandshapes(json) {
  const errors = [];
  if (!json || typeof json !== 'object') errors.push('root:notObject');
  if (!Array.isArray(json.handshapes)) errors.push('handshapes:notArray');
  else {
    json.handshapes.forEach((h, i) => {
      if (!h.code) errors.push(`handshapes[${i}].code:missing`);
      if (h.angles && typeof h.angles !== 'object') errors.push(`handshapes[${i}].angles:notObject`);
    });
  }
  return errors;
}

function _validateNmfRules(json) {
  const errors = [];
  if (!json || typeof json !== 'object') errors.push('root:notObject');
  if (!Array.isArray(json.rules)) errors.push('rules:notArray');
  else {
    json.rules.forEach((r, i) => {
      if (!r.id) errors.push(`rules[${i}].id:missing`);
      if (!r.if) errors.push(`rules[${i}].if:missing`);
      if (!r.level) errors.push(`rules[${i}].level:missing`);
    });
  }
  return errors;
}

async function loadHandshapes({ force = false } = {}) {
  if (!force && _cache.handshapes) return _cache.handshapes;
  const json = await _fetchJSON(RUNTIME_PATHS.handshapes);
  const errors = _validateHandshapes(json);
  if (errors.length) console.warn('[signDataLoader] handshapes validation warnings:', errors);
  _cache.handshapes = json;
  return json;
}

async function loadNmfRules({ force = false } = {}) {
  if (!force && _cache.nmfRules) return _cache.nmfRules;
  const json = await _fetchJSON(RUNTIME_PATHS.nmfRules);
  const errors = _validateNmfRules(json);
  if (errors.length) console.warn('[signDataLoader] nmfRules validation warnings:', errors);
  _cache.nmfRules = json;
  return json;
}

function getHandshapes() {
  if (!_cache.handshapes) throw new Error('Handshapes not loaded yet – call loadHandshapes() first');
  return _cache.handshapes.handshapes;
}

function getHandshape(code) {
  return getHandshapes().find(h => h.code === code) || null;
}

function getNmfRules() {
  if (!_cache.nmfRules) throw new Error('NMF rules not loaded yet – call loadNmfRules() first');
  return _cache.nmfRules.rules;
}

function getVersions() {
  return {
    handshapes: _cache.handshapes?.version || null,
    nmfRules: _cache.nmfRules?.version || null
  };
}

async function preloadAll() {
  // Parallel load
  await Promise.all([loadHandshapes(), loadNmfRules()]);
  return getVersions();
}

export {
  loadHandshapes,
  loadNmfRules,
  getHandshapes,
  getHandshape,
  getNmfRules,
  getVersions,
  preloadAll
};

export default {
  loadHandshapes,
  loadNmfRules,
  getHandshapes,
  getHandshape,
  getNmfRules,
  getVersions,
  preloadAll
};
