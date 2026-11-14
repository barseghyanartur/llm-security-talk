import marimo

app = marimo.App(app_title="LLM03: Supply chain")

with app.setup:
    import pickle
    import tempfile
    from pathlib import Path

    import marimo as mo
    import numpy as np
    from safetensors.numpy import load_file, save_file

    # Proof that attacker code ran during a load. Harmless: the "attack" below
    # just creates this file. We delete it before each run and check if it came
    # back. A real payload could run anything the process can.
    MARKER = Path(tempfile.gettempdir()) / "llm03_code_ran.txt"

    class _Reupload:
        # A pickle runs whatever __reduce__ names when it is loaded. A real model
        # file (.bin / .pt) is a pickle, so loading one can run code like this —
        # here, the builtin open() creates MARKER as a visible side effect.
        def __reduce__(self):
            return (open, (str(MARKER), "w"))

    # The same fine-tuned model, published two ways under the same name.
    WEIGHTS = {"embeddings": np.zeros(4, dtype=np.float32)}
    HUB = Path(tempfile.mkdtemp())

    # The real publisher ships safetensors: numbers only, no code can run.
    trusted = HUB / "acme-ai"
    trusted.mkdir()
    save_file(WEIGHTS, trusted / "model.safetensors")

    # The attacker re-published it as a pickle with code stapled on.
    attacker = HUB / "user-7f3a21"
    attacker.mkdir()
    with open(attacker / "pytorch_model.bin", "wb") as f:
        pickle.dump(_Reupload(), f)

    REPOS = {
        "acme-ai/sentiment  (official)": trusted,
        "user-7f3a21/sentiment  (a stranger)": attacker,
    }


@app.function
def load_model(path: Path):
    """Load a model file the way PyTorch does: .safetensors is data-only,
    a .bin / .pt is a pickle, so loading it runs any code inside."""
    if path.suffix == ".safetensors":
        return load_file(path)
    with open(path, "rb") as f:
        return pickle.load(f)


@app.function
def vulnerable(repo: Path) -> tuple[str, bool]:
    # Download the model and load whatever file it ships. No checks.
    weight_file = next(repo.iterdir())
    MARKER.unlink(missing_ok=True)
    load_model(weight_file)
    if MARKER.exists():
        return f"Loaded {repo.name}/{weight_file.name} — it ran code on load.", True
    return f"Loaded {repo.name}/{weight_file.name} — no code ran.", False


@app.function
def fixed(repo: Path) -> tuple[str, bool]:
    # Refuse anything that is not safetensors, so a pickle never gets loaded.
    weight_file = next(repo.iterdir())
    name = f"{repo.name}/{weight_file.name}"
    if weight_file.suffix != ".safetensors":
        return f"Refused {name}: only safetensors allowed.", False
    MARKER.unlink(missing_ok=True)
    load_model(weight_file)
    return f"Loaded {name} — safe (data only).", MARKER.exists()


@app.function
def show(answer, hit: bool):
    """Red banner if the attack worked, green if it was blocked."""
    label = "🚨 the model ran attacker code" if hit else "✅ safe"
    color = "#fde0e0" if hit else "#e3f6e5"
    body = mo.vstack([mo.md(f"### {label}"), mo.md(f"```text\n{answer}\n```")])
    return body.style({"background": color, "padding": "1rem", "border-radius": "10px"})


@app.cell
def _():
    mo.md(
        """
        # LLM03 — Supply chain

        You download a fine-tuned model from a hub. A stranger re-published it
        under a look-alike name with code stapled on. Loading a `.bin` runs that
        code — before you ever run the model. **Load only safetensors.**
        """
    )
    return


@app.cell
def _():
    names = list(REPOS)
    vuln_in = mo.ui.dropdown(names, value=names[1], label="Download from")
    vuln_go = mo.ui.run_button(label="Load")
    fix_in = mo.ui.dropdown(names, value=names[1], label="Download from")
    fix_go = mo.ui.run_button(label="Load")
    return fix_go, fix_in, vuln_go, vuln_in


@app.cell
def _(vuln_go, vuln_in):
    vuln_panel = (
        show(*vulnerable(REPOS[vuln_in.value]))
        if vuln_go.value
        else mo.md("*Press Load.*")
    )
    return (vuln_panel,)


@app.cell
def _(fix_go, fix_in):
    fix_panel = (
        show(*fixed(REPOS[fix_in.value])) if fix_go.value else mo.md("*Press Load.*")
    )
    return (fix_panel,)


@app.cell
def _(fix_go, fix_in, fix_panel, vuln_go, vuln_in, vuln_panel):
    mo.ui.tabs(
        {
            "Vulnerable": mo.vstack([vuln_in, vuln_go, vuln_panel]),
            "Fixed": mo.vstack([fix_in, fix_go, fix_panel]),
        }
    )
    return


if __name__ == "__main__":
    app.run()
