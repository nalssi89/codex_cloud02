"""한반도 일일 예보 지도 생성기.

Open-Meteo API(키 불필요)에서 한반도 격자 예보를 받아
cartopy 지도와 서울 시계열 그래프를 그리고, 정적 웹페이지(site/)를 만든다.
GitHub Actions에서 매일 실행되어 GitHub Pages로 게시된다.

로컬 실행:  python daily_forecast/forecast.py --out daily_forecast/site
"""

from __future__ import annotations

import argparse
import html
import json
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import requests  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.colors import BoundaryNorm  # noqa: E402

API = "https://api.open-meteo.com/v1/forecast"
KST = timezone(timedelta(hours=9))

# 한반도 격자 (0.5° 간격)
LATS = np.round(np.arange(33.0, 39.01, 0.5), 2)
LONS = np.round(np.arange(124.5, 130.51, 0.5), 2)
EXTENT = [124.3, 130.7, 32.8, 39.2]
DAYS = 3
CHUNK = 60  # 한 번 요청에 담을 지점 수

# 기상청 모델 우선, 실패하면 Open-Meteo 기본(best_match)으로 대체
MODELS = ["kma_seamless", None]

CITIES = {
    "서울": (37.57, 126.98),
    "강릉": (37.75, 128.89),
    "대전": (36.35, 127.38),
    "광주": (35.16, 126.85),
    "대구": (35.87, 128.60),
    "부산": (35.18, 129.08),
    "제주": (33.50, 126.53),
}

DAILY_VARS = ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"]


def setup_font() -> None:
    names = {f.name for f in font_manager.fontManager.ttflist}
    for cand in ("NanumGothic", "NanumBarunGothic", "Noto Sans CJK KR", "Malgun Gothic"):
        if cand in names:
            plt.rcParams["font.family"] = cand
            break
    plt.rcParams["axes.unicode_minus"] = False


def get_json(params: dict, retries: int = 4) -> dict | list:
    for i in range(retries):
        try:
            r = requests.get(API, params=params, timeout=60)
            data = r.json()
            if isinstance(data, dict) and data.get("error"):
                raise RuntimeError(data.get("reason", "Open-Meteo error"))
            r.raise_for_status()
            return data
        except Exception as exc:  # noqa: BLE001
            if i == retries - 1:
                raise
            wait = 5 * (i + 1)
            print(f"  요청 실패({exc}); {wait}초 후 재시도")
            time.sleep(wait)
    raise RuntimeError("unreachable")


def fetch_grid(model: str | None) -> dict:
    """격자 전 지점의 일별 예보를 받아 (변수, 일, 위도, 경도) 배열로 반환."""
    lat2d, lon2d = np.meshgrid(LATS, LONS, indexing="ij")
    flat_lat, flat_lon = lat2d.ravel(), lon2d.ravel()
    results: list[dict] = []
    for s in range(0, flat_lat.size, CHUNK):
        params = {
            "latitude": ",".join(f"{v:.2f}" for v in flat_lat[s : s + CHUNK]),
            "longitude": ",".join(f"{v:.2f}" for v in flat_lon[s : s + CHUNK]),
            "daily": ",".join(DAILY_VARS),
            "timezone": "Asia/Seoul",
            "forecast_days": DAYS,
        }
        if model:
            params["models"] = model
        data = get_json(params)
        results.extend(data if isinstance(data, list) else [data])
        time.sleep(1)

    dates = results[0]["daily"]["time"]
    out = {"dates": dates}
    for v in DAILY_VARS:
        arr = np.array(
            [[np.nan if x is None else x for x in res["daily"][v]] for res in results],
            dtype=float,
        )  # (지점, 일)
        out[v] = arr.T.reshape(len(dates), LATS.size, LONS.size)
    if np.all(np.isnan(out["temperature_2m_max"])):
        raise RuntimeError(f"모델 {model}: 자료가 모두 비어 있음")
    return out


def fetch_city_hourly(lat: float, lon: float, model: str | None) -> dict:
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,precipitation",
        "timezone": "Asia/Seoul",
        "forecast_days": 7,
    }
    if model:
        params["models"] = model
    return get_json(params)["hourly"]


def fetch_all() -> tuple[dict, dict, str]:
    last_exc: Exception | None = None
    for model in MODELS:
        label = model or "best_match"
        try:
            print(f"격자 예보 요청 (모델: {label}, {LATS.size * LONS.size}개 지점)")
            grid = fetch_grid(model)
            seoul = fetch_city_hourly(*CITIES["서울"], model)
            return grid, seoul, label
        except Exception as exc:  # noqa: BLE001
            print(f"  모델 {label} 실패: {exc}")
            last_exc = exc
    raise SystemExit(f"모든 모델 요청 실패: {last_exc}")


# ---------------------------------------------------------------- 그림

