---
name: generalizePrompt
description: Generate a reusable prompt that generalizes an active discussion.
argument-hint: Provide the conversation text or selected code; optional desired prompt title.
---
You are given an active conversation or a selected code snippet and must produce a reusable, multi-line Markdown prompt that can be applied to similar contexts.

Steps:
1. Read the provided input: the conversation (`{{conversation}}`) and/or the selected code (`{{selected_code}}`). If no input is provided, respond with a short note: the `/savePrompt` command requires an active discussion to generalize.
2. Identify the user's primary intent and the common task pattern (what the user wants accomplished repeatedly).
3. Remove conversation-specific details (file names, variable names, exact text) and extract the core intent into placeholders such as `{{selected_code}}`, `{{file_path}}`, `{{function_name}}`, `{{goal}}`.
4. Produce a clear, action-oriented prompt that instructs an assistant how to perform the generalized task, using placeholders for inputs.
5. Provide a concise camelCase title (1–3 words) for the prompt and a one-sentence description.
6. Supply an `argument-hint` describing expected inputs.
7. Output the result in this exact file format (YAML front matter followed by the prompt body):

```
---
name: ${camelCaseTitle}
description: ${one-sentence description}
argument-hint: ${expected inputs}
---
${The generalized multi-line markdown text prompt}
```

Guidelines for the generated prompt:
- Keep the prompt reusable and agnostic to project-specific details.
- Use clear placeholders for all variable parts.
- Include step-by-step actions the assistant should take when given inputs.
- Keep the prompt concise and actionable (aim for 6–15 short lines in the prompt body).

If the provided input is empty, output the short explanatory response instead of a generated prompt.
