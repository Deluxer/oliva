import pprint

def stream(graph, formatted_input, config=None):
    # Execute workflow and collect results
    results = []
    for output in graph.stream(formatted_input, config=config):
        for key, value in output.items():
            pprint.pprint(f"Output from node '{key}':")
            pprint.pprint("---")
            pprint.pprint(value, indent=2, width=80, depth=None)
            pprint.pprint("\n---\n")
            results.append(value['messages'])

    finalMessage = results[0][-1]
    return finalMessage.content

def invoke(graph, formatted_input, config=None):
    response = graph.invoke(formatted_input, config=config)
    finalMessage = response["messages"][-1]
    return finalMessage.content