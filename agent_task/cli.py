"""
CLI interface for the Task-Specific AI Agent Platform.
"""
from typing import Any
import os

from cleo.application import Application
from cleo.commands.command import Command
from cleo.helpers import argument, option
from rich.console import Console
from rich.table import Table
from rich.tree import Tree

from .task_manager import TaskManager
from .api import TaskHubAPI

console = Console()

class InitCommand(Command):
    """
    Create new task structure.
    
    init
        {task_name : Name of the task to create (alphanumeric and hyphens only)}
    """
    
    name = "init"
    description = "Create new task structure"
    arguments = [
        argument("task_name", "Name of the task to create (alphanumeric and hyphens only)")
    ]
    
    def handle(self) -> int:
        task_name = self.argument("task_name")
        try:
            project_dir = TaskManager.init_task(task_name)
            
            # Create tree view of the structure
            tree = Tree(f"[bold cyan]{task_name}/[/]")
            tree.add("[bold green]README.md[/]")
            
            rules_tree = tree.add("[bold yellow]rules/[/]")
            rules_tree.add("[bold green]rule.mdc[/]")
            
            mcp_tree = tree.add("[bold yellow]mcp/[/]")
            
            self.line(f"\nCreated new task: <info>{task_name}</info>")
            self.line(f"Location: {project_dir}")
            self.line("\nProject structure:")
            console.print(tree)
            return 0
        except Exception as e:
            self.line_error(f"Error creating task: {e}")
            return 1

class TasksCommand(Command):
    """
    Show saved tasks.
    
    tasks
        {--detail : Show detailed information about each task}
    """
    
    name = "tasks"
    description = "Show saved tasks"
    options = [
        option("detail", "d", "Show detailed information about each task")
    ]
    
    def handle(self) -> int:
        try:
            tasks = TaskManager.list_tasks()
            
            if not tasks:
                self.line("No tasks found.")
                return 0
            
            show_detail = self.option("detail")
            
            if show_detail:
                # Show detailed view
                for task in tasks:
                    console.print(f"\n[bold cyan]{task['name']}[/]")
                    console.print("=" * len(task['name']))
                    
                    if task.get('description'):
                        console.print(f"Description: {task['description']}")
                    
                    # Show metadata if available
                    if 'version' in task:
                        console.print(f"Version: {task['version']}")
                    if 'author' in task:
                        console.print(f"Author: {task['author']}")
                    if 'license' in task:
                        console.print(f"License: {task['license']}")
                    if 'tags' in task and task['tags']:
                        console.print(f"Tags: {', '.join(task['tags'])}")
                    
                    # Show components
                    components = []
                    if task['has_readme']:
                        components.append("[green]README[/]")
                    if task['has_rules']:
                        components.append("[yellow]Rules[/]")
                    if task['has_mcp']:
                        components.append("[blue]MCP[/]")
                    if components:
                        console.print("Components:", ", ".join(components))
                    
                    # Show files
                    if task['files']:
                        console.print("\nFiles:")
                        for file in task['files']:
                            console.print(f"  - {file}")
                            
                    console.print(f"Path: {task['path']}\n")
            else:
                # Show simple table view
                table = Table(title="Available Tasks")
                table.add_column("Name", style="cyan")
                table.add_column("Description", style="green")
                table.add_column("Components", style="yellow")
                
                for task in tasks:
                    components = []
                    if task['has_readme']:
                        components.append("README")
                    if task['has_rules']:
                        components.append("Rules")
                    if task['has_mcp']:
                        components.append("MCP")
                        
                    table.add_row(
                        task["name"],
                        task["description"] or "(no description)",
                        ", ".join(components) or "(empty)"
                    )
                
                console.print(table)
            
            return 0
        except Exception as e:
            self.line_error(f"Error listing tasks: {str(e)}")
            return 1

class LoadCommand(Command):
    """
    Import task to current project.
    
    load
        {task_name : Name of the task to load (must exist in tasks directory)}
    """
    
    name = "load"
    description = "Import task to current project"
    arguments = [
        argument("task_name", "Name of the task to load (must exist in tasks directory)")
    ]
    
    def handle(self) -> int:
        task_name = self.argument("task_name")
        try:
            TaskManager.load_task(task_name)
            self.line(f"Loaded task: <info>{task_name}</info>")
            return 0
        except Exception as e:
            self.line_error(f"Error loading task: {e}")
            return 1

class ArchiveCommand(Command):
    """
    Archive task to Cursor AI configuration.
    
    archive
        {task_name : Name of the task to archive (must exist in tasks directory)}
        {--remove-current : Remove the task files from current directory after archiving}
    """
    
    name = "archive"
    description = "Archive task to Cursor AI configuration"
    arguments = [
        argument("task_name", "Name of the task to archive (must exist in tasks directory)")
    ]
    options = [
        option("remove-current", None, "Remove the task files from current directory after archiving")
    ]
    
    def handle(self) -> int:
        task_name = self.argument("task_name")
        remove_current = self.option("remove-current")
        try:
            TaskManager.archive_task(task_name, remove_current=remove_current)
            self.line(f"Archived task: <info>{task_name}</info>")
            if remove_current:
                self.line("Removed task files from current directory")
            return 0
        except Exception as e:
            self.line_error(f"Error archiving task: {e}")
            return 1

class PublishCommand(Command):
    """
    Share task publicly.
    
    publish
        {task_name : Name of the task to publish (must exist in tasks directory)}
        {--user-id=default : User ID for publishing (default: 'default')}
    """
    
    name = "publish"
    description = "Share task publicly"
    arguments = [
        argument("task_name", "Name of the task to publish (must exist in tasks directory)")
    ]
    options = [
        option("user-id", "u", "User ID for publishing", flag=False, default="default")
    ]
    
    def handle(self) -> int:
        task_name = self.argument("task_name")
        user_id = self.option("user-id")
        
        try:
            url = TaskManager.publish_task(task_name, user_id)
            self.line(f"Published task: <info>{task_name}</info>")
            self.line(f"Task URL: {url}")
            return 0
            
        except Exception as e:
            self.line_error(f"Error publishing task: {str(e)}")
            return 1

class CloneCommand(Command):
    """
    Download from marketplace.
    
    clone
        {url : URL or path of the task to clone (e.g., user/task-name)}
    """
    
    name = "clone"
    description = "Download from marketplace"
    arguments = [
        argument("url", "URL or path of the task to clone (e.g., user/task-name)")
    ]
    
    def handle(self) -> int:
        url = self.argument("url")
        try:
            task_name = TaskManager.clone_task(url)
            self.line(f"Cloned task: <info>{task_name}</info>")
            return 0
        except Exception as e:
            self.line_error(f"Error cloning task: {e}")
            return 1

def create_application() -> Application:
    """Create and configure the CLI application."""
    app = Application("agent-task", "0.1.0")
    
    # Register commands
    app.add(InitCommand())
    app.add(TasksCommand())
    app.add(LoadCommand())
    app.add(ArchiveCommand())
    app.add(PublishCommand())
    app.add(CloneCommand())
    
    return app

def main() -> Any:
    """Main entry point for the CLI."""
    return create_application().run()

if __name__ == "__main__":
    main() 