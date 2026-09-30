import requests
import base64

api_key = input("Please enter your VirusTotal API key: ")
a = input("Please enter the url you'd like to analyze: ")
url_id = base64.urlsafe_b64encode(a.encode()).decode().strip("=")


headers = {

    "x-apikey": api_key
}
response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)

if response.status_code == 200:
    data = response.json()
    info = data["data"]["attributes"]["last_analysis_stats"]
    if info["malicious"] >= 3:
       risk_level = "HIGH"
       reason = "The number of malicious detections meets the threshold for a high risk classification."
       recommendation = "Do not visit this URL or enter any sensitive information."
    elif info["malicious"] > 0 or info["suspicious"] > 0:
        risk_level = "MEDIUM"
        reason="The URL received malicious or suspicious detections, but did not meet the high-risk threshold."
        recommendation = "Proceed with caution. Avoid entering sensitive information."
    else:
        risk_level = "LOW"
        reason ="No malicious or suspicious detections were reported."
        recommendation = "No significant threats were detected. Continue to use normal caution."


    print(f"\n{a} Analysis Completed.\n")
    print("Analysis Results:")

    print(f"Malicious: {info['malicious']}")
    print(f"Suspicious: {info['suspicious']}")
    print(f"Harmless: {info['harmless']}")
    print(f"Undetected: {info['undetected']}")

    if info["malicious"] > 0:
        print(f"{info['malicious']} security vendors flagged this URL as malicious.")
    if info["suspicious"] > 0:
        print(f"{info['suspicious']} security vendors flagged this URL as suspicious.")
    print(f"\nRisk Level: {risk_level}")
    print(f"Reason: {reason}")
    print(f"Recommendation: {recommendation}")
else:
    print("Error Code:", response.status_code)
    print("Error Message:", response.text)
