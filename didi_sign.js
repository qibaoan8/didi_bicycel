/**
 * Created by admin on 2018/5/2.
 */

function parse(t) {
    for (var e = t.length, n = [], r = 0; r < e; r++)
        n[r >>> 2] |= (255 & t.charCodeAt(r)) << 24 - r % 4 * 8;
    return {"words":n,"sigBytes":e}
}

function doFinalize(text) {
    var t = text
      , e = t.words
      , n = 8 * t.sigBytes
      , r = 8 * t.sigBytes;
    return e[r >>> 5] |= 128 << 24 - r % 32,
    e[14 + (r + 64 >>> 9 << 4)] = Math.floor(n / 4294967296),
    e[15 + (r + 64 >>> 9 << 4)] = n,
    t.sigBytes = 4 * e.length,
    hash_process(t),
    _hash;
}

function hash_process(text,e) {
    var n = text
      , r = text.words
      , o = text.sigBytes
      , a = 16 //text.blockSize 一般都是16
      , u = o / (4 * a);
        e = 112; // 这个值是通过js调试出来的，基本每次都是112，源代码是一个特别复杂的数字算的
        for (var c = 0; c < e; c += a)
            doProcessBlock(r, c);
        c = r.splice(0, e),
        n.sigBytes -= o;
}

function doProcessBlock(t, e) {
    for (var n = _hash.words, r = n[0], a = n[1], i = n[2], u = n[3], c = n[4], s = 0; 80 > s; s++) {
        if (16 > s)
            what_oo[s] = 0 | t[e + s];
        else {
            var f = what_oo[s - 3] ^ what_oo[s - 8] ^ what_oo[s - 14] ^ what_oo[s - 16];
            what_oo[s] = f << 1 | f >>> 31;
        }
        f = (r << 5 | r >>> 27) + c + what_oo[s],
        f = 20 > s ? f + (1518500249 + (a & i | ~a & u)) : 40 > s ? f + (1859775393 + (a ^ i ^ u)) : 60 > s ? f + ((a & i | a & u | i & u) - 1894007588) : f + ((a ^ i ^ u) - 899497514),
        c = u,
        u = i,
        i = a << 30 | a >>> 2,
        a = r,
        r = f;
    }
    n[0] = n[0] + r | 0,
    n[1] = n[1] + a | 0,
    n[2] = n[2] + i | 0,
    n[3] = n[3] + u | 0,
    n[4] = n[4] + c | 0;
}

function stringify(t) {
    var e = t.words;
    t = t.sigBytes;
    for (var n = [], r = 0; r < t; r++) {
        var o = e[r >>> 2] >>> 24 - r % 4 * 8 & 255;
        n.push((o >>> 4).toString(16)),
        n.push((15 & o).toString(16));
    }
    return n.join("");
}

var _hash = {
    "sigBytes":20,
    "words":[
        1732584193,
        4023233417,
        2562383102,
        271733878,
        3285377520
    ]
};

what_oo = [];

// base64_txt = 'aDVhcHAwN2EwMjk0NDc3NmI3NjM4ZTliOTA3OTMzNjN1c2VyUm9sZTF0dGlkaDV0aW1lc3RhbXAxNTI1MjM5NTEyMTY2cXVlcnlSYWRpdXMxMDAwcGluTG5nMTE2LjQ0MzU1cGluTGF0MzkuOTIxOW9zVmVyc2lvbmlPUyAxMC4wLjFvc1R5cGUxbW9iaWxlVHlwZWRldnRvb2xzaHdJZDEwMDAwY2l0eUlkMWFwcFZlcnNpb24xLjAuMGFwcEtleWg1YXBwYmNkMGFmNzQ2MTY5MWMxZTMwYmNkNjEwOThmYXBpVmVyc2lvbjEuMC4wYXBpaHR3LmwubmVhcmJ5VmVoaWNsZXNoNWFwcDA3YTAyOTQ0Nzc2Yjc2MzhlOWI5MDc5MzM2Mw=='
base64_txt = process.argv[2];

test = parse(base64_txt);
data_json = doFinalize(test);

sign = stringify(data_json);
console.log(sign);

