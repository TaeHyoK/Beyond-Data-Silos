# 구성요소 제거 실험

논문의 실험 설정과 최종 실행·평가 코드를 모은 디렉터리다. 저장소 루트에서 실행한다. 실험 결과·생성 보고서·수집 원자료·평가 입력과 응답은 포함하지 않는다.

| 위치 | 내용 |
|---|---|
| `run_config/` | 수집·기업 설정, 조건별 입력 준비, 보고서 생성·반복 실행, Judge |
| `ablation_suite/` | 무작위 뉴스 표본 추출과 입력 유틸리티 |
| `ablation_evaluation/` | 조건별 입력 발견과 평가 유틸리티 |
| `real_report_evaluation/` | 서술 본문 추출과 BERTScore |
| `docs/` | 실험 조건과 재현 절차 |

[실험 방법](docs/ABLATION.md)과 [일반 Judge 실행 안내](run_config/FINAL_REPORT_LLM_JUDGE.md)를 참고한다. NP1·NP2·NP3는 `run_config/no_peer_target_llm_judge.py`의 평가 기준이며 별도 보고서 생성 조건이 아니다.

```bash
python -m pip install -e ".[eval,dev]"
python ablation/run_config/final_report_llm_judge.py --help
python ablation/run_config/no_peer_target_llm_judge.py --help
PYTHONPATH=src:ablation python ablation/run_config/rerun_ablation.py --help
python -m pytest -q
```

실행에는 개인 API 키와 별도 원자료·참조 PDF·동결 입력이 필요하다. `--help`와 테스트는 모델을 호출하지 않는다. Judge 유료 실행에는 `--execute-paid-api`와 예상 호출 수 확인이 필요하다. 새로운 생성·평가는 기존 논문 결과와 분리한다.