TEMP_LEVELS = np.arange(-20, 38, 2)
PRECIP_LEVELS = [0.1, 1, 5, 10, 20, 30, 50, 80, 120]
WEEKDAY = "월화수목금토일"


def day_label(iso: str) -> str:
    d = datetime.fromisoformat(iso)
    return f"{d.month}/{d.day}({WEEKDAY[d.weekday()]})"


def nearest(lat: float, lon: float) -> tuple[int, int]:
    return int(np.abs(LATS - lat).argmin()), int(np.abs(LONS - lon).argmin())


def map_panels(field: np.ndarray, dates: list[str], title: str, cmap, levels,
               unit: str, fmt: str, path: Path, extend: str) -> None:
    proj = ccrs.PlateCarree()
    fig, axes = plt.subplots(1, len(dates), figsize=(4.6 * len(dates), 5.4),
                             subplot_kw={"projection": proj}, constrained_layout=True)
    norm = BoundaryNorm(levels, cmap.N, extend=extend)
    for ax, i in zip(np.atleast_1d(axes), range(len(dates))):
        ax.set_extent(EXTENT, crs=proj)
        cf = ax.contourf(LONS, LATS, field[i], levels=levels, cmap=cmap, norm=norm,
                         extend=extend, transform=proj)
        ax.add_feature(cfeature.COASTLINE.with_scale("50m"), linewidth=0.7, edgecolor="#333")
        ax.add_feature(cfeature.BORDERS.with_scale("50m"), linewidth=0.5,
                       edgecolor="#555", linestyle=":")
        gl = ax.gridlines(draw_labels=True, linewidth=0.3, color="#999", alpha=0.6)
        gl.top_labels = gl.right_labels = False
        gl.xlabel_style = gl.ylabel_style = {"size": 8, "color": "#555"}
        for name, (la, lo) in CITIES.items():
            j, k = nearest(la, lo)
            val = field[i, j, k]
            if np.isnan(val):
                continue
            ax.plot(lo, la, "o", ms=3, color="#111", transform=proj)
            ax.text(lo + 0.12, la + 0.08, f"{name} {val:{fmt}}", fontsize=8,
                    transform=proj, color="#111",
                    bbox={"boxstyle": "round,pad=0.15", "fc": "white", "ec": "none", "alpha": 0.75})
        ax.set_title(f"{title} · {day_label(dates[i])}", fontsize=12, fontweight="bold")
    cb = fig.colorbar(cf, ax=axes, orientation="horizontal", shrink=0.6, pad=0.02, aspect=40)
    cb.set_label(unit)
    fig.savefig(path, dpi=110)
    plt.close(fig)


def meteogram(hourly: dict, path: Path) -> None:
    t = [datetime.fromisoformat(x) for x in hourly["time"]]
    temp = np.array([np.nan if v is None else v for v in hourly["temperature_2m"]], float)
    pr = np.array([np.nan if v is None else v for v in hourly["precipitation"]], float)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(11, 5.6), sharex=True,
                                 gridspec_kw={"height_ratios": [2, 1]}, constrained_layout=True)
    a1.plot(t, temp, color="#c4452f", lw=2)
    a1.set_ylabel("기온 (°C)")
    span = np.nanmax(temp) - np.nanmin(temp)
    a1.set_ylim(np.nanmin(temp) - 0.15 * span - 1, np.nanmax(temp) + 0.15 * span + 1)
    a1.set_title("서울 7일 시간별 예보", fontsize=13, fontweight="bold", loc="left")
    imax, imin = np.nanargmax(temp), np.nanargmin(temp)
    for idx, va in ((imax, "bottom"), (imin, "top")):
        a1.plot(t[idx], temp[idx], "o", ms=6, color="#c4452f", mec="white", mew=1.5)
        a1.annotate(f"{temp[idx]:.1f}°C", (t[idx], temp[idx]), xytext=(0, 6 if va == "bottom" else -6),
                    textcoords="offset points", ha="center", va=va, fontsize=9)
    a2.bar(t, pr, width=1 / 24 * 0.8, color="#2f6fb0")
    a2.set_ylabel("강수 (mm/h)")
    a2.set_ylim(0, max(1.0, np.nanmax(pr) * 1.2 if np.isfinite(np.nanmax(pr)) else 1.0))
    for ax in (a1, a2):
        ax.grid(axis="y", color="#ddd", lw=0.6)
        ax.spines[["top", "right"]].set_visible(False)
        for d in range(1, 8):
            ax.axvline(t[0] + timedelta(days=d), color="#bbb", lw=0.6, ls="--")
    a2.xaxis.set_major_locator(matplotlib.dates.DayLocator())
    a2.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
        lambda x, _: day_label(matplotlib.dates.num2date(x).strftime("%Y-%m-%d"))))
    fig.savefig(path, dpi=110)
    plt.close(fig)


# ---------------------------------------------------------------- 웹페이지

PAGE = """<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>한반도 일일 예보</title>
<style>
:root{{--bg:#f7f7f5;--card:#fff;--ink:#1d1d1b;--muted:#666;--line:#e3e3df}}
@media (prefers-color-scheme:dark){{:root{{--bg:#151515;--card:#1f1f1f;--ink:#eee;--muted:#aaa;--line:#333}}
img{{background:#fff;border-radius:6px}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:system-ui,-apple-system,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;line-height:1.55}}
main{{max-width:1100px;margin:0 auto;padding:24px 16px 48px}}
h1{{margin:0 0 4px;font-size:1.6rem}} .meta{{color:var(--muted);font-size:.9rem;margin-bottom:20px}}
section{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;margin:16px 0}}
h2{{margin:0 0 10px;font-size:1.1rem}} img{{width:100%;height:auto;display:block}}
table{{border-collapse:collapse;width:100%;font-size:.92rem}} th,td{{padding:6px 8px;border-bottom:1px solid var(--line);text-align:right}}
th:first-child,td:first-child{{text-align:left}} .wrap{{overflow-x:auto}}
footer{{color:var(--muted);font-size:.8rem;margin-top:24px}}
</style></head><body><main>
<h1>한반도 일일 예보</h1>
<div class="meta">갱신: {updated} KST · 모델: {model} · 자료: Open-Meteo</div>
<section><h2>주요 도시 요약</h2><div class="wrap"><table>
<thead><tr><th>도시</th>{head}</tr></thead><tbody>{rows}</tbody></table></div>
<p class="meta" style="margin:8px 0 0">최저 / 최고 기온(°C) · 일강수량(mm), 0.5° 격자의 가장 가까운 지점 값</p></section>
<section><h2>최고기온</h2><img src="tmax.png" alt="최고기온 지도"></section>
<section><h2>최저기온</h2><img src="tmin.png" alt="최저기온 지도"></section>
<section><h2>일강수량</h2><img src="precip.png" alt="일강수량 지도"></section>
<section><h2>서울 7일 시간별</h2><img src="seoul.png" alt="서울 시간별 기온과 강수"></section>
<footer>GitHub Actions가 매일 자동으로 생성합니다. 원자료: <a href="data.json">data.json</a></footer>
</main></body></html>
"""


def build_page(out: Path, grid: dict, model: str) -> None:
    dates = grid["dates"]
    head = "".join(f"<th>{day_label(d)}</th>" for d in dates)
    rows, summary = [], {}
    for name, (la, lo) in CITIES.items():
        j, k = nearest(la, lo)
        cells, summary[name] = [], []
        for i in range(len(dates)):
            tn = float(grid["temperature_2m_min"][i, j, k])
            tx = float(grid["temperature_2m_max"][i, j, k])
            pr = float(grid["precipitation_sum"][i, j, k])
            cells.append(f"<td>{tn:.0f} / {tx:.0f}° · {pr:.1f}</td>")
            summary[name].append({"date": dates[i], "tmin": tn, "tmax": tx, "precip": pr})
        rows.append(f"<tr><td>{html.escape(name)}</td>{''.join(cells)}</tr>")
    updated = datetime.now(KST).strftime("%Y-%m-%d %H:%M")
    (out / "index.html").write_text(
        PAGE.format(updated=updated, model=html.escape(model), head=head, rows="".join(rows)),
        encoding="utf-8")
    (out / "data.json").write_text(json.dumps(
        {"updated_kst": updated, "model": model, "dates": dates,
         "lats": LATS.tolist(), "lons": LONS.tolist(), "cities": summary,
         "grid": {v: np.where(np.isnan(grid[v]), None, np.round(grid[v], 1)).tolist()
                  for v in DAILY_VARS}},
        ensure_ascii=False), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="daily_forecast/site")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    setup_font()

    grid, seoul, model = fetch_all()
    dates = grid["dates"]
    print("그림 생성")
    map_panels(grid["temperature_2m_max"], dates, "일 최고기온", plt.get_cmap("RdBu_r"),
               TEMP_LEVELS, "°C", ".0f", out / "tmax.png", "both")
    map_panels(grid["temperature_2m_min"], dates, "일 최저기온", plt.get_cmap("RdBu_r"),
               TEMP_LEVELS, "°C", ".0f", out / "tmin.png", "both")
    map_panels(grid["precipitation_sum"], dates, "일 강수량", plt.get_cmap("Blues"),
               PRECIP_LEVELS, "mm", ".1f", out / "precip.png", "max")
    meteogram(seoul, out / "seoul.png")
    build_page(out, grid, model)
    print(f"완료: {out.resolve()}")


if __name__ == "__main__":
    main()
