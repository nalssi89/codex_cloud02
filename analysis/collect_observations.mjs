#!/usr/bin/env node
// Fresh station observations; generated data never replace the shipped package.
import https from "node:https";
import { createHash } from "node:crypto";
import { mkdir, readFile, readdir, stat, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createInterface } from "node:readline/promises";
import { gzipSync, gunzipSync } from "node:zlib";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const source = path.join(root, "GLOSEA6_KMA_20220301-20260831_v1");
const destination = path.join(root, "observations", "kmahub_refresh");
const endpoint = "https://apihub.kma.go.kr/api/typ01/url/kma_sfcdd3.php";
const singleEndpoint = "https://apihub.kma.go.kr/api/typ01/url/kma_sfcdd.php";
const revision = "e5c1e0cefbea07021aa294ea1a2789e39216b0e6";

export function parseDaily(body, stationIds, start, end) {
  if (!body.includes("#START7777") || !body.includes("#7777END")) {
    throw new Error("Daily response is incomplete or is not KMA observation data");
  }
  const fields = body.split(/\r?\n/u)
    .map(line => line.match(/^#\s*(\d+)\.\s+([A-Z0-9_]+)\s*:/u))
    .filter(Boolean)
    .sort((a, b) => Number(a[1]) - Number(b[1]))
    .map(match => match[2]);
  for (const name of ["TM", "STN", "TA_AVG", "RN_DAY"]) {
    if (!fields.includes(name)) throw new Error(`Missing response field: ${name}`);
  }
  const rows = [];
  const seen = new Set();
  for (const line of body.split(/\r?\n/u)) {
    const text = line.trim();
    if (!text || text.startsWith("#")) continue;
    const cells = text.includes(",")
      ? text.replace(/,$/u, "").split(",").map(cell => cell.trim())
      : text.split(/\s+/u);
    if (cells.length !== fields.length) throw new Error("Malformed daily observation row");
    const record = Object.fromEntries(fields.map((field, index) => [field, cells[index]]));
    if (!/^\d{8}$/u.test(record.TM) || record.TM < start || record.TM > end) {
      throw new Error("Observation date outside requested period");
    }
    if (!stationIds.has(Number(record.STN))) throw new Error("Unexpected station in response");
    const key = `${record.TM}:${record.STN}`;
    if (seen.has(key)) throw new Error(`Duplicate station/date: ${key}`);
    seen.add(key);
    for (const field of ["TA_AVG", "RN_DAY"]) {
      if (!record[field] || !Number.isFinite(Number(record[field]))) {
        throw new Error(`Non-numeric ${field}: ${key}`);
      }
    }
    rows.push({ date: record.TM, station: Number(record.STN),
      temperature: Number(record.TA_AVG), rain: Number(record.RN_DAY) });
  }
  if (!rows.length) throw new Error("No station observations returned");
  return rows;
}

export function validTemperature(value) {
  // Same missing-value boundary as kmahub's collector; -9 is valid temperature.
  return Number.isFinite(value) && value > -90;
}

export function rainValue(value) {
  // kmahub maps RN_DAY=-9 (no measured precipitation) to zero. Other negative
  // values are not silently clamped: missing/unknown codes are audited.
  if (value === -9) return 0;
  return Number.isFinite(value) && value >= 0 ? value : null;
}

function sha256(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

function requestHTTP(url) {
  return new Promise((resolve, reject) => {
    const call = https.get(url, { timeout: 120000 }, response => {
      const chunks = [];
      response.on("data", chunk => chunks.push(chunk));
      response.on("error", () => reject(new Error("KMA response interrupted")));
      response.on("end", () => {
        if (response.statusCode !== 200) {
          reject(new Error(`KMA HTTP status ${response.statusCode}`));
        } else {
          resolve(Buffer.concat(chunks));
        }
      });
    });
    call.on("timeout", () => call.destroy(new Error("KMA request timeout")));
    // Do not print exceptions carrying a credential-bearing URL.
    call.on("error", error => reject(new Error(`KMA transport failure: ${error.code ?? error.name}`)));
  });
}

// Nested month-to-day fallback must not multiply simultaneous KMA requests.
let requestTail = Promise.resolve();
function request(url) {
  const result = requestTail.then(() => requestHTTP(url));
  requestTail = result.then(() => undefined, () => undefined);
  return result;
}

function dateText(day) {
  return day.toISOString().slice(0, 10).replaceAll("-", "");
}

function calendar(start, end) {
  const dates = [];
  const day = new Date(`${start.slice(0, 4)}-${start.slice(4, 6)}-${start.slice(6, 8)}T00:00:00Z`);
  for (; dateText(day) <= end; day.setUTCDate(day.getUTCDate() + 1)) dates.push(dateText(day));
  return dates;
}

function csv(rows) {
  return `${rows.map(row => row.join(",")).join("\n")}\n`;
}

async function main() {
  const args = process.argv.slice(2);
  if (args.includes("--help")) {
    console.log("Usage: node analysis/collect_observations.mjs [--auth-stdin] [--end YYYYMMDD]\n" +
      "Collect 62-station daily data from 19910101 through the given date (default yesterday).\n" +
      "Use KMA_API_AUTH_KEY or hidden terminal stdin; write observations/kmahub_refresh/.\n" +
      "Does not activate the source or overwrite shipped inputs.");
    return;
  }
  const endIndex = args.indexOf("--end");
  const endArgument = endIndex >= 0 ? args[endIndex + 1] : undefined;
  const allowed = args.filter((_, index) => endIndex < 0 || (index !== endIndex && index !== endIndex + 1));
  if (allowed.some(arg => arg !== "--auth-stdin")) throw new Error("Unexpected arguments; use --help");
  const yesterday = new Date();
  yesterday.setUTCDate(yesterday.getUTCDate() - 1);
  const start = "19910101";
  const end = endArgument ?? dateText(yesterday);
  if (!/^\d{8}$/u.test(end) || end < start || !calendar(end, end).length) {
    throw new Error("Invalid --end date");
  }
  let authKey = process.env.KMA_API_AUTH_KEY;
  if (args.includes("--auth-stdin")) {
    console.log("AUTH_REQUIRED");
    const input = createInterface({ input: process.stdin, terminal: false });
    authKey = (await input.question("")).trim();
    input.close();
  }
  if (!authKey) throw new Error("KMA_API_AUTH_KEY is required");
  const metadata = await readFile(path.join(source, "metadata", "asos_kma_station_list.csv"), "utf8");
  const stations = metadata.trim().split(/\r?\n/u).slice(1).map(line => Number(line.split(",")[0]));
  const stationSet = new Set(stations);
  if (stations.length !== 62 || stationSet.size !== 62) throw new Error("Expected 62 unique stations");
  await mkdir(path.join(destination, "raw"), { recursive: true });
  const dailyRows = [["DATE", "AREA", "T15M", "PRCP", "N_STATION_T15M",
    "N_STATION_PRCP", "N_STATION_REQUIRED", "N_STATION_TOTAL", "QC_T15M", "QC_PRCP"]];
  const stationRows = [["DATE", "STN", "TA_AVG_RAW", "RN_DAY_RAW", "T15M_VALID", "PRCP_VALID", "PRCP"]];
  const gaps = [["DATE", "STN", "ISSUE", "RAW_VALUE"]];
  const requests = [];
  const counts = { temperature: {}, precipitation: {}, station_rows: {} };
  const missingCodes = { temperature: {}, precipitation: {} };
  const started = new Date().toISOString();
  const cachedIntervals = (await readdir(path.join(destination, "raw")))
    .map(name => name.match(/^asos_(\d{8})_(\d{8})\.txt\.gz$/u))
    .filter(Boolean)
    .map(match => ({ start: match[1], end: match[2] }));
  async function fetchRange(from, to, single = false) {
    const rawName = `raw/asos_${from}_${to}.txt.gz`;
    const rawPath = path.join(destination, rawName);
    let packed;
    let bytes;
    let retrieved;
    let downloaded = false;
    let actualEndpoint = single ? singleEndpoint : endpoint;
    try {
      packed = await readFile(rawPath);
      bytes = gunzipSync(packed);
      retrieved = (await stat(rawPath)).mtime.toISOString();
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
      const prefix = cachedIntervals.filter(item => item.start === from && item.end < to)
        .sort((a, b) => b.end.localeCompare(a.end))[0];
      if (prefix) {
        const left = await fetchRange(from, prefix.end);
        const next = new Date(`${prefix.end.slice(0, 4)}-${prefix.end.slice(4, 6)}-${prefix.end.slice(6, 8)}T00:00:00Z`);
        next.setUTCDate(next.getUTCDate() + 1);
        const right = await fetchRange(dateText(next), to);
        return [...left, ...right];
      }
      const url = new URL(actualEndpoint);
      const dates = single ? { tm: from, disp: "1" } : { tm1: from, tm2: to };
      Object.entries({ ...dates, stn: stations.join(":"), help: "1", authKey })
        .forEach(([name, value]) => url.searchParams.set(name, value));
      try {
        bytes = await request(url);
      } catch (failure) {
        if (failure.message !== "KMA HTTP status 504") throw failure;
        if (single) {
          // The observed gateway outage is not missing observation data.
          // Keep this exact day pending in the monitored process until the
          // service responds; never invent or drop its station values.
          let delay = 10000;
          for (;;) {
            console.log(`SERVICE_WAIT date=${from} status=504`);
            await new Promise(resolve => setTimeout(resolve, delay));
            try {
              bytes = await request(url);
              break;
            } catch (again) {
              if (again.message !== "KMA HTTP status 504") throw again;
              delay = Math.min(delay * 2, 60000);
            }
          }
        } else {
          const days = calendar(from, to);
          // The range endpoint timed out even for one date, while the user's
          // single-day endpoint returned all 62 stations for that exact date.
          const collected = [];
          for (let index = 0; index < days.length; index += 3) {
            const results = await Promise.all(days.slice(index, index + 3)
              .map(day => fetchRange(day, day, true)));
            for (const result of results) collected.push(...result);
          }
          return collected;
        }
      }
      packed = gzipSync(bytes);
      retrieved = new Date().toISOString();
      downloaded = true;
    }
    const body = new TextDecoder("euc-kr").decode(bytes);
    if (!downloaded) {
      const dataLine = body.split(/\r?\n/u).find(line => /^\d{8}[,\s]/u.test(line));
      actualEndpoint = dataLine?.includes(",") ? singleEndpoint : endpoint;
    }
    const rows = parseDaily(body, stationSet, from, to);
    // Store only a complete, successfully parsed API response.
    if (downloaded) {
      await writeFile(rawPath, packed);
      cachedIntervals.push({ start: from, end: to });
    }
    requests.push({ start: from, end: to, endpoint: actualEndpoint, stations,
      bytes: bytes.length, sha256: sha256(bytes), relative_path: rawName,
      stored_sha256: sha256(packed), retrieved_at_utc: retrieved, rows: rows.length });
    return rows;
  }
  for (let year = 1991; year <= Number(end.slice(0, 4)); year += 1) {
    const from = `${year}0101`;
    const to = year === Number(end.slice(0, 4)) ? end : `${year}1231`;
    let annualCache = false;
    try {
      annualCache = (await stat(path.join(destination, `raw/asos_${from}_${to}.txt.gz`))).isFile();
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
    const rows = [];
    if (annualCache) {
      rows.push(...await fetchRange(from, to));
    } else {
      // Annual requests hit the API gateway's 504 deadline. Month-sized,
      // independently persisted chunks avoid repeating a failed large query.
      const intervals = [];
      for (let month = 1; month <= 12; month += 1) {
        const monthStart = `${year}${String(month).padStart(2, "0")}01`;
        if (monthStart > to) break;
        const monthEnd = dateText(new Date(Date.UTC(year, month, 0)));
        intervals.push([monthStart, monthEnd > to ? to : monthEnd]);
      }
      for (let index = 0; index < intervals.length; index += 3) {
        const results = await Promise.all(intervals.slice(index, index + 3)
          .map(([a, b]) => fetchRange(a, b)));
        for (const result of results) rows.push(...result);
      }
    }
    rows.sort((a, b) => a.date.localeCompare(b.date) || a.station - b.station);
    const grouped = new Map();
    for (const row of rows) {
      if (!grouped.has(row.date)) grouped.set(row.date, new Map());
      grouped.get(row.date).set(row.station, row);
      const temperatureValid = validTemperature(row.temperature);
      const rain = rainValue(row.rain);
      stationRows.push([row.date, row.station, row.temperature, row.rain,
        Number(temperatureValid), Number(rain !== null), rain ?? ""]);
      if (!temperatureValid) {
        gaps.push([row.date, row.station, "TEMPERATURE_VALUE_MISSING", row.temperature]);
        missingCodes.temperature[row.temperature] = (missingCodes.temperature[row.temperature] ?? 0) + 1;
      }
      if (rain === null) {
        gaps.push([row.date, row.station, "PRECIPITATION_VALUE_MISSING", row.rain]);
        missingCodes.precipitation[row.rain] = (missingCodes.precipitation[row.rain] ?? 0) + 1;
      }
    }
    for (const day of calendar(from, to)) {
      const records = grouped.get(day) ?? new Map();
      const temperatures = [];
      const precipitation = [];
      for (const station of stations) {
        const row = records.get(station);
        if (!row) {
          gaps.push([day, station, "STATION_DATE_ROW_MISSING", ""]);
          continue;
        }
        if (validTemperature(row.temperature)) temperatures.push(row.temperature);
        const rain = rainValue(row.rain);
        if (rain !== null) precipitation.push(rain);
      }
      const t = temperatures.length;
      const p = precipitation.length;
      counts.temperature[t] = (counts.temperature[t] ?? 0) + 1;
      counts.precipitation[p] = (counts.precipitation[p] ?? 0) + 1;
      counts.station_rows[records.size] = (counts.station_rows[records.size] ?? 0) + 1;
      const meanT = t ? temperatures.reduce((sum, value) => sum + value, 0) / t : NaN;
      const meanP = p ? precipitation.reduce((sum, value) => sum + value, 0) / p : NaN;
      dailyRows.push([day, "kma", meanT, meanP, t, p, 50, 62,
        t >= 50 ? "OK" : "INSUFFICIENT_VALID_STATIONS",
        p >= 50 ? "OK" : "INSUFFICIENT_VALID_STATIONS"]);
    }
    console.log(`COLLECT ${year} rows=${rows.length} expected=${calendar(from, to).length * 62}`);
  }
  const daily = gzipSync(Buffer.from(csv(dailyRows)));
  const stationData = gzipSync(Buffer.from(csv(stationRows)));
  await writeFile(path.join(destination, "asos_kma_daily.csv.gz"), daily);
  await writeFile(path.join(destination, "station_daily.csv.gz"), stationData);
  await writeFile(path.join(destination, "coverage_gaps.csv"), csv(gaps));
  const provenance = {
    source_policy: "Fresh KMA API Hub station-date observations; source values > -90 for temperature; " +
      "RN_DAY=-9 maps to zero following kmahub; other negative rain values excluded and audited. " +
      "Daily equal-weight means of actual valid contributors, minimum50, no imputation or 62/n scaling.",
    source_start: start, source_end: end, source_daily_sha256: sha256(daily),
    station_daily_sha256: sha256(stationData), stations, retrieved_at_utc: new Date().toISOString(),
    retrieval_started_at_utc: started, endpoint, secondary_endpoint: singleEndpoint,
    repository: "https://github.com/nalssi89/kmahub",
    repository_revision: revision, daily_rows: dailyRows.length - 1,
    station_date_rows: stationRows.length - 1, expected_station_date_rows: (dailyRows.length - 1) * 62,
    counts, missing_codes: missingCodes, gap_records: gaps.length - 1,
    precipitation_code_policy_reference: "scripts/collect-south-korea-may-2026.js:102-111",
    required_stations_policy: "Preserves supplied package minimum50; NOT a KMA API QC flag.",
    qc_flag_origin: "Derived validity/count checks on returned measurements, not independent instrument QC.",
    requests: requests.sort((a, b) => a.start.localeCompare(b.start)),
  };
  await writeFile(path.join(destination, "provenance.json"), `${JSON.stringify(provenance, null, 2)}\n`);
  // A compact machine-readable audit is separate from provenance.
  await writeFile(path.join(destination, "coverage_audit.json"),
    `${JSON.stringify({ ...provenance, requests: undefined }, null, 2)}\n`);
  console.log(`COMPLETE ${JSON.stringify({ daily_rows: provenance.daily_rows,
    station_date_rows: provenance.station_date_rows, counts, gap_records: provenance.gap_records })}`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch(error => {
    console.error(`ERROR ${error.message}`);
    process.exitCode = 1;
  });
}
