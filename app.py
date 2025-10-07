
import sqlite3
from contextlib import closing
import pandas as pd
import streamlit as st
from datetime import datetime

DB_PATH = "liberal_arts.db"

# -----------------------------
# Database helpers
# -----------------------------
def init_db():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS daily_memo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                fact TEXT,
                question TEXT,
                conclusion TEXT,
                next_topic TEXT,
                created_at TEXT NOT NULL
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS weekly_report (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                theme TEXT NOT NULL,
                conclusion TEXT,
                evidence1 TEXT,
                evidence2 TEXT,
                evidence3 TEXT,
                counter TEXT,
                summary TEXT,
                created_at TEXT NOT NULL
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS monthly_presentation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                problem TEXT,
                hypothesis TEXT,
                reasoning1 TEXT,
                reasoning2 TEXT,
                reasoning3 TEXT,
                counter_reassert TEXT,
                takeaway TEXT,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()

def insert_daily(date, fact, question, conclusion, next_topic):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO daily_memo (date, fact, question, conclusion, next_topic, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (date, fact, question, conclusion, next_topic, datetime.utcnow().isoformat()))
        conn.commit()

def insert_weekly(theme, conclusion, e1, e2, e3, counter, summary):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO weekly_report (theme, conclusion, evidence1, evidence2, evidence3, counter, summary, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (theme, conclusion, e1, e2, e3, counter, summary, datetime.utcnow().isoformat()))
        conn.commit()

def insert_monthly(title, problem, hypothesis, r1, r2, r3, counter_reassert, takeaway):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO monthly_presentation (title, problem, hypothesis, reasoning1, reasoning2, reasoning3, counter_reassert, takeaway, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, problem, hypothesis, r1, r2, r3, counter_reassert, takeaway, datetime.utcnow().isoformat()))
        conn.commit()

def fetch_table(name):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        df = pd.read_sql_query(f"SELECT * FROM {name} ORDER BY id DESC", conn)
    return df

def export_markdown():
    """Export all entries into a single Markdown text."""
    parts = ["# Liberal Arts Practice Export\n"]
    # Daily
    daily = fetch_table("daily_memo")
    if not daily.empty:
        parts.append("## Daily Memos\n")
        for _, row in daily.iterrows():
            parts.append(f"### {row['date']} (ID: {row['id']})\n")
            parts.append(f"- 事実: {row['fact'] or ''}\n")
            parts.append(f"- 問い: {row['question'] or ''}\n")
            parts.append(f"- 結論: {row['conclusion'] or ''}\n")
            parts.append(f"- 次に調べたいこと: {row['next_topic'] or ''}\n")
            parts.append("")
    # Weekly
    weekly = fetch_table("weekly_report")
    if not weekly.empty:
        parts.append("## Weekly Reports\n")
        for _, row in weekly.iterrows():
            parts.append(f"### テーマ: {row['theme']} (ID: {row['id']})\n")
            parts.append(f"- 結論: {row['conclusion'] or ''}\n")
            parts.append(f"- 根拠1: {row['evidence1'] or ''}\n")
            parts.append(f"- 根拠2: {row['evidence2'] or ''}\n")
            parts.append(f"- 根拠3: {row['evidence3'] or ''}\n")
            parts.append(f"- 反対意見/反論: {row['counter'] or ''}\n")
            parts.append(f"- まとめ: {row['summary'] or ''}\n")
            parts.append("")
    # Monthly
    monthly = fetch_table("monthly_presentation")
    if not monthly.empty:
        parts.append("## Monthly Presentations\n")
        for _, row in monthly.iterrows():
            parts.append(f"### タイトル: {row['title']} (ID: {row['id']})\n")
            parts.append(f"- 問題提起: {row['problem'] or ''}\n")
            parts.append(f"- 仮説/結論: {row['hypothesis'] or ''}\n")
            parts.append(f"- 根拠1: {row['reasoning1'] or ''}\n")
            parts.append(f"- 根拠2: {row['reasoning2'] or ''}\n")
            parts.append(f"- 根拠3: {row['reasoning3'] or ''}\n")
            parts.append(f"- 反論と再主張: {row['counter_reassert'] or ''}\n")
            parts.append(f"- まとめ・学び・次の問い: {row['takeaway'] or ''}\n")
            parts.append("")
    return "\n".join(parts)

# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="Liberal Arts Practice", page_icon="🧠", layout="wide")
st.title("🧠 リベラルアーツ鍛錬アプリ（最小セット）")
st.write("毎日の1枚メモ、週1レポート、月1ミニ発表の素振りを行うための極小アプリです。")

init_db()

with st.sidebar:
    st.header("メニュー")
    page = st.radio("ページを選択", ["ホーム", "1日1枚メモ", "週1レポート", "月1ミニ発表", "ダッシュボード / エクスポート"])
    st.markdown("---")
    st.caption("作成：Python + Streamlit / SQLite")

if page == "ホーム":
    st.subheader("使い方")
    st.markdown(
        "1. **1日1枚メモ**で「事実・問い・結論・次に調べたいこと」を5〜10分で入力します。  \n"
        "2. **週1レポート**で、結論→根拠3点→反論→まとめのA4一枚を作ります。  \n"
        "3. **月1ミニ発表**で、3〜5枚相当の骨子（タイトル〜まとめ）を作ります。  \n"
        "右上の**ダッシュボード**から一覧とエクスポートができます。"
    )
    st.info("ヒント：毎日同じ時間に1枚メモを作ると継続しやすいです。")

