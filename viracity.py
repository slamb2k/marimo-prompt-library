""" 
The Viracity app is a tool that allows users to interact with 
various language models (LLMs) to generate text based on a selected prompt. 
The app provides a selection of LLMs to choose from, as well as a selection 
of prompts to use with the chosen LLM. 
Users can also input their own prompts and fill in placeholders to generate text. 
The app is designed to be user-friendly and accessible to users with no prior experience with LLMs. 
"""

import marimo

__generated_with = "0.9.9"
app = marimo.App(width="medium", app_title="Viracity", css_file="vira.css")


@app.cell
def __():
    import re
    import html
    import json
    import marimo as mo
    import risk_json_to_md as rjtm
    from src.marimo_notebook.modules import prompt_library_module, llm_module
    import re  # For regex to extract placeholders
    from openai import AzureOpenAI
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    return (
        AzureOpenAI,
        DefaultAzureCredential,
        get_bearer_token_provider,
        html,
        json,
        llm_module,
        mo,
        prompt_library_module,
        re,
        rjtm,
    )


@app.cell
def __(
    AzureOpenAI,
    DefaultAzureCredential,
    get_bearer_token_provider,
    prompt_library_module,
):
    map_prompt_library: dict = prompt_library_module.pull_in_prompt_library()

    token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

    client = AzureOpenAI(
        azure_endpoint="https://gpt-review.openai.azure.com/",
        azure_ad_token_provider=token_provider,
        api_version="2024-05-01-preview",
    )
    return client, map_prompt_library, token_provider


@app.cell
def __(llm_module):
    llm_o1_mini, llm_o1_preview = llm_module.build_o1_series()
    llm_gpt_4o_latest, llm_gpt_4o_mini = llm_module.build_openai_latest_and_fastest()
    # llm_sonnet = llm_module.build_sonnet_3_5()
    # gemini_1_5_pro, gemini_1_5_flash = llm_module.build_gemini_duo()

    services = {
        "aoai-standard": "Azure OpenAI",
        "aoai-on-your-data": "Azure OpenAI On Your Data",
        "openai": "OpenAI",
    }

    models = {
        "o1-mini": llm_o1_mini,
        "o1-preview": llm_o1_preview,
        "gpt-4o-latest": llm_gpt_4o_latest,
        "gpt-4o-mini": llm_gpt_4o_mini,
        # "sonnet-3.5": llm_sonnet,
        # "gemini-1-5-pro": gemini_1_5_pro,
        # "gemini-1-5-flash": gemini_1_5_flash,
    }
    return (
        llm_gpt_4o_latest,
        llm_gpt_4o_mini,
        llm_o1_mini,
        llm_o1_preview,
        models,
        services,
    )


@app.cell
def __():
    prompt_styles = {"padding": "10px", "border-radius": "10px", "color": "grey"}
    return (prompt_styles,)


@app.cell
def __(mo):
    mo.md("""<h1 style="text-align: center; font-family: Sixtyfour Convergence; font-size: 64pt">VIRACITY</h1>""")
    return


@app.cell
def __(mo, prompt_styles, selected_prompt):
    prompt_template = mo.vstack(
        [
            mo.md("""
            <br/>
            
            ## Prompt Template
            """),
            mo.accordion(
                {
                    "Expand to view details...": mo.md(
                        f"```xml\n{selected_prompt}\n```"
                    ).style(prompt_styles)
                }
            ),
        ]
    )

    prompt_template
    return (prompt_template,)


@app.cell
def __(map_prompt_library, mo):
    request_args = mo.ui.dictionary(
        {
            "max_tokens": mo.ui.number(0,4096,128,16),
            "temperature": mo.ui.slider(0,1,0.05,0.1,show_value=True),
            "top_p": mo.ui.slider(0,1,0.05,0.1,show_value=True),
            "n": mo.ui.slider(1,128,1,1,show_value=True),
            "presence_penalty": mo.ui.slider(-2,2,1,0,show_value=True),
            "frequency_penalty": mo.ui.slider(-2,2,1,0,show_value=True)
        }
    )

    selected_prompt_name = "pr-risk-review.xml"
    selected_prompt = map_prompt_library[selected_prompt_name]

    prompt_args = mo.ui.dictionary(
        {
            "max_tokens": mo.ui.number(0,4096,128,16),
            "temperature": mo.ui.slider(0,1,0.05,0.1,show_value=True),
            "top_p": mo.ui.slider(0,1,0.05,0.1,show_value=True),
            "n": mo.ui.slider(1,128,1,1,show_value=True),
            "presence_penalty": mo.ui.slider(-2,2,1,0,show_value=True),
            "frequency_penalty": mo.ui.slider(-2,2,1,0,show_value=True)
        }
    )
    return prompt_args, request_args, selected_prompt, selected_prompt_name


