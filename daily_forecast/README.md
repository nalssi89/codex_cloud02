# 한반도 일일 예보 (GitHub Actions + Pages)

매일 아침 Open-Meteo에서 한반도 0.5° 격자 예보를 받아 지도를 그리고 GitHub Pages에 게시합니다.

- **자료**: [Open-Meteo](https://open-meteo.com) (API 키 불필요). 기상청 모델(`kma_seamless`)을 먼저 시도하고, 실패하면 기본 모델(`best_match`)을 씁니다.
- **결과물**: 3일 최고·최저기온, 일강수량 지도, 서울 7일 시간별 그래프, 주요 도시 요약표, `data.json`
- **실행 시각**: 매일 06:17 KST (`.github/workflows/daily-forecast.yml`의 `cron`)

## 처음 한 번만 설정

1. 저장소 **Settings → Pages → Build and deployment → Source** 를 **GitHub Actions** 로 바꿉니다.
2. 워크플로 파일이 **main** 브랜치에 있어야 예약 실행과 게시가 됩니다.
3. **Actions** 탭 → "한반도 일일 예보" → **Run workflow** 로 바로 한 번 실행해 볼 수 있습니다.

게시 주소: `https://<사용자명>.github.io/<저장소명>/`

## 로컬 실행

```bash
pip install -r daily_forecast/requirements.txt
python daily_forecast/forecast.py --out daily_forecast/site
```

## 고쳐 쓰기

- 영역·해상도: `forecast.py`의 `LATS`, `LONS`, `EXTENT`
- 도시: `CITIES`
- 예보 일수: `DAYS`
- 실행 시각: 워크플로의 `cron` (UTC 기준, 한국시간 −9시간)
