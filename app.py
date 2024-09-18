import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
import pandas as pd

# Global variables to keep track of the conversation state and selected options
conversation_state = None
selected_case_type = None
selected_act = None
selected_evidences = []
defendant_evidences = []

# Evidence types and weights
evidence_list = {
    1: "Contractual Documents",
    2: "Financial Records",
    3: "Performance Records",
    4: "Expert Testimony",
    5: "Digital Evidence",
    6: "Legal Documents",
    7: "Photographs and Videos",
    8: "Internal Memos and Reports",
    9: "Testimonies and Depositions",
    10: "Regulatory and Compliance Documents"
}
evidence_weights = {
    1: 0.15,  # Example weights for evidence
    2: 0.10,
    3: 0.10,
    4: 0.15,
    5: 0.10,
    6: 0.10,
    7: 0.05,
    8: 0.05,
    9: 0.10,
    10: 0.10
}

# Expanded list of acts under commercial courts
commercial_acts = {
    "Breach of Contract": {
        "acts": [
            "Indian Contract Act, 1872",
            "Specific Relief Act, 1963",
            "Sale of Goods Act, 1930",
            "Contracts Act, 2013"  # Example additional act
        ],
        "cross_complaints": {
            1: "The other party may argue that there was no valid contract or that they were not in breach.",
            2: "The defendant might file for non-performance due to impossibility or argue for damages instead of specific performance.",
            3: "The other party may claim that the goods were not of the quality agreed upon or were delivered late.",
            4: "The defendant could argue that the new Contracts Act, 2013 does not apply to the case."
        },
        "winning_strategies": {
            1: "To win under the Indian Contract Act, 1872, ensure that all contract terms are clear and were explicitly agreed upon. Collect all relevant communications and documents.",
            2: "Under the Specific Relief Act, 1963, focus on demonstrating that specific performance is the only adequate remedy and that monetary damages would be insufficient.",
            3: "For the Sale of Goods Act, 1930, provide evidence that the goods delivered were of the agreed-upon quality and were delivered on time.",
            4: "If using the Contracts Act, 2013, highlight how it applies to the contract and how the defendant's actions breach its provisions."
        }
    },
    "Intellectual Property Dispute": {
        "acts": [
            "Patents Act, 1970",
            "Trade Marks Act, 1999",
            "Copyright Act, 1957",
            "Design Act, 2000",  # Example additional act
            "Geographical Indications of Goods Act, 1999"  # Example additional act
        ],
        "cross_complaints": {
            1: "The defendant could argue that the patent is invalid or challenge the originality of the invention.",
            2: "The opposing party might claim that their use of the trademark is in good faith or not confusingly similar.",
            3: "The other party could argue for fair use or challenge the originality of the copyrighted work.",
            4: "The defendant might claim that the design is not unique or that it does not infringe on the plaintiff's rights.",
            5: "The other party could argue that the geographical indication is not valid or applicable."
        },
        "winning_strategies": {
            1: "For the Patents Act, 1970, establish the novelty and non-obviousness of your invention. Strong patent documentation and expert testimony can bolster your case.",
            2: "Under the Trade Marks Act, 1999, demonstrate the likelihood of confusion between the marks and establish the distinctiveness of your trademark.",
            3: "To win under the Copyright Act, 1957, prove the originality of the work and that the defendant's use does not qualify as fair use.",
            4: "For the Design Act, 2000, provide evidence that the design is original and has been copied by the defendant.",
            5: "Under the Geographical Indications of Goods Act, 1999, demonstrate that the geographical indication is valid and that the defendant's use infringes on it."
        }
    },
    "Corporate Governance Issue": {
        "acts": [
            "Companies Act, 2013",
            "SEBI Act, 1992",
            "Insolvency and Bankruptcy Code, 2016",
            "Depositories Act, 1996"  # Example additional act
        ],
        "cross_complaints": {
            1: "The opposing party might file a case for mismanagement or oppression if the governance issue is claimed to harm shareholders.",
            2: "The defendant may argue that the securities regulations were followed or that any discrepancies were minor.",
            3: "The other party may argue that the company is not actually insolvent or dispute the claims of financial distress.",
            4: "The defendant might claim that the depository regulations were adhered to and that the issue lies elsewhere."
        },
        "winning_strategies": {
            1: "To win under the Companies Act, 2013, provide evidence of good corporate governance practices and compliance with legal requirements. Documented board decisions can support your case.",
            2: "For the SEBI Act, 1992, focus on demonstrating strict compliance with securities regulations. Any discrepancies should be shown as minor and unintentional.",
            3: "In the case of the Insolvency and Bankruptcy Code, 2016, establish that the financial distress is genuine and provide a clear resolution plan.",
            4: "For the Depositories Act, 1996, present evidence that depository regulations were not followed by the opposing party."
        }
    },
    "Fraud and Misrepresentation": {
        "acts": [
            "Indian Penal Code, 1860",
            "Civil Procedure Code, 1908",
            "Consumer Protection Act, 2019",
            "Prevention of Corruption Act, 1988"  # Example additional act
        ],
        "cross_complaints": {
            1: "The defendant may argue that no fraudulent intent was present or that the alleged misrepresentation was not material.",
            2: "The other party might claim that the claims are exaggerated or that there was no actual harm caused.",
            3: "The defendant may assert that the complaint falls outside the scope of consumer protection or that the complaint was filed too late.",
            4: "The defendant might claim that any alleged corruption is not relevant to the current dispute."
        },
        "winning_strategies": {
            1: "Under the Indian Penal Code, 1860, gather evidence showing intent to deceive and the impact of the fraud.",
            2: "For the Civil Procedure Code, 1908, ensure all procedural requirements are met and present clear evidence of the misrepresentation.",
            3: "In the Consumer Protection Act, 2019, demonstrate how the misrepresentation harmed you as a consumer and provide strong evidence of the fraudulent practices.",
            4: "If invoking the Prevention of Corruption Act, 1988, present clear evidence of corrupt practices that support your case."
        }
    },
    "Partnership Disputes": {
        "acts": [
            "Indian Partnership Act, 1932",
            "Limited Liability Partnership Act, 2008",
            "Companies Act, 2013",
            "Partnership Act, 2019"  # Example additional act
        ],
        "cross_complaints": {
            1: "The opposing party may argue that the partnership agreement was not breached or that the issues are not as severe as claimed.",
            2: "The defendant might argue that the limited liability protections were violated or that the partnership was legally constituted.",
            3: "The other party may claim that the dispute is a result of internal mismanagement or that the issues fall under corporate governance rather than partnership disputes.",
            4: "The defendant could argue that the new Partnership Act, 2019 does not apply or that the provisions are not relevant."
        },
        "winning_strategies": {
            1: "Under the Indian Partnership Act, 1932, present a clear partnership agreement and evidence of the breach.",
            2: "For the Limited Liability Partnership Act, 2008, provide documentation showing adherence to LLP regulations and the nature of the dispute.",
            3: "In the context of the Companies Act, 2013, highlight how the issues relate to the partnership agreement and not corporate governance.",
            4: "If using the Partnership Act, 2019, show how the new provisions affect the dispute and how they support your position."
        }
    }
}


