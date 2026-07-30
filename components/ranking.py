"""
components/ranking.py
----------------------
Module 10 & 11 from the project spec: Ranking Candidates + Download Results.

Builds the comparison/ranking table from a list of analysis result dicts
and renders it, plus a CSV download button.
"""

import html

import pandas as pd
import streamlit as st

from components.theme import recommendation_badge, render_html


def build_ranking_dataframe(results: list) -> pd.DataFrame:
    """
    results: list of dicts, each shaped like the output of
             ai.chains.analyze_resume()

    Returns a pandas DataFrame sorted by score (highest first).
    """
    rows = []
    for r in results:
        rows.append(
            {
                "Candidate": r.get("candidate", "Unknown"),
                "Score (%)": r.get("score", 0),
                "Missing Skills": ", ".join(r.get("missing_skills", [])) or "-",
                "Recommendation": r.get("recommendation", "-"),
                "Justification": r.get("justification", ""),
            }
        )

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values(by="Score (%)", ascending=False).reset_index(drop=True)
        df.index = df.index + 1  # rank starts at 1
        df.index.name = "Rank"

    return df


def render_ranking_table(results: list):
    """
    Renders the ranking table + CSV export button in the main page.
    """
    if not results:
        return

    render_html(
        "<p class='section-title' style='font-size:1.2rem;'>🏆 Candidate Ranking</p>"
    )

    df = build_ranking_dataframe(results)

    rows_html = ""
    for rank, row in df.iterrows():
        candidate = html.escape(str(row["Candidate"]))
        score = row["Score (%)"]
        missing = html.escape(str(row["Missing Skills"]))
        justification = html.escape(str(row["Justification"]))
        is_top = rank == 1
        row_class = "rank-top" if is_top else ""
        badge_class = "rank-badge rank-badge-top" if is_top else "rank-badge"
        rows_html += f"""
        <tr class="{row_class}">
            <td style="width:60px;"><span class="{badge_class}">{rank}</span></td>
            <td><b>{candidate}</b></td>
            <td style="min-width:160px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <div class="score-bar-wrap" style="width:100px;">
                        <div class="score-bar-fill" style="width:{score}%;"></div>
                    </div>
                    <span style="font-family:'IBM Plex Mono', monospace; font-weight:600; color:#1F3A5F;">{score}%</span>
                </div>
            </td>
            <td>{missing}</td>
            <td>{recommendation_badge(row['Recommendation'])}</td>
            <td style="max-width:320px; color:#5B564A;">{justification}</td>
        </tr>
        """

    table_html = f"""
    <table class="ranking-table">
        <thead>
            <tr>
                <th>Rank</th>
                <th>Candidate</th>
                <th>Score</th>
                <th>Missing Skills</th>
                <th>Recommendation</th>
                <th>Justification</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    """
    render_html(table_html)

    st.write("")
    csv_bytes = df.to_csv(index=True).encode("utf-8")
    st.download_button(
        label="⬇️ Export Ranking as CSV",
        data=csv_bytes,
        file_name="candidate_ranking.csv",
        mime="text/csv",
        type="primary",
    )