@app.cell
def __(mo, re, rjtm, selected_prompt, selected_prompt_name):
    mo.stop(not selected_prompt_name or not selected_prompt, "")

    # Extract placeholders from the prompt
    placeholders = re.findall(r"\{\{(.*?)\}\}", selected_prompt)
    placeholders = list(set(placeholders))  # Remove duplicates

    code_files = rjtm.get_example_code_files()
    diff = rjtm.get_example_diff()

    # Create text areas for placeholders, using the placeholder text as the label
    placeholder_inputs = [
        mo.ui.text_area(label=ph, placeholder=f"Enter {ph}", value = code_files if ph == "code-files" else diff, rows=10, full_width=True)
        for ph in placeholders
    ]

    # Create an array of placeholder inputs
    placeholder_array = mo.ui.array(
        placeholder_inputs,
        label="variables",
    )
    return (
        code_files,
        diff,
        placeholder_array,
        placeholder_inputs,
        placeholders,
    )


@app.cell
def __(mo, models, services):
    service_dropdown = mo.ui.dropdown(
        options=services,
        label="Select an AI Service",
        value="aoai-standard",
    )
    model_dropdown = mo.ui.dropdown(
        options=models,
        label="Select an LLM Model",
        value="gpt-4o-latest",
    )
    return model_dropdown, service_dropdown


@app.cell
def __(mo):
    inscope_check = mo.ui.checkbox(
        label="Only indexed docs",
    )

    strictness_slider = mo.ui.slider(
        start=1,
        stop=5,
        step=1,
        label="Strictness",
    )
    return inscope_check, strictness_slider


@app.cell
def __(
    inscope_check,
    mo,
    model_dropdown,
    placeholder_array,
    request_args,
    service_dropdown,
    strictness_slider,
):
    tab1 = mo.hstack(
      [request_args, request_args.value],
      justify="space-between"
    )

    tab2 = mo.vstack([placeholder_array])

    tab3 = mo.vstack([service_dropdown, model_dropdown])

    tab4 = mo.vstack([inscope_check, strictness_slider])
    return tab1, tab2, tab3, tab4


@app.cell
def __(mo, tab1, tab2, tab3, tab4):
    tabs = mo.ui.tabs(
        {
            "LLM Params": tab1,
            "Prompt Arguments": tab2,
            "Execution Arguments": tab3,
            "On Your Data": tab4
        }
    )

    run_cell = mo.vstack(
        [
            mo.md("""
            <br/>

            ## Prompt Options
            """),
            mo.accordion(
                {
                    "Expand to view options...": tabs
                }
            ),
        ]
    )

    run_cell
    return run_cell, tabs


@app.cell
def __(mo):
    execute_prompt_button = mo.ui.run_button(label="Run Prompt")

    button_cell = mo.vstack(
        [
            mo.md("""
            <br/>
            <br/>
            """),
            execute_prompt_button,
        ]
    )

    button_cell
    return button_cell, execute_prompt_button


@app.cell
def __(execute_prompt_button, mo, placeholder_array, placeholders):
    mo.stop(not placeholder_array.value or not len(placeholder_array.value), "")

    # Check if any values are missing
    if any(not value.strip() for value in placeholder_array.value):
        mo.stop(True, mo.md("**Please fill in all placeholders.**"))

    # Ensure the 'Proceed' button has been pressed
    mo.stop(
        not execute_prompt_button.value,
        mo.md("Please press the 'Run Prompt' button to continue."),
    )

    # Map the placeholder names to the values
    filled_values = dict(zip(placeholders, placeholder_array.value))
    return (filled_values,)


@app.cell
def __(filled_values, selected_prompt):
    # Replace placeholders in the prompt
    final_prompt = selected_prompt
    for key, value in filled_values.items():
        final_prompt = final_prompt.replace(f"{{{{{key}}}}}", value)

    # Create context_filled_prompt
    context_filled_prompt = final_prompt
    return context_filled_prompt, final_prompt, key, value


@app.cell
def __(context_filled_prompt, mo, prompt_styles):
    mo.vstack(
        [
            # mo.md("""
            # <br/>
            # <br/>
            # """),
            mo.accordion(
                {
                    "#### Expand to view executed prompt...": mo.md(
                        f"```xml\n{context_filled_prompt}\n```"
                    ).style(prompt_styles)
                }
            ),
            mo.md("<br/>"),
        ]
    )
    return


