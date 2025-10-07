
# リベラルアーツ鍛錬アプリ（最小セット）

中学生〜大人まで使える「1日1枚メモ・週1レポート・月1ミニ発表」を記録・一覧・エクスポートできる極小Webアプリです。

## 動作要件
- Python 3.9+
- macOS / Windows / Linux いずれも可
- デフォルトはローカルSQLiteに保存（ネット接続不要）
- Supabase等のPostgreSQLを利用する場合はインターネット接続と `DATABASE_URL` の設定が必要

## 使い方（3分）
1. このフォルダを任意の場所に保存します。
2. ターミナル（またはPowerShell）でフォルダに移動：
   ```bash
   cd liberal_arts_app
   ```
3. 依存をインストール：
   ```bash
   pip install -r requirements.txt
   ```
4. アプリを起動：
   ```bash
   streamlit run app.py
   ```
5. ブラウザが自動で開かない場合は、表示されたURL（通常 http://localhost:8501）にアクセスします。

### 環境変数
- `DATABASE_URL`: SQLAlchemy互換の接続文字列。Supabaseの値（`postgres://...`）も自動で `postgresql+psycopg2://` に変換されます。
- `APP_PASSCODE`: 任意設定。設定した場合はアプリ起動時にワンタイム入力が求められます。

## 機能
- 1日1枚メモ：日付／事実／問い／結論／次の問いを保存
- 週1レポート：結論→根拠3つ→反論→まとめ
- 月1ミニ発表：問題提起／仮説／根拠3つ／反論と再主張／まとめ
- 一覧表示：最新順データフレーム
- エクスポート：CSV（3種）とMarkdown（全件まとめ）

## データ保存
- `DATABASE_URL` が未設定の場合はカレントディレクトリに `liberal_arts.db`（SQLite）として保存します。
- `DATABASE_URL` を設定するとPostgreSQL（例：Supabase）に保存されます。
- CSVは同ディレクトリに `daily_memo.csv` などのファイルで出力します。

## よくある質問
- **PDF出力は？**  
  MarkdownやCSVをエディタ／表計算ソフトで開き、「印刷→PDF保存」をご利用ください。
- **バックアップは？**  
  `liberal_arts.db` と CSV をクラウドドライブにコピーすればOKです。
- **編集/削除は？**  
  シンプル化のため、このバージョンは“追記＋一覧”に絞っています。編集・削除機能の追加も可能です。

---
© 2025
