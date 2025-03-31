import google.generativeai as genai
def save_transaction(data):
    """Save transaction data to a text file."""
    ai_model_(data)
    
def ai_model_(data):
    sys_ins = """You are an AI agent specializing in fraud detection for financial transactions. Your task is to analyze a current transaction (Input 1) against historical transaction data (Input 2) and generate two outputs:  

1. *Fraud Score* (0–100): A numerical risk assessment.  

2. *Reasoning Summary*: A concise breakdown of anomalies detected.  



### *Instructions for Analysis:*  

1. *Process Inputs*:  

   - *Input 1 (Current Transaction)*: A comma-separated string in the format:  

     account_number,amount,time,transaction_type,ip. (If input transaction amount is negative or zero or else is the data is inconsistent then just give the output as -1 and for output2 give reason as invalid data)  

   - *Input 2 (Historical Transactions)*: A multi-line string of historical records in the schema:   (If input  data is inconsistent then just give the output as -1 and for output2 give reason as invalid data)  

     transaction_id,sender_account,receiver_account,amount,ip,transaction_type,currency,transaction_success,remarks,status,trans_time.  



2. *Apply Detection Criteria*:  

   - *Transaction Frequency*:  

     - Check recent transactions (last 1 hour, 24 hours) for spikes in activity or failed attempts.  

   - *Amount Anomaly*:  

     - Compare the current amount to historical averages/medians. Flag deviations >3× the average.  

   - *Time/Type Patterns*:  

     - Identify if the transaction occurs at unusual hours or mismatches the account’s typical transaction type (e.g., sudden international transfer).  

   - *IP Address*:  

     - Check if the IP is new, foreign, or inconsistent with historical patterns.  



3. *Score Calculation*:  

   - Assign weights to anomalies:  

     - *High Impact* (e.g., extreme amount deviation, foreign IP): +40–60 points.  

     - *Medium Impact* (e.g., unusual time, type mismatch): +20–40 points.  

     - *Low Impact* (e.g., minor frequency spike): +10–20 points.  

   - Combine weighted anomalies to calculate the final score (0–100).  



4. *Output Format*:  

   - *Fraud Score*: A number between 0 and 100.  

   - *Reasoning Summary*: A bulleted list of key findings, formatted as:  

       

     **Fraud Score:** [X]/100 ([Risk Level])  



     **Reasoning Summary:**  

     1. [Anomaly 1]  

     2. [Anomaly 2]  

     ...  

       



---  



### *Example Output*:  Fraud Score: 92/100 (High Risk)Reasoning Summary:Amount Deviation: Transaction amount (₹10,000) is 17.6× higher than the historical average (₹568).Unusual Timing: Transaction occurred at 02:00 AM, outside typical activity hours (09:00 AM – 04:00 PM).IP Consistency: IP address (192.168.1.10) matches historical domestic transactions (no anomaly).Copy---  



### *Rules*:  

- Prioritize clarity and brevity.  

- Use only line breaks and simple formatting (no markdown tables).  

- If no anomalies are found, state: "Low risk: No significant deviations detected."  

- Flag even minor inconsistencies for transparency.

  

give me the fraud score in the first output column and also given the fraud score in second output column with reasoning also"""
    res_3 = generate_response(sys_ins, f"{data}")

    return res_3
def generate_response(system_instruction: str, user_input: str) -> str:
    # Configure API key
    genai.configure(api_key="AIzaSyA8jsA-iZ9rbo60GwHEoTM0FdybbIItFx0")
    
    # Load the generative model
    model = genai.GenerativeModel("gemini-2.0-flash")  # Ensure model name is correct
    
    # Generate response
    response = model.generate_content(
        [system_instruction, user_input]  # Gemini API accepts a list of messages
    )
    
    # Extract text from the response
    response_text = response.text if hasattr(response, 'text') else "Error generating response"

    with open("response.txt", "w") as file:
        file.write(response_text)
    
    # print("Response:\n", response_text)
    return response_text