elif page == "1日1枚メモ":
    st.subheader("🗒️ 1日1枚メモ")
    with st.form("daily_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("日付", value=None, format="YYYY-MM-DD")
        with col2:
            st.caption("※日付未選択の場合は保存時に本日の日付が入ります")
        fact = st.text_area("今日の学び・気づき（事実）", height=100, placeholder="例：物価上昇のニュースを見た。")
        question = st.text_area("なぜそうなっている？（問い）", height=80, placeholder="例：なぜ利上げは物価に効くのか？")
        conclusion = st.text_area("自分の考え（結論）", height=80, placeholder="例：需要と金利の関係で...")
        next_topic = st.text_area("次に調べたいこと", height=60, placeholder="例：利上げと景気の関係")
        submitted = st.form_submit_button("保存")
        if submitted:
            d = date.isoformat() if date else datetime.now().date().isoformat()
            insert_daily(d, fact.strip(), question.strip(), conclusion.strip(), next_topic.strip())
            st.success("保存しました。")
    st.markdown("### 最近のメモ")
    df = fetch_table("daily_memo")
    if df.empty:
        st.caption("まだデータがありません。")
    else:
        st.dataframe(df.drop(columns=["created_at"]), use_container_width=True, hide_index=True)

elif page == "週1レポート":
    st.subheader("🧩 週1レポート（A4一枚）")
    with st.form("weekly_form", clear_on_submit=True):
        theme = st.text_input("テーマ", placeholder="例：なぜ同じニュースでも意見が分かれるのか？")
        conclusion = st.text_area("結論（1行）", height=60)
        c1, c2, c3 = st.columns(3)
        with c1:
            e1 = st.text_area("根拠①", height=100)
        with c2:
            e2 = st.text_area("根拠②", height=100)
        with c3:
            e3 = st.text_area("根拠③", height=100)
        counter = st.text_area("反対意見／反論", height=100)
        summary = st.text_area("まとめ（学び・次の問い）", height=100)
        submitted = st.form_submit_button("保存")
        if submitted:
            insert_weekly(theme.strip(), conclusion.strip(), e1.strip(), e2.strip(), e3.strip(), counter.strip(), summary.strip())
            st.success("保存しました。")
    st.markdown("### レポート一覧")
    df = fetch_table("weekly_report")
    if df.empty:
        st.caption("まだデータがありません。")
    else:
        st.dataframe(df.drop(columns=["created_at"]), use_container_width=True, hide_index=True)

elif page == "月1ミニ発表":
    st.subheader("🌍 月1ミニ発表（3〜5枚相当）")
    with st.form("monthly_form", clear_on_submit=True):
        title = st.text_input("タイトル", placeholder="例：SNS時代に“正しさ”をどう考えるか？")
        problem = st.text_area("問題提起", height=100, placeholder="例：最近こう感じた／こういう出来事があった")
        hypothesis = st.text_area("私の仮説（結論）", height=80, placeholder="例：○○が原因だと思う")
        r1, r2, r3 = st.columns(3)
        with r1:
            reasoning1 = st.text_area("根拠1（経験）", height=120)
        with r2:
            reasoning2 = st.text_area("根拠2（データ）", height=120)
        with r3:
            reasoning3 = st.text_area("根拠3（引用）", height=120)
        counter_re = st.text_area("反論と再主張", height=100)
        takeaway = st.text_area("まとめ・学び・次の問い", height=100)
        submitted = st.form_submit_button("保存")
        if submitted:
            insert_monthly(title.strip(), problem.strip(), hypothesis.strip(), reasoning1.strip(), reasoning2.strip(), reasoning3.strip(), counter_re.strip(), takeaway.strip())
            st.success("保存しました。")
    st.markdown("### 発表骨子 一覧")
    df = fetch_table("monthly_presentation")
    if df.empty:
        st.caption("まだデータがありません。")
    else:
        st.dataframe(df.drop(columns=["created_at"]), use_container_width=True, hide_index=True)

elif page == "ダッシュボード / エクスポート":
    st.subheader("📊 ダッシュボード / エクスポート")
    colA, colB, colC = st.columns(3)
    with colA:
        daily_df = fetch_table("daily_memo")
        st.metric("1日1枚メモ 件数", len(daily_df))
    with colB:
        weekly_df = fetch_table("weekly_report")
        st.metric("週1レポート 件数", len(weekly_df))
    with colC:
        monthly_df = fetch_table("monthly_presentation")
        st.metric("月1ミニ発表 件数", len(monthly_df))

    st.markdown("---")
    st.markdown("#### エクスポート")
    # CSV exports
    if st.button("CSVを書き出す"):
        with closing(sqlite3.connect(DB_PATH)) as conn:
            pd.read_sql_query("SELECT * FROM daily_memo", conn).to_csv("daily_memo.csv", index=False)
            pd.read_sql_query("SELECT * FROM weekly_report", conn).to_csv("weekly_report.csv", index=False)
            pd.read_sql_query("SELECT * FROM monthly_presentation", conn).to_csv("monthly_presentation.csv", index=False)
        st.success("CSVを書き出しました。以下からダウンロードできます。")

    for fname, label in [
        ("daily_memo.csv", "📥 daily_memo.csv"),
        ("weekly_report.csv", "📥 weekly_report.csv"),
        ("monthly_presentation.csv", "📥 monthly_presentation.csv"),
    ]:
        try:
            with open(fname, "rb") as f:
                st.download_button(label, data=f, file_name=fname, mime="text/csv", use_container_width=True)
        except FileNotFoundError:
            pass

    md_text = export_markdown()
    st.download_button("📥 まとめMarkdownをダウンロード (export.md)", data=md_text, file_name="export.md", mime="text/markdown", use_container_width=True)

    st.caption("※PDF化は、お使いのテキストエディタやブラウザの印刷機能から行ってください。")
