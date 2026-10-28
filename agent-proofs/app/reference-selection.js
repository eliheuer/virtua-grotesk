/* Shared selection contract: nearest real weight, lower on ties; variable wins exact ties. */
(function (root) {
  'use strict';
  function choose(faces, requested) {
    const ranked = faces.map(face => {
      const weight = Math.max(face.minWeight, Math.min(face.maxWeight, requested));
      return {face, weight, distance: Math.abs(requested - weight), variable: Boolean(face.axes?.wght)};
    });
    ranked.sort((a, b) => a.distance - b.distance || a.weight - b.weight ||
      Number(b.variable) - Number(a.variable) || (a.face.path < b.face.path ? -1 : a.face.path > b.face.path ? 1 : 0));
    return ranked[0];
  }
  const api = {choose};
  if (typeof module !== 'undefined') module.exports = api;
  else root.ProofReferences = api;
})(globalThis);
