"""ASOS+AWS(약 700개 지점) 기후통계 일자료 내려받기 (기상청 API허브 sts_ta, sts_rn).

사용법 (apihub.kma.go.kr 접속 가능한 환경에서):
    export KMA_AUTH=발급키
    python 41_fetch_sts.py ta 19930101 20261031
    python 41_fetch_sts.py rn 19930101 20261031
출력: sts_{ta|rn}_YYYY.csv (연도별), 첫 호출 원문 raw_sts_{ta|rn}_sample.txt (열 확인용)

- 하루 단위로 전 지점(stn_id=0)을 받는다. tm1~tm2 기간 조회가 여러 날을 허용하면 STEP_DAYS를 늘린다.
- disp=0 (빈칸 없는 CSV), help=0. 열 이름은 원문 첫 줄 또는 '#' 주석에서 읽는다.
- 기온 일평균(TA_DAVG)은 하루 8회 정시 평균임에 유의.
"""
import os, sys, io, time, datetime as dt, urllib.request
import pandas as pd

BASE = "https://apihub.kma.go.kr/api/typ01/url/"
KEY = os.environ.get("KMA_AUTH", "")
OUT = os.path.dirname(os.path.abspath(__file__))
STEP_DAYS = 1


def get(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url + f"&authKey={KEY}", timeout=90) as r:
                return r.read().decode("euc-kr", errors="replace")
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 ** (i + 1))


def parse(txt):
    lines = [l for l in txt.splitlines() if l.strip()]
    head = [l for l in lines if l.startswith("#")]
    body = [l for l in lines if not l.startswith("#")]
    # 헤더 후보: 마지막 '#' 줄의 쉼표 구분 이름, 없으면 본문 첫 줄
    names = None
    if head and "," in head[-1]:
        names = [c.strip(" #") for c in head[-1].split(",")]
    df = pd.read_csv(io.StringIO("\n".join(body)), header=None if names else 0)
    if names and len(names) >= df.shape[1]:
        df.columns = names[: df.shape[1]]
    return df


def run(var, d1, d2):
    t, t_end = dt.datetime.strptime(d1, "%Y%m%d"), dt.datetime.strptime(d2, "%Y%m%d")
    year, frames, first = t.year, [], True
    while t <= t_end:
        t2 = min(t + dt.timedelta(days=STEP_DAYS - 1), t_end)
        txt = get(f"{BASE}sts_{var}.php?tm1={t:%Y%m%d}&tm2={t2:%Y%m%d}&stn_id=0&help=0&disp=0")
        if first:
            open(os.path.join(OUT, f"raw_sts_{var}_sample.txt"), "w").write(txt); first = False
        frames.append(parse(txt))
        t = t2 + dt.timedelta(days=1)
        if t.year != year or t > t_end:
            pd.concat(frames).to_csv(os.path.join(OUT, f"sts_{var}_{year}.csv"), index=False)
            print(var, year, sum(len(f) for f in frames)); frames, year = [], t.year


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], sys.argv[3])
