from src.core.config import load_yaml, ConfigError  # 누락 설정 파일 예외 동작을 검증합니다.
from pathlib import Path  # tmp_path 타입 힌트에 사용합니다.


def test_load_yaml_missing(tmp_path: Path):  # 없는 YAML 파일을 읽으면 ConfigError가 발생해야 합니다.
    try:
        load_yaml(tmp_path / "nope.yml")
        assert False, "should raise"
    except ConfigError:
        assert True
