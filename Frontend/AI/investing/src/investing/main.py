import warnings
from investing.crew import Investing

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run(ticker):
    """
    Run the crew.
    """
    inputs = {
        'ticker': ticker,
    }
    
    try:
        Investing().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
    
def testing():
    """
    Crew testing 
    """

    inputs = {
        'ticker': 'SOL',
    }

    try:
        Investing().crew().test(inputs=inputs, n_iterations=10, eval_llm=False)
    except Exception as e:
        raise Exception(e)
    

if __name__ == '__main__':
    testing()
