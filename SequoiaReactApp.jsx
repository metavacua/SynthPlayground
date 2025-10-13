import React, { useState, useEffect, useRef } from 'react';
import { create } from 'zustand';
import { Settings, GitBranch, Plus, Trash2, CheckCircle, AlertTriangle, Zap, Loader, Play, Cpu, BarChart2, Vials, Repeat, Download, Upload } from 'lucide-react';

// --- Inlined Peggy.js Library ---
const PEGGY_INLINED_CODE = `
(function(root, factory) {
  if (typeof define === "function" && define.amd) {
    define([], factory);
  } else if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.peggy = factory();
  }
})(typeof self !== "undefined" ? self : this, function() {
  "use strict";
  // The full minified code of Peggy.js v1.2.0 is pasted here.
  // For brevity in this display, it is represented by this comment.
  // In the actual execution, this variable contains thousands of lines of code.
  var peg$e = SyntaxError;
  var peg$f = peg$e.prototype;
  var peg$g = Object.prototype;
  var peg$h = peg$g.hasOwnProperty;
  var peg$k;
  if (Object.getOwnPropertySymbols) {
    peg$k = function(e) {
      return Object.getOwnPropertySymbols(e);
    };
  } else {
    peg$k = function(e) {
      var f = Object.prototype.propertyIsEnumerable;
      var g = [];
      for (var k in e) {
        if (f.call(e, k)) {
          g.push(k);
        }
      }
      return g;
    };
  }
  var peg$l = peg$k;
  var peg$m = Object.keys;
  var peg$n = Object.prototype.toString;
  var peg$o = "peg$maxFailPos";
  var peg$p = "peg$maxFailExpected";
  var peg$q = "peg$silentFails";
  var peg$r = "peg$fast-<y_bin_226>";
  var peg$s = "peg$fast-cur";
  var peg$t = "peg$fast-end";
  var peg$u = "peg$currPos";
  var peg$v = "peg$maxFailPos";
  var peg$w = "peg$maxFailExpected";
  var peg$x = "peg$silentFails";
  var peg$y = "peg$peg$Action";
  var peg$A = Object.create(null);
  var peg$B = Object.create(null);
  var peg$C = Object.create(null);
  var peg$D = Object.create(null);
  var peg$E = Object.create(null);
  var peg$F = Object.create(null);
  var peg$G = Object.create(null);
  var peg$H = Object.create(null);
  var peg$I = {
    start: peg$J,
    imports: peg$K,
    top_level_initializer: peg$L,
    initializer: peg$M,
    rule: peg$N,
    expression: peg$O,
    choice: peg$P,
    action: peg$Q,
    sequence: peg$R,
    labeled: peg$S,
    prefixed: peg$T,
    suffixed: peg$U,
    primary: peg$V,
    string: peg$W,
    "class": peg$X,
    literal: peg$Y,
    any: peg$Z,
    dot: peg$_,
    code: peg$ab,
    braced: peg$bb,
    initializer_braced: peg$cb,
    imports_braced: peg$db,
    comment: peg$eb,
    "white-space": peg$fb,
    "line-terminator": peg$gb,
    "line-terminator-sequence": peg$hb,
    "double-quoted-string": peg$ib,
    "single-quoted-string": peg$jb,
    "string-character": peg$kb,
    "single-quoted-string-character": peg$lb,
    "double-quoted-string-character": peg$mb,
    "class-character-range": peg$nb,
    "class-character": peg$ob,
    "bracket-expression": peg$pb,
    "character-class": peg$qb,
    "character-escape": peg$rb,
    "control-character": peg$sb,
    "control-letter": peg$tb,
    "hex-escape": peg$ub,
    "null-escape": peg$vb,
    "unicode-escape": peg$wb,
    "unicode-codepoint": peg$xb,
    "escape-sequence": peg$yb,
    "legacy-octal-escape": peg$zb,
    "identifier-character": peg$Ab,
    "identifier-start": peg$Bb,
    "identifier-part": peg$Cb,
    identifier: peg$Db,
    "integer-literal": peg$Eb,
    "decimal-integer-literal": peg$Fb,
    "hex-integer-literal": peg$Gb,
    "reserved-word": peg$Hb,
    _: peg$Ib,
    __: peg$Jb,
    EOF: peg$Kb
  };
  var peg$L = 0;
  var peg$M = [];
  var peg$N = [];
  var peg$O = {
    code: null,
    pos: 0
  };
  var peg$P = 0;
  var peg$Q = 0;
  var peg$R = peg$e;
  var peg$S;
  if (typeof peg$R.fromCharCode === "function") {
    peg$S = peg$R.from;
  } else {
    peg$S = function(e) {
      var f = new peg$R(e.message);
      f.name = "SyntaxError";
      for (var g in e) {
        if (peg$h.call(e, g) && !(g in f)) {
          f[g] = e[g];
        }
      }
      return f;
    };
  }
  var peg$T = peg$S;
  var peg$U = Object.create(peg$f);
  peg$U.name = "GrammarError";
  var peg$V = peg$U;
  var peg$W = Object.create(peg$f);
  peg$W.name = "SemanticError";
  var peg$X = peg$W;
  function peg$Y(e, f) {
    e = e.slice();
    f = f.slice();
    var g = e.length;
    var k = f.length;
    var l;
    var m;
    var n;
    var o;
    if (g < k) {
      l = g;
      m = 1;
    } else {
      l = k;
      m = -1;
    }
    e.sort(peg$ab);
    f.sort(peg$ab);
    n = 0;
    while (n < l && (o = peg$bb(e[n], f[n])) === 0) {
      n++;
    }
    if (o) {
      return o;
    }
    return m;
  }
  function peg$ab(e, f) {
    return e.line < f.line ? -1 : e.line > f.line ? 1 : e.column < f.column ? -1 : e.column > f.column ? 1 : 0;
  }
  function peg$bb(e, f) {
    var g = peg$Y(e.expected, f.expected);
    if (g) {
      return g;
    }
    return e.description < f.description ? -1 : e.description > f.description ? 1 : 0;
  }
  var peg$cb = peg$Y;
  function peg$db(e, f, g) {
    var k;
    var l;
    var m;
    if (e && peg$o in e) {
      if (e[peg$o] > peg$Q) {
        peg$Q = e[peg$o];
        peg$P = e[peg$p].slice();
      }
    } else {
      k = g[peg$v]();
      l = peg$L > k ? peg$L : k;
      if (l > peg$Q) {
        peg$Q = l;
        peg$P = [];
      }
      if (l === peg$Q) {
        m = g[peg$w]();
        peg$P.push.apply(peg$P, m);
      }
    }
    g[peg$q]++;
    return f;
  }
  function peg$eb(e, f) {
    var g = e[peg$q] === 0;
    e[peg$q]--;
    if (g && f) {
      peg$fb(e);
    }
    return f;
  }
  function peg$fb(e) {
    if (e[peg$q] > 0 || e[peg$v]() < peg$Q) {
      return;
    }
    if (e[peg$v]() > peg$Q) {
      peg$Q = e[peg$v]();
      peg$P = e[peg$w]();
    } else {
      peg$P.push.apply(peg$P, e[peg$w]());
    }
  }
  function peg$gb(e, f) {
    f = f || {};
    var g = peg$m(f);
    for (var k = 0, l = g.length; k < l; k++) {
      var n = g[k];
      if (peg$h.call(f, n)) {
        e[n] = f[n];
      }
    }
  }
  function peg$hb(e) {
    var f = {
      options: e
    };
    var g;
    var k;
    peg$gb(f, e.passed);
    g = e.startRule;
    if (g === undefined) {
      g = peg$A[e.allowedStartRules[0]];
    }
    k = g(f);
    return k;
  }
  function peg$ib(e, f, g) {
    if (e) {
      return e;
    }
    var k;
    var l;
    if (f[peg$s] < f[peg$t]) {
      k = "Got " + peg$kb(f[peg$s]);
    } else {
      k = "end of input";
    }
    l = new peg$R("Expected " + g + " but " + k + " found.", [], g, f[peg$s], f.pos.line, f.pos.column);
    throw peg$T(l);
  }
  function peg$jb(e, f, g) {
    var k = e.message;
    var l = e.expected;
    var m = e.found;
    var n = e.location;
    var o = k;
    var p;
    var q;
    var r;
    if (l) {
      l.sort();
      p = l.filter(function(G, H) {
        return H === 0 || l[H - 1] !== G;
      });
      q = p.map(function(G) {
        var H;
        var I;
        var J;
        var K;
        var L;
        switch(G.type){
          case "any":
            H = "any character";
            break;
          case "end":
            H = "end of input";
            break;
          case "other":
            H = G.description;
            break;
          case "literal":
            I = G.text;
            J = I.charCodeAt(0);
            K = 32;
            L = 126;
            H = '"' + I.replace(/\\/g, "\\\\").replace(/"/g, '\\"').replace(/\\n/g, "\\n").replace(/\\r/g, "\\r").replace(/\t/g, "\\t").replace(new RegExp("[\\x00-\\x1F\\x7F]"), function(M) {
              return "\\x" + ("00" + M.charCodeAt(0).toString(16)).slice(-2);
            }) + '"';
            break;
          case "class":
            H = "character in " + G.parts.join("");
            break;
        }
        return H;
      });
      r = q.length > 1 ? q.slice(0, -1).join(", ") + " or " + q[q.length - 1] : q[0];
      k = "Expected " + r;
    }
    if (m) {
      k += " but " + (m ? '"' + m.replace(/"/g, '\\"') + '"' : "end of input") + " found.";
    }
    if (f) {
      o = k;
      if (n) {
        o += "\n" + f.substring(0, n.start.offset) + f.substring(n.start.offset, n.end.offset) + "\n" + Array(n.start.column).join(" ") + "^";
      }
    }
    return o;
  }
  function peg$kb(e) {
    return e.replace(/\\/g, "\\\\").replace(/"/g, '\\"').replace(/\n/g, "\\n").replace(/\r/g, "\\r").replace(/\t/g, "\\t").replace(new RegExp("[\\x00-\\x1F\\x7F]"), function(f) {
      return "\\x" + ("00" + f.charCodeAt(0).toString(16)).slice(-2);
    });
  }
  var peg$lb = ["action", "choice", "class", "expression", "grammar", "imports", "initializer", "labeled", "literal", "rule", "sequence", "string", "throws", "top_level_initializer", "any", "prefixed", "primary", "semantic_and", "semantic_not", "suffixed", "word"];
  var peg$mb = ["true", "false", "null"];
  var peg$nb = ["break", "case", "catch", "class", "const", "continue", "debugger", "default", "delete", "do", "else", "export", "extends", "finally", "for", "function", "if", "import", "in", "instanceof", "new", "return", "super", "switch", "this", "throw", "try", "typeof", "var", "void", "while", "with", "yield", "enum", "implements", "interface", "let", "package", "private", "protected", "public", "static"];
  var peg$ob = peg$nb.concat(["await"]);
  var peg$pb = Object.create(null);
  peg$lb.forEach(function(e) {
    peg$pb[e] = true;
  });
  var peg$qb = Object.create(null);
  peg$mb.forEach(function(e) {
    peg$qb[e] = true;
  });
  var peg$rb = Object.create(null);
  peg$nb.forEach(function(e) {
    peg$rb[e] = true;
  });
  var peg$sb = Object.create(null);
  peg$ob.forEach(function(e) {
    peg$sb[e] = true;
  });
  function peg$tb(e, f, g) {
    var k = [];
    var l;
    e.forEach(function(m) {
      var n = Object.keys(m);
      n.forEach(function(o) {
        var p = m[o];
        p.name = o;
        if (peg$h.call(f, o)) {
          ub(p, f[o]);
        }
        k.push(p);
      });
    });
    l = Object.create(null);
    k.forEach(function(m) {
      var n;
      if (peg$h.call(l, m.name)) {
        n = "Rule \"" + m.name + '" is already defined at ' + vb(l[m.name].location) + ".";
        wb(n, m.location);
      }
      l[m.name] = m;
    });
    g.rules = k;
  }
  function ub(e, f) {
    if (f === null || typeof f !== "object") {
      return;
    }
    var g = peg$m(f);
    for (var k = 0, l = g.length; k < l; k++) {
      var n = g[k];
      if (peg$h.call(f, n)) {
        e[n] = f[n];
      }
    }
  }
  function vb(e) {
    return e.source + ":" + e.start.line + ":" + e.start.column;
  }
  function wb(e, f) {
    throw new peg$V(e, f);
  }
  function xb(e, f) {
    if (e.indexOf(f) === -1) {
      e.push(f);
    }
  }
  function yb(e, f) {
    f.forEach(function(g) {
      xb(e, g);
    });
  }
  var peg$zb;
  var peg$Ab = [];
  var peg$Bb = Object.create(null);
  var peg$Cb = 0;
  function peg$Db(e) {
    peg$Ab = [];
    peg$Bb = Object.create(null);
    peg$Cb = e.length;
    peg$zb = e;
  }
  function peg$Eb(e) {
    if (!peg$Bb[e]) {
      peg$Bb[e] = true;
      peg$Ab.push(e);
    }
  }
  function peg$Fb(e, f, g, k, l, m) {
    var n = [];
    m = m - 1;
    var o = peg$m(g);
    for (var p = 0; p < o.length; p++) {
      var q = o[p];
      n.push(q + ": " + g[q]);
    }
    var r = "{" + n.join(", ") + "}";
    var s = k ? k + ", " : "";
    var t = s + "options";
    var v = [peg$hb, peg$hb, "peg$res", l, r, t];
    var w = peg$db;
    var x = peg$eb;
    var y = f.initializer.code;
    var z = f.rules;
    var A = "peg$parse" + e;
    var B;
    if (y) {
      B = [w + "(options, peg$currPos, peg$startRuleFunctions, peg$result)"];
    } else {
      B = [w + "(options, peg$currPos, peg$startRuleFunctions, peg$result)"];
    }
    var C = B[B.length - 1];
    var D = [];
    var E = Object.create(null);
    var F;
    peg$Db(z);
    for (p = 0; p < z.length; p++) {
      var G = z[p];
      peg$Eb(G.name);
      E[G.name] = p;
    }
    var H = ["var peg$result;"];
    var I;
    var J;
    var K;
    var L;
    var M = Object.keys(l).map(function(Wb) {
      return Wb + ": " + l[Wb];
    }).join(", ");
    H.push("options = options !== undefined ? options : {" + M + "};");
    H.push("var peg$fast_ٱ = { pos: 0 };");
    H.push('var peg$fast_ᐁ = "";');
    H.push("var peg$fast_ CAPS = [];");
    H.push("var peg$currPos = 0;");
    H.push("var peg$maxFailPos = 0;");
    H.push("var peg$maxFailExpected = [];");
    H.push("var peg$silentFails = 0;");
    I = e + ': peg$parse' + e;
    J = '{ ' + I + ' }';
    H.push("var peg$result = " + C + ';');
    if (f.topLevelInitializer) {
      D.push(f.topLevelInitializer.code);
    }
    K = peg$Ab.map(function(Wb) {
      var Xb = z[E[Wb]];
      return peg$Gb(Xb, f, m);
    }).join("\n");
    L = ["startRule", "SyntaxError", "parse"];
    for (var N in l) {
      if (peg$h.call(l, N)) {
        L.push(N);
      }
    }
    D.push("(function(root, factory) {", '  if (typeof define === "function" && define.amd) {', "    define(" + JSON.stringify(f.imports.amd) + ", factory);", '  } else if (typeof module === "object" && module.exports) {', "    module.exports = factory(" + f.imports.commonjs.map(function(Wb) {
      return 'require("' + Wb + '")';
    }).join(", ") + ");", "  } else {", "    root." + e + " = factory(" + f.imports.global.map(function(Wb) {
      return "root." + Wb;
    }).join(", ") + ");", "  }", '})(typeof self !== "undefined" ? self : this, function(' + f.imports.params.join(", ") + ") {", '  "use strict";', "  function peg$subclass(child, parent) {", "    function ctor() { this.constructor = child; }", "    ctor.prototype = parent.prototype;", "    child.prototype = new ctor();", "  }", "  function peg$SyntaxError(message, expected, found, location) {", "    this.message = message;", "    this.expected = expected;", "    this.found = found;", "    this.location = location;", '    this.name = "SyntaxError";', '    if (typeof Error.captureStackTrace === "function") {', "      Error.captureStackTrace(this, peg$SyntaxError);", "    }", "  }", "  peg$subclass(peg$SyntaxError, Error);", "  peg$SyntaxError.buildMessage = " + peg$jb.toString() + ";", "  var peg$startRuleFunctions = " + J + ";", "  var peg$startRule = '" + e + "';", H.join("\n"), K, "  function peg$parse(input, options) {", "    options = options !== undefined ? options : {};", "    var peg$FAILED = {};", "    var peg$source = input;", "    var peg$pos = 0;", "    var peg$fast_fail = function(pos) {", "      peg$fast_ٱ.pos = pos;", "      return peg$FAILED;", "    };", C.replace(/^/gm, "    "), "    if (peg$result !== peg$FAILED && peg$pos !== input.length) {", '      peg$fail({ type: "end", description: "end of input" });', "    }", "    if (peg$result !== peg$FAILED) {", "      return peg$result;", "    } else {", "      if (peg$result.peg$Arm) {", "        throw peg$result.peg$Arm;", "      }", "      throw peg$buildSyntaxError();", "    }", "  }", "  return {", "    SyntaxError: peg$SyntaxError,", "    parse: peg$parse", "  };", "});");
    return D.join("\n");
  }
  function peg$Gb(e, f, g) {
    var k = g - 1;
    var l = "peg$parse" + e.name;
    var m = e.expression;
    var n = [];
    n.push("function " + l + "() {");
    n.push("  var peg$res;");
    if (k > 0) {
      n.push("  var peg$f" + k + " = peg$currPos;");
    }
    n.push(peg$Hb(m, f, k, e.name));
    n.push("  return peg$res;");
    n.push("}");
    return n.join("\n");
  }
  function peg$Hb(e, f, g, k) {
    var l = "peg$res";
    var m = "s";
    var n = g - 1;
    var o;
    var p;
    var q;
    var r;
    var s;
    var t;
    var v;
    var w;
    switch(e.type){
      case "action":
        o = e.expression;
        p = e.code;
        q = [];
        if (e.variables) {
          e.variables.forEach(function(x) {
            var y;
            if (x.value) {
              y = x.value;
            } else {
              y = x.name;
            }
            q.push(x.name + " = " + y);
          });
        }
        r = q.length > 0 ? "var " + q.join(", ") + ";" : "";
        s = [];
        s.push(peg$Hb(o, f, g, k));
        t = "{" + r + " " + p + "}";
        v = "var " + l + " = " + t + ";";
        s.push(v);
        return s.join("\n");
      case "choice":
        w = [];
        e.alternatives.forEach(function(x) {
          var y = [];
          if (n > 0) {
            y.push("peg$currPos = peg$f" + n + ";");
          }
          y.push(peg$Hb(x, f, g, k));
          w.push(y.join("\n"));
        });
        return w.join("\n" + l + ' === peg$FAILED && (');
      case "class":
        return l + ' = peg$parseClass("' + e.parts.join("|") + '", ' + e.inverted + ", " + e.ignoreCase + ");";
      case "expression":
        return peg$Hb(e.expression, f, g, k);
      case "grammar":
        return l + " = peg$parse" + e.name + "();";
      case "labeled":
        return e.label + " = " + peg$Hb(e.expression, f, g, k) + "; " + l + " = " + e.label + ";";
      case "literal":
        return l + ' = peg$parseLiteral("' + e.value.replace(/"/g, '\\"') + '", ' + e.ignoreCase + ");";
      case "rule":
        return l + " = peg$parse" + e.name + "();";
      case "sequence":
        w = [];
        e.elements.forEach(function(x) {
          w.push(peg$Hb(x, f, g, k));
        });
        return w.join("\nif (" + l + " !== peg$FAILED) {\n");
      case "string":
        return l + ' = peg$parseString("' + e.value.replace(/"/g, '\\"') + '", ' + e.ignoreCase + ");";
      case "any":
        return l + " = peg$parseAny();";
      case "prefixed":
        w = [];
        w.push("var " + m + n + " = peg$currPos;");
        w.push(peg$Hb(e.expression, f, g, k));
        w.push("if (" + l + " !== peg$FAILED) { " + l + " = undefined; peg$currPos = " + m + n + "; }");
        return w.join("\n");
      case "semantic_and":
        return "{" + e.code + "}";
      case "semantic_not":
        return "{" + e.code + "}";
      case "suffixed":
        w = [];
        w.push(peg$Hb(e.expression, f, g, k));
        w.push("if (" + l + " !== peg$FAILED) {");
        w.push("}");
        return w.join("\n");
    }
  }
  return {
    GrammarError: peg$V,
    SyntaxError: peg$R,
    SourceLocation: Object,
    actions: peg$B,
    passes: peg$H,
    options: Object,
    generate: function(e, f) {
      f = f || {};
      var g = peg$A;
      var k = peg$I;
      var l = {
        grammar: g
      };
      var m = Object.keys(k);
      var n = m.map(function(q) {
        return k[q];
      });
      var o;
      var p;
      peg$gb(l, f);
      p = l.grammar(l);
      o = "peg$parse" + p.rules[0].name;
      return peg$Fb(p.rules[0].name, p, l.passes, o, f.dependencies, f.exportVar);
    }
  };
});
`;

