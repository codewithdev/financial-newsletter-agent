import os
import subprocess
import time 
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.style import Style

#Loading env variables from the .env file
load_dotenv(override=True)

#Initialize OpenAI client

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#Customization of console I/O
console = Console()


def run_agent(command, agent_name):
    """Runs an agent and captures its output"""
    with console.status(f"[bold green]Running {agent_name}...", spinner="bouncingBar"):
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode!=0:
            console.print(Panel(f"[bold red]Error running {agent_name}:[/bold red]\n {result.stderr}",
                                title="Error", expand=False, border_style="red"))
            return False
        return True
    
def analyze_content(file_path, input_prompt):
    """Use OpenAI API to analyze a file's content based on a given prompt."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content= file.read()
    with console.status("[bold blue] Analyzing content...", spinner="dots"):
        response = client.chat.completions.create(
            model = "gpt-4o",
            message = [
                {"role": "system", "content": input_prompt},
                {"role": "user", "content": content }
            ]
        )
    analysis = response.choices[0].message.content.strip()
    return analysis


def main():
    console.print(Panel("Newsletter Generation Process", style="bold yellow"))

    #Collect news from the article (web_agent.py)

    if not run_agent('python web_agent.py', 'web_agent.py'):
        return
    
    #Analysis of content on content.txt

    analysis_prompt= ("You are an expert editor for a tech newsletter. Assess the following collected news articles "
        "for relevance, quality, and engagement. Identify any issues and suggest improvements. "
        "If the content is suitable, confirm that it meets the standards.")
    content_analysis= analyze_content('content.txt', analysis_prompt)
    console.print(Panel(content_analysis, title="Content Analysis", expand=False, border_style="blue"))


# Some more code


if __name__ == "__main__":
    main()





