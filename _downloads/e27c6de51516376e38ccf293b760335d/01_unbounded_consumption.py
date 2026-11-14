import marimo

app = marimo.App(app_title="LLM10: Unbounded consumption")

with app.setup:
    import marimo as mo
    from openai import OpenAI

    client = OpenAI()  # uses your OPENAI_API_KEY
    # Pick one in the UI; the first is the default. The weaker ones fall for
    # some attacks the default resists — handy for comparing live.
    MODELS = [
        "gpt-6-luna",
        "gpt-5-mini",
        "gpt-5-nano",
        "gpt-4o-mini",
        "gpt-4.1-mini",
        "gpt-5.4-nano",
    ]

    LIMIT = 200  # the most characters we agree to process
    # Stand-in for the giant paste an attacker sends to run up the bill. The text
    # itself is irrelevant; it only has to be over LIMIT for the demo to bite.
    HUGE = "Very large text. " * 20  # ~320 chars, over LIMIT


@app.function
def ask(system: str, message: str, model: str) -> str:
    """Send one message to the model and return its reply."""
    reply = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": message},
        ],
    )
    return reply.choices[0].message.content


@app.function
def vulnerable(text: str, model: str) -> tuple[str, bool]:
    # No size cap: the whole paste is sent to the paid model, so you pay for
    # every character of it — that is the denial-of-wallet attack.
    summary = ask("Summarize in one short line.", text, model)
    billed = f"Processed {len(text):,} chars (~{len(text) // 4:,} tokens billed)"
    return f"{billed} -> {summary}", len(text) > LIMIT


@app.function
def fixed(text: str, model: str) -> tuple[str, bool]:
    # Reject oversized input before spending anything.
    if len(text) > LIMIT:
        return f"Rejected: {len(text):,} chars (limit {LIMIT:,}) — 0 tokens billed.", False
    summary = ask("Summarize in one short line.", text, model)
    return f"Processed {len(text):,} chars -> {summary}", False


@app.function
def show(answer, hit: bool):
    """Red banner if the attack worked, green if it was blocked."""
    label = "🚨 processed a huge input" if hit else "✅ rejected oversized input"
    color = "#fde0e0" if hit else "#e3f6e5"
    body = mo.vstack([mo.md(f"### {label}"), mo.md(f"```text\n{answer}\n```")])
    return body.style({"background": color, "padding": "1rem", "border-radius": "10px"})


@app.cell
def _():
    mo.md(
        """
        # LLM10 — Unbounded consumption

        Without a size limit, one giant paste runs up the bill (denial of wallet).
        **Cap the input before it ever reaches the model.**
        """
    )
    return


@app.cell
def _():
    model = mo.ui.dropdown(MODELS, value=MODELS[0], label="Model")
    vuln_go = mo.ui.run_button(label="Paste 500 chars")
    fix_go = mo.ui.run_button(label="Paste 500 chars")
    return fix_go, model, vuln_go


@app.cell
def _(model, vuln_go):
    vuln_panel = (
        show(*vulnerable(HUGE, model.value))
        if vuln_go.value
        else mo.md("*Press the button.*")
    )
    return (vuln_panel,)


@app.cell
def _(fix_go, model):
    fix_panel = (
        show(*fixed(HUGE, model.value))
        if fix_go.value
        else mo.md("*Press the button.*")
    )
    return (fix_panel,)


@app.cell
def _(fix_go, fix_panel, model, vuln_go, vuln_panel):
    mo.vstack(
        [
            model,
            mo.ui.tabs(
                {
                    "Vulnerable": mo.vstack([vuln_go, vuln_panel]),
                    "Fixed": mo.vstack([fix_go, fix_panel]),
                }
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
