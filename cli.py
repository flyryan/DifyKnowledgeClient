#!/usr/bin/env python3
import os
import sys
from typing import Optional, Dict, Any, List
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.text import Text
from rich import box
from rich.columns import Columns
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import click

from dify_client.client import DifyClient
from dify_client.api_client import APIError

console = Console()


class DifyInteractiveCLI:
    """Interactive CLI for Dify Knowledge Base management."""
    
    def __init__(self):
        try:
            self.client = DifyClient()
            self.current_dataset_id = None
            self.current_dataset_name = None
            self.current_document_id = None
            self.current_document_name = None
        except Exception as e:
            console.print(f"[red]Error initializing client: {e}[/red]")
            sys.exit(1)
    
    def print_header(self):
        """Print the application header."""
        console.clear()
        console.print(Panel.fit(
            "[bold cyan]Dify Knowledge Base Client[/bold cyan]\n"
            "[dim]Interactive interface for managing knowledge bases[/dim]",
            border_style="cyan"
        ))
    
    def print_current_context(self):
        """Print current context (selected KB and document)."""
        if self.current_dataset_name:
            context = f"[green]KB:[/green] {self.current_dataset_name}"
            if self.current_document_name:
                context += f" | [green]Doc:[/green] {self.current_document_name}"
            console.print(Panel(context, title="Current Context", border_style="dim"))
    
    def main_menu(self):
        """Display main menu."""
        while True:
            self.print_header()
            self.print_current_context()
            
            menu_items = [
                "1. Knowledge Base Management",
                "2. Document Management",
                "3. Segment/Chunk Management",
                "4. Search & Retrieval",
                "5. Metadata Management",
                "0. Exit"
            ]
            
            console.print("\n[bold]Main Menu:[/bold]")
            for item in menu_items:
                console.print(f"  {item}")
            
            choice = Prompt.ask("\n[cyan]Select option[/cyan]", choices=["0", "1", "2", "3", "4", "5"])
            
            if choice == "0":
                if Confirm.ask("\n[yellow]Are you sure you want to exit?[/yellow]"):
                    console.print("[green]Goodbye![/green]")
                    break
            elif choice == "1":
                self.knowledge_base_menu()
            elif choice == "2":
                self.document_menu()
            elif choice == "3":
                self.segment_menu()
            elif choice == "4":
                self.retrieval_menu()
            elif choice == "5":
                self.metadata_menu()
    
    def knowledge_base_menu(self):
        """Knowledge base management menu."""
        while True:
            self.print_header()
            self.print_current_context()
            
            menu_items = [
                "1. List Knowledge Bases",
                "2. Create Knowledge Base",
                "3. Select Knowledge Base",
                "4. View Current KB Details",
                "5. Update Current KB",
                "6. Delete Current KB",
                "7. View Available Embedding Models",
                "0. Back to Main Menu"
            ]
            
            console.print("\n[bold]Knowledge Base Management:[/bold]")
            for item in menu_items:
                console.print(f"  {item}")
            
            choice = Prompt.ask("\n[cyan]Select option[/cyan]", choices=["0", "1", "2", "3", "4", "5", "6", "7"])
            
            if choice == "0":
                break
            elif choice == "1":
                self.list_knowledge_bases()
            elif choice == "2":
                self.create_knowledge_base()
            elif choice == "3":
                self.select_knowledge_base()
            elif choice == "4":
                self.view_knowledge_base_details()
            elif choice == "5":
                self.update_knowledge_base()
            elif choice == "6":
                self.delete_knowledge_base()
            elif choice == "7":
                self.view_embedding_models()
    
    def list_knowledge_bases(self):
        """List all knowledge bases."""
        try:
            keyword = Prompt.ask("\nSearch keyword (optional)", default="")
            page = IntPrompt.ask("Page", default=1)
            limit = IntPrompt.ask("Items per page", default=20)
            
            with console.status("[bold green]Loading knowledge bases..."):
                response = self.client.knowledge_bases.list_datasets(
                    keyword=keyword if keyword else None,
                    page=page,
                    limit=limit
                )
            
            if not response.get('data'):
                console.print("\n[yellow]No knowledge bases found.[/yellow]")
                return
            
            table = Table(title="Knowledge Bases", box=box.ROUNDED)
            table.add_column("ID", style="dim", width=36)
            table.add_column("Name", style="cyan", no_wrap=True)
            table.add_column("Docs", justify="right", style="green")
            table.add_column("Words", justify="right", style="green")
            table.add_column("Permission", style="yellow")
            table.add_column("Indexing", style="magenta")
            
            for kb in response['data']:
                table.add_row(
                    kb['id'],
                    kb['name'],
                    str(kb.get('document_count', 0)),
                    str(kb.get('word_count', 0)),
                    kb.get('permission', 'N/A'),
                    kb.get('indexing_technique', 'N/A')
                )
            
            console.print(table)
            console.print(f"\n[dim]Page {page} of {response.get('total', 0) // limit + 1} | Total: {response.get('total', 0)}[/dim]")
            
        except APIError as e:
            console.print(f"\n[red]API Error: {e}[/red]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def create_knowledge_base(self):
        """Create a new knowledge base."""
        try:
            console.print("\n[bold]Create New Knowledge Base[/bold]")
            
            name = Prompt.ask("Name")
            description = Prompt.ask("Description (optional)", default="")
            
            indexing_technique = Prompt.ask(
                "Indexing technique",
                choices=["high_quality", "economy", "none"],
                default="none"
            )
            
            permission = Prompt.ask(
                "Permission",
                choices=["only_me", "all_team_members", "partial_members"],
                default="only_me"
            )
            
            data = {
                'name': name,
                'permission': permission
            }
            
            if description:
                data['description'] = description
            
            if indexing_technique != "none":
                data['indexing_technique'] = indexing_technique
                
                # If indexing technique is set, ask for embedding model
                if Confirm.ask("Configure embedding model?", default=True):
                    provider = Prompt.ask("Embedding model provider (e.g., zhipuai)")
                    model = Prompt.ask("Embedding model name (e.g., embedding-3)")
                    data['embedding_model_provider'] = provider
                    data['embedding_model'] = model
                
                # Ask for retrieval model configuration
                if Confirm.ask("Configure retrieval model?", default=True):
                    search_method = Prompt.ask(
                        "Search method",
                        choices=["semantic_search", "keyword_search", "full_text_search", "hybrid_search"],
                        default="semantic_search"
                    )
                    top_k = IntPrompt.ask("Top K results", default=2)
                    
                    retrieval_model = self.client.knowledge_bases.create_retrieval_model(
                        search_method=search_method,
                        top_k=top_k
                    )
                    data['retrieval_model'] = retrieval_model
            
            with console.status("[bold green]Creating knowledge base..."):
                response = self.client.knowledge_bases.create_dataset(**data)
            
            console.print(f"\n[green]✓ Knowledge base created successfully![/green]")
            console.print(f"[dim]ID: {response['id']}[/dim]")
            
            if Confirm.ask("\nSelect this knowledge base?", default=True):
                self.current_dataset_id = response['id']
                self.current_dataset_name = response['name']
            
        except APIError as e:
            console.print(f"\n[red]API Error: {e}[/red]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def select_knowledge_base(self):
        """Select a knowledge base to work with."""
        try:
            # First list available KBs
            with console.status("[bold green]Loading knowledge bases..."):
                response = self.client.knowledge_bases.list_datasets(limit=100)
            
            if not response.get('data'):
                console.print("\n[yellow]No knowledge bases found.[/yellow]")
                return
            
            # Create a mapping of names to IDs
            kb_map = {kb['name']: kb['id'] for kb in response['data']}
            kb_names = list(kb_map.keys())
            
            # Use prompt_toolkit for autocomplete
            completer = WordCompleter(kb_names, ignore_case=True)
            
            console.print("\n[bold]Available Knowledge Bases:[/bold]")
            for name in kb_names:
                console.print(f"  • {name}")
            
            selected_name = prompt(
                "\nEnter knowledge base name: ",
                completer=completer
            )
            
            if selected_name in kb_map:
                self.current_dataset_id = kb_map[selected_name]
                self.current_dataset_name = selected_name
                console.print(f"\n[green]✓ Selected: {selected_name}[/green]")
            else:
                console.print(f"\n[red]Knowledge base '{selected_name}' not found.[/red]")
            
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def view_knowledge_base_details(self):
        """View details of current knowledge base."""
        if not self.current_dataset_id:
            console.print("\n[yellow]No knowledge base selected.[/yellow]")
            Prompt.ask("\n[dim]Press Enter to continue[/dim]")
            return
        
        try:
            with console.status("[bold green]Loading knowledge base details..."):
                kb = self.client.knowledge_bases.get_dataset(self.current_dataset_id)
            
            # Create details panel
            details = f"""
[bold]Name:[/bold] {kb.get('name', 'N/A')}
[bold]ID:[/bold] {kb.get('id', 'N/A')}
[bold]Description:[/bold] {kb.get('description') or 'None'}
[bold]Permission:[/bold] {kb.get('permission', 'N/A')}
[bold]Provider:[/bold] {kb.get('provider', 'N/A')}
[bold]Documents:[/bold] {kb.get('document_count', 0)}
[bold]Words:[/bold] {kb.get('word_count', 0):,}
[bold]Apps:[/bold] {kb.get('app_count', 0)}
[bold]Indexing Technique:[/bold] {kb.get('indexing_technique') or 'Not set'}
[bold]Embedding Model:[/bold] {kb.get('embedding_model') or 'Not set'}
[bold]Embedding Provider:[/bold] {kb.get('embedding_model_provider') or 'Not set'}
"""
            
            console.print(Panel(details, title="Knowledge Base Details", border_style="cyan"))
            
            # Show retrieval model if available
            if kb.get('retrieval_model_dict'):
                rm = kb['retrieval_model_dict']
                retrieval_details = f"""
[bold]Search Method:[/bold] {rm.get('search_method', 'N/A')}
[bold]Top K:[/bold] {rm.get('top_k', 'N/A')}
[bold]Reranking:[/bold] {'Enabled' if rm.get('reranking_enable') else 'Disabled'}
[bold]Score Threshold:[/bold] {'Enabled' if rm.get('score_threshold_enabled') else 'Disabled'}
"""
                console.print(Panel(retrieval_details, title="Retrieval Model", border_style="magenta"))
            
        except APIError as e:
            console.print(f"\n[red]API Error: {e}[/red]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def update_knowledge_base(self):
        """Update current knowledge base."""
        if not self.current_dataset_id:
            console.print("\n[yellow]No knowledge base selected.[/yellow]")
            Prompt.ask("\n[dim]Press Enter to continue[/dim]")
            return
        
        try:
            console.print("\n[bold]Update Knowledge Base[/bold]")
            console.print("[dim]Leave blank to keep current value[/dim]\n")
            
            data = {}
            
            name = Prompt.ask("Name (optional)", default="")
            if name:
                data['name'] = name
            
            description = Prompt.ask("Description (optional)", default="")
            if description:
                data['description'] = description
            
            if Confirm.ask("Update indexing technique?", default=False):
                indexing = Prompt.ask(
                    "Indexing technique",
                    choices=["high_quality", "economy"],
                    default="high_quality"
                )
                data['indexing_technique'] = indexing
            
            if Confirm.ask("Update permission?", default=False):
                permission = Prompt.ask(
                    "Permission",
                    choices=["only_me", "all_team_members", "partial_members"],
                    default="only_me"
                )
                data['permission'] = permission
            
            if Confirm.ask("Update embedding model?", default=False):
                provider = Prompt.ask("Embedding model provider")
                model = Prompt.ask("Embedding model name")
                data['embedding_model_provider'] = provider
                data['embedding_model'] = model
            
            if Confirm.ask("Update retrieval model?", default=False):
                search_method = Prompt.ask(
                    "Search method",
                    choices=["semantic_search", "keyword_search", "full_text_search", "hybrid_search"],
                    default="semantic_search"
                )
                top_k = IntPrompt.ask("Top K results", default=2)
                
                retrieval_model = self.client.knowledge_bases.create_retrieval_model(
                    search_method=search_method,
                    top_k=top_k
                )
                data['retrieval_model'] = retrieval_model
            
            if data:
                with console.status("[bold green]Updating knowledge base..."):
                    response = self.client.knowledge_bases.update_dataset(
                        self.current_dataset_id,
                        **data
                    )
                
                console.print(f"\n[green]✓ Knowledge base updated successfully![/green]")
                
                if 'name' in data:
                    self.current_dataset_name = data['name']
            else:
                console.print("\n[yellow]No updates specified.[/yellow]")
            
        except APIError as e:
            console.print(f"\n[red]API Error: {e}[/red]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def delete_knowledge_base(self):
        """Delete current knowledge base."""
        if not self.current_dataset_id:
            console.print("\n[yellow]No knowledge base selected.[/yellow]")
            Prompt.ask("\n[dim]Press Enter to continue[/dim]")
            return
        
        try:
            console.print(f"\n[bold red]Delete Knowledge Base: {self.current_dataset_name}[/bold red]")
            
            if Confirm.ask("\n[red]Are you sure? This action cannot be undone![/red]", default=False):
                confirm_name = Prompt.ask(f"\nType the name '{self.current_dataset_name}' to confirm")
                
                if confirm_name == self.current_dataset_name:
                    with console.status("[bold red]Deleting knowledge base..."):
                        self.client.knowledge_bases.delete_dataset(self.current_dataset_id)
                    
                    console.print(f"\n[green]✓ Knowledge base deleted successfully![/green]")
                    self.current_dataset_id = None
                    self.current_dataset_name = None
                    self.current_document_id = None
                    self.current_document_name = None
                else:
                    console.print("\n[yellow]Deletion cancelled - name did not match.[/yellow]")
            else:
                console.print("\n[yellow]Deletion cancelled.[/yellow]")
            
        except APIError as e:
            console.print(f"\n[red]API Error: {e}[/red]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def view_embedding_models(self):
        """View available embedding models."""
        try:
            with console.status("[bold green]Loading embedding models..."):
                response = self.client.knowledge_bases.get_available_embedding_models()
            
            if not response.get('data'):
                console.print("\n[yellow]No embedding models found.[/yellow]")
                return
            
            for provider in response['data']:
                provider_name = provider['label'].get('en_US', provider['provider'])
                console.print(f"\n[bold cyan]{provider_name}[/bold cyan] ({provider['provider']})")
                console.print(f"[dim]Status: {provider['status']}[/dim]")
                
                if provider.get('models'):
                    table = Table(box=box.SIMPLE)
                    table.add_column("Model", style="green")
                    table.add_column("Type", style="yellow")
                    table.add_column("Context Size", justify="right")
                    table.add_column("Status", style="cyan")
                    
                    for model in provider['models']:
                        table.add_row(
                            model['model'],
                            model.get('model_type', 'N/A'),
                            str(model.get('model_properties', {}).get('context_size', 'N/A')),
                            model.get('status', 'N/A')
                        )
                    
                    console.print(table)
            
        except APIError as e:
            console.print(f"\n[red]API Error: {e}[/red]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def document_menu(self):
        """Document management menu."""
        if not self.current_dataset_id:
            console.print("\n[yellow]Please select a knowledge base first.[/yellow]")
            Prompt.ask("\n[dim]Press Enter to continue[/dim]")
            return
        
        while True:
            self.print_header()
            self.print_current_context()
            
            menu_items = [
                "1. List Documents",
                "2. Create Document from Text",
                "3. Create Document from File",
                "4. Select Document",
                "5. Update Current Document",
                "6. Delete Current Document",
                "7. Check Indexing Status",
                "0. Back to Main Menu"
            ]
            
            console.print("\n[bold]Document Management:[/bold]")
            for item in menu_items:
                console.print(f"  {item}")
            
            choice = Prompt.ask("\n[cyan]Select option[/cyan]", choices=["0", "1", "2", "3", "4", "5", "6", "7"])
            
            if choice == "0":
                break
            elif choice == "1":
                self.list_documents()
            elif choice == "2":
                self.create_document_from_text()
            elif choice == "3":
                self.create_document_from_file()
            elif choice == "4":
                self.select_document()
            elif choice == "5":
                self.update_document()
            elif choice == "6":
                self.delete_document()
            elif choice == "7":
                self.check_indexing_status()
    
    def list_documents(self):
        """List documents in current knowledge base."""
        try:
            keyword = Prompt.ask("\nSearch keyword (optional)", default="")
            page = IntPrompt.ask("Page", default=1)
            limit = IntPrompt.ask("Items per page", default=20)
            
            with console.status("[bold green]Loading documents..."):
                response = self.client.documents.list_documents(
                    self.current_dataset_id,
                    keyword=keyword if keyword else None,
                    page=page,
                    limit=limit
                )
            
            if not response.get('data'):
                console.print("\n[yellow]No documents found.[/yellow]")
                return
            
            table = Table(title="Documents", box=box.ROUNDED)
            table.add_column("Name", style="cyan")
            table.add_column("Status", style="yellow")
            table.add_column("Words", justify="right", style="green")
            table.add_column("Created", style="dim")
            table.add_column("ID", style="dim", width=36)
            
            for doc in response['data']:
                status_color = "green" if doc.get('indexing_status') == 'completed' else "yellow"
                table.add_row(
                    doc['name'],
                    f"[{status_color}]{doc.get('indexing_status', 'N/A')}[/{status_color}]",
                    str(doc.get('word_count', 0)),
                    doc.get('created_from', 'N/A'),
                    doc['id']
                )
            
            console.print(table)
            console.print(f"\n[dim]Page {page} of {response.get('total', 0) // limit + 1} | Total: {response.get('total', 0)}[/dim]")
            
        except APIError as e:
            console.print(f"\n[red]API Error: {e}[/red]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def create_document_from_text(self):
        """Create a document from text input."""
        try:
            console.print("\n[bold]Create Document from Text[/bold]")
            
            name = Prompt.ask("Document name")
            
            console.print("\n[dim]Enter document text (press Ctrl+D when done):[/dim]")
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                pass
            
            text = "\n".join(lines)
            
            if not text.strip():
                console.print("\n[yellow]No text entered. Cancelled.[/yellow]")
                return
            
            indexing = Prompt.ask(
                "Indexing technique",
                choices=["high_quality", "economy"],
                default="high_quality"
            )
            
            # Advanced options
            data = {
                'name': name,
                'text': text,
                'indexing_technique': indexing
            }
            
            if Confirm.ask("\nConfigure advanced options?", default=False):
                doc_form = Prompt.ask(
                    "Document form",
                    choices=["text_model", "qa_model", "hierarchical_model"],
                    default="text_model"
                )
                data['doc_form'] = doc_form
                
                if doc_form == 'qa_model':
                    lang = Prompt.ask("Document language (e.g., English, Chinese)", default="English")
                    data['doc_language'] = lang
                
                # Process rule
                mode = Prompt.ask(
                    "Processing mode",
                    choices=["automatic", "custom", "hierarchical"],
                    default="automatic"
                )
                
                if mode == "custom":
                    separator = Prompt.ask("Segment separator", default="\\n")
                    max_tokens = IntPrompt.ask("Max tokens per segment", default=1000)
                    
                    process_rule = self.client.documents.create_process_rule(
                        mode="custom",
                        segmentation={
                            'separator': separator,
                            'max_tokens': max_tokens
                        }
                    )
                    data['process_rule'] = process_rule
                else:
                    data['process_rule'] = {'mode': mode}
            
            with console.status("[bold green]Creating document..."):
                response = self.client.documents.create_document_from_text(
                    self.current_dataset_id,
                    **data
                )
            
            console.print(f"\n[green]✓ Document created successfully![/green]")
            console.print(f"[dim]ID: {response['document']['id']}[/dim]")
            console.print(f"[dim]Status: {response['document']['indexing_status']}[/dim]")
            
            if response.get('batch'):
                console.print(f"[dim]Batch: {response['batch']}[/dim]")
            
        except APIError as e:
            console.print(f"\n[red]API Error: {e}[/red]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def create_document_from_file(self):
        """Create a document from file upload."""
        try:
            console.print("\n[bold]Create Document from File[/bold]")
            
            file_path = Prompt.ask("File path")
            
            # Check if file exists
            if not Path(file_path).exists():
                console.print(f"\n[red]File not found: {file_path}[/red]")
                return
            
            indexing = Prompt.ask(
                "Indexing technique",
                choices=["high_quality", "economy"],
                default="high_quality"
            )
            
            # Prepare data
            data = {
                'file_path': file_path,
                'indexing_technique': indexing
            }
            
            if Confirm.ask("\nConfigure advanced options?", default=False):
                doc_form = Prompt.ask(
                    "Document form",
                    choices=["text_model", "qa_model", "hierarchical_model"],
                    default="text_model"
                )
                data['doc_form'] = doc_form
                
                if doc_form == 'qa_model':
                    lang = Prompt.ask("Document language (e.g., English, Chinese)", default="English")
                    data['doc_language'] = lang
                
                # Process rule
                mode = Prompt.ask(
                    "Processing mode",
                    choices=["automatic", "custom", "hierarchical"],
                    default="automatic"
                )
                
                if mode == "custom":
                    separator = Prompt.ask("Segment separator", default="\\n")
                    max_tokens = IntPrompt.ask("Max tokens per segment", default=1000)
                    
                    process_rule = self.client.documents.create_process_rule(
                        mode="custom",
                        segmentation={
                            'separator': separator,
                            'max_tokens': max_tokens
                        }
                    )
                    data['process_rule'] = process_rule
                else:
                    data['process_rule'] = {'mode': mode}
            
            with console.status("[bold green]Uploading document..."):
                response = self.client.documents.create_document_from_file(
                    self.current_dataset_id,
                    **data
                )
            
            console.print(f"\n[green]✓ Document uploaded successfully![/green]")
            console.print(f"[dim]ID: {response['document']['id']}[/dim]")
            console.print(f"[dim]Name: {response['document']['name']}[/dim]")
            console.print(f"[dim]Status: {response['document']['indexing_status']}[/dim]")
            
            if response.get('batch'):
                console.print(f"[dim]Batch: {response['batch']}[/dim]")
            
        except APIError as e:
            console.print(f"\n[red]API Error: {e}[/red]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def select_document(self):
        """Select a document to work with."""
        try:
            # First list available documents
            with console.status("[bold green]Loading documents..."):
                response = self.client.documents.list_documents(
                    self.current_dataset_id,
                    limit=100
                )
            
            if not response.get('data'):
                console.print("\n[yellow]No documents found.[/yellow]")
                return
            
            # Create a mapping of names to IDs
            doc_map = {doc['name']: doc['id'] for doc in response['data']}
            doc_names = list(doc_map.keys())
            
            # Use prompt_toolkit for autocomplete
            completer = WordCompleter(doc_names, ignore_case=True)
            
            console.print("\n[bold]Available Documents:[/bold]")
            for name in doc_names:
                console.print(f"  • {name}")
            
            selected_name = prompt(
                "\nEnter document name: ",
                completer=completer
            )
            
            if selected_name in doc_map:
                self.current_document_id = doc_map[selected_name]
                self.current_document_name = selected_name
                console.print(f"\n[green]✓ Selected: {selected_name}[/green]")
            else:
                console.print(f"\n[red]Document '{selected_name}' not found.[/red]")
            
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def update_document(self):
        """Update current document."""
        if not self.current_document_id:
            console.print("\n[yellow]No document selected.[/yellow]")
            Prompt.ask("\n[dim]Press Enter to continue[/dim]")
            return
        
        try:
            console.print("\n[bold]Update Document[/bold]")
            
            update_type = Prompt.ask(
                "Update type",
                choices=["text", "file"],
                default="text"
            )
            
            if update_type == "text":
                name = Prompt.ask("New name (optional)", default="")
                
                if Confirm.ask("Update document text?", default=False):
                    console.print("\n[dim]Enter new text (press Ctrl+D when done):[/dim]")
                    lines = []
                    try:
                        while True:
                            line = input()
                            lines.append(line)
                    except EOFError:
                        pass
                    
                    text = "\n".join(lines)
                else:
                    text = None
                
                if name or text:
                    with console.status("[bold green]Updating document..."):
                        response = self.client.documents.update_document_by_text(
                            self.current_dataset_id,
                            self.current_document_id,
                            name=name if name else None,
                            text=text if text else None
                        )
                    
                    console.print(f"\n[green]✓ Document updated successfully![/green]")
                    
                    if name:
                        self.current_document_name = name
                else:
                    console.print("\n[yellow]No updates specified.[/yellow]")
            
            else:  # file
                file_path = Prompt.ask("File path")
                
                if not Path(file_path).exists():
                    console.print(f"\n[red]File not found: {file_path}[/red]")
                    return
                
                name = Prompt.ask("New name (optional)", default="")
                
                with console.status("[bold green]Updating document..."):
                    response = self.client.documents.update_document_by_file(
                        self.current_dataset_id,
                        self.current_document_id,
                        file_path,
                        name=name if name else None
                    )
                
                console.print(f"\n[green]✓ Document updated successfully![/green]")
                
                if name:
                    self.current_document_name = name
            
        except APIError as e:
            console.print(f"\n[red]API Error: {e}[/red]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def delete_document(self):
        """Delete current document."""
        if not self.current_document_id:
            console.print("\n[yellow]No document selected.[/yellow]")
            Prompt.ask("\n[dim]Press Enter to continue[/dim]")
            return
        
        try:
            console.print(f"\n[bold red]Delete Document: {self.current_document_name}[/bold red]")
            
            if Confirm.ask("\n[red]Are you sure? This action cannot be undone![/red]", default=False):
                with console.status("[bold red]Deleting document..."):
                    self.client.documents.delete_document(
                        self.current_dataset_id,
                        self.current_document_id
                    )
                
                console.print(f"\n[green]✓ Document deleted successfully![/green]")
                self.current_document_id = None
                self.current_document_name = None
            else:
                console.print("\n[yellow]Deletion cancelled.[/yellow]")
            
        except APIError as e:
            console.print(f"\n[red]API Error: {e}[/red]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def check_indexing_status(self):
        """Check document indexing status."""
        try:
            batch = Prompt.ask("\nEnter batch number")
            
            with console.status("[bold green]Checking indexing status..."):
                response = self.client.documents.get_document_indexing_status(
                    self.current_dataset_id,
                    batch
                )
            
            if not response.get('data'):
                console.print("\n[yellow]No indexing information found.[/yellow]")
                return
            
            for doc in response['data']:
                status_color = "green" if doc.get('indexing_status') == 'completed' else "yellow"
                
                details = f"""
[bold]Document ID:[/bold] {doc.get('id', 'N/A')}
[bold]Status:[/bold] [{status_color}]{doc.get('indexing_status', 'N/A')}[/{status_color}]
[bold]Progress:[/bold] {doc.get('completed_segments', 0)}/{doc.get('total_segments', 0)} segments
[bold]Started:[/bold] {doc.get('processing_started_at', 'N/A')}
[bold]Completed:[/bold] {doc.get('completed_at', 'N/A')}
"""
                
                if doc.get('error'):
                    details += f"[bold red]Error:[/bold red] {doc['error']}"
                
                console.print(Panel(details, title="Indexing Status", border_style="cyan"))
            
        except APIError as e:
            console.print(f"\n[red]API Error: {e}[/red]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def segment_menu(self):
        """Segment/chunk management menu."""
        if not self.current_dataset_id or not self.current_document_id:
            console.print("\n[yellow]Please select a knowledge base and document first.[/yellow]")
            Prompt.ask("\n[dim]Press Enter to continue[/dim]")
            return
        
        while True:
            self.print_header()
            self.print_current_context()
            
            menu_items = [
                "1. List Segments",
                "2. Add Segments",
                "3. Update Segment",
                "4. Delete Segment",
                "5. Manage Child Chunks",
                "0. Back to Main Menu"
            ]
            
            console.print("\n[bold]Segment Management:[/bold]")
            for item in menu_items:
                console.print(f"  {item}")
            
            choice = Prompt.ask("\n[cyan]Select option[/cyan]", choices=["0", "1", "2", "3", "4", "5"])
            
            if choice == "0":
                break
            elif choice == "1":
                self.list_segments()
            elif choice == "2":
                self.add_segments()
            elif choice == "3":
                self.update_segment()
            elif choice == "4":
                self.delete_segment()
            elif choice == "5":
                self.manage_child_chunks()
    
    def list_segments(self):
        """List segments in current document."""
        try:
            keyword = Prompt.ask("\nSearch keyword (optional)", default="")
            page = IntPrompt.ask("Page", default=1)
            limit = IntPrompt.ask("Items per page", default=20)
            
            with console.status("[bold green]Loading segments..."):
                response = self.client.segments.list_segments(
                    self.current_dataset_id,
                    self.current_document_id,
                    keyword=keyword if keyword else None,
                    page=page,
                    limit=limit
                )
            
            if not response.get('data'):
                console.print("\n[yellow]No segments found.[/yellow]")
                return
            
            console.print(f"\n[bold]Document Form: {response.get('doc_form', 'N/A')}[/bold]")
            
            for i, segment in enumerate(response['data'], 1):
                console.print(f"\n[bold cyan]Segment {i}:[/bold cyan]")
                console.print(f"[dim]ID: {segment['id']}[/dim]")
                console.print(f"[bold]Content:[/bold] {segment['content'][:200]}{'...' if len(segment['content']) > 200 else ''}")
                
                if segment.get('answer'):
                    console.print(f"[bold]Answer:[/bold] {segment['answer'][:200]}{'...' if len(segment['answer']) > 200 else ''}")
                
                console.print(f"[dim]Words: {segment.get('word_count', 0)} | Tokens: {segment.get('tokens', 0)} | Hits: {segment.get('hit_count', 0)}[/dim]")
                
                if segment.get('keywords'):
                    console.print(f"[dim]Keywords: {', '.join(segment['keywords'])}[/dim]")
                
                console.print(f"[dim]Status: {segment.get('status', 'N/A')} | Enabled: {segment.get('enabled', True)}[/dim]")
                console.print("─" * 50)
            
            console.print(f"\n[dim]Page {page} of {response.get('total', 0) // limit + 1} | Total: {response.get('total', 0)}[/dim]")
            
        except APIError as e:
            console.print(f"\n[red]API Error: {e}[/red]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def add_segments(self):
        """Add segments to current document."""
        try:
            console.print("\n[bold]Add Segments[/bold]")
            
            segments = []
            
            while True:
                console.print(f"\n[cyan]Segment {len(segments) + 1}:[/cyan]")
                
                content = Prompt.ask("Content")
                if not content:
                    break
                
                segment = {'content': content}
                
                # Check if document is in Q&A mode
                if Confirm.ask("Is this a Q&A segment?", default=False):
                    answer = Prompt.ask("Answer")
                    segment['answer'] = answer
                
                if Confirm.ask("Add keywords?", default=False):
                    keywords_str = Prompt.ask("Keywords (comma-separated)")
                    keywords = [k.strip() for k in keywords_str.split(',') if k.strip()]
                    segment['keywords'] = keywords
                
                segments.append(segment)
                
                if not Confirm.ask("\nAdd another segment?", default=True):
                    break
            
            if segments:
                with console.status("[bold green]Adding segments..."):
                    response = self.client.segments.add_segments(
                        self.current_dataset_id,
                        self.current_document_id,
                        segments
                    )
                
                console.print(f"\n[green]✓ Added {len(segments)} segment(s) successfully![/green]")
            else:
                console.print("\n[yellow]No segments added.[/yellow]")
            
        except APIError as e:
            console.print(f"\n[red]API Error: {e}[/red]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def update_segment(self):
        """Update a segment."""
        try:
            segment_id = Prompt.ask("\nSegment ID")
            
            console.print("\n[bold]Update Segment[/bold]")
            console.print("[dim]Leave blank to keep current value[/dim]\n")
            
            data = {}
            
            if Confirm.ask("Update content?", default=False):
                content = Prompt.ask("New content")
                data['content'] = content
            
            if Confirm.ask("Update answer?", default=False):
                answer = Prompt.ask("New answer")
                data['answer'] = answer
            
            if Confirm.ask("Update keywords?", default=False):
                keywords_str = Prompt.ask("Keywords (comma-separated)")
                keywords = [k.strip() for k in keywords_str.split(',') if k.strip()]
                data['keywords'] = keywords
            
            if Confirm.ask("Update enabled status?", default=False):
                enabled = Confirm.ask("Enabled?", default=True)
                data['enabled'] = enabled
            
            if data:
                with console.status("[bold green]Updating segment..."):
                    response = self.client.segments.update_segment(
                        self.current_dataset_id,
                        self.current_document_id,
                        segment_id,
                        **data
                    )
                
                console.print(f"\n[green]✓ Segment updated successfully![/green]")
            else:
                console.print("\n[yellow]No updates specified.[/yellow]")
            
        except APIError as e:
            console.print(f"\n[red]API Error: {e}[/red]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def delete_segment(self):
        """Delete a segment."""
        try:
            segment_id = Prompt.ask("\nSegment ID")
            
            if Confirm.ask("\n[red]Are you sure you want to delete this segment?[/red]", default=False):
                with console.status("[bold red]Deleting segment..."):
                    self.client.segments.delete_segment(
                        self.current_dataset_id,
                        self.current_document_id,
                        segment_id
                    )
                
                console.print(f"\n[green]✓ Segment deleted successfully![/green]")
            else:
                console.print("\n[yellow]Deletion cancelled.[/yellow]")
            
        except APIError as e:
            console.print(f"\n[red]API Error: {e}[/red]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def manage_child_chunks(self):
        """Manage child chunks (hierarchical mode)."""
        console.print("\n[yellow]Child chunk management is for hierarchical mode documents.[/yellow]")
        console.print("[dim]This feature allows managing sub-segments within parent segments.[/dim]")
        
        # This would need a submenu similar to segment management
        # For brevity, I'll skip the full implementation
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def retrieval_menu(self):
        """Search and retrieval menu."""
        if not self.current_dataset_id:
            console.print("\n[yellow]Please select a knowledge base first.[/yellow]")
            Prompt.ask("\n[dim]Press Enter to continue[/dim]")
            return
        
        while True:
            self.print_header()
            self.print_current_context()
            
            menu_items = [
                "1. Search Knowledge Base",
                "2. Advanced Search with Custom Settings",
                "0. Back to Main Menu"
            ]
            
            console.print("\n[bold]Search & Retrieval:[/bold]")
            for item in menu_items:
                console.print(f"  {item}")
            
            choice = Prompt.ask("\n[cyan]Select option[/cyan]", choices=["0", "1", "2"])
            
            if choice == "0":
                break
            elif choice == "1":
                self.search_knowledge_base()
            elif choice == "2":
                self.advanced_search()
    
    def search_knowledge_base(self):
        """Search the knowledge base."""
        try:
            query = Prompt.ask("\nSearch query")
            
            if not query:
                console.print("\n[yellow]No query entered.[/yellow]")
                return
            
            with console.status("[bold green]Searching..."):
                response = self.client.retrieval.retrieve_chunks(
                    self.current_dataset_id,
                    query
                )
            
            if not response.get('records'):
                console.print(f"\n[yellow]No results found for '{query}'.[/yellow]")
                return
            
            console.print(f"\n[bold]Search Results for '{query}':[/bold]")
            
            for i, record in enumerate(response['records'], 1):
                segment = record['segment']
                score = record.get('score', 0)
                
                console.print(f"\n[bold cyan]Result {i}:[/bold cyan]")
                console.print(f"[bold]Document:[/bold] {segment.get('document', {}).get('name', 'N/A')}")
                console.print(f"[bold]Content:[/bold] {segment['content'][:300]}{'...' if len(segment['content']) > 300 else ''}")
                
                if segment.get('answer'):
                    console.print(f"[bold]Answer:[/bold] {segment['answer'][:300]}{'...' if len(segment['answer']) > 300 else ''}")
                
                console.print(f"[dim]Score: {score:.6f} | Words: {segment.get('word_count', 0)} | Position: {segment.get('position', 'N/A')}[/dim]")
                
                if segment.get('keywords'):
                    console.print(f"[dim]Keywords: {', '.join(segment['keywords'][:5])}{'...' if len(segment['keywords']) > 5 else ''}[/dim]")
                
                console.print("─" * 50)
            
        except APIError as e:
            console.print(f"\n[red]API Error: {e}[/red]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def advanced_search(self):
        """Advanced search with custom retrieval settings."""
        try:
            query = Prompt.ask("\nSearch query")
            
            if not query:
                console.print("\n[yellow]No query entered.[/yellow]")
                return
            
            console.print("\n[bold]Configure Search Settings:[/bold]")
            
            search_method = Prompt.ask(
                "Search method",
                choices=["semantic_search", "keyword_search", "full_text_search", "hybrid_search"],
                default="semantic_search"
            )
            
            top_k = IntPrompt.ask("Number of results (top K)", default=5)
            
            reranking = Confirm.ask("Enable reranking?", default=False)
            
            retrieval_model_data = {
                'search_method': search_method,
                'top_k': top_k,
                'reranking_enable': reranking
            }
            
            if reranking:
                provider = Prompt.ask("Reranking provider")
                model = Prompt.ask("Reranking model")
                retrieval_model_data['reranking_provider_name'] = provider
                retrieval_model_data['reranking_model_name'] = model
            
            if search_method == 'hybrid_search':
                weight = float(Prompt.ask("Semantic search weight (0.0-1.0)", default="0.5"))
                retrieval_model_data['weights'] = weight
            
            if Confirm.ask("Enable score threshold?", default=False):
                threshold = float(Prompt.ask("Score threshold", default="0.0"))
                retrieval_model_data['score_threshold_enabled'] = True
                retrieval_model_data['score_threshold'] = threshold
            
            retrieval_model = self.client.retrieval.create_retrieval_model(**retrieval_model_data)
            
            with console.status("[bold green]Searching..."):
                response = self.client.retrieval.retrieve_chunks(
                    self.current_dataset_id,
                    query,
                    retrieval_model=retrieval_model
                )
            
            if not response.get('records'):
                console.print(f"\n[yellow]No results found for '{query}'.[/yellow]")
                return
            
            console.print(f"\n[bold]Advanced Search Results for '{query}':[/bold]")
            console.print(f"[dim]Method: {search_method} | Results: {len(response['records'])}[/dim]")
            
            for i, record in enumerate(response['records'], 1):
                segment = record['segment']
                score = record.get('score', 0)
                
                console.print(f"\n[bold cyan]Result {i}:[/bold cyan]")
                console.print(f"[bold]Document:[/bold] {segment.get('document', {}).get('name', 'N/A')}")
                console.print(f"[bold]Content:[/bold] {segment['content'][:300]}{'...' if len(segment['content']) > 300 else ''}")
                
                if segment.get('answer'):
                    console.print(f"[bold]Answer:[/bold] {segment['answer'][:300]}{'...' if len(segment['answer']) > 300 else ''}")
                
                console.print(f"[dim]Score: {score:.6f} | Words: {segment.get('word_count', 0)}[/dim]")
                console.print("─" * 50)
            
        except APIError as e:
            console.print(f"\n[red]API Error: {e}[/red]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def metadata_menu(self):
        """Metadata management menu."""
        if not self.current_dataset_id:
            console.print("\n[yellow]Please select a knowledge base first.[/yellow]")
            Prompt.ask("\n[dim]Press Enter to continue[/dim]")
            return
        
        while True:
            self.print_header()
            self.print_current_context()
            
            menu_items = [
                "1. List Metadata",
                "2. Create Metadata",
                "3. Update Metadata",
                "4. Delete Metadata",
                "5. Toggle Built-in Metadata",
                "0. Back to Main Menu"
            ]
            
            console.print("\n[bold]Metadata Management:[/bold]")
            for item in menu_items:
                console.print(f"  {item}")
            
            choice = Prompt.ask("\n[cyan]Select option[/cyan]", choices=["0", "1", "2", "3", "4", "5"])
            
            if choice == "0":
                break
            elif choice == "1":
                self.list_metadata()
            elif choice == "2":
                self.create_metadata()
            elif choice == "3":
                self.update_metadata()
            elif choice == "4":
                self.delete_metadata()
            elif choice == "5":
                self.toggle_builtin_metadata()
    
    def list_metadata(self):
        """List metadata for current knowledge base."""
        try:
            with console.status("[bold green]Loading metadata..."):
                response = self.client.retrieval.list_metadata(self.current_dataset_id)
            
            if not response.get('doc_metadata'):
                console.print("\n[yellow]No custom metadata found.[/yellow]")
            else:
                table = Table(title="Document Metadata", box=box.ROUNDED)
                table.add_column("ID", style="dim")
                table.add_column("Name", style="cyan")
                table.add_column("Type", style="yellow")
                table.add_column("Use Count", justify="right", style="green")
                
                for meta in response['doc_metadata']:
                    table.add_row(
                        meta['id'],
                        meta['name'],
                        meta['type'],
                        str(meta.get('use_count', 0))
                    )
                
                console.print(table)
            
            console.print(f"\n[bold]Built-in Metadata:[/bold] {'[green]Enabled[/green]' if response.get('built_in_field_enabled') else '[red]Disabled[/red]'}")
            
        except APIError as e:
            console.print(f"\n[red]API Error: {e}[/red]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def create_metadata(self):
        """Create new metadata."""
        try:
            console.print("\n[bold]Create Metadata[/bold]")
            
            name = Prompt.ask("Metadata name")
            metadata_type = Prompt.ask("Metadata type", default="string")
            
            with console.status("[bold green]Creating metadata..."):
                response = self.client.retrieval.create_metadata(
                    self.current_dataset_id,
                    metadata_type,
                    name
                )
            
            console.print(f"\n[green]✓ Metadata created successfully![/green]")
            console.print(f"[dim]ID: {response['id']}[/dim]")
            
        except APIError as e:
            console.print(f"\n[red]API Error: {e}[/red]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def update_metadata(self):
        """Update metadata."""
        try:
            metadata_id = Prompt.ask("\nMetadata ID")
            new_name = Prompt.ask("New name")
            
            with console.status("[bold green]Updating metadata..."):
                response = self.client.retrieval.update_metadata(
                    self.current_dataset_id,
                    metadata_id,
                    new_name
                )
            
            console.print(f"\n[green]✓ Metadata updated successfully![/green]")
            
        except APIError as e:
            console.print(f"\n[red]API Error: {e}[/red]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def delete_metadata(self):
        """Delete metadata."""
        try:
            metadata_id = Prompt.ask("\nMetadata ID")
            
            if Confirm.ask("\n[red]Are you sure you want to delete this metadata?[/red]", default=False):
                with console.status("[bold red]Deleting metadata..."):
                    self.client.retrieval.delete_metadata(
                        self.current_dataset_id,
                        metadata_id
                    )
                
                console.print(f"\n[green]✓ Metadata deleted successfully![/green]")
            else:
                console.print("\n[yellow]Deletion cancelled.[/yellow]")
            
        except APIError as e:
            console.print(f"\n[red]API Error: {e}[/red]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")
    
    def toggle_builtin_metadata(self):
        """Toggle built-in metadata."""
        try:
            action = Prompt.ask(
                "\nAction",
                choices=["enable", "disable"]
            )
            
            with console.status(f"[bold green]{action.capitalize()}ing built-in metadata..."):
                self.client.retrieval.toggle_builtin_metadata(
                    self.current_dataset_id,
                    action
                )
            
            console.print(f"\n[green]✓ Built-in metadata {action}d successfully![/green]")
            
        except APIError as e:
            console.print(f"\n[red]API Error: {e}[/red]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
        
        Prompt.ask("\n[dim]Press Enter to continue[/dim]")


@click.command()
def main():
    """Dify Knowledge Base Interactive Client"""
    cli = DifyInteractiveCLI()
    cli.main_menu()


if __name__ == "__main__":
    main()