def chatbot_response(user_input):
    global conversation_state, selected_case_type, selected_act, selected_evidences, defendant_evidences

    if conversation_state is None:
        if "file case" in user_input.lower():
            conversation_state = "select_case_type"
            return "What type of case would you like to file?\n" + \
                   "\n".join([f"{i+1}. {case_type}" for i, case_type in enumerate(commercial_acts.keys())])
        else:
            return "Please specify that you want to file a case."

    elif conversation_state == "select_case_type":
        try:
            option = int(user_input)
            if option in range(1, len(commercial_acts) + 1):
                selected_case_type = list(commercial_acts.keys())[option - 1]
                conversation_state = "list_acts"
                return f"Here are the acts under which you can file a {selected_case_type} case:\n" + \
                       "\n".join([f"{i+1}. {act}" for i, act in enumerate(commercial_acts[selected_case_type]["acts"])]) + \
                       "\nPlease enter the number corresponding to the act."
            else:
                return "Please enter a valid number."
        except ValueError:
            return "Please enter a valid number."

    elif conversation_state == "list_acts":
        try:
            act_number = int(user_input)
            if act_number in range(1, len(commercial_acts[selected_case_type]["acts"]) + 1):
                selected_act = act_number
                conversation_state = "give_winning_advice"
                return f"You've selected Act {act_number}. " \
                       f"The other party might file a cross-complaint as follows:\n" + \
                       commercial_acts[selected_case_type]["cross_complaints"].get(act_number, "No information available.") + \
                       "\nWould you like to know how you can win this case? (yes/no)"
            else:
                return "Please enter a valid number corresponding to the act."
        except ValueError:
            return "Please enter a valid number."

    elif conversation_state == "give_winning_advice":
        if user_input.lower() in ["yes", "y"]:
            conversation_state = "ask_evidence"
            return "Great! To calculate your winning percentage, I need to know which evidence you have. Please select from the following options:\n" + \
                   "\n".join([f"{num}. {desc}" for num, desc in evidence_list.items()]) + \
                   "\nEnter the serial numbers of the evidence you have, separated by commas (e.g., 1, 2, 4)."
        else:
            conversation_state = None
            return "Okay, let me know if you need further assistance."

    elif conversation_state == "ask_evidence":
        try:
            selected_evidences = list(map(int, user_input.split(',')))
            conversation_state = "ask_defendant_evidence"
            return "Thank you. Now, please enter the serial numbers of the evidence that the defendant has, separated by commas (e.g., 1, 2, 4)."
        except ValueError:
            return "Please enter valid serial numbers separated by commas."

    elif conversation_state == "ask_defendant_evidence":
        try:
            defendant_evidences = list(map(int, user_input.split(',')))
            plaintiff_winning_percentage = calculate_winning_percentage(selected_evidences)
            defendant_winning_percentage = calculate_winning_percentage(defendant_evidences)
            
            if plaintiff_winning_percentage > defendant_winning_percentage:
                winner = "You (Plaintiff)"
                result_message = f"Based on the evidence:\n" \
                                 f"Your winning percentage: {plaintiff_winning_percentage:.2f}%\n" \
                                 f"Defendant's winning percentage: {defendant_winning_percentage:.2f}%\n" \
                                 f"{winner} has a better chance of winning the case."
            elif defendant_winning_percentage > plaintiff_winning_percentage:
                result_message = f"Based on the evidence:\n" \
                                 f"Your winning percentage: {plaintiff_winning_percentage:.2f}%\n" \
                                 f"Defendant's winning percentage: {defendant_winning_percentage:.2f}%\n" \
                                 f"The Defendant has a better chance of winning the case.\n" \
                                 f"You might consider appealing for a stay to collect more evidence.\n" \
                                 f"Would you like to know how to appeal for a stay order? (yes/no)"
            else:
                result_message = f"Based on the evidence:\n" \
                                 f"Your winning percentage: {plaintiff_winning_percentage:.2f}%\n" \
                                 f"Defendant's winning percentage: {defendant_winning_percentage:.2f}%\n" \
                                 f"Neither party has a clear advantage based on the evidence."

            conversation_state = "appeal_advice"
            return result_message
        except ValueError:
            return "Please enter valid serial numbers separated by commas."

    elif conversation_state == "appeal_advice":
        if user_input.lower() in ["yes", "y"]:
            return "To appeal for a stay order to collect more evidence, you should follow these steps:\n" \
                   "1. File a formal application with the court requesting a stay of proceedings. Clearly state the reasons why you need additional time to collect evidence.\n" \
                   "2. Provide a detailed explanation of the evidence you are seeking and how it will impact the case.\n" \
                   "3. Demonstrate that the additional evidence is crucial for your case and that you have acted diligently but require more time.\n" \
                   "4. Include any supporting documentation or affidavits that justify your request.\n" \
                   "5. Attend the court hearing where the application will be considered and present your case convincingly.\n" \
                   "6. Await the court's decision on the stay order application. If granted, ensure you collect and submit the additional evidence promptly."

        else:
            conversation_state = None
            return "Okay, let me know if you need further assistance."

    elif conversation_state == "view_past_cases":
        return open_past_case_file()

