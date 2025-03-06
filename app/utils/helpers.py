import pprint

def stream(graph, formatted_input):
        # Execute workflow and collect results
        results = []
        for output in graph.stream(formatted_input):
            for key, value in output.items():
                pprint.pprint(f"Output from node '{key}':")
                pprint.pprint("---")
                pprint.pprint(value, indent=2, width=80, depth=None)
                pprint.pprint("\n---\n")
                results.append(value['messages'][0])

        finalMessage = results[-1]
        return finalMessage

def invoke(graph, formatted_input):
    response = graph.invoke(formatted_input)
    finalMessage = response["messages"][-1]
    return finalMessage