"""
CLI for Flowchart Generator with Workflow Simplifier
"""

import typer
from pathlib import Path
from typing import Optional
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.preprocessor import WorkflowSimplifier

app = typer.Typer()

@app.command()
def simplify(
    input_file: Path = typer.Argument(..., help="Input file with messy workflow text"),
    output: Optional[Path] = typer.Option(None, "-o", "--output", help="Output file for clean workflow"),
    generate: Optional[Path] = typer.Option(None, "-g", "--generate", help="Also generate flowchart to this file"),
    config: Optional[Path] = typer.Option(None, "-c", "--config", help="Config file for simplifier options"),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Verbose output")
):
    """
    Simplify messy workflow text into clean, numbered format.
    
    Examples:
        py -m cli.main simplify messy.txt -o clean.txt
        py -m cli.main simplify messy.txt -o clean.txt -g flowchart.png
        py -m cli.main simplify messy.txt -v
    """
    # Read input
    if not input_file.exists():
        typer.echo(f"Error: Input file '{input_file}' not found", err=True)
        raise typer.Exit(1)
    
    messy_text = input_file.read_text(encoding='utf-8')
    
    if verbose:
        typer.echo(f"📖 Reading from: {input_file}")
        typer.echo(f"📏 Input length: {len(messy_text)} characters")
    
    # Load config if provided
    simplifier_config = {}
    if config:
        import json
        simplifier_config = json.loads(config.read_text())
        if verbose:
            typer.echo(f"⚙️  Loaded config: {simplifier_config}")
    
    # Simplify
    simplifier = WorkflowSimplifier(simplifier_config)
    
    if verbose:
        typer.echo("🔄 Simplifying workflow...")
    
    try:
        clean_text = simplifier.simplify(messy_text)
    except Exception as e:
        typer.echo(f"Error during simplification: {e}", err=True)
        raise typer.Exit(1)
    
    # Determine output path
    if not output:
        output = input_file.with_name(f"{input_file.stem}_clean.txt")
    
    # Write output
    output.write_text(clean_text, encoding='utf-8')
    
    if verbose:
        typer.echo(f"✅ Clean workflow saved to: {output}")
        typer.echo(f"📏 Output length: {len(clean_text)} characters")
        typer.echo(f"\n👁️  Preview:")
        lines = clean_text.split('\n')[:10]
        for line in lines:
            typer.echo(f"  {line}")
        if len(clean_text.split('\n')) > 10:
            typer.echo("  ...")
    else:
        typer.echo(f"✅ Simplified workflow saved to: {output}")
    
    # Optionally generate flowchart
    if generate:
        if verbose:
            typer.echo(f"\n🎨 Generating flowchart to: {generate}")
        
        typer.echo("⚠️  Flowchart generation not yet implemented. Coming soon!")
        typer.echo("    Use the clean workflow file with your flowchart generator.")

@app.command()
def analyze(
    input_file: Path = typer.Argument(..., help="Workflow file to analyze"),
):
    """
    Analyze a workflow file and show detected structure.
    
    Useful for debugging and understanding how the simplifier interprets text.
    """
    if not input_file.exists():
        typer.echo(f"Error: Input file '{input_file}' not found", err=True)
        raise typer.Exit(1)
    
    messy_text = input_file.read_text(encoding='utf-8')
    
    simplifier = WorkflowSimplifier()
    
    # Get structured data
    try:
        steps = simplifier.simplify_to_dict(messy_text)
    except Exception as e:
        typer.echo(f"Error during analysis: {e}", err=True)
        raise typer.Exit(1)
    
    typer.echo("\n📊 Workflow Analysis\n")
    typer.echo(f"Total steps: {len(steps)}")
    
    # Count step types
    types = {}
    for step in steps:
        step_type = step.get('type', 'step')
        types[step_type] = types.get(step_type, 0) + 1
    
    typer.echo("\nStep types:")
    for step_type, count in types.items():
        typer.echo(f"  - {step_type}: {count}")
    
    # Show decision points
    decisions = [s for s in steps if s.get('type') == 'decision']
    if decisions:
        typer.echo(f"\n🔀 Decision points: {len(decisions)}")
        for idx, decision in enumerate(decisions, 1):
            typer.echo(f"\n  {idx}. {decision['text']}")
            branches = decision.get('branches', [])
            for branch in branches:
                typer.echo(f"     • {branch}")
    
    # Show all steps
    typer.echo("\n📋 All Steps:\n")
    for step in steps:
        number = step['number']
        text = step['text']
        step_type = step.get('type', 'step')
        
        type_icon = {
            'start': '🟢',
            'end': '🔴',
            'decision': '🔶',
            'step': '🟦'
        }.get(step_type, '🔷')
        
        typer.echo(f"  {type_icon} {number}. {text}")
        
        if step_type == 'decision':
            branches = step.get('branches', [])
            for branch in branches:
                typer.echo(f"       └─ {branch}")
    
    typer.echo()

@app.command()
def version():
    """Show version information."""
    typer.echo("🔹 Flowchart Generator with Workflow Simplifier")
    typer.echo("Version: 1.0.0 (Beta)")
    typer.echo("Author: Aren Garro")

if __name__ == "__main__":
    app()
