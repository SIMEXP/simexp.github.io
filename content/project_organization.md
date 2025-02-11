# Project organization

## Components
 * a slack channel, created using a project template
   * project overview, with list of members and roles, as well as links to all the main elements (gdocs, github repos, website)
   * task manager
 * One github repo per component of the project


## Naming conventions
 * slack: `project-<name>` where name is all lower case, and can have subcomponents separated by hyphens that work well without  hyphens. For example `project-mario-curiosity`, where `mariocuriosity` also works.
 * github: `<project_name>.<component>`. Example `mario_curiosity.scene_agents` (project name is similar to slack, but with `_` instead of `.`)
 * Special cases: datasets. For datasets, `component` need to be a well documented processing pipeline designed to be reused for anyone interested in the dataset.
