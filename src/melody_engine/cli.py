import argparse
import os
import sys
from src.melody_engine.models import SongSpec
from src.melody_engine.hook_generator import HookGenerator
from src.melody_engine.phrase_builder import PhraseBuilder
from src.melody_engine.scorer import BaselineScorer
from src.melody_engine.midi_export import Exporter

def main():
    parser = argparse.ArgumentParser(description="MelodyEngine_Lab V0.1 CLI")

    subparsers = parser.add_subparsers(dest="command", required=True)

    gen_parser = subparsers.add_parser("generate")
    gen_parser.add_argument("--style", type=str, required=True, help="Style pack name (e.g. ARABESK_POP)")
    gen_parser.add_argument("--makam", type=str, required=True, help="Makam name (e.g. NIHAVENT)")
    gen_parser.add_argument("--bpm", type=int, required=True, help="BPM")
    gen_parser.add_argument("--tonic", type=str, required=True, help="Tonic (e.g. D)")
    gen_parser.add_argument("--seed", type=int, required=True, help="Random seed")
    gen_parser.add_argument("--count", type=int, default=32, help="Number of candidates to generate")
    gen_parser.add_argument("--output", type=str, required=True, help="Output directory")

    args = parser.parse_args()

    if args.command == "generate":
        spec = SongSpec(
            style=args.style,
            makam=args.makam,
            tonic=args.tonic,
            bpm=args.bpm,
            meter="4/4", # Defaulting for this slice
            energy=0.7,
            vocal_range=("G3", "C5"), # Defaulting
            seed=args.seed
        )

        generator = HookGenerator(spec)
        scorer = BaselineScorer(spec)
        builder = PhraseBuilder(spec)
        exporter = Exporter(bpm=spec.bpm)

        os.makedirs(args.output, exist_ok=True)

        candidates = generator.generate_candidates(args.count)

        scored_candidates = []
        for i, hook in enumerate(candidates):
            score_res = scorer.score(hook)
            scored_candidates.append({
                "id": i+1,
                "hook": hook,
                "score_res": score_res
            })

        # Filter and rank
        valid_candidates = [c for c in scored_candidates if not c["score_res"].get("rejected", False)]
        valid_candidates.sort(key=lambda c: c["score_res"].get("total_score", 0), reverse=True)

        report_path = os.path.join(args.output, "ranking_report.txt")
        with open(report_path, "w") as f:
            f.write(f"Generated {args.count} candidates.\n")
            f.write(f"Valid: {len(valid_candidates)}\n\n")
            for c in valid_candidates:
                f.write(f"Candidate {c['id']}: Score {c['score_res'].get('total_score'):.3f} - Details: {c['score_res']}\n")

            rejected = [c for c in scored_candidates if c["score_res"].get("rejected", False)]
            if rejected:
                f.write("\nRejected:\n")
                for c in rejected:
                    f.write(f"Candidate {c['id']}: {c['score_res']['reason']}\n")

        print(f"Generated {args.count} candidates. Valid: {len(valid_candidates)}.")

        if valid_candidates:
            top_candidate = valid_candidates[0]
            top_hook = top_candidate["hook"]
            print(f"Top candidate is ID {top_candidate['id']} with score {top_candidate['score_res']['total_score']:.3f}.")

            # Export Top Hook IR
            ir_path = os.path.join(args.output, "top_candidate.json")
            exporter.export_json(top_hook, ir_path)

            # Export Top Hook MIDI
            midi_path = os.path.join(args.output, "top_candidate.mid")
            exporter.export_midi(top_hook, midi_path)

            # Expand to 8-bar chorus
            chorus = builder.expand_to_chorus(top_hook)
            chorus_midi_path = os.path.join(args.output, "top_candidate_chorus.mid")
            exporter.export_midi(chorus, chorus_midi_path)

            print(f"Outputs written to {args.output}")
        else:
            print("No valid candidates generated.")

if __name__ == "__main__":
    main()
