import tools
import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

# Initialize Rich Console
console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    console.print(Panel.fit("[bold cyan]🎓 AI STUDY CONCIERGE: Activated[/bold cyan]"))
    
    # --- Step 1: Input ---
    console.print("\n[bold yellow]Select Source:[/bold yellow]")
    console.print("1. Search Topic (Wikipedia)")
    console.print("2. Ask a Question (Gemini AI)")
    
    
    choice = console.input("\n> ")
    
    raw_content = ""
    
    if choice == "1":
        topic = console.input("Enter Topic Name: ")
        raw_content = tools.fetch_wikipedia_content(topic)
        
    elif choice == "2":
        question = console.input("Enter your Question: ")
        raw_content = tools.fetch_gemini_content(question)

   
    
    else:
        console.print("[bold red]❌ Invalid choice.[/bold red]")
        return

    if not raw_content:
        console.print("[bold red]❌ Failed to get content. Exiting.[/bold red]")
        return

    # --- Step 2: Context ---
    console.print("\n[bold yellow]How deep should we go?[/bold yellow]")
    level = console.input("Type: [green]beginner[/green], [yellow]intermediate[/yellow], or [red]advanced[/red]\n> ").lower()

    # --- Step 3: Agent Execution ---
    console.print("\n[bold magenta]🧠 AI Agent is reading and generating your study pack...[/bold magenta]")
    with console.status("[bold green]Working on it...[/bold green]", spinner="dots"):
        study_data = tools.generate_study_material(raw_content, level)

    if not study_data:
        console.print("[bold red]❌ AI generation failed.[/bold red]")
        return

    tools.save_results(study_data)

    # --- Step 4: The "Concierge" Experience ---
    while True:
        clear_screen()
        console.print(Panel(f"[bold blue]TOPIC: {study_data['topic_title']} ({level.upper()})[/bold blue]"))
        console.print("1. [bold]Read Summary[/bold]")
        console.print("2. [bold]View Flashcards[/bold]")
        console.print("3. [bold]Take Quiz[/bold]")
        console.print("4. [bold red]Exit[/bold red]")
        
        action = console.input("\nChoose an activity (1-4): ")

        if action == "1":
            clear_screen()
            console.print(Panel("[bold]📝 SUMMARY[/bold]"))
            # Render Markdown nicely
            md = Markdown(study_data['summary'])
            console.print(md)
            console.input("\n[dim]Press Enter to go back...[/dim]")

        elif action == "2":
            for idx, card in enumerate(study_data['flashcards'], 1):
                clear_screen()
                console.print(Panel(f"Card {idx}/{len(study_data['flashcards'])}"))
                console.print(f"\n[bold cyan]FRONT:[/bold cyan] {card['front']}")
                console.input("\n[dim][Press Enter to flip][/dim]")
                console.print(f"\n[bold green]BACK: [/bold green] {card['back']}")
                console.input("\n[dim][Press Enter for next card][/dim]")

        elif action == "3":
            score = 0
            clear_screen()
            console.print(Panel("[bold]📝 QUIZ TIME[/bold]"))
            
            for idx, q in enumerate(study_data['quiz'], 1):
                console.print(f"\n[bold]Q{idx}: {q['question']}[/bold]")
                for opt in q['options']:
                    console.print(opt)
                
                user_ans = console.input("\nYour Answer (A/B/C/D): ").upper()
                correct_letter = q['correct_answer'][0].upper()
                
                if user_ans == correct_letter:
                    console.print("[bold green]✅ Correct![/bold green]")
                    # UPDATED: Show the explanation
                    console.print(f"[italic cyan]💡 {q.get('explanation', 'No explanation provided.')}[/italic cyan]")
                    score += 1
                else:
                    console.print(f"[bold red]❌ Wrong.[/bold red] The correct answer was: {q['correct_answer']}")
                    # UPDATED: Show the explanation
                    console.print(f"[italic cyan]💡 Explanation: {q.get('explanation', 'No explanation provided.')}[/italic cyan]")
                
                console.input("[dim]Press Enter for next question...[/dim]")
            
            console.print(f"\n[bold yellow]Final Score: {score}/{len(study_data['quiz'])}[/bold yellow]")
            console.input("\n[dim]Press Enter to go back...[/dim]")

        elif action == "4":
            console.print("[bold green]Happy Studying! 👋[/bold green]")
            break

if __name__ == "__main__":
    main()