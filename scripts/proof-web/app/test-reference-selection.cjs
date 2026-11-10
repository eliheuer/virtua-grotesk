const assert = require('node:assert/strict');
const {choose} = require('./reference-selection.js');
const face = (min, max = min, path = 'face') => ({minWeight:min, maxWeight:max, path, axes:min === max ? {} : {wght:[min,min,max]}});
assert.equal(choose([face(600),face(500)],550).weight,500);
assert.equal(choose([face(500),face(600)],560).weight,600);
assert.equal(choose([face(400,700)],900).weight,700);
assert.equal(choose([face(400),face(100,900)],400).variable,true);
assert.equal(choose([face(400,400,'b'),face(400,400,'a')],400).face.path,'a');
console.log('Reference weight selection passed');
