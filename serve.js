/* Viewcut static server — no dependencies, mp4/webm safe, range-robust. */
const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = process.env.PORT ? Number(process.env.PORT) : 5174;
const ROOT = __dirname;

const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".mp4": "video/mp4",
  ".webm": "video/webm",
  ".mp3": "audio/mpeg",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
  ".woff2": "font/woff2",
};

const server = http.createServer((req, res) => {
  try {
    if (req.method !== "GET" && req.method !== "HEAD") {
      res.writeHead(405, { allow: "GET, HEAD" });
      return res.end();
    }
    const url = decodeURIComponent(req.url.split("?")[0]);
    let file = path.normalize(path.join(ROOT, url === "/" ? "index.html" : url));
    if (!file.startsWith(ROOT)) {
      res.writeHead(403);
      return res.end("Forbidden");
    }
    if (fs.existsSync(file) && fs.statSync(file).isDirectory()) {
      file = path.join(file, "index.html");
    }
    if (!fs.existsSync(file)) {
      res.writeHead(404, { "content-type": "text/plain; charset=utf-8" });
      return res.end("Not found");
    }
    const ext = path.extname(file).toLowerCase();
    const type = TYPES[ext] || "application/octet-stream";
    const stat = fs.statSync(file);

    let start = 0;
    let end = stat.size - 1;
    let partial = false;
    const range = req.headers.range;
    if (range && /^bytes=/i.test(range)) {
      const m = /^(\d*)-(\d*)$/.exec(range.replace(/^bytes=/i, "").trim());
      if (m) {
        const s = m[1];
        const e = m[2];
        if (s === "" && e !== "") {
          start = Math.max(0, stat.size - Number(e));
        } else {
          start = s === "" ? 0 : Number(s);
          if (e !== "") end = Math.min(Number(e), stat.size - 1);
        }
        if (Number.isNaN(start) || start >= stat.size || start > end) {
          res.writeHead(416, { "content-range": `bytes */${stat.size}` });
          return res.end();
        }
        partial = true;
      }
    }

    const headers = {
      "content-type": type,
      "accept-ranges": "bytes",
      "content-length": partial ? end - start + 1 : stat.size,
    };
    if (partial) headers["content-range"] = `bytes ${start}-${end}/${stat.size}`;
    res.writeHead(partial ? 206 : 200, headers);
    if (req.method === "HEAD") return res.end();

    const stream = fs.createReadStream(file, { start, end });
    stream.on("error", () => {
      if (!res.headersSent) res.writeHead(500);
      res.destroy();
    });
    res.on("close", () => stream.destroy());
    res.on("error", () => stream.destroy());
    stream.pipe(res);
  } catch (err) {
    if (!res.headersSent) {
      res.writeHead(500, { "content-type": "text/plain; charset=utf-8" });
      res.end("Server error: " + err.message);
    } else {
      res.destroy();
    }
  }
});

server.listen(PORT, "127.0.0.1", () => {
  console.log(`Viewcut running → http://localhost:${PORT}`);
});