def calculate_winning_percentage(evidence_list):
    total_weight = sum(evidence_weights.get(evidence, 0) for evidence in evidence_list)
    base_percentage = 50
    winning_percentage = base_percentage + total_weight * 100
    return min(winning_percentage, 100)  # Ensure it doesn't exceed 100%

def open_past_case_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return "No file selected."

    try:
        df = pd.read_csv(file_path)
        
        if not {'Case Type', 'Act', 'Case Date', 'Winner', 'Judgment'}.issubset(df.columns):
            return "CSV file does not contain the required columns."
        
        filtered_df = df[
            (df['Case Type'] == selected_case_type) & 
            (df['Act'] == commercial_acts[selected_case_type]["acts"][selected_act - 1])
        ]

        if filtered_df.empty:
            return "No relevant past cases found."

        result = "Relevant Past Cases:\n"
        for _, row in filtered_df.iterrows():
            result += f"Case Date: {row['Case Date']}, Winner: {row['Winner']}, Judgment: {row['Judgment']}\n"
        return result

    except Exception as e:
        return f"An error occurred: {e}"

def send_message():
    user_input = user_entry.get()
    chat_window.insert(tk.END, "You: " + user_input + "\n")
    chat_window.insert(tk.END, "Bot: " + chatbot_response(user_input) + "\n")
    user_entry.delete(0, tk.END)


app = tk.Tk()
app.title("Commercial Case Chatbot")


chat_window = scrolledtext.ScrolledText(app, width=50, height=20, wrap=tk.WORD)
chat_window.pack(pady=10)


user_entry = tk.Entry(app, width=40)
user_entry.pack(pady=5)


send_button = tk.Button(app, text="Send", command=send_message)
send_button.pack()


view_past_case_button = tk.Button(app, text="View Past Case", command=lambda: chat_window.insert(tk.END, "Bot: " + open_past_case_file() + "\n"))
view_past_case_button.pack(pady=5)


app.mainloop()
