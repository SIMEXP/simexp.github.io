# Project Organization

## Components
- **Slack Channel**  
  Each project must have a dedicated Slack channel, created using a standardized project template. This channel should include:
  - **Project Overview:** A summary listing team members, their roles, and links to all key resources (e.g., Google Docs, GitHub repositories, project website).
  - **Task Manager:** A dedicated space for tracking project tasks and deadlines.

- **GitHub Repositories**  
  Every distinct project component should be housed in its own GitHub repository. This modular structure promotes clarity and simplifies collaboration.

## Naming Conventions
- **Slack Channel:**  
  Adopt the format `project-<name>`, where `<name>` is entirely in lowercase and may include subcomponents separated by hyphens.  
  *Example:* `project-mario-curiosity`.

- **GitHub Repositories:**  
  Use the format `<project_name>.<component_name>`, with underscores permitted in both parts.  
  *Example:* `mario_curiosity.scene_agents`.  
  *Note:* Although the Slack channel uses hyphens, the GitHub naming convention favors underscores for readability and consistency.

- **Special Cases – Github repositories for Reusable Datasets:**  
  For datasets intended for community sharing (e.g., datasets collected by CNeuroMod):
  - The `<project_name>` should correspond to the dataset’s name.
  - The `<component_name>` should describe a well-documented processing pipeline designed for reuse.

  Conversely, datasets generated specifically for a single project—without broader community reuse—should be managed as standard project components under the primary `<project_name>`.
