"""북한 27개 지점 평년값·관측자료 내려받기 (기상청 API허브).

사용법 (apihub.kma.go.kr 접속 가능한 환경에서):
    export KMA_AUTH=발급키
    python 40_fetch_nk.py normals          # 1991~2020 일·월 평년값 (전 지점)
    python 40_fetch_nk.py stations         # 지점 위경도 (특정 시각 관측에서 추출)
    python 40_fetch_nk.py hourly 1991 2026 # 시간자료 → 일자료(평균·최고·최저기온, 강수) 집계

출력: 같은 폴더의 nk_norm_D.csv, nk_norm_M.csv, nk_stations.csv, nk_daily_YYYY.csv
"""
import os, sys, io, time, datetime as dt
import urllib.request
import pandas as pd

BASE = "https://apihub.kma.go.kr/api/typ01/url/"
KEY = os.environ.get("KMA_AUTH", "")
OUT = os.path.dirname(os.path.abspath(__file__))


def get(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url + f"&authKey={KEY}", timeout=60) as r:
                return r.read().decode("euc-kr", errors="replace")
        except Exception as e:  # 네트워크 오류는 지수 대기 후 재시도
            if i == tries - 1:
                raise
            time.sleep(2 ** (i + 1))


def parse(txt, cols):
    """'#'로 시작하는 주석을 뺀 공백 구분 표를 읽는다. cols는 출력결과 표의 순서."""
    rows = [l.split() for l in txt.splitlines() if l.strip() and not l.startswith("#")]
    rows = [r[: len(cols)] for r in rows if len(r) >= len(cols)]
    df = pd.DataFrame(rows, columns=cols)
    return df.apply(pd.to_numeric, errors="ignore")


NORM_COLS = ["ST", "STN", "MM", "DD", "TA", "TA_MAX", "TA_MIN", "RN"]  # 앞쪽 열만 사용; 응답 헤더로 확인 필요


def normals():
    for norm in ["D", "M"]:
        txt = get(f"{BASE}sfc_nko_norm1.php?norm={norm}&tmst=2021&stn=0&MM1=1&DD1=1&MM2=12&DD2=31")
        open(os.path.join(OUT, f"raw_norm_{norm}.txt"), "w").write(txt)  # 열 순서 확인용 원문
        parse(txt, NORM_COLS).to_csv(os.path.join(OUT, f"nk_norm_{norm}.csv"), index=False)


SFC_COLS = ["TM", "STN", "LON", "LAT", "PS", "PT", "PR", "TA", "TD", "WC", "WP", "CA", "CD",
            "CH", "CL", "CM", "CT", "WD", "WS", "RH", "RN", "PA"]  # 원문 헤더로 순서 확인 필요


def stations():
    txt = get(f"{BASE}nko_sfctm.php?tm=202301010000&stn=&help=0")
    open(os.path.join(OUT, "raw_sfctm_sample.txt"), "w").write(txt)
    df = parse(txt, SFC_COLS)
    df[["STN", "LON", "LAT"]].drop_duplicates("STN").to_csv(os.path.join(OUT, "nk_stations.csv"), index=False)


def hourly(y1, y2):
    for y in range(y1, y2 + 1):
        frames, t = [], dt.datetime(y, 1, 1)
        while t.year == y:
            t2 = min(t + dt.timedelta(hours=47), dt.datetime(y, 12, 31, 23))
            txt = get(f"{BASE}nko_sfctm.php?tm1={t:%Y%m%d%H00}&tm2={t2:%Y%m%d%H00}&stn=&help=0")
            frames.append(parse(txt, SFC_COLS))
            t = t2 + dt.timedelta(hours=1)
        h = pd.concat(frames)
        h = h.replace([-9, -99, -999, -9.9, -99.9], pd.NA)
        h["TA"] = h["TA"] / 10.0  # 0.1 C
        # 일 경계: KST 기준(UTC+9)으로 맞춘다
        h["DATE"] = (pd.to_datetime(h["TM"].astype(str), format="%Y%m%d%H%M") + pd.Timedelta(hours=9)).dt.date
        d = h.groupby(["STN", "DATE"]).agg(TA=("TA", "mean"), TA_MAX=("TA", "max"), TA_MIN=("TA", "min"),
                                         N=("TA", "count"))
        # 강수: SYNOP RN은 RH시간 누적값이라 그대로 더하면 중복된다.
        # 6시간 누적 보고(RH==6)가 있으면 그것만, 없으면 12시간 누적(RH==12)만 더한다.
        # 주의: 일 경계(KST 09시 vs 00시)와 누적 구간이 맞는지 원문으로 확인 필요.
        r = h.dropna(subset=["RN", "RH"])
        r = r[r["RN"] >= 0]
        rn6 = r[r["RH"] == 6].groupby(["STN", "DATE"])["RN"].sum()
        rn12 = r[r["RH"] == 12].groupby(["STN", "DATE"])["RN"].sum()
        d["RN"] = rn6.combine_first(rn12)
        d.to_csv(os.path.join(OUT, f"nk_daily_{y}.csv"))
        print(y, len(d))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "normals":
        normals()
    elif cmd == "stations":
        stations()
    elif cmd == "hourly":
        hourly(int(sys.argv[2]), int(sys.argv[3]))