@app.cell
def __(client, context_filled_prompt, mo, model_dropdown):
    search_endpoint = "https://virasecurity.search.windows.net"
    search_index = "virasecurity"
    system_prompt_old = """You are an expert assistant specialised in the review of code for potential risks and security issues.

    - YOU MUST GENERATE CITATION BASED ON THE RETRIEVED DOCUMENTS IN YOUR RESPONSE
    - You are polite, helpful and knowledgeable, but if you don't know the answer, let the user know and do not make up the answer!
    - You are expected to provide a detailed analysis of the code provided and suggest possible fixes.
    - You should search the indexed documents for the most relevant information to provide the best possible response.
    - The response should be outputted in JSON.
    """

    system_prompt = """You are an expert in software security and code review, tasked with analyzing the provided code for potential risks and security issues. Your goal is to provide a detailed, well-researched, and actionable security review for the provided source code. Security review should be based on external knowledge as well as retrieved documents.

    When the user provides the code changes in the _diff-of-code_, follow these steps:

    <thinking>
    1. Carefully review the provided _diff-of-code_ and search the indexed documents for relevant information that can help you identify potential risks and security issues in the code, as well as suggest possible fixes.
    3. Extract the most relevant information from the retrieved documents and organize it in a structured way to support your analysis.
    4. Prioritize suggesting security issues that you are either CONFIDENT of or if it is highly related to the retrieved documents.
    5. Always provide inline citations to any retrieved documents used to support your analysis.
    6. The response should be outputted in JSON.
    </thinking>"""

    # Get the selected model
    model = model_dropdown.value
    # Run the prompt through the model using context_filled_prompt
    with mo.status.spinner(title="Running prompt..."):
        completion = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=4096,
            response_format={ "type": "json_object" },
            temperature=0.0000001,
            top_p=0.001,
            seed=42,
            messages=[
                {
                    "role": "user",
                    "content": context_filled_prompt,
                }
            ],
            extra_body={
                "data_sources": [
                    {
                        "type": "azure_search",
                        "parameters": {
                            "endpoint": search_endpoint,
                            "index_name": search_index,
                            "in_scope": False,
                            "strictness": 3,
                            "top_n_documents": 11,
                            "query_type": "vector_semantic_hybrid",
                            "embedding_dependency": {
                                "type": "deployment_name",
                                "deployment_name": "text-embedding-ada-002",
                            },
                            "semantic_configuration": "default",
                            "allow_partial_result": True,
                            "authentication": {
                                "type": "system_assigned_managed_identity"
                            },
                            "role_information": system_prompt
                        }
                    }
                ]
            }
        )

    print(f"Completion: {completion}")

    prompt_response = completion.choices[0].message.content
    prompt_context = completion.choices[0].message.context

    print(f"Unformatted Response: {prompt_response}")

    mo.md(f"<br/><br/>\n# **Prompt Output**\n---\n{completion.model_dump_json(indent=2)}")

    # render the citations
    for citation_index, citation in enumerate(prompt_context["citations"]):
        # Extract the citation information from the response, so we
        # can render it in the output more effectively.
        url = citation["url"]
        filepath = citation["filepath"]
        chunk_id = citation["chunk_id"]
        title = citation["title"]
        snippet = citation["content"].replace(title, f"🔗 {title}")

        # The citation reference (e.g. [doc1], [doc2], etc.) to find and replace
        # with a new hyperlink and tooltip containing the content of the citation.
        # If available, the source url will also be provided.
        citation_reference = f"[doc{citation_index + 1}]"

        citation_content = f"{mo.md(snippet)}".replace("\"", "'")
        citation_content = citation_content.replace("\\u200b", "")
        citation_content = citation_content.replace("\\","\\\\")
        citation_content = citation_content.replace("SE_DENY_REMOTE_INTERACTIVE_LOGON_NAME,SE_BATCH_LOGON_NAME,SE_DENY_NETWORK_LOGON_NAME,SE_INTERACTIVE_LOGON_NAME",
                                                    "SE_DENY_REMOTE_INTERACTIVE_LOGON_NAME, SE_BATCH_LOGON_NAME, SE_DENY_NETWORK_LOGON_NAME, SE_INTERACTIVE_LOGON_NAME")
        

        citation_detail = f"<details><summary>{title} - [View File]({url})</summary><br/><div style='padding: 20px 30px 30px 30px;'>{citation_content}</div></details>"

        prompt_response = prompt_response.replace(citation_reference, citation_detail)

    print(prompt_response)
    return (
        chunk_id,
        citation,
        citation_content,
        citation_detail,
        citation_index,
        citation_reference,
        completion,
        filepath,
        model,
        prompt_context,
        prompt_response,
        search_endpoint,
        search_index,
        snippet,
        system_prompt,
        system_prompt_old,
        title,
        url,
    )


@app.cell
def __(llm_module, mo, prompt_response, rjtm):
    # Clean off any backticks if the json is returned as a code block
    json_response = llm_module.parse_markdown_backticks(prompt_response)

    # Set vertical alignment for markdown table cells to the top
    table_cell_styles = """<style>
            /* Vertically align all table content to the top */
            .markdown table td {
                vertical-align: top;
            }
        </style>
        """

    # Run the prompt through the model using context_filled_prompt
    with mo.status.spinner(title="Formatting output..."):
        formatted_output = rjtm.json_to_markdown(json_response)

    print(f"Formatted Response: {formatted_output}")

    mo.md(f"{table_cell_styles}<br/><br/>\n\n\n{formatted_output}")
    return formatted_output, json_response, table_cell_styles


if __name__ == "__main__":
    app.run()
