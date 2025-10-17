import sqlite3
import re
from pathlib import Path
from typing import List, Sequence, Tuple, Optional, Iterable, Any

# ──────────────────────────────────────────────────────────────────────────────
# Markdown table (pandas 없이)
# ──────────────────────────────────────────────────────────────────────────────
def _markdown_table(headers: Sequence[str], rows: Sequence[Sequence[object]], max_rows: int = 500) -> str:
    """간단한 Markdown 테이블 포매터 (pandas 불필요)."""
    headers = list(headers or [])
    rows = list(rows or [])

    if not headers and not rows:
        return "_(no rows)_"

    clipped = rows[:max_rows]
    str_rows: List[List[str]] = [[("" if c is None else str(c)) for c in r] for r in clipped]
    str_headers: List[str] = [("" if h is None else str(h)) for h in headers]

    col_count = len(str_headers) if str_headers else (len(str_rows[0]) if str_rows else 0)
    if col_count == 0:
        return "_(no rows)_"

    widths = [0] * col_count
    if str_headers:
        for i, h in enumerate(str_headers):
            widths[i] = max(widths[i], len(h))
    for r in str_rows:
        for i, cell in enumerate(r):
            widths[i] = max(widths[i], len(cell))

    def fmt_row(cells: Sequence[str]) -> str:
        parts = []
        for i in range(col_count):
            val = cells[i] if i < len(cells) else ""
            parts.append(" " + val.ljust(widths[i]) + " ")
        return "|" + "|".join(parts) + "|"

    lines = []
    if str_headers:
        lines.append(fmt_row(str_headers))
        lines.append("|" + "|".join(["-" * (w + 2) for w in widths]) + "|")
    else:
        lines.append("|" + "|".join(["-" * (w + 2) for w in widths]) + "|")

    for r in str_rows:
        lines.append(fmt_row(r))

    if len(rows) > max_rows:
        lines.append(f"\n_... {len(rows) - max_rows} more rows truncated ..._")

    return "\n".join(lines)

# ──────────────────────────────────────────────────────────────────────────────
# SQLite helpers (pandas 제거)
# ──────────────────────────────────────────────────────────────────────────────
def _conn(db_path: str | Path, *, ro: bool = False, timeout: float = 5.0) -> sqlite3.Connection:
    """SQLite 연결 (행을 dict처럼 다루기 위해 row_factory 사용)."""
    p = Path(db_path)
    if ro:
        uri = f"file:{p.as_posix()}?mode=ro"
        conn = sqlite3.connect(uri, uri=True, timeout=timeout)
    else:
        conn = sqlite3.connect(p.as_posix(), timeout=timeout)
    conn.row_factory = sqlite3.Row
    return conn

def _is_select(q: str) -> bool:
    q = (q or "").strip().lower()
    return q.startswith("select") or q.startswith("with")  # CTE 허용

def _ensure_limit(q: str, default_limit: int = 500) -> str:
    q = (q or "").strip().rstrip(";")
    # 이미 LIMIT이 있으면 그대로 둠
    if re.search(r"\blimit\b\s+\d+", q, flags=re.I):
        return q
    # SELECT/CTE에만 LIMIT 보강
    return f"{q} LIMIT {default_limit}" if _is_select(q) else q

def _clean_table_name(name: str) -> str:
    name = (name or "").strip().strip('`"\'')
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
        return name
    return f'"{name}"'

# ──────────────────────────────────────────────────────────────────────────────
# 실행 & 결과 포매팅 (pandas 없이)
# ──────────────────────────────────────────────────────────────────────────────
def sql_execute(
    db_path: str | Path,
    q: str,
    params: Optional[Sequence[Any]] = None,
    *,
    default_limit: int = 500,
    ro: bool | None = None
) -> str:
    """
    쿼리 실행 후 마크다운/요약 문자열 반환.
    - SELECT/CTE: 결과를 마크다운 표로
    - DML/DDL   : 영향 행수/lastrowid 요약
    """
    q = (q or "").strip()
    if not q:
        return "FAIL | empty query"

    is_read = _is_select(q)
    # 읽기 쿼리는 read-only 모드로, 나머지는 read-write로
    ro = True if ro is None and is_read else (False if ro is None else ro)
    q_exec = _ensure_limit(q, default_limit=default_limit)

    try:
        with _conn(db_path, ro=ro) as conn:
            cur = conn.cursor()
            cur.execute(q_exec, params or [])
            if is_read:
                rows = cur.fetchall()  # list[sqlite3.Row]
                headers = [d[0] for d in (cur.description or [])]
                # Row → list 로 변환
                plain_rows = [[row[h] for h in headers] for row in rows] if headers else []
                return _markdown_table(headers, plain_rows, max_rows=default_limit)
            else:
                conn.commit()
                rc = cur.rowcount  # -1일 수 있음 (sqlite 특성)
                lrid = cur.lastrowid
                return f"OK | rows_affected={rc} | lastrowid={lrid}"
    except sqlite3.Error as e:
        return f"FAIL | sqlite error: {e.__class__.__name__}: {e}"
    except Exception as e:
        return f"FAIL | error: {e.__class__.__name__}: {e}"

# ──────────────────────────────────────────────────────────────────────────────
# 유틸 쿼리 (테이블 나열/스키마 보기) — pandas 없이
# ──────────────────────────────────────────────────────────────────────────────
def list_tables(db_path: str | Path) -> str:
    q = """
    SELECT name AS table_name
    FROM sqlite_master
    WHERE type='table' AND name NOT LIKE 'sqlite_%'
    ORDER BY name
    """
    return sql_execute(db_path, q, ro=True)

def describe_table(db_path: str | Path, table_name: str) -> str:
    t = _clean_table_name(table_name)
    q = f'PRAGMA table_info({t})'
    return sql_execute(db_path, q, ro=True)
