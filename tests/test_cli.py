import subprocess
import os

def test_cli(tmpdir):
    out_dir = os.path.join(tmpdir, "cli_out")

    cmd = [
        "python", "-m", "src.melody_engine.cli", "generate",
        "--style", "ARABESK_POP",
        "--makam", "NIHAVENT",
        "--bpm", "92",
        "--tonic", "D",
        "--seed", "42",
        "--count", "10",
        "--output", out_dir
    ]

    # Run the CLI using python module execution
    # Ensure PYTHONPATH is correct during test execution. We can pass it via env.
    env = os.environ.copy()
    env["PYTHONPATH"] = "."

    res = subprocess.run(cmd, env=env, capture_output=True, text=True)

    assert res.returncode == 0
    assert "Generated 10 candidates" in res.stdout

    # Check outputs
    assert os.path.exists(os.path.join(out_dir, "ranking_report.txt"))
    assert os.path.exists(os.path.join(out_dir, "top_candidate.json"))
    assert os.path.exists(os.path.join(out_dir, "top_candidate.mid"))
    assert os.path.exists(os.path.join(out_dir, "top_candidate_chorus.mid"))