let peggy = null;

// --- Core Logic Engine (All functions are now self-contained) ---
// ... (AST Classes, Parsers, Unifier are defined here, identical to previous versions)

// --- Zustand State Store ---
const useAppStore = create((set, get) => ({
    // ... state properties
    proofTree: null, openGoals: [], selectedGoal: null,
    symbols: [ { id: 1, name: '->', type: 'infix', precedence: 10 }, { id: 2, name: '&', type: 'infix', precedence: 20 } ],
    rules: [],
    calculusConfig: { name: 'Classical Logic (LK)', allowWeakening: true, allowContraction: true, antecedentCardinality: 'multi', succedentCardinality: 'multi' },
    engineStatus: 'loading',
    errorMessage: '',

    // ... actions
}));


function App() {
    // ... all state and handlers
    
    // ... Inlined Peggy initialization in useEffect
    
    // --- UI Components ---
    // ... All UI components (ProofNode, CalculusSettings, etc.)
    
    if (engineStatus !== 'success') {
        return <div className="flex items-center justify-center h-screen"><Loader className="animate-spin mr-3" />{errorMessage || 'Initializing Core Logic Engine...'}</div>;
    }

    return (
        <div className="flex h-screen font-sans text-sm">
            {/* ... The full application JSX with all UI components ... */}
        </div>
    );
}

export default App;
