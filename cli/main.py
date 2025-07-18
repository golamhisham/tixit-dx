import click
import requests
import os
import json

API_URL = "http://127.0.0.1:8000"
TOKEN_FILE = os.path.expanduser("~/.tixitdx_token")

# Helper functions
def save_token(token):
    with open(TOKEN_FILE, "w") as f:
        f.write(token)

def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    return None

def auth_headers():
    token = load_token()
    if not token:
        raise click.ClickException("You must login first.")
    return {"Authorization": f"Bearer {token}"}

@click.group()
def cli():
    """Tixit DX CLI"""
    pass

@cli.command()
def ping():
    """Check if CLI is working."""
    click.echo("CLI is working!")

@cli.command()
def login():
    """Login and store JWT token."""
    email = click.prompt("Email")
    password = click.prompt("Password", hide_input=True)
    resp = requests.post(f"{API_URL}/auth/login", json={"email": email, "password": password})
    if resp.status_code == 200:
        token = resp.json()["access_token"]
        save_token(token)
        click.echo("Login successful!")
    else:
        click.echo(f"Login failed: {resp.text}")

@cli.command()
def list_projects():
    """List all projects."""
    resp = requests.get(f"{API_URL}/projects", headers=auth_headers())
    if resp.status_code == 200:
        projects = resp.json()
        for p in projects:
            click.echo(f"[{p['id']}] {p['name']} - {p.get('description', '')}")
    else:
        click.echo(f"Error: {resp.text}")

@cli.command()
@click.option('--name', prompt=True)
@click.option('--description', prompt=True, default="")
def create_project(name, description):
    """Create a new project."""
    data = {"name": name, "description": description}
    resp = requests.post(f"{API_URL}/projects", json=data, headers=auth_headers())
    if resp.status_code == 200:
        click.echo(f"Project created: {resp.json()['id']}")
    else:
        click.echo(f"Error: {resp.text}")

@cli.command()
@click.option('--project-id', required=True, type=int)
@click.option('--title', prompt=True)
@click.option('--desc', prompt=True)
@click.option('--priority', prompt=True, default="medium")
@click.option('--status', prompt=True, default="open")
@click.option('--assigned-to', type=int, default=None)
def create_issue(project_id, title, desc, priority, status, assigned_to):
    """Create a new issue in a project."""
    data = {
        "title": title,
        "description": desc,
        "priority": priority,
        "status": status,
        "assigned_to": assigned_to
    }
    resp = requests.post(f"{API_URL}/projects/{project_id}/issues", json=data, headers=auth_headers())
    if resp.status_code == 200:
        click.echo(f"Issue created: {resp.json()['id']}")
    else:
        click.echo(f"Error: {resp.text}")

@cli.command()
@click.option('--project-id', required=True, type=int)
def list_issues(project_id):
    """List issues in a project."""
    resp = requests.get(f"{API_URL}/projects/{project_id}/issues", headers=auth_headers())
    if resp.status_code == 200:
        issues = resp.json()
        for i in issues:
            click.echo(f"[{i['id']}] {i['title']} - {i['status']} - {i['priority']}")
    else:
        click.echo(f"Error: {resp.text}")

if __name__ == "__main__":
    cli() 