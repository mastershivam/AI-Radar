from HuggingFace_data_puller import HuggingFace_BlogPost_Puller
from OpenAI_data_puller import OpenAI_BlogPost_Puller
from Anthropic_data_puller import Anthropic_BlogPost_Puller
from datetime import date


def main():
    date_input=date(2025, 7, 23)
    prompt = f"Access the link provided, summarise the blog post, and return a summary of the blog post in a couple of lines.\n"

    # these functions take an optional 'date' variable that can be used to specify a date: usage (date=date(2025, 7, 25)))
    HuggingFace_BlogPost_Puller(prompt,date_input)
    OpenAI_BlogPost_Puller(prompt,date_input)
    Anthropic_BlogPost_Puller(prompt,date_input)
    
main()