# agent.py
from tools import load_csv, show_head, calculate_stats, correlation, generate_plot

# Optional OpenAI GPT (for fallback explanations)
try:
    from openai import OpenAI
    client = OpenAI()
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False

def ask_agent(prompt: str):
    if OPENAI_AVAILABLE:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            return response.choices[0].message.content
        except Exception:
            return f"GPT API not available or quota exceeded. Mock response: {prompt}"
    else:
        return f"GPT API not available. Mock response: {prompt}"

def process_nlp_query(query: str):
    """Detect basic NLP queries and run tools automatically."""
    q = query.lower()

    # Correlation
    if "correlation" in q:
        # detect columns
        cols = []
        if "revenue" in q:
            cols.append("Revenue")
        if "profit" in q:
            cols.append("Profit")
        if len(cols) >= 2:
            corr_matrix = correlation()
            corr_value = corr_matrix[cols[0]][cols[1]]
            return f"The correlation between {cols[0]} and {cols[1]} is {corr_value:.2f}"
        return "Please specify at least two numeric columns for correlation."

    # Statistics
    if "statistics" in q or "describe" in q or "summary" in q:
        stats_data = calculate_stats()
        return f"Summary statistics:\n{stats_data}"

    # Head / preview
    if "head" in q or "first rows" in q:
        return show_head()

    # Plot
    if "plot" in q:
        # naive detection for x and y columns
        if "revenue" in q and "profit" in q:
            return generate_plot(x_col="Revenue", y_col="Profit", plot_type="scatter")
        return "Please specify columns for plotting (e.g., Revenue vs Profit)."

    # If none matched, fallback to GPT
    return ask_agent(query)

if __name__ == "__main__":
    print("🚀 Autonomous AI Data Analyst with NLP is ready!")

    while True:
        query = input("Ask the agent (or type 'exit'): ")
        if query.lower() in ['exit','quit']:
            break

        # Simple tool command detection
        if query.startswith("load "):
            file = query.split(" ")[1]
            print(load_csv(file))
        elif query.startswith("head"):
            print(show_head())
        elif query.startswith("stats"):
            print(calculate_stats())
        elif query.startswith("corr"):
            print(correlation())
        elif query.startswith("plot"):
            parts = query.split(" ")
            if len(parts) == 4:
                x_col, y_col, plot_type = parts[1], parts[2], parts[3]
                print(generate_plot(x_col=x_col, y_col=y_col, plot_type=plot_type))
            else:
                print("Use: plot x_col y_col type")
        else:
            # NLP processing
            print(process_nlp_query(query